// Generated from current Elixir source. Do not edit.
module app {
  // src: lib/workflow.ex:4
  pure val Workflow_init_0: { admitted: bool, approved: str, revision: str } = { revision: "r1", approved: "none", admitted: false }
  // src: lib/workflow.ex:36
  pure def Workflow_approve_1(arg0: { admitted: bool, approved: str, revision: str }): { admitted: bool, approved: str, revision: str } = { admitted: (arg0).admitted, approved: (arg0).revision, revision: (arg0).revision }
  // src: lib/workflow.ex:40
  pure def Workflow_edit_2(arg0: { admitted: bool, approved: str, revision: str }, arg1: str): { admitted: bool, approved: str, revision: str } = { admitted: false, approved: (arg0).approved, revision: arg1 }
  // src: lib/workflow.ex:24
  pure def Workflow_edit_event_2(arg0: { admitted: bool, approved: str, revision: str }, arg1: str): { admitted: bool, approved: str, revision: str } = (if ((arg1 == "edit_r1")) Workflow_edit_2(arg0, "r1") else (if ((arg1 == "edit_r2")) Workflow_edit_2(arg0, "r2") else arg0))
  // src: lib/workflow.ex:48
  pure def Workflow_admission_1(arg0: { admitted: bool, approved: str, revision: str }): bool = ((arg0).approved != "none")
  // src: lib/workflow.ex:44
  pure def Workflow_start_1(arg0: { admitted: bool, approved: str, revision: str }): { admitted: bool, approved: str, revision: str } = { admitted: Workflow_admission_1(arg0), approved: (arg0).approved, revision: (arg0).revision }
  // src: lib/workflow.ex:16
  pure def Workflow_dispatch_2(arg0: { admitted: bool, approved: str, revision: str }, arg1: str): { admitted: bool, approved: str, revision: str } = (if ((arg1 == "start")) Workflow_start_1(arg0) else Workflow_edit_event_2(arg0, arg1))
  // src: lib/workflow.ex:8
  pure def Workflow_step_2(arg0: { admitted: bool, approved: str, revision: str }, arg1: str): { admitted: bool, approved: str, revision: str } = (if ((arg1 == "approve")) Workflow_approve_1(arg0) else Workflow_dispatch_2(arg0, arg1))
}
