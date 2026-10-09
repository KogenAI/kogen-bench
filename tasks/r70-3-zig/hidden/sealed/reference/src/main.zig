const std = @import("std");
const core = @import("core.zig");
const c = @import("c");

fn writeAll(fd: c_int, bytes: []const u8) void {
    var offset: usize = 0;
    while (offset < bytes.len) {
        const written = c.write(fd, bytes[offset..].ptr, bytes.len - offset);
        if (written <= 0) return;
        offset += @intCast(written);
    }
}

fn fail(code: u8, message: []const u8) noreturn {
    writeAll(2, message);
    std.process.exit(code);
}

pub fn physicalLines(allocator: std.mem.Allocator, input: []const u8) ![][]const u8 {
    var lines = std.array_list.Managed([]const u8).init(allocator);
    var start: usize = 0;
    for (input, 0..) |byte, index| {
        if (byte == '\n') {
            var line = input[start..index];
            if (std.mem.endsWith(u8, line, "\r")) line = line[0 .. line.len - 1];
            try lines.append(line);
            start = index + 1;
        }
    }
    var last = input[start..];
    if (std.mem.endsWith(u8, last, "\r")) last = last[0 .. last.len - 1];
    try lines.append(last);
    return lines.toOwnedSlice();
}

pub fn load(allocator: std.mem.Allocator, path: ?[]const u8, prefix: []const u8) ![]u8 {
    _ = prefix;
    var fd: c_int = c.STDIN_FILENO;
    if (path) |path_value| {
        if (!std.mem.eql(u8, path_value, "-")) {
            const path_z = try allocator.dupeSentinel(u8, path_value, 0);
            defer allocator.free(path_z);
            fd = c.open(path_z.ptr, c.O_RDONLY);
            if (fd < 0) return error.CannotReadInput;
            defer _ = c.close(fd);
        }
    }
    var bytes = std.array_list.Managed(u8).init(allocator);
    var chunk: [4096]u8 = undefined;
    while (true) {
        const count = c.read(fd, &chunk, chunk.len);
        if (count < 0) return error.CannotReadInput;
        if (count == 0) break;
        try bytes.appendSlice(chunk[0..@intCast(count)]);
    }
    return bytes.toOwnedSlice();
}

pub fn main(init: std.process.Init.Minimal) void {
    const allocator = std.heap.page_allocator;
    var iterator = std.process.Args.Iterator.init(init.args);
    _ = iterator.next();
    var args = std.array_list.Managed([]const u8).init(allocator);
    while (iterator.next()) |arg| {
        args.append(arg[0..arg.len]) catch fail(5, "error: request failed\n");
    }
    const output = core.execute(allocator, args.items) catch |err| switch (err) {
        error.InvalidArguments => fail(2, "error: invalid arguments\n"),
        else => fail(5, "error: request failed\n"),
    };
    writeAll(1, output);
}

test "physical line endings" {
    const lines = try physicalLines(std.testing.allocator, "a\r\n\nb\r");
    defer std.testing.allocator.free(lines);
    try std.testing.expectEqual(@as(usize, 3), lines.len);
    try std.testing.expectEqualStrings("a", lines[0]);
    try std.testing.expectEqualStrings("", lines[1]);
    try std.testing.expectEqualStrings("b", lines[2]);
}
