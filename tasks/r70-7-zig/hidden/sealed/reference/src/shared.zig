const std = @import("std");

pub const LoadResult = union(enum) {
    bytes: []u8,
    failure: []const u8,
};

pub fn physicalLines(allocator: std.mem.Allocator, text: []const u8) std.mem.Allocator.Error![][]const u8 {
    var lines: std.ArrayList([]const u8) = .empty;
    var iterator = std.mem.splitScalar(u8, text, '\n');
    while (iterator.next()) |line| {
        const normalized = if (std.mem.endsWith(u8, line, "\r")) line[0 .. line.len - 1] else line;
        try lines.append(allocator, normalized);
    }
    return lines.toOwnedSlice(allocator);
}

pub fn load(
    io: std.Io,
    allocator: std.mem.Allocator,
    path: ?[]const u8,
    prefix: []const u8,
) std.mem.Allocator.Error!LoadResult {
    if (path == null or std.mem.eql(u8, path.?, "-")) {
        var reader = std.Io.File.stdin().readerStreaming(io, &.{});
        const bytes = reader.interface.allocRemaining(allocator, .unlimited) catch {
            return cannotRead(allocator, prefix);
        };
        return .{ .bytes = bytes };
    }
    const bytes = std.Io.Dir.cwd().readFileAlloc(io, path.?, allocator, .unlimited) catch {
        return cannotRead(allocator, prefix);
    };
    return .{ .bytes = bytes };
}

fn cannotRead(allocator: std.mem.Allocator, prefix: []const u8) std.mem.Allocator.Error!LoadResult {
    return .{ .failure = try std.fmt.allocPrint(allocator, "{s}: cannot read input", .{prefix}) };
}

test "physical line endings" {
    const allocator = std.testing.allocator;
    const lines = try physicalLines(allocator, "a\r\n\nb\r");
    defer allocator.free(lines);
    try std.testing.expectEqual(@as(usize, 3), lines.len);
    try std.testing.expectEqualStrings("a", lines[0]);
    try std.testing.expectEqualStrings("", lines[1]);
    try std.testing.expectEqualStrings("b", lines[2]);
}
