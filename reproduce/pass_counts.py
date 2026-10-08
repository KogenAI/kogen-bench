"""Validate pass counts in round-page Markdown tables against cells.jsonl."""
import json
import re
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path


FRACTION_RE = re.compile(r"(?<![A-Za-z0-9_])(\d+)\s*/\s*(\d+)(?!\d)")
REPEAT_SUFFIX_RE = re.compile(r"(?:[-_](?:r|rep)\d+)$", re.IGNORECASE)


def markdown_tables(text):
    """Yield (header, rows, start_line) for Markdown pipe tables outside fences."""
    lines = text.splitlines()
    in_fence = False
    i = 0
    while i < len(lines):
        if re.match(r"^\s*(```|~~~)", lines[i]):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence or "|" not in lines[i]:
            i += 1
            continue
        start = i
        block = []
        while i < len(lines) and "|" in lines[i]:
            block.append(lines[i])
            i += 1
        if len(block) < 2:
            continue
        header = [value.strip() for value in block[0].strip().strip("|").split("|")]
        separator = [value.strip() for value in block[1].strip().strip("|").split("|")]
        if len(header) != len(separator) or not all(re.fullmatch(r":?-{3,}:?", value) for value in separator):
            continue
        rows = []
        for offset, line in enumerate(block[2:], start=2):
            values = [value.strip() for value in line.strip().strip("|").split("|")]
            if len(values) == len(header):
                rows.append((dict(zip(header, values)), start + offset + 1))
        yield header, rows, start + 1


def _is_pass_table(header, rows):
    normalized = [value.strip().lower() for value in header]
    has_pass_header = any(re.search(r"\bpass(?:es)?\b", value) for value in normalized)
    if has_pass_header:
        return True
    ratio_headers = ("result", "score", "hidden-suite", "passes")
    for row, _ in rows:
        for key, value in row.items():
            if any(term in key.lower() for term in ratio_headers) and FRACTION_RE.search(value):
                return True
    # Tables with model/stack/builder rows and arms as columns are pass tables
    # even when their cells only contain x/y values.
    has_group_row = any(re.search(r"\b(model|stack|builder)\b", value) for value in normalized)
    return has_group_row and any(FRACTION_RE.search(value) for row, _ in rows for value in row.values())


def _arm_candidates(round_rows, task, displayed_arm):
    if not displayed_arm or displayed_arm.lower() in {"not recorded", "arm label not retained", "—", "-"}:
        return set()
    candidates = {
        row.get("arm") for row in round_rows
        if row.get("task") == task and isinstance(row.get("arm"), str)
    }
    exact = {arm for arm in candidates if arm.lower() == displayed_arm.lower()}
    if exact:
        return exact

    tail = displayed_arm.rsplit(":", 1)[-1]
    matches = set()
    for arm in candidates:
        arm_tail = arm.rsplit(":", 1)[-1]
        stem = REPEAT_SUFFIX_RE.sub("", arm_tail)
        arm_tail_lower = arm_tail.lower()
        stem_lower = stem.lower()
        tail_lower = tail.lower()
        if arm_tail_lower == tail_lower or stem_lower == tail_lower:
            matches.add(arm)
            continue
        # Some public capture labels omit a round prefix or repeat suffix.
        # Require a delimiter before the omitted portion so e.g. `w2` does
        # not also match the distinct compound arm `w1+w2`.
        if stem_lower.endswith(tail_lower):
            preceding = stem_lower[:-len(tail_lower)]
            if not preceding or preceding.endswith(("-", ":", "_")):
                matches.add(arm)
    if not matches:
        return set()
    # A shorthand is only safe when all matches are repetitions of the same
    # exact arm stem. Distinct model/cohort arms must be printed separately.
    stems = {REPEAT_SUFFIX_RE.sub("", arm.rsplit(":", 1)[-1]) for arm in matches}
    if len(stems) > 1:
        return {"__ambiguous__"}
    return matches


