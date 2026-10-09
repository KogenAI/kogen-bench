const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});
    const root_source = b.path("src/main.zig");

    const executable_module = b.createModule(.{
        .root_source_file = root_source,
        .target = target,
        .optimize = optimize,
    });
    const executable = b.addExecutable(.{
        .name = "kogen",
        .root_module = executable_module,
    });
    b.installArtifact(executable);

    const test_module = b.createModule(.{
        .root_source_file = root_source,
        .target = target,
        .optimize = optimize,
    });
    const tests = b.addTest(.{ .root_module = test_module });
    const run_tests = b.addRunArtifact(tests);
    b.step("test", "Run deterministic project checks").dependOn(&run_tests.step);
}
