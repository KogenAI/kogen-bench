/* fxa.c - arm-a static twin of launcher_payload() in cmp.py.
 *
 * Replaces the bash bridge+script payload with one static libc-only launcher
 * (no /proc, no PATH lookups, no shell; execs absolute paths only).
 *   Stage 1: argv = [FXA, marker, delay, fx, mode, args...]  (argv[0] has '/')
 *            -> execve(argv[0], &argv[1]) so argv0 becomes the marker.
 *   Stage 2: argv = [marker, delay, fx, mode, args...]       (argv[0] no '/')
 *            mem_cap/pids_cap: fork holder + worker, wait worker, create the
 *            done file (delay), wait holder, exit worker rc.
 *            delay != "run": fork+wait fixture, sleep delay s, exit rc.
 *            else: execve fixture directly.
 *   Holder:  argv = [marker-holder], argc == 1 -> sleep 120 s, exit 0.
 * The holder re-execs this binary as dirname(fx)/fxa: fxa and fx live in the
 * same read-only folder, so no extra path has to be passed.
 * Known non-semantic differences from the bash wrapper:
 *   (1) no separate external `sleep` child in the survivor delay (the wrapper
 *       itself sleeps);
 *   (2) bash-added environment variables (PWD, SHLVL, _) are not added.
 */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

extern char **environ;

static void nap(unsigned long sec) {
    struct timespec ts;
    ts.tv_sec = (time_t)sec;
    ts.tv_nsec = 0;
    while (nanosleep(&ts, &ts) < 0 && errno == EINTR) { }
}

/* bash convention: 126 cannot execute, 127 not found / other failure */
static int exec_fail_code(void) {
    return (errno == EACCES || errno == ENOEXEC) ? 126 : 127;
}

static int wait_rc(pid_t pid) {
    int st;
    while (waitpid(pid, &st, 0) < 0) {
        if (errno != EINTR) return 127;
    }
    if (WIFEXITED(st)) return WEXITSTATUS(st);
    if (WIFSIGNALED(st)) return 128 + WTERMSIG(st);
    return 1;
}

static int parse_secs(const char *s, unsigned long *out) {
    unsigned long v = 0;
    if (*s == '\0') return -1;
    for (; *s; s++) {
        if (*s < '0' || *s > '9') return -1;
        v = v * 10UL + (unsigned long)(*s - '0');
        if (v > 1000000000UL) return -1;
    }
    *out = v;
    return 0;
}

/* Fixture child: argv0 = marker, then mode and args (cargv is prepared). */
static pid_t spawn_fx(const char *fx, char **cargv) {
    pid_t pid = fork();
    if (pid == 0) {
        execve(fx, cargv, environ);
        _exit(127);
    }
    return pid;
}

/* Holder child: exec dirname(fx)/fxa as [marker-holder] with CMPMARK replaced. */
static pid_t spawn_holder(const char *marker, const char *fx) {
    pid_t pid = fork();
    if (pid != 0) return pid;
    const char *slash = strrchr(fx, '/');
    if (slash == NULL) _exit(127);
    size_t ml = strlen(marker), dl = (size_t)(slash - fx) + 1, n = 0, i;
    while (environ[n] != NULL) n++;
    char **env = malloc((n + 2) * sizeof *env);
    char *mark = malloc(ml + 16);        /* "CMPMARK=" marker "-holder" NUL */
    char *path = malloc(dl + 4);         /* dirname + "/" + "fxa" NUL */
    if (env == NULL || mark == NULL || path == NULL) _exit(127);
    memcpy(mark, "CMPMARK=", 8);
    memcpy(mark + 8, marker, ml);
    memcpy(mark + 8 + ml, "-holder", 8);
    memcpy(path, fx, dl);
    memcpy(path + dl, "fxa", 4);
    int found = 0;
    for (i = 0; i < n; i++) {
        if (strncmp(environ[i], "CMPMARK=", 8) == 0) { env[i] = mark; found = 1; }
        else env[i] = environ[i];
    }
    if (!found) env[n++] = mark;
    env[n] = NULL;
    char *hargv[2] = { mark + 8, NULL };
    execve(path, hargv, env);
    _exit(127);
}

int main(int argc, char **argv) {
    if (argc < 1) return 125;
    size_t n0 = strlen(argv[0]);
    int has_slash = strchr(argv[0], '/') != NULL;
    if (!has_slash && argc == 1 && n0 >= 7 && strcmp(argv[0] + n0 - 7, "-holder") == 0) {
        nap(120);
        return 0;
    }
    if (has_slash) {                      /* stage 1: re-exec with argv0 = marker */
        if (argc < 5) return 125;
        execve(argv[0], &argv[1], environ);
        return exec_fail_code();
    }
    if (argc < 4) return 125;             /* stage 2: marker delay fx mode [args] */
    char *marker = argv[0], *delay = argv[1], *fx = argv[2], *mode = argv[3];
    argv[2] = marker;                     /* cargv = [marker, mode, args..., NULL] */
    char **cargv = &argv[2];
    if (strcmp(mode, "mem_cap") == 0 || strcmp(mode, "pids_cap") == 0) {
        pid_t holder = spawn_holder(marker, fx);
        if (holder < 0) return 125;
        pid_t worker = spawn_fx(fx, cargv);
        if (worker < 0) return 125;
        int rc = wait_rc(worker);
        int fd = open(delay, O_WRONLY | O_CREAT | O_TRUNC, 0666);   /* : > "$1" */
        if (fd >= 0) (void)close(fd);
        int st;
        while (waitpid(holder, &st, 0) < 0 && errno == EINTR) { }
        return rc;
    }
    if (strcmp(delay, "run") != 0) {
        unsigned long secs;
        if (parse_secs(delay, &secs) != 0) return 125;
        pid_t pid = spawn_fx(fx, cargv);
        if (pid < 0) return 125;
        int rc = wait_rc(pid);
        nap(secs);
        return rc;
    }
    execve(fx, cargv, environ);
    return exec_fail_code();
}
