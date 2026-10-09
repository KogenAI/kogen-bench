const std = @import("std");
const builtin = @import("builtin");
const c = @import("c");
const List = std.array_list.Managed;

const TokenLimit: u64 = 9_007_199_254_740_991;
const MaxHeaderBytes: usize = 65_536;
const MaxLineBytes: usize = 8_192;

const Endpoint = struct {
    host: []const u8,
    host_header: []const u8,
    port: u16,
    target: []const u8,
};

const Options = struct {
    url: []const u8,
    prompt: []const u8,
    timeout_ms: u64,
    usage_path: []const u8,
    endpoint: Endpoint,
};

const Result = struct {
    text: []const u8,
    input_tokens: u64,
    output_tokens: u64,
};

const Usage = struct { input: u64, output: u64 };

const Headers = struct {
    status: u16,
    content_length: ?usize = null,
    chunked: bool = false,
};

pub fn execute(allocator: std.mem.Allocator, args: []const []const u8) error{ InvalidArguments, RequestFailed }![]const u8 {
    const options = parseArgs(args) orelse return error.InvalidArguments;
    const request_body = encodePrompt(allocator, options.prompt) catch return error.RequestFailed;
    var result: ?Result = null;
    var attempt: usize = 0;
    while (attempt < 2) : (attempt += 1) {
        result = performAttempt(allocator, &options, request_body) catch |err| {
            if (err == error.Retryable and attempt == 0) continue;
            return error.RequestFailed;
        };
        break;
    }
    const complete = result orelse return error.RequestFailed;
    writeUsageAtomically(allocator, options.usage_path, complete.input_tokens, complete.output_tokens) catch return error.RequestFailed;
    var output = List(u8).init(allocator);
    output.appendSlice(complete.text) catch return error.RequestFailed;
    output.append('\n') catch return error.RequestFailed;
    return output.toOwnedSlice() catch return error.RequestFailed;
}

fn parseArgs(args: []const []const u8) ?Options {
    if (args.len != 9 or !std.mem.eql(u8, args[0], "model")) return null;
    var url: ?[]const u8 = null;
    var prompt: ?[]const u8 = null;
    var timeout: ?[]const u8 = null;
    var usage: ?[]const u8 = null;
    var index: usize = 1;
    while (index < args.len) : (index += 2) {
        if (index + 1 >= args.len) return null;
        const slot = args[index];
        const value = args[index + 1];
        if (std.mem.eql(u8, slot, "--url")) {
            if (url != null) return null;
            url = value;
        } else if (std.mem.eql(u8, slot, "--prompt")) {
            if (prompt != null or !validUtf8(value)) return null;
            prompt = value;
        } else if (std.mem.eql(u8, slot, "--idle-timeout-ms")) {
            if (timeout != null) return null;
            timeout = value;
        } else if (std.mem.eql(u8, slot, "--usage-file")) {
            if (usage != null) return null;
            usage = value;
        } else return null;
    }
    const url_value = url orelse return null;
    const prompt_value = prompt orelse return null;
    const usage_value = usage orelse return null;
    if (usage_value.len == 0) return null;
    const timeout_value = timeout orelse return null;
    if (timeout_value.len == 0) return null;
    for (timeout_value) |byte| if (!std.ascii.isDigit(byte)) return null;
    const timeout_ms = std.fmt.parseInt(u64, timeout_value, 10) catch return null;
    if (timeout_ms < 1 or timeout_ms > 60_000) return null;
    const endpoint = parseUrl(url_value) orelse return null;
    return .{
        .url = url_value,
        .prompt = prompt_value,
        .timeout_ms = timeout_ms,
        .usage_path = usage_value,
        .endpoint = endpoint,
    };
}

