# kogen-verification-orphan-sweep-6ac87f0

Kogen's acceptance step runs a command from the request (often one that starts a server) and should leave nothing of its own running afterwards. A change to the verification component (`6ac87f0`) landed to sweep such leftover processes. We checked, without any model, whether it does. **On Linux, the landed change swept 5 of the 6 leftover-server cases, exactly the same as the version before it (`587f67d`); the one case that survives is a launcher that clears the environment, starts a new session, exits, and closes inherited file descriptors, as Python's subprocess module does by default. The 6 of 6 the landing was meant to reach is not met.** On macOS the check did not run.

*Late: published 4 h after the result because of a session outage; announced to main before append.*

## What was run
Kogen `573d023` assembled twice, differing only in the verification component: the control keeps `587f67d`, the candidate takes the landed `6ac87f0`. Both were built the same way for Linux x86-64 with the same Go version (the other four components and the vendored loop are identical in both). No model was called and nothing was spent.

The fixture (`data/fixture_orphscreen_test.go`) calls the acceptance runner on six commands that each leave a `sleep` process behind, then waits 1.5 s and looks for it. A bystander `sleep`, started outside the run in its own session before each case, must still be alive afterwards. A second test runs four fixed commands through the runner and compares exit status and output between arms. A third, outside the six, repeats the failing case with the launcher keeping its inherited descriptors.

## Result
| Case | Control `587f67d` | Candidate `6ac87f0` |
| --- | --- | --- |
| plain `&` | swept | swept |
| `nohup &` | swept | swept |
| new session, environment kept | swept | swept |
| environment cleared, same process group | swept | swept |
| environment cleared, `( ... &)` subshell | swept | swept |
| environment cleared, new session, launcher exited | **survives** (parent is init) | **survives** (parent is init) |

- **Pass condition** (6 of 6 swept on Linux): not met, 5 of 6 in both arms. No case differs between the arms.
- **Bystander:** alive after all 12 runs, so the sweep is not too broad.
- **Exit status and output:** identical between arms for all four commands (exit 7 with `out`, `err`; exit 0 with `fine`; exit 143 with no output; exit 3 with `bg`).
- **Why the last case survives (diagnostic, not one of the six):** the landed change finds leftovers by an open file descriptor on a marker file the run creates, plus a marker in the environment. A launcher using Python's `subprocess.Popen` closes descriptors above 2 in the child by default, and the case also clears the environment and starts a new session, so nothing is left to find. With the same launcher told to keep descriptors, the control leaves the process running and the candidate sweeps it. So the landing handles a launcher that keeps inherited descriptors and not one that closes them. Launchers in other languages commonly close descriptors above 2 as well, so the gap is probably not limited to Python; only Python was measured.
- **Not shown:** that this case occurred in the hang that motivated the change, and how often real acceptance commands launch servers this way.

## Limits
Linux only. The same fixture on macOS did not run: the machine was busy for the whole window and the job gave up at its time limit, so the macOS behaviour (where the sweep relies on the marker alone) is unmeasured. One run of each case per arm; the cases are deterministic launchers, not a sample of real acceptance commands. A candidate assembled from a source commit is not the released binary, though the other components are the adopted pins.

## Rerun
Control: Kogen `573d023` with the verification component at `587f67d`. Candidate: the same with the verification component at `6ac87f0`. Copy `data/fixture_orphscreen_test.go` into the verification component's `verify/` directory (it uses that package's `RunAcceptance` and test helpers), run it on Linux with `go test -count=1 -v -run 'TestClimbLeftoverServers|TestClimbExitOutput|TestClimbDiagKeepFD' ./verify/` in each tree, and compare the two outputs. The component sources are in private repositories, so this step needs access to them.

The counts above rebuild from the committed tables with the standard library only:

```sh
python3 -I reproduce/kogen-verification-orphan-sweep-6ac87f0/report.py reproduce/kogen-verification-orphan-sweep-6ac87f0/data | diff - reproduce/kogen-verification-orphan-sweep-6ac87f0/expected-output.txt
```
