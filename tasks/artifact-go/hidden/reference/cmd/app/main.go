package main

import (
	"os"

	"wordfreq/freq"
)

func main() {
	os.Exit(freq.Run(os.Args[1:], os.Stdin, os.Stdout, os.Stderr))
}
