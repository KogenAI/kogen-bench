#define _GNU_SOURCE
#include <dirent.h>
#include <errno.h>
#include <limits.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#include "erl_nif.h"

static ERL_NIF_TERM atom_true;
static ERL_NIF_TERM atom_false;

static int is_child_setup(pid_t pid) {
  char path[64];
  char comm[64];
  char status_line[256];
  long parent = -1;

  if (snprintf(path, sizeof(path), "/proc/%ld/comm", (long)pid) >= (int)sizeof(path)) return 0;
  FILE *file = fopen(path, "r");
  if (file == NULL) return 0;
  int matching_name = fgets(comm, sizeof(comm), file) != NULL &&
                      strcmp(comm, "erl_child_setup\n") == 0;
  fclose(file);
  if (!matching_name) return 0;

  if (snprintf(path, sizeof(path), "/proc/%ld/status", (long)pid) >= (int)sizeof(path)) return 0;
  file = fopen(path, "r");
  if (file == NULL) return 0;
  while (fgets(status_line, sizeof(status_line), file) != NULL) {
    if (strncmp(status_line, "PPid:", 5) == 0) {
      (void)sscanf(status_line + 5, "%ld", &parent);
      break;
    }
  }
  fclose(file);
  return parent == (long)getpid();
}

static int find_child_setup(pid_t *pids, size_t capacity) {
  DIR *tasks = opendir("/proc/self/task");
  if (tasks == NULL) return -1;
  size_t count = 0;
  struct dirent *task;
  while ((task = readdir(tasks)) != NULL) {
    char *end = NULL;
    (void)strtol(task->d_name, &end, 10);
    if (end == task->d_name || *end != '\0') continue;

    char path[128];
    if (snprintf(path, sizeof(path), "/proc/self/task/%s/children", task->d_name) >= (int)sizeof(path)) {
      closedir(tasks);
      return -1;
    }
    FILE *file = fopen(path, "r");
    if (file == NULL) continue;
    long child;
    while (fscanf(file, "%ld", &child) == 1) {
      if (child <= 0 || child > INT_MAX || !is_child_setup((pid_t)child)) continue;
      int duplicate = 0;
      for (size_t i = 0; i < count; i++) {
        if (pids[i] == (pid_t)child) duplicate = 1;
      }
      if (!duplicate) {
        if (count == capacity) {
          fclose(file);
          closedir(tasks);
          return -1;
        }
        pids[count++] = (pid_t)child;
      }
    }
    fclose(file);
  }
  closedir(tasks);
  return (int)count;
}

static int signal_child_setup(pid_t pid) {
#if defined(SYS_pidfd_open) && defined(SYS_pidfd_send_signal)
  int pidfd = (int)syscall(SYS_pidfd_open, pid, 0);
  if (pidfd >= 0) {
    if (!is_child_setup(pid)) {
      close(pidfd);
      return 1;
    }
    int result = (int)syscall(SYS_pidfd_send_signal, pidfd, SIGKILL, NULL, 0);
    int saved_errno = errno;
    close(pidfd);
    return result == 0 || saved_errno == ESRCH;
  }
  if (errno != ENOSYS && errno != EINVAL) return errno == ESRCH;
#endif
  if (!is_child_setup(pid)) return 1;
  return kill(pid, SIGKILL) == 0 || errno == ESRCH;
}

static uint64_t monotonic_ms(void) {
  struct timespec now;
  if (clock_gettime(CLOCK_MONOTONIC, &now) != 0) return 0;
  return (uint64_t)now.tv_sec * 1000 + (uint64_t)now.tv_nsec / 1000000;
}

static void sleep_ms(long milliseconds) {
  struct timespec delay = {milliseconds / 1000, (milliseconds % 1000) * 1000000};
  while (nanosleep(&delay, &delay) != 0 && errno == EINTR) {
  }
}

static ERL_NIF_TERM prepare_shutdown(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[]) {
  (void)env;
  (void)argc;
  (void)argv;
  uint64_t deadline = monotonic_ms() + 3000;
  for (;;) {
    pid_t helpers[32];
    int count = find_child_setup(helpers, sizeof(helpers) / sizeof(helpers[0]));
    if (count < 0) return atom_false;
    if (count == 0) return atom_true;
    for (int i = 0; i < count; i++) {
      if (!signal_child_setup(helpers[i])) return atom_false;
    }
    if (monotonic_ms() >= deadline) return atom_false;
    sleep_ms(5);
  }
}

static int load(ErlNifEnv *env, void **priv_data, ERL_NIF_TERM load_info) {
  (void)priv_data;
  (void)load_info;
  atom_true = enif_make_atom(env, "true");
  atom_false = enif_make_atom(env, "false");
  return 0;
}

static ErlNifFunc functions[] = {
    {"prepare_shutdown_nif", 0, prepare_shutdown, ERL_NIF_DIRTY_JOB_IO_BOUND},
};

ERL_NIF_INIT(approval_io, functions, load, NULL, NULL, NULL)
