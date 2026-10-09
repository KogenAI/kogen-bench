const std = @import("std");

extern "c" fn flock(fd: c_int, operation: c_int) c_int;
extern "c" fn fsync(fd: c_int) c_int;
extern "c" fn getpid() c_int;

const lock_ex: c_int = 2;
const lock_un: c_int = 8;

const Job = struct {
    id: []const u8,
    argv: [][]const u8,
    attempts: u64,
    done: bool,
    exit_code: i32,
    stdout: []const u8,
    stderr: []const u8,
};

const State = struct { jobs: []Job };

const ResultLine = struct {
    id: []const u8,
    attempt: u64,
    exit_code: i32,
    stdout: []const u8,
    stderr: []const u8,
    status: []const u8,
};

pub const Failure = struct {
    code: u8,
    message: []const u8,
};

pub const Outcome = union(enum) {
    output: []const u8,
    failure: Failure,
};

const Command = enum { add, run, status };
const Parsed = struct {
    command: Command,
    store: []const u8,
    id: ?[]const u8 = null,
    argv_json: ?[]const u8 = null,
};

const StoreLock = struct {
    file: std.Io.File,

    fn release(self: StoreLock, io: std.Io) void {
        _ = flock(@intCast(self.file.handle), lock_un);
        self.file.close(io);
    }
};

fn failure(code: u8, message: []const u8) Outcome {
    return .{ .failure = .{ .code = code, .message = message } };
}

fn invalid() Outcome {
    return failure(2, "error: invalid arguments");
}

fn storeFailure() Outcome {
    return failure(4, "error: store failure");
}

fn duplicateFailure() Outcome {
    return failure(3, "error: duplicate job id");
}

fn equal(left: []const u8, right: []const u8) bool {
    return std.mem.eql(u8, left, right);
}

fn parseArgs(args: []const []const u8) ?Parsed {
    if (args.len < 2 or !equal(args[0], "queue")) return null;

    const command: Command = if (equal(args[1], "add")) .add else if (equal(args[1], "run")) .run else if (equal(args[1], "status")) .status else return null;

    var store: ?[]const u8 = null;
    var id: ?[]const u8 = null;
    var argv_json: ?[]const u8 = null;
    var index: usize = 2;
    while (index < args.len) {
        const key = args[index];
        if (index + 1 >= args.len) return null;
        const value = args[index + 1];

        if (equal(key, "--store")) {
            if (store != null) return null;
            store = value;
        } else if (command == .add and equal(key, "--id")) {
            if (id != null) return null;
            id = value;
        } else if (command == .add and equal(key, "--argv")) {
            if (argv_json != null) return null;
            argv_json = value;
        } else {
            return null;
        }
        index += 2;
    }

    const store_path = store orelse return null;
    if (store_path.len == 0) return null;
    if (command == .add) {
        const job_id = id orelse return null;
        if (!validId(job_id)) return null;
        const encoded_argv = argv_json orelse return null;
        if (encoded_argv.len == 0) return null;
    } else if (id != null or argv_json != null) {
        return null;
    }

    return .{ .command = command, .store = store_path, .id = id, .argv_json = argv_json };
}

fn validId(id: []const u8) bool {
    if (id.len == 0 or id.len > 64 or !asciiAlphanumeric(id[0])) return false;
    for (id) |byte| {
        if (!asciiAlphanumeric(byte) and byte != '.' and byte != '_' and byte != '-') return false;
    }
    return true;
}

fn asciiAlphanumeric(byte: u8) bool {
    return (byte >= 'A' and byte <= 'Z') or (byte >= 'a' and byte <= 'z') or (byte >= '0' and byte <= '9');
}

fn parseArgv(allocator: std.mem.Allocator, source: []const u8) (std.mem.Allocator.Error || error{InvalidArgv})![][]const u8 {
    const parsed = std.json.parseFromSliceLeaky(std.json.Value, allocator, source, .{}) catch return error.InvalidArgv;
    if (parsed != .array or parsed.array.items.len == 0) return error.InvalidArgv;

    const argv = try allocator.alloc([]const u8, parsed.array.items.len);
    for (parsed.array.items, 0..) |value, index| {
        if (value != .string or value.string.len == 0 or std.mem.indexOfScalar(u8, value.string, 0) != null) return error.InvalidArgv;
        argv[index] = try allocator.dupe(u8, value.string);
    }
    return argv;
}

fn openStore(io: std.Io, path: []const u8) !std.Io.Dir {
    try std.Io.Dir.cwd().createDirPath(io, path);
    if (std.fs.path.isAbsolute(path)) return std.Io.Dir.openDirAbsolute(io, path, .{});
    return std.Io.Dir.cwd().openDir(io, path, .{});
}

