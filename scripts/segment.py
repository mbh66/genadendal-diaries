"""Split one diary's normalised text into sentences, each tagged with the line IDs it covers.

The translation works on whole sentences, and every translated passage must say
which manuscript lines it comes from. This script rebuilds running text from
data/<file>.csv and records, for each sentence, the ID of the line where it
starts and the line where it ends, plus the manuscript page.

Rules:
- <pb> rows mark manuscript pages and are not text.
- Catchwords: the first word of a new page repeats the last word of the page
  before. When the two match, the repeat is dropped.
- A normalised line ending in "-" is joined to the next line when that line
  starts with a lower-case letter.

Usage: python scripts/segment.py data/A363597.csv > work/A363597_sentences.tsv
Output columns: n, first_id, last_id, page, sentence
"""
import csv
import re
import sys

PB = re.compile(r'<pb n="([^"]+)"')
ORDINAL = re.compile(r"(?<![\d.])\d{1,2}\.$")
ABBREV = re.compile(r"(?:^|[\s(])(?:Br|Brr|Geschw|v|Joh|Dan|Chr|[A-ZÄÖÜ])\.$")
SENT_END = re.compile(r'([.!?][“”"‘’)]*)(\s+)(?=[„“"‘(]?[A-ZÄÖÜ0-9–—])')


def norm_token(t):
    return re.sub(r"[^\wäöüÄÖÜß]", "", t).lower()


def tokens(rows, col="normalised"):
    """Yield (token, line_id, page) in reading order."""
    page = None
    out = []
    just_broke = False
    for r in rows:
        t = r[col].strip()
        m = PB.search(t)
        if m and t.startswith("<pb"):
            page = m.group(1)
            just_broke = True
            continue
        if not t:
            continue
        words = t.split()
        if just_broke and out and words:
            prev, first = out[-1][0], words[0]
            a, b = norm_token(prev), norm_token(first)
            if prev.endswith("-") and b.startswith(a) and a:
                # "Wit-" + "Witterung": the new page repeats the whole word
                out[-1] = (first, out[-1][1], out[-1][2])
                words = words[1:]
            elif a and b and (a == b or (len(b) >= 2 and a.endswith(b))):
                # catchword repeated ("ihnen" / "ihnen", "unterwegs" / "wegs")
                words = words[1:]
        just_broke = False
        for w in words:
            if out and out[-1][0].endswith("-") and w[:1].islower():
                prev, pid, ppage = out.pop()
                out.append((prev[:-1] + w, pid, ppage))  # keep the start line's ID
                continue
            out.append((w, r["id"], page))
    return out


def sentences(toks):
    s = " ".join(w for w, _, _ in toks)
    char_owner = []  # the (line_id, page) that owns each character of s
    for w, lid, page in toks:
        if char_owner:
            char_owner.append(char_owner[-1])
        char_owner.extend([(lid, page)] * len(w))
    start = 0
    for m in SENT_END.finditer(s):
        end = m.end(1)
        if ORDINAL.search(s[max(0, end - 4):end]):
            continue  # "am 2. Mai", "das 3. Jahr": an ordinal, not a sentence end
        if ABBREV.search(s[max(0, end - 6):end]):
            continue  # "Br. Rose", "Carl v. Forestier", "Joh. Christian"
        yield s[start:end], char_owner[start], char_owner[end - 1]
        start = m.end()
    if start < len(s):
        yield s[start:], char_owner[start], char_owner[-1]


if __name__ == "__main__":
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(["n", "first_id", "last_id", "page", "sentence"])
    for i, (sent, a, b) in enumerate(sentences(tokens(rows)), 1):
        w.writerow([i, a[0], b[0], a[1], sent])
