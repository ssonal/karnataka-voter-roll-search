# Karnataka Voter Roll Search

A Codex skill for finding people across Karnataka voter-roll, SIR, ASDDO/ASD, and historical-roll PDFs.

It uses the shell to:

- enumerate complete Google Drive folders;
- find every part and room for a polling station;
- download and search only the relevant PDFs;
- report exact, fuzzy, and surname-only candidates separately.

## Install

```bash
git clone https://github.com/ssonal/karnataka-voter-roll-search.git \
  ~/.codex/skills/karnataka-voter-roll-search
```

Then ask Codex:

```text
Use $karnataka-voter-roll-search to find every part for Example Public School
in this Drive folder and check Anita Sample across all matching PDFs.
```

## Run the CLI directly

```bash
python3 scripts/investigate_rolls.py \
  --folder-url 'GOOGLE_DRIVE_FOLDER_URL' \
  --station 'Example Public School' \
  --name 'Anita Sample' \
  --source-type ASDDO \
  --output './roll-search'
```

Requirements: Python 3.10+, `uvx` or `gdown>=6.1.0`, and Poppler's `pdftotext`.

Run tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Important

- ASDDO/ASD files are flagged subsets, not complete electoral rolls.
- A missing or poorly extracted name is not proof that a person is unregistered.
- Do not commit voter PDFs, extracted records, reports, or personal details.

See [SKILL.md](SKILL.md) for the full workflow and guardrails.

MIT licensed. See [LICENSE](LICENSE).
