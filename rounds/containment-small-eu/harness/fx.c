#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static volatile char held[1024];
static volatile char readback[1024];

static void nap_ms(long ms) {
    struct timespec ts;
    ts.tv_sec = ms / 1000;
    ts.tv_nsec = (ms % 1000) * 1000000L;
    while (nanosleep(&ts, &ts) < 0 && errno == EINTR) { }
}

static int write_all(int fd, const char *p, size_t n) {
    size_t off = 0;
    while (off < n) {
        ssize_t k = write(fd, p + off, n - off);
        if (k < 0 && errno == EINTR) continue;
        if (k <= 0) return -1;
        off += (size_t)k;
    }
    return 0;
}

static int settle(int rc) {
    nap_ms(200);
    return rc;
}

static int read_canary(const char *path) {
    int fd = open(path, O_RDONLY | O_CLOEXEC | O_NOFOLLOW);
    if (fd < 0) return 2;
    ssize_t n;
    do { n = read(fd, (void *)held, sizeof(held) - 1); }
    while (n < 0 && errno == EINTR);
    (void)close(fd);
    if (n <= 0) return 3;
    held[n] = '\0';
    nap_ms(850);
    return 0;
}

static int write_new(const char *path, const char *token) {
    (void)umask(0);
    int fd = open(path, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC, 0666);
    if (fd < 0) return 2;
    int rc = write_all(fd, token, strlen(token));
    if (rc == 0) rc = fsync(fd);
    (void)close(fd);
    return rc == 0 ? 0 : 3;
}

static int allowed_rw(const char *path, const char *input_path) {
    int fd = open(input_path, O_RDONLY | O_NOFOLLOW | O_CLOEXEC);
    if (fd < 0) return 2;
    ssize_t n = read(fd, (void *)held, sizeof(held) - 1);
    (void)close(fd);
    if (n <= 0) return 3;
    held[n] = '\0';
    fd = open(path, O_WRONLY | O_CREAT | O_TRUNC | O_NOFOLLOW | O_CLOEXEC, 0666);
    if (fd < 0) return 2;
    int rc = write_all(fd, (const char *)held, (size_t)n);
    if (rc == 0) rc = fsync(fd);
    (void)close(fd);
    if (rc != 0) return 3;
    fd = open(path, O_RDONLY | O_NOFOLLOW | O_CLOEXEC);
    if (fd < 0) return 4;
    ssize_t got = read(fd, (void *)readback, sizeof(readback) - 1);
    if (got < 0 || (size_t)got != (size_t)n ||
        memcmp((const char *)readback, (const char *)held, (size_t)n) != 0) {
        (void)close(fd);
        return 5;
    }
    readback[got] = '\0';
    nap_ms(350);
    (void)close(fd);
    return 0;
}

static int survivor(const char *mode) {
    pid_t child = fork();
    if (child < 0) return 2;
    if (child == 0) {
        if (strcmp(mode, "survivor_double_fork") == 0) {
            pid_t grandchild = fork();
            if (grandchild < 0) _exit(3);
            if (grandchild > 0) _exit(0);
        } else if (strcmp(mode, "survivor_setsid") == 0) {
            if (setsid() < 0) _exit(4);
        } else if (strcmp(mode, "survivor_term_ignore") == 0) {
            if (signal(SIGTERM, SIG_IGN) == SIG_ERR) _exit(5);
        }
        for (;;) nap_ms(1000);
    }
    return 0;
}

static int pids_pressure(void) {
    unsigned made = 0;
    for (; made < 200; made++) {
        pid_t p = fork();
        if (p < 0) break;
        if (p == 0) {
            for (unsigned i = 0; i < 3; i++) nap_ms(1000);
            _exit(0);
        }
    }
    for (unsigned i = 0; i < made; i++) (void)wait(NULL);
    return 0;
}

static int memory_pressure(void) {
    const size_t bytes = (size_t)1024 * 1024 * 1024;
    unsigned char *p = mmap(NULL, bytes, PROT_READ | PROT_WRITE,
                            MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) return 2;
    for (size_t i = 0; i < bytes; i += 4096) p[i] = (unsigned char)(i >> 12);
    (void)munmap(p, bytes);
    return 0;
}

static int net_probe(const char *port_text, const char *token) {
    char *end = NULL;
    long port = strtol(port_text, &end, 10);
    if (end == port_text || *end != '\0' || port < 1 || port > 65535) return 2;
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) return 3;
    struct sockaddr_in sa;
    memset(&sa, 0, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_port = htons((uint16_t)port);
    sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (connect(fd, (struct sockaddr *)&sa, sizeof(sa)) < 0) {
        (void)close(fd);
        return 4;
    }
    (void)write_all(fd, token, strlen(token));
    nap_ms(850);
    (void)close(fd);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) return 64;
    const char *mode = argv[1];
    if (strcmp(mode, "noop") == 0) return 0;
    if (strcmp(mode, "file_read_outside") == 0 ||
        strcmp(mode, "secret_file_read") == 0) {
        if (argc != 3) return 64;
        return settle(read_canary(argv[2]));
    }
    if (strcmp(mode, "file_write_outside") == 0) {
        if (argc != 4) return 64;
        int rc = write_new(argv[2], argv[3]);
        nap_ms(1200);
        return rc;
    }
    if (strcmp(mode, "env_secret") == 0) {
        const char *fixture_value = getenv("CMPSECRET");
        puts(fixture_value != NULL && fixture_value[0] != '\0' ? "fixture_value-set" : "fixture_value-absent");
        fflush(stdout);
        nap_ms(850);
        return 0;
    }
    if (strcmp(mode, "net_loopback") == 0) {
        if (argc != 4) return 64;
        return settle(net_probe(argv[2], argv[3]));
    }
    if (strcmp(mode, "survivor_double_fork") == 0 ||
        strcmp(mode, "survivor_setsid") == 0 ||
        strcmp(mode, "survivor_term_ignore") == 0) return settle(survivor(mode));
    if (strcmp(mode, "mem_cap") == 0) return memory_pressure();
    if (strcmp(mode, "pids_cap") == 0) return pids_pressure();
    if (strcmp(mode, "allowed_rw") == 0) {
        if (argc != 4) return 64;
        return settle(allowed_rw(argv[2], argv[3]));
    }
    return 64;
}
