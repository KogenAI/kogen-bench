Feature: Word-frequency report

  Scenario: words are ordered by count and then by word
    Given the input text:
      """
      pear apple pear fig apple pear zed
      """
    When I run wordfreq with no arguments
    Then the exit status is 0
    And stdout is:
      """
      pear 3
      apple 2
      fig 1
      zed 1
      """
    And stderr is empty

  Scenario: case is folded and punctuation separates words
    Given the input text:
      """
      The THE the Cat, cat; dog
      """
    When I run wordfreq with no arguments
    Then the exit status is 0
    And stdout is:
      """
      the 3
      cat 2
      dog 1
      """

  Scenario: a non-ASCII byte separates words
    Given the input bytes "cafÃ© cafÃ© naÃ¯ve"
    When I run wordfreq with no arguments
    Then the exit status is 0
    And stdout is:
      """
      caf 2
      na 1
      ve 1
      """

  Scenario: min keeps words that occur at least N times
    Given the input text:
      """
      c c c b b a
      """
    When I run wordfreq with "--min 2"
    Then the exit status is 0
    And stdout is:
      """
      c 3
      b 2
      """

  Scenario: top keeps the first N words after min
    Given the input text:
      """
      c c c b b a
      """
    When I run wordfreq with "--min 2 --top 1"
    Then the exit status is 0
    And stdout is:
      """
      c 3
      """

  Scenario: json prints one array line
    Given the input text:
      """
      b a b
      """
    When I run wordfreq with "--format json"
    Then the exit status is 0
    And stdout is:
      """
      [{"word":"b","count":2},{"word":"a","count":1}]
      """
    And stderr is empty

  Scenario: json with no words is an empty array
    Given the input text:
      """
      , ;
      """
    When I run wordfreq with "--format json"
    Then the exit status is 0
    And stdout is:
      """
      []
      """

  Scenario: a path argument reads that file
    Given a file "notes" containing:
      """
      file file other
      """
    When I run wordfreq with "@notes --top 1"
    Then the exit status is 0
    And stdout is:
      """
      file 2
      """

  Scenario: a lone dash reads stdin
    Given the input text:
      """
      x x y
      """
    When I run wordfreq with "-"
    Then the exit status is 0
    And stdout is:
      """
      x 2
      y 1
      """

  Scenario: a repeated option is reported before its value is checked
    When I run wordfreq with "--top 1 --top"
    Then the exit status is 2
    And stdout is empty
    And stderr is "wordfreq: duplicate option '--top'"

  Scenario: a bad value is reported with the flag
    When I run wordfreq with "--min 0"
    Then the exit status is 2
    And stdout is empty
    And stderr is "wordfreq: invalid value for '--min': '0'"

  Scenario: an unknown option is an argument error
    When I run wordfreq with "--min=2"
    Then the exit status is 2
    And stderr is "wordfreq: unknown option '--min=2'"

  Scenario: a second input path is an argument error
    When I run wordfreq with "one.txt two.txt"
    Then the exit status is 2
    And stderr is "wordfreq: expected at most one input path"

  Scenario: a missing file is a runtime error
    When I run wordfreq with "@missing"
    Then the exit status is 1
    And stdout is empty
    And stderr is "wordfreq: cannot read input"
