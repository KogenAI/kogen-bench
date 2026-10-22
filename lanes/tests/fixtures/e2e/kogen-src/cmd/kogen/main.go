// A stand-in Kogen for the end-to-end test: runs tests/fake-kogen in the mode compiled in here.
// A lane's patch changes `mode`. After `intent shape` it can lay a fixed Intent over the shaped one.
package main

import (
	"os"
	"os/exec"
	"path/filepath"
)

const mode = "correct"

func main() {
	args := os.Args[1:]
	py, _ := exec.LookPath("python3")
	cmd := exec.Command(py, append([]string{os.Getenv("FAKE_KOGEN_SCRIPT")}, args...)...)
	cmd.Env = append(os.Environ(), "FAKE_KOGEN_MODE="+mode)
	cmd.Stdin, cmd.Stdout, cmd.Stderr = os.Stdin, os.Stdout, os.Stderr
	code := 0
	if err := cmd.Run(); err != nil {
		code = 3
		if ee, ok := err.(*exec.ExitError); ok {
			code = ee.ExitCode()
		}
	}
	if from := os.Getenv("LANE_SHAPE_INTENT"); code == 0 && len(args) >= 3 && args[0] == "intent" && args[1] == "shape" && from != "" {
		for _, name := range []string{"intent.md", "acceptance.feature"} {
			data, err := os.ReadFile(filepath.Join(from, name))
			if err == nil {
				os.WriteFile(filepath.Join(".kogen", "intents", args[2], name), data, 0o644)
			}
		}
	}
	os.Exit(code)
}
