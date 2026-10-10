#!/usr/bin/env python3
"""Monomorphic source-directed inference and Lean 4 emission; stdlib only."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def ident(s):
    return "v_" + re.sub(r"[^a-zA-Z0-9_]", "_", s)


def atom(s):
    return "a_" + re.sub(r"[^a-zA-Z0-9_]", "_", s)


def fail(n, message):
    loc = n.get("loc", {"file": "IR", "line": 1, "column": 1})
    raise ValueError(f'FV-LEAN {loc["file"]}:{loc["line"]}:{loc.get("column", 1)}: {message}')


class Type:
    def __init__(self, kind=None, fields=None, items=None, tag=None):
        self.parent = self
        self.kind = kind
        self.fields = fields or {}
        self.items = items or []
        self.closed = None
        self.optional = set()
        self.tag = tag

    def root(self):
        if self.parent is not self:
            self.parent = self.parent.root()
        return self.parent


def unify(a, b, n):
    a, b = a.root(), b.root()
    if a is b:
        return a
    def contains(container, target, seen):
        container = container.root()
        if container is target: return True
        if id(container) in seen: return False
        seen.add(id(container))
        return any(contains(x, target, seen) for x in list(container.fields.values()) + container.items)
    if (a.kind is None and contains(b, a, set())) or (b.kind is None and contains(a, b, set())):
        fail(n, "recursive record/tuple types are outside the subset")
    if a.kind and b.kind and a.kind != b.kind:
        fail(n, f"inconsistent types: {a.kind} versus {b.kind}")
    if a.kind is None:
        a, b = b, a
    b.parent = a
    if a.kind == "record":
        if a.tag and b.tag and a.tag != b.tag:
            fail(n, "incompatible struct/map identities")
        a.tag = a.tag or b.tag
        if a.closed is not None and b.closed is not None and a.closed != b.closed:
            fail(n, "inconsistent record construction shapes")
        for key, value in b.fields.items():
            if key in a.fields:
                unify(a.fields[key], value, n)
            else:
                a.fields[key] = value
        a.optional |= b.optional
        a.closed = a.closed if a.closed is not None else b.closed
        if a.closed is not None and set(a.fields) - a.closed - a.optional:
            fail(n, "field access/update absent from constructed record")
    if a.kind == "tuple" and b.kind == "tuple":
        if len(a.items) != len(b.items):
            fail(n, "tuple arity mismatch")
        for x, y in zip(a.items, b.items):
            unify(x, y, n)
    return a


class Emitter:
    def __init__(self, ir, laws):
        if ir.get("version") != 1:
            raise ValueError("unsupported IR version")
        self.ir, self.laws = ir, laws
        self.types = {}
        self.functions = {}
        self.atoms = {"missing", "nil"}
        self.record_names = {}
        for mod in ir["modules"]:
            for fn in mod["functions"]:
                key = (mod["name"], fn["name"], len(fn["params"]))
                if key not in self.functions:
                    self.functions[key] = {"params": [Type() for _ in fn["params"]], "result": Type(), "clauses": [], "deps": set()}
                self.functions[key]["clauses"].append(fn)
        for key, fn in self.functions.items():
            for clause in fn["clauses"]:
                env = {}
                for p, t in zip(clause["params"], fn["params"]):
                    self.pattern(p, t, env)
                unify(fn["result"], self.infer(clause["body"], env, key), clause)
        self.order = []
        visiting = set()
        visited = set()
        def visit(key):
            if key in visiting:
                fail(self.functions[key]["clauses"][0], "recursive helpers are outside the subset")
            if key in visited:
                return
            visiting.add(key)
            for dep in sorted(self.functions[key]["deps"]):
                visit(dep)
            visiting.remove(key)
            visited.add(key)
            self.order.append(key)
        for key in sorted(self.functions):
            visit(key)
        for t in self.types.values():
            self.register(t)
        for value in laws.get("domains", {}).values():
            if isinstance(value, list):
                self.atoms.update(x for x in value if isinstance(x, str))
        self.atoms.update(laws.get("events", []))
        if laws["task"] == "F01":
            fn = self.functions[(laws["module"], "can_read", 2)]
            optional = {(id(t.root()), field.split(".")[1]) for field in laws["missing_fields"] for t in [fn["params"][0 if field.startswith("actor.") else 1]]}
            def check(node):
                if isinstance(node, list):
                    for child in node: check(child)
                elif isinstance(node, dict):
                    if node.get("kind") in ("get", "update"):
                        base = self.types[id(node["base"])].root()
                        fields = [node["field"]] if node["kind"] == "get" else [f["name"] for f in node["fields"]]
                        if any((id(base), field) in optional for field in fields):
                            fail(node, "direct access/update to an optional input field may raise; use Map.get/has_key?")
                    for child in node.values(): check(child)
            check(ir)

    def register(self, t):
        t = t.root()
        if t.kind is None:
            t.kind = "atom"  # finite unused parameter; calls still constrain used values
        if t.kind == "record":
            name = self.typename(t)
            if name in self.record_names:
                prev = self.record_names[name]
                for field in t.fields:
                    unify(prev.fields[field], t.fields[field], {"loc": {"file": "IR", "line": 1}})
            else:
                self.record_names[name] = t
            for child in t.fields.values():
                self.register(child)
        if t.kind == "tuple":
            for child in t.items:
                self.register(child)

    def field(self, t, name, n, optional=False):
        r = Type("record", {name: Type()})
        if optional:
            r.optional.add(name)
        root = unify(t, r, n)
        return root.fields[name]

    def pattern(self, n, expected, env):
        k = n["kind"]
        self.types[id(n)] = expected
        if k == "var":
            if n["name"] in env:
                fail(n, "repeated variables in patterns are unsupported")
            env[n["name"]] = expected
        elif k == "wildcard":
            pass
        elif k in ("atom", "bool", "int"):
            unify(expected, Type(k), n)
            if k == "atom":
                self.atoms.add(n["value"])
        elif k == "record_pattern":
            for f in n["fields"]:
                self.pattern(f["value"], self.field(expected, f["name"], n, True), env)
        elif k == "tuple_pattern":
            t = Type("tuple", items=[Type() for _ in n["items"]])
            unify(expected, t, n)
            for p, typ in zip(n["items"], t.items):
                self.pattern(p, typ, env)
        else:
            fail(n, "unsupported pattern kind " + k)

    def infer(self, n, env, key):
        k = n["kind"]
        if k in ("bool", "int", "atom"):
            t = Type(k)
            if k == "atom": self.atoms.add(n["value"])
        elif k == "var":
            if n["name"] not in env: fail(n, "unbound variable " + n["name"])
            t = env[n["name"]]
        elif k == "binary":
            a, b = self.infer(n["left"], env, key), self.infer(n["right"], env, key)
            unify(a, b, n)
            if n["op"] in ("and", "or"):
                unify(a, Type("bool"), n); t = Type("bool")
            elif n["op"] in ("+", "-"):
                unify(a, Type("int"), n); t = Type("int")
            elif n["op"] in ("==", "!="):
                t = Type("bool")
            else: fail(n, "unsupported binary operator")
        elif k == "unary":
            if n["op"] != "not": fail(n, "unsupported unary operator")
            unify(self.infer(n["value"], env, key), Type("bool"), n); t = Type("bool")
        elif k == "if":
            unify(self.infer(n["condition"], env, key), Type("bool"), n)
            t = unify(self.infer(n["then"], env, key), self.infer(n["else"], env, key), n)
        elif k == "let":
            child = dict(env)
            self.pattern(n["pattern"], self.infer(n["value"], env, key), child)
            t = self.infer(n["body"], child, key)
        elif k == "case":
            subject = self.infer(n["value"], env, key); t = Type()
            for branch in n["branches"]:
                child = dict(env); self.pattern(branch["pattern"], subject, child)
                unify(t, self.infer(branch["body"], child, key), branch)
        elif k == "record":
            t = Type("record", {f["name"]: self.infer(f["value"], env, key) for f in n["fields"]}, tag=n.get("struct") or "map")
            t.closed = set(t.fields)
        elif k == "update":
            t = self.infer(n["base"], env, key)
            if n.get("struct"):
                unify(t, Type("record", tag=n["struct"]), n)
            for f in n["fields"]:
                unify(self.field(t, f["name"], n), self.infer(f["value"], env, key), f)
        elif k == "get":
            t = self.field(self.infer(n["base"], env, key), n["field"], n)
        elif k == "tuple":
            t = Type("tuple", items=[self.infer(x, env, key) for x in n["items"]])
        elif k == "call":
            if n["module"] == "Map":
                args = n["args"]
                if len(args) < 2 or args[1]["kind"] != "atom": fail(n, "Map helper needs literal atom field")
                rec = self.infer(args[0], env, key)
                field = self.field(rec, args[1]["value"], n, True)
                if n["name"] == "get":
                    default = args[2] if len(args) == 3 else {"kind": "atom", "value": "nil", "loc": n["loc"]}
                    unify(field, self.infer(default, env, key), n); t = field
                elif n["name"] == "has_key?": t = Type("bool")
                else: fail(n, "unsupported Map function")
            else:
                target = (n["module"] or key[0], n["name"], len(n["args"]))
                if target not in self.functions: fail(n, "unknown/effectful helper " + str(target))
                self.functions[key]["deps"].add(target)
                fn = self.functions[target]
                for x, expected in zip(n["args"], fn["params"]): unify(self.infer(x, env, key), expected, x)
                t = fn["result"]
        else: fail(n, "unsupported IR kind " + k)
        self.types[id(n)] = t
        return t

    def typename(self, t):
        t = t.root()
        if t.kind == "record": return ("S_" + ident(t.tag) + "_" if t.tag and t.tag != "map" else "R_") + "_".join(sorted(t.fields))
        if t.kind == "tuple": return "(" + " × ".join(self.typename(x) for x in t.items) + ")"
        return {"atom": "Atom", "bool": "Bool", "int": "Int"}[t.kind]

    def default(self, t):
        return {"atom": ".a_missing", "bool": "false", "int": "0"}.get(t.root().kind, "default")

    def pat(self, n):
        k = n["kind"]
        if k == "var": return ident(n["name"])
        if k == "wildcard": return "_"
        if k == "atom": return "." + atom(n["value"])
        if k == "bool": return str(n["value"]).lower()
        if k == "int": return str(n["value"])
        if k == "tuple_pattern": return "(" + ", ".join(self.pat(x) for x in n["items"]) + ")"
        if k == "record_pattern":
            fs = {f["name"]: f["value"] for f in n["fields"]}
            items = []
            for field in sorted(self.types[id(n)].root().fields):
                items.extend([self.pat(fs[field]) if field in fs else "_", "true" if field in fs else "_"])
            return "⟨" + ", ".join(items) + "⟩"
        fail(n, "unsupported emitted pattern")

    def expr(self, n, key):
        k = n["kind"]
        e = lambda x: self.expr(x, key)
        if k == "var": out = ident(n["name"])
        elif k == "atom": out = "Atom." + atom(n["value"])
        elif k == "bool": out = str(n["value"]).lower()
        elif k == "int": out = f"({n['value']} : Int)"
        elif k == "binary":
            op = {"and": "&&", "or": "||", "==": "==", "!=": "!=", "+": "+", "-": "-"}[n["op"]]
            out = f"({e(n['left'])} {op} {e(n['right'])})"
        elif k == "unary": out = "(!" + e(n["value"]) + ")"
        elif k == "if": out = f"(if {e(n['condition'])} then {e(n['then'])} else {e(n['else'])})"
        elif k == "let": out = f"(let {self.pat(n['pattern'])} := {e(n['value'])}; {e(n['body'])})"
        elif k == "case":
            out = "(match " + e(n["value"]) + " with\n" + "\n".join("| " + self.pat(b["pattern"]) + " => " + e(b["body"]) for b in n["branches"]) + ")"
        elif k == "tuple": out = "(" + ", ".join(e(x) for x in n["items"]) + ")"
        elif k == "record":
            fs = {f["name"]: f["value"] for f in n["fields"]}
            pairs = []
            for field, t in sorted(self.types[id(n)].root().fields.items()):
                pairs.extend([f"{ident(field)} := {e(fs[field]) if field in fs else self.default(t)}", f"{ident(field)}_present := {'true' if field in fs else 'false'}"])
            out = "({ " + ", ".join(pairs) + " } : " + self.typename(self.types[id(n)]) + ")"
        elif k == "update": out = "{ " + e(n["base"]) + " with " + ", ".join(ident(f["name"]) + " := " + e(f["value"]) for f in n["fields"]) + " }"
        elif k == "get": out = e(n["base"]) + "." + ident(n["field"])
        elif k == "call":
            if n["module"] == "Map":
                args = n["args"]; base, field = e(args[0]), ident(args[1]["value"])
                if n["name"] == "has_key?": out = base + "." + field + "_present"
                else:
                    default = e(args[2]) if len(args) == 3 else "Atom.a_nil"
                    out = f"(if {base}.{field}_present then {base}.{field} else {default})"
            else:
                target = (n["module"] or key[0], n["name"], len(n["args"]))
                out = "(" + self.fnname(target) + (" " if n["args"] else "") + " ".join(e(x) for x in n["args"]) + ")"
        else: fail(n, "cannot emit kind " + k)
        return f"(/- src: {n['loc']['file']}:{n['loc']['line']} -/ {out})"

    def fnname(self, key): return ident(key[0] + "_" + key[1] + "_" + str(key[2]))

    def implementation(self):
        lines = ["-- Generated from current Elixir source; never edit this file.", "namespace FV", "inductive Atom where"]
        lines += ["  | " + atom(a) for a in sorted(self.atoms)]
        lines += ["  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited", ""]
        for name, typ in sorted(self.record_names.items()):
            lines.append("structure " + name + " where")
            for field, t in sorted(typ.fields.items()):
                lines.extend([f"  {ident(field)} : {self.typename(t)} := {self.default(t)}", f"  {ident(field)}_present : Bool := false"])
            lines.extend(["  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited", ""])
        for key in self.order:
            fn = self.functions[key]
            args = " ".join(f"(p{i} : {self.typename(t)})" for i, t in enumerate(fn["params"]))
            cl = fn["clauses"][0]
            lines.append(f"-- src: {cl['loc']['file']}:{cl['loc']['line']}")
            lines.append(f"def {self.fnname(key)} {args} : {self.typename(fn['result'])} :=")
            if fn["params"]:
                lines.append("  match " + ", ".join(f"p{i}" for i in range(len(fn["params"]))) + " with")
                for c in fn["clauses"]:
                    lines.append("  | " + ", ".join(self.pat(p) for p in c["params"]) + " => " + self.expr(c["body"], key))
            else: lines.append("  " + self.expr(cl["body"], key))
            lines.append("")
        mod = self.laws["module"]
        if self.laws["task"] == "F01":
            fn = self.functions[(mod, "can_read", 2)]
            lines += ["abbrev Actor := " + self.typename(fn["params"][0]), "abbrev Resource := " + self.typename(fn["params"][1]), "abbrev canRead := " + self.fnname((mod, "can_read", 2))]
        else:
            lines += ["abbrev State := " + self.typename(self.functions[(mod, "init", 0)]["result"]), "abbrev init := " + self.fnname((mod, "init", 0)), "abbrev step := " + self.fnname((mod, "step", 2))]
        lines.append("end FV\n")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ir", type=Path); parser.add_argument("laws", type=Path); parser.add_argument("out", type=Path)
    parser.add_argument("--freeze-laws", action="store_true")
    args = parser.parse_args()
    ir, laws = json.loads(args.ir.read_text()), json.loads(args.laws.read_text())
    emitter = Emitter(ir, laws)
    implementation = emitter.implementation()
    args.out.mkdir(parents=True, exist_ok=True)
    ir_bytes = args.ir.read_bytes()
    (args.out / "ir.json").write_bytes(ir_bytes)
    (args.out / "Implementation.lean").write_text(implementation)
    generated = {(m[1], int(m[2])): i for i, line in enumerate(implementation.splitlines(), 1) for m in re.finditer(r"src: ([^\s]+):(\d+)", line)}
    source_map = []
    def map_nodes(node, path):
        if isinstance(node, list):
            for i, child in enumerate(node): map_nodes(child, path + "." + str(i))
        elif isinstance(node, dict):
            if "kind" in node and "loc" in node:
                loc = node["loc"]
                source_map.append({"node_id": path, "kind": node["kind"], **loc, "generated_line": generated.get((loc["file"], loc["line"]))})
            for key, child in node.items(): map_nodes(child, path + "." + key)
    map_nodes(ir, "ir")
    (args.out / "source-map.json").write_text(json.dumps(source_map, indent=2) + "\n")
    (args.out / "lean-toolchain").write_text("fv-4.34.1\n")
    (args.out / "lakefile.lean").write_text('import Lake\nopen Lake DSL\npackage fv where\n@[default_target]\nlean_lib Laws where\n')
    if args.freeze_laws:
        from laws import generate
        fixed = generate(laws)
        target = args.out / "Laws.lean"
        if target.exists() and target.read_text() != fixed: raise ValueError("refusing to overwrite fixed Laws.lean")
        target.write_text(fixed)
        (args.out / "laws.sha256").write_text(hashlib.sha256(fixed.encode()).hexdigest() + "\n")
    digest = hashlib.sha256(ir_bytes + implementation.encode()).hexdigest()
    print("FV-REGENERATED " + digest)


if __name__ == "__main__":
    try: main()
    except (ValueError, KeyError) as exc:
        import sys
        print(str(exc), file=sys.stderr); sys.exit(2)
