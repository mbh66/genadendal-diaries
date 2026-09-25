# Instructions for Claude: Genadendal Diaries

This repository holds machine-readable transcriptions of the Moravian mission diaries of Baviaanskloof (Genadendal), 1792 to 1805, and new English translations made entry by entry. Read `README.md` and `CONTRIBUTING.md` before starting. The owner is Michael (GitHub: mbh66), who is not a programmer: explain Git steps in plain language when you report to him.

## Current state (September 2026)

- `translations/en/A363597/` is done: 15 entries, the pilot, all `machine-translation-unreviewed`. Use it as the model for format, tone and notes.
- `translations/en/A363596/` is done: 13 entries, March 1795 to March 1796.
- **A363595** (German, 14,904 rows) is in progress. Entries 01 to 10 cover lines 00002 to 5017 (23 November 1792 to 31 July 1793). The next batch starts with August 1793 at line 5017 (*Den 1. August*); the second diary ends at line 5998 and the third begins at line 6006. The transcription jumps from page image 56 to 64 between lines 2861 and 2863, losing the end of March and most of April 1793. The image numbers also jump at lines 3579 and 4620, but the text runs on there.
- In A363595 the diplomatic column sometimes runs a few lines behind the normalised column (for example at lines 915 to 922). Packets and line markers follow the normalised column.
- After A363595: **A363349** (Dutch, 16,455 rows).
- A363595 and A363349 are too large for one session. Work in batches of about 10 entries per session and per pull request.

## How to translate a file

1. **Define the entries.** Create `translations/en/<file>/entries.csv` with the columns `entry,title,period,first_line,last_line`. An entry is one month of the diary, or one section where the manuscript is organised by report. Find the boundaries from the headings and dates in `text/<file>_normalised.txt` and the line IDs in `data/<file>.csv`. Two entries may share a line when a new date begins mid-line. Titles are plain, for example `March 1795`.
2. **Build the packets.** `python scripts/translate.py packets <file>` writes one packet per entry to `work/<file>/` (git-ignored): the normalised text by sentence with line IDs and pages, then the diplomatic transcription line by line.
3. **Translate each entry** into `work/<file>/en/<entry>.md`, following the rules below. Copy the opening note block from an A363597 file.
4. **Assemble.** `python scripts/translate.py assemble <file> --method "Machine translation by Claude (model <your model ID>), one entry at a time, from the normalised German, checked against the diplomatic transcription" --date <YYYY-MM-DD>`. For A363349 write "from the Dutch diplomatic transcription, checked against the German" in the method. Assemble never overwrites an existing file unless you pass `--force`; do not force over a file someone has reviewed.
5. **Check.** `python scripts/translate.py check <file>` must report 0 problems before you commit. For a partial batch, list only the finished entries in `entries.csv`, or expect the check to report the uncovered lines of the unfinished ones and say so in the pull request.
6. **Compare lengths.** For each passage, the English word count is usually 0.8 to 1.3 times the German token count. A much lower ratio usually means a sentence was skipped.
7. **Open a pull request** from a branch named `translate/<file>-<first entry>-<last entry>`. In the description, list the entries, the line range, and every doubtful reading you flagged. Never merge it yourself: Michael reviews and merges.

## Translation rules

- **Source.** Translate from the normalised German, sentence by sentence, and check every passage against the diplomatic column, which is the record of what the manuscript says. Where they disagree, follow the diplomatic.
- **A363349 is different.** The manuscript is Dutch: the diplomatic column is Dutch and the "normalised" column is a German translation of it. Translate from the Dutch and use the German only as a check. `segment.py` builds sentences from the normalised column, so extend `packets` with an option to segment the diplomatic column before you start this file.
- **1792 to 1794.** Check readings against Bredekamp, Flegg and Plüddemann (eds), *The Genadendal Diaries*, vol. 1 (UWC, 1992) if Michael supplies passages. It is in copyright: never copy its wording.
- **Whole sentences.** Each paragraph is preceded by `<!-- lines FIRST-LAST -->` with the line IDs as they appear after the last underscore (`00025`, `137`). Paragraph breaks follow the diary's dated entries and topics.
- **Faithful, plain English.** Keep the diarists' meaning, order and piety; do not modernise their views. Split very long German sentences where that keeps the meaning. Keep numbers and dates as written, in the form "24 May".
- **South African (British) spelling**: baptised, Saviour, neighbour, honour.
- **Terms and names** follow `glossary.csv`: the Saviour; congregation; brothers and sisters; the speaking; baptised into the death of Jesus; communicant; candidate for baptism; fell asleep, went happily home, departed this life (keep the difference). Add new people, places and terms to the glossary with the line where they first appear, and check the line ID in `data/`.
- **Offensive words.** Where the manuscript has "Hottentot" or "Kaffer", keep the word in the translation, as the diarists wrote it. Never use either word in your own voice: notes, glossary explanations, commit messages and pull requests use Khoekhoe (or Khoe, or the specific people) and Xhosa. The normalised column sometimes inserts modern terms ("Xhosa", "Khoikhoi"); the translation follows the manuscript, with a note.
- **Editorial additions** go in square brackets. Doubtful readings, garbled or missing text, date problems and identifications go in numbered notes under `## Notes` at the end of the file, with the German or Dutch quoted and "To be checked against the image" where the manuscript image would settle it. Do not guess silently.
- **Status.** Every new file is `machine-translation-unreviewed`. Only a person can change that.

## Known problems in the source

- The transcription is automatic (handwritten text recognition). Expect misread words and lost lines.
- The normalised column mishandles page breaks: dropped or doubled catchwords, repeated syllables (*würwürde*), stray fragments (*Tau.* for the end of *gethan*). Rows starting `<pb` are page markers, not text.
- Line IDs are zero-padded below 100 and unpadded from 100 (`..._00099`, `..._100`). A363349 has 18 repeated IDs in its register section; gaps in the numbering are in the source.
- Archive shelf marks sometimes appear in the text (*P.A.I. R.5.E. 6.* at the head of A363596, *PAIRSE 12* in A363597). Leave them untranslated with a note.
- The English and Afrikaans columns in `data/` are unreliable line-by-line machine translations. Do not use them.

## Do not

- Edit `data/` or `text/`. They must stay reproducible from the Zenodo PDFs (`scripts/extract.py`, `scripts/reading.py`).
- Add the PDFs to the repository.
- Change the licence, CITATION.cff or README claims without Michael's agreement.
- Make the repository public, create releases, or change settings. Those are Michael's decisions.

## Writing style for anything addressed to Michael

American spelling in chat. No em dashes, no "not X but Y" constructions, no three-part rhythmic lists, no hollow praise, no closing summaries. Answer directly.
