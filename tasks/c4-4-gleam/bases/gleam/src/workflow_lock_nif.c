#define _GNU_SOURCE
#include <erl_nif.h>
#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <unistd.h>

typedef struct {
  int fd;
} lock_resource;

static ErlNifResourceType *lock_type;
static ERL_NIF_TERM atom_ok;
static ERL_NIF_TERM atom_error;
static ERL_NIF_TERM atom_nil;

static void lock_destructor(ErlNifEnv *env, void *object) {
  (void)env;
  lock_resource *lock = object;
  if (lock->fd >= 0) {
    (void)close(lock->fd);
    lock->fd = -1;
  }
}

static ERL_NIF_TERM failure(ErlNifEnv *env) {
  return enif_make_tuple2(env, atom_error, atom_nil);
}

static int copy_path(ErlNifEnv *env, ERL_NIF_TERM term, char **path) {
  ErlNifBinary binary;
  if (!enif_inspect_binary(env, term, &binary) ||
      memchr(binary.data, '\0', binary.size) != NULL) {
    return 0;
  }
  *path = enif_alloc(binary.size + 1);
  if (*path == NULL) return 0;
  memcpy(*path, binary.data, binary.size);
  (*path)[binary.size] = '\0';
  return 1;
}

static ERL_NIF_TERM lock_exclusive(ErlNifEnv *env, int argc,
                                   const ERL_NIF_TERM argv[]) {
  (void)argc;
  char *path = NULL;
  if (!copy_path(env, argv[0], &path)) return failure(env);

  int fd = open(path, O_CREAT | O_RDWR | O_CLOEXEC, 0600);
  enif_free(path);
  if (fd < 0) return failure(env);

  struct stat metadata;
  if (fstat(fd, &metadata) != 0 || !S_ISREG(metadata.st_mode)) {
    (void)close(fd);
    return failure(env);
  }

  int result;
  do {
    result = flock(fd, LOCK_EX);
  } while (result < 0 && errno == EINTR);
  if (result < 0) {
    (void)close(fd);
    return failure(env);
  }

  lock_resource *lock = enif_alloc_resource(lock_type, sizeof(*lock));
  if (lock == NULL) {
    (void)close(fd);
    return failure(env);
  }
  lock->fd = fd;
  ERL_NIF_TERM resource = enif_make_resource(env, lock);
  enif_release_resource(lock);
  return enif_make_tuple2(env, atom_ok, resource);
}

static ERL_NIF_TERM release_lock(ErlNifEnv *env, int argc,
                                 const ERL_NIF_TERM argv[]) {
  (void)argc;
  lock_resource *lock = NULL;
  if (!enif_get_resource(env, argv[0], lock_type, (void **)&lock)) {
    return failure(env);
  }
  if (lock->fd >= 0) {
    int fd = lock->fd;
    lock->fd = -1;
    if (close(fd) != 0 && errno != EINTR) return failure(env);
  }
  return atom_nil;
}

static ERL_NIF_TERM fsync_directory(ErlNifEnv *env, int argc,
                                    const ERL_NIF_TERM argv[]) {
  (void)argc;
  char *path = NULL;
  if (!copy_path(env, argv[0], &path)) return failure(env);
  int fd = open(path, O_RDONLY | O_DIRECTORY | O_CLOEXEC);
  enif_free(path);
  if (fd < 0) return failure(env);
  int result;
  do {
    result = fsync(fd);
  } while (result < 0 && errno == EINTR);
  int close_result = close(fd);
  if (result != 0 || (close_result != 0 && errno != EINTR)) return failure(env);
  return atom_ok;
}

static int load(ErlNifEnv *env, void **private_data, ERL_NIF_TERM load_info) {
  (void)private_data;
  (void)load_info;
  atom_ok = enif_make_atom(env, "ok");
  atom_error = enif_make_atom(env, "error");
  atom_nil = enif_make_atom(env, "nil");
  lock_type = enif_open_resource_type(env, NULL, "workflow_flock_resource",
                                      lock_destructor, ERL_NIF_RT_CREATE, NULL);
  return lock_type == NULL ? -1 : 0;
}

static ErlNifFunc functions[] = {
    {"lock_exclusive", 1, lock_exclusive, ERL_NIF_DIRTY_JOB_IO_BOUND},
    {"release_lock", 1, release_lock, 0},
    {"fsync_directory", 1, fsync_directory, ERL_NIF_DIRTY_JOB_IO_BOUND},
};

ERL_NIF_INIT(workflow_os, functions, load, NULL, NULL, NULL)
