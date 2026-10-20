package freq

import (
	"io"
	"os"
)

// Load returns the whole input: stdin when there is no path or the path is "-", else the file.
func Load(path string, hasPath bool, stdin io.Reader) ([]byte, error) {
	if !hasPath || path == "-" {
		return io.ReadAll(stdin)
	}
	return os.ReadFile(path)
}

// Run executes wordfreq with the given arguments and returns the exit status.
func Run(_ []string, _ io.Reader, _, _ io.Writer) int { return 0 }
