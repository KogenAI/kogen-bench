# Private data and task grading

Hidden suites and grader code are shipped under each task as they are added. “Hidden” means hidden from the coding agent during a run; it does not mean withheld from you as a repository reader. Task-specific grading materials are in `tasks/<id>/hidden/` and `tasks/<id>/grader/` and must stay outside the agent-visible workspace during execution.

The following remain private because they can grant access, identify people or infrastructure, or expose raw account activity:

- Credentials, authentication files, private keys, account data, and invoices.
- Real hostnames and IP addresses. Public records use venue aliases and generic environment descriptions.
- Raw transcripts, stderr and egress logs, diagnostic grade tails, and failing-test lists.
- Production systems, private code trees, and running-cell workspaces.

The new Ubuntu host kit documents its fixed `/srv/bh/bench` installation root and the generic `/home/bench` service account. Those paths identify the public setup layout only; credentials, host identities, and run data remain private.

Public task prompts and bases, shipped hidden suites and graders, sanitized outcome metadata, and documented aggregate results are retained. A source-reported hash for an absent source record cannot be independently verified from this repository.
