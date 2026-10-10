@core:§5
Feature: Durable Kogen state reconciles dead Builds and expires recovery

  @core:§5 @core:§6 @quint:recovery.terminalize @quint:recovery.preserveAll @quint:recovery.lifecycleValid @quint:recovery.configuredRetention @quint:recovery.expireAll @quint:recovery.safe @quint:cli.recoverySummary @quint:kogen_io.Seam
  Scenario: A crashed Build remains unverified and its preserved recovery expires on the test clock
    Given a temporary HOME and a Git repository on branch "main"
    Given Kogen's test clock starts at 1700000000000 milliseconds
    When I run "kogen init"
    Then the exit code is 0
    Given project check "contract" returns "pass" within 1000 milliseconds and Build budget 3600000 milliseconds
    Given fake provider script "basic-farewell" is configured with auth "valid"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 0
    When I run "kogen intent approve farewell"
    Then the exit code is 5
    Then stdout captures the Intent approval hash as "approval_hash"
    When I run "kogen intent approve farewell {{approval_hash}} --by Ada"
    Then the exit code is 0
    Given fake provider script "farewell-build-crash" is configured with auth "valid"
    When I run "kogen queue start --detach"
    Then the exit code is 0
    When I wait for provider script "farewell-build-crash" at gate "crash-after-edit"
    When I run "kogen status --json"
    When I kill the trace-owned detached Kogen queue process
    When I run "kogen status"
    Then the latest status output reports a failed or interrupted intent with preserved unverified recovery and an expiry
    When I advance Kogen's test clock by 1209600000 milliseconds
    When I run "kogen status"
    Then status confirms expired recovery is removed and deletion is journaled
