"""Turn the CSVs in data/ into plain reading texts in text/, one per column.

Page markers become [p. N] lines, and line-end hyphens (⸗ or =) are joined.
Only the diplomatic and normalised columns are written: the English column in
the source is an unreliable line-by-line machine translation (see README).

Usage: python scripts/reading.py data text"""
import csv, re, sys
from pathlib import Path

PB = re.compile(r'<pb n="([^"]+)"')

def build(rows, col, dehyphen):
    out, buf = [], ""
    for r in rows:
        t = r[col].strip()
        m = PB.search(r["normalised"]) or PB.search(t)
        if m and t.startswith("<pb"):
            if buf: out.append(buf.strip()); buf = ""
            out.append(f"\n[p. {m.group(1)}]")
            continue
        if not t or "Wird geladen" in t:
            if col == "english" and r["normalised"].strip():
                t = f"[missing: {r['id']}]"
            else:
                continue
        if dehyphen and buf.endswith(("⸗", "=")):
            buf = buf[:-1] + t
        else:
            buf = (buf + " " + t) if buf else t
    if buf: out.append(buf.strip())
    return "\n".join(out).strip() + "\n"

if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("*.csv")):
        rows = list(csv.DictReader(open(f, encoding="utf-8")))
        stem = f.stem.replace("NL-UtHUA_", "").replace("_Diary-Genadendal", "")
        for col, name, dh in [("diplomatic", "diplomatic", True),
                              ("normalised", "normalised", True)]:
            (dst / f"{stem}_{name}.txt").write_text(build(rows, col, dh), encoding="utf-8")
        print(stem, "done")
