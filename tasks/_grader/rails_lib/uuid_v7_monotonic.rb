# frozen_string_literal: true

# Grader-side preload (RUBYOPT -r). Fizzy ids are base36 UUIDv7 from SecureRandom.uuid_v7, which has only millisecond ordering: two records created
# within the same millisecond get randomly ordered ids. Upstream tests that create rows back to back and then compare id order (e.g.
# test/models/storage/totaled_test.rb "materialize_storage updates cursor to latest entry") therefore fail now and then on a fast machine, and a
# flaky app-suite test fails the whole grade at the preverify step (seen once in 15 parity replays). Ask Ruby for sub-millisecond ordering bits
# (still a valid UUIDv7); nothing about id format is otherwise changed.
require "securerandom"
SecureRandom.singleton_class.prepend(Module.new { def uuid_v7(extra_timestamp_bits: 12) = super })
