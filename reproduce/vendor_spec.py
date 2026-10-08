#!/usr/bin/env python3
"""Build the reviewed, sanitized v1.2 clause-reference snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/KogenAI/kogen-spec"
ORIGINAL_REVISION = "1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0"
SANITIZED_REVISION = "30d9b25e4eefa7117121de44298fed504b429f4e"
OMITTED_UPSTREAM_PATHS = [
    {"path": "spec/APPENDIX-REFERENCE.md", "reason": "removed from the upstream public-release tree; editorial reference material"},
    {"path": "spec/COVERAGE.md", "reason": "removed from the upstream public-release tree; coverage note not required to resolve published clauses"},
    {"path": "spec/DRIFT-v1.2.md", "reason": "removed from the upstream public-release tree; historical drift note"},
    {"path": "spec/REVIEW-1.md", "reason": "removed from the upstream public-release tree; review record"},
    {"path": "spec/REVIEW-1-RESPONSE.md", "reason": "removed from the upstream public-release tree; review response"},
]

SOURCES = {
    "01-cli.md": "spec/01-cli.md",
    "02-formats.md": "spec/02-formats.md",
    "03-build.md": "spec/03-build.md",
    "04-provider.md": "spec/04-provider.md",
    "05-sandbox-custody.md": "spec/05-sandbox-custody.md",
    "06-non-goals.md": "spec/06-non-goals.md",
    "CLI-RULE.txt": "CLI-RULE.txt",
    "CONFORMANCE-v1.2-CASES.md": "spec/CONFORMANCE-v1.2-CASES.md",
    "CONFORMANCE.md": "spec/CONFORMANCE.md",
    "README.md": "spec/README.md",
    "data/constants.json": "spec/data/constants.json",
    "data/help/kogen-intent-approve.txt": "spec/data/help/kogen-intent-approve.txt",
    "data/help/kogen-intent-remove.txt": "spec/data/help/kogen-intent-remove.txt",
    "data/help/kogen-intent-shape.txt": "spec/data/help/kogen-intent-shape.txt",
    "data/help/kogen-intent.txt": "spec/data/help/kogen-intent.txt",
    "data/help/kogen-provider-list.txt": "spec/data/help/kogen-provider-list.txt",
    "data/help/kogen-provider-login.txt": "spec/data/help/kogen-provider-login.txt",
    "data/help/kogen-provider-logout.txt": "spec/data/help/kogen-provider-logout.txt",
    "data/help/kogen-provider-use.txt": "spec/data/help/kogen-provider-use.txt",
    "data/help/kogen-provider.txt": "spec/data/help/kogen-provider.txt",
    "data/help/kogen-queue-start.txt": "spec/data/help/kogen-queue-start.txt",
    "data/help/kogen-queue-stop.txt": "spec/data/help/kogen-queue-stop.txt",
    "data/help/kogen-queue.txt": "spec/data/help/kogen-queue.txt",
    "data/help/kogen-status.txt": "spec/data/help/kogen-status.txt",
    "data/help/kogen-version.txt": "spec/data/help/kogen-version.txt",
    "data/help/kogen.txt": "spec/data/help/kogen.txt",
    "data/lint.json": "spec/data/lint.json",
    "data/moved.json": "spec/data/moved.json",
    "data/yaml-errors.json": "spec/data/yaml-errors.json",
    "quint/CLASSIFICATION.md": "quint/CLASSIFICATION.md",
}

REPLACEMENTS = {
    "01-cli.md": {
        3: "The command tree is fixed by [CLI-RULE.txt](CLI-RULE.txt). Help text is the byte-exact pages in [data/help/](data/help/). The provider names are `chatgpt` and `grok` on the existing `login`, `logout`, and `use` commands (§4.10). No command, subcommand, or flag is added.",
    },
    "02-formats.md": {
        67: "  - v1.1 decision dated 5 Oct 2026: the shaper has a dedicated Sol default rather than inheriting the builder model. In v1, shaper = builder mapped the default gpt-6.1-sol builder to gpt-6-luna/max for shaping.",
    },
    "03-build.md": {
        6: "**Build invariants (decisions dated 5 Oct 2026).**",
    },
    "04-provider.md": {
        187: " \"reply\":{\"calls\":[{\"name\":\"shell\",\"arguments\":{\"cmd\":\"printf 'Hello, developer!\\\\n' > lib/greet.txt\"}}]}}",
        335: "2. Device request: form body `client_id=<client-id>` and `scope=openid profile email offline_access grok-cli:access api:access`. If discovery omits the device endpoint, use `<issuer>/oauth2/device/code`. The token endpoint comes from discovery. Both must be `https` with no userinfo.",
    },
    "CLI-RULE.txt": {
        1: "The public Kogen CLI command tree is fixed: `kogen status [<slug>] [--watch] [--json]`, `kogen intent shape <slug> <file|->`, `kogen intent approve <slug> [<hash>]`, `kogen intent remove <slug> [--force]`, `kogen queue start [--detach] | stop`, `kogen provider list | login chatgpt | logout chatgpt | use chatgpt --as <label> [--project]`, `kogen version`, `kogen help`, with options --project/--origin/--base/--by. Commands, subcommands, and flags are fixed to preserve a stable CLI.",
        3: "Decision dated 6 Oct 2026: provider names may include `grok` (SuperGrok subscription) alongside `chatgpt` on the existing provider commands. This adds no commands or flags.",
    },
    "CONFORMANCE.md": {
        338: "Example test, `.kogen/acceptance/greet.t.sh`: `t_A1() { grep -qx 'Hello, developer!' lib/greet.txt; }`. Fake builder steps make changes with `shell` calls.",
    },
    "quint/CLASSIFICATION.md": {
        3: "**Source of authority:** [CLI-RULE.txt](../CLI-RULE.txt), dated product decisions recorded in the v1.2 specification, and `spec/`. G = GUARANTEED, L = LIKELY, E = EXPERIMENTAL. A row classifies the **whole numbered section**; a mixed row names its guaranteed kernel. Later evidence may promote L/E only through a spec and test change. Dn refers to decision n in the ledger; F refers to its frozen-round decisions. The fixed CLI and the hash/queue/landing safety contract take priority over historical Elixir behavior. The frozen conformance suite is v1.1 and cannot by itself validate all v1.2 detail.",
    },
}

README = """# Kogen specification v1.2 — public snapshot

