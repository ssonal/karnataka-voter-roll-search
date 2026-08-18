---
name: karnataka-voter-roll-search
description: Investigate Karnataka electoral-roll, SIR, ASDDO/ASD, and historical voter-list records using official CEO Karnataka pages, Google Drive folders, and PDF rolls. Use when Codex must map an address to district/Assembly Constituency/part/room, enumerate every polling-station PDF, search people despite spelling or data-entry variations, distinguish current from 2002/2004 constituencies, or verify whether a person appears in a full roll versus a flagged ASDDO list.
---

# Karnataka Voter Roll Search

Use web search, browser interaction, and shell automation tactically. Choose the tool that best fits each step while preserving evidence and verifying completeness.

Discover official sources autonomously. Do not ask the user to find or provide CEO Karnataka pages, Drive folders, district folders, AC folders, or PDF URLs when they are publicly discoverable. Ask for a link only after official-source discovery has genuinely failed or when the user refers to a private/non-public source.

## Default workflow

1. Record the known facts without blocking on optional details:
   - full and familiar names, birth year or approximate age, relatives
   - current address and the period it applies to
   - current polling station, AC, and part, when known
   - each former address and the approximate years it applied
   - former polling station, AC, and part for each period, when known
   - target election year or roll type
   Keep current and former facts in separate timeline buckets. Never silently use a current polling station, AC, or part as evidence for a historical address.
2. Classify the source before searching:
   - full electoral roll
   - ASDDO/ASD or other flagged subset
   - historical roll, especially pre-delimitation 2002/2004 material
3. Start from the official CEO Karnataka entry points in [references/karnataka-electoral-sources.md](references/karnataka-electoral-sources.md). Use web search or browser navigation to resolve their current linked folders and files; never make source discovery the user's job.
4. Enumerate complete Drive folders with shell metadata or another complete-listing interface when practical. Browser navigation is useful, but never infer completeness from only the currently rendered rows of a virtualized folder.
5. Match the polling-station name across the complete metadata. Include every room and part, even when part numbers are separated by dozens of unrelated files.
6. Download only the relevant PDFs, extract all pages, and search all matched parts together.
7. Search exact names, likely spelling variants, surname-only occurrences, relatives, and age ranges. Treat fuzzy hits as candidates, not identities.
8. Render or open pages containing plausible candidates to verify the extracted text visually.
9. Report the searched scope, exact part/room mapping, matches and near-matches, and the source-type caveat.

## Internal automation

After discovering the relevant public Drive folder, run the bundled investigator internally. Do not instruct the user to run it:

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

If the user already supplied PDFs, bypass Drive internally:

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
- Treat current and former polling stations as separate leads tied to their stated time periods. If the user is unsure which station applies to which address, resolve the ambiguity from official records instead of combining them.
- Filename ordering is lexicographic, not geographic; Part 231 and Parts 304–310 may belong to the same building.
- Similar surnames, Christian names, ages, or nearby serials are leads—not proof of identity.

## Tactical tool choice

- Use web search and browser interaction to discover current official pages, follow changing links, understand page hierarchy, handle authentication or CAPTCHA, inspect individual records, and visually verify PDF candidates.
- Use shell scripts or complete-listing APIs to enumerate large folders, download a scoped set of PDFs, extract text, and search many parts reproducibly.
- Mix these tools freely. Do not force shell use when browser or web search is more efficient, and do not trust a virtualized browser list as complete without forcing or independently verifying full pagination.

## Deliverable

Lead with the result, then provide:

- source and roll type;
- current and historical district/AC mappings separately, when established;
- every part and room searched;
- exact matches and clearly labelled near-matches;
- links or local paths to source PDFs;
- limitations and the next most useful source.
