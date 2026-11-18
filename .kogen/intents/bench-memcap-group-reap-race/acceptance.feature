Feature: Process group custody check waits for a group that is tearing down
  This feature covers lanes.common._require_group_gone, which decides after a group leader was reaped whether the process group is gone or custody is unknown.

  Scenario: A member that exits shortly after the leader does not make custody unknown
    When bench-memcap-group-reap-race: the leader of a process group is reaped and the last other member exits 0.5 seconds later
    Then bench-memcap-group-reap-race: the group check returns without raising CustodyUnknown
    And bench-memcap-group-reap-race: the group check took at least 0.4 seconds

  Scenario: A member that outlives the wait bound leaves custody unknown
    When bench-memcap-group-reap-race: a member of the process group is still alive after the wait bound, shortened to 0.3 seconds
    Then bench-memcap-group-reap-race: the group check raises CustodyUnknown
    And bench-memcap-group-reap-race: the group check took at least 0.3 seconds

  Scenario: A permission error leaves custody unknown at once
    When bench-memcap-group-reap-race: the group probe raises PermissionError with the default wait bound
    Then bench-memcap-group-reap-race: the group check raises CustodyUnknown
    And bench-memcap-group-reap-race: the group check took less than 1 second

  Scenario: Waiting sends no signal to the group
    When bench-memcap-group-reap-race: the group is checked while its last member exits 0.5 seconds after the leader and signals are recorded
    Then bench-memcap-group-reap-race: no signal other than the zero probe was sent to the group

  Scenario: The cgroup test file is untouched
    When bench-memcap-group-reap-race: the memcap test file is read
    Then bench-memcap-group-reap-race: the memcap test file is byte-identical to its content on main and keeps both branches
