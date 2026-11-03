package conformance

import (
	"context"
	"crypto/sha256"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"kogen-loop/api"
	"kogen-loop/loop"
)

// Scripted sessions; each records every provider request body (root/home/tmp normalised).
func TestL1RequestBytes(t *testing.T) {
	sessions := map[string][]map[string]any{
		"toolerror": {
			call("a1", "read_file", map[string]any{"path": "gone.txt"}),
			call("a2", "read_file", map[string]any{"path": "dir"}),
			call("a3", "read_file", map[string]any{"path": "../x"}),
			call("a4", "write_file", map[string]any{"path": "guard.txt", "content": "x"}),
			call("a5", "shell", map[string]any{"handle": "nope"}),
			call("a6", "shell", map[string]any{"command": "pkill -f nothing-at-all"}),
			call("a7", "view_image", map[string]any{"path": "bad.png"}),
			call("a8", "list_files", map[string]any{"path": "~"}),
			call("a9", "search_text", map[string]any{"pattern": "a", "path": "a.txt/x"}),
		},
		"malformed": {
			call("b1", "delete_file", map[string]any{"path": "a.txt"}),
			call("b2", "read_file", map[string]any{}),
			call("b3", "read_file", map[string]any{"path": nil}),
			call("b4", "write_file", map[string]any{"path": "b.txt"}),
			call("b5", "write_file", map[string]any{"path": "b.txt", "content": 7}),
			call("b6", "search_text", map[string]any{}),
			call("b7", "view_image", map[string]any{}),
			call("b8", "view_image", map[string]any{"path": 3}),
			call("b9", "shell", map[string]any{"command": "echo a", "handle": "h"}),
			call("ba", "shell", map[string]any{}),
			call("bb", "shell", map[string]any{"command": 5}),
		},
		"mixed-ok": {
			call("c1", "read_file", map[string]any{"path": "a.txt"}),
			call("c2", "write_file", map[string]any{"path": "n.txt", "content": "hi"}),
			call("c3", "shell", map[string]any{"command": "exit 3"}),
			call("c4", "list_files", map[string]any{}),
			call("c5", "read_file", map[string]any{"path": "missing"}),
		},
	}
	// each session also run as one call per exchange, to give several request bodies
	for _, split := range []bool{false, true} {
		for name, items := range sessions {
			label := fmt.Sprintf("%s-split=%v", name, split)
			w := newWorld(t).signIn()
			for n, c := range map[string]string{"a.txt": "alpha\n", "bad.png": "not a png"} {
				_ = os.WriteFile(filepath.Join(w.root, n), []byte(c), 0o644)
			}
			_ = os.Mkdir(filepath.Join(w.root, "dir"), 0o755)
			var ex []exchange
			if split {
				for _, it := range items {
					ex = append(ex, exchange{ID: "r", Items: []map[string]any{it}})
				}
			} else {
				ex = append(ex, exchange{ID: "r", Items: items})
			}
			ex = append(ex, exchange{ID: "e", Items: []map[string]any{call("end", "finish", map[string]any{"summary": "done"})}})
			f := newFakeProvider(t, ex)
			var events []api.Event
			cfg := sessionConfig(w, f, &events)
			cfg.Protected = []string{"guard.txt"}
			cfg.Enabled = []string{"read_file", "write_file", "list_files", "search_text", "shell", "view_image"}
			s, err := loop.NewSession(cfg)
			if err != nil {
				t.Fatal(err)
			}
			res, err := s.Round(context.Background(), "open")
			if err != nil || res.Ending != loop.EndTerminal {
				t.Fatalf("%s: %v %v", label, res, err)
			}
			var sb strings.Builder
			for i, b := range f.rawBodies {
				s := string(b)
				for _, p := range []string{w.root, w.home, w.tmp} {
					s = strings.ReplaceAll(s, p, "<DIR>")
				}
				sb.WriteString(fmt.Sprintf("--- %s request %d\n%s\n", label, i, s))
			}
			out := os.Getenv("L1_OUT")
			if out == "" {
				t.Fatal("L1_OUT unset")
			}
			_ = os.MkdirAll(out, 0o755)
			body := sb.String()
			if err := os.WriteFile(filepath.Join(out, label+".txt"), []byte(body), 0o644); err != nil {
				t.Fatal(err)
			}
			t.Logf("%s: %d requests, sha256 %x", label, len(f.rawBodies), sha256.Sum256([]byte(body)))
		}
	}
}
