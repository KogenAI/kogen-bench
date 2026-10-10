# Revision-bound build admission

`Workflow.init/0` starts at revision `r1`, with no approval (`none`) and
`admitted` false. `step/2` handles `approve`, `edit_r1`, `edit_r2`, and `start`.
Approve stores the current revision token. An edit selects the named revision
and resets admitted to false; it retains the approval token as historical
evidence. Start sets admitted to true exactly when the stored approval equals
the current revision. Thus an approval for a different revision grants no
eligibility. Selecting the approved token again restores eligibility on the
next start. Approve does not itself start a build. Other events leave state
unchanged. Check every sequence of zero through six events.