fn parseUrl(raw: []const u8) ?Endpoint {
    const scheme_end = std.mem.indexOf(u8, raw, "://") orelse return null;
    if (!std.ascii.eqlIgnoreCase(raw[0..scheme_end], "http")) return null;
    const authority_start = scheme_end + 3;
    var authority_end = raw.len;
    for (raw[authority_start..], authority_start..) |byte, index| {
        if (byte == '/' or byte == '?' or byte == '#') {
            authority_end = index;
            break;
        }
    }
    if (authority_end == authority_start) return null;
    const raw_authority = raw[authority_start..authority_end];
    const authority = if (std.mem.lastIndexOfScalar(u8, raw_authority, '@')) |at|
        raw_authority[at + 1 ..]
    else
        raw_authority;
    if (authority.len == 0) return null;
    for (authority) |byte| {
        if (byte <= 0x20 or byte == 0x7f or byte == '\\') return null;
    }
    var host: []const u8 = undefined;
    var host_header: []const u8 = authority;
    var port: u16 = 80;
    if (authority[0] == '[') {
        const close = std.mem.indexOfScalar(u8, authority, ']') orelse return null;
        if (close <= 1) return null;
        host = authority[1..close];
        const rest = authority[close + 1 ..];
        if (rest.len > 0) {
            if (rest[0] != ':') return null;
            port = parsePort(rest[1..]) orelse return null;
        }
    } else {
        var colons: usize = 0;
        for (authority) |byte| if (byte == ':') {
            colons += 1;
        };
        if (colons > 1) return null;
        if (std.mem.lastIndexOfScalar(u8, authority, ':')) |colon| {
            host = authority[0..colon];
            port = parsePort(authority[colon + 1 ..]) orelse return null;
        } else host = authority;
    }
    if (host.len == 0) return null;
    for (host) |byte| if (byte <= 0x20 or byte == 0x7f or byte == '/' or byte == '?' or byte == '#') return null;
    var target = raw[authority_end..];
    if (std.mem.indexOfScalar(u8, target, '#')) |fragment| target = target[0..fragment];
    if (target.len == 0) target = "/";
    if (target[0] == '?') {
        // The leading slash is added while writing the request.
    } else if (target[0] != '/') return null;
    for (target) |byte| if (byte <= 0x20 or byte == 0x7f) return null;
    if (std.mem.indexOfScalar(u8, raw, '%')) |percent| {
        var i = percent;
        while (i < raw.len) : (i += 1) {
            if (raw[i] == '%') {
                if (i + 2 >= raw.len or !isHexDigit(raw[i + 1]) or !isHexDigit(raw[i + 2])) return null;
                i += 2;
            }
        }
    }
    host_header = authority;
    return .{ .host = host, .host_header = host_header, .port = port, .target = target };
}

fn parsePort(raw: []const u8) ?u16 {
    if (raw.len == 0) return null;
    for (raw) |byte| if (!std.ascii.isDigit(byte)) return null;
    return std.fmt.parseInt(u16, raw, 10) catch null;
}

fn isHexDigit(byte: u8) bool {
    return std.ascii.isDigit(byte) or (byte >= 'a' and byte <= 'f') or (byte >= 'A' and byte <= 'F');
}

fn encodePrompt(allocator: std.mem.Allocator, prompt: []const u8) ![]u8 {
    var out = List(u8).init(allocator);
    try out.appendSlice("{\"prompt\":\"");
    const hex = "0123456789abcdef";
    for (prompt) |byte| {
        switch (byte) {
            '"' => try out.appendSlice("\\\""),
            '\\' => try out.appendSlice("\\\\"),
            '\n' => try out.appendSlice("\\n"),
            '\r' => try out.appendSlice("\\r"),
            '\t' => try out.appendSlice("\\t"),
            0...8, 11...12, 14...0x1f => {
                try out.appendSlice("\\u00");
                try out.append(hex[byte >> 4]);
                try out.append(hex[byte & 0x0f]);
            },
            else => try out.append(byte),
        }
    }
    try out.appendSlice("\"}");
    return out.toOwnedSlice();
}

