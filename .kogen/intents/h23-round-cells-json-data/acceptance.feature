Feature: Retained cells.json of the h23 round
  This feature checks that the registered h23 round holds its retained raw data file and that the inventory entry lists it.

  Scenario: The round directory holds the retained data file
    Given h23-round-cells-json-data: the repository working tree
    Then h23-round-cells-json-data: the round directory holds only the allowed files and cells.json is the source data with its 18 slots

  Scenario: The inventory entry lists the data file before the page
    Given h23-round-cells-json-data: the repository working tree
    Then h23-round-cells-json-data: the inventory keeps the earlier entries in order and ends with the one h23 entry listing cells.json then the page
