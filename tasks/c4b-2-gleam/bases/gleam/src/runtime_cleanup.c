/* Retire and reap the unused ERTS subprocess broker before running this
 * process-only CLI. All store operations use in-process OS facilities. */
#define _GNU_SOURCE
#include <erl_nif.h>
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
static ERL_NIF_TERM quiesce(ErlNifEnv *env,int argc,const ERL_NIF_TERM args[]) {
    (void)argc;(void)args;
    char path[128];snprintf(path,sizeof(path),"/proc/self/task/%ld/children",(long)getpid());
    FILE *children=fopen(path,"r");if(!children)return enif_make_atom(env,"error");
    long pid;
    while(fscanf(children,"%ld",&pid)==1) {
        snprintf(path,sizeof(path),"/proc/%ld/comm",pid);
        FILE *comm=fopen(path,"r");if(!comm)continue;
        char name[64];int match=fgets(name,sizeof(name),comm)!=NULL && strcmp(name,"erl_child_setup\n")==0;
        fclose(comm);
        if(match) {
            if(kill((pid_t)pid,SIGKILL)<0 && errno!=ESRCH){fclose(children);return enif_make_atom(env,"error");}
            int rc;do{rc=waitpid((pid_t)pid,NULL,0);}while(rc<0 && errno==EINTR);
            if(rc<0 && errno!=ECHILD){fclose(children);return enif_make_atom(env,"error");}
        }
    }
    fclose(children);return enif_make_atom(env,"nil");
}
static ErlNifFunc funcs[]={{"quiesce",0,quiesce,ERL_NIF_DIRTY_JOB_IO_BOUND}};
ERL_NIF_INIT(runtime_cleanup,funcs,NULL,NULL,NULL,NULL)