fn connect(allocator: std.mem.Allocator, endpoint: Endpoint) !c_int {
    const host_z = try allocator.dupeSentinel(u8, endpoint.host, 0);
    defer allocator.free(host_z);
    var port_buffer: [6]u8 = undefined;
    const port_text = try std.fmt.bufPrint(port_buffer[0..5], "{d}", .{endpoint.port});
    port_buffer[port_text.len] = 0;
    const port_z = port_buffer[0..port_text.len :0];
    var hints = std.mem.zeroes(c.struct_addrinfo);
    hints.ai_family = c.AF_UNSPEC;
    hints.ai_socktype = c.SOCK_STREAM;
    hints.ai_protocol = c.IPPROTO_TCP;
    var first: ?*c.struct_addrinfo = null;
    if (c.getaddrinfo(host_z.ptr, port_z.ptr, &hints, &first) != 0) return error.Retryable;
    defer c.freeaddrinfo(first);
    var entry = first;
    while (entry) |item| : (entry = item.ai_next) {
        const fd = c.socket(item.ai_family, item.ai_socktype, item.ai_protocol);
        if (fd < 0) continue;
        if (builtin.os.tag == .macos) {
            var one: c_int = 1;
            _ = c.setsockopt(fd, c.SOL_SOCKET, c.SO_NOSIGPIPE, &one, @sizeOf(c_int));
        }
        if (c.connect(fd, item.ai_addr, item.ai_addrlen) == 0) return fd;
        _ = c.close(fd);
    }
    return error.Retryable;
}

const Reader = struct {
    fd: c_int,

    fn next(self: *Reader, timeout_ms: u64, deadline_ms: ?i64) !?u8 {
        var remaining: i64 = @intCast(timeout_ms);
        if (deadline_ms) |deadline| {
            remaining = deadline - nowMs();
            if (remaining <= 0) return error.Timeout;
        }
        var descriptor = c.struct_pollfd{ .fd = self.fd, .events = c.POLLIN, .revents = 0 };
        const poll_timeout: c_int = @intCast(@min(remaining, std.math.maxInt(c_int)));
        const ready = c.poll(&descriptor, 1, poll_timeout);
        if (ready == 0) return error.Timeout;
        if (ready < 0) return error.ReadFailure;
        var byte: u8 = 0;
        const count = c.recv(self.fd, &byte, 1, 0);
        if (count == 0) return null;
        if (count < 0) return error.ReadFailure;
        return byte;
    }
};

fn nowMs() i64 {
    var value: c.struct_timespec = undefined;
    if (c.clock_gettime(c.CLOCK_MONOTONIC, &value) != 0) return 0;
    return @as(i64, @intCast(value.tv_sec)) * 1000 + @divTrunc(@as(i64, @intCast(value.tv_nsec)), 1_000_000);
}

fn performAttempt(allocator: std.mem.Allocator, options: *const Options, body: []const u8) anyerror!Result {
    const header_deadline = nowMs() + @as(i64, @intCast(options.timeout_ms));
    const fd = try connect(allocator, options.endpoint);
    defer _ = c.close(fd);
    const request = try makeRequest(allocator, options.endpoint, body);
    try sendAll(fd, request);
    var reader = Reader{ .fd = fd };
    const header_bytes = readHeaders(allocator, &reader, options.timeout_ms, header_deadline) catch |err| {
        if (err == error.Timeout or err == error.ReadFailure or err == error.EndOfStream) return error.Retryable;
        return error.Fatal;
    };
    const headers = parseHeaders(header_bytes) catch return error.Fatal;
    if (headers.status >= 500 and headers.status <= 599) return error.Retryable;
    if (headers.status < 200 or headers.status > 299) return error.Fatal;
    var response = List(u8).init(allocator);
    if (headers.chunked) {
        readChunked(allocator, &reader, options.timeout_ms, &response) catch |err| {
            if (err == error.Timeout or err == error.ReadFailure or err == error.EndOfStream) return error.Retryable;
            return error.Fatal;
        };
    } else if (headers.content_length) |length| {
        var read_count: usize = 0;
        while (read_count < length) : (read_count += 1) {
            const byte = reader.next(options.timeout_ms, null) catch |err| {
                if (err == error.Timeout or err == error.ReadFailure) return error.Retryable;
                return error.Fatal;
            } orelse return error.Retryable;
            response.append(byte) catch return error.Fatal;
        }
    } else {
        while (true) {
            const byte = reader.next(options.timeout_ms, null) catch |err| {
                if (err == error.Timeout or err == error.ReadFailure) return error.Retryable;
                return error.Fatal;
            } orelse break;
            response.append(byte) catch return error.Fatal;
        }
    }
    return parseSse(allocator, response.items) catch error.Fatal;
}

