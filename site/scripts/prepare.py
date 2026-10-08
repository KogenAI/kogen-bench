#!/usr/bin/env python3
"""Build the site's normalized, source-only data from this repository."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import csv
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


SITE = Path(__file__).resolve().parents[1]
ROOT = SITE.parent
GENERATED = SITE / ".generated"
sys.path.insert(0, str(ROOT / "reproduce"))
from missing_reasons import load_legend  # noqa: E402
from partitioned_jsonl import MAX_PARTITION_BYTES, read_partitions  # noqa: E402

GITHUB = "https://github.com/KogenAI/kogen-bench"
EXPECTED_HYPOTHESES = {f"H{i:02d}" for i in range(1, 154)}
PRIVATE_PATH = re.compile(
    r"(?<![A-Za-z0-9])(?:/(?:Users|home|tmp|private|Volumes|var/folders)/[^\s\"'<>]+|"
    r"~/(?:Library|Documents|Desktop|Areas)/[^\s\"'<>]+|"
    r"[A-Za-z]:\\(?:Users|home|Documents)\\[^\s\"'<>]+)"
)


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def read_text(rel: str) -> str:
    text = (ROOT / rel).read_text(encoding="utf-8")
    # Public historical locators are not useful links on the website. Keep the
    # evidence bytes and hashes unchanged; abbreviate only these known locators.
    if rel == "rounds/stack-oneshot-conformance/README.md":
        for locator in (
            "/tmp/claude-501/linux-batch/conformance3/results-eu/go/results.jsonl",
            "/tmp/claude-501/linux-batch/conformance3/results-eu/ts/results.jsonl",
            "/tmp/claude-501/cx/logs/KRS-INT6.last.md",
        ):
            text = text.replace(locator, "[unpublished local artifact] " + locator.rsplit("/", 1)[-1])
    return text


def split_table_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def clean_md(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = value.replace("**", "").replace("__", "").replace("*", "")
    return value.strip()


def source_url(rel: str, revision: str) -> str:
    return f"{GITHUB}/blob/{revision}/{rel}"


def source_link(rel: str, revision: str, label: str | None = None) -> dict:
    return {"path": rel, "label": label or PurePosixPath(rel).name, "url": source_url(rel, revision)}


def parse_hypotheses() -> list[dict]:
    text = read_text("hypotheses/README.md")
    rows: list[dict] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) < 5 or not re.fullmatch(r"H\d{2,3}", cells[0]):
            continue
        owner_match = re.search(r"\(([^)]+\.md)\)", cells[4])
        if not owner_match:
            raise ValueError(f"Hypothesis row {cells[0]} has no family source link")
        family_path = str(PurePosixPath("hypotheses") / PurePosixPath(owner_match.group(1)).name)
        family_match = re.match(r"f(\d{2})", PurePosixPath(family_path).name)
        if not family_match:
            raise ValueError(f"Could not identify family for {cells[0]}")
        rows.append(
            {
                "id": cells[0],
                "slug": cells[0].lower(),
                "family_id": f"F{family_match.group(1)}",
                "family_slug": f"f{family_match.group(1)}",
                "proposition": clean_md(cells[2]),
                "status": clean_md(cells[3]),
                "source_path": "hypotheses/README.md",
                "family_source": family_path,
            }
        )
    ids = [item["id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Hypothesis register contains duplicate IDs")
    if set(ids) != EXPECTED_HYPOTHESES:
        missing = sorted(EXPECTED_HYPOTHESES - set(ids))
        extra = sorted(set(ids) - EXPECTED_HYPOTHESES)
        raise ValueError(f"Hypothesis inventory mismatch; missing={missing}; extra={extra}")
    return rows


def parse_findings() -> tuple[str, list[dict]]:
    text = read_text("FINDINGS.md")
    matches = list(re.finditer(r"(?m)^##\s+(F\d{2})\s+(.+?)\s*$", text))
    sections: list[dict] = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append(
            {
                "id": match.group(1),
                "slug": match.group(1).lower(),
                "title": match.group(2).strip(),
                "markdown": text[match.end() : end].strip(),
            }
        )
    return text[: matches[0].start()].strip() if matches else text, sections


def parse_evidence_map() -> tuple[str, list[dict], str]:
    text = read_text("EVIDENCE-MAP.md")
    start = text.find("## Clause map")
    if start < 0:
        return text, [], ""
    tail = text[start:]
    coverage_match = re.search(r"(?m)^##\s+Decision-ID coverage\s*$", tail)
    clause_tail = tail[: coverage_match.start()] if coverage_match else tail
    decision_coverage = tail[coverage_match.end() :].strip() if coverage_match else ""
    headings = list(re.finditer(r"(?m)^###\s+\[(.+?)\]\(#([^)]+)\)\s*$", clause_tail))
    sections: list[dict] = []
    for i, match in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(clause_tail)
        section_md = clause_tail[match.end() : end].strip()
        sections.append(
            {
                "id": match.group(2).lower(),
                "title": clean_md(match.group(1)),
                "markdown": section_md,
                "hypothesis_ids": sorted(set(re.findall(r"\bH\d{2,3}\b", section_md)), key=lambda x: int(x[1:])),
                "round_ids": sorted(set(re.findall(r"rounds/([a-z0-9][a-z0-9-]+)/README\.md", section_md))),
                "claim_ids": sorted(set(re.findall(r"\bCL-[A-Za-z0-9_-]+\b", section_md))),
            }
        )
    ids = [item["id"] for item in sections]
    if len(ids) != len(set(ids)):
        raise ValueError("Evidence map contains duplicate clause anchors")
    intro = re.sub(r"(?m)^#\s+Evidence map\s*\n+", "", text[:start].strip(), count=1)
    return intro, sections, decision_coverage


def load_jsonl(rel: str) -> list[dict]:
    rows = []
    for number, line in enumerate(read_text(rel).splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {rel}:{number}: {exc}") from exc
    return rows


def load_indexed_jsonl(directory: str) -> list[dict]:
    return read_partitions(ROOT / directory)[1]


def load_indexed_run_records() -> tuple[dict, list[dict], dict[str, dict]]:
    index = json.loads(read_text("results/run-records/index.json"))
    if index.get("index_schema_version") != "1.0" or not isinstance(index.get("files"), list):
        raise ValueError("Unsupported or malformed run-record index")
    rows: list[dict] = []
    by_round: dict[str, dict] = {}
    max_bytes = MAX_PARTITION_BYTES
    missing_codes = load_legend(ROOT / "results" / "missing-reasons.json")
    unassigned_code = next(
        code for code, entry in missing_codes.items()
        if entry["reason"] == "No unambiguous owning round tag"
        and entry["reconstructable_from"] == "none"
    )
    for entry in index["files"]:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("round_id"), str)
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", entry["round_id"])
            or entry.get("file") != f"{entry['round_id']}.jsonl"
            or not isinstance(entry.get("bytes"), int)
            or isinstance(entry.get("bytes"), bool)
            or entry.get("bytes", -1) < 0
            or entry["bytes"] > max_bytes
            or entry["round_id"] in by_round
        ):
            raise ValueError("Malformed run-record partition entry")
        rel = f"results/run-records/{entry['file']}"
        raw = (ROOT / rel).read_bytes()
        if len(raw) != entry.get("bytes") or hashlib.sha256(raw).hexdigest() != entry.get("sha256"):
            raise ValueError(f"Run-record index fingerprint mismatch: {rel}")
        partition = load_jsonl(rel)
        if len(partition) != entry.get("record_count"):
            raise ValueError(f"Run-record index count mismatch: {rel}")
        if any(row.get("schema_version") != entry.get("schema_version") for row in partition):
            raise ValueError(f"Run-record schema version mismatch: {rel}")
        if entry["round_id"] == "unassigned":
            if any(
                row.get("audit_round") != "unmapped"
                or not isinstance(row.get("round_id"), dict)
                or row["round_id"].get("missing") != unassigned_code
                for row in partition
            ):
                raise ValueError(f"Unassigned round-tag reason mismatch: {rel}")
        elif any(row.get("audit_round") != entry["round_id"] or row.get("round_id") != entry["round_id"] for row in partition):
            raise ValueError(f"Run-record round mismatch: {rel}")
        by_round[entry["round_id"]] = {**entry, "path": rel}
        rows.extend(partition)
    if "unassigned" not in by_round:
        raise ValueError("Run-record index has no unassigned partition")
    return index, rows, by_round


def load_csv(rel: str) -> list[dict]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def page_record(route: str, title: str, markdown: str, source_paths: list[str], status: str = "") -> dict:
    normalized_route = "/" if route == "/" else "/" + route.strip("/") + "/"
    source_paths = list(dict.fromkeys(source_paths))
    return {
        "route": normalized_route,
        "title": title,
        "status": status,
        "markdown": markdown.strip() + "\n",
        "source_path": source_paths[0] if source_paths else "README.md",
        "sources": source_paths,
    }


def related_markdown(hypotheses: list[str], rounds: list[str], claims: list[str]) -> str:
    lines: list[str] = []
    if hypotheses:
        lines += ["### Related hypotheses", ""]
        lines += [f"- [{hid}](/hypotheses/{hid.lower()}/)" for hid in hypotheses]
        lines.append("")
    if rounds:
        lines += ["### Related experiments", ""]
        lines += [f"- [{rid}](/rounds/{rid.lower()}/)" for rid in rounds]
        lines.append("")
    if claims:
        lines += ["### Related claims", ""]
        lines += [f"- [{cid}](/claims/{cid.lower()}/)" for cid in claims]
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    revision = run_git("rev-parse", "HEAD")
    tracked = run_git("ls-files").splitlines()

    hypothesis_rows = parse_hypotheses()
    h_by_id = {item["id"]: item for item in hypothesis_rows}
    family_ids = sorted({item["family_id"] for item in hypothesis_rows})

    findings_intro, findings = parse_findings()
    if {item["id"] for item in findings} != set(family_ids) or len(findings) != 14:
        raise ValueError("FINDINGS.md does not contain exactly one section for each registered family")
    finding_by_id = {item["id"]: item for item in findings}

    round_ids = json.loads(read_text("rounds/index.json"))
    if not isinstance(round_ids, list) or not all(isinstance(item, str) for item in round_ids):
        raise ValueError("rounds/index.json must be a list of round IDs")
    if len(round_ids) != len(set(round_ids)):
        raise ValueError("rounds/index.json contains duplicate IDs")
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*", item) for item in round_ids):
        raise ValueError("rounds/index.json contains an ID outside the stable route grammar")

    tracked_round_dirs = sorted(
        {
            PurePosixPath(path).parts[1]
            for path in tracked
            if path.startswith("rounds/") and len(PurePosixPath(path).parts) > 2
        }
    )
    unregistered_round_dirs = sorted(set(tracked_round_dirs) - set(round_ids))
    missing_round_dirs = sorted(set(round_ids) - set(tracked_round_dirs))
    inventory_failures = [
        f"rounds/index.json names {rid}, but no tracked rounds/{rid}/ source exists."
        for rid in missing_round_dirs
    ]

    claims = load_jsonl("results/claim-ledger.jsonl")
    claim_ids = [row.get("claim_id") for row in claims]
    if any(not isinstance(cid, str) or not cid for cid in claim_ids) or len(claim_ids) != len(set(claim_ids)):
        raise ValueError("Claim ledger contains a missing or duplicate claim_id")
    claim_by_id = {row["claim_id"]: row for row in claims}

    crosswalk = load_indexed_jsonl("results/source-crosswalk")
    round_statuses: dict[str, set[str]] = defaultdict(set)
    round_hypotheses: dict[str, set[str]] = defaultdict(set)
    round_claims: dict[str, set[str]] = defaultdict(set)
    for row in crosswalk:
        rid = row.get("round_id")
        if not isinstance(rid, str):
            continue
        if row.get("record_role") == "round_disposition" and row.get("round_status"):
            round_statuses[rid].add(str(row["round_status"]))
        for hid in row.get("hypothesis_ids") or []:
            if hid in h_by_id:
                round_hypotheses[rid].add(hid)
        for cid in row.get("claim_ids") or []:
            if cid in claim_by_id:
                round_claims[rid].add(cid)
    for rid, statuses in round_statuses.items():
        if len(statuses) > 1:
            inventory_failures.append(
                f"Conflicting structured round statuses for {rid}: {', '.join(sorted(statuses))}."
            )

    try:
        grade_join_rows = load_csv("results/grade-join.csv")
        grade_join_input = load_jsonl("results/grade-join-input.jsonl")
    except OSError:
        grade_join_rows = []
        grade_join_input = []
    run_record_index, run_record_rows, run_record_files = load_indexed_run_records()
    run_record_sources = {
        row["cell_id"]: f"results/run-records/{row['round_id'] if isinstance(row.get('round_id'), str) else 'unassigned'}.jsonl"
        for row in run_record_rows
        if isinstance(row.get("cell_id"), str)
    }
    graded_run_ids = [
        row.get("cell_id") for row in run_record_rows
        if row.get("graded") is True and isinstance(row.get("cell_id"), str)
    ]
    public_grade_ids = {
        row.get("cell_id") for row in load_jsonl("reproduce/inputs/grades.final.jsonl")
        if isinstance(row.get("cell_id"), str) and row.get("cell_id")
    }
    grade_join_ids = [row.get("delivery_id") for row in grade_join_rows]
    grade_ids = [row.get("official_grade_id") for row in grade_join_rows]
    public_join_count = sum(grade_id in public_grade_ids for grade_id in grade_ids)
    capture_reported_count = sum(grade_id not in public_grade_ids for grade_id in grade_ids)
    crosswalk_by_delivery: dict[str, list[dict]] = defaultdict(list)
    exact_crosswalk_ids = set()
    for row in crosswalk:
        if row.get("record_role") != "captured_delivery":
            continue
        source_id = row.get("source_record_id")
        expected_source = run_record_sources.get(source_id)
        if expected_source:
            if row.get("source_file") != expected_source:
                raise ValueError(f"Captured-delivery crosswalk path does not match the run-record index: {source_id}")
            crosswalk_by_delivery[str(row.get("source_record_id"))].append(row)
            if row.get("linkage_status") == "exact_official_grade_join":
                exact_crosswalk_ids.add(row.get("source_record_id"))
        elif str(row.get("source_file", "")).startswith("results/run-records/"):
            raise ValueError(f"Captured-delivery crosswalk ID is absent from the run-record index: {source_id}")
    crosswalk_complete = bool(grade_join_rows) and all(
        len(crosswalk_by_delivery.get(str(row.get("delivery_id")), [])) == 1
        and crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("source_record_id") == row.get("official_grade_id")
        and crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("public_cell_id") == row.get("official_grade_id")
        and crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("linked_cell_ids") == [row.get("official_grade_id")]
        and crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("linkage_status") == (
            "exact_official_grade_join"
            if row.get("official_grade_id") in public_grade_ids
            else "capture_reported_identity_mapping"
        )
        and crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("grade_publication_label") == (
            "capture-reported grade; official export row absent"
            if row.get("publication_scope") == "capture_reported_export_absent"
            else "officially graded; in the public export"
        )
        for row in grade_join_rows
    ) and exact_crosswalk_ids == {row.get("delivery_id") for row in grade_join_rows if row.get("official_grade_id") in public_grade_ids}
    b1_join_complete = (
        len(grade_join_input) == 5020
        and len(grade_join_rows) == 5020
        and len(set(grade_join_ids)) == 5020
        and len(set(grade_ids)) == 5020
        and len(set(graded_run_ids)) == 5020
        and set(grade_join_ids) == set(graded_run_ids)
        and len({row.get("delivery_id") for row in grade_join_input}) == 5020
        and len({row.get("official_grade_id") for row in grade_join_input}) == 5020
        and all(row.get("delivery_id") == row.get("official_grade_id") for row in grade_join_input)
        and all(
            (row.get("source") == "grades.final.jsonl" and "exact equality" in str(row.get("rule", "")))
            if row.get("official_grade_id") in public_grade_ids
            else (row.get("source") == "run-record capture metadata" and "capture-reported" in str(row.get("rule", "")) and "official export row absent" in str(row.get("rule", "")))
            for row in grade_join_input
        )
        and all(row.get("delivery_id") == row.get("official_grade_id") for row in grade_join_rows)
        and set(grade_ids) == {row.get("official_grade_id") for row in grade_join_input}
        and all(
            (row.get("source") == "grades.final.jsonl" and "exact equality" in str(row.get("rule", "")))
            if row.get("official_grade_id") in public_grade_ids
            else (row.get("source") == "run-record capture metadata" and "capture-reported" in str(row.get("rule", "")) and "official export row absent" in str(row.get("rule", "")))
            for row in grade_join_rows
        )
        and all(row.get("publication_scope") == ("public_export" if row.get("official_grade_id") in public_grade_ids else "capture_reported_export_absent") for row in grade_join_rows)
        and crosswalk_complete
        and public_join_count == 5020
        and capture_reported_count == 0
        and all(
            crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("grade_publication_status") == row.get("publication_scope")
            and crosswalk_by_delivery[str(row.get("delivery_id"))][0].get("grade_publication_label") == (
                "capture-reported grade; official export row absent"
                if row.get("publication_scope") == "capture_reported_export_absent"
                else "officially graded; in the public export"
            )
            for row in grade_join_rows
        )
    )

    claims_by_round: dict[str, list[dict]] = defaultdict(list)
    claims_by_hypothesis: dict[str, list[dict]] = defaultdict(list)
    for claim in claims:
        if claim.get("round_id"):
            claims_by_round[str(claim["round_id"])].append(claim)
        for hid in claim.get("hypothesis_ids") or []:
            if hid in h_by_id:
                claims_by_hypothesis[hid].append(claim)

    family_sources = sorted({item["family_source"] for item in hypothesis_rows})
    families = []
    for family_id in family_ids:
        slug = family_id.lower()
        members = [item for item in hypothesis_rows if item["family_id"] == family_id]
        family_path = members[0]["family_source"]
        family_text = read_text(family_path)
        heading = next((line[2:].strip() for line in family_text.splitlines() if line.startswith("# ")), family_id)
        title = re.sub(r"^F\d{2}\s*[—-]?\s*", "", heading)
        rounds_for_family = sorted(
            rid for rid, hs in round_hypotheses.items() if hs.intersection(item["id"] for item in members)
        )
        claims_for_family = sorted(
            {claim["claim_id"] for member in members for claim in claims_by_hypothesis[member["id"]]}
            | {cid for rid in rounds_for_family for cid in round_claims.get(rid, set())}
        )
        families.append(
            {
                "id": family_id,
                "slug": slug,
                "title": title,
                "source_path": family_path,
                "markdown": family_text,
                "hypothesis_ids": [item["id"] for item in members],
                "round_ids": rounds_for_family,
                "claim_ids": claims_for_family,
            }
        )

    reproduction_inventory = json.loads(read_text("reproduce/round-inventory.json"))
    if reproduction_inventory.get("schema_version") != "1.0":
        raise ValueError("Unsupported reproduction inventory schema")
    round_inventory = reproduction_inventory.get("rounds")
    if not isinstance(round_inventory, list):
        raise ValueError("reproduce/round-inventory.json must contain a rounds list")
    inventory_ids = [item.get("round_id") for item in round_inventory]
    if len(inventory_ids) != len(set(inventory_ids)) or set(inventory_ids) != set(round_ids):
        raise ValueError("Reproduction inventory must contain exactly one row per rounds/index.json ID")
    round_inventory_enriched = []
    for item in round_inventory:
        match = re.match(r"(?:python3?\s+)?([^\s]+\.py)(?:\s|$)", item.get("script") or "")
        round_inventory_enriched.append({**item, "script_path": match.group(1) if match else None})
    round_inventory_by_id = {item["round_id"]: item for item in round_inventory_enriched}
    inventory_script_paths = sorted(
        {
            match.group(1)
            for item in round_inventory
            if isinstance(item.get("script"), str)
            for match in [re.match(r"(?:python3?\s+)?([^\s]+\.py)(?:\s|$)", item["script"])]
            if match
        }
    )

    # The reviewed status inventory supersedes historical crosswalk labels.
    reviewed_statuses = {}
    for line in read_text("rounds/STATUS.md").splitlines():
        match = re.fullmatch(r"([^|]+) \| ([A-Z]+) \| (.+)", line)
        if match:
            reviewed_statuses[match[1].strip()] = match[2]
    if set(reviewed_statuses) != set(round_ids):
        raise ValueError("Reviewed status inventory does not match registered rounds")

    round_records = []
    for rid in round_ids:
        path = f"rounds/{rid}/README.md"
        markdown = read_text(path)
        hs = sorted(round_hypotheses.get(rid, set()), key=lambda x: int(x[1:]))
        cids = sorted({claim["claim_id"] for claim in claims_by_round.get(rid, [])} | round_claims.get(rid, set()))
        statuses = round_statuses.get(rid, set())
        status = reviewed_statuses[rid]
        title_match = re.search(r"(?m)^#\s+(.+?)\s*$", markdown)
        title = title_match.group(1) if title_match else rid
        markdown_body = re.sub(r"(?m)^#\s+.+?\n+", "", markdown, count=1)
        results_path = f"rounds/{rid}/RESULTS.md"
        reproduction = round_inventory_by_id[rid]
        script_match = re.match(r"(?:python3?\s+)?([^\s]+\.py)(?:\s|$)", reproduction.get("script") or "")
        run_record_file = run_record_files.get(rid)
        round_records.append(
            {
                "id": rid,
                "slug": rid,
                "title": title,
                "status": status,
                "source_path": path,
                "markdown": markdown_body,
                "results_source_path": results_path if (ROOT / results_path).is_file() else None,
                "results_markdown": read_text(results_path) if (ROOT / results_path).is_file() else "",
                "run_record_file": run_record_file,
                "reproduction": {**reproduction, "script_path": script_match.group(1) if script_match else None},
                "hypothesis_ids": hs,
                "family_ids": sorted({h_by_id[hid]["family_id"] for hid in hs}),
                "claim_ids": cids,
            }
        )

    evidence_intro, evidence, evidence_decision_coverage = parse_evidence_map()
    evidence_ids = {item["id"] for item in evidence}
    for clause in evidence:
        clause["round_ids"] = [rid for rid in clause["round_ids"] if rid in round_ids]
        clause["claim_ids"] = [cid for cid in clause["claim_ids"] if cid in claim_by_id]
        clause["hypothesis_ids"] = [hid for hid in clause["hypothesis_ids"] if hid in h_by_id]

    publication_register = json.loads(read_text("results/publication-blockers.json"))
    publication_blockers = publication_register.get("blockers", [])
    gate_ids = [item.get("id") for item in publication_blockers]
    if not publication_blockers or any(not isinstance(value, str) or not value for value in gate_ids) or len(set(gate_ids)) != len(gate_ids):
        raise ValueError("Publication register must contain unique named gates")
    if any(item.get("status") not in {"open", "resolved"} for item in publication_blockers):
        raise ValueError("Publication register contains an unknown gate status")
    expected_publication_status = "blocked" if any(item.get("status") != "resolved" for item in publication_blockers) else "ready"
    if publication_register.get("publication_status") != expected_publication_status:
        raise ValueError("Publication status must follow the evidence gate statuses")
    grade_register = next((item for item in publication_blockers if item.get("evidence_key") == "official_grade_export_join"), {})
    expected_grade_status = "resolved" if b1_join_complete else "open"
    if grade_register.get("status") != expected_grade_status:
        raise ValueError("Official-grade gate status differs from its independently cross-checked export evidence")
    spec_register = next((item for item in publication_blockers if item.get("evidence_key") == "spec_decision_sources"), {})
    spec_inputs = spec_register.get("evidence_inputs", [])
    expected_spec_status = "resolved" if spec_inputs and all((ROOT / item).exists() for item in spec_inputs) else "open"
    if spec_register.get("status") != expected_spec_status:
        raise ValueError("Specification-source gate status differs from its declared source files")
    if grade_register.get("evidence_path") != "results/GRADE-JOIN.md":
        raise ValueError("Official-grade gate must link results/GRADE-JOIN.md")
    publication_validation = read_text("results/publication-validation.md")

    gate_summaries = "\n".join(
        f"- {item['id']} ({item['status']}): {item.get('summary', '')}"
        for item in publication_blockers
    )
    publication_status_blurb = (
        f"Publication status is **{publication_register['publication_status']}**. "
        + " ".join(f"{item['id']} is {item['status']}: {item.get('summary', '')}" for item in publication_blockers)
    )

    indexed_families = [
        "results/source-crosswalk",
        "reproduce/inputs/run-evidence",
        "reproduce/inputs/context-evidence",
        "reproduce/inputs/ungraded-evidence",
    ]
    indexed_jsonl_files = [entry["path"] for entry in run_record_files.values()]
    index_files = ["results/run-records/index.json"]
    for directory in indexed_families:
        index, _rows = read_partitions(ROOT / directory)
        index_files.append(f"{directory}/index.json")
        indexed_jsonl_files.extend(f"{directory}/{entry['file']}" for entry in index["files"])
    jsonl_files = sorted(
        [
            str(PurePosixPath(path))
            for path in tracked
            if re.fullmatch(r"results/[^/]+\.jsonl", path) and (ROOT / path).is_file()
        ]
        + indexed_jsonl_files
    )
    index_files = sorted(set(index_files))
    json_files = ["results/missing-reasons.json"]
    reproduce_script_paths = sorted(
        path for path in tracked if path.startswith("reproduce/") and path.endswith(".py") and "/__pycache__/" not in path
    )
    # Validate each published JSONL before copying it to the static downloads.
    for rel in jsonl_files:
        load_jsonl(rel)

    source_paths = [
        "README.md",
        "site/content/research.md",
        "rounds/STATUS.md",
        "CREDITS.md",
        "reproduce/VERIFY.md",
        "reproduce/RERUN.md",
        "site/content/about.md",
        "site/content/contact.md",
        "site/content/privacy.md",
        "FINDINGS.md",
        "hypotheses/README.md",
        *family_sources,
        "rounds/index.json",
        *index_files,
        *json_files,
        "rounds/GLOSSARY.md",
        *[item["source_path"] for item in round_records],
        *[item["results_source_path"] for item in round_records if item["results_source_path"]],
        *jsonl_files,
        "results/README.md",
        "results/publication-validation.md",
        "results/publication-blockers.json",
        "EVIDENCE-MAP.md",
        "METHOD.md",
        "STANDARD.md",
        "reproduce/README.md",
        *reproduce_script_paths,
        *inventory_script_paths,
        "reproduce/round-inventory.json",
    ]
    source_paths = list(dict.fromkeys(source_paths))
    for rel in source_paths:
        path = ROOT / rel
        if not path.is_file():
            raise ValueError(f"Required site source file is missing: {rel}")
        # Reproduction scripts are linked as repository sources and represented
        # by hashes only; their contents are not copied into the generated site.
        if rel.endswith(".py"):
            continue
        content = read_text(rel)
        if PRIVATE_PATH.search(content):
            raise ValueError(f"Private filesystem path detected in site source: {rel}")

    source_files = []
    for rel in source_paths:
        if rel.endswith(".py"):
            # Scripts are linked but not rendered. Hash their committed object,
            # so unrelated edits in a dirty worktree cannot enter the snapshot.
            content = subprocess.check_output(["git", "show", f"HEAD:{rel}"], cwd=ROOT)
        else:
            content = (ROOT / rel).read_bytes()
        source_files.append(
            {
                "path": rel,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
                "url": source_url(rel, revision),
            }
        )

    families_by_id = {item["id"]: item for item in families}
    rounds_by_id = {item["id"]: item for item in round_records}

    pages: list[dict] = []
    pages.append(
        page_record(
            "/",
            "Kogen Bench",
            f"""# Kogen Bench