fn acquireLock(io: std.Io, dir: std.Io.Dir) !StoreLock {
    const file = try dir.createFile(io, ".lock", .{ .read = true, .truncate = false });
    if (flock(@intCast(file.handle), lock_ex) != 0) {
        file.close(io);
        return error.LockFailure;
    }
    return .{ .file = file };
}

fn emptyState(allocator: std.mem.Allocator) !State {
    return .{ .jobs = try allocator.alloc(Job, 0) };
}

fn readState(allocator: std.mem.Allocator, io: std.Io, dir: std.Io.Dir) !State {
    const contents = dir.readFileAlloc(io, "state.json", allocator, .unlimited) catch |err| switch (err) {
        error.FileNotFound => return emptyState(allocator),
        else => return err,
    };
    return std.json.parseFromSliceLeaky(State, allocator, contents, .{}) catch error.CorruptState;
}

fn writeState(allocator: std.mem.Allocator, io: std.Io, dir: std.Io.Dir, state: State) !void {
    const encoded = try std.json.Stringify.valueAlloc(allocator, state, .{});
    const temporary = try std.fmt.allocPrint(allocator, ".state-{d}.tmp", .{getpid()});
    dir.deleteFile(io, temporary) catch {};
    var committed = false;
    defer {
        if (!committed) dir.deleteFile(io, temporary) catch {};
    }

    {
        var file = try dir.createFile(io, temporary, .{ .exclusive = true });
        defer file.close(io);
        try file.writeStreamingAll(io, encoded);
        try file.sync(io);
    }
    try dir.rename(temporary, dir, "state.json", io);
    committed = true;
    var sync_dir = try dir.openDir(io, ".", .{ .iterate = true });
    defer sync_dir.close(io);
    if (fsync(@intCast(sync_dir.handle)) != 0) return error.DirectorySyncFailure;
}

fn append(list: *std.ArrayList(u8), allocator: std.mem.Allocator, bytes: []const u8) !void {
    try list.appendSlice(allocator, bytes);
}

fn appendFormat(list: *std.ArrayList(u8), allocator: std.mem.Allocator, comptime format: []const u8, arguments: anytype) !void {
    try append(list, allocator, try std.fmt.allocPrint(allocator, format, arguments));
}

fn addJob(allocator: std.mem.Allocator, io: std.Io, dir: std.Io.Dir, state: *State, parsed: Parsed) Outcome {
    const job_id = parsed.id.?;
    for (state.jobs) |job| {
        if (equal(job.id, job_id)) return duplicateFailure();
    }

    const argv = parseArgv(allocator, parsed.argv_json.?) catch |err| {
        if (err == error.InvalidArgv) return invalid();
        return storeFailure();
    };
    const jobs = allocator.alloc(Job, state.jobs.len + 1) catch return storeFailure();
    @memcpy(jobs[0..state.jobs.len], state.jobs);
    jobs[state.jobs.len] = .{
        .id = allocator.dupe(u8, job_id) catch return storeFailure(),
        .argv = argv,
        .attempts = 0,
        .done = false,
        .exit_code = 0,
        .stdout = "",
        .stderr = "",
    };
    state.jobs = jobs;
    writeState(allocator, io, dir, state.*) catch return storeFailure();
    return .{ .output = std.fmt.allocPrint(allocator, "queued {s}\n", .{job_id}) catch return storeFailure() };
}

fn showStatus(allocator: std.mem.Allocator, state: State) Outcome {
    var output: std.ArrayList(u8) = .empty;
    for (state.jobs) |job| {
        if (!job.done) {
            appendFormat(&output, allocator, "{s} pending\n", .{job.id}) catch return storeFailure();
        } else if (job.exit_code == 0) {
            appendFormat(&output, allocator, "{s} succeeded\n", .{job.id}) catch return storeFailure();
        } else {
            appendFormat(&output, allocator, "{s} failed {d}\n", .{ job.id, job.exit_code }) catch return storeFailure();
        }
    }
    return .{ .output = output.toOwnedSlice(allocator) catch return storeFailure() };
}

const ChildOutput = struct { code: i32, stdout: []const u8, stderr: []const u8 };

fn runChild(allocator: std.mem.Allocator, io: std.Io, argv: []const []const u8) !ChildOutput {
    const result = std.process.run(allocator, io, .{ .argv = argv }) catch {
        return .{ .code = 127, .stdout = "", .stderr = "exec failed\n" };
    };
    const code: i32 = switch (result.term) {
        .exited => |status| @intCast(status),
        .signal => |signal| 128 + @as(i32, @intCast(@backingInt(signal))),
        .stopped, .unknown => 128,
    };
    return .{
        .code = code,
        .stdout = try decodeUtf8Lossy(allocator, result.stdout),
        .stderr = try decodeUtf8Lossy(allocator, result.stderr),
    };
}

