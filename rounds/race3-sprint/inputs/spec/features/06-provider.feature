@core:§6
Feature: ChatGPT account selection and the local provider test seam

  @core:§3 @core:§6 @core:§5 @quint:cli.providerLogin @quint:cli.providerUse @quint:cli.providerLogout @quint:cli.providerList @quint:kogen.provider @quint:kogen_io.seamEnvironment @quint:kogen_io.validSeam
  Scenario: Login, project account use, and logout affect only the selected machine account
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given fake OpenID script "login-default" is configured
    When I run "kogen provider login chatgpt"
    Then the exit code is 0
    Then stdout contains "default"
    Given fake OpenID script "login-research" is configured
    When I run "kogen provider login chatgpt --as research"
    Then the exit code is 0
    Then stdout contains "research"
    When I run "kogen provider use chatgpt --as research --project @repo"
    Then the exit code is 0
    Then provider account choices are under temporary HOME and absent from repository
    Given fake provider script "research-account-shape" is configured with auth "absent"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 0
    Given fake OpenID script "logout-research" is configured
    When I run "kogen provider logout chatgpt --as research"
    Then the exit code is 0
    When I run "kogen provider list"
    Then the exit code is 0
    Then stdout contains "default"
    Then stdout contains "signed in"

  @core:§6 @quint:kogen_io.validInjected @quint:kogen_io.ProviderEndpoint
  Scenario: Injected auth calls the fake endpoint without becoming a saved login
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given fake provider script "basic-farewell" is configured with auth "valid"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 0
    Then the file "~/.kogen/accounts.yaml" is absent

  @core:§6 @quint:kogen.provider @quint:kogen_io.validInjected @quint:kogen_io.ProviderEndpoint
  Scenario: Expired injected auth is rejected before any fake provider request
    Given a temporary HOME and a Git repository on branch "main"
    When I run "kogen init"
    Then the exit code is 0
    Given fake provider script "no-provider-turns" is configured with auth "expired"
    When I run "kogen intent shape farewell -" with stdin:
      """
      Write goodbye.txt with Goodbye.
      """
    Then the exit code is 4
