#!/usr/bin/env python3
"""Validate generated routes, source links, privacy, and numeric provenance labels."""

from __future__ import annotations

import html
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import threading
from html.parser import HTMLParser
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit


SITE = Path(__file__).resolve().parents[1]
ROOT = SITE.parent
DIST = SITE / "dist"
DATA = json.loads((SITE / ".generated" / "site-data.json").read_text(encoding="utf-8"))
PUBLICATION_BLOCKERS = DATA.get("meta", {}).get("publication_blockers", [])
PRIVATE_PATH = re.compile(
    r"(?<![A-Za-z0-9])(?:/(?:Users|home|tmp|private|Volumes|var/folders)/[^\s\"'<>]+|"
    r"~/(?:Library|Documents|Desktop|Areas)/[^\s\"'<>]+|"
    r"[A-Za-z]:\\(?:Users|home|Documents)\\[^\s\"'<>]+)"
)
NUMERIC_ID = re.compile(r"(?<![A-Za-z0-9])(?:[A-Z]{1,5}[A-Za-z0-9-]*\d[A-Za-z0-9-]*|[a-z]{1,5}[a-z0-9-]*\d[a-z0-9-]*|[0-9a-f]{10,40})(?![A-Za-z0-9])")
NUMBER = re.compile(r"\d")


class PageParser(HTMLParser):
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str, str]] = []
        self.ids: set[str] = set()
        self.has_markdown_alternate = False
        self.has_github_source = False
        self.has_policy = False
        self.origin_stack: list[tuple[str, set[str]]] = []
        self.text_chunks: list[tuple[str, str]] = []
        self.skip_text = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
        if tag in {"a", "link"} and values.get("href"):
            rel = values.get("rel", "")
            href = values["href"]
            self.links.append((href, rel, tag))
            if tag == "link" and "alternate" in rel and values.get("type") == "text/markdown":
                self.has_markdown_alternate = True
            if href.startswith("https://github.com/KogenAI/kogen-bench/blob/"):
                self.has_github_source = True
        if tag in {"script", "img", "source"} and values.get("src"):
            self.links.append((values["src"], "", tag))
        if tag == "body" and values.get("data-number-policy") == "claim-ledger-or-source-reported":
            self.has_policy = True
        classes = set(values.get("class", "").split())
        origins = set()
        if "source-reported" in classes or values.get("data-origin") == "source-reported":
            origins.add("source-reported")
        origin = values.get("data-origin")
        if origin in {"claim-ledger", "source-register", "round-crosswalk", "snapshot", "identifier"}:
            origins.add(origin)
        if self.origin_stack:
            origins |= self.origin_stack[-1][1]
        if tag not in self.VOID_TAGS:
            self.origin_stack.append((tag, origins))
        if tag in {"script", "style", "title"}:
            self.skip_text += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "title"} and self.skip_text:
            self.skip_text -= 1
        if tag not in self.VOID_TAGS:
            for index in range(len(self.origin_stack) - 1, -1, -1):
                if self.origin_stack[index][0] == tag:
                    del self.origin_stack[index:]
                    break

    def handle_data(self, data: str) -> None:
        if not self.skip_text and data.strip():
            origin = ",".join(sorted(self.origin_stack[-1][1])) if self.origin_stack else ""
            self.text_chunks.append((data, origin))


def output_path_for_href(href: str, current_file: Path) -> tuple[Path | None, str]:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None, ""
    path = unquote(parsed.path)
    if not path:
        return current_file, parsed.fragment
    if path.startswith("/"):
        target = DIST / path.lstrip("/")
    else:
        target = (current_file.parent / path).resolve()
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    elif not target.suffix:
        index_target = target / "index.html"
        target = index_target if index_target.exists() else target.with_suffix(".html")
    return target, parsed.fragment


def is_numeric_id_chunk(text: str) -> bool:
    residue = NUMERIC_ID.sub("", text)
    return not NUMBER.search(residue)


