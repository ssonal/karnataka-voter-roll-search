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

Tell Codex what you know. You do not need to find any website or Drive link:

```text
Use $karnataka-voter-roll-search.

Names: Anita Sample and Joseph Sample
Birth years or approximate ages: 1964 and 1966

Current address: 45 Current Road, Bengaluru
Current polling station: Example Public School (if known)

Former address: 12 Old Road, Bengaluru
Years at former address: approximately 2000-2005
Former polling station: unknown

Records to check: current ASDDO and the 2002 voter roll
```

Current and former polling stations, relatives' names, birth years, constituency, or part numbers are helpful when available. Write `unknown` for anything you do not know.

The skill will find the official CEO Karnataka sources itself, map the available details, enumerate every matching part and room, download only the relevant PDFs, search spelling variations, and clearly separate exact matches from weaker leads.

## Important

- ASDDO/ASD files are flagged subsets, not complete electoral rolls.
- A missing or poorly extracted name is not proof that a person is unregistered.
- Codex may ask permission before accessing or downloading public files.
- Do not publish voter PDFs, extracted records, reports, or personal details.

MIT licensed. See [LICENSE](LICENSE).
