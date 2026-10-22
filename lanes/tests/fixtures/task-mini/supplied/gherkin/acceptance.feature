Feature: Add two numbers

  Scenario: the sum of two numbers is returned
    When I add 2 and 3
    Then the result is 5

  Scenario: negative numbers are summed too
    When I add -2 and 3
    Then the result is 1
