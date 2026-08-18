# Karnataka Voter Roll Search

A shell-first Codex skill for investigating Karnataka electoral rolls, SIR material, ASDDO/ASD lists, historical voter records, polling-station parts, and spelling variations in voter names.

It is designed for messy real-world election data: long Google Drive folders, non-contiguous part numbers, multiple rooms in the same polling-station building, manually entered names, inconsistent transliteration, and pre-delimitation constituencies.

## Why this exists

Google Drive displays large folders incrementally. A polling station that appears to have one room in the browser may have additional rooms much later in the folder. Drawing conclusions from the visible rows can therefore miss relevant parts entirely.

This skill defaults to a reproducible workflow:

1. Enumerate the complete folder from the shell.
2. Find every filename matching the polling station.
3. Download only those PDFs.
4. Extract and search all matched parts together.
5. Report exact, fuzzy, and surname-only candidates separately.
6. Preserve the distinction between a full electoral roll and an ASDDO/ASD flagged subset.

## Install as a Codex skill

Clone the repository into your personal skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/ssonal/karnataka-voter-roll-search.git \
  ~/.codex/skills/karnataka-voter-roll-search
```

Restart Codex if the skill does not appear immediately. Invoke it explicitly with `$karnataka-voter-roll-search`, or ask naturally about Karnataka voter-list, SIR, ASDDO, constituency, part, room, or historical-roll research.

Example prompt:

```text
Use $karnataka-voter-roll-search to enumerate every room for Example Public
School in this CEO Karnataka Drive folder and check Anita Sample and Joseph
Sample across all matching ASDDO PDFs.
```

## Bundled command-line investigator

The skill includes a standalone utility for public Google Drive folders containing text-readable PDFs:

```bash
python3 scripts/investigate_rolls.py \
  --folder-url 'GOOGLE_DRIVE_FOLDER_URL' \
  --station 'Example Public School' \
  --name 'Anita Sample' \
  --name 'Joseph Sample' \
  --source-type ASDDO \
  --output './roll-search'
```

For PDFs already downloaded locally:

```bash
python3 scripts/investigate_rolls.py \
  --pdf-dir './downloaded-parts' \
  --name 'Mary Sample' \
  --source-type 'full roll' \
  --output './roll-search'
```

The output directory contains:

- `manifest.json` — every matched file, AC, and part
- `pdfs/` — relevant downloaded PDFs when using Drive
- `text/` — layout-preserving extracted text
- `candidates.json` — machine-readable search candidates
- `report.md` — human-readable findings and caveats

## Requirements

- Python 3.10+
- [`gdown`](https://github.com/wkentaro/gdown) or `uvx` for public Google Drive folders
- Poppler's `pdftotext` for PDF extraction

The skill checks for these commands and reports a clear error if one is unavailable.

## Important limitations

- An ASDDO/ASD file is not the complete electoral roll. A missing name means only that no match was found in the flagged files searched.
- Failed or sparse PDF extraction is not evidence of absence. Image-only PDFs require OCR and visual verification.
- A current Assembly Constituency number should not be projected backward to 2002/2004 without historical boundary evidence.
- Fuzzy matches are leads, not proof of identity. Verify age, relatives, address, EPIC number, part, and source page.
- Google Drive or election-site authentication and CAPTCHA challenges may still require user interaction.

## Privacy

The workflow searches PDFs locally and downloads only relevant polling-station files. Do not commit voter PDFs, extracted voter records, search reports, or personal details to this repository. Share only the minimum rows necessary for the person requesting the search.

## Repository structure

```text
SKILL.md                                Codex workflow and guardrails
agents/openai.yaml                      Codex UI metadata
scripts/investigate_rolls.py            Deterministic folder/PDF/name-search CLI
tests/test_name_matching.py             Name-matching regression tests
references/karnataka-electoral-sources.md  Source and interpretation notes
LICENSE                                 MIT license
```

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

## License

[MIT](LICENSE)
