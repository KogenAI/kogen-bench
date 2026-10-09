const std = @import("std");
const core = @import("core.zig");

pub const LoadResult = union(enum) {
    bytes: []u8,
    failure: []const u8,
};

pub fn physicalLine(line: []const u8) []const u8 {
    return if (std.mem.endsWith(u8, line, "\r")) line[0 .. line.len - 1] else line;
}

pub fn physicalLines(allocator: std.mem.Allocator, text: []const u8) ![][]const u8 {
    var lines: std.ArrayList([]const u8) = .empty;
    var start: usize = 0;
    for (text, 0..) |byte, index| {
        if (byte != '\n') continue;
        try lines.append(allocator, physicalLine(text[start..index]));
        start = index + 1;
    }
    try lines.append(allocator, physicalLine(text[start..]));
    return try lines.toOwnedSlice(allocator);
}

pub fn load(
    allocator: std.mem.Allocator,
    io: std.Io,
    path: ?[]const u8,
    prefix: []const u8,
) !LoadResult {
    if (path) |file_path| {
        if (!std.mem.eql(u8, file_path, "-")) {
            const bytes = std.Io.Dir.cwd().readFileAlloc(io, file_path, allocator, .unlimited) catch {
                return .{ .failure = try std.fmt.allocPrint(allocator, "{s}: cannot read input", .{prefix}) };
            };
            return .{ .bytes = bytes };
        }
    }

    var bytes: std.ArrayList(u8) = .empty;
    var buffer: [4096]u8 = undefined;
    while (true) {
        const amount = std.Io.File.stdin().readStreaming(io, &.{&buffer}) catch {
            return .{ .failure = try std.fmt.allocPrint(allocator, "{s}: cannot read input", .{prefix}) };
        };
        if (amount == 0) break;
        try bytes.appendSlice(allocator, buffer[0..amount]);
    }
    return .{ .bytes = try bytes.toOwnedSlice(allocator) };
}

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    const args = try init.minimal.args.toSlice(allocator);
    const response = try core.execute(allocator, init.io, args[1..]);

    var stdout_buffer: [4096]u8 = undefined;
    var stdout = std.Io.File.stdout().writer(init.io, &stdout_buffer);
    try stdout.interface.writeAll(response.stdout);
    try stdout.interface.flush();

    if (response.stderr) |message| {
        var stderr_buffer: [1024]u8 = undefined;
        var stderr = std.Io.File.stderr().writer(init.io, &stderr_buffer);
        try stderr.interface.writeAll(message);
        try stderr.interface.writeAll("\n");
        try stderr.interface.flush();
    }
    if (response.exit_code != 0) std.process.exit(response.exit_code);
}

test {
    _ = core;
}

test "physical line endings" {
    const allocator = std.testing.allocator;
    const lines = try physicalLines(allocator, "a\r\n\nb\r");
    defer allocator.free(lines);
    try std.testing.expectEqual(@as(usize, 3), lines.len);
    try std.testing.expectEqualStrings("a", lines[0]);
    try std.testing.expectEqualStrings("", lines[1]);
    try std.testing.expectEqualStrings("b", lines[2]);
    try std.testing.expectEqualStrings("row\r", physicalLine("row\r\r"));
}
