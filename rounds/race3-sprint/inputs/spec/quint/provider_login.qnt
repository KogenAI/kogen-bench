// A changed provider subject cannot replace a saved account without a decision.
module provider_login {
  import kogen_io.* from "./kogen_io"
  type State = {
    phase: str, savedLabel: str, savedSubject: str, newLabel: str, newSubject: str,
    oauthSubject: str, replacementConfirmed: bool, loginCount: int, saveCount: int
  }
  pure val initial: State = {
    phase: "oauth-complete", savedLabel: "default", savedSubject: "subject-A",
    newLabel: "", newSubject: "", oauthSubject: "subject-B",
    replacementConfirmed: false, loginCount: 1, saveCount: 0
  }
  pure def nonTty(s: State): State =
    if (s.phase == "oauth-complete" and s.oauthSubject != s.savedSubject)
      { ...s, phase: "decision-needed" }
    else s
  pure def saveNew(s: State, label: str, valid: bool, available: bool): State =
    if (s.phase == "oauth-complete" and s.oauthSubject != s.savedSubject and
        valid and available and label != "" and label != s.savedLabel)
      { ...s, phase: "saved-new", newLabel: label, newSubject: s.oauthSubject, saveCount: s.saveCount + 1 }
    else s
  pure def selectReplace(s: State): State =
    if (s.phase == "oauth-complete" and s.oauthSubject != s.savedSubject)
      { ...s, phase: "confirm-replacement" }
    else s
  pure def confirmReplace(s: State, confirmed: bool): State =
    if (s.phase != "confirm-replacement") s
    else if (confirmed)
      { ...s, phase: "saved-replaced", savedSubject: s.oauthSubject,
        replacementConfirmed: true, saveCount: s.saveCount + 1 }
    else { ...s, phase: "decision-needed" }
  pure def safe(s: State): bool = and {
    s.loginCount == 1, s.saveCount >= 0, s.saveCount <= 1,
    s.savedSubject != "subject-A" implies and {
      s.phase == "saved-replaced", s.replacementConfirmed, s.saveCount == 1
    },
    s.newSubject != "" implies and {
      s.phase == "saved-new", s.newLabel != "", s.savedSubject == "subject-A",
      s.newSubject == s.oauthSubject, s.saveCount == 1
    },
    s.phase == "decision-needed" implies and {
      s.savedSubject == "subject-A", s.newSubject == "", s.saveCount == 0
    },
    s.phase == "confirm-replacement" implies and {
      s.savedSubject == "subject-A", not(s.replacementConfirmed), s.saveCount == 0
    }
  }
  run nonTtyKeepsSavedAccountAndRequestsDecisionTest = {
    val pending = nonTty(initial)
    init.expect(and {
      pending.phase == "decision-needed", pending.savedSubject == "subject-A",
      pending.newSubject == "", pending.loginCount == 1, safe(pending)
    })
  }
  run newLabelSavesCompletedLoginAndKeepsOldAccountTest = {
    val saved = saveNew(initial, "alex", true, true)
    init.expect(and {
      saved.phase == "saved-new", saved.savedSubject == "subject-A",
      saved.newSubject == "subject-B", saved.newLabel == "alex",
      saved.loginCount == 1, saved.saveCount == 1, safe(saved)
    })
  }
  run replacementNeedsSeparateConfirmationTest = {
    val pending = selectReplace(initial)
    val saved = confirmReplace(pending, true)
    init.expect(and {
      pending.savedSubject == "subject-A", pending.phase == "confirm-replacement",
      saved.savedSubject == "subject-B", saved.replacementConfirmed,
      saved.loginCount == 1, saved.saveCount == 1, safe(saved)
    })
  }
  run declinedReplacementKeepsOldAccountTest = {
    val declined = confirmReplace(selectReplace(initial), false)
    init.expect(and {
      declined.phase == "decision-needed", declined.savedSubject == "subject-A",
      not(declined.replacementConfirmed), declined.saveCount == 0, safe(declined)
    })
  }
  run invalidOrOccupiedNewLabelCannotBeSavedTest = {
    val invalid = saveNew(initial, "bad label", false, true)
    val occupied = saveNew(initial, "taken", true, false)
    init.expect(and { invalid == initial, occupied == initial, safe(invalid), safe(occupied) })
  }
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, lastStep' = [], ioSeam' = defaultSeam }
  action step = any {
    all { st' = nonTty(st), lastStep' = [], ioSeam' = ioSeam },
    all { st' = saveNew(st, "alex", true, true), lastStep' = [], ioSeam' = ioSeam },
    all { st' = saveNew(st, "bad label", false, true), lastStep' = [], ioSeam' = ioSeam },
    all { st' = saveNew(st, "taken", true, false), lastStep' = [], ioSeam' = ioSeam },
    all { st' = selectReplace(st), lastStep' = [], ioSeam' = ioSeam },
    all { st' = confirmReplace(st, true), lastStep' = [], ioSeam' = ioSeam },
    all { st' = confirmReplace(st, false), lastStep' = [], ioSeam' = ioSeam }
  }
  val invariant = safe(st)
}
