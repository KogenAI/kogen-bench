Feature: Room booking conflict checker

  Scenario: help prints the exact usage
    When I run kogen with "--help"
    Then the exit status is 0
    And stdout is:
      """
      Usage: kogen-sched [--gap MINUTES] [--room ROOM] [--format text|json] [--strict] [FILE|-]
      Report conflicting room bookings from FILE or stdin.
      """

  Scenario: bookings without overlap report no conflict
    Given the input text:
      """
      a AB001 09:00 10:00
      a AB002 10:00 11:00
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      bookings=2 conflicts=0
      """

  Scenario: an overlap is reported with its length
    Given the input text:
      """
      lab AB001 09:00 10:00
      lab AB002 09:45 11:00
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      CONFLICT lab AB001 AB002 overlap=15
      bookings=2 conflicts=1
      """

  Scenario: a gap setting reports bookings that start too soon
    Given the input text:
      """
      r AB001 09:00 10:00
      r AB002 10:03 11:00
      """
    When I run kogen with "--gap 5"
    Then the exit status is 0
    And stdout is:
      """
      CONFLICT r AB001 AB002 gap=3
      bookings=2 conflicts=1
      """

  Scenario: rooms do not conflict with each other
    Given the input text:
      """
      a AB001 09:00 10:00
      b AB002 09:00 10:00
      """
    When I run kogen with no arguments
    Then stdout is:
      """
      bookings=2 conflicts=0
      """

  Scenario: JSON output lists the conflicts
    Given the input text:
      """
      r AB001 09:00 10:00
      r AB002 09:30 10:00
      """
    When I run kogen with "--format json"
    Then the exit status is 0
    And stdout is:
      """
      {"bookings":2,"conflicts":[{"room":"r","first":"AB001","second":"AB002","overlap":30}]}
      """

  Scenario: strict mode exits 3 when there are conflicts
    Given the input text:
      """
      r AB001 09:00 10:00
      r AB002 09:30 10:00
      """
    When I run kogen with "--strict"
    Then the exit status is 3

  Scenario: an end before the start is reported on its line
    Given the input text:
      """
      # bookings
      r AB001 10:00 09:00
      """
    When I run kogen with no arguments
    Then the exit status is 1
    And stderr is "sched:2: end must be after start"

  Scenario: a duplicate id is refused
    Given the input text:
      """
      a AB001 09:00 10:00
      b AB001 11:00 12:00
      """
    When I run kogen with no arguments
    Then the exit status is 1
    And stderr is "sched:2: duplicate id 'AB001'"

  Scenario: a gap above 120 is an invalid value
    When I run kogen with "--gap 200"
    Then the exit status is 2
    And stderr is "sched: invalid value for '--gap': '200'"
