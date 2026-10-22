Feature: Bounded integer stack virtual machine

  Scenario: help prints the exact usage without reading input
    Given the input text:
      """
      invalid source
      """
    When I run kogen with "--help"
    Then the exit status is 0
    And stdout is:
      """
      Usage: kogen-vm [--steps N] [--stack N] [FILE|-]
      Run a bounded integer stack program.
      Options:
        --steps N    Maximum instructions executed (default 10000).
        --stack N    Maximum stack depth (default 256).
        --help       Show this help.
      """
    And stderr is empty

  Scenario: arithmetic consumes right then left operands
    Given the input text:
      """
      PUSH 8
      PUSH 3
      SUB
      OUT
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      5
      """
    And stderr is empty

  Scenario: division truncates toward zero
    Given the input text:
      """
      PUSH -7
      PUSH 3
      DIV
      OUT
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      -2
      """
    And stderr is empty

  Scenario: remainder follows the dividend sign
    Given the input text:
      """
      PUSH -7
      PUSH 3
      MOD
      OUT
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      -1
      """
    And stderr is empty

  Scenario: JZ jumps only for zero
    Given the input text:
      """
      PUSH 0
      JZ yes
      PUSH 99
      OUT
      yes:
      PUSH 4
      OUT
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      4
      """

  Scenario: comments need a space before the marker
    Given the input text:
      """
      PUSH 4 # accepted
      OUT
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      4
      """

  Scenario: HALT skips execution but parsing still validates later code
    Given the input text:
      """
      PUSH 7
      OUT
      HALT
      PUSH 1
      OUT
      """
    When I run kogen with no arguments
    Then the exit status is 0
    And stdout is:
      """
      7
      """

  Scenario: a duplicate label is found before an unresolved target
    Given the input text:
      """
      JMP absent
      same:
      same:
      """
    When I run kogen with no arguments
    Then the exit status is 1
    And stdout is empty
    And stderr is "vm:3:1: duplicate label"

  Scenario: whole-input ASCII validation precedes an earlier syntax error
    Given the input bytes "BOGUS\na\u00ff\n"
    When I run kogen with no arguments
    Then the exit status is 1
    And stdout is empty
    And stderr is "vm:2:2: expected ASCII"

  Scenario: the stack limit is configurable
    Given the input text:
      """
      PUSH 1
      PUSH 2
      OUT
      OUT
      """
    When I run kogen with "--stack 1"
    Then the exit status is 1
    And stdout is empty
    And stderr is "vm:2:1: stack overflow"

  Scenario: runtime errors discard earlier output
    Given the input text:
      """
      PUSH 7
      OUT
      PUSH 1
      PUSH 0
      DIV
      """
    When I run kogen with no arguments
    Then the exit status is 1
    And stdout is empty
    And stderr is "vm:5:1: division by zero"

  Scenario: the step limit is checked before the next instruction
    Given the input text:
      """
      PUSH 1
      OUT
      """
    When I run kogen with "--steps 1"
    Then the exit status is 1
    And stdout is empty
    And stderr is "vm:2:1: step limit exceeded"