fn makeRequest(allocator: std.mem.Allocator, endpoint: Endpoint, body: []const u8) ![]u8 {
    var request = List(u8).init(allocator);
    try request.appendSlice("POST ");
    if (endpoint.target[0] == '?') try request.append('/');
    try request.appendSlice(endpoint.target);
    try request.appendSlice(" HTTP/1.1\r\nHost: ");
    try request.appendSlice(endpoint.host_header);
    try request.appendSlice("\r\nContent-Type: application/json\r\nAccept: text/event-stream\r\nContent-Length: ");
    const length_text = try std.fmt.allocPrint(allocator, "{d}", .{body.len});
    defer allocator.free(length_text);
    try request.appendSlice(length_text);
    try request.appendSlice("\r\nConnection: close\r\n\r\n");
    try request.appendSlice(body);
    return request.toOwnedSlice();
}

fn sendAll(fd: c_int, bytes: []const u8) !void {
    var offset: usize = 0;
    while (offset < bytes.len) {
        const flags: c_int = if (builtin.os.tag == .linux) c.MSG_NOSIGNAL else 0;
        const count = c.send(fd, bytes[offset..].ptr, bytes.len - offset, flags);
        if (count <= 0) return error.Retryable;
        offset += @intCast(count);
    }
}

fn readHeaders(allocator: std.mem.Allocator, reader: *Reader, timeout_ms: u64, deadline: i64) ![]u8 {
    var bytes = List(u8).init(allocator);
    while (bytes.items.len < MaxHeaderBytes) {
        const byte = try reader.next(timeout_ms, deadline) orelse return error.EndOfStream;
        try bytes.append(byte);
        if (std.mem.endsWith(u8, bytes.items, "\r\n\r\n")) return bytes.toOwnedSlice();
    }
    return error.HeaderTooLarge;
}

fn parseHeaders(bytes: []const u8) !Headers {
    const first_end = std.mem.indexOf(u8, bytes, "\r\n") orelse return error.Malformed;
    const status_line = bytes[0..first_end];
    const space = std.mem.indexOfScalar(u8, status_line, ' ') orelse return error.Malformed;
    var rest = std.mem.trimStart(u8, status_line[space..], " ");
    if (rest.len < 3 or !std.ascii.isDigit(rest[0]) or !std.ascii.isDigit(rest[1]) or !std.ascii.isDigit(rest[2])) return error.Malformed;
    const status = std.fmt.parseInt(u16, rest[0..3], 10) catch return error.Malformed;
    rest = rest[3..];
    if (rest.len > 0 and rest[0] != ' ' and rest[0] != '\t') return error.Malformed;
    var result = Headers{ .status = status };
    var start = first_end + 2;
    while (start < bytes.len - 2) {
        const end_rel = std.mem.indexOf(u8, bytes[start..], "\r\n") orelse return error.Malformed;
        if (end_rel == 0) break;
        const line = bytes[start .. start + end_rel];
        const colon = std.mem.indexOfScalar(u8, line, ':') orelse return error.Malformed;
        if (colon == 0) return error.Malformed;
        const name = line[0..colon];
        const value = std.mem.trim(u8, line[colon + 1 ..], " \t");
        if (std.ascii.eqlIgnoreCase(name, "content-length")) {
            if (result.content_length != null) return error.Malformed;
            result.content_length = std.fmt.parseInt(usize, value, 10) catch return error.Malformed;
        } else if (std.ascii.eqlIgnoreCase(name, "transfer-encoding")) {
            var values = std.mem.splitScalar(u8, value, ',');
            while (values.next()) |encoding| {
                if (std.ascii.eqlIgnoreCase(std.mem.trim(u8, encoding, " \t"), "chunked")) result.chunked = true;
            }
        }
        start += end_rel + 2;
    }
    return result;
}

