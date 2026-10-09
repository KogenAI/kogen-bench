const std = @import("std");

pub const PhysicalLines = struct {
    text: []const u8,
    start: usize = 0,
    done: bool = false,

    pub fn next(self: *PhysicalLines) ?[]const u8 {
        if (self.done) return null;

        const end = std.mem.indexOfScalarPos(u8, self.text, self.start, '\n') orelse self.text.len;
        var line = self.text[self.start..end];
        if (std.mem.endsWith(u8, line, "\r")) line = line[0 .. line.len - 1];

        if (end == self.text.len) {
            self.done = true;
        } else {
            self.start = end + 1;
        }
        return line;
    }
};

pub fn physicalLines(text: []const u8) PhysicalLines {
    return .{ .text = text };
}

pub fn load(io: std.Io, allocator: std.mem.Allocator, path: ?[]const u8) ![]u8 {
    const limit: std.Io.Limit = .limited(1024 * 1024 + 1);

    if (path == null or std.mem.eql(u8, path.?, "-")) {
        var input_buffer: [4096]u8 = undefined;
        var reader = std.Io.File.stdin().reader(io, &input_buffer);
        return reader.interface.allocRemaining(allocator, limit);
    }

    return std.Io.Dir.cwd().readFileAlloc(io, path.?, allocator, limit);
}
