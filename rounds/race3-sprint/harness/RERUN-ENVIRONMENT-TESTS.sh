#!/bin/bash
# Run unsandboxed by the supervisor; the FD test also needs final/core/target/release/kogen.
set -e
cd "$(dirname "$0")/../conformance"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" python3 -m unittest -v \
  test_environment_passthrough.EnvironmentPassthroughTest.test_toolchain_path_and_homes_reach_each_runner \
  test_process_cleanup.ProcessCleanupTest.test_quint_case_descriptors_return_to_baseline_under_low_limit
