@M
Feature: Frozen maintenance priority extension
  Priority changes queued build dispatch and is exposed through existing messages.
  The repository landing lane remains FIFO by original acceptance sequence.

  Background:
    Given a fresh data directory and two private worker work directories
    And a bare repository "r1" with branch "main" and base commit "base1"
    And a coordinator listening on a reserved localhost port

  @M01
  Scenario: Omitted priority normalizes to normal across the public contract
    When I submit "j1" with the six base fields and no priority
    Then submit exits 0 with seq 1
    And status and wait expose priority "normal"
    And the worker assignment exposes priority "normal"
    When I resubmit "j1" with explicit priority "normal"
    Then submit exits 0 with seq 1 and duplicate true

  @M02
  Scenario: High priority is accepted and invalid values do not mutate acceptance
    When I submit "j1" with priority "high"
    Then submit exits 0 and status exposes priority "high"
    When I submit new IDs with priority null, "urgent", and a non-string value
    Then each submit exits 2 with INVALID_JOB
    And no invalid submission allocates a sequence or adds a job record

  @M03
  Scenario: High priority dispatches first without preempting running work
    Given "j1" has priority "normal" and is assigned to worker "w1"
    When I accept "j2" with priority "high"
    And worker "w2" becomes available
    Then "j2" is assigned before queued normal-priority jobs
    And "j1" remains running on "w1" with its original attempt and is not preempted

  @M04
  Scenario: Priority FIFO order survives lease requeue
    Given "j1" and "j2" have priority "high" in that acceptance order
    And "j3" has priority "normal"
    When the worker owning "j1" dies and its lease expires
    Then "j1" is requeued with priority "high" and its original acceptance sequence
    And "j1" is assigned before "j2" and "j3"
    And within each priority, lower original acceptance sequence dispatches first

  @M05
  Scenario: Priority does not change per-repository landing FIFO
    Given earlier "j1" has priority "normal" and later "j2" has priority "high"
    And "j2" finishes its initial build before "j1"
    When both jobs become ready
    Then "j2" cannot enter landing before "j1" is terminal
    And the repository lands "j1" then "j2" with at most one active landing

  @M06
  Scenario: Normalized priority identity and ordering survive restart
    Given "j1" is accepted with omitted priority and "j2" with priority "high"
    When I restart the coordinator and resubmit "j1" with explicit priority "normal"
    Then the replay is duplicate true with the original sequence
    And status preserves "j1" as normal and "j2" as high
    When I resubmit "j1" with priority "high"
    Then submit exits 2 with ID_CONFLICT and does not change state
    And the next dispatch still follows priority then original acceptance sequence