def check_intent_phone_width(errors: list[str]) -> str:
    css = (SITE / "src/styles/global.css").read_text(encoding="utf-8")
    if ".page-title h1{min-width:0;max-width:100%;overflow-wrap:anywhere;word-break:normal}" not in css:
        errors.append("Intent clause heading lacks the long-token phone-wrap rule")
    candidates = [
        shutil.which(name)
        for name in ("google-chrome", "chromium", "chromium-browser", "chrome")
    ]
    candidates.extend(
        [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    )
    browser = next((Path(item) for item in candidates if item and Path(item).is_file()), None)
    if browser is None:
        return "skipped (Chromium unavailable; CSS reflow rule checked)"

    route = "/evidence/21-intent-kogenintentsintentmd/"
    probe = DIST / "__mobile-width-check.html"
    probe.write_text(
        "<!doctype html><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>html,body{margin:0;width:100%;height:100%;border:0}"
        "iframe{margin:0;width:390px;height:900px;border:0}</style>"
        f"<iframe id='target' src='{route}'></iframe><output id='result'></output>"
        "<script>const f=document.querySelector('#target');const o=document.querySelector('#result');"
        "f.addEventListener('load',()=>{const d=f.contentDocument.documentElement;"
        "const cw=d.clientWidth,sw=d.scrollWidth,fw=Math.round(f.getBoundingClientRect().width);"
        "const ok=fw===390&&cw===390&&sw<=cw+1;"
        "document.documentElement.dataset.mobileWidth=ok?'PASS':`FAIL-${sw}-${cw}`;"
        "o.textContent=`intent document scrollWidth=${sw}, clientWidth=${cw}, frame=${fw}`;});</script>",
        encoding="utf-8",
    )

    class QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DIST), **kwargs)

        def log_message(self, *_args):
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    try:
        with tempfile.TemporaryDirectory(prefix="kogen-mobile-check-") as profile:
            try:
                result = subprocess.run(
                    [
                        str(browser),
                        "--headless=new",
                        "--disable-gpu",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-background-networking",
                        "--disable-extensions",
                        "--disable-default-apps",
                        "--no-first-run",
                        "--hide-scrollbars",
                        "--window-size=390,900",
                        "--virtual-time-budget=3500",
                        f"--user-data-dir={profile}",
                        "--dump-dom",
                        f"http://127.0.0.1:{server.server_address[1]}/__mobile-width-check.html",
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                output = result.stdout
                completed = result.returncode == 0
            except subprocess.TimeoutExpired as exc:
                output = exc.stdout or ""
                if isinstance(output, bytes):
                    output = output.decode(errors="replace")
                # Chrome on macOS can keep background processes alive after it
                # has dumped the page. The DOM marker proves the measurement
                # finished, even if Chrome does not terminate promptly.
                completed = 'data-mobile-width="PASS"' in output
                if not completed:
                    errors.append("Intent clause page measurement did not complete before the browser timeout")
                    return "failed"
        if not completed or 'data-mobile-width="PASS"' not in output:
            failed = re.search(r'data-mobile-width="([^"]+)"', output)
            errors.append("Intent clause page exceeds its 390px viewport" + (f" ({failed.group(1)})" if failed else "; browser measurement did not complete"))
            return "failed"
        measurement = re.search(r"intent document scrollWidth=(\d+), clientWidth=(\d+)", output)
        if measurement:
            return f"passed at 390px ({measurement.group(1)}px scroll / {measurement.group(2)}px client)"
        return "passed at 390px"
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"Intent clause phone-width browser assertion failed: {exc}")
        return "failed"
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=2)
        probe.unlink(missing_ok=True)


