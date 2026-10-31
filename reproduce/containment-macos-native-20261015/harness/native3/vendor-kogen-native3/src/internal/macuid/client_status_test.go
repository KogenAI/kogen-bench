package macuid

import "testing"

func TestStatusFrameCheckAdmitsOnlyAReadyNativeUnqualifiedCustodian(t *testing.T) {
	if err := (StatusFrame{Status: "ready", Launch: LaunchVersion}).Check(); err != nil {
		t.Fatal(err)
	}
	for name, s := range map[string]StatusFrame{
		"not-ready":     {Status: "busy", Launch: LaunchVersion},
		"old-launch":    {Status: "ready", Launch: 0},
		"claims-qualif": {Status: "ready", Launch: LaunchVersion, Qualified: true},
	} {
		if s.Check() == nil {
			t.Fatal(name, "accepted")
		}
	}
}
