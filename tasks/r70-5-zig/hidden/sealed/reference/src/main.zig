const std = @import("std");
const shared = @import("shared.zig");
const core = @import("core.zig");

pub const physicalLines = shared.physicalLines;
pub const load = shared.load;

pub fn main(init: std.process.Init) void {
    const allocator = init.arena.allocator();
    var argv = std.process.Args.Iterator.init(init.minimal.args);
    _ = argv.next();
    var args: std.ArrayList([]const u8) = .empty;
    while (argv.next()) |arg| {
        args.append(allocator, arg) catch {
            writeStderr(init.io, "config: cannot read input\n");
            std.process.exit(1);
        };
    }

    const result = core.execute(init.io, allocator, args.items) catch {
        writeStderr(init.io, "config: cannot read input\n");
        std.process.exit(1);
    };
    switch (result) {
        .output => |output| {
            _ = std.Io.File.stdout().writeStreamingAll(init.io, output) catch {};
        },
        .failure => |failure| {
            writeStderr(init.io, failure.message);
            writeStderr(init.io, "\n");
            std.process.exit(failure.code);
        },
    }
}

fn writeStderr(io: std.Io, bytes: []const u8) void {
    _ = std.Io.File.stderr().writeStreamingAll(io, bytes) catch {};
}

test "physical line endings" {
    var lines = physicalLines("a\r\n\nb\r");
    try std.testing.expectEqualStrings("a", lines.next().?);
    try std.testing.expectEqualStrings("", lines.next().?);
    try std.testing.expectEqualStrings("b", lines.next().?);
    try std.testing.expect(lines.next() == null);
}
