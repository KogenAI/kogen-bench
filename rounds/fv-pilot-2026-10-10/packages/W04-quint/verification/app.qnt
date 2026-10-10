// Generated from current Elixir source. Do not edit.
module app {
  // src: lib/preservation.ex:4
  pure val Preservation_init_0: { pending: bool, saved: bool, work: bool } = { work: true, saved: false, pending: false }
  // src: lib/preservation.ex:48
  pure def Preservation_cleanup_ready_1(arg0: { pending: bool, saved: bool, work: bool }): bool = (arg0).pending
  // src: lib/preservation.ex:52
  pure def Preservation_retire_1(arg0: { pending: bool, saved: bool, work: bool }): { pending: bool, saved: bool, work: bool } = { pending: false, saved: (arg0).saved, work: false }
  // src: lib/preservation.ex:40
  pure def Preservation_cleanup_1(arg0: { pending: bool, saved: bool, work: bool }): { pending: bool, saved: bool, work: bool } = (if (Preservation_cleanup_ready_1(arg0)) Preservation_retire_1(arg0) else arg0)
  // src: lib/preservation.ex:24
  pure def Preservation_cleanup_event_2(arg0: { pending: bool, saved: bool, work: bool }, arg1: str): { pending: bool, saved: bool, work: bool } = (if (((arg1 == "cleanup") or (arg1 == "retry"))) Preservation_cleanup_1(arg0) else arg0)
  // src: lib/preservation.ex:36
  pure def Preservation_failed_1(arg0: { pending: bool, saved: bool, work: bool }): { pending: bool, saved: bool, work: bool } = { pending: (arg0).work, saved: (arg0).saved, work: (arg0).work }
  // src: lib/preservation.ex:16
  pure def Preservation_dispatch_2(arg0: { pending: bool, saved: bool, work: bool }, arg1: str): { pending: bool, saved: bool, work: bool } = (if ((arg1 == "preserve_fail")) Preservation_failed_1(arg0) else Preservation_cleanup_event_2(arg0, arg1))
  // src: lib/preservation.ex:32
  pure def Preservation_preserve_1(arg0: { pending: bool, saved: bool, work: bool }): { pending: bool, saved: bool, work: bool } = { pending: (arg0).work, saved: ((arg0).saved or (arg0).work), work: (arg0).work }
  // src: lib/preservation.ex:8
  pure def Preservation_step_2(arg0: { pending: bool, saved: bool, work: bool }, arg1: str): { pending: bool, saved: bool, work: bool } = (if ((arg1 == "preserve_ok")) Preservation_preserve_1(arg0) else Preservation_dispatch_2(arg0, arg1))
}
