# Karnataka electoral sources and interpretation

## Official entry points

- CEO Karnataka voter lists: <https://ceo.karnataka.gov.in/voter_list.html>
- CEO Karnataka ASDDO page: <https://ceo.karnataka.gov.in/asddo.html>

Follow the current links from these pages rather than hardcoding temporary Google Drive folder IDs in the skill.

## Record hierarchy

Common filenames encode an election/state prefix, AC number, part number, polling-station building, room, and generation timestamp. For example, `S10_160_304_...Room No.2...pdf` indicates AC 160 and Part 304; the room must still be read from the filename or PDF header.

Do not assume files for one building are contiguous. Drive sorts filenames lexicographically, and election offices may publish replacements or supplements under distant part numbers.

## Source types

### Full electoral roll

Use this to determine whether a voter is present in a part. Check the main roll and all supplements that apply to the requested date.

### ASDDO/ASD and similar lists

These are flagged subsets, commonly showing fields such as elector name, relative, age, and an uncollectable reason such as permanently shifted, death, or untraceable/absent. They are not a substitute for the full roll.

Conclusions must say “not found in the ASDDO files searched,” never “not on the electoral roll.”

### Historical 2002/2004 material

Treat historical constituency mapping as a separate research problem. Delimitation and administrative changes mean a present-day AC or part is not reliable evidence for 2002. Start from the old address, contemporaneous locality spelling, historical district/AC listings, and adjacent plausible parts.

Manual data entry creates variant locality and personal-name spellings. Search address tokens individually and tolerate substitutions, omissions, initials, transliteration, and reordered names.

## Identity checks

Rank evidence approximately as follows:

1. EPIC number or exact person plus linked household relative
2. surname plus given-name variant, compatible age, and matching relative
3. exact name with compatible locality/part
4. surname-only or first-name-only occurrence

Never merge people based only on a common name. Preserve the row exactly and label uncertain results as candidates.

## Privacy

Download and search electoral PDFs locally when possible. Share only the rows necessary to answer the request. Avoid publishing bulk voter data or unrelated personal details.
