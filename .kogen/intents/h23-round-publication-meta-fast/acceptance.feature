Feature: Make the h23 round pass the release validator

  This feature checks the status row, the README publication metadata and the recompute script of the h23 round, each with one fast command and no model.

  Scenario: The status row and the README metadata are present in the required form
    Given h23-round-publication-meta-fast: the repository working tree
    Then h23-round-publication-meta-fast: STATUS.md has one DESCRIPTIVE row with the three reason codes and the README has the metadata lines and sections

  Scenario: The release validator reports no failure line for the round
    Given h23-round-publication-meta-fast: the repository working tree
    Then h23-round-publication-meta-fast: the release validator reports no failure line for the round

  Scenario: The historical round metadata test passes unchanged
    Given h23-round-publication-meta-fast: the repository working tree
    Then h23-round-publication-meta-fast: the historical round metadata test passes alone and the release test files are unchanged

  Scenario: The recompute script has the exact bytes and prints the task means
    Given h23-round-publication-meta-fast: the repository working tree
    Then h23-round-publication-meta-fast: recompute.py has the exact retained bytes and prints the expected task means

  Scenario: Exactly the three requested paths are changed
    Given h23-round-publication-meta-fast: the repository working tree
    Then h23-round-publication-meta-fast: exactly the three requested paths are changed