fn readCrlfLine(allocator: std.mem.Allocator, reader: *Reader, timeout_ms: u64) ![]u8 {
    var line = List(u8).init(allocator);
    while (line.items.len < MaxLineBytes) {
        const byte = try reader.next(timeout_ms, null) orelse return error.EndOfStream;
        if (byte == '\n') {
            if (line.items.len == 0 or line.items[line.items.len - 1] != '\r') return error.Malformed;
            _ = line.pop();
            return line.toOwnedSlice();
        }
        try line.append(byte);
    }
    return error.LineTooLong;
}

fn readChunked(allocator: std.mem.Allocator, reader: *Reader, timeout_ms: u64, out: *List(u8)) !void {
    while (true) {
        const size_line = try readCrlfLine(allocator, reader, timeout_ms);
        const semicolon = std.mem.indexOfScalar(u8, size_line, ';') orelse size_line.len;
        if (semicolon == 0) return error.Malformed;
        const size = std.fmt.parseInt(usize, size_line[0..semicolon], 16) catch return error.Malformed;
        if (size == 0) {
            while (true) {
                const trailer = try readCrlfLine(allocator, reader, timeout_ms);
                if (trailer.len == 0) return;
                if (std.mem.indexOfScalar(u8, trailer, ':') == null) return error.Malformed;
            }
        }
        var count: usize = 0;
        while (count < size) : (count += 1) {
            const byte = try reader.next(timeout_ms, null) orelse return error.EndOfStream;
            try out.append(byte);
        }
        const cr = try reader.next(timeout_ms, null) orelse return error.EndOfStream;
        const lf = try reader.next(timeout_ms, null) orelse return error.EndOfStream;
        if (cr != '\r' or lf != '\n') return error.Malformed;
    }
}

fn parseSse(allocator: std.mem.Allocator, input: []const u8) !Result {
    var text = List(u8).init(allocator);
    var event_data = List(u8).init(allocator);
    var has_data = false;
    var usage: ?Usage = null;
    var start: usize = 0;
    for (input, 0..) |byte, index| {
        if (byte != '\n') continue;
        var line = input[start..index];
        if (std.mem.endsWith(u8, line, "\r")) line = line[0 .. line.len - 1];
        if (!validUtf8(line)) return error.InvalidUtf8;
        if (line.len == 0) {
            if (has_data) {
                if (std.mem.eql(u8, event_data.items, "[DONE]")) {
                    const final_usage = usage orelse return error.MissingUsage;
                    return .{
                        .text = text.toOwnedSlice() catch return error.OutOfMemory,
                        .input_tokens = final_usage.input,
                        .output_tokens = final_usage.output,
                    };
                }
                try consumeEvent(allocator, event_data.items, &text, &usage);
            }
            event_data.clearRetainingCapacity();
            has_data = false;
        } else if (line[0] != ':') {
            if (std.mem.startsWith(u8, line, "data:")) {
                var value = line[5..];
                if (value.len > 0 and value[0] == ' ') value = value[1..];
                if (has_data) try event_data.append('\n');
                try event_data.appendSlice(value);
                has_data = true;
            }
        }
        start = index + 1;
    }
    const tail = input[start..];
    if (!validUtf8(tail)) return error.InvalidUtf8;
    return error.MissingDone;
}

fn consumeEvent(allocator: std.mem.Allocator, data: []const u8, text: *List(u8), usage: *?Usage) !void {
    var parsed = try std.json.parseFromSlice(std.json.Value, allocator, data, .{
        .parse_numbers = false,
        .duplicate_field_behavior = .use_last,
    });
    defer parsed.deinit();
    const object = switch (parsed.value) {
        .object => |value| value,
        else => return error.NotObject,
    };
    const kind = object.get("type") orelse return;
    if (kind != .string) return;
    if (std.mem.eql(u8, kind.string, "text")) {
        const value = object.get("text") orelse return error.InvalidText;
        if (value != .string) return error.InvalidText;
        try text.appendSlice(value.string);
    } else if (std.mem.eql(u8, kind.string, "usage")) {
        const input_value = object.get("input_tokens") orelse return error.InvalidUsage;
        const output_value = object.get("output_tokens") orelse return error.InvalidUsage;
        const input_count = tokenCount(input_value) orelse return error.InvalidUsage;
        const output_count = tokenCount(output_value) orelse return error.InvalidUsage;
        usage.* = .{ .input = input_count, .output = output_count };
    }
}

