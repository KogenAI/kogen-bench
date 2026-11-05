// Command kogen-b is arm B of Lab C1: a binary that links package verify (kogen-verification
// 3cb7305a plus c1-reaper-continuous.patch) so its init() can act as the acceptance-reaper helper.
package main

import (
	"fmt"
	"os"

	_ "github.com/KogenAI/kogen-verification/verify"
)

func main() {
	fmt.Fprintln(os.Stderr, "usage: kogen-b --kogen-verification-acceptance-reaper <script>")
	os.Exit(2)
}
