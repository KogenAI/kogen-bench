package contract

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"

	"github.com/KogenAI/kogen-executor/executor"
	"github.com/KogenAI/kogen-review/review"
	"github.com/KogenAI/kogen-verification/verify"
)

// Replay of recorded submit_review sequences (model-free). REPLAY_FILE names a JSON list of
// sequences, REPLAY_OUT the file the outcomes are written to; without REPLAY_FILE the test skips.

type replaySeq struct {
	Name       string            `json:"name"`
	Acceptance json.RawMessage   `json:"acceptance"`
	EditRound  int               `json:"edit_round"`
	Rounds     []json.RawMessage `json:"rounds"`
}

type replayExecutor struct {
	t         *testing.T
	seq       replaySeq
	root      string
	round     int
	feedbacks []string
}

func (x *replayExecutor) Describe() executor.Descriptor { return externalDescriptor() }

func (x *replayExecutor) Start(ctx context.Context, task executor.Task, emit executor.Sink) (executor.Session, error) {
	return &replaySession{x: x}, nil
}

type replaySession struct{ x *replayExecutor }

func (s *replaySession) Handle() executor.Handle {
	return executor.Handle{Role: executor.RoleReview, Executor: "fixture-executor", Version: "1.0.0", SessionID: "replay-session"}
}
func (s *replaySession) Close() error { return nil }
func (s *replaySession) Round(ctx context.Context, in executor.Input) (executor.RoundResult, error) {
	x := s.x
	x.feedbacks = append(x.feedbacks, in.Feedback)
	if x.round >= len(x.seq.Rounds) {
		x.t.Fatalf("%s: the review asked for round %d, the recording has %d", x.seq.Name, x.round+1, len(x.seq.Rounds))
	}
	x.round++
	if x.round == x.seq.EditRound {
		// The reviewer edits the candidate during this round, as the recorded one did.
		writeFile(x.t, filepath.Join(x.root, "app.txt"), otherText)
	}
	r := structured(string(x.seq.Rounds[x.round-1]))
	r.Handle = s.Handle()
	return r, nil
}

var (
	reMissing = regexp.MustCompile(`(?s)requirement ".*?" was listed by an earlier submission of this review and is missing: keep every requirement in requirements, with evidence observed on the current tree`)
	kinds     = map[string]string{
		"not_run":          "which did not run on the current tree (not_run)",
		"no_scenario":      "which names no scenario of the acceptance result",
		"other_tree":       "whose result is of tree",
		"scenario_failed":  "which failed on the current tree",
		"scenario_other":   "whose result on the current tree is",
		"no_evidence":      "has no evidence: probe it",
		"not_met":          "is not met",
		"listed_twice":     "is listed twice",
		"probe":            "cites a probe",
		"shape":            "requirements must be a JSON array",
		"verdict_shape":    "submit_review needs verdict",
		"finding":          "each finding needs path",
	}
)

type replayRound struct {
	Round   int            `json:"round"`
	Refused bool           `json:"refused"`
	Missing int            `json:"missing_problems"`
	Other   map[string]int `json:"other_problems"`
}

type replayOut struct {
	Name    string        `json:"name"`
	Outcome string        `json:"outcome"` // approved | review_invalid | error
	Reason  string        `json:"reason,omitempty"`
	Rounds  []replayRound `json:"rounds"`
	Used    int           `json:"rounds_used"`
}

func classify(text string) (missing int, other map[string]int) {
	missing = len(reMissing.FindAllString(text, -1))
	rest := reMissing.ReplaceAllString(text, "")
	other = map[string]int{}
	for k, frag := range kinds {
		if n := strings.Count(rest, frag); n > 0 {
			other[k] = n
		}
	}
	return
}

func replayOne(t *testing.T, seq replaySeq) replayOut {
	in, h := newReview(t)
	if len(seq.Acceptance) > 0 && string(seq.Acceptance) != "null" {
		var acc verify.Acceptance
		if err := json.Unmarshal(seq.Acceptance, &acc); err != nil {
			t.Fatal(err)
		}
		in.Evidence.Pass.Acceptance = &acc
	}
	if seq.EditRound > 0 {
		// The pass the repair is verified by: green on the reviewer-edited tree.
		p := verify.Pass{N: 2, Clean: true, Green: true, Tree: otherTree}
		if in.Evidence.Pass.Acceptance != nil {
			p.Acceptance = in.Evidence.Pass.Acceptance
		}
		h.verifies = []verify.Pass{p}
	}
	x := &replayExecutor{t: t, seq: seq, root: in.Candidate.Root}
	res, err := review.NewExternal(x, externalDescriptor(), 4).Review(context.Background(), in, h)
	out := replayOut{Name: seq.Name, Used: x.round}
	switch {
	case err == nil && res.Record.Verdict == "approve":
		out.Outcome = "approved"
	case res.Invalid != nil:
		out.Outcome, out.Reason = "review_invalid", res.Invalid.Reason
	default:
		out.Outcome = "error"
		if err != nil {
			out.Reason = err.Error()
		}
	}
	// A round is refused when the next round's feedback is a refusal, or, for the last round, when the review ended invalid.
	for k := 0; k < x.round; k++ {
		rr := replayRound{Round: k + 1}
		var text string
		if k+1 < len(x.feedbacks) {
			if f := x.feedbacks[k+1]; strings.HasPrefix(f, "Not a valid verdict:") {
				rr.Refused, text = true, f
			}
		} else if out.Outcome == "review_invalid" && res.Invalid != nil {
			rr.Refused, text = true, strings.Join(res.Invalid.Problems, "; ")
		}
		if rr.Refused {
			rr.Missing, rr.Other = classify(text)
		}
		out.Rounds = append(out.Rounds, rr)
	}
	return out
}

func TestReplayRecordedSequences(t *testing.T) {
	file := os.Getenv("REPLAY_FILE")
	if file == "" {
		t.Skip("REPLAY_FILE not set")
	}
	data, err := os.ReadFile(file)
	if err != nil {
		t.Fatal(err)
	}
	var seqs []replaySeq
	if err := json.Unmarshal(data, &seqs); err != nil {
		t.Fatal(err)
	}
	var outs []replayOut
	for _, s := range seqs {
		outs = append(outs, replayOne(t, s))
	}
	b, _ := json.MarshalIndent(outs, "", " ")
	if err := os.WriteFile(os.Getenv("REPLAY_OUT"), b, 0o600); err != nil {
		t.Fatal(err)
	}
}