def _pass_values(header, row):
    found = []
    for key, value in row.items():
        key_lower = key.lower()
        if re.search(r"\bpass(?:es)?\b", key_lower):
            if re.fullmatch(r"\d+", value):
                found.append((key, int(value)))
            else:
                matches = FRACTION_RE.findall(value)
                if len(matches) == 1:
                    found.append((key, int(matches[0][0])))
                elif len(matches) > 1:
                    found.append((key, None))
                elif value.strip().lower() not in {"", "—", "-", "n/a"}:
                    found.append((key, None))
        elif any(term in key_lower for term in ("result", "score", "hidden-suite")):
            matches = FRACTION_RE.findall(value)
            if len(matches) == 1:
                found.append((key, int(matches[0][0])))
            elif len(matches) > 1:
                found.append((key, None))
    return found


def validate_round_page(page, round_id, cell_rows):
    """Return diagnostics and checked group count for one round page."""
    errors = []
    checked = 0
    round_rows = [row for row in cell_rows if row.get("round") == round_id]
    text = page.read_text()
    # Round 70's generated measurement tables use heterogeneous metrics
    # (hidden-test fractions, timing, tokens, and costs). Their dedicated
    # sibling audit recomputes every cell from public ledgers and runs its own
    # mutation self-test, so the generic outcome-pass table parser must leave
    # those marked blocks to that validator.
    generated_ranges = []
    for match in re.finditer(r"<!-- (R70-[A-Z0-9-]+):BEGIN -->(.*?)<!-- \1:END -->", text, re.DOTALL):
        start_line = text.count("\n", 0, match.start()) + 1
        end_line = text.count("\n", 0, match.end()) + 1
        generated_ranges.append((start_line, end_line))
    for header, table_rows, start_line in markdown_tables(text):
        if any(start <= start_line <= end for start, end in generated_ranges):
            continue
        if not _is_pass_table(header, table_rows):
            continue
        normalized = {value.strip().lower(): value for value in header}
        task_header = next((value for key, value in normalized.items() if key in {"task id", "task", "task / stack", "task / model"}), None)
        arm_header = next((value for key, value in normalized.items() if "arm" in key), None)
        model_header = next((value for key, value in normalized.items() if key in {"model", "model / effort", "builder"}), None)
        stack_header = next((value for key, value in normalized.items() if key == "stack"), None)

        # Matrix tables need a row/column allocation convention. Require an
        # explicit task and arm key so their counts cannot be silently skipped.
        if not task_header or not arm_header:
            errors.append(
                f"{page.relative_to(page.parents[1])}:{start_line}: pass-count table must use task and exact-arm columns"
            )
            continue

        totals = defaultdict(int)
        labels = {}
        line_numbers = defaultdict(list)
        invalid_values = []
        for row, line_number in table_rows:
            task = row.get(task_header, "").strip()
            arm = row.get(arm_header, "").strip()
            for column, count in _pass_values(header, row):
                if count is None:
                    invalid_values.append(line_number)
                    continue
                key = (task, arm, column)
                totals[key] += count
                labels[key] = row
                line_numbers[key].append(line_number)
        for line_number in invalid_values:
            errors.append(f"{page.relative_to(page.parents[1])}:{line_number}: unparseable pass count")

        for (task, arm, column), actual in totals.items():
            if task.lower() in {"", "not recorded", "task identity not retained", "—", "-"}:
                expected = 0
            else:
                arm_set = _arm_candidates(round_rows, task, arm)
                if "__ambiguous__" in arm_set:
                    errors.append(
                        f"{page.relative_to(page.parents[1])}:{line_numbers[(task, arm, column)][0]}: arm label {arm!r} maps to multiple exported arms; print the full arm label"
                    )
                    continue
                selected = [row for row in round_rows if row.get("task") == task]
                if arm_set:
                    selected = [row for row in selected if row.get("arm") in arm_set]
                elif actual or any(row.get("task") == task for row in round_rows):
                    errors.append(
                        f"{page.relative_to(page.parents[1])}:{line_numbers[(task, arm, column)][0]}: task/arm key {task!r} / {arm!r} cannot be matched to official rows in cells.jsonl"
                    )
                    continue
                else:
                    selected = []
                if model_header:
                    model = labels[(task, arm, column)].get(model_header, "").strip()
                    if model and model.lower() not in {"unknown", "not recorded", "—", "-"}:
                        selected = [row for row in selected if str(row.get("model", "")) == model]
                if stack_header:
                    stack = labels[(task, arm, column)].get(stack_header, "").strip()
                    if stack and stack.lower() not in {"unknown", "not recorded", "—", "-"}:
                        errors.append(
                            f"{page.relative_to(page.parents[1])}:{line_numbers[(task, arm, column)][0]}: stack-only pass tables must be expanded to task and exact-arm rows"
                        )
                        continue
                expected = sum(row.get("ITT outcome") == "pass" for row in selected)
            checked += 1
            if actual != expected:
                lines = ",".join(str(line) for line in line_numbers[(task, arm, column)])
                errors.append(
                    f"{page.relative_to(page.parents[1])}:{lines}: table pass count {actual} for {task!r} / {arm!r} != cells.jsonl count {expected}"
                )
    return errors, checked


