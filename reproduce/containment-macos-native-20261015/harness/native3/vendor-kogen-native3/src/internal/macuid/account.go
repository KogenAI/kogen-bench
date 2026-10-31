package macuid

import (
	"fmt"
	"regexp"
)

type Account struct {
	Name        string       `json:"name"`
	UID         uint32       `json:"uid"`
	GID         uint32       `json:"gid"`
	GUID        string       `json:"generated_uid"`
	Home        string       `json:"home"`
	Shell       string       `json:"shell"`
	Groups      []uint32     `json:"groups"`
	LocalGroups []LocalGroup `json:"-"`
}

type Accounts interface{ Lookup(string) (Account, error) }

func CheckAccount(db Accounts, want Account, controllerUID uint32) (Account, error) {
	if db == nil || !regexp.MustCompile(`^_kogen_build_[a-z0-9_]{1,32}$`).MatchString(want.Name) {
		return Account{}, fmt.Errorf("reserved Build account registration required")
	}
	got, err := db.Lookup(want.Name)
	if err != nil {
		return Account{}, fmt.Errorf("dedicated Build account absent: operator must run the admin setup: %w", err)
	}
	if got.Name != want.Name || got.UID < 501 || got.GID < 501 || got.UID == controllerUID || got.UID != want.UID || got.GID != want.GID || got.GUID == "" || got.GUID != want.GUID || got.Shell != "/usr/bin/false" || got.Home != "/var/empty" {
		return Account{}, fmt.Errorf("Build account identity/privilege drift")
	}
	if err := checkGroupPaths(got); err != nil {
		return Account{}, err
	}
	return got, nil
}
