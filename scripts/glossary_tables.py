"""Write the people and places in glossary.csv as Markdown tables.

glossary.csv is the source. This script writes reference/people.md and
reference/places.md from it, with each first mention linked to the translated
entry that holds that line. Run it again after changing the glossary:

  python scripts/glossary_tables.py
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import translate as T  # noqa: E402

ROOT = T.ROOT
OUT = ROOT / "reference"


def entry_finder():
    """Map (file, line ID) to the translated entry file that covers the line."""
    cache = {}

    def find(stem, line):
        if stem not in cache:
            rows = T.load_rows(stem)
            start = T.body_start(rows)
            ids = [r["id"] for r in rows]
            spans = []
            for e in T.load_entries(stem):
                a = T.locate(ids, e["first_line"], start)
                b = T.locate(ids, e["last_line"], start)
                files = list((ROOT / "translations" / "en" / stem).glob(f"{e['entry']}-*.md"))
                if files:
                    spans.append((a, b, e["entry"], files[0]))
            cache[stem] = (ids, start, spans)
        ids, start, spans = cache[stem]
        target = f"NL-UtHUA_{stem}_{line}"
        try:
            i = ids.index(target, start)
        except ValueError:
            return None
        for a, b, entry, path in spans:
            if a <= i <= b:
                return entry, path
        return None

    return find


def cell(text):
    return text.replace("|", "\\|").strip()


def sort_key(row):
    name = re.sub(r"^(the|a) ", "", row["term"], flags=re.I)
    return name.lower()


def first_mention(find, value):
    m = re.match(r"(A36\d{4})_(\w+)$", value)
    if not m:
        return cell(value)
    stem, line = m.groups()
    hit = find(stem, line)
    if not hit:
        return f"{stem}, line {line}"
    entry, path = hit
    return f"[{stem} entry {entry}](../{path.relative_to(ROOT).as_posix()}), line {line}"


def table(rows, find, title, intro, kind_label):
    out = [f"# {title}", "", intro, "",
           f"| {kind_label} | In the translations | Spellings in the sources | Notes | First mention |",
           "| --- | --- | --- | --- | --- |"]
    for r in sorted(rows, key=sort_key):
        out.append("| {} | {} | {} | {} | {} |".format(
            cell(r["term"]), cell(r["english_rendering"]), cell(r["forms_in_source"]),
            cell(r["note"]), first_mention(find, r["first_seen"])))
    unidentified = sum(1 for r in rows if re.search(r"[Nn]ot identified", r["note"]))
    out += ["", f"{len(rows)} entries; {unidentified} marked \"Not identified\".", ""]
    return "\n".join(out)


INTRO = ("Generated from [`glossary.csv`](../glossary.csv) by `scripts/glossary_tables.py`; "
         "edit the CSV, not this file, and run the script again. "
         "*In the translations* is the form the English translations use. "
         "*Spellings in the sources* are the forms in the transcriptions, which are automatic and often misread names; "
         "\"(A363349)\" marks forms from the Dutch file. "
         "*First mention* is the first line where the name was recorded, linked to the translated entry.")


def main():
    rows = list(csv.DictReader(open(ROOT / "glossary.csv", encoding="utf-8")))
    find = entry_finder()
    OUT.mkdir(exist_ok=True)
    people = [r for r in rows if r["kind"] == "person"]
    places = [r for r in rows if r["kind"] == "place"]
    (OUT / "people.md").write_text(table(people, find, "People", INTRO, "Person"), encoding="utf-8")
    (OUT / "places.md").write_text(table(places, find, "Places", INTRO, "Place"), encoding="utf-8")
    print(f"wrote reference/people.md ({len(people)}) and reference/places.md ({len(places)})")


if __name__ == "__main__":
    main()
