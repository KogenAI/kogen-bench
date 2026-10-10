-- Generated from current Elixir source; never edit this file.
namespace FV
inductive Atom where
  | a_approve
  | a_edit_r1
  | a_edit_r2
  | a_missing
  | a_nil
  | a_none
  | a_r1
  | a_r2
  | a_start
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

structure R_admitted_approved_revision where
  v_admitted : Bool := false
  v_admitted_present : Bool := false
  v_approved : Atom := .a_missing
  v_approved_present : Bool := false
  v_revision : Atom := .a_missing
  v_revision_present : Bool := false
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

-- src: lib/workflow.ex:48
def v_Workflow_admission_1 (p0 : R_admitted_approved_revision) : Bool :=
  match p0 with
  | v_state => (/- src: lib/workflow.ex:49 -/ ((/- src: lib/workflow.ex:49 -/ (/- src: lib/workflow.ex:49 -/ v_state).v_approved) != (/- src: lib/workflow.ex:49 -/ Atom.a_none)))

-- src: lib/workflow.ex:36
def v_Workflow_approve_1 (p0 : R_admitted_approved_revision) : R_admitted_approved_revision :=
  match p0 with
  | v_state => (/- src: lib/workflow.ex:37 -/ { (/- src: lib/workflow.ex:37 -/ v_state) with v_approved := (/- src: lib/workflow.ex:37 -/ (/- src: lib/workflow.ex:37 -/ v_state).v_revision) })

-- src: lib/workflow.ex:40
def v_Workflow_edit_2 (p0 : R_admitted_approved_revision) (p1 : Atom) : R_admitted_approved_revision :=
  match p0, p1 with
  | v_state, v_revision => (/- src: lib/workflow.ex:41 -/ { (/- src: lib/workflow.ex:41 -/ v_state) with v_revision := (/- src: lib/workflow.ex:41 -/ v_revision), v_admitted := (/- src: lib/workflow.ex:41 -/ false) })

-- src: lib/workflow.ex:24
def v_Workflow_edit_event_2 (p0 : R_admitted_approved_revision) (p1 : Atom) : R_admitted_approved_revision :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/workflow.ex:25 -/ (if (/- src: lib/workflow.ex:25 -/ ((/- src: lib/workflow.ex:25 -/ v_event) == (/- src: lib/workflow.ex:25 -/ Atom.a_edit_r1))) then (/- src: lib/workflow.ex:26 -/ (v_Workflow_edit_2 (/- src: lib/workflow.ex:26 -/ v_state) (/- src: lib/workflow.ex:26 -/ Atom.a_r1))) else (/- src: lib/workflow.ex:28 -/ (if (/- src: lib/workflow.ex:28 -/ ((/- src: lib/workflow.ex:28 -/ v_event) == (/- src: lib/workflow.ex:28 -/ Atom.a_edit_r2))) then (/- src: lib/workflow.ex:29 -/ (v_Workflow_edit_2 (/- src: lib/workflow.ex:29 -/ v_state) (/- src: lib/workflow.ex:29 -/ Atom.a_r2))) else (/- src: lib/workflow.ex:31 -/ v_state)))))

-- src: lib/workflow.ex:44
def v_Workflow_start_1 (p0 : R_admitted_approved_revision) : R_admitted_approved_revision :=
  match p0 with
  | v_state => (/- src: lib/workflow.ex:45 -/ { (/- src: lib/workflow.ex:45 -/ v_state) with v_admitted := (/- src: lib/workflow.ex:45 -/ (v_Workflow_admission_1 (/- src: lib/workflow.ex:45 -/ v_state))) })

-- src: lib/workflow.ex:16
def v_Workflow_dispatch_2 (p0 : R_admitted_approved_revision) (p1 : Atom) : R_admitted_approved_revision :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/workflow.ex:17 -/ (if (/- src: lib/workflow.ex:17 -/ ((/- src: lib/workflow.ex:17 -/ v_event) == (/- src: lib/workflow.ex:17 -/ Atom.a_start))) then (/- src: lib/workflow.ex:18 -/ (v_Workflow_start_1 (/- src: lib/workflow.ex:18 -/ v_state))) else (/- src: lib/workflow.ex:20 -/ (v_Workflow_edit_event_2 (/- src: lib/workflow.ex:20 -/ v_state) (/- src: lib/workflow.ex:20 -/ v_event)))))

-- src: lib/workflow.ex:4
def v_Workflow_init_0  : R_admitted_approved_revision :=
  (/- src: lib/workflow.ex:5 -/ ({ v_admitted := (/- src: lib/workflow.ex:5 -/ false), v_admitted_present := true, v_approved := (/- src: lib/workflow.ex:5 -/ Atom.a_none), v_approved_present := true, v_revision := (/- src: lib/workflow.ex:5 -/ Atom.a_r1), v_revision_present := true } : R_admitted_approved_revision))

-- src: lib/workflow.ex:8
def v_Workflow_step_2 (p0 : R_admitted_approved_revision) (p1 : Atom) : R_admitted_approved_revision :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/workflow.ex:9 -/ (if (/- src: lib/workflow.ex:9 -/ ((/- src: lib/workflow.ex:9 -/ v_event) == (/- src: lib/workflow.ex:9 -/ Atom.a_approve))) then (/- src: lib/workflow.ex:10 -/ (v_Workflow_approve_1 (/- src: lib/workflow.ex:10 -/ v_state))) else (/- src: lib/workflow.ex:12 -/ (v_Workflow_dispatch_2 (/- src: lib/workflow.ex:12 -/ v_state) (/- src: lib/workflow.ex:12 -/ v_event)))))

abbrev State := R_admitted_approved_revision
abbrev init := v_Workflow_init_0
abbrev step := v_Workflow_step_2
end FV
