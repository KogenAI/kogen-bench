@core:§7
Feature: User-visible Kogen commits follow Git configuration and hooks

  @core:§7 @core:§4.6 @quint:git.createLanding @quint:git.trustedSettings @quint:landing.invariant
  Scenario: A landed Build is one ordinary commit with the sole Kogen Intent trailer
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Existing project.
      """
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
    Given fake provider script "farewell-build" is configured with auth "valid"
    When I run "kogen queue start"
    Then the exit code is 0
    Then branch "main" has head commit with only trailer "Kogen-Intent: farewell"

  @core:§7 @core:§4.6 @quint:git.safeObjects @quint:landing.invariant
  Scenario: A failing user pre-commit hook prevents branch publication
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Existing project.
      """
    When I run "kogen init"
    Then the exit code is 0
    Given project check "contract" returns "pass" within 1000 milliseconds and Build budget 3600000 milliseconds
    Given executable file ".git/hooks/pre-commit" contains:
      """
      #!/bin/sh
      echo "hook fixture failed" >&2
      exit 1
      """
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
    Given fake provider script "farewell-build-hook" is configured with auth "valid"
    When I run "kogen queue start"
    Then the exit code is 1
    Then there is no new commit
    Then the file "goodbye.txt" is absent
