"""Extract the Genadendal Diaries tables (Google Sheets PDF exports, Zenodo 18095167) to CSV.

Each PDF is a five-column table: ID, diplomatic transcription, normalised text,
English, Afrikaans. Column bounds are read from the header row on every page,
because they shift from page to page. Needs poppler's pdftotext (24.x, -tsv).

Usage: python scripts/extract.py <folder with the Zenodo PDFs> data
Writes data/A363349.csv and so on. The PDFs are not kept in this repository;
download them from Zenodo and check them against SHA256SUMS first."""
import csv, re, subprocess, sys
from pathlib import Path

HEAD = {"ID": "id", "Diplomatische": "diplomatic", "Normalisierter": "normalised",
        "Englisch": "english", "Afrikaans": "afrikaans"}
ID_RE = re.compile(r"^NL-UtHUA_A\d+_\d+$")
FIELDS = ["id", "pdf_page", "diplomatic", "normalised", "english", "afrikaans"]

def words_by_page(pdf):
    tsv = subprocess.run(["pdftotext", "-tsv", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    pages = {}
    for line in tsv.splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 12 or f[0] != "5":
            continue
        pages.setdefault(int(f[1]), []).append(
            {"x": float(f[6]), "top": float(f[7]), "text": f[11]})
    return pages

def extract(pdf):
    rows = []
    for pno, words in sorted(words_by_page(pdf).items()):
        heads = {}
        for w in words:
            if w["text"] in HEAD and HEAD[w["text"]] not in heads and w["top"] < 80:
                heads[HEAD[w["text"]]] = w
        if len(heads) < 5:
            print(f"  {pdf.name} p{pno}: header incomplete {sorted(heads)}", file=sys.stderr)
            continue
        order = sorted(heads, key=lambda n: heads[n]["x"])
        starts = [heads[n]["x"] for n in order]
        body_top = max(heads[n]["top"] for n in order) + 6
        lines = {}
        for w in words:
            if body_top < w["top"] < 560:          # skip header and footer bands
                lines.setdefault(round(w["top"]), []).append(w)
        for top in sorted(lines):
            cells = {n: [] for n in order}
            for w in sorted(lines[top], key=lambda w: w["x"]):
                i = max([k for k, s in enumerate(starts) if w["x"] >= s - 3] or [0])
                cells[order[i]].append(w["text"])
            rec = {n: " ".join(v) for n, v in cells.items()}
            if ID_RE.match(rec["id"]):
                rec["pdf_page"] = pno
                rows.append(rec)
            elif rows and not rec["id"]:            # a wrapped line belongs to the row above
                for n in order[1:]:
                    if rec[n]:
                        rows[-1][n] = (rows[-1][n] + " " + rec[n]).strip()
    return rows

def is_missing(text):
    return "Wird geladen" in text or not text.strip()

if __name__ == "__main__":
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(src.glob("*.pdf")):
        rows = extract(pdf)
        name = pdf.stem.replace("NL-UtHUA_", "").replace("_Diary-Genadendal", "")
        with open(out / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
        text_rows = [r for r in rows if r["normalised"].strip() and not r["normalised"].startswith("<pb")]
        miss = sum(is_missing(r["english"]) for r in text_rows)
        print(f"{pdf.name}: {len(rows)} rows, {len(text_rows)} with text, English missing in {miss}")
