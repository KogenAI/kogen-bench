@B
Feature: Durable jobs and ordered landing through the public contract
  The same CLI and JSON-lines decisions apply to both architecture arms.
  Every repository and process in this feature is an isolated temporary fixture.

  Background:
    Given a fresh data directory and two private worker work directories
    And a bare repository "r1" with branch "main" and base commit "base1"
    And a coordinator listening on a reserved localhost port

  @B01
  Scenario: Startup readiness and empty status
    When I run status with --json before starting workers
    Then it exits 0 with version 1 and an empty jobs array
    And coordinator readiness was printed within 10 seconds of launch
    And the coordinator ready line names its canonical data directory and live PID
    And state.json is a complete version 1 snapshot with next_seq 1

  @B02
  Scenario: A patched job passes both builds and lands exactly once
    Given workers "w1" and "w2" are ready
    When I submit "j1" adding a source file whose build checks its content
    Then submit exits 0 with id "j1", seq 1, and duplicate false
    When I wait for "j1" with a 30 second caller budget
    Then wait exits 0 with a complete landed job record
    And "r1" advances by exactly one direct-child commit named "kogen-mini: j1"
    And the landed_commit equals the target branch head
    And exactly two successful command invocations are recorded for "j1"
    And both phase output files contain the fixture's expected output
    And terminal ownership fields are null and reason is null

  @B03
  Scenario: Identical submission is idempotent before and after completion
    When I submit "j1" without any ready worker
    And I resubmit identical normalized input with JSON keys reordered
    Then the second submit exits 0 with seq 1 and duplicate true
    And status contains exactly one queued job with attempt 0
    Given workers "w1" and "w2" are ready
    When "j1" has landed and I submit its identical input again
    Then submit exits 0 with seq 1 and duplicate true
    And neither another attempt nor another target commit is created

  @B04
  Scenario: Validation and conflicting IDs never mutate acceptance
    When I submit "j1" without any ready worker
    And I submit the same ID with a different patch
    Then that submit exits 2 with ID_CONFLICT
    When I submit an input with timeout_s zero
    Then that submit exits 2 with INVALID_JOB
    When I run submit with an unknown flag
    Then it exits 2 without a protocol submission
    And status still contains only "j1" with seq 1
    And state.json still has next_seq 2

  @B05
  Scenario: Caller wait expiry is separate from a job timeout
    When I submit "j1" without any ready worker
    And I wait for "j1" with a zero second caller budget
    Then wait exits 4 with a queued record and does not cancel "j1"
    When I wait for an unknown ID with a zero second caller budget
    Then it exits 2 with NOT_FOUND and no stdout
    And status and the durable input of "j1" are unchanged

  @B06
  Scenario: Faster later builds cannot overtake the repository landing lane
    Given workers "w1" and "w2" are ready
    And "j1" and "j2" make independent nonconflicting additions to "r1"
    And the first command of "j1" is held by an external build gate
    When I submit "j1" followed by "j2"
    Then both jobs have distinct assigned attempts
    And "j2" becomes ready while "j1" remains running
    And the target branch remains at "base1"
    When I release the initial build gate of "j1"
    Then both jobs land with commit subjects ordered "j1", "j2"
    And at most one job for "r1" is landing in each observed status snapshot

  @B07
  Scenario: A different repository can land while an earlier job is blocked
    Given a bare repository "r2" with branch "main" and base commit "base2"
    And workers "w1" and "w2" are ready
    And "j1" on "r1" is held in its initial build
    When I submit "j2" on "r2" with a passing build
    Then "j2" lands while "j1" is still running
    And "r1" remains at "base1"
    And "r2" has exactly one new commit for "j2"

  @B08
  Scenario: An initial build failure releases the lane for a later success
    Given workers "w1" and "w2" are ready
    When I submit "j1" whose initial command exits 7
    And I submit a nonconflicting passing "j2" for the same repository
    Then wait for "j1" exits 1 with failed and build_failed
    And "j2" lands
    And the target history contains "j2" once and no commit for "j1"

  @B09
  Scenario: A patch that cannot apply fails without running its build
    Given workers "w1" and "w2" are ready
    When I submit "j1" with a valid JSON patch string that cannot apply at its base
    Then submission is accepted
    And wait exits 1 with failed and patch_failed
    And no command invocation for "j1" is recorded
    And "r1" remains at "base1"

  @B10
  Scenario: Conflicting patch replay is rejected in the landing lane
    Given workers "w1" and "w2" are ready
    And "j1" and "j2" replace the same base line with different content
    When I submit "j1" followed by "j2" with passing initial builds
    Then "j1" lands
    And wait for "j2" exits 1 with rejected and rebase_failed
    And "r1" contains only the landed effect of "j1"

  @B11
  Scenario: A rebased source must pass a mandatory second build
    Given workers "w1" and "w2" are ready
    And "j1" adds a file that makes the build of "j2" fail
    And "j2" changes a different file and initially builds before "j1" lands
    When I submit "j1" followed by "j2" and release the gates in order
    Then "j1" lands
    And "j2" records a successful initial build and a failed landing build
    And wait for "j2" exits 1 with rejected and landing_build_failed
    And "r1" contains no landed commit for "j2"

  @B12
  Scenario: Queued cancellation is terminal and repeatable
    When I submit "j1" without any ready worker
    And I cancel "j1"
    Then cancel exits 0 with cancelled and cancel_requested true
    And wait for "j1" exits 1 with cancelled and user_cancelled
    When I cancel "j1" again and then start both workers
    Then cancel_requested remains true
    And "j1" never gains an attempt or a target commit
    When I query status without --json
    Then it prints the specified tab-separated header and one cancelled row