This directory is a locally sanitized, navigable **v1.2 clause-reference snapshot**. Its content baseline is [upstream revision 1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0](https://github.com/KogenAI/kogen-spec/tree/1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0). The upstream public-release revision used for publication sanitization is [30d9b25e4eefa7117121de44298fed504b429f4e](https://github.com/KogenAI/kogen-spec/commit/30d9b25e4eefa7117121de44298fed504b429f4e).

Personal filesystem locations, owner quotations, and internal attribution were removed or rewritten. Some editorial changes mean these published bytes are not claimed to be byte-identical to either upstream revision. [SOURCE.json](SOURCE.json) preserves the original source paths and hashes separately from the SHA-256 hashes of the bytes published here; [SHA256SUMS](SHA256SUMS) checks the published files.

## Included inventory

- Core v1.2 clauses: [CLI](01-cli.md), [formats](02-formats.md), [Build](03-build.md), [providers](04-provider.md), [sandbox custody](05-sandbox-custody.md), and [non-goals](06-non-goals.md).
- Conformance references: [v1.2 cases](CONFORMANCE-v1.2-CASES.md) and [conformance contract](CONFORMANCE.md).
- Public CLI command tree: [CLI-RULE.txt](CLI-RULE.txt).
- Clause classification: [Quint classification](quint/CLASSIFICATION.md).
- Normative data: [constants](data/constants.json), [lint rules](data/lint.json), [moved-command metadata](data/moved.json), and [YAML errors](data/yaml-errors.json).
- Exact CLI help pages: [kogen](data/help/kogen.txt), [version](data/help/kogen-version.txt), [status](data/help/kogen-status.txt), [intent](data/help/kogen-intent.txt), [intent shape](data/help/kogen-intent-shape.txt), [intent approve](data/help/kogen-intent-approve.txt), [intent remove](data/help/kogen-intent-remove.txt), [provider](data/help/kogen-provider.txt), [provider list](data/help/kogen-provider-list.txt), [provider login](data/help/kogen-provider-login.txt), [provider logout](data/help/kogen-provider-logout.txt), [provider use](data/help/kogen-provider-use.txt), [queue](data/help/kogen-queue.txt), [queue start](data/help/kogen-queue-start.txt), and [queue stop](data/help/kogen-queue-stop.txt).
- Provenance and published-byte integrity: [SOURCE.json](SOURCE.json) and [SHA256SUMS](SHA256SUMS).

## Omitted upstream material

This is a clause-reference excerpt, not a copy of the full upstream repository or its decision ledger. The upstream public-release revision removes the appendix reference, coverage and v1.2 drift notes, and review records from its public tree. Those historical/editorial files are not needed to resolve the clauses linked by EVIDENCE-MAP.md. The underlying decision ledger remains absent, so this snapshot does not establish comprehensive decision-to-clause coverage.

## Sources and precedence

1. The fixed public command tree is defined in [CLI-RULE.txt](CLI-RULE.txt); dated decisions in the v1.2 source clauses govern product rules.
2. Measurements inform success rate, speed, and cost; they remain distinct from normative product choices.
3. The specification records target contracts and deferred designs. A normative clause or conformance result does not establish an efficacy benefit.
4. The reference implementation supplies exact strings and constants where the sources above are silent.
"""


def run(*args: str, cwd: Path | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        list(args), cwd=cwd, check=True,
        stdout=subprocess.PIPE if capture else None,
        text=True,
    )
    return result.stdout.strip() if capture else ""


def replace_lines(relative: str, data: bytes) -> bytes:
    replacements = REPLACEMENTS.get(relative, {})
    if not replacements:
        return data
    lines = data.decode("utf-8").splitlines(keepends=True)
    for number, replacement in replacements.items():
        index = number - 1
        if index >= len(lines):
            raise ValueError(f"Pinned source line missing in {relative}:{number}")
        ending = "\r\n" if lines[index].endswith("\r\n") else "\n" if lines[index].endswith("\n") else ""
        lines[index] = replacement + ending
    return "".join(lines).encode("utf-8")


def verify_revision(repository: Path, revision: str) -> None:
    actual = run("git", "-C", str(repository), "rev-parse", revision, capture=True)
    if actual != revision:
        raise ValueError(f"Fetched Kogen spec revision differs from requested pin: {revision}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", help="local path or URL of the kogen-spec Git repository")
    parser.add_argument("--destination", type=Path, default=ROOT / "spec", help="output directory (must not exist)")
    args = parser.parse_args()
    repository_arg = args.repository
    if "://" not in repository_arg:
        repository_arg = str(Path(repository_arg).expanduser())
    destination = args.destination.resolve()
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing snapshot directory: {destination}")

    with tempfile.TemporaryDirectory(prefix="kogen-spec-v1.2-") as temporary:
        temp_root = Path(temporary)
        clone = temp_root / "repository"
        original = temp_root / "original"
        sanitized = temp_root / "sanitized"
        run("git", "clone", "--quiet", "--no-checkout", repository_arg, str(clone))
        for revision in (ORIGINAL_REVISION, SANITIZED_REVISION):
            run("git", "-C", str(clone), "fetch", "--quiet", "--depth=1", "origin", revision)
        run("git", "-C", str(clone), "worktree", "add", "--quiet", "--detach", str(original), ORIGINAL_REVISION)
        run("git", "-C", str(clone), "worktree", "add", "--quiet", "--detach", str(sanitized), SANITIZED_REVISION)
        verify_revision(original, ORIGINAL_REVISION)
        verify_revision(sanitized, SANITIZED_REVISION)

        scan_script = sanitized / "tools" / "public_scan.py"
        if not scan_script.is_file():
            raise SystemExit("Pinned public-release revision does not contain tools/public_scan.py")
        subject = run("git", "-C", str(sanitized), "show", "-s", "--format=%s", SANITIZED_REVISION, capture=True)
        if not re.search(r"sanitiz|public release", subject, re.IGNORECASE):
            raise SystemExit("Pinned sanitized revision subject does not identify a sanitization/public release")
        run(sys.executable, str(scan_script), cwd=sanitized)

        for omitted in OMITTED_UPSTREAM_PATHS:
            check = subprocess.run(
                ["git", "-C", str(sanitized), "cat-file", "-e", f"{SANITIZED_REVISION}:{omitted['path']}"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            if check.returncode == 0:
                raise SystemExit(f"Expected editorial material is still present in public-release revision: {omitted['path']}")

        stage = temp_root / "snapshot"
        stage.mkdir()
        originals: list[dict[str, str]] = []
        published: list[dict[str, str]] = []
        for relative, source_path in sorted(SOURCES.items()):
            source = original / source_path
            if not source.is_file() or source.is_symlink():
                raise SystemExit(f"Pinned v1.2 source is missing or not a regular file: {source_path}")
            source_bytes = source.read_bytes()
            originals.append({
                "path": relative,
                "source_path": source_path,
                "source_revision": ORIGINAL_REVISION,
                "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
            })
            content = source_bytes
            if relative == "README.md":
                content = README.encode("utf-8")
            else:
                content = replace_lines(relative, content)
            output = stage / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
            published.append({"path": relative, "sha256": hashlib.sha256(content).hexdigest()})

        source_record = {
            "repository": REPOSITORY,
            "content_version": "v1.2",
            "original_cited_revision": ORIGINAL_REVISION,
            "sanitized_published_revision": SANITIZED_REVISION,
            "sanitized_published_revision_subject": subject,
            "snapshot_kind": "locally sanitized v1.2 clause-reference excerpt",
            "original_source_hashes": originals,
            "published_content_hashes": published,
            "omitted_upstream_paths": OMITTED_UPSTREAM_PATHS,
        }
        (stage / "SOURCE.json").write_text(json.dumps(source_record, indent=2) + "\n", encoding="utf-8")
        sums = [
            f"{hashlib.sha256((stage / row['path']).read_bytes()).hexdigest()}  {row['path']}"
            for row in published
        ]
        sums.append(f"{hashlib.sha256((stage / 'SOURCE.json').read_bytes()).hexdigest()}  SOURCE.json")
        (stage / "SHA256SUMS").write_text("\n".join(sorted(sums, key=lambda row: row.split("  ", 1)[1])) + "\n", encoding="utf-8")

        run(sys.executable, str(ROOT / "reproduce" / "validate_spec_snapshot.py"), "--snapshot", str(stage))
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(stage), destination)
    print(f"Vendored the locally sanitized v1.2 clause-reference snapshot from {ORIGINAL_REVISION} using public-release revision {SANITIZED_REVISION}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
