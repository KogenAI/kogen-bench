package macuid

import (
	"strings"
	"testing"
)

func studioAccount() Account {
	a := testAccount()
	a.Groups = []uint32{a.GID, 12, 61, 100, 701}
	a.LocalGroups = append(a.LocalGroups,
		LocalGroup{Name: "admin", GID: 80, GUID: "uuid-withheld"},
		LocalGroup{Name: "_lpadmin", GID: 98, GUID: "uuid-withheld", NestedGroups: []string{"uuid-withheld"}},
		LocalGroup{Name: "_lpoperator", GID: 100, GUID: "uuid-withheld", NestedGroups: []string{"uuid-withheld", "uuid-withheld"}},
		LocalGroup{Name: "com.apple.sharepoint.group.1", GID: 701, GUID: "uuid-withheld", NestedGroups: []string{"uuid-withheld"}},
	)
	return a
}

func TestAccountStudioMembershipPaths(t *testing.T) {
	cases := []struct {
		name    string
		change  func(*Account)
		failure string
	}{
		{"Studio exact graph", func(a *Account) {}, ""},
		{"direct 100", func(a *Account) { a.LocalGroups[5].GroupMembership = []string{a.Name} }, "direct account"},
		{"admin-containing-account path", func(a *Account) { a.LocalGroups[3].GroupMembers = []string{a.GUID} }, "direct account"},
		{"private-primary path even if id omits", func(a *Account) { a.LocalGroups[3].NestedGroups = []string{a.LocalGroups[0].GUID} }, "unqualified nested"},
		{"cycle in nonmember sibling", func(a *Account) { a.LocalGroups[3].NestedGroups = []string{a.LocalGroups[4].GUID} }, "cycle"},
		{"unreadable GUID", func(a *Account) { a.LocalGroups[3].GUID = "" }, "ambiguous"},
		{"unknown sibling", func(a *Account) { a.LocalGroups[4].NestedGroups = []string{"uuid-withheld"} }, "unknown nested"},
		{"ambiguous GID", func(a *Account) { a.LocalGroups[3].GID = 12 }, "ambiguous"},
		{"GID 12 does not grant status", func(a *Account) {
			a.LocalGroups[1].GUID = "uuid-withheld"
			a.LocalGroups[6].NestedGroups = nil
		}, "unexplained"},
		{"direct universal", func(a *Account) { a.LocalGroups[1].GroupMembership = []string{a.Name} }, "direct account"},
		{"intermediate universal path", func(a *Account) { a.LocalGroups[5].NestedGroups = []string{a.LocalGroups[6].GUID} }, ""},
		{"no graph evidence", func(a *Account) { a.LocalGroups = nil }, "missing"},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			a := studioAccount()
			c.change(&a)
			_, err := CheckAccount(&fakeAccounts{account: a}, testAccount(), 501)
			if c.failure == "" {
				if err != nil {
					t.Fatal(err)
				}
			} else if err == nil || !strings.Contains(err.Error(), c.failure) {
				t.Fatalf("wanted %q; got %v", c.failure, err)
			}
		})
	}
}

func TestDirectoryAccountAuthentication(t *testing.T) {
	for _, c := range []struct {
		name, authority  string
		present, allowed bool
	}{
		{"absent AA", "", false, true}, {"disabled AA", ";DisabledUser;", true, true},
		{"containing disabled marker", ";DisabledUser;;ShadowHash;", true, false},
		{"password AA", ";ShadowHash;", true, false}, {"empty present AA", "", true, false},
		{"inexact marker", "DisabledUser", true, false},
	} {
		t.Run(c.name, func(t *testing.T) {
			fields := map[string]string{"UniqueID": "601", "PrimaryGroupID": "601", "GeneratedUID": testAccount().GUID, "UserShell": "/usr/bin/false", "NFSHomeDirectory": "/var/empty"}
			if c.present {
				fields["AuthenticationAuthority"] = c.authority
			}
			_, err := directoryAccount("_kogen_build_default", fields)
			if (err == nil) != c.allowed {
				t.Fatal(err)
			}
		})
	}
}

func TestDirectoryRecordAmbiguity(t *testing.T) {
	for _, text := range []string{"GeneratedUID: A\nGeneratedUID: B\n", "unreadable\n", " orphan\n"} {
		if _, err := directoryFields(text); err == nil {
			t.Fatal("ambiguous record accepted", text)
		}
	}
	fields, err := directoryFields("GroupMembership:\n  user\ndsAttrTypeNative:NestedGroups:\n  GUID\n")
	if err != nil || strings.TrimSpace(fields["GroupMembership"]) != "user" || strings.TrimSpace(fields["NestedGroups"]) != "GUID" {
		t.Fatal(fields, err)
	}
}
