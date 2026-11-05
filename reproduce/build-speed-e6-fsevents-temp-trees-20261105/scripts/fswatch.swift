// Passive FSEvents file-event counter. Counts events per (prefix, kind) under the given roots; writes TSV on SIGTERM/SIGINT and every 60 s.
import Foundation
import CoreServices

let args = CommandLine.arguments
guard args.count >= 4 else { fputs("usage: fswatch out.tsv depth root...\n", stderr); exit(2) }
let outPath = args[1]
let depth = Int(args[2]) ?? 1   // path components under the root that name the "prefix"
let roots = Array(args[3...])
var counts: [String: [String: Int]] = [:]   // prefix -> kind -> n
var total = 0
let lock = NSLock()

func normalise(_ name: String) -> String {
    // strip trailing random suffix: -XXXXXX / .XXXXXX / digits
    var s = name
    if let r = s.range(of: "[-.]?[A-Za-z0-9]{6}$", options: .regularExpression), s.distance(from: s.startIndex, to: r.lowerBound) > 3 { s.removeSubrange(r) }
    while let l = s.last, l.isNumber || l == "-" { s.removeLast() }
    return s
}

func dump() {
    lock.lock(); defer { lock.unlock() }
    var out = "prefix\tcreated\tremoved\tmodified\trenamed\ttotal\n"
    for (p, k) in counts.sorted(by: { $0.value.values.reduce(0,+) > $1.value.values.reduce(0,+) }) {
        let c = k["created"] ?? 0, r = k["removed"] ?? 0, m = k["modified"] ?? 0, n = k["renamed"] ?? 0
        out += "\(p)\t\(c)\t\(r)\t\(m)\t\(n)\t\(c+r+m+n)\n"
    }
    out += "#TOTAL\t\t\t\t\t\(total)\n"
    try? out.write(toFile: outPath, atomically: true, encoding: .utf8)
}

let cb: FSEventStreamCallback = { _, info, n, paths, flags, _ in
    let arr = unsafeBitCast(paths, to: NSArray.self) as! [String]
    lock.lock(); defer { lock.unlock() }
    for i in 0..<n {
        let f = flags[i]
        if f & UInt32(kFSEventStreamEventFlagItemIsFile) == 0 && f & UInt32(kFSEventStreamEventFlagItemIsSymlink) == 0 { continue }
        let path = arr[i]
        var prefix = "?"
        for r in roots where path.hasPrefix(r) {
            let rest = path.dropFirst(r.count).split(separator: "/", omittingEmptySubsequences: true)
            let comps = rest.prefix(depth).map { normalise(String($0)) }
            prefix = (URL(fileURLWithPath: r).lastPathComponent) + "/" + comps.joined(separator: "/")
            break
        }
        var kinds: [String] = []
        if f & UInt32(kFSEventStreamEventFlagItemCreated) != 0 { kinds.append("created") }
        if f & UInt32(kFSEventStreamEventFlagItemRemoved) != 0 { kinds.append("removed") }
        if f & UInt32(kFSEventStreamEventFlagItemModified) != 0 { kinds.append("modified") }
        if f & UInt32(kFSEventStreamEventFlagItemRenamed) != 0 { kinds.append("renamed") }
        if kinds.isEmpty { continue }
        for k in kinds { counts[prefix, default: [:]][k, default: 0] += 1 }
        total += 1
    }
}

var ctx = FSEventStreamContext()
let stream = FSEventStreamCreate(nil, cb, &ctx, roots as CFArray, FSEventStreamEventId(kFSEventStreamEventIdSinceNow), 0.2,
    FSEventStreamCreateFlags(kFSEventStreamCreateFlagFileEvents | kFSEventStreamCreateFlagNoDefer | kFSEventStreamCreateFlagUseCFTypes))!
FSEventStreamSetDispatchQueue(stream, DispatchQueue.main)
FSEventStreamStart(stream)
signal(SIGTERM, SIG_IGN); signal(SIGINT, SIG_IGN)
let s1 = DispatchSource.makeSignalSource(signal: SIGTERM, queue: .main); s1.setEventHandler { dump(); exit(0) }; s1.resume()
let s2 = DispatchSource.makeSignalSource(signal: SIGINT, queue: .main); s2.setEventHandler { dump(); exit(0) }; s2.resume()
let t = DispatchSource.makeTimerSource(queue: .main); t.schedule(deadline: .now() + 60, repeating: 60); t.setEventHandler { dump() }; t.resume()
dump()
RunLoop.main.run()