fn isContinuation(byte: u8) bool {
    return byte >= 0x80 and byte <= 0xbf;
}

fn sequenceLength(first: u8) usize {
    if (first >= 0xc2 and first <= 0xdf) return 2;
    if (first >= 0xe0 and first <= 0xef) return 3;
    if (first >= 0xf0 and first <= 0xf4) return 4;
    return 0;
}

fn validSecond(first: u8, second: u8) bool {
    if (!isContinuation(second)) return false;
    if (first == 0xe0) return second >= 0xa0;
    if (first == 0xed) return second <= 0x9f;
    if (first == 0xf0) return second >= 0x90;
    if (first == 0xf4) return second <= 0x8f;
    return true;
}

fn decodeUtf8Lossy(allocator: std.mem.Allocator, input: []const u8) ![]const u8 {
    const capacity = std.math.mul(usize, input.len, 3) catch return error.OutOfMemory;
    const output = try allocator.alloc(u8, capacity);
    var output_len: usize = 0;
    var index: usize = 0;

    while (index < input.len) {
        const first = input[index];
        if (first < 0x80) {
            output[output_len] = first;
            output_len += 1;
            index += 1;
            continue;
        }

        const length = sequenceLength(first);
        if (length == 0) {
            @memcpy(output[output_len .. output_len + 3], "\xef\xbf\xbd");
            output_len += 3;
            index += 1;
            continue;
        }
        if (index + 1 >= input.len or !validSecond(first, input[index + 1])) {
            @memcpy(output[output_len .. output_len + 3], "\xef\xbf\xbd");
            output_len += 3;
            index += 1;
            continue;
        }

        var valid_prefix: usize = 2;
        while (valid_prefix < length and index + valid_prefix < input.len and isContinuation(input[index + valid_prefix])) : (valid_prefix += 1) {}
        if (valid_prefix < length) {
            @memcpy(output[output_len .. output_len + 3], "\xef\xbf\xbd");
            output_len += 3;
            index += valid_prefix;
            continue;
        }

        @memcpy(output[output_len .. output_len + length], input[index .. index + length]);
        output_len += length;
        index += length;
    }

    return output[0..output_len];
}

fn runPending(allocator: std.mem.Allocator, io: std.Io, dir: std.Io.Dir, state: *State) Outcome {
    const row_indices = allocator.alloc(usize, state.jobs.len) catch return storeFailure();
    var row_count: usize = 0;

    for (state.jobs, 0..) |*job, index| {
        if (job.done) continue;
        job.attempts += 1;
        writeState(allocator, io, dir, state.*) catch return storeFailure();

        const child = runChild(allocator, io, job.argv) catch return storeFailure();
        job.done = true;
        job.exit_code = child.code;
        job.stdout = child.stdout;
        job.stderr = child.stderr;
        row_indices[row_count] = index;
        row_count += 1;
        writeState(allocator, io, dir, state.*) catch return storeFailure();
    }

    var output: std.ArrayList(u8) = .empty;
    for (row_indices[0..row_count]) |index| {
        const job = state.jobs[index];
        const line = ResultLine{
            .id = job.id,
            .attempt = job.attempts,
            .exit_code = job.exit_code,
            .stdout = job.stdout,
            .stderr = job.stderr,
            .status = if (job.exit_code == 0) "succeeded" else "failed",
        };
        const encoded = std.json.Stringify.valueAlloc(allocator, line, .{}) catch return storeFailure();
        append(&output, allocator, encoded) catch return storeFailure();
        append(&output, allocator, "\n") catch return storeFailure();
    }
    return .{ .output = output.toOwnedSlice(allocator) catch return storeFailure() };
}

pub fn execute(allocator: std.mem.Allocator, io: std.Io, args: []const []const u8) Outcome {
    const parsed = parseArgs(args) orelse return invalid();
    const dir = openStore(io, parsed.store) catch return storeFailure();
    defer dir.close(io);

    const store_lock = acquireLock(io, dir) catch return storeFailure();
    defer store_lock.release(io);

    var state = readState(allocator, io, dir) catch return storeFailure();
    return switch (parsed.command) {
        .add => addJob(allocator, io, dir, &state, parsed),
        .run => runPending(allocator, io, dir, &state),
        .status => showStatus(allocator, state),
    };
}