fn tokenCount(value: std.json.Value) ?u64 {
    if (value != .number_string) return null;
    return exactInteger(value.number_string);
}

fn exactInteger(raw: []const u8) ?u64 {
    if (raw.len == 0) return null;
    var at: usize = 0;
    var negative = false;
    if (raw[at] == '-') {
        negative = true;
        at += 1;
        if (at == raw.len) return null;
    }
    var exponent_at = raw.len;
    for (raw[at..], at..) |byte, index| {
        if (byte == 'e' or byte == 'E') {
            exponent_at = index;
            break;
        }
    }
    const mantissa = raw[at..exponent_at];
    const dot = std.mem.indexOfScalar(u8, mantissa, '.') orelse mantissa.len;
    const fraction_len = if (dot < mantissa.len) mantissa.len - dot - 1 else 0;
    var digits = List(u8).init(std.heap.page_allocator);
    defer digits.deinit();
    for (mantissa) |byte| if (byte != '.') {
        if (!std.ascii.isDigit(byte)) return null;
        digits.append(byte) catch return null;
    };
    var first: usize = 0;
    while (first < digits.items.len and digits.items[first] == '0') : (first += 1) {}
    if (first == digits.items.len) return 0;
    var exponent: i64 = 0;
    if (exponent_at < raw.len) {
        const exp_text = raw[exponent_at + 1 ..];
        exponent = parseSaturatedExponent(exp_text) orelse return null;
    }
    const fraction_i64: i64 = @intCast(fraction_len);
    const scale: i64 = if (exponent < std.math.minInt(i64) + fraction_i64)
        std.math.minInt(i64)
    else
        exponent - fraction_i64;
    var end = digits.items.len;
    if (scale < 0) {
        const need_remove: u64 = @intCast(if (scale == std.math.minInt(i64)) std.math.maxInt(i64) else -scale);
        var trailing: usize = 0;
        while (trailing < end - first and digits.items[end - trailing - 1] == '0') : (trailing += 1) {}
        if (need_remove > trailing) return null;
        end -= @intCast(need_remove);
    } else if (scale > 0) {
        if (scale > 16 or end - first + @as(usize, @intCast(scale)) > 16) return null;
        end += @intCast(scale);
    }
    const length = end - first;
    if (length > 16) return null;
    var result: u64 = 0;
    var index = first;
    while (index < end) : (index += 1) {
        const digit: u8 = if (index < digits.items.len) digits.items[index] - '0' else 0;
        result = result * 10 + digit;
    }
    if (result > TokenLimit or (negative and result != 0)) return null;
    return result;
}

fn parseSaturatedExponent(raw: []const u8) ?i64 {
    if (raw.len == 0) return null;
    var index: usize = 0;
    var sign: i64 = 1;
    if (raw[index] == '+' or raw[index] == '-') {
        if (raw[index] == '-') sign = -1;
        index += 1;
        if (index == raw.len) return null;
    }
    var value: i64 = 0;
    while (index < raw.len) : (index += 1) {
        const byte = raw[index];
        if (!std.ascii.isDigit(byte)) return null;
        const digit: i64 = byte - '0';
        value = if (value > @divTrunc(std.math.maxInt(i64) - digit, 10)) std.math.maxInt(i64) else value * 10 + digit;
    }
    return if (sign < 0) -value else value;
}

