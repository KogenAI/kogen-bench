-- Generated from current Elixir source; never edit this file.
namespace FV
inductive Atom where
  | a_cleanup
  | a_missing
  | a_nil
  | a_preserve_fail
  | a_preserve_ok
  | a_retry
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

structure R_pending_saved_work where
  v_pending : Bool := false
  v_pending_present : Bool := false
  v_saved : Bool := false
  v_saved_present : Bool := false
  v_work : Bool := false
  v_work_present : Bool := false
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

-- src: lib/preservation.ex:48
def v_Preservation_cleanup_ready_1 (p0 : R_pending_saved_work) : Bool :=
  match p0 with
  | v_state => (/- src: lib/preservation.ex:49 -/ (/- src: lib/preservation.ex:49 -/ v_state).v_pending)

-- src: lib/preservation.ex:52
def v_Preservation_retire_1 (p0 : R_pending_saved_work) : R_pending_saved_work :=
  match p0 with
  | v_state => (/- src: lib/preservation.ex:53 -/ { (/- src: lib/preservation.ex:53 -/ v_state) with v_work := (/- src: lib/preservation.ex:53 -/ false), v_pending := (/- src: lib/preservation.ex:53 -/ false) })

-- src: lib/preservation.ex:40
def v_Preservation_cleanup_1 (p0 : R_pending_saved_work) : R_pending_saved_work :=
  match p0 with
  | v_state => (/- src: lib/preservation.ex:41 -/ (if (/- src: lib/preservation.ex:41 -/ (v_Preservation_cleanup_ready_1 (/- src: lib/preservation.ex:41 -/ v_state))) then (/- src: lib/preservation.ex:42 -/ (v_Preservation_retire_1 (/- src: lib/preservation.ex:42 -/ v_state))) else (/- src: lib/preservation.ex:44 -/ v_state)))

-- src: lib/preservation.ex:24
def v_Preservation_cleanup_event_2 (p0 : R_pending_saved_work) (p1 : Atom) : R_pending_saved_work :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/preservation.ex:25 -/ (if (/- src: lib/preservation.ex:25 -/ ((/- src: lib/preservation.ex:25 -/ ((/- src: lib/preservation.ex:25 -/ v_event) == (/- src: lib/preservation.ex:25 -/ Atom.a_cleanup))) || (/- src: lib/preservation.ex:25 -/ ((/- src: lib/preservation.ex:25 -/ v_event) == (/- src: lib/preservation.ex:25 -/ Atom.a_retry))))) then (/- src: lib/preservation.ex:26 -/ (v_Preservation_cleanup_1 (/- src: lib/preservation.ex:26 -/ v_state))) else (/- src: lib/preservation.ex:28 -/ v_state)))

-- src: lib/preservation.ex:36
def v_Preservation_failed_1 (p0 : R_pending_saved_work) : R_pending_saved_work :=
  match p0 with
  | v_state => (/- src: lib/preservation.ex:37 -/ { (/- src: lib/preservation.ex:37 -/ v_state) with v_pending := (/- src: lib/preservation.ex:37 -/ (/- src: lib/preservation.ex:37 -/ v_state).v_work) })

-- src: lib/preservation.ex:16
def v_Preservation_dispatch_2 (p0 : R_pending_saved_work) (p1 : Atom) : R_pending_saved_work :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/preservation.ex:17 -/ (if (/- src: lib/preservation.ex:17 -/ ((/- src: lib/preservation.ex:17 -/ v_event) == (/- src: lib/preservation.ex:17 -/ Atom.a_preserve_fail))) then (/- src: lib/preservation.ex:18 -/ (v_Preservation_failed_1 (/- src: lib/preservation.ex:18 -/ v_state))) else (/- src: lib/preservation.ex:20 -/ (v_Preservation_cleanup_event_2 (/- src: lib/preservation.ex:20 -/ v_state) (/- src: lib/preservation.ex:20 -/ v_event)))))

-- src: lib/preservation.ex:4
def v_Preservation_init_0  : R_pending_saved_work :=
  (/- src: lib/preservation.ex:5 -/ ({ v_pending := (/- src: lib/preservation.ex:5 -/ false), v_pending_present := true, v_saved := (/- src: lib/preservation.ex:5 -/ false), v_saved_present := true, v_work := (/- src: lib/preservation.ex:5 -/ true), v_work_present := true } : R_pending_saved_work))

-- src: lib/preservation.ex:32
def v_Preservation_preserve_1 (p0 : R_pending_saved_work) : R_pending_saved_work :=
  match p0 with
  | v_state => (/- src: lib/preservation.ex:33 -/ { (/- src: lib/preservation.ex:33 -/ v_state) with v_saved := (/- src: lib/preservation.ex:33 -/ ((/- src: lib/preservation.ex:33 -/ (/- src: lib/preservation.ex:33 -/ v_state).v_saved) || (/- src: lib/preservation.ex:33 -/ (/- src: lib/preservation.ex:33 -/ v_state).v_work))), v_pending := (/- src: lib/preservation.ex:33 -/ (/- src: lib/preservation.ex:33 -/ v_state).v_work) })

-- src: lib/preservation.ex:8
def v_Preservation_step_2 (p0 : R_pending_saved_work) (p1 : Atom) : R_pending_saved_work :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/preservation.ex:9 -/ (if (/- src: lib/preservation.ex:9 -/ ((/- src: lib/preservation.ex:9 -/ v_event) == (/- src: lib/preservation.ex:9 -/ Atom.a_preserve_ok))) then (/- src: lib/preservation.ex:10 -/ (v_Preservation_preserve_1 (/- src: lib/preservation.ex:10 -/ v_state))) else (/- src: lib/preservation.ex:12 -/ (v_Preservation_dispatch_2 (/- src: lib/preservation.ex:12 -/ v_state) (/- src: lib/preservation.ex:12 -/ v_event)))))

abbrev State := R_pending_saved_work
abbrev init := v_Preservation_init_0
abbrev step := v_Preservation_step_2
end FV
