@core:§3
Feature: The Kogen command line is a fixed contract

  @core:§3 @quint:cli.topCommands @quint:cli.validateInvocation
  Scenario: Top-level help lists implemented commands and the reserved update command
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen help"
    Then the exit code is 0
    Then stdout contains "kogen init"
    Then stdout contains "kogen queue start"
    Then stdout contains "kogen provider login chatgpt"
    Then stdout contains "kogen update"

  @core:§3 @quint:cli.validateInvocation @quint:cli.queueExit
  Scenario: Content and undeclared model options are rejected by argv parsing
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen intent shape farewell Write goodbye.txt with Goodbye"
    Then the exit code is 2
    When I run "kogen queue start --model gpt-6-luna"
    Then the exit code is 2

  @core:§3 @quint:cli.boardOrder @quint:cli.intentRow @quint:status.observe
  Scenario: Text and JSONL status expose a shaped draft
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given fake provider script "basic-farewell" is configured with auth "valid"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 0
    When I run "kogen status"
    Then stdout contains "Drafts"
    Then stdout contains "farewell"
    Then "kogen status --json" JSONL output has an intent row with status "draft"

  @core:§3 @quint:cli.watchStart @quint:cli.queueBackground @quint:cli.stopActiveQueue @quint:status.watchDone @quint:queue.start @quint:queue.serial
  Scenario: A detached queue completes its current Build after stop while watch observes changed state
    Given a temporary HOME and a Git repository on branch "main"
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
    Given fake provider script "farewell-build-held" is configured with auth "valid"
    When I run "kogen queue start --detach"
    Then the exit code is 0
    When I wait for provider script "farewell-build-held" at gate "builder-next-turn"
    When I start "kogen status --watch" in the background as "watch"
    Then background command "watch" prints a frame containing "Building"
    When I run "kogen queue stop"
    Then the exit code is 0
    When I release provider script "farewell-build-held" at gate "builder-next-turn"
    Then background command "watch" eventually exits with code 0
    Then background command "watch" prints a frame containing "Landed"
    Then "kogen status --json" JSONL output has an intent row with status "landed"
