-- Generated from current Elixir source; never edit this file.
namespace FV
inductive Atom where
  | a_guest
  | a_missing
  | a_nil
  | a_owner
  | a_t1
  | a_t2
  | a_viewer
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

structure R_role_tenant where
  v_role : Atom := .a_missing
  v_role_present : Bool := false
  v_tenant : Atom := .a_missing
  v_tenant_present : Bool := false
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

structure R_tenant where
  v_tenant : Atom := .a_missing
  v_tenant_present : Bool := false
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

-- src: lib/access.ex:21
def v_TenantGate_actor_role_1 (p0 : R_role_tenant) : Atom :=
  match p0 with
  | v_actor => (/- src: lib/access.ex:22 -/ (if (/- src: lib/access.ex:22 -/ v_actor).v_role_present then (/- src: lib/access.ex:22 -/ v_actor).v_role else (/- src: lib/access.ex:22 -/ Atom.a_missing)))

-- src: lib/access.ex:13
def v_TenantGate_actor_tenant_1 (p0 : R_role_tenant) : Atom :=
  match p0 with
  | v_actor => (/- src: lib/access.ex:14 -/ (if (/- src: lib/access.ex:14 -/ v_actor).v_tenant_present then (/- src: lib/access.ex:14 -/ v_actor).v_tenant else (/- src: lib/access.ex:14 -/ Atom.a_missing)))

-- src: lib/access.ex:25
def v_TenantGate_fields_present_3 (p0 : Atom) (p1 : Atom) (p2 : Atom) : Bool :=
  match p0, p1, p2 with
  | v_actor_tenant, v_resource_tenant, v_role => (/- src: lib/access.ex:27 -/ ((/- src: lib/access.ex:26 -/ ((/- src: lib/access.ex:26 -/ ((/- src: lib/access.ex:26 -/ v_actor_tenant) != (/- src: lib/access.ex:26 -/ Atom.a_missing))) && (/- src: lib/access.ex:27 -/ ((/- src: lib/access.ex:27 -/ v_resource_tenant) != (/- src: lib/access.ex:27 -/ Atom.a_missing))))) && (/- src: lib/access.ex:28 -/ ((/- src: lib/access.ex:28 -/ v_role) != (/- src: lib/access.ex:28 -/ Atom.a_missing)))))

-- src: lib/access.ex:17
def v_TenantGate_resource_tenant_1 (p0 : R_tenant) : Atom :=
  match p0 with
  | v_resource => (/- src: lib/access.ex:18 -/ (if (/- src: lib/access.ex:18 -/ v_resource).v_tenant_present then (/- src: lib/access.ex:18 -/ v_resource).v_tenant else (/- src: lib/access.ex:18 -/ Atom.a_missing)))

-- src: lib/access.ex:37
def v_TenantGate_owner_read_3 (p0 : Atom) (p1 : Atom) (p2 : Atom) : Bool :=
  match p0, p1, p2 with
  | v_role, v_actor_tenant, v_resource_tenant => (/- src: lib/access.ex:38 -/ ((/- src: lib/access.ex:38 -/ ((/- src: lib/access.ex:38 -/ v_role) == (/- src: lib/access.ex:38 -/ Atom.a_owner))) && (/- src: lib/access.ex:38 -/ ((/- src: lib/access.ex:38 -/ v_actor_tenant) == (/- src: lib/access.ex:38 -/ v_resource_tenant)))))

-- src: lib/access.ex:41
def v_TenantGate_viewer_read_3 (p0 : Atom) (p1 : Atom) (p2 : Atom) : Bool :=
  match p0, p1, p2 with
  | v_role, v__actor_tenant, v__resource_tenant => (/- src: lib/access.ex:42 -/ ((/- src: lib/access.ex:42 -/ v_role) == (/- src: lib/access.ex:42 -/ Atom.a_viewer)))

-- src: lib/access.ex:31
def v_TenantGate_role_admitted_3 (p0 : Atom) (p1 : Atom) (p2 : Atom) : Bool :=
  match p0, p1, p2 with
  | v_role, v_actor_tenant, v_resource_tenant => (/- src: lib/access.ex:32 -/ (let v_owner := (/- src: lib/access.ex:32 -/ (v_TenantGate_owner_read_3 (/- src: lib/access.ex:32 -/ v_role) (/- src: lib/access.ex:32 -/ v_actor_tenant) (/- src: lib/access.ex:32 -/ v_resource_tenant))); (/- src: lib/access.ex:33 -/ (let v_viewer := (/- src: lib/access.ex:33 -/ (v_TenantGate_viewer_read_3 (/- src: lib/access.ex:33 -/ v_role) (/- src: lib/access.ex:33 -/ v_actor_tenant) (/- src: lib/access.ex:33 -/ v_resource_tenant))); (/- src: lib/access.ex:34 -/ ((/- src: lib/access.ex:34 -/ v_owner) || (/- src: lib/access.ex:34 -/ v_viewer)))))))

-- src: lib/access.ex:5
def v_TenantGate_can_read_2 (p0 : R_role_tenant) (p1 : R_tenant) : Bool :=
  match p0, p1 with
  | v_actor, v_resource => (/- src: lib/access.ex:6 -/ (let v_actor_tenant := (/- src: lib/access.ex:6 -/ (v_TenantGate_actor_tenant_1 (/- src: lib/access.ex:6 -/ v_actor))); (/- src: lib/access.ex:7 -/ (let v_resource_tenant := (/- src: lib/access.ex:7 -/ (v_TenantGate_resource_tenant_1 (/- src: lib/access.ex:7 -/ v_resource))); (/- src: lib/access.ex:8 -/ (let v_role := (/- src: lib/access.ex:8 -/ (v_TenantGate_actor_role_1 (/- src: lib/access.ex:8 -/ v_actor))); (/- src: lib/access.ex:9 -/ (let v_present := (/- src: lib/access.ex:9 -/ (v_TenantGate_fields_present_3 (/- src: lib/access.ex:9 -/ v_actor_tenant) (/- src: lib/access.ex:9 -/ v_resource_tenant) (/- src: lib/access.ex:9 -/ v_role))); (/- src: lib/access.ex:10 -/ ((/- src: lib/access.ex:10 -/ v_present) && (/- src: lib/access.ex:10 -/ (v_TenantGate_role_admitted_3 (/- src: lib/access.ex:10 -/ v_role) (/- src: lib/access.ex:10 -/ v_actor_tenant) (/- src: lib/access.ex:10 -/ v_resource_tenant)))))))))))))

abbrev Actor := R_role_tenant
abbrev Resource := R_tenant
abbrev canRead := v_TenantGate_can_read_2
end FV
