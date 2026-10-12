# Optional difficulty increases

- Require recovery when the process is killed immediately after CAS, reconciling
  a journal against the target without double application.
- Permit merge commits in changes and require rebase-merges topology preservation.
- Add bounded check timeouts with process-group termination and descendant cleanup.
- Support multiple configured targets and reject landing onto a branch checked out
  in any linked worktree without modifying that checkout.
- Require durable fsync publication and recovery during interrupted rebase and abort.
