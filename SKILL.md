---
name: karnataka-voter-roll-search
description: Investigate Karnataka electoral-roll, SIR, ASDDO/ASD, and historical voter-list records using official CEO Karnataka pages, Google Drive folders, and PDF rolls. Use when Codex must map an address to district/Assembly Constituency/part/room, enumerate every polling-station PDF, search people despite spelling or data-entry variations, distinguish current from 2002/2004 constituencies, or verify whether a person appears in a full roll versus a flagged ASDDO list.
---

# Karnataka Voter Roll Search

Use a shell-first, evidence-preserving workflow. Treat browser folder listings as discovery aids only: Google Drive virtualizes long folders and can hide later, non-contiguous parts.

## Default workflow

1. Record the known facts without blocking on optional details:
   - full and familiar names, birth year or approximate age, relatives
   - address at the relevant date
   - election year or roll type
   - known current AC, part, polling station, or Drive folder
2. Classify the source before searching:
   - full electoral roll
   - ASDDO/ASD or other flagged subset
   - historical roll, especially pre-delimitation 2002/2004 material
3. Prefer official CEO Karnataka entry points and their linked files. Read [references/karnataka-electoral-sources.md](references/karnataka-electoral-sources.md) when choosing sources or interpreting results.
4. Enumerate the complete Drive folder from the shell. Never infer completeness from the visible browser rows.
5. Match the polling-station name across the complete metadata. Include every room and part, even when part numbers are separated by dozens of unrelated files.
6. Download only the relevant PDFs, extract all pages, and search all matched parts together.
7. Search exact names, likely spelling variants, surname-only occurrences, relatives, and age ranges. Treat fuzzy hits as candidates, not identities.
8. Render or open pages containing plausible candidates to verify the extracted text visually.
9. Report the searched scope, exact part/room mapping, matches and near-matches, and the source-type caveat.

## Run the bundled investigator

Use the deterministic CLI for public Google Drive folders containing text-readable PDFs:

```bash
python3 scripts/investigate_rolls.py \
  --folder-url 'GOOGLE_DRIVE_FOLDER_URL' \
  --station 'Maruthi Vidyalaya' \
  --name 'Anita Sample' \
  --name 'Joseph Sample' \
  --output './roll-search'
```

The script:

- calls `gdown>=6.1.0 --folder --json` (pinned automatically when using `uvx`) to enumerate the full folder without downloading it;
- filters filenames by all normalized station-name tokens;
- identifies AC and part numbers from filenames where possible;
- downloads only matched PDFs;
- uses `pdftotext -layout` on every matched PDF;
- generates `manifest.json` and `report.md` with exact, likely, and surname-only candidates.

If PDFs are already local, bypass Drive:

```bash
python3 scripts/investigate_rolls.py \
  --pdf-dir './downloaded-parts' \
  --name 'Mary Sample' \
  --output './roll-search'
```

Request network approval when required. Do not download an entire AC folder merely to search one polling station.

## Search and verification rules

- Search all room PDFs as one corpus.
- Include common first-name variants and truncations; use surname plus a given name or relative as the strongest signal.
- Compare age to the roll's generation year, allowing for off-by-one errors and stale ages.
- Inspect neighboring entries when household members may be sequential.
- Preserve EPIC number, serial number, part, room, age, relative, reason, source PDF, and page for candidates.
- If extraction is sparse or garbled, render pages and OCR them. Do not treat failed extraction as absence.
- State “no match in the files searched,” not “the person is not registered.”

## Critical interpretation guardrails

- An ASDDO/ASD file is not the full electoral roll. Absence from it only means no match in that flagged subset.
- A polling-station building can contain many rooms and parts. Search every matching filename.
- Current AC numbers cannot be projected backward to 2002/2004 without historical boundary evidence. Search the historical address under the contemporaneous district/AC hierarchy and check adjacent plausible parts.
- Filename ordering is lexicographic, not geographic; Part 231 and Parts 304–310 may belong to the same building.
- Similar surnames, Christian names, ages, or nearby serials are leads—not proof of identity.

## Browser fallback

Use browser interaction only when shell metadata access fails because of authentication, CAPTCHA, or a non-public source. Even then, force or verify full pagination before concluding how many files exist. Return to scripted download and corpus search as soon as direct file URLs or IDs are available.

## Deliverable

Lead with the result, then provide:

- source and roll type;
- district/AC if established;
- every part and room searched;
- exact matches and clearly labelled near-matches;
- links or local paths to source PDFs;
- limitations and the next most useful source.
