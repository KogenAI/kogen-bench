const std = @import("std");
const core = @import("core.zig");

pub fn physicalLines(allocator: std.mem.Allocator, text: []const u8) ![][]const u8 {
    var lines: std.ArrayList([]const u8) = .empty;
    var parts = std.mem.splitScalar(u8, text, '\n');
    while (parts.next()) |part| {
        const line = if (std.mem.endsWith(u8, part, "\r")) part[0 .. part.len - 1] else part;
        try lines.append(allocator, line);
    }
    return lines.toOwnedSlice(allocator);
}

pub const LoadResult = union(enum) {
    bytes: []u8,
    error_message: []u8,
};

fn readError(allocator: std.mem.Allocator, prefix: []const u8) std.mem.Allocator.Error!LoadResult {
    return .{ .error_message = try std.fmt.allocPrint(allocator, "{s}: cannot read input", .{prefix}) };
}

pub fn load(
    allocator: std.mem.Allocator,
    io: std.Io,
    path: ?[]const u8,
    prefix: []const u8,
) std.mem.Allocator.Error!LoadResult {
    if (path) |value| {
        if (!std.mem.eql(u8, value, "-")) {
            const bytes = std.Io.Dir.cwd().readFileAlloc(io, value, allocator, .unlimited) catch |err| {
                if (err == error.OutOfMemory) return error.OutOfMemory;
                return readError(allocator, prefix);
            };
            return .{ .bytes = bytes };
        }
    }

    var buffer: [4096]u8 = undefined;
    var reader = std.Io.File.stdin().reader(io, &buffer);
    const bytes = reader.interface.allocRemaining(allocator, .unlimited) catch |err| {
        if (err == error.OutOfMemory) return error.OutOfMemory;
        return readError(allocator, prefix);
    };
    return .{ .bytes = bytes };
}

pub fn main(init: std.process.Init) void {
    const allocator = init.arena.allocator();
    var iter = init.minimal.args.iterate();
    _ = iter.next();

    var args: std.ArrayList([]const u8) = .empty;
    while (iter.next()) |arg| args.append(allocator, arg) catch return;

    const result = core.execute(allocator, init.io, args.items);
    std.Io.File.stdout().writeStreamingAll(init.io, result.stdout) catch {};
    std.Io.File.stderr().writeStreamingAll(init.io, result.stderr) catch {};
    if (result.exit_code != 0) std.process.exit(result.exit_code);
}

test "physical line endings" {
    const lines = try physicalLines(std.testing.allocator, "a\r\n\nb\r");
    defer std.testing.allocator.free(lines);
    try std.testing.expectEqual(@as(usize, 3), lines.len);
    try std.testing.expectEqualStrings("a", lines[0]);
    try std.testing.expectEqualStrings("", lines[1]);
    try std.testing.expectEqualStrings("b", lines[2]);
}
