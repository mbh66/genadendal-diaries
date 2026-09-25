"""Prepare translation packets and check finished translations.

The translations are made one diary entry at a time. An entry is a stretch of
manuscript lines (usually one month) listed in translations/en/<file>/entries.csv
with its first and last line ID. This script does not call a translation model.
It does two jobs around the translation step:

  packets  Write one source packet per entry to work/<file>/: the normalised
           German as whole sentences, each with its line IDs and page, and the
           diplomatic transcription of the same lines for checking.

  assemble Wrap each translated body in work/<file>/en/<entry>.md with the
           front matter from entries.csv and write it to translations/en/<file>/.

  check    Confirm that every Markdown file in translations/en/<file>/ has the
           required front matter, that its line range matches entries.csv, and
           that the entries cover the file's text lines with no gaps.

Usage:
  python scripts/translate.py packets A363597
  python scripts/translate.py assemble A363597 --method "..." --date 2026-09-25
  python scripts/translate.py check A363597
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from segment import PB, sentences, tokens  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EDITION = "Garcés Pérez and Lasch, Zenodo, doi:10.5281/zenodo.18095167, version 0.3"
REQUIRED = ["title", "source_file", "entry", "period", "first_line", "last_line",
            "source_column", "method", "review_status", "licence"]


def load_rows(stem):
    return list(csv.DictReader(open(ROOT / "data" / f"{stem}.csv", encoding="utf-8")))


def load_entries(stem):
    return list(csv.DictReader(open(ROOT / "translations" / "en" / stem / "entries.csv",
                                    encoding="utf-8")))


def slice_rows(rows, first, last, with_page=False):
    ids = [r["id"] for r in rows]
    a, b = ids.index(first), ids.index(last)
    part = rows[a: b + 1]
    if with_page:  # prepend the page marker in force, so the first sentence knows its page
        k = a
        while k > 0 and not rows[k]["normalised"].startswith("<pb"):
            k -= 1
        if k != a:
            part = [rows[k]] + part
    return part


def packets(stem):
    rows = load_rows(stem)
    out = ROOT / "work" / stem
    out.mkdir(parents=True, exist_ok=True)
    for e in load_entries(stem):
        part = slice_rows(rows, e["first_line"], e["last_line"], with_page=True)
        lines = [f"# {e['entry']} {e['title']} ({e['first_line']} to {e['last_line']})", "",
                 "## Normalised German, by sentence", ""]
        for i, (s, a, b) in enumerate(sentences(tokens(part)), 1):
            lines.append(f"{i}\t{a[0].split('_')[-1]}-{b[0].split('_')[-1]}\tp.{a[1]}\t{s}")
        lines += ["", "## Diplomatic transcription, by line", ""]
        for r in part:
            if not PB.search(r["diplomatic"]):
                lines.append(f"{r['id'].split('_')[-1]}\t{r['diplomatic']}")
        (out / f"{e['entry']}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"packets written to {out}")


def pages_of(rows):
    pages = []
    current = None
    for r in rows:
        m = PB.search(r["normalised"])
        if m and r["normalised"].startswith("<pb"):
            current = m.group(1)
        elif r["normalised"].strip() and current and current not in pages:
            pages.append(current)
    return pages


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower().replace("'", "")).strip("-")


def assemble(stem, method, date, force=False):
    rows = load_rows(stem)
    src = ROOT / "work" / stem / "en"
    dst = ROOT / "translations" / "en" / stem
    for e in load_entries(stem):
        body_path = src / f"{e['entry']}.md"
        if not body_path.exists():
            continue
        pages = pages_of(slice_rows(rows, e["first_line"], e["last_line"], with_page=True))
        fm = [
            "---",
            f'title: "{e["title"]}"',
            f"source_file: NL-UtHUA_{stem}",
            f'entry: "{e["entry"]}"',
            f"period: {e['period']}",
            f"first_line: {e['first_line']}",
            f"last_line: {e['last_line']}",
            f'pages: "{pages[0]} to {pages[-1]}"' if len(pages) > 1 else f'pages: "{pages[0]}"',
            "source_column: normalised German, checked against the diplomatic transcription",
            f'source_edition: "{EDITION}"',
            f'method: "{method}"',
            f"translated: {date}",
            "review_status: machine-translation-unreviewed",
            "reviewers: []",
            "licence: CC BY 4.0",
            "---",
            "",
            "",
        ]
        out = dst / f"{e['entry']}-{slug(e['title'])}.md"
        if out.exists() and not force:
            # translations/ is the working copy once a file exists: reviewers edit it there
            print("kept", out.relative_to(ROOT), "(exists; use --force to replace)")
            continue
        out.write_text("\n".join(fm) + body_path.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[m.end():]


def check(stem):
    rows = load_rows(stem)
    ids = [r["id"] for r in rows]
    text_idx = {i for i, r in enumerate(rows)
                if r["normalised"].strip() and not r["normalised"].startswith("<pb")}
    covered = set()
    problems = 0
    entries = {e["entry"]: e for e in load_entries(stem)}
    files = sorted((ROOT / "translations" / "en" / stem).glob("*.md"))
    for f in files:
        meta, body = front_matter(f)
        if meta is None:
            print(f"{f.name}: no front matter"); problems += 1; continue
        missing = [k for k in REQUIRED if k not in meta]
        if missing:
            print(f"{f.name}: missing {missing}"); problems += 1
        e = entries.get(meta.get("entry"))
        if not e:
            print(f"{f.name}: entry {meta.get('entry')} not in entries.csv"); problems += 1; continue
        if (meta.get("first_line"), meta.get("last_line")) != (e["first_line"], e["last_line"]):
            print(f"{f.name}: line range differs from entries.csv"); problems += 1
        a, b = ids.index(e["first_line"]), ids.index(e["last_line"])
        covered.update(range(a, b + 1))
        for ref in re.findall(r"<!-- lines (\w+)-(\w+)", body):
            for x in ref:
                full = f"NL-UtHUA_{stem}_{x}"
                if full not in ids or not a <= ids.index(full) <= b:
                    print(f"{f.name}: passage marker {x} outside the entry"); problems += 1
    gaps = sorted(text_idx - covered)
    if gaps:
        print(f"{len(gaps)} text lines not covered, first: {[ids[i] for i in gaps[:5]]}")
        problems += 1
    print(f"{len(files)} files checked, {problems} problem(s)")
    return problems


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["packets", "assemble", "check"])
    ap.add_argument("stem")
    ap.add_argument("--method", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.cmd == "packets":
        packets(a.stem)
    elif a.cmd == "assemble":
        assemble(a.stem, a.method, a.date, a.force)
    else:
        sys.exit(1 if check(a.stem) else 0)
