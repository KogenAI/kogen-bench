package macuid

import (
	"fmt"
	"strconv"
	"strings"
)

// Full-record reads permit an absent AuthenticationAuthority without dscl's
// missing-requested-attribute error. Duplicate attributes fail closed.
func directoryFields(text string) (map[string]string, error) {
	fields := map[string]string{}
	lastKey := ""
	for _, line := range strings.Split(text, "\n") {
		if strings.TrimSpace(line) == "" {
			continue
		}
		if strings.HasPrefix(line, " ") || strings.HasPrefix(line, "\t") {
			if lastKey == "" {
				return nil, fmt.Errorf("orphan directory continuation")
			}
			fields[lastKey] += " " + strings.TrimSpace(line)
			continue
		}
		line = strings.TrimPrefix(line, "dsAttrTypeNative:")
		key, val, ok := strings.Cut(line, ":")
		if !ok || key == "" {
			return nil, fmt.Errorf("unreadable directory record")
		}
		if _, exists := fields[key]; exists {
			return nil, fmt.Errorf("ambiguous directory attribute: %s", key)
		}
		fields[key], lastKey = strings.TrimSpace(val), key
	}
	return fields, nil
}

// disabledAuthentication accepts an absent AuthenticationAuthority or exactly
// one value equal to ";DisabledUser;". Mixed (";DisabledUser; ;ShadowHash;"),
// duplicated, empty or otherwise extended authorities refuse. setup/common.sh
// applies the same rule; authority_cases.json pins the shared vectors.
func disabledAuthentication(fields map[string]string) bool {
	authority, present := fields["AuthenticationAuthority"]
	if !present {
		return true
	}
	values := strings.Fields(authority)
	return len(values) == 1 && values[0] == ";DisabledUser;"
}

func directoryAccount(name string, fields map[string]string) (Account, error) {
	uid, err := strconv.ParseUint(fields["UniqueID"], 10, 32)
	if err != nil {
		return Account{}, err
	}
	gid, err := strconv.ParseUint(fields["PrimaryGroupID"], 10, 32)
	if err != nil {
		return Account{}, err
	}
	if !disabledAuthentication(fields) {
		return Account{}, fmt.Errorf("interactive authentication must be disabled")
	}
	if !groupGUID.MatchString(strings.ToUpper(fields["GeneratedUID"])) {
		return Account{}, fmt.Errorf("invalid account GUID")
	}
	return Account{Name: name, UID: uint32(uid), GID: uint32(gid), GUID: fields["GeneratedUID"], Home: fields["NFSHomeDirectory"], Shell: fields["UserShell"]}, nil
}

func directoryGroup(name string, fields map[string]string) (LocalGroup, error) {
	gid, err := strconv.ParseUint(fields["PrimaryGroupID"], 10, 32)
	if err != nil {
		return LocalGroup{}, err
	}
	return LocalGroup{Name: name, GID: uint32(gid), GUID: fields["GeneratedUID"], GroupMembership: strings.Fields(fields["GroupMembership"]), GroupMembers: strings.Fields(fields["GroupMembers"]), NestedGroups: strings.Fields(fields["NestedGroups"])}, nil
}