fn validUtf8(input: []const u8) bool {
    var index: usize = 0;
    while (index < input.len) {
        const first = input[index];
        if (first <= 0x7f) {
            index += 1;
            continue;
        }
        if (first >= 0xc2 and first <= 0xdf) {
            if (index + 1 >= input.len or input[index + 1] < 0x80 or input[index + 1] > 0xbf) return false;
            index += 2;
            continue;
        }
        if (first >= 0xe0 and first <= 0xef) {
            if (index + 2 >= input.len) return false;
            const second = input[index + 1];
            const third = input[index + 2];
            if (third < 0x80 or third > 0xbf) return false;
            if (first == 0xe0) {
                if (second < 0xa0 or second > 0xbf) return false;
            } else if (first == 0xed) {
                if (second < 0x80 or second > 0x9f) return false;
            } else if (second < 0x80 or second > 0xbf) return false;
            index += 3;
            continue;
        }
        if (first >= 0xf0 and first <= 0xf4) {
            if (index + 3 >= input.len) return false;
            const second = input[index + 1];
            if (input[index + 2] < 0x80 or input[index + 2] > 0xbf or input[index + 3] < 0x80 or input[index + 3] > 0xbf) return false;
            if (first == 0xf0) {
                if (second < 0x90 or second > 0xbf) return false;
            } else if (first == 0xf4) {
                if (second < 0x80 or second > 0x8f) return false;
            } else if (second < 0x80 or second > 0xbf) return false;
            index += 4;
            continue;
        }
        return false;
    }
    return true;
}

fn writeUsageAtomically(allocator: std.mem.Allocator, path: []const u8, input_tokens: u64, output_tokens: u64) !void {
    const slash = std.mem.lastIndexOfScalar(u8, path, '/');
    const parent = if (slash) |index| (if (index == 0) "/" else path[0..index]) else ".";
    try makeParents(allocator, parent);
    const pid = c.getpid();
    const stamp = nowMs();
    const temp = try std.fmt.allocPrint(allocator, "{s}/.kogen-usage-{d}-{d}", .{ parent, pid, stamp });
    defer allocator.free(temp);
    const temp_z = try allocator.dupeSentinel(u8, temp, 0);
    defer allocator.free(temp_z);
    const path_z = try allocator.dupeSentinel(u8, path, 0);
    defer allocator.free(path_z);
    const fd = c.open(temp_z.ptr, c.O_WRONLY | c.O_CREAT | c.O_EXCL, @as(c_int, 0o600));
    if (fd < 0) return error.AtomicWriteFailed;
    var keep = false;
    defer {
        _ = c.close(fd);
        if (!keep) _ = c.unlink(temp_z.ptr);
    }
    var record = std.array_list.Managed(u8).init(allocator);
    const record_text = try std.fmt.allocPrint(allocator, "{{\"input_tokens\":{d},\"output_tokens\":{d}}}\n", .{ input_tokens, output_tokens });
    defer allocator.free(record_text);
    try record.appendSlice(record_text);
    var offset: usize = 0;
    while (offset < record.items.len) {
        const written = c.write(fd, record.items[offset..].ptr, record.items.len - offset);
        if (written <= 0) return error.AtomicWriteFailed;
        offset += @intCast(written);
    }
    if (c.fsync(fd) != 0) return error.AtomicWriteFailed;
    if (c.rename(temp_z.ptr, path_z.ptr) != 0) return error.AtomicWriteFailed;
    keep = true;
}

fn makeParents(allocator: std.mem.Allocator, path: []const u8) !void {
    if (path.len == 0 or std.mem.eql(u8, path, ".")) return;
    const path_z = try allocator.dupeSentinel(u8, path, 0);
    defer allocator.free(path_z);
    var index: usize = if (path[0] == '/') 1 else 0;
    while (index < path.len) : (index += 1) {
        if (path[index] == '/') {
            const saved = path_z[index];
            path_z[index] = 0;
            if (index > 0) _ = c.mkdir(path_z.ptr, 0o755);
            path_z[index] = saved;
        }
    }
    _ = c.mkdir(path_z.ptr, 0o755);
}

// Decimal arithmetic avoids rounding fractional/exponent JSON tokens through f64.
test "exact integer usage values" {
    try std.testing.expectEqual(@as(?u64, 3), exactInteger("3.0"));
    try std.testing.expectEqual(@as(?u64, 3), exactInteger("3e0"));
    try std.testing.expectEqual(@as(?u64, null), exactInteger("3.00000000000000000001"));
    try std.testing.expectEqual(@as(?u64, TokenLimit), exactInteger("9007199254740991.0"));
    try std.testing.expectEqual(@as(?u64, null), exactInteger("9007199254740992"));
}