def main() -> None:
    errors: list[str] = []
    page_files = sorted(DIST.rglob("*.html"))
    content_pages = [path for path in page_files if path.name != "404.html"]
    page_count = len(content_pages)

    for failure in DATA["meta"]["inventory_failures"]:
        errors.append(f"data gate: {failure}")

    expected_hypotheses = {f"H{i:02d}" for i in range(1, 154)}
    index_path = DIST / "index.json"
    snapshot_path = DIST / "snapshot.json"
    agent_paths = [DIST / name for name in ("llms.txt", "llms-full.txt", "index.json", "snapshot.json", "search-index.json", "sitemap.xml")]
    for path in agent_paths:
        if not path.is_file():
            errors.append(f"missing agent surface: /{path.relative_to(DIST)}")
    if index_path.is_file():
        index = json.loads(index_path.read_text(encoding="utf-8"))
        actual_hypotheses = {item["id"] for item in index.get("hypotheses", [])}
        if actual_hypotheses != expected_hypotheses:
            errors.append("/index.json does not contain H01–H153 exactly once")
        if len(index.get("hypotheses", [])) != 153:
            errors.append("/index.json has a duplicate or missing hypothesis route")
        if len(index.get("rounds", [])) != len(DATA["rounds"]):
            errors.append("/index.json round inventory differs from rounds/index.json")
        if index.get("unregistered_round_dirs") != DATA["meta"].get("unregistered_round_dirs", []):
            errors.append("/index.json does not disclose tracked, unregistered round directories omitted from the archive")
        if len(index.get("claims", [])) != len(DATA["claims"]):
            errors.append("/index.json claim inventory differs from the claim ledger")
        if not index.get("number_policy"):
            errors.append("/index.json does not state numeric provenance policy")
        blockers = index.get("publication_blockers") or []
        blocker_ids = [item.get("id") for item in blockers]
        if not blockers or any(not isinstance(value, str) or not value for value in blocker_ids) or len(set(blocker_ids)) != len(blocker_ids):
            errors.append("/index.json publication gate IDs must be nonempty and unique")
        if any(item.get("status") not in {"resolved", "open"} for item in blockers):
            errors.append("/index.json contains an unknown publication gate status")
        expected_publication_status = "blocked" if any(item.get("status") != "resolved" for item in blockers) else "ready"
        if index.get("publication_status") != expected_publication_status or index.get("publication_status") != DATA["meta"].get("publication_status"):
            errors.append("/index.json publication status does not follow its evidence gate states")
        join = DATA.get("meta", {}).get("publication_join", {})
        if (join.get("total"), join.get("public_export"), join.get("capture_reported_export_absent")) != (5020, 5020, 0):
            errors.append("Publication join metadata must report 5,020 exact public matches and no capture-reported-only mappings")
        grade_gate = next((item for item in blockers if item.get("evidence_key") == "official_grade_export_join"), {})
        if grade_gate.get("status") != "resolved" or grade_gate.get("evidence_path") != "results/GRADE-JOIN.md":
            errors.append("Official-grade evidence gate must disclose its resolved exact join and link GRADE-JOIN.md")
        if index.get("publication_validation_url") != "/publication-validation/":
            errors.append("/index.json does not link the publication validation report")
        inventory = DATA.get("reproduction_inventory", [])
        inventory_ids = [item.get("round_id") for item in inventory]
        if len(inventory_ids) != len(set(inventory_ids)) or set(inventory_ids) != set(DATA["meta"]["round_index_ids"]):
            errors.append("Per-round reproduction inventory does not match rounds/index.json exactly")
        replay_ids = sorted(item.get("round_id") for item in inventory if item.get("full_execution_replayable"))
        if replay_ids != DATA.get("round_inventory_full_replay_ids") or replay_ids != index.get("full_execution_replayable_rounds"):
            errors.append("Per-round full-execution replay summary is inconsistent")

    snapshot_path = DIST / "snapshot.json"
    if snapshot_path.is_file():
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        gates = snapshot.get("publication_gates") or []
        index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.is_file() else {}
        expected_gates = index.get("publication_blockers", [])
        if gates != expected_gates:
            errors.append("/snapshot.json publication gates differ from /index.json")
        revision = snapshot.get("data_revision")
        try:
            head_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        except subprocess.CalledProcessError:
            head_revision = ""
        if revision != head_revision:
            errors.append("/snapshot.json was not built from the current HEAD revision")
        for source in snapshot.get("source_files", []):
            source_path = source.get("path")
            if not isinstance(source_path, str):
                errors.append("/snapshot.json has a source row without a path")
                continue
            try:
                committed = subprocess.check_output(["git", "show", f"HEAD:{source_path}"], cwd=ROOT)
            except subprocess.CalledProcessError:
                errors.append(f"/snapshot.json source is absent from HEAD: {source_path}")
                continue
            digest = hashlib.sha256(committed).hexdigest()
            if digest != source.get("sha256"):
                errors.append(f"/snapshot.json source hash is stale for HEAD:{source_path}")
            if source.get("url", "").find(f"/{revision}/") < 0:
                errors.append(f"/snapshot.json source URL does not pin the built revision: {source_path}")
        source_paths = {item.get("path") for item in snapshot.get("source_files", [])}
        if "results/publication-validation.md" not in source_paths:
            errors.append("/snapshot.json does not hash results/publication-validation.md")

    llms_path = DIST / "llms.txt"
    if llms_path.is_file():
        llms = llms_path.read_text(encoding="utf-8")
        for required in ("5,020 of 5,020", "84 model pass", "19 model fail", "25 invalid control_apply", "not model failures", "grade-join.md", "/publication-validation/"):
            if required not in llms.lower():
                errors.append(f"/llms.txt does not disclose/link publication gate detail: {required}")
        for gate in PUBLICATION_BLOCKERS:
            if f"{gate.get('id')} ({gate.get('status')})" not in llms or gate.get("summary", "") not in llms:
                errors.append(f"/llms.txt omits current publication evidence gate: {gate.get('id')}")
    full_guide_path = DIST / "llms-full.txt"
    if full_guide_path.is_file():
        full_guide = full_guide_path.read_text(encoding="utf-8")
        for required in ("5,020 of 5,020", "84 model PASS", "19 model FAIL", "25 invalid control_apply", "not model failures", "GRADE-JOIN.md", "source-reported"):
            if required.lower() not in full_guide.lower():
                errors.append(f"/llms-full.txt does not disclose publication gate detail: {required}")
        for gate in PUBLICATION_BLOCKERS:
            if f"{gate.get('id')} ({gate.get('status')})" not in full_guide or gate.get("summary", "") not in full_guide:
                errors.append(f"/llms-full.txt omits current publication evidence gate: {gate.get('id')}")

    validation_page = DIST / "publication-validation" / "index.html"
    if not validation_page.is_file():
        errors.append("Missing /publication-validation/ HTML page")
    else:
        content = validation_page.read_text(encoding="utf-8")
        spec_gate = next((item for item in PUBLICATION_BLOCKERS if item.get("evidence_key") == "spec_decision_sources"), {})
        for required in ("5,020/5,020", "84 model PASS", "19 model FAIL", "25 invalid", "not model failures", "results/GRADE-JOIN.md", f"All {spec_gate.get('count')} linked v1.2 fragments", "B2 is resolved", "results/publication-validation.md"):
            if required not in content:
                errors.append(f"/publication-validation/ does not render validation source detail: {required}")

    evidence_page = DIST / "evidence" / "index.html"
    if not evidence_page.is_file():
        errors.append("Missing /evidence/ HTML page")
    else:
        content = evidence_page.read_text(encoding="utf-8")
        for required in ("locally verified", "decision ledger", "comprehensive decision-to-clause coverage remains limited"):
            if required not in content:
                errors.append(f"/evidence/ dropped an EVIDENCE-MAP caveat paragraph: {required}")

    spec_fragment_links = {
        target
        for target in re.findall(r"\]\((spec/[^)\s]+\.md#[^)]+)\)", (ROOT / "EVIDENCE-MAP.md").read_text(encoding="utf-8"))
    }
    expected_fragment_count = next(
        (item.get("count") for item in PUBLICATION_BLOCKERS if item.get("evidence_key") == "spec_decision_sources"),
        None,
    )
    if len(spec_fragment_links) != expected_fragment_count:
        errors.append(f"EVIDENCE-MAP source-link inventory differs from the declared {expected_fragment_count} pinned v1.2 fragments")
    else:
        revision = DATA.get("meta", {}).get("revision", "")
        expected_urls = {
            f"https://github.com/KogenAI/kogen-bench/blob/{revision}/{target}"
            for target in spec_fragment_links
        }
        rendered_urls: set[str] = set()
        for clause in DATA.get("evidence", []):
            page = DIST / "evidence" / clause.get("id", "") / "index.html"
            if not page.is_file():
                continue
            parser = PageParser()
            parser.feed(page.read_text(encoding="utf-8"))
            rendered_urls.update(
                href for href, _rel, _tag in parser.links
                if href.startswith(f"https://github.com/KogenAI/kogen-bench/blob/{revision}/spec/")
            )
        if rendered_urls != expected_urls:
            errors.append(
                "Rendered evidence pages do not link every pinned v1.2 fragment to its source: "
                f"missing={len(expected_urls - rendered_urls)}, extra={len(rendered_urls - expected_urls)}"
            )

    intent_clause = next(
        (item for item in DATA.get("evidence", []) if item.get("id") == "21-intent-kogenintentsintentmd"),
        None,
    )
    intent_page = DIST / "evidence" / "21-intent-kogenintentsintentmd" / "index.html"
    if intent_clause is None or not intent_page.is_file():
        errors.append("Missing rendered Intent clause page for title check")
    else:
        intent_html = intent_page.read_text(encoding="utf-8")
        h1_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", intent_html, re.DOTALL)
        rendered_h1 = html.unescape(re.sub(r"<[^>]+>", "", h1_match.group(1))) if h1_match else ""
        if "`" in intent_clause.get("title", "") or "`" in rendered_h1 or ".kogen/intents/<slug>/intent.md" not in rendered_h1:
            errors.append("Rendered Intent clause title must show its path without Markdown backticks")

    for round_id in ("l0-reconcile", "l3-repair", "l6-auditor-replay", "r70-rve-task8v2"):
        round_page = DIST / "rounds" / round_id / "index.html"
        if not round_page.is_file():
            errors.append(f"Missing structured round HTML page: /rounds/{round_id}/")
            continue
        content = round_page.read_text(encoding="utf-8")
        for required in ("Reproduction inventory", "Full execution replay", "Repository reproduction guide"):
            if required not in content:
                errors.append(f"/rounds/{round_id}/ is missing reproduction detail: {required}")
        if "This is a status-only page" in content:
            errors.append(f"/rounds/{round_id}/ still renders a status-only shell")

    for page_file in page_files:
        try:
            content = page_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PRIVATE_PATH.search(content):
            errors.append(f"private filesystem path in generated HTML: {page_file.relative_to(DIST)}")
        parser = PageParser()
        parser.feed(content)
        if page_file.name != "404.html":
            if not parser.has_markdown_alternate:
                errors.append(f"missing .md alternate: {page_file.relative_to(DIST)}")
            if not parser.has_github_source:
                errors.append(f"missing GitHub source link: {page_file.relative_to(DIST)}")
            if not parser.has_policy:
                errors.append(f"missing numeric provenance policy: {page_file.relative_to(DIST)}")
        for text, origin in parser.text_chunks:
            if page_file.name == "404.html":
                continue
            if NUMBER.search(text) and not is_numeric_id_chunk(text):
                if not any(label in origin for label in ("source-reported", "claim-ledger", "source-register", "round-crosswalk", "snapshot")):
                    errors.append(f"unlabelled number in {page_file.relative_to(DIST)}: {text.strip()[:96]}")
                    break
        for href, _rel, _tag in parser.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                if href.startswith(("javascript:", "data:")):
                    errors.append(f"unsafe URL in {page_file.relative_to(DIST)}")
                continue
            target, fragment = output_path_for_href(href, page_file)
            if target is None:
                continue
            if not target.is_file():
                errors.append(f"internal link has no target: {page_file.relative_to(DIST)} -> {href}")
                continue
            if fragment and target.suffix in {".html", ".htm"}:
                target_parser = PageParser()
                target_parser.feed(target.read_text(encoding="utf-8"))
                if unquote(fragment) not in target_parser.ids:
                    errors.append(f"internal anchor has no target: {page_file.relative_to(DIST)} -> {href}")

        for css_url in re.findall(r"url\((?:['\"]?)([^)'\"]+)(?:['\"]?)\)", content):
            if css_url.startswith(("data:", "https://", "http://")):
                continue
            target, _fragment = output_path_for_href(css_url, page_file)
            if target is not None and not target.is_file():
                errors.append(f"internal asset has no target: {page_file.relative_to(DIST)} -> {css_url}")

    markdown_link = re.compile(r"(?<!!)\]\(([^)]+)\)")
    for markdown_file in DIST.rglob("*.md"):
        try:
            content = markdown_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PRIVATE_PATH.search(content):
            errors.append(f"private filesystem path in generated Markdown: {markdown_file.relative_to(DIST)}")
        for raw_href in markdown_link.findall(content):
            href = raw_href.strip().split()[0].strip("<>")
            if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                if href.startswith(("javascript:", "data:")):
                    errors.append(f"unsafe URL in {markdown_file.relative_to(DIST)}")
                continue
            target, fragment = output_path_for_href(href, markdown_file)
            if target is None:
                continue
            if not target.is_file():
                errors.append(f"Markdown link has no target: {markdown_file.relative_to(DIST)} -> {href}")
            elif fragment and target.suffix in {".html", ".htm"}:
                target_parser = PageParser()
                target_parser.feed(target.read_text(encoding="utf-8"))
                if unquote(fragment) not in target_parser.ids:
                    errors.append(f"Markdown anchor has no target: {markdown_file.relative_to(DIST)} -> {href}")

    text_suffixes = {".html", ".json", ".txt", ".md", ".xml", ".jsonl", ".css", ".js", ".svg"}
    for path in DIST.rglob("*"):
        if not path.is_file() or path.suffix not in text_suffixes:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PRIVATE_PATH.search(content):
            errors.append(f"private filesystem path in generated output: {path.relative_to(DIST)}")

    expected_markdown = len(DATA["pages"])
    actual_markdown = len(list(DIST.rglob("*.md")))
    if actual_markdown != expected_markdown:
        errors.append(f"Markdown alternate mismatch: expected {expected_markdown}, found {actual_markdown}")

    intent_width_result = check_intent_phone_width(errors)
    print(f"Static HTML content pages: {page_count}")
    print(f"Generated Markdown pages and source guides: {actual_markdown}")
    print(f"Intent clause phone-width assertion: {intent_width_result}")
    print("Build checks: no private paths, internal links, source links, Markdown alternates, and numeric provenance labels inspected.")
    if errors:
        print(f"Build-check failures: {len(errors)}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Build checks passed.")


if __name__ == "__main__":
    main()
