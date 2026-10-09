const std = @import("std");
const core = @import("core.zig");

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    var args: std.ArrayList([]const u8) = .empty;
    var iterator = init.minimal.args.iterate();
    _ = iterator.next();
    while (iterator.next()) |arg| try args.append(allocator, arg);

    switch (try core.execute(init.io, allocator, args.items)) {
        .output => |output| std.Io.File.stdout().writeStreamingAll(init.io, output) catch {},
        .failure => |failure| {
            const message = try std.fmt.allocPrint(allocator, "{s}\n", .{failure.message});
            std.Io.File.stderr().writeStreamingAll(init.io, message) catch {};
            std.process.exit(failure.code);
        },
    }
}