The research behind Kogen. What helps a coding agent finish software correctly, and at what cost? Explore experiments on models, plans, context, checks and recovery.

{read_text("site/content/research.md")}

## Start with a question

- [Read findings](/findings/)
- [Browse hypotheses](/hypotheses/)
- [Find an experiment](/rounds/)
- [Trace a specification clause to evidence](/evidence/)

## Read results with their status

The findings pages summarize the source record. A status such as INTERIM, CONFOUNDED, WITHDRAWN, or NOT-RUN limits what can be concluded. A missing value stays missing. Claim ledger rows retain their own evidence status and exact cohort; the site does not turn a source-reported number into a verified result by displaying it.

## For agents

- [Machine-readable index](/index.json)
- [Agent guide](/llms.txt)
- [Full bounded guide](/llms-full.txt)
- [Snapshot and source hashes](/snapshot.json)

## Publication status

{publication_status_blurb} See [the grade-join scope](https://github.com/KogenAI/kogen-bench/blob/{revision}/results/GRADE-JOIN.md) and [publication validation](/publication-validation/).
""",
            ["README.md", "site/content/research.md", "results/publication-blockers.json", "results/publication-validation.md", "results/GRADE-JOIN.md"],
        )
    )

    pages.append(
        page_record(
            "/findings/",
            "Findings",
            "# Findings\n\nThe family-by-family source summary is reproduced below. Figures that are not reconciled to a claim ledger remain source-reported; follow the source and related claim records for the limits.\n\n" + "\n".join(
                f"- [{item['id']} — {item['title']}](/findings/{item['slug']}/)" for item in findings
            ),
            ["FINDINGS.md"],
        )
    )
    for item in findings:
        family = families_by_id[item["id"]]
        body = (
            f"# {item['id']} — {item['title']}\n\n"
            "> Source narrative: values not linked to an eligible claim ledger row are source-reported and not independently promoted here.\n\n"
            + item["markdown"]
            + "\n\n## Related records\n\n"
            + related_markdown(family["hypothesis_ids"], family["round_ids"], family["claim_ids"])
        )
        pages.append(
            page_record(
                f"/findings/{item['slug']}/",
                item["title"],
                body,
                ["FINDINGS.md", family["source_path"]],
                "SOURCE SUMMARY",
            )
        )

    hypothesis_index_body = "# Hypotheses\n\nEach proposition and evidence status comes from the public hypothesis register. Status describes the record, not whether a proposition is true.\n\n| ID | Family | Proposition | Evidence status |\n| --- | --- | --- | --- |\n"
    for hyp in hypothesis_rows:
        proposition = hyp["proposition"].replace("|", "\\|")
        status = hyp["status"].replace("|", "\\|")
        hypothesis_index_body += (
            f"| [{hyp['id']}](/hypotheses/{hyp['slug']}/) | [{hyp['family_id']}](/families/{hyp['family_slug']}/) | "
            f"{proposition} | {status} |\n"
        )
    pages.append(page_record("/hypotheses/", "Hypotheses", hypothesis_index_body, ["hypotheses/README.md"]))

    family_index_body = "# Families\n\n" + "\n".join(
        f"- [{family['id']} — {family['title']}](/families/{family['slug']}/) · [findings](/findings/{family['slug']}/)"
        for family in families
    )
    pages.append(page_record("/families/", "Families", family_index_body, ["hypotheses/README.md"]))

    for hyp in hypothesis_rows:
        hclaims = sorted(claims_by_hypothesis.get(hyp["id"], []), key=lambda row: row["claim_id"])
        hrounds = sorted(
            {rid for rid, hs in round_hypotheses.items() if hyp["id"] in hs},
        )
        hfamilypath = hyp["family_source"]
        body = (
            f"# {hyp['id']}\n\n"
            f"**Family:** [{hyp['family_id']}](/families/{hyp['family_slug']}/) — {families_by_id[hyp['family_id']]['title']}\n\n"
            f"**Falsifiable proposition:** {hyp['proposition']}\n\n"
            f"**Current evidence status:** {hyp['status']}\n\n"
            "This proposition and status are transcribed from the source hypothesis register; any numeric target in the proposition is not a measured result. The register does not provide a separate falsification rule or next-test field for this entry. The linked family and round sources retain their original limits.\n\n"
            + related_markdown([hyp["id"]], hrounds, [row["claim_id"] for row in hclaims])
        )
        pages.append(page_record(f"/hypotheses/{hyp['slug']}/", hyp["id"], body, ["hypotheses/README.md", hfamilypath], hyp["status"]))

    for family in families:
        body = (
            f"# {family['id']} — {family['title']}\n\n"
            "> Family source text is narrative from the repository. Any numeric value in that text remains source-reported unless an exact claim ledger entry supplies it.\n\n"
            + family["markdown"]
            + "\n\n## Related structured records\n\n"
            + related_markdown(family["hypothesis_ids"], family["round_ids"], family["claim_ids"])
        )
        pages.append(
            page_record(
                f"/families/{family['slug']}/",
                f"{family['id']} — {family['title']}",
                body,
                [family["source_path"], "hypotheses/README.md"],
                "SOURCE SUMMARY",
            )
        )

    rounds_index_body = "# Experiments and rounds\n\nThe canonical register is `rounds/index.json`. Rows without a structured status remain marked as such. Filters work with JavaScript; the complete table remains in the HTML without it.\n\n| Round | Status | Families | Related hypotheses |\n| --- | --- | --- | --- |\n"
    for round_item in round_records:
        families_text = ", ".join(f"[{fid}](/families/{fid.lower()}/)" for fid in round_item["family_ids"]) or "Not linked"
        hs_text = ", ".join(f"[{hid}](/hypotheses/{hid.lower()}/)" for hid in round_item["hypothesis_ids"]) or "Not linked"
        rounds_index_body += (
            f"| [{round_item['id']}](/rounds/{round_item['slug']}/) | {round_item['status']} | {families_text} | {hs_text} |\n"
        )
    pages.append(page_record("/rounds/", "Experiments and rounds", rounds_index_body, ["rounds/index.json", "results/source-crosswalk/index.json"]))

    for round_item in round_records:
        note = (
            "No structured status is available in the source crosswalk; the README and any results document are still shown as source material."
            if round_item["status"] == "STATUS NOT STRUCTURED"
            else f"Reviewed status from rounds/STATUS.md: {round_item['status']}."
        )
        reproduction = round_item["reproduction"]
        inputs_note = ", ".join(f"`{path}`" for path in reproduction["inputs"]) or "none identified"
        script_note = f"`{reproduction['script']}`" if reproduction["script"] else "none published"
        result_section = (
            "\n\n## Results source\n\n" + round_item["results_markdown"]
            if round_item["results_markdown"]
            else ""
        )
        body = (
            f"# {round_item['title']}\n\n"
            f"**Round ID:** {round_item['id']}  \n**Status:** {round_item['status']}\n\n"
            f"> {note}\n\n"
            "> Round README and results text are source material. Numeric values not tied to a claim ledger record remain source-reported.\n\n"
            + round_item["markdown"]
            + result_section
            + (
                f"\n\n## Captured run records\n\n[{round_item['run_record_file']['path']}](/downloads/{round_item['run_record_file']['path']}) · "
                f"{round_item['run_record_file']['record_count']} records · {round_item['run_record_file']['bytes']:,} bytes · "
                f"[immutable source]({source_url(round_item['run_record_file']['path'], revision)}).\n"
                if round_item["run_record_file"]
                else "\n\n## Captured run records\n\nNo records for this round are listed in the [run-record index](/downloads/results/run-records/index.json).\n"
            )
            + "\n\n## Reproduction inventory\n\n"
            + f"- **Type:** {reproduction['replay_type']}\n- **Script:** {script_note}\n- **Inputs:** {inputs_note}\n"
            + f"- **Full execution replay:** {'available' if reproduction['full_execution_replayable'] else 'unavailable'}\n"
            + f"- **Scope:** {reproduction['availability_note']}\n\n"
            + "See the [complete per-round reproduction inventory](/reproduce/) and the [repository reproduction guide](https://github.com/KogenAI/kogen-bench/blob/"
            + revision
            + "/reproduce/README.md).\n\n## Related records\n\n"
            + related_markdown(round_item["hypothesis_ids"], [round_item["id"]], round_item["claim_ids"])
        )
        pages.append(
            page_record(
                f"/rounds/{round_item['slug']}/",
                round_item["title"],
                body,
                [
                    round_item["source_path"],
                    *([round_item["results_source_path"]] if round_item["results_source_path"] else []),
                    "results/run-records/index.json",
                    *([round_item["run_record_file"]["path"]] if round_item["run_record_file"] else []),
                    "rounds/index.json",
                    "results/source-crosswalk/index.json",
                    "rounds/STATUS.md",
                    "reproduce/round-inventory.json",
                    *([reproduction["script_path"]] if reproduction.get("script_path") else []),
                ],
                round_item["status"],
            )
        )

    claims_index_body = "# Claims\n\nEach record is transcribed from `results/claim-ledger.jsonl`. Ledger status, evidence status, population, and unit remain attached; the site does not recompute or pool claim values.\n\n| Claim | Status | Metric | Round | Hypotheses |\n| --- | --- | --- | --- | --- |\n"
    for claim in claims:
        round_cell = f"[{claim.get('round_id')}](/rounds/{str(claim.get('round_id')).lower()}/)" if claim.get("round_id") in rounds_by_id else "Not linked"
        hypothesis_cell = ", ".join(
            f"[{hid}](/hypotheses/{hid.lower()}/)" for hid in claim.get("hypothesis_ids", []) if hid in h_by_id
        ) or "Not linked"
        claims_index_body += (
            f"| [{claim['claim_id']}](/claims/{claim['claim_id'].lower()}/) | {claim.get('claim_status') or 'Not recorded'} | "
            f"{claim.get('metric') or 'Not recorded'} | {round_cell} | {hypothesis_cell} |\n"
        )
    pages.append(page_record("/claims/", "Claims", claims_index_body, ["results/claim-ledger.jsonl"]))

    for claim in claims:
        cid = claim["claim_id"]
        rid = claim.get("round_id")
        hs = [hid for hid in (claim.get("hypothesis_ids") or []) if hid in h_by_id]
        exact = claim.get("exact_cell_ids") or []
        values = {
            key: claim.get(key)
            for key in (
                "metric",
                "numerator",
                "denominator",
                "unit",
                "comparison",
                "analysis_rule",
                "evidence_status",
                "claim_status",
                "publication_status",
                "reported_values",
                "interpretation",
                "reconciliation_status",
                "denominator_variants",
                "evidence",
            )
            if key in claim
        }
        values_md = "\n".join(f"- **{key}:** `{json.dumps(value, ensure_ascii=False, sort_keys=True)}`" for key, value in values.items())
        body = (
            f"# {cid}\n\n"
            "**Source:** `results/claim-ledger.jsonl`  \n"
            f"**Ledger status:** {claim.get('claim_status') or 'Not recorded'}  \n"
            f"**Evidence status:** {claim.get('evidence_status') or 'Not recorded'}\n\n"
            "Values below are transcribed from this claim-ledger entry. The site does not recalculate them. A status such as INTERIM, CONFOUNDED, or WITHDRAWN is not a validated advantage.\n\n"
            "## Claim fields\n\n"
            + values_md
            + "\n\n## Population references\n\n"
            + (f"Round: [{rid}](/rounds/{str(rid).lower()}/)\n\n" if rid in rounds_by_id else "Round: not linked to the round register.\n\n")
            + related_markdown(hs, [rid] if rid in rounds_by_id else [], [])
            + (f"Exact cell IDs are listed in the [source ledger](https://github.com/KogenAI/kogen-bench/blob/{revision}/results/claim-ledger.jsonl); the site does not join outcome-only rows by guessed keys.\n" if exact else "The ledger does not provide exact cell IDs for this claim.\n")
        )
        pages.append(page_record(f"/claims/{cid.lower()}/", cid, body, ["results/claim-ledger.jsonl"], str(claim.get("claim_status") or "Not recorded")))

    evidence_index_body = "# Evidence map\n\n" + evidence_intro + "\n\nEach clause page follows the authored clause map in `EVIDENCE-MAP.md`. Related IDs come from explicit source references and structured claim/crosswalk records.\n\n" + "\n".join(
        f"- [{clause['title'].replace('<slug>', '&lt;slug&gt;')}](/evidence/{clause['id']}/)" for clause in evidence
    ) + "\n\n## Decision-ID coverage\n\n" + evidence_decision_coverage
    pages.append(page_record("/evidence/", "Evidence map", evidence_index_body, ["EVIDENCE-MAP.md", "results/publication-blockers.json"]))
    for clause in evidence:
        title_markdown = clause["title"].replace("<slug>", "&lt;slug&gt;")
        body = (
            f"# {title_markdown}\n\n"
            "> The clause text and evidence status below are from the source map. Numeric figures remain source-reported unless tied to a claim-ledger record.\n\n"
            + clause["markdown"]
            + "\n\n## Related records\n\n"
            + related_markdown(clause["hypothesis_ids"], clause["round_ids"], clause["claim_ids"])
        )
        pages.append(page_record(f"/evidence/{clause['id']}/", clause["title"], body, ["EVIDENCE-MAP.md"], "SOURCE MAP"))

    comparison_claims = [claim for claim in claims if claim.get("comparison") not in (None, "", [], {})]
    comparison_body = (
        "# Comparisons\n\nNo new winner is computed here. This page lists only claim-ledger records with an explicit `comparison` field. Cohorts remain separate, and source status is shown on each claim.\n\n"
        + ("## Explicit comparison records\n\n" if comparison_claims else "No claim-ledger record currently supplies a structured comparison field.\n\n")
        + "\n".join(
            f"- [{claim['claim_id']}](/claims/{claim['claim_id'].lower()}/) — {claim.get('claim_status', 'Not recorded')} · {claim.get('evidence_status', 'Not recorded')}"
            for claim in comparison_claims
        )
    )
    pages.append(page_record("/comparisons/", "Comparisons", comparison_body, ["results/claim-ledger.jsonl", "FINDINGS.md"]))

    method_text = read_text("METHOD.md")
    standard_text = read_text("STANDARD.md")
    methods_body = (
        "# Method\n\nThe text in these source documents is reproduced as authored. Numeric historical values in narrative remain source-reported unless an exact claim-ledger record identifies them.\n\n"
        "## Method and interpretation\n\n"
        + method_text
        + "\n\n## Standard run record\n\n"
        + standard_text
    )
    pages.append(page_record("/methods/", "Method", methods_body, ["METHOD.md", "STANDARD.md"], "SOURCE DOCUMENTS"))

    pages.append(
        page_record(
            "/publication-validation/",
            "Publication validation",
            f"# Publication validation\n\n{publication_status_blurb} The full validation report and structured evidence-gate register are below.\n\n"
            + publication_validation
            + "\n\n## Structured evidence-gate register\n\n"
            + gate_summaries
            + "\n\nSee [GRADE-JOIN.md](" + source_url("results/GRADE-JOIN.md", revision) + ") and the [evidence map](/evidence/).\n",
            ["results/publication-validation.md", "results/publication-blockers.json", "results/GRADE-JOIN.md", "EVIDENCE-MAP.md"],
            "BLOCKED",
        )
    )

    reproduce_text = read_text("reproduce/README.md")
    reproduce_body = (
        "# Reproduce\n\nThe instructions below are reproduced from `reproduce/README.md`. The verification guide distinguishes recomputable records from missing historical inputs. The rerun guide covers the published task bases and grading material, requirements, and remaining gaps.\n\n"
        + reproduce_text
        + "\n\n## Per-round reproduction inventory\n\nSee the complete [HTML inventory](/reproduce/) for one row per registered round, including script, inputs, replay type, and full execution replay availability. The structured inventory is [`reproduce/round-inventory.json`](https://github.com/KogenAI/kogen-bench/blob/"
        + revision
        + "/reproduce/round-inventory.json).\n"
        + "\n\n## Public reproduction scripts\n\n"
        + "\n".join(f"- [`{path}`]({source_url(path, revision)})" for path in reproduce_script_paths)
    )
    pages.append(page_record("/reproduce/", "Reproduce", reproduce_body, ["reproduce/README.md", *reproduce_script_paths], "SOURCE GUIDE"))

    for route, title, source in [("verify", "Verify published numbers", "reproduce/VERIFY.md"), ("rerun", "Rerun and regrade tasks", "reproduce/RERUN.md"), ("credits", "Credits", "CREDITS.md")]:
        pages.append(page_record(f"/{route}/", title, read_text(source), [source], "SOURCE GUIDE"))

    glossary_text = read_text("rounds/GLOSSARY.md")
    pages.append(
        page_record(
            "/glossary/",
            "Glossary",
            "> Terms and definitions are reproduced from the public glossary. Numeric historical values in source narrative remain source-reported unless tied to a claim-ledger record.\n\n" + glossary_text,
            ["rounds/GLOSSARY.md"],
            "SOURCE DOCUMENT",
        )
    )

    download_files = []
    for rel in jsonl_files:
        record_entry = next((entry for entry in run_record_files.values() if entry["path"] == rel), None)
        download_files.append(
            {
                "path": rel,
                "url": "/downloads/" + rel,
                "source_url": source_url(rel, revision),
                "description": (
                    f"Round {record_entry['round_id']}: {record_entry['record_count']} records, {record_entry['bytes']:,} bytes."
                    if record_entry
                    else "Direct public JSONL source snapshot. The site does not merge or recompute rows from this file."
                ),
            }
        )
    data_body = (
        "# Data downloads\n\nThese are direct copies of public repository files. Outcome exports, captured run records, and claim-ledger entries are distinct inputs. Downloading a file does not make an unreconciled row an exact-cell claim.\n\n"
        "## Publication evidence status\n\n" + publication_status_blurb + " See [GRADE-JOIN.md](" + source_url("results/GRADE-JOIN.md", revision) + ") and [publication validation](/publication-validation/).\n\n"
        "## Public JSONL files\n\nRun records and source evidence are split by round; each family has a checksummed index. Missing-value codes are expanded by the [legend](/downloads/results/missing-reasons.json).\n\n"
        + "\n".join(f"- [`{item['path']}`]({item['url']}) · [source]({item['source_url']})" for item in download_files)
        + "\n\n## Snapshot\n\n- [Source hashes and immutable links](/snapshot.json)\n- [Round index](/downloads/rounds/index.json)\n- [Run-record index](/downloads/results/run-records/index.json)\n"
        + "- [Source-crosswalk index](/downloads/results/source-crosswalk/index.json)\n"
        + "- [Run-evidence index](/downloads/reproduce/inputs/run-evidence/index.json)\n"
        + "- [Context-evidence index](/downloads/reproduce/inputs/context-evidence/index.json)\n"
        + "- [Ungraded-evidence index](/downloads/reproduce/inputs/ungraded-evidence/index.json)\n"
        + "- [Missing-reasons legend](/downloads/results/missing-reasons.json)\n- [Claim and relationship index](/index.json)\n"
    )
    pages.append(page_record("/data/", "Data downloads", data_body, ["results/README.md", "results/GRADE-JOIN.md", "rounds/index.json", *index_files, *json_files, "results/claim-ledger.jsonl"]))

    for name in ("about", "contact", "privacy"):
        source = f"site/content/{name}.md"
        pages.append(page_record(f"/{name}/", name.capitalize(), read_text(source), [source]))

    # Machine-readable agent index: every hypothesis, registered round, and claim gets a stable URL.
    index = {
        "schema_version": "1.0",
        "downloads": download_files,
        "site": "https://bench.kogen.dev",
        "data_revision": revision,
        "number_policy": "Hypothesis, round, and claim identifiers are identifiers. Numeric values in source narrative are source-reported; claim values are transcribed from the claim ledger with their evidence status.",
        "snapshot_url": "/snapshot.json",
        "publication_status": publication_register["publication_status"],
        "publication_validation_url": "/publication-validation/",
        "publication_blockers": publication_blockers,
        "unregistered_round_dirs": unregistered_round_dirs,
        "reproduction_inventory_url": "/reproduce/",
        "full_execution_replayable_rounds": sorted(item["round_id"] for item in round_inventory_enriched if item["full_execution_replayable"]),
        "hypotheses": [
            {
                "id": hyp["id"],
                "url": f"/hypotheses/{hyp['slug']}/",
                "status": hyp["status"],
                "family_id": hyp["family_id"],
                "family_url": f"/families/{hyp['family_slug']}/",
                "proposition": hyp["proposition"],
                "source": source_url("hypotheses/README.md", revision),
                "rounds": sorted(rid for rid, hs in round_hypotheses.items() if hyp["id"] in hs),
                "claims": sorted(row["claim_id"] for row in claims_by_hypothesis.get(hyp["id"], [])),
            }
            for hyp in hypothesis_rows
        ],
        "rounds": [
            {
                "id": item["id"],
                "url": f"/rounds/{item['slug']}/",
                "status": item["status"],
                "title": item["title"],
                "family_ids": item["family_ids"],
                "hypotheses": item["hypothesis_ids"],
                "claims": item["claim_ids"],
                "source": source_url(item["source_path"], revision),
                "run_records": item["run_record_file"],
                "reproduction": item["reproduction"],
            }
            for item in round_records
        ],
        "claims": [
            {
                "id": row["claim_id"],
                "url": f"/claims/{row['claim_id'].lower()}/",
                "status": row.get("claim_status", "Not recorded"),
                "evidence_status": row.get("evidence_status", "Not recorded"),
                "round_id": row.get("round_id"),
                "round_url": f"/rounds/{str(row.get('round_id')).lower()}/" if row.get("round_id") in rounds_by_id else None,
                "hypothesis_ids": [hid for hid in row.get("hypothesis_ids", []) if hid in h_by_id],
                "metric": row.get("metric"),
                "unit": row.get("unit"),
                "reconciliation_status": row.get("reconciliation_status"),
                "source": source_url("results/claim-ledger.jsonl", revision),
            }
            for row in claims
        ],
        "evidence": [
            {
                "id": clause["id"],
                "title": clause["title"],
                "url": f"/evidence/{clause['id']}/",
                "hypothesis_ids": clause["hypothesis_ids"],
                "round_ids": clause["round_ids"],
                "claim_ids": clause["claim_ids"],
                "source": source_url("EVIDENCE-MAP.md", revision),
            }
            for clause in evidence
        ],
    }

    family_data = [
        {
            **family,
            "finding_title": finding_by_id[family["id"]]["title"],
            "hypotheses": [hyp for hyp in hypothesis_rows if hyp["family_id"] == family["id"]],
        }
        for family in families
    ]
    data = {
        "meta": {
            "site": "https://bench.kogen.dev",
            "revision": revision,
            "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "number_policy": "Numbers from structured claims are transcribed from results/claim-ledger.jsonl. Numeric values in source narrative are labelled source-reported; the site does not derive numeric results from prose.",
            "source_files": source_files,
            "inventory_failures": inventory_failures,
            "publication_status": publication_register["publication_status"],
            "publication_blockers": publication_blockers,
            "publication_gates": publication_blockers,
            "publication_join": {
                "exact_complete": b1_join_complete,
                "total": len(grade_join_rows),
                "public_export": public_join_count,
                "capture_reported_export_absent": capture_reported_count,
                "evidence_path": "results/GRADE-JOIN.md",
            },
            "round_index_ids": round_ids,
            "unregistered_round_dirs": unregistered_round_dirs,
            "jsonl_files": jsonl_files,
            "index_files": index_files,
            "json_files": json_files,
        },
        "findings_intro": findings_intro,
        "documents": {
            "method": read_text("METHOD.md"),
            "standard": read_text("STANDARD.md"),
            "reproduce": read_text("reproduce/README.md"),
            "publication_validation": publication_validation,
            "glossary": read_text("rounds/GLOSSARY.md"),
        },
        "findings": findings,
        "families": family_data,
        "hypotheses": hypothesis_rows,
        "rounds": round_records,
        "claims": claims,
        "evidence": evidence,
        "evidence_map_intro": evidence_intro,
        "evidence_decision_coverage": evidence_decision_coverage,
        "reproduction_inventory": round_inventory_enriched,
        "round_inventory_full_replay_ids": sorted(item["round_id"] for item in round_inventory_enriched if item["full_execution_replayable"]),
        "downloads": download_files,
        "reproduce_scripts": reproduce_script_paths,
        "index": index,
        "pages": pages,
    }
    (GENERATED / "site-data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(
        f"Prepared {len(hypothesis_rows)} hypotheses, {len(round_records)} registered rounds, "
        f"{len(claims)} claims, {len(evidence_ids)} evidence clauses, and {len(source_files)} source files."
    )
    for failure in inventory_failures:
        print(f"DATA GATE: {failure}")
    for round_id in unregistered_round_dirs:
        print(f"ARCHIVE EXCLUSION: tracked rounds/{round_id}/ is unregistered and omitted from this site snapshot.")


if __name__ == "__main__":
    main()
