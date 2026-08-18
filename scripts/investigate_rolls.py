#!/usr/bin/env python3
"""Enumerate polling-station PDFs, extract them, and search voter names."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse


EPIC_RE = re.compile(r"\b[A-Z]{2,4}\d{6,10}\b", re.I)
AC_PART_RE = re.compile(r"^[^_]+_(\d+)_(\d+)_")


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def edit_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        next_row = [i]
        for j, cb in enumerate(b, 1):
            next_row.append(min(next_row[-1] + 1, row[j] + 1, row[j - 1] + (ca != cb)))
        row = next_row
    return row[-1]


def token_similar(query: str, candidate: str) -> bool:
    if query == candidate:
        return True
    allowance = 1 if len(query) <= 5 else 2 if len(query) <= 9 else 3
    return abs(len(query) - len(candidate)) <= allowance and edit_distance(query, candidate) <= allowance


def gdown_base() -> list[str]:
    if shutil.which("uvx"):
        # Folder metadata mode was introduced in gdown 6.1.0. Pin the minimum
        # version so uvx cannot resolve an older CLI without --json support.
        return ["uvx", "--from", "gdown>=6.1.0", "gdown"]
    if shutil.which("gdown"):
        help_result = subprocess.run(["gdown", "--help"], capture_output=True, text=True)
        if help_result.returncode == 0 and "--json" in help_result.stdout:
            return ["gdown"]
        raise SystemExit("Installed gdown does not support --json; install gdown>=6.1.0.")
    raise SystemExit("Need uvx or gdown>=6.1.0 in PATH to enumerate Google Drive folders.")


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def list_folder(url: str) -> list[dict[str, str]]:
    result = run(gdown_base() + ["--folder", "--json", url], capture=True)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Could not parse gdown folder metadata: {exc}\n{result.stderr}") from exc
    if not isinstance(data, list):
        raise SystemExit("Unexpected gdown metadata format; expected a JSON list.")
    return data


def drive_id(url: str) -> str:
    parsed = urlparse(url)
    query_id = parse_qs(parsed.query).get("id", [""])[0]
    if query_id:
        return query_id
    match = re.search(r"/d/([^/]+)", parsed.path)
    if match:
        return match.group(1)
    raise ValueError(f"No Google Drive file ID in {url}")


def station_matches(path: str, station: str) -> bool:
    wanted = normalized(station).split()
    haystack = normalized(path)
    return bool(wanted) and all(token in haystack for token in wanted)


def parse_ac_part(path: str) -> tuple[int | None, int | None]:
    match = AC_PART_RE.search(Path(path).name)
    return (int(match.group(1)), int(match.group(2))) if match else (None, None)


@dataclass(frozen=True)
class Candidate:
    query: str
    strength: str
    pdf: str
    page: int
    line: int
    text: str


def row_name(text: str) -> str:
    match = EPIC_RE.search(text)
    if not match:
        return text
    tail = text[match.end():].strip()
    return re.split(r"\s{2,}", tail, maxsplit=1)[0]


def classify(query: str, text: str) -> str | None:
    query_tokens = normalized(query).split()
    if not query_tokens:
        return None
    person_tokens = normalized(row_name(text)).split()
    line_tokens = normalized(text).split()
    if all(token in person_tokens for token in query_tokens):
        return "exact"
    # Electoral rolls often put an initial after the family name (for example,
    # "VICTORIA BRUNDA A"). Never use a one- or two-character initial as the
    # fuzzy surname anchor; it would match nearly every row in the corpus.
    surname_index = next(
        (index for index in range(len(query_tokens) - 1, -1, -1) if len(query_tokens[index]) >= 3),
        len(query_tokens) - 1,
    )
    surname = query_tokens[surname_index]
    surname_hit = any(token_similar(surname, token) for token in person_tokens)
    given = [token for index, token in enumerate(query_tokens) if index != surname_index and len(token) >= 3]
    given_hit = any(token_similar(q, token) for q in given for token in person_tokens)
    if surname_hit and (given_hit or len(query_tokens) == 1):
        return "likely"
    # Keep surname-only results exact. Fuzzy surname matching without a given
    # name produces too many unrelated candidates for common Indian names.
    if surname in line_tokens:
        return "surname-only"
    return None


def search_text(query: str, text_path: Path) -> list[Candidate]:
    results: list[Candidate] = []
    page = 1
    for line_no, raw in enumerate(text_path.read_text(errors="replace").splitlines(keepends=True), 1):
        # Only emit complete electoral rows. Wrapped continuation lines can
        # contain a surname alone and otherwise look like a candidate.
        if EPIC_RE.search(raw):
            strength = classify(query, raw)
            if strength:
                results.append(Candidate(query, strength, text_path.with_suffix(".pdf").name, page, line_no, raw.strip()))
        page += raw.count("\f")
    return results


def unique_candidates(candidates: list[Candidate]) -> list[Candidate]:
    seen: set[tuple[str, str, int, str]] = set()
    result: list[Candidate] = []
    for candidate in candidates:
        key = (candidate.query, candidate.pdf, candidate.line, candidate.strength)
        if key not in seen:
            seen.add(key)
            result.append(candidate)
    return result


def extract_pdf(pdf: Path, text: Path) -> None:
    if not shutil.which("pdftotext"):
        raise SystemExit("pdftotext is required (install Poppler) to extract the PDFs.")
    run(["pdftotext", "-layout", str(pdf), str(text)])


def write_report(
    path: Path,
    source_type: str,
    matched: list[dict[str, object]],
    candidates: list[Candidate],
    queries: list[str],
) -> None:
    lines = ["# Karnataka voter-record search", "", f"Source type: **{source_type}**", ""]
    lines += ["## Parts and rooms searched", ""]
    for item in matched:
        ac = item.get("ac") if item.get("ac") is not None else "?"
        part = item.get("part") if item.get("part") is not None else "?"
        lines.append(f"- AC {ac}, Part {part}: `{item['path']}`")
    lines += ["", "## Name results", ""]
    for query in queries:
        hits = [candidate for candidate in candidates if candidate.query == query]
        lines.append(f"### {query}")
        lines.append("")
        if not hits:
            lines.append("No exact or fuzzy candidate in the files searched.")
        else:
            for hit in hits:
                lines.append(f"- **{hit.strength}**, `{hit.pdf}` page {hit.page}: {hit.text}")
        lines.append("")
    lines += ["## Interpretation", ""]
    if source_type.casefold() in {"asddo", "asd", "flagged"}:
        lines.append("This is a flagged subset, not the complete electoral roll. A missing name is only absent from the files searched.")
    else:
        lines.append("A missing name means no match was found in this downloaded corpus; verify supplements, extraction quality, and adjacent plausible parts.")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--folder-url", help="Public Google Drive folder containing PDFs")
    source.add_argument("--pdf-dir", type=Path, help="Directory containing already-downloaded PDFs")
    parser.add_argument("--station", help="Polling-station name; all normalized tokens must match the filename")
    parser.add_argument("--name", action="append", required=True, dest="names", help="Name to search; repeat as needed")
    parser.add_argument("--source-type", default="ASDDO", help="ASDDO, full roll, historical, or another precise label")
    parser.add_argument("--output", type=Path, required=True, help="Directory for PDFs, text, manifest, and report")
    parser.add_argument("--metadata-only", action="store_true", help="Enumerate and filter without downloading/searching")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    matched: list[dict[str, object]] = []

    if args.folder_url:
        if not args.station:
            parser.error("--station is required with --folder-url")
        all_items = list_folder(args.folder_url)
        for item in all_items:
            remote_path = item.get("path", "")
            if station_matches(remote_path, args.station):
                ac, part = parse_ac_part(remote_path)
                matched.append({"url": item.get("url", ""), "path": remote_path, "ac": ac, "part": part})
        matched.sort(key=lambda item: (item.get("part") is None, item.get("part") or 0, str(item.get("path"))))
        if not matched:
            raise SystemExit(f"No complete-folder filename match for station: {args.station}")
        pdf_dir = args.output / "pdfs"
        pdf_dir.mkdir(exist_ok=True)
        if not args.metadata_only:
            for item in matched:
                destination = pdf_dir / Path(str(item["path"])).name
                if not destination.exists() or destination.stat().st_size == 0:
                    run(gdown_base() + [drive_id(str(item["url"])), "-O", str(destination)])
    else:
        pdf_dir = args.pdf_dir
        assert pdf_dir is not None
        pdf_paths = sorted(pdf_dir.glob("*.pdf"))
        if not pdf_paths:
            raise SystemExit(f"No PDFs found in {pdf_dir}")
        for pdf in pdf_paths:
            ac, part = parse_ac_part(pdf.name)
            matched.append({"url": "", "path": pdf.name, "ac": ac, "part": part})

    manifest = {
        "source_type": args.source_type,
        "folder_url": args.folder_url,
        "station": args.station,
        "names": args.names,
        "matched_count": len(matched),
        "matched": matched,
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Matched {len(matched)} PDF(s). Manifest: {args.output / 'manifest.json'}")
    if args.metadata_only:
        return 0

    text_dir = args.output / "text"
    text_dir.mkdir(exist_ok=True)
    candidates: list[Candidate] = []
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        text_path = text_dir / f"{pdf.stem}.txt"
        extract_pdf(pdf, text_path)
        for query in args.names:
            candidates.extend(search_text(query, text_path))
    candidates = unique_candidates(candidates)
    query_order = {query: index for index, query in enumerate(args.names)}
    strength_order = {"exact": 0, "likely": 1, "surname-only": 2}
    candidates.sort(
        key=lambda candidate: (
            query_order[candidate.query],
            strength_order[candidate.strength],
            candidate.pdf,
            candidate.page,
            candidate.line,
        )
    )
    (args.output / "candidates.json").write_text(
        json.dumps([asdict(candidate) for candidate in candidates], indent=2, ensure_ascii=False) + "\n"
    )
    report_path = args.output / "report.md"
    write_report(report_path, args.source_type, matched, candidates, args.names)
    print(f"Candidates: {len(candidates)}. Report: {report_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed ({exc.returncode}): {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