def validate_all_round_pages(root, cell_rows):
    errors = []
    checked = 0
    round_ids = json.loads((root / "rounds" / "index.json").read_text(encoding="utf-8"))
    for round_id in round_ids:
        folder = root / "rounds" / round_id
        for page in (folder / "README.md", folder / "RESULTS.md"):
            if not page.is_file():
                continue
            page_errors, page_checked = validate_round_page(page, round_id, cell_rows)
            errors.extend(page_errors)
            checked += page_checked
    return errors, checked


def collect_planned_task_pairs(root, task_ids):
    """Collect exact task IDs listed by public round plans or planned-n tables."""
    known = set(task_ids)
    pairs = set()
    round_ids = json.loads((root / "rounds" / "index.json").read_text(encoding="utf-8"))
    for round_id in round_ids:
        page = root / "rounds" / round_id / "README.md"
        if not page.is_file():
            continue
        text = page.read_text()
        for line in text.splitlines():
            if re.search(r"\bplanned tasks?\b|\bplan lists\b|\bsurviving plan lists\b", line, re.IGNORECASE):
                pairs.update((task_id, round_id) for task_id in known if task_id in line)
        for header, table_rows, _ in markdown_tables(text):
            names = {value.strip().lower(): value for value in header}
            task_header = next((value for key, value in names.items() if key in {"task id", "task"}), None)
            planned_header = next((value for key, value in names.items() if "planned n" in key), None)
            if task_header and planned_header:
                for row, _ in table_rows:
                    task_id = row.get(task_header, "").strip()
                    if task_id in known:
                        pairs.add((task_id, round_id))

    for round_id in round_ids:
        plan = root / "rounds" / round_id / "PLAN.json"
        if not plan.is_file():
            continue
        try:
            content = json.loads(plan.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        stack = [content]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
            elif isinstance(value, str) and value in known:
                pairs.add((value, round_id))
    return pairs


def self_test(root):
    """Check that a copied table passes, then fails when its pass count is changed."""
    round_id = "r-pass-count-self-test"
    good_text = (
        "| Task ID | Exact arm label in export | Pass |\n"
        "| --- | --- | ---: |\n"
        "| task-a | arm-a | 1 |\n"
    )
    cells = [{"round": round_id, "task": "task-a", "arm": "arm-a", "ITT outcome": "pass"}]
    with tempfile.TemporaryDirectory(prefix="pass-count-self-test-", dir=root / "reproduce") as temporary:
        page_dir = Path(temporary) / "rounds" / round_id
        page_dir.mkdir(parents=True)
        good_page = page_dir / "README.md"
        good_page.write_text(good_text)
        good_errors, _ = validate_round_page(good_page, round_id, cells)
        if good_errors:
            raise RuntimeError("Pass-count self-test fixture unexpectedly failed: " + "; ".join(good_errors))

        wrong_page = page_dir / "README-wrong.md"
        shutil.copyfile(good_page, wrong_page)
        wrong_page.write_text(wrong_page.read_text().replace("| task-a | arm-a | 1 |", "| task-a | arm-a | 2 |"))
        wrong_errors, _ = validate_round_page(wrong_page, round_id, cells)
        if not any("table pass count 2" in error and "cells.jsonl count 1" in error for error in wrong_errors):
            raise RuntimeError("Pass-count self-test did not reject the deliberately wrong temporary copy")
