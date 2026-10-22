Feature: UTC cron occurrence finder

  Scenario: help prints the exact usage
    Given the input text:
      """
      invalid record
      """
    When I run kogen with "--help"
    Then the exit status is 0
    And stdout is:
      """
      Usage: kogen-cron [--after YYYY-MM-DDTHH:MM] [--count N] [--format text|json] [FILE|-]
      Find upcoming UTC minutes for named cron expressions.
      Options:
        --after VALUE    Exclusive UTC starting minute (default 2000-01-01T00:00).
        --count N        Occurrences per expression (default 3; range 1..20).
        --format FORMAT  Output text (default) or json.
        --help           Show this help.
      """
    And stderr is empty

  Scenario: the starting minute is excluded
    Given the input text:
      """
      every * * * * *
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 2"
    Then the exit status is 0
    And stdout is:
      """
      every	1	2
      """

  Scenario: lists and stepped ranges select matching minutes
    Given the input text:
      """
      picks 1,3-7/2 * * * *
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 3"
    Then the exit status is 0
    And stdout is:
      """
      picks	1	3	5
      """

  Scenario: day-of-month and day-of-week restrictions use OR
    Given the input text:
      """
      day 0 0 1 * 0
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 3"
    Then the exit status is 0
    And stdout is:
      """
      day	4320	14400	24480
      """

  Scenario: day of week seven aliases Sunday
    Given the input text:
      """
      sunday 0 0 * * 7
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 1"
    Then the exit status is 0
    And stdout is:
      """
      sunday	4320
      """

  Scenario: JSON uses the required ordered compact fields
    Given the input text:
      """
      one 1 0 1 1 *
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 1 --format json"
    Then the exit status is 0
    And stdout is:
      """
      {"schedules":[{"name":"one","runs":[1]}]}
      """

  Scenario: a full-line comment and blank line are ignored
    Given the input text:
      """
      # title

      once 1 0 1 1 *
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 1"
    Then the exit status is 0
    And stdout is:
      """
      once	1
      """

  Scenario: an invalid later record is reported before searching
    Given the input text:
      """
      first * * * * *
      broken 60 * * * *
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 1"
    Then the exit status is 1
    And stdout is empty
    And stderr is "cron:2:8: invalid minute field"

  Scenario: duplicate names are rejected
    Given the input text:
      """
      job * * * * *
      job 0 * * * *
      """
    When I run kogen with "--after 1970-01-01T00:00 --count 1"
    Then the exit status is 1
    And stdout is empty
    And stderr is "cron:2:1: duplicate name"

  Scenario: field syntax errors use the field start column
    Given the input text:
      """
      job * 3-1 * * *
      """
    When I run kogen with no arguments
    Then the exit status is 1
    And stdout is empty
    And stderr is "cron:1:7: invalid hour field"

  Scenario: a tab is rejected before field parsing
    Given the input text:
      """
      job	0 * * * *
      """
    When I run kogen with no arguments
    Then the exit status is 1
    And stdout is empty
    And stderr is "cron:1:4: tab is not allowed"

  Scenario: insufficient occurrences discard all pending output
    Given the input text:
      """
      leap 0 0 29 2 *
      """
    When I run kogen with "--after 2096-03-01T00:00 --count 20"
    Then the exit status is 1
    And stdout is empty
    And stderr is "cron:1:1: not enough occurrences in search horizon"
