# Genadendal Diaries

Machine-readable transcriptions of the Moravian mission diaries of Baviaanskloof (Genadendal, Western Cape) from 1792 to 1805, with new English translations made entry by entry and a review process that readers of old German and Dutch can join.

The texts come from the edition by Juan Luis Garcés Pérez and Alexander Lasch, *Multilingual working and reading versions of the "Genadendal Diaries" from the Utrecht Archives* (Zenodo, version 0.3, 30 December 2025, [doi:10.5281/zenodo.18095167](https://doi.org/10.5281/zenodo.18095167)), made by the Moravian Knowledge Network team in Dresden from manuscripts held at Het Utrechts Archief. This repository is not part of that edition and has not been reviewed by its makers.

> **Status.** Private working repository. The first translation (A363597) is a pilot and has not been checked by a person. Nothing here should be quoted as a finished translation.

## The diaries

In 1792 three Moravian missionaries, Hendrik Marsveld, Daniel Schwinn and Johann Christian Kühnel, re-founded the mission at Baviaanskloof that Georg Schmidt had begun in 1738. The missionaries sent regular diaries and reports to the church in Europe. The copies used here are in the archive of the Moravian congregation at Zeist, now at Het Utrechts Archief.

The diaries are a missionary record, written by the missionaries for their church. They tell the story from one side: the Khoekhoe people of the mission appear through the missionaries' eyes and words, and their own accounts are reported second hand when they appear at all.

## The files

| File | Language of the manuscript | What it covers | PDF pages | Rows |
| --- | --- | --- | ---: | ---: |
| A363595 | German | Diary of the three missionaries, November 1792 to 1795 | 202 | 14,904 |
| A363349 | Dutch | Diaries and reports, April 1793 to 1798; 10 April to 31 August 1794 missing | 204 | 16,455 |
| A363596 | German | "Diary of the 3 Brethren at the Cape, 1795–96", from March 1795 | 46 | 3,398 |
| A363597 | German | Diary May 1803 to February 1804; extract June to November 1804; report December 1804 to May 1805; account of the death and burial of Br. Rose (12 October, probably 1805) | 29 | 2,173 |

The periods come from the headings in the files themselves. A363597 runs well past the "May 1803 to February 1804" of its title page.

The PDFs are not kept here. Download them from Zenodo and check them against [`SHA256SUMS`](SHA256SUMS). The MD5 checksums of the local copies match those Zenodo lists for version 0.3.

## What is in this repository

```
data/              one CSV per file, one row per manuscript line
text/              joined reading texts: diplomatic (as written) and normalised
translations/en/   new English translations, one Markdown file per diary entry
glossary.csv       people, places, terms, and the policy on offensive words
scripts/           extract.py, reading.py, segment.py, translate.py
CITATION.cff       how to cite this repository and the edition it builds on
CONTRIBUTING.md    how to check a passage
SHA256SUMS         checksums of the Zenodo PDFs
```

### data/

Each CSV has the columns `id, pdf_page, diplomatic, normalised, english, afrikaans`. They were extracted from the PDFs with `scripts/extract.py` (poppler `pdftotext -tsv`, version 24.02). Running the script again on the Zenodo PDFs reproduces the CSVs byte for byte.

- `id` is the line ID from the edition, for example `NL-UtHUA_A363597_00025`. The number after the last underscore is zero-padded to five digits below 100 and unpadded from 100 up (`NL-UtHUA_A363597_137`). Use the ID exactly as written.
- Rows whose text is `<pb n="2a" source="...jpg" />` mark the start of a manuscript page. The last word of each page is repeated at the top of the next, as a catchword.
- Gaps in the ID numbering are in the source files; the extraction lost nothing. A363349 has 18 repeated IDs in its register section.

### text/

Reading texts made from `data/` with `scripts/reading.py`: page markers become `[p. N]` and line-end hyphens are joined. Catchwords are left in.

### translations/en/

One Markdown file per diary entry, usually one month. The front matter records the source file, the first and last line ID, the manuscript pages, the source column, the method (model and date) and the review status. Inside the file, each paragraph is preceded by a comment giving its line range, for example `<!-- lines 00025-00031 -->`. `translations/en/<file>/entries.csv` lists the entries and their line ranges, and `python scripts/translate.py check A363597` confirms that the entries cover every text line of the file.

Every translation is labelled `machine-translation-unreviewed` until a person has checked it against the German or Dutch. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Limits of the texts

Read these before relying on anything here.

1. **The transcription is automatic.** Zenodo describes the versions as automatically transcribed, normalised and translated. The diplomatic column has misread words and some lost lines (for example A363597 line 1730). Where it matters, check the manuscript image.
2. **The normalised column is also automatic, and sometimes goes beyond normalising.** It handles page breaks unevenly (dropped catchwords, repeated syllables, stray fragments such as *Tau.* for the end of *gethan*). In places it replaces historical vocabulary with modern terms: A363597 line 2098 has *Xhosa* where the manuscript has *Kaffern*, and eight lines of A363595 (11217 to 11374) have *Khoikhoi* where the transcription has *Gottentotten*, a misreading of *Hottentotten*. The diplomatic column is the record of what the manuscript says.
3. **In A363349 the manuscript is Dutch.** The diplomatic column is Dutch, and the "normalised" column is a German translation of it.
4. **The English column in the source is unreliable.** It is an automatic translation made one line at a time, so sentences are cut apart. 57 cells hold only "Wird geladen..." ("Loading..."): 40 in A363596 and 17 in A363597. There are mistranslations (*Kennzeichen* as "license plate"; "the Hottentots showed themselves very grateful for this instruction" as "I am very grateful for this lesson"). The Afrikaans column was made the same way. Neither is used for the new translations.

## Translation method

- Translate from the normalised German, sentence by sentence, and check each passage against the diplomatic transcription. For A363349, work from the Dutch and use the German as a check.
- Work one entry at a time so that sentences stay whole, and record the line IDs of every passage.
- Keep names and terms consistent with `glossary.csv`.
- Mark editorial additions in square brackets, and explain doubtful readings in numbered notes at the end of each file.
- Label every passage as a machine translation until a person has checked it.
- For 1792 to 1794, check against the printed edition: H.C. Bredekamp, A.B.L. Flegg and H.E.F. Plüddemann (eds), *The Genadendal Diaries*, vol. 1 (UWC Institute for Historical Research, 1992). It is in copyright: use it to check the translations and do not copy from it.

### Offensive words

The diarists call Khoekhoe people "Hottentots" and Xhosa people "Kaffers". Both words are offensive, and the second became a severe racial slur in South Africa. The translations keep them where the diarists used them, because a translation must show what its source says. They are explained in `glossary.csv` and in a note on first use. They never appear in our own words: README text, notes and glossary explanations use Khoekhoe (or Khoe, or the name of a particular people) and Xhosa.

## Citing

Cite a passage by file, line ID and release, for example: Genadendal Diaries, A363597, lines 00025–00031 (release v0.1). Always credit the edition by Garcés Pérez and Lasch as the source of the transcriptions. See [CITATION.cff](CITATION.cff).

## Credits

- Transcriptions, normalised text and the source English and Afrikaans columns: Juan Luis Garcés Pérez (SLUB Dresden) and Alexander Lasch (TU Dresden), Moravian Knowledge Network, [#DigitalHerrnhut](https://dhh.hypotheses.org/). Licensed CC BY 4.0.
- Manuscripts: Het Utrechts Archief, archive of the Evangelische Broedergemeente Zeist.
- Extraction scripts, new English translations and glossary: this repository.

## Licence

The texts in `data/` and `text/`, the translations in `translations/`, and `glossary.csv` are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). The scripts in `scripts/` are licensed under the MIT licence. See [LICENSE](LICENSE).
