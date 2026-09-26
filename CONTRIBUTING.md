# Checking a passage

The English translations here were made by a machine and need people who read eighteenth-century German or Dutch to check them. You do not need to know Git well: GitHub's web editor is enough.

## What to check

1. Pick a file in `translations/en/` whose front matter says `review_status: machine-translation-unreviewed`.
2. Each paragraph starts with a comment such as `<!-- lines 00025-00031 -->`. Find those line IDs in `data/<file>.csv` and read the `diplomatic` column (what the manuscript says) and the `normalised` column (the same text in modern spelling).
3. Where you can, look at the manuscript image named in the `<pb>` row above the lines. The transcription is automatic and does misread words. [`reference/image-checks.md`](reference/image-checks.md) lists the readings the notes flag for checking, page image by page image.
4. Compare the English with the German or Dutch. Look for:
   - wrong meaning, or a sentence left out or added;
   - a doubtful reading that needs a note;
   - names and terms that differ from `glossary.csv`;
   - the diarists' own words turned into modern ones, or modern words put in their mouths.

## How to propose a change

1. Open the file on GitHub and choose **Edit**.
2. Correct the English in place. If a reading is doubtful, add a numbered note at the end of the file and say what the manuscript or transcription has.
3. If you checked the whole file, change the front matter:
   ```yaml
   review_status: reviewed
   reviewers: [your name or GitHub handle]
   ```
   If you checked only part of it, use `review_status: partly-reviewed` and say in the pull request which line ranges you checked.
4. Save the change as a pull request. In the description, say which lines you checked and against what (transcription, image, or the printed edition).

Every change is read by a maintainer before it is merged. Please do not copy text from the 1992 printed edition of *The Genadendal Diaries*: it is in copyright. You may use it to check a reading and say so in your pull request.

## Review statuses

| Status | Meaning |
| --- | --- |
| `machine-translation-unreviewed` | Made by a machine; no person has checked it. |
| `partly-reviewed` | A person has checked some passages; the pull request says which. |
| `reviewed` | A person has checked the whole file against the German or Dutch. |

## Offensive words

The diarists call Khoekhoe people "Hottentots" and Xhosa people "Kaffers". Keep these words in the translations where the manuscript has them, and do not use them anywhere else. See the README and `glossary.csv`.

## Working on the scripts

```
python scripts/extract.py <folder with the Zenodo PDFs> data   # PDFs to CSV
python scripts/reading.py data text                             # CSV to reading texts
python scripts/translate.py packets A363597                     # source packets per entry, in work/
python scripts/translate.py check A363597                       # front matter and line coverage
python scripts/glossary_tables.py                               # reference/people.md and places.md from glossary.csv
```

The scripts need Python 3.10 or later; `extract.py` also needs poppler's `pdftotext` (version 24 or later).

## Line IDs and entries

A new translation starts with a row in `translations/en/<file>/entries.csv` giving the entry number, title, period, and first and last line ID. Two entries may share a line when a new date begins in the middle of it. Run `translate.py check` before opening a pull request: it reports any text line that no entry covers.
