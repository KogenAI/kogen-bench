@core:§4
Feature: Kogen initializes, shapes, approves, builds, checks, and lands work

  @core:§3 @core:§4.1 @core:§7 @quint:cli.initCommand @quint:init.runInit @quint:init.initializeFiles @quint:init.initGitExpectation @quint:git.initialize
  Scenario: Init preserves existing ignore rules and commits exactly its two paths
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Welcome.
      """
    Given file ".gitignore" contains:
      """
      # keep this rule
      *.tmp
      """
    When I run "kogen init"
    Then the exit code is 0
    Then the file ".gitignore" includes text "# keep this rule"
    Then Git ignores path ".kogen/local/"
    Then Git does not ignore path ".kogen/project.yaml"
    Then the last commit changes exactly:
      """
      .gitignore
      .kogen/project.yaml
      """
    Then branch "main" has head commit subject "Initialize Kogen project"

  @core:§3 @core:§4.1 @core:§7 @quint:cli.initCommand @quint:init.runInit @quint:init.safe @quint:config.required @quint:git.initialize
  Scenario: Init creates the exact bare config and initial history commit
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Then the file ".kogen/project.yaml" contains:
      """
      name: project
      checks: []
      """
    Then the last commit changes exactly:
      """
      .gitignore
      .kogen/project.yaml
      """
    Then branch "main" has head commit subject "Initial commit"

  @core:§3 @core:§4.1 @quint:cli.initCommand @quint:init.runInit @quint:config.schemaIssues
  Scenario: Init is a no-op for an existing valid config
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Existing project.
      """
    Given file ".kogen/project.yaml" contains:
      """
      name: existing
      checks: []
      """
    When I run "kogen init"
    Then the exit code is 0
    Then there is no new commit
    Then the file ".kogen/project.yaml" contains:
      """
      name: existing
      checks: []
      """

  @core:§3 @core:§4.1 @quint:cli.initCommand @quint:config.schemaIssues @quint:init.runInit
  Scenario: Config validation rejects duplicate YAML keys
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Existing project.
      """
    Given file ".kogen/project.yaml" contains:
      """
      name: project
      name: duplicate
      checks: []
      """
    When I run "kogen init"
    Then the exit code is 3
    Then there is no new commit

  @core:§3 @core:§4.1 @quint:cli.initCommand @quint:config.schemaIssues @quint:init.runInit
  Scenario: Config validation rejects unknown keys at the top level
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Existing project.
      """
    Given file ".kogen/project.yaml" contains:
      """
      name: project
      checks: []
      credentials:
        account: personal
      """
    When I run "kogen init"
    Then the exit code is 3
    Then there is no new commit

  @core:§3 @core:§4.1 @quint:cli.initCommand @quint:config.checkRow @quint:config.projectKeys
  Scenario: Check config rejects shell strings, zero timeouts, and unknown check keys
    Given a temporary HOME and a Git repository on branch "main"
    Given file ".kogen/project.yaml" contains:
      """
      name: project
      checks:
        - name: lint
          argv: cargo test
          timeout_ms: 0
          shell: true
      """
    When I run "kogen init"
    Then the exit code is 3
    Then there is no new commit

  @core:§3 @core:§4.2 @quint:cli.shapeResult @quint:shape.shape @quint:intent.shape
  Scenario: Shape reads the request from a file and returns an unapproved Intent
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given file "request.txt" contains:
      """
      Write goodbye.txt with Goodbye.
      """
    Given fake provider script "basic-farewell" is configured with auth "valid"
    When I run "kogen intent shape farewell request.txt"
    Then the exit code is 0
    Then stdout contains "farewell"
    Then stdout contains "kogen intent approve farewell"

  @core:§3 @core:§4.2 @quint:cli.shapeResult @quint:shape.shape @quint:shape.safe @quint:intent.shape
  Scenario: Shape accepts the same exact request bytes from stdin
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given fake provider script "basic-farewell" is configured with auth "valid"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 0
    Then stdout contains "farewell"
    Then stdout contains "kogen intent approve farewell"

  @core:§3 @core:§4.2 @quint:cli.shapeResult @quint:shape.shape @quint:shape.shapePass
  Scenario: Shape may return branching questions without manufacturing an Intent
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given fake provider script "farewell-questions" is configured with auth "valid"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye, using an appropriate tone.
      """
    Then the exit code is 0
    Then stdout contains "tone"

  @core:§3 @core:§4.3 @quint:cli.reviewCommand @quint:approve.approve @quint:approve.exactApproval
  Scenario: The review card shows an exact hash and approval waits for a caller action
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
    Then stdout contains "kogen intent approve farewell"
    Then "kogen status --json" JSONL output has an intent row with status "draft"
    When I run "kogen intent approve farewell {{approval_hash}} --by Ada"
    Then the exit code is 0

  @core:§3 @core:§4.3 @quint:cli.approveCommand @quint:approve.exactApproval @quint:approve.changedBytesInvalidateTest
  Scenario: Changing one approved Intent byte invalidates the saved approval hash
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
    When I change one byte in the shaped Intent "farewell"
    When I run "kogen intent approve farewell {{approval_hash}} --by Ada"
    Then the exit code is 1

  @core:§3 @core:§4.2 @core:§4.3 @quint:cli.shapeResult @quint:cli.approveCommand @quint:shape.shapePass @quint:shape.cargoBaseValidation @quint:approve.authorize @quint:approve.editBinding @quint:approve.exactApproval
  Scenario: Changing the accepted Rust source bytes invalidates their approval
    Given a temporary HOME and a Git repository on branch "main"
    Given file "Cargo.toml" contains:
      """
      [package]
      name = "greeter"
      version = "0.1.0"
      edition = "2021"
      """
    Given file "src/lib.rs" contains:
      """
      """
    When I run "kogen init"
    Then the exit code is 0
    Given project check "contract" returns "pass" within 1000 milliseconds and Build budget 3600000 milliseconds
    Given fake provider script "cargo-farewell" is configured with auth "valid"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 0
    Then the file ".kogen/local/acceptance/farewell.rs" contains:
      """
      use greeter::farewell_message;
      #[test]
      fn acceptance_a1() {
          assert_eq!(farewell_message(), "Goodbye");
      }
      """
    When I run "kogen intent approve farewell"
    Then the exit code is 5
    Then stdout captures the Intent approval hash as "approval_hash"
    When I run "kogen intent approve farewell {{approval_hash}} --by Ada"
    Then the exit code is 0
    Then the file ".kogen/acceptance/farewell.rs" contains:
      """
      use greeter::farewell_message;
      #[test]
      fn acceptance_a1() {
          assert_eq!(farewell_message(), "Goodbye");
      }
      """
    Given file ".kogen/local/acceptance/farewell.rs" contains:
      """
      use greeter::farewell_message;
      #[test]
      fn acceptance_a1() {
          assert_eq!(farewell_message(), "Hello");
      }
      """
    When I run "kogen intent approve farewell {{approval_hash}} --by Ada"
    Then the exit code is 1

  @core:§3 @core:§4.4 @core:§4.5 @core:§4.6 @quint:cli.queueResult @quint:queue.start @quint:build.complete @quint:check.exactCandidatePassesTest @quint:landing.invariant @quint:git.safeCheckouts
  Scenario: Foreground queue start checks and lands the exact candidate into the checkout
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
    Then the file "goodbye.txt" contains:
      """
      Goodbye
      """
    Then "kogen status --json" JSONL output has an intent row with status "landed"

  @core:§4.5 @quint:check.redCheckFailsTest @quint:check.safe @quint:landing.invariant
  Scenario: A known red project check prevents landing
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given project check "contract" returns "red" within 1000 milliseconds and Build budget 3600000 milliseconds
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
    Then the exit code is 1
    Then there is no new commit
    Then the file "goodbye.txt" is absent
    Then "kogen status --json" JSONL output has an intent row with status "failed"

  @core:§4.5 @quint:check.couldNotCheckNeverVerifiesTest @quint:check.safe @quint:landing.invariant
  Scenario: A timed-out check is could-not-check and cannot land
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given project check "contract" returns "timeout" within 100 milliseconds and Build budget 3600000 milliseconds
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
    Then the exit code is 1
    Then stdout contains "could-not-check"
    Then there is no new commit
    Then the file "goodbye.txt" is absent
    Then "kogen status --json" JSONL output has an intent row with status "blocked"

  @core:§4.4 @core:§4.6 @core:§6 @quint:process.deadlineSafe @quint:build.timeoutPreventsCandidateTest @quint:landing.invariant @quint:kogen_io.validSeam
  Scenario: The absolute Build budget covers the Builder response and blocks landing on expiry
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given project check "contract" returns "pass" within 1000 milliseconds and Build budget 1000 milliseconds
    Given Kogen's time scale is "0.1"
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
    Given fake provider script "farewell-build-delayed" is configured with auth "valid"
    When I run "kogen queue start"
    Then the exit code is 1
    Then there is no new commit
    Then the file "goodbye.txt" is absent

  @core:§4.6 @core:§6 @quint:landing.integrateTurn @quint:landing.movedTip @quint:landing.invariant @quint:git.safeCheckouts @quint:git.exactCandidate @quint:kogen_io.SetupOp
  Scenario: A lost publication CAS rebases on the new tip and rechecks before landing
    Given a temporary HOME and a Git repository on branch "main"
    Given the repository has committed file "README.md" containing:
      """
      Original.
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
    Given landing barrier "before-publication" is armed
    Given landing barrier "after-cas-loss" is armed
    Given fake provider script "farewell-build" is configured with auth "valid"
    When I start "kogen queue start" in the background as "queue"
    When I wait for landing barrier "before-publication" as "publication"
    When I commit on branch "main" with subject "Concurrent update" and file "README.md" containing:
      """
      Updated upstream.
      """
    When I release landing barrier saved as "publication"
    When I wait for landing barrier "after-cas-loss" as "cas_loss"
    When I release landing barrier saved as "cas_loss"
    Then background command "queue" eventually exits with code 0
    Then the file "README.md" contains:
      """
      Updated upstream.
      """
    Then the file "goodbye.txt" contains:
      """
      Goodbye
      """
    Then project check "contract" ran at least 2 times
    Then "kogen status --json" JSONL output has an intent row with status "landed"
