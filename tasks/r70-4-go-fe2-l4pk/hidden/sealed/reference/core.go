package main

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

const usage4 = "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n"

func git4(repo string, args ...string) (string, error) {
	cmd := exec.Command("git", append([]string{"-C", repo}, args...)...)
	out, err := cmd.Output()
	return strings.TrimSpace(string(out)), err
}

func land(args []string) (string, int, error) {
	values := map[string]string{}
	seen := map[string]bool{}
	allowed := map[string]bool{"--repo": true, "--target": true, "--base": true, "--candidate": true}
	for i := 0; i < len(args); i++ {
		key := args[i]
		if !allowed[key] || i+1 >= len(args) || seen[key] {
			return "", 2, errors.New(strings.TrimSuffix(usage4, "\n"))
		}
		i++
		values[key] = args[i]
		seen[key] = true
	}
	for key := range allowed {
		if values[key] == "" {
			return "", 2, errors.New(strings.TrimSuffix(usage4, "\n"))
		}
	}
	repo, target, base, cand := values["--repo"], values["--target"], values["--base"], values["--candidate"]
	parents, err := git4(repo, "rev-list", "--parents", "-n", "1", cand)
	parts := strings.Fields(parents)
	if err != nil || len(parts) != 2 || parts[1] != base {
		return "", 1, errors.New("cas-land: invalid repository or commit")
	}
	current, err := git4(repo, "rev-parse", "--verify", target)
	if err != nil || !strings.HasPrefix(target, "refs/") {
		return "", 1, errors.New("cas-land: invalid repository or commit")
	}
	newOID := cand
	rebased := current != base
	work := ""
	if rebased {
		work, err = os.MkdirTemp("", "cas-land-")
		if err != nil {
			return "", 1, errors.New("cas-land: invalid repository or commit")
		}
		defer func() { _ = os.RemoveAll(work) }()
		if _, err = git4(repo, "worktree", "add", "--detach", work, cand); err != nil {
			return "", 1, errors.New("cas-land: invalid repository or commit")
		}
		cmd := exec.Command("git", "-C", work, "rebase", "--onto", current, base)
		if output, rebaseErr := cmd.CombinedOutput(); rebaseErr != nil {
			unmerged, diffErr := git4(work, "diff", "--name-only", "--diff-filter=U")
			_ = exec.Command("git", "-C", work, "rebase", "--abort").Run()
			_ = exec.Command("git", "-C", repo, "worktree", "remove", "--force", work).Run()
			if diffErr == nil && unmerged != "" {
				return "", 20, errors.New("cas-land: conflict")
			}
			return "", 1, errors.New("cas-land: invalid repository or commit")
		} else if len(output) > 0 {
			_ = output
		}
		newOID, err = git4(work, "rev-parse", "HEAD")
		if err != nil {
			return "", 1, errors.New("cas-land: invalid repository or commit")
		}
		_ = exec.Command("git", "-C", repo, "worktree", "remove", "--force", work).Run()
	}
	if _, err = git4(repo, "update-ref", target, newOID, current); err != nil {
		return "", 30, errors.New("cas-land: lost race")
	}
	if rebased {
		return fmt.Sprintf("rebased %s\n", newOID), 10, nil
	}
	return fmt.Sprintf("landed %s\n", newOID), 0, nil
}

func execute(args []string) (string, int, error) { return land(args) }
