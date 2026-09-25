# Instructions for Claude: Genadendal Diaries

This repository holds machine-readable transcriptions of the Moravian mission diaries of Baviaanskloof (Genadendal), 1792 to 1805, and new English translations made entry by entry. Read `README.md` and `CONTRIBUTING.md` before starting. The owner is Michael (GitHub: mbh66), who is not a programmer: explain Git steps in plain language when you report to him.

## Current state (September 2026)

- `translations/en/A363597/` is done: 15 entries, the pilot, all `machine-translation-unreviewed`. Use it as the model for format, tone and notes.
- `translations/en/A363596/` is done: 13 entries, March 1795 to March 1796.
- `translations/en/A363595/` is done: 31 entries, 23 November 1792 to 28 February 1795 (lines 00002 to 14965; the file has 14,904 rows, but the line IDs run to 14965). The July and August 1794 diaries each appear twice (entries 22 to 25); both copies are translated, and the notes of each use the other to correct misreadings. Gaps: page images 56 to 64 (end of March and most of April 1793), images 168 to 176 (4 April to about 8 June 1794), and a lost stretch in the second August 1794 copy between lines 9830 and 9832 (27 to about 30 August 1794).
- Misreadings in A363595 that may recur elsewhere: *Pferde* for *Klocke*; *Speiſen* or *Waſchen* for *Sprechen*; *Caß* or *Caſe* for *Caap*; *Gottentotten* for *Hottentotten* (lines 11217 to 11374, where the normalised column has *Khoikhoi*); *Br.* for *Hr.* before the names of officials and visitors in Marsveld's and Schwinn's reports; and wrong day numbers (the December 1794 diary has 14th for Sunday 7 December).
- **A363349** (Dutch, 16,455 rows) is in progress. Entries 01 to 30 are done: 1 April 1793 to 9 April 1794 and 1 September 1794 to 6 December 1795, lines 00002 to 11429, with Mrs Smith's letter as entry 06 and the baptised sisters' words to Europe (January 1795) as entry 20. The Dutch is a shorter version of the German diaries A363595 (to February 1795) and A363596 (from March 1795) for the same months; each entry cross-checks the German and notes where one settles the other's misreadings. The Dutch fills A363595's gaps for April 1793 and for 4 to 9 April 1794, and often settles its garbled readings (from September 1794 the German misreadings are many; the Dutch is usually the better text). From April 1795 (entry 23) the Dutch is a polished "continuation" for readers, with its own page numbers, and seems to have been translated from the German manuscript: in February 1795 it takes a German page number as a distance (entry 21, note 3), and in entry 27 German words run into the transcription (note 14).
- Next batch: **A363349 from 7 December 1795** (line 11435, the heading of the diary for 7 December 1795 to 14 March 1796; A363596 entries 11 to 13 are the German for these months). The rest of the file is not in date order: after March 1796 come the diaries for 20 May 1797 to 28 February 1798 (from line 12208), a second copy of the same months (from line 12958), 23 November 1792 to 31 March 1793 (from line 13702; the German is A363595 entries 01 to 06), 1 November 1796 to 19 May 1797 (from line 15492) and 26 June to 1 November 1796 (from line 16165). Mind the missing lines described under "Known problems" (every 82nd line ID; in entries 21 to 30 nearly every one lost a line of text, which the German supplied), and watch for repeated page images, which occur in this file (images 50 to 56, 73 and 74, 76 and 77, and 100 and 101 so far; a leaf of the Dutch copy is probably lost between images 96 and 97, entry 16, note 22): when two images hold the same text, translate it once, mark the repeat in square brackets, and use each copy to fill the lines the other has lost, as in entries 11, 14 and 16.
- A363349 is too large for one session. Work in batches of about 10 entries per session and per pull request.

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
- The diplomatic and normalised columns are sometimes out of step by a line or more (A363595 lines 915 to 922 and 9025). Packets and line markers follow the normalised column.
- Line IDs are zero-padded below 100 and unpadded from 100 (`..._00099`, `..._100`); in A363349 the padding runs to `..._00126`, and `..._127` is the first unpadded ID. Copy line IDs from the packet or `data/`. Gaps in the numbering are in the source; in A363349 many gaps lose no text, but some lose a line, so read across every gap. From line 2746 to the end of A363349, every line ID that leaves 40 when divided by 82 is missing (2746, 2828, ..., 8158, 8240, 8322, 8404 and so on), and most of these gaps lose a line of text; the German diary A363595 usually supplies the sense.
- A363349 opens with a register of 20 rows (before the first `<pb`) whose IDs repeat those of the headings they point to (3067, 5036 and so on). `translate.py` skips the register when it looks up line IDs. `packets` segments the Dutch diplomatic column for A363349 by default (`--column` overrides) and prints the German normalised column line by line below it.
- In A363349 the manuscript's page numbers sometimes run into the text (*10. Na den Eeten*) or stand alone at the head of a page; leave them out of the translation.
- Archive shelf marks sometimes appear in the text (*P.A.I. R.5.E. 6.* at the head of A363596, *PAIRSE 12* in A363597). Leave them untranslated with a note.
- The English and Afrikaans columns in `data/` are unreliable line-by-line machine translations. Do not use them.

## Do not

- Edit `data/` or `text/`. They must stay reproducible from the Zenodo PDFs (`scripts/extract.py`, `scripts/reading.py`).
- Add the PDFs to the repository.
- Change the licence, CITATION.cff or README claims without Michael's agreement.
- Make the repository public, create releases, or change settings. Those are Michael's decisions.

## Writing style for anything addressed to Michael

American spelling in chat. No em dashes, no "not X but Y" constructions, no three-part rhythmic lists, no hollow praise, no closing summaries. Answer directly.
