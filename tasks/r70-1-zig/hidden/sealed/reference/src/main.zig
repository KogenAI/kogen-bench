const std = @import("std");
const core = @import("core.zig");

pub fn physicalLines(allocator: std.mem.Allocator, text: []const u8) ![][]const u8 {
    var count: usize = 1;
    for (text) |byte| if (byte == '\n') {
        count += 1;
    };
    const lines = try allocator.alloc([]const u8, count);
    var index: usize = 0;
    var start: usize = 0;
    for (text, 0..) |byte, offset| {
        if (byte != '\n') continue;
        var line = text[start..offset];
        if (std.mem.endsWith(u8, line, "\r")) line = line[0 .. line.len - 1];
        lines[index] = line;
        index += 1;
        start = offset + 1;
    }
    var line = text[start..];
    if (std.mem.endsWith(u8, line, "\r")) line = line[0 .. line.len - 1];
    lines[index] = line;
    return lines;
}

pub const LoadResult = union(enum) {
    bytes: []u8,
    error_message: []u8,
};

pub fn load(allocator: std.mem.Allocator, io: std.Io, path: ?[]const u8, prefix: []const u8) !LoadResult {
    if (path) |file_path| {
        if (!std.mem.eql(u8, file_path, "-")) {
            const data = std.Io.Dir.cwd().readFileAlloc(io, file_path, allocator, .unlimited) catch {
                return .{ .error_message = try std.fmt.allocPrint(allocator, "{s}: cannot read input", .{prefix}) };
            };
            return .{ .bytes = data };
        }
    }

    var data: std.ArrayList(u8) = .empty;
    var buffer: [4096]u8 = undefined;
    while (true) {
        const amount = std.posix.read(std.posix.STDIN_FILENO, &buffer) catch {
            return .{ .error_message = try std.fmt.allocPrint(allocator, "{s}: cannot read input", .{prefix}) };
        };
        if (amount == 0) break;
        try data.appendSlice(allocator, buffer[0..amount]);
    }
    return .{ .bytes = try data.toOwnedSlice(allocator) };
}

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    const args = try init.minimal.args.toSlice(allocator);
    const cli_args = try allocator.alloc([]const u8, args.len - 1);
    for (args[1..], 0..) |arg, index| cli_args[index] = arg;

    switch (core.execute(allocator, init.io, cli_args)) {
        .output => |output| try std.Io.File.stdout().writeStreamingAll(init.io, output),
        .failure => |failure| {
            var buffer: [512]u8 = undefined;
            var writer = std.Io.File.stderr().writer(init.io, &buffer);
            try writer.interface.print("{s}\n", .{failure.message});
            try writer.interface.flush();
            std.process.exit(failure.code);
        },
    }
}

test "physical line endings" {
    const lines = try physicalLines(std.testing.allocator, "a\r\n\nb\r");
    defer std.testing.allocator.free(lines);
    try std.testing.expectEqual(@as(usize, 3), lines.len);
    try std.testing.expectEqualStrings("a", lines[0]);
    try std.testing.expectEqualStrings("", lines[1]);
    try std.testing.expectEqualStrings("b", lines[2]);
}
