package shape

import "github.com/KogenAI/kogen-loop/sys"

func asSysLines(err error) ([]string, bool) {
	e, ok := sys.AsError(err)
	if !ok {
		return nil, false
	}
	return e.Lines, true
}
