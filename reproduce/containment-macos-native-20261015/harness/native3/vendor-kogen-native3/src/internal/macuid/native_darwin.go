//go:build darwin && cgo

package macuid

/*
#cgo LDFLAGS: -lproc
#include <libproc.h>
#include <sys/sysctl.h>
#include <sys/proc_info.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// KERN_PROC_UID and KERN_PROC_RUID cover both effective and real membership.
// sysctl's successful zero-byte result distinguishes empty from observation loss.
// Never accept an oversized/truncated list as an empty or complete scan.
static int mu_pids(uint32_t uid, int flavor, int *out, int capacity, int *count) {
    int mib[4] = {CTL_KERN, KERN_PROC, flavor, (int)uid};
    size_t n = 0;
    if (sysctl(mib, 4, NULL, &n, NULL, 0)) return errno;
    if (n > (size_t)capacity * sizeof(struct kinfo_proc)) return EOVERFLOW;
    size_t cap = (size_t)capacity * sizeof(struct kinfo_proc);
    struct kinfo_proc *buf = calloc(1, cap);
    if (!buf) return ENOMEM;
    n = cap;
    if (sysctl(mib, 4, buf, &n, NULL, 0)) { int e = errno; free(buf); return e; }
    if (n % sizeof(struct kinfo_proc) || n >= cap) { free(buf); return EOVERFLOW; }
    *count = (int)(n / sizeof(struct kinfo_proc));
    for (int i = 0; i < *count; ++i) out[i] = buf[i].kp_proc.p_pid;
    free(buf);
    return 0;
}
static int mu_info(int pid, struct proc_bsdinfo *b) {
    errno = 0;
    int n = proc_pidinfo(pid, PROC_PIDTBSDINFO, 0, b, sizeof(*b));
    return n == sizeof(*b) ? 0 : (errno ? errno : EIO);
}
static int mu_usage(int pid, struct rusage_info_v2 *r) {
    errno = 0;
    return proc_pid_rusage(pid, RUSAGE_INFO_V2, (rusage_info_t *)r) ? (errno ? errno : EIO) : 0;
}
static int mu_threads(int pid, uint64_t *out) {
    struct proc_taskinfo b;
    errno = 0;
    int n = proc_pidinfo(pid, PROC_PIDTASKINFO, 0, &b, sizeof(b));
    if (n != sizeof(b)) return errno ? errno : EIO;
    *out = b.pti_threadnum;
    return 0;
}
static int mu_boot(char *buf, size_t capacity) {
    size_t n = capacity;
    return sysctlbyname("kern.bootsessionuuid", buf, &n, NULL, 0) ? errno : 0;
}
static int mu_peer(int fd, uint32_t *uid, uint32_t *gid) {
    uid_t u; gid_t g;
    if (getpeereid(fd, &u, &g)) return errno;
    *uid = u; *gid = g; return 0;
}
*/
import "C"

import (
	"context"
	"fmt"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
	"time"
	"unsafe"
)

type NativeTable struct {
	uid, gid     uint32
	helper, boot string
}

func NewNativeTable(uid, gid uint32, helper string) (*NativeTable, error) {
	if uid < 501 || gid < 501 || !pathOK(helper) {
		return nil, fmt.Errorf("reserved UID/GID and absolute trusted helper required")
	}
	var boot [128]C.char
	if err := C.mu_boot(&boot[0], C.size_t(len(boot))); err != 0 {
		return nil, fmt.Errorf("boot incarnation unavailable: %w", syscall.Errno(err))
	}
	identity := C.GoString(&boot[0])
	if identity == "" {
		return nil, ErrObservation
	}
	return &NativeTable{uid: uid, gid: gid, helper: helper, boot: identity}, nil
}

func (t *NativeTable) Snapshot(ctx context.Context, uid uint32) ([]Process, error) {
	if uid != t.uid {
		return nil, fmt.Errorf("unregistered UID")
	}
	pids := map[int]bool{}
	for _, flavor := range []C.int{C.KERN_PROC_UID, C.KERN_PROC_RUID} {
		if err := ctx.Err(); err != nil {
			return nil, err
		}
		buf := make([]C.int, MaxRecords+1)
		var count C.int
		if err := C.mu_pids(C.uint32_t(uid), flavor, (*C.int)(unsafe.Pointer(&buf[0])), C.int(len(buf)), &count); err != 0 {
			return nil, fmt.Errorf("UID enumeration unavailable: %w", syscall.Errno(err))
		}
		for _, pid := range buf[:int(count)] {
			if pid > 0 {
				pids[int(pid)] = true
			}
		}
	}
	if len(pids) > MaxRecords {
		return nil, ErrObservation
	}
	ps := []Process{}
	var fault error
	for pid := range pids {
		if err := ctx.Err(); err != nil {
			return ps, err
		}
		var before, after C.struct_proc_bsdinfo
		if err := C.mu_info(C.int(pid), &before); err != 0 {
			fault = ErrObservation
			continue
		}
		if uint32(before.pbi_uid) != uid && uint32(before.pbi_ruid) != uid {
			fault = ErrObservation
			continue
		}
		p := Process{PID: pid, UID: uint32(before.pbi_uid), RealUID: uint32(before.pbi_ruid), Identity: fmt.Sprintf("darwin:%s:%d:%d.%d", t.boot, pid, uint64(before.pbi_start_tvsec), uint64(before.pbi_start_tvusec)), Zombie: before.pbi_status == 5}
		var usage C.struct_rusage_info_v2
		if err := C.mu_usage(C.int(pid), &usage); err != 0 {
			// Zombies cannot run, but their final CPU is unavailable to this sampler.
			if !p.Zombie {
				fault = ErrObservation
			}
		} else {
			p.RSS = uint64(usage.ri_resident_size)
			u, k := uint64(usage.ri_user_time), uint64(usage.ri_system_time)
			if ^uint64(0)-u < k {
				return ps, ErrObservation
			}
			p.CPU = u + k
		}
		if !p.Zombie {
			var threads C.uint64_t
			if err := C.mu_threads(C.int(pid), &threads); err != 0 {
				fault = ErrObservation
			} else {
				p.Threads = uint64(threads)
			}
		}
		if err := C.mu_info(C.int(pid), &after); err != 0 || before.pbi_start_tvsec != after.pbi_start_tvsec || before.pbi_start_tvusec != after.pbi_start_tvusec || before.pbi_uid != after.pbi_uid || before.pbi_ruid != after.pbi_ruid {
			fault = ErrObservation
			continue
		}
		ps = append(ps, p)
	}
	return ps, fault
}

