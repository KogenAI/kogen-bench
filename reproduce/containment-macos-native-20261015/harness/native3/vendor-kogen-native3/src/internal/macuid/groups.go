package macuid

import (
	"embed"
	"encoding/json"
	"fmt"
	"regexp"
	"strings"
)

// Shared with setup/check_groups.py. GIDs (including 12/61) and names never
// confer universal status. Every account-containing path must originate at one
// of these GUIDs; unrelated sibling branches contribute no membership paths.
//
//go:embed universal_roots.json
var universalData embed.FS
var universalRoots = func() map[string]string {
	b, err := universalData.ReadFile("universal_roots.json")
	if err != nil {
		panic(err)
	}
	var roots map[string]string
	if err := json.Unmarshal(b, &roots); err != nil {
		panic(err)
	}
	return roots
}()

// LocalGroup is read-only Directory Services evidence, never config authority.
type LocalGroup struct {
	Name                                        string
	GID                                         uint32
	GUID                                        string
	GroupMembership, GroupMembers, NestedGroups []string
}

var groupGUID = regexp.MustCompile(`^[0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12}$`)

type membershipPaths struct {
	roots  map[string]bool
	unsafe bool
}

func checkGroupPaths(a Account) error {
	records := map[string]LocalGroup{}
	gids, names := map[uint32]bool{}, map[string]bool{}
	private := ""
	for _, g := range a.LocalGroups {
		g.GUID = strings.ToUpper(g.GUID)
		for _, member := range append(append([]string{}, g.GroupMembers...), g.NestedGroups...) {
			if !groupGUID.MatchString(strings.ToUpper(member)) {
				return fmt.Errorf("invalid membership GUID")
			}
		}
		if g.Name == "" || strings.ContainsAny(g.Name, "/\x00") || !groupGUID.MatchString(g.GUID) || gids[g.GID] || names[g.Name] {
			return fmt.Errorf("ambiguous local group identity")
		}
		if _, exists := records[g.GUID]; exists {
			return fmt.Errorf("duplicate group GUID")
		}
		gids[g.GID], names[g.Name] = true, true
		records[g.GUID] = g
		if g.Name == a.Name && g.GID == a.GID {
			private = g.GUID
		}
	}
	if _, universal := universalRoots[private]; universal {
		return fmt.Errorf("private group uses universal GUID")
	}
	if private == "" {
		return fmt.Errorf("private primary group identity missing")
	}
	if len(records[private].NestedGroups) != 0 {
		return fmt.Errorf("private group nesting")
	}
	memo, visiting := map[string]membershipPaths{}, map[string]bool{}
	var paths func(string) (membershipPaths, error)
	paths = func(guid string) (membershipPaths, error) {
		guid = strings.ToUpper(guid)
		g, exists := records[guid]
		if !exists {
			return membershipPaths{}, fmt.Errorf("unknown nested group GUID: %s", guid)
		}
		if visiting[guid] {
			return membershipPaths{}, fmt.Errorf("group nesting cycle")
		}
		if p, ok := memo[guid]; ok {
			return p, nil
		}
		visiting[guid] = true
		direct := false
		for _, name := range g.GroupMembership {
			direct = direct || name == a.Name
		}
		for _, member := range g.GroupMembers {
			direct = direct || strings.EqualFold(member, a.GUID)
		}
		if direct && guid != private {
			return membershipPaths{}, fmt.Errorf("direct account group membership: %d %s", g.GID, g.Name)
		}
		p := membershipPaths{roots: map[string]bool{}, unsafe: guid == private}
		if root, ok := universalRoots[guid]; ok {
			p.roots[root] = true
		}
		for _, child := range g.NestedGroups {
			cp, err := paths(child)
			if err != nil {
				return p, err
			}
			for root := range cp.roots {
				p.roots[root] = true
			}
			p.unsafe = p.unsafe || cp.unsafe
		}
		visiting[guid] = false
		memo[guid] = p
		return p, nil
	}
	for guid := range records {
		if _, err := paths(guid); err != nil {
			return err
		}
	}
	resolved := map[uint32]bool{}
	for _, gid := range a.Groups {
		resolved[gid] = true
	}
	if !resolved[a.GID] {
		return fmt.Errorf("primary GID missing from resolved membership")
	}
	for guid, g := range records {
		if guid == private {
			delete(resolved, g.GID)
			continue
		}
		p := memo[guid]
		if p.unsafe {
			return fmt.Errorf("unqualified nested group membership: %d %s", g.GID, g.Name)
		}
		if resolved[g.GID] && len(p.roots) == 0 {
			return fmt.Errorf("unexplained resolved group membership: %d %s", g.GID, g.Name)
		}
		delete(resolved, g.GID)
	}
	if len(resolved) != 0 {
		return fmt.Errorf("unmapped resolved group membership")
	}
	return nil
}
