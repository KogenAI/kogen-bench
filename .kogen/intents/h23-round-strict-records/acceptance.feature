Feature: Strict Standard records and declarations for the h23 round
  This feature checks that the h23 round directory holds its four strict record files and nothing else.

  Scenario: records.jsonl holds one record per new attempt
    Given h23-round-strict-records: the h23 round directory with its retained cells.json
    Then h23-round-strict-records: records.jsonl holds one line per new attempt with the slot arm, task and rep

  Scenario: declarations use registered reason codes and match the records
    Given h23-round-strict-records: the h23 round directory with its retained cells.json
    Then h23-round-strict-records: every missing-field declaration uses a registered reason code and matches the records

  Scenario: the four added files hold no private text
    Given h23-round-strict-records: the h23 round directory with its retained cells.json
    Then h23-round-strict-records: the four added files hold no home path, host name, IP address, e-mail address, credential, raw transcript or account meter

  Scenario: the round directory holds exactly six entries
    Given h23-round-strict-records: the h23 round directory with its retained cells.json
    Then h23-round-strict-records: the h23 round directory holds each of README.md, cells.json and the four added files
    And h23-round-strict-records: the h23 round directory holds no file or subdirectory besides those six
