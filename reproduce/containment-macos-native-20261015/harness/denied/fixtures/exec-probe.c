/* Disallowed-exec helper: a native Mach-O the runner plants outside every
 * grant. It only writes the runner-supplied start witness. */
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    const char *path = getenv("CMPMAC_HELPER_WITNESS");
    if (path == NULL) return 3;
    int fd = open(path, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW, 0600);
    if (fd < 0) return 4;
    if (write(fd, "helper-start\n", 13) != 13) return 5;
    return close(fd) == 0 ? 0 : 6;
}
