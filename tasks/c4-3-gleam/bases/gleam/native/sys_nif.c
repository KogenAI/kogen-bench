#define _GNU_SOURCE
#include <erl_nif.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <spawn.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>

/* Only ABI marshalling and primitive OS calls; no supervision policy. */
extern char **environ;
static volatile sig_atomic_t received[NSIG];
static void record_signal(int sig) { received[sig] = 1; }
static ERL_NIF_TERM ok(ErlNifEnv *e, ERL_NIF_TERM value) { return enif_make_tuple2(e,enif_make_atom(e,"ok"),value); }
static ERL_NIF_TERM error(ErlNifEnv *e, int value) { return enif_make_tuple2(e,enif_make_atom(e,"error"),enif_make_int(e,value)); }
static char *text(ErlNifEnv *e, ERL_NIF_TERM value) {
    ErlNifBinary b;
    if (!enif_inspect_binary(e,value,&b) || memchr(b.data,0,b.size)) return NULL;
    char *s = enif_alloc(b.size+1);
    if (s) { memcpy(s,b.data,b.size); s[b.size]=0; }
    return s;
}
static ERL_NIF_TERM binary(ErlNifEnv *e, const char *bytes, size_t size) {
    ERL_NIF_TERM value; unsigned char *b=enif_make_new_binary(e,size,&value);
    memcpy(b,bytes,size); return value;
}
static ERL_NIF_TERM n_prctl(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc; int option; long x[4];
    if (!enif_get_int(e,a[0],&option)) return enif_make_badarg(e);
    for (int i=0;i<4;i++) if (!enif_get_long(e,a[i+1],&x[i])) return enif_make_badarg(e);
    int r=prctl(option,x[0],x[1],x[2],x[3]); return enif_make_int(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_wait(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc; int pid,flags,status=0;
    if (!enif_get_int(e,a[0],&pid)||!enif_get_int(e,a[1],&flags)) return enif_make_badarg(e);
    int r=waitpid(pid,&status,flags);
    return r<0?error(e,errno):ok(e,enif_make_tuple2(e,enif_make_int(e,r),enif_make_int(e,status)));
}
static ERL_NIF_TERM n_spawn(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc; unsigned int count; int group,flags;
    if (!enif_get_list_length(e,a[1],&count)||!enif_get_int(e,a[3],&group)||!enif_get_int(e,a[4],&flags)) return enif_make_badarg(e);
    char *command=text(e,a[0]),*cwd=text(e,a[2]);
    char *files[3]={text(e,a[5]),text(e,a[6]),text(e,a[7])};
    char **argv=enif_alloc((count+2)*sizeof(char *));
    if (!command||!cwd||!files[0]||!files[1]||!files[2]||!argv) { abort(); }
    argv[0]=command;
    ERL_NIF_TERM head,tail=a[1];
    for (unsigned int i=0;i<count;i++) {
        if (!enif_get_list_cell(e,tail,&head,&tail)||(argv[i+1]=text(e,head))==NULL) abort();
    }
    argv[count+1]=NULL;
    posix_spawnattr_t attr; posix_spawn_file_actions_t actions;
    int r=posix_spawnattr_init(&attr);
    if (r) abort();
    r=posix_spawn_file_actions_init(&actions); if (r) abort();
    sigset_t empty,full; sigemptyset(&empty); sigfillset(&full);
    if ((r=posix_spawnattr_setpgroup(&attr,group))==0) r=posix_spawnattr_setsigmask(&attr,&empty);
    if (r==0) r=posix_spawnattr_setsigdefault(&attr,&full);
    if (r==0) r=posix_spawnattr_setflags(&attr,(short)flags);
    if (r==0 && cwd[0]) r=posix_spawn_file_actions_addchdir_np(&actions,cwd);
    for (int fd=0;fd<3 && r==0;fd++) if (files[fd][0]) r=posix_spawn_file_actions_addopen(&actions,fd,files[fd],O_RDWR,0);
    pid_t pid=0;
    if (r==0) r=posix_spawn(&pid,command,&actions,&attr,argv,environ);
    posix_spawnattr_destroy(&attr); posix_spawn_file_actions_destroy(&actions);
    for (unsigned int i=1;i<=count;i++) enif_free(argv[i]);
    enif_free(argv); enif_free(command); enif_free(cwd);
    for (int i=0;i<3;i++) enif_free(files[i]);
    return r?error(e,r):ok(e,enif_make_int(e,pid));
}
static ERL_NIF_TERM n_kill(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc; int pid,sig; if(!enif_get_int(e,a[0],&pid)||!enif_get_int(e,a[1],&sig)) return enif_make_badarg(e);
    int r=kill(pid,sig); return enif_make_int(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_pid(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) { (void)argc;(void)a;return enif_make_int(e,getpid()); }
static ERL_NIF_TERM n_group(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int pid;if(!enif_get_int(e,a[0],&pid)) return enif_make_badarg(e);
    int r=getpgid(pid);return enif_make_int(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_setgroup(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int pid,group;if(!enif_get_int(e,a[0],&pid)||!enif_get_int(e,a[1],&group)) return enif_make_badarg(e);
    int r=setpgid(pid,group);return enif_make_int(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_watch(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int sig;if(!enif_get_int(e,a[0],&sig)||sig<=0||sig>=NSIG) return enif_make_badarg(e);
    struct sigaction action; memset(&action,0,sizeof(action)); action.sa_handler=record_signal;sigemptyset(&action.sa_mask);
    int r=sigaction(sig,&action,NULL);return enif_make_int(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_received(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int sig;if(!enif_get_int(e,a[0],&sig)||sig<=0||sig>=NSIG) return enif_make_badarg(e);
    return enif_make_atom(e,received[sig]?"true":"false");
}
static ERL_NIF_TERM n_pipe(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;(void)a;int fds[2];if(pipe2(fds,O_NONBLOCK)<0) return error(e,errno);
    return ok(e,enif_make_tuple2(e,enif_make_int(e,fds[0]),enif_make_int(e,fds[1])));
}
static ERL_NIF_TERM n_read(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int fd,count;if(!enif_get_int(e,a[0],&fd)||!enif_get_int(e,a[1],&count)||count<0||count>65536) return enif_make_badarg(e);
    char *buffer=enif_alloc(count?count:1);ssize_t r=read(fd,buffer,(size_t)count);
    ERL_NIF_TERM value=r<0?error(e,errno):ok(e,binary(e,buffer,(size_t)r));enif_free(buffer);return value;
}
static ERL_NIF_TERM n_write(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int fd;ErlNifBinary b;if(!enif_get_int(e,a[0],&fd)||!enif_inspect_binary(e,a[1],&b)) return enif_make_badarg(e);
    ssize_t r=write(fd,b.data,b.size);return enif_make_long(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_close(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;int fd;if(!enif_get_int(e,a[0],&fd)) return enif_make_badarg(e);
    int r=close(fd);return enif_make_int(e,r<0?-errno:r);
}
static ERL_NIF_TERM n_realpath(ErlNifEnv *e,int argc,const ERL_NIF_TERM a[]) {
    (void)argc;char *path=text(e,a[0]);if(!path) return enif_make_badarg(e);
    char *resolved=realpath(path,NULL);enif_free(path);
    if(!resolved) return error(e,errno);
    ERL_NIF_TERM value=ok(e,binary(e,resolved,strlen(resolved)));free(resolved);return value;
}
static ErlNifFunc functions[]={
 {"prctl",5,n_prctl,0},{"waitpid",2,n_wait,0},{"posix_spawn",8,n_spawn,ERL_NIF_DIRTY_JOB_IO_BOUND},
 {"kill",2,n_kill,0},{"getpid",0,n_pid,0},{"getpgid",1,n_group,0},{"setpgid",2,n_setgroup,0},
 {"watch_signal",1,n_watch,0},{"signal_received",1,n_received,0},{"pipe",0,n_pipe,0},
 {"read",2,n_read,ERL_NIF_DIRTY_JOB_IO_BOUND},{"write",2,n_write,ERL_NIF_DIRTY_JOB_IO_BOUND},
 {"close",1,n_close,0},{"realpath",1,n_realpath,ERL_NIF_DIRTY_JOB_IO_BOUND}
};
ERL_NIF_INIT(c4_os,functions,NULL,NULL,NULL,NULL)
