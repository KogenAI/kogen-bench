const std = @import("std");
const core = @import("core.zig");

pub const PhysicalLines = struct {
    text: []const u8,
    offset: usize = 0,
    done: bool = false,

    pub fn next(self: *PhysicalLines) ?[]const u8 {
        if (self.done) return null;
        const rest = self.text[self.offset..];
        if (std.mem.indexOfScalar(u8, rest, '\n')) |newline| {
            self.offset += newline + 1;
            return trimCarriageReturn(rest[0..newline]);
        }
        self.done = true;
        return trimCarriageReturn(rest);
    }
};

fn trimCarriageReturn(line: []const u8) []const u8 {
    if (line.len > 0 and line[line.len - 1] == '\r') return line[0 .. line.len - 1];
    return line;
}

pub fn load(allocator: std.mem.Allocator, path: ?[]const u8, prefix: []const u8) ![]u8 {
    _ = prefix;
    var file_path: ?[:0]u8 = null;
    var fd: c_int = 0;
    if (path) |name| {
        if (!std.mem.eql(u8, name, "-")) {
            file_path = try allocator.dupeZ(u8, name);
            fd = open(file_path.?.ptr, @as(c_int, 0));
            if (fd < 0) return error.CannotReadInput;
        }
    }
    defer {
        if (fd != 0) _ = close(fd);
    }

    var bytes: std.ArrayList(u8) = .empty;
    var chunk: [4096]u8 = undefined;
    while (true) {
        const count = read(fd, &chunk, chunk.len);
        if (count < 0) return error.CannotReadInput;
        if (count == 0) break;
        try bytes.appendSlice(allocator, chunk[0..@intCast(count)]);
    }
    return try bytes.toOwnedSlice(allocator);
}

extern "c" fn open(path: [*:0]const u8, flags: c_int, ...) c_int;
extern "c" fn read(fd: c_int, buffer: [*]u8, count: usize) isize;
extern "c" fn close(fd: c_int) c_int;

pub fn main(init: std.process.Init.Minimal) u8 {
    const allocator = std.heap.page_allocator;
    const args = init.args.vector;
    if (args.len == 0) return 2;
    return @intCast(core.execute(allocator, args[1..]));
}

test "physical line endings" {
    var lines = PhysicalLines{ .text = "a\r\n\nb\r" };
    const expected = [_][]const u8{ "a", "", "b" };
    for (expected) |line| {
        const actual = lines.next() orelse return error.TestExpectedEqual;
        try std.testing.expectEqualSlices(u8, line, actual);
    }
    try std.testing.expect(lines.next() == null);
}
