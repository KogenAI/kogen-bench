Feature: The leftover child test outlives the shortened process group wait
  This feature covers the test method test_leftover_child_is_unknown_without_post_reap_signal in test_common.py, which must exercise a grandchild that outlives the group wait bound without changing common.py.

  Scenario: The test method passes alone
    When bench-leftover-child-test-outlives-group-wait: the method test_leftover_child_is_unknown_without_post_reap_signal is run alone once with python3 -m unittest
    Then bench-leftover-child-test-outlives-group-wait: the run reports one test and OK with no skip and no failure

  Scenario: The grandchild outlives the shortened bound and exits by itself
    When bench-leftover-child-test-outlives-group-wait: the same method is run once with a recorder of signals and of the leftover group lifetime
    Then bench-leftover-child-test-outlives-group-wait: the test passed and CustodyUnknown was raised while the wait bound was 0.3 seconds
    Then bench-leftover-child-test-outlives-group-wait: the group was still alive right after the raise, then disappeared by itself within 6 seconds with no signal sent

  Scenario: Only test_common.py changes
    When bench-leftover-child-test-outlives-group-wait: the bytes of common.py and test_memcap.py and the list of changed files are read
    Then bench-leftover-child-test-outlives-group-wait: common.py and test_memcap.py are byte-identical to the base tree and test_common.py is the only changed file
