# Karnataka Voter Roll Search

A Codex skill for finding people across Karnataka voter-roll, SIR, ASDDO/ASD, and historical-roll PDFs.

## Install - no Terminal needed

Open Codex and paste this:

```text
Use $skill-installer to install the skill from
https://github.com/ssonal/karnataka-voter-roll-search
```

Codex will install it for you. The skill will be available in your next message.

## Use it

Paste the official voter-list or Google Drive link and say what you know:

```text
Use $karnataka-voter-roll-search.

Polling station: Example Public School
Names: Anita Sample and Joseph Sample
Approximate ages: 60 and 58
Link: GOOGLE_DRIVE_OR_CEO_KARNATAKA_URL
```

Old address, relatives' names, birth years, constituency, or part numbers are helpful when available, but you do not need to know everything before starting.

The skill will enumerate every matching part and room, download only the relevant PDFs, search spelling variations, and clearly separate exact matches from weaker leads.

## Important

- ASDDO/ASD files are flagged subsets, not complete electoral rolls.
- A missing or poorly extracted name is not proof that a person is unregistered.
- Codex may ask permission before accessing or downloading public files.
- Do not publish voter PDFs, extracted records, reports, or personal details.

MIT licensed. See [LICENSE](LICENSE).
