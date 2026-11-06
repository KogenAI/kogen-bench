package shape

import "strings"

// arm B2: the line through evidenceRuleHints as the readiness gate does.
func aor2Hinted(s string) string { return strings.Join(evidenceRuleHints(strings.Split(s, " | ")), " | ") }