// The short-lived signal helper drops all root credentials and supplementary
// groups BEFORE kill(-1). Permission checks happen in the kernel, so a PID reuse
// race cannot make the root custodian signal an unrelated different-UID process.
// UID membership is exclusive to one lease. This is not an arbitrary-PID API.
func (t *NativeTable) SignalUID(ctx context.Context, uid uint32, sig Signal) error {
	if uid != t.uid || (sig != Term && sig != Kill) {
		return fmt.Errorf("unregistered UID or signal")
	}
	if os.Geteuid() != 0 {
		return fmt.Errorf("root launchd custodian required")
	}
	cmd := exec.CommandContext(ctx, t.helper, "--macuid-signal", string(sig), strconv.FormatUint(uint64(uid), 10))
	cmd.Env = []string{}
	cmd.SysProcAttr = &syscall.SysProcAttr{Credential: &syscall.Credential{Uid: t.uid, Gid: t.gid, Groups: []uint32{}}, Setsid: true}
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("credential-scoped signal helper failed: %w", err)
	}
	return nil
}

func SignalRole(args []string) (bool, error) {
	if len(args) == 0 || (args[0] != "--macuid-signal" && args[0] != "--macuid-signal-group") {
		return false, nil
	}
	group := args[0] == "--macuid-signal-group"
	if (!group && len(args) != 3) || (group && len(args) != 4) {
		return true, fmt.Errorf("invalid signal role")
	}
	uid, err := strconv.ParseUint(args[2], 10, 32)
	if err != nil || uid < 501 || os.Getuid() != int(uid) || os.Geteuid() != int(uid) {
		return true, fmt.Errorf("signal role requires dropped reserved credentials")
	}
	var sig syscall.Signal
	switch args[1] {
	case string(Term):
		sig = syscall.SIGTERM
	case string(Kill):
		sig = syscall.SIGKILL
	default:
		return true, fmt.Errorf("invalid custody signal")
	}
	target := -1
	if group {
		pgid, perr := strconv.ParseUint(args[3], 10, 31)
		if perr != nil || pgid < 2 {
			return true, fmt.Errorf("invalid process group")
		}
		target = -int(pgid)
	}
	err = syscall.Kill(target, sig)
	if err == syscall.ESRCH {
		err = nil
	}
	return true, err
}

type NativeAccounts struct{}

func (NativeAccounts) Lookup(name string) (Account, error) {
	if strings.ContainsAny(name, "/\x00") || !strings.HasPrefix(name, "_kogen_build_") {
		return Account{}, fmt.Errorf("invalid local account")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	query := func(path string, args ...string) ([]byte, error) {
		cmd := exec.CommandContext(ctx, path, args...)
		cmd.Env = []string{}
		return cmd.Output()
	}
	b, err := query("/usr/bin/dscl", "/Local/Default", "-read", "/Users/"+name)
	if err != nil {
		return Account{}, err
	}
	fields, err := directoryFields(string(b))
	if err != nil {
		return Account{}, err
	}
	a, err := directoryAccount(name, fields)
	if err != nil {
		return Account{}, err
	}
	gb, err := query("/usr/bin/id", "-G", name)
	if err != nil {
		return Account{}, err
	}
	for _, v := range strings.Fields(string(gb)) {
		n, err := strconv.ParseUint(v, 10, 32)
		if err != nil {
			return Account{}, err
		}
		a.Groups = append(a.Groups, uint32(n))
	}
	// Read every local group, not just id's cached memberships. Missing GUIDs,
	// dangling nesting, duplicate identities and all cycles fail in CheckAccount.
	names, err := query("/usr/bin/dscl", "/Local/Default", "-list", "/Groups")
	if err != nil {
		return Account{}, err
	}
	for _, groupName := range strings.Split(strings.TrimSuffix(string(names), "\n"), "\n") {
		if groupName == "" || strings.ContainsAny(groupName, "/\x00") {
			return Account{}, fmt.Errorf("invalid group name")
		}
		b, err := query("/usr/bin/dscl", "/Local/Default", "-read", "/Groups/"+groupName)
		if err != nil {
			return Account{}, err
		}
		fields, err := directoryFields(string(b))
		if err != nil {
			return Account{}, err
		}
		group, err := directoryGroup(groupName, fields)
		if err != nil {
			return Account{}, err
		}
		a.LocalGroups = append(a.LocalGroups, group)
	}

	return a, nil
}

func PeerUID(conn *net.UnixConn) (uint32, error) {
	raw, err := conn.SyscallConn()
	if err != nil {
		return 0, err
	}
	var uid, gid C.uint32_t
	var e C.int
	err = raw.Control(func(fd uintptr) { e = C.mu_peer(C.int(fd), &uid, &gid) })
	if err != nil {
		return 0, err
	}
	if e != 0 {
		return 0, syscall.Errno(e)
	}
	return uint32(uid), nil
}
