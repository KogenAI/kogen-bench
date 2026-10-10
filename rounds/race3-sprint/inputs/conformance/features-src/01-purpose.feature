@core:§1
Feature: Kogen shapes work through its own ChatGPT Shaper

  @core:§1 @core:§3 @quint:kogen.provider @quint:kogen_io.Cmd @quint:kogen_io.ProviderEndpoint @quint:kogen_io.validInjected @quint:build.shaperRole @quint:shape.shape @quint:shape.safe @quint:cli.shapeResult
  Scenario: The ordinary executable returns an unapproved Intent from the Shaper
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
