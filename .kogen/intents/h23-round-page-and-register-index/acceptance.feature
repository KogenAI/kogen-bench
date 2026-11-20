Feature: Publish the h23 round page and register the round

  This feature checks that the h23 DESCRIPTIVE round page exists with the retained bytes and that the round is registered in the round register, the round index and the reproduction inventory.

  Scenario: The round page is the retained page and alone in its directory
    Given h23-round-page-and-register-index: the repository working tree
    Then h23-round-page-and-register-index: the round page equals the retained page and the round directory holds only the allowed files

  Scenario: The round register lists the round
    Given h23-round-page-and-register-index: the repository working tree
    Then h23-round-page-and-register-index: the round register is the earlier register, one blank line and the retained bullet line

  Scenario: The index and the inventory register the round
    Given h23-round-page-and-register-index: the repository working tree
    Then h23-round-page-and-register-index: the index and the inventory each keep the earlier entries in order and gain exactly one new last entry for the round
