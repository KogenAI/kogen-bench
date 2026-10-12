@F
Feature: Recovery and descendant containment under process faults
  Independent containment must survive application process deaths.
  Every SIGKILL targets a recorded fixture PID rather than a process-name match.

  Background:
    Given a fresh data directory and two private worker work directories
    And a bare repository "r1" with branch "main" and base commit "base1"
    And a coordinator listening on a reserved localhost port

  @F01
  Scenario: An acknowledged running job survives coordinator SIGKILL
    Given worker "w1" is ready and "w2" is not started
    And accepted "j1" is held in its initial command with a known lease deadline
    When I SIGKILL the coordinator and restart it with the same data and port
    Then "j1" remains queryable with its original input, seq, and acceptance time
    And no old lease is extended by restart
    And the old attempt descendants are dead by their recorded lease deadline
    When a fresh worker session is ready and the fixture permits retry success
    Then "j1" lands once with a higher attempt

  @F02
  Scenario: Coordinator death during a gated landing rerun preserves ordering
    Given both workers are ready
    And "j1" is held in its landing command before intent preparation
    And a later nonconflicting "j2" for "r1" is ready
    When I SIGKILL and restart the coordinator
    Then neither job is lost and "j2" cannot overtake "j1"
    And the old landing command tree is dead by its original deadline
    When workers reconnect after cleanup and the fixture permits retry success
    Then the target history contains "j1", "j2" in that order exactly once

  @F03
  Scenario: A crash racing with a successful landing cannot duplicate its commit
    Given worker "w1" is ready and "j1" is held in its landing command
    When I release the landing gate and SIGKILL the coordinator while observing the target head
    And I restart the coordinator with the same data and port
    And I allow any unprepared retry to complete
    Then "j1" eventually has one immutable landed_commit
    And the branch contains exactly one commit named "kogen-mini: j1"
    And the candidate recorded by any observed prepared intent is the recovered landed_commit
    When I restart the coordinator again and resubmit identical "j1"
    Then no additional commit or terminal-state change occurs

  @F04
  Scenario: Worker SIGKILL expires its lease and retries on a second worker
    Given worker "w1" owns running "j1" behind an initial build gate
    And worker "w2" is ready and idle
    When I SIGKILL worker "w1" immediately after observing a renewal
    Then "j1" is queued or has a higher attempt within one second after that lease expires
    And the replacement attempt does not overlap any live old descendant
    When I permit the replacement initial and landing commands to pass
    Then "j1" lands once on "w2" with a higher attempt

  @F05
  Scenario: An expired worker token cannot affect a replacement attempt
    Given a protocol fixture worker owns "j1" and records its session and lease token
    When the fixture stops heartbeating until the lease expires
    And a fresh worker acquires a higher attempt for "j1"
    And the old fixture sends its old heartbeat and an unsaved success result
    Then each reply is STALE_LEASE or STALE_SESSION as its session lifetime dictates
    And status still identifies the replacement attempt and owner
    And the stale messages never advance the target or extend the old deadline

  @F06
  Scenario: Cancellation kills double-fork and setsid descendants
    Given worker "w1" runs "j1" whose command registers a double-fork setsid child and waits
    And the full fixture PID registry is confirmed alive
    When I cancel "j1" while the worker and coordinator are connected
    Then the durable cancellation request cannot be overwritten by success
    And every registered descendant is dead within two seconds
    And wait exits 1 with cancelled and user_cancelled
    And the target has not advanced

  @F07
  Scenario: Command timeout kills the entire detached descendant tree
    Given worker "w1" runs "j1" with timeout_s 2 and a registered detached descendant tree
    When the command budget expires
    Then all registered descendants are dead within one second after the budget
    And wait exits 1 with timed_out and build_timeout
    And no target commit for "j1" exists
    And timeout does not require cancellation or worker restart

  @F08
  Scenario: Worker SIGKILL does not require restart to reap detached children
    Given worker "w1" runs "j1" with a registered double-fork setsid tree
    When I record the acknowledged lease deadline and SIGKILL worker "w1"
    And I do not restart "w1"
    Then every registered descendant is dead by the recorded hard deadline
    And the coordinator exposes retry within one second after that deadline
    And no stale attempt commit reaches the target

  @F09
  Scenario: Containment still expires when both application processes are killed
    Given worker "w1" runs "j1" with a registered detached descendant tree
    When I record the acknowledged lease deadline
    And I SIGKILL the worker and coordinator without restarting either
    Then every registered descendant is dead by the original hard deadline
    When I restart the coordinator and start a fresh worker session
    Then the accepted job is present and retries without overlapping the old tree
    And it can land exactly once after the fixture allows success

  @F10
  Scenario: Terminal records and acceptance survive repeated coordinator restarts
    Given "j1" has landed and "j2" has failed its initial build
    When I SIGKILL and restart the coordinator three times on the same data directory
    Then both terminal records remain exactly equal to their saved records
    And status order, seq values, next_seq, and target history are unchanged
    When I submit a new "j3"
    Then its acceptance sequence is the next unused sequence

  @F11
  Scenario: Graceful worker shutdown cleans descendants before immediate retry
    Given worker "w1" runs "j1" with a registered detached descendant tree
    And worker "w2" is ready and idle
    When I SIGTERM worker "w1"
    Then "w1" exits 0 after every registered descendant is dead
    And "w1" exits within two seconds of SIGTERM
    And the coordinator exposes a queued or higher-attempt "j1" within one second of shutdown acknowledgement
    And no old descendant overlaps the replacement command
    When the replacement fixture is permitted to pass
    Then "j1" lands once

  @F12
  Scenario: Cancellation and timeout during landing leave the target unchanged
    Given worker "w1" runs "j1" behind a landing gate with a detached descendant tree
    When I cancel "j1" before any prepared intent exists
    Then the whole landing command tree is killed within two seconds
    And "j1" is cancelled with no target commit
    Given worker "w1" runs a new "j2" whose initial build passes and landing command has timeout_s 2
    When that landing command times out with detached descendants
    Then its whole tree is dead within one second after the budget
    And "j2" is rejected with landing_timeout
    And "r1" remains at "base1"
