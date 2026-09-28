"""Decode Puech 2006 (STDJ 55) Hebrew text of 3Q15 from the PDF text layer.

The Hebrew is set in a legacy 8-bit font ("SuperHebrew", final forms partly in "HebraicaII"),
stored in visual left-to-right order. Numeral signs are vector drawings, not text; they are
emitted as placeholders ⟦N:x0-x1⟧ to be filled from the page image.
"""
import glob, json, sys, re
import pymupdf

S = "/tmp/claude-0/-home-user-AncientHebrewTexts/d46e2cba-d27e-5141-8a52-ea8809971413/scratchpad"

HEB = {
    'a': 'א', 'b': 'ב', 'g': 'ג', 'd': 'ד', 'h': 'ה', 'w': 'ו', 'z': 'ז', 'j': 'ח', 'f': 'ט',
    'y': 'י', 'k': 'כ', 'l': 'ל', 'm': 'מ', 'n': 'נ', 's': 'ס', '[': 'ע', 'p': 'פ', 'x': 'צ',
    'q': 'ק', 'r': 'ר', 'ç': 'ש', 't': 'ת', 'c': 'שׂ',
    'û': 'ך', '˚': 'ך', 'µ': 'ם', 'ˆ': 'ן', '¹': 'ף', 'å': 'ץ', 'Å': 'ץ', '≈': 'ץ',
    # sigla drawn in the Hebrew font
    '¿': '[', '?': ']', '÷': '/', 'Ñ': '(', 'ñ': ')',
}
GRK = {'A': 'Α', 'B': 'Β', 'G': 'Γ', 'D': 'Δ', 'E': 'Ε', 'Z': 'Ζ', 'H': 'Η', 'Q': 'Θ', 'I': 'Ι',
       'K': 'Κ', 'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'X': 'Ξ', 'O': 'Ο', 'P': 'Π', 'R': 'Ρ', 'S': 'Σ',
       'T': 'Τ', 'U': 'Υ', 'F': 'Φ', 'C': 'Χ', 'Y': 'Ψ', 'W': 'Ω'}
MIRROR = {'(': ')', ')': '(', '[': ']', ']': '[', '{': '}', '}': '{', '<': '>', '>': '<'}

PUECH = lambda n: glob.glob(f"/home/user/AncientHebrewTexts/Le Rouleau*-{n}.pdf")[0]


def page(g):
    doc = pymupdf.open(PUECH((g - 1) // 70 + 1))
    return doc[(g - 1) % 70]


def chars_of(p):
    """All characters with font, size, bbox, from rawdict."""
    out = []
    for b in p.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                for c in s["chars"]:
                    out.append(dict(c=c["c"], font=s["font"].split("+")[-1], size=s["size"],
                                    x0=c["bbox"][0], x1=c["bbox"][2], y0=c["bbox"][1], y1=c["bbox"][3],
                                    base=c["origin"][1]))
    return out


def hebrew_block(p):
    """Return chars that belong to the scroll text block, grouped into visual lines."""
    ch = chars_of(p)
    heb = [c for c in ch if c["font"].startswith("SuperHebrew") and c["c"] in HEB]
    if not heb:
        return [], []
    # the block: SuperHebrew letters in the text lines (not in commentary); lines ~13pt apart
    bases = sorted({round(c["base"]) for c in heb})
    # cluster baselines within 4pt
    clusters = []
    for b in bases:
        if clusters and b - clusters[-1][-1] <= 4:
            clusters[-1].append(b)
        else:
            clusters.append([b])
    lines = []
    for cl in clusters:
        lo, hi = min(cl) - 5, max(cl) + 4
        row = [c for c in ch if lo <= c["base"] <= hi]
        heb_x = [c for c in row if c["font"].startswith("SuperHebrew") and c["c"] in HEB]
        xmin = min(c["x0"] for c in heb_x) - 40
        gx = [c["x0"] for c in row if c["font"].startswith("SuperGreek")]
        if gx: xmin = min(xmin, min(gx) - 2)
        xmax = max(c["x1"] for c in row if c["font"].startswith(("SuperHebrew", "LetterGothic"))) + 2
        row = [c for c in row if xmin <= c["x0"] <= xmax]
        lines.append(dict(base=sum(cl) / len(cl), chars=sorted(row, key=lambda c: c["x0"])))
    return lines, p.get_drawings()


def classify(c):
    f, ch = c["font"], c["c"]
    if ch == " ":
        return "S"
    if f.startswith(("SuperHebrew", "HebraicaII")):
        if ch in HEB:
            return "H"
        if ch.isdigit():
            return "DH"          # digit glyph in the Hebrew font: line number or numeral sign
        return "H"
    if f.startswith("SuperGreek"):
        return "G"
    if f.startswith("Symbol"):
        return "NUM"
    if f.startswith("LetterGothic") or ch.isdigit():
        return "D"
    if ch.isalpha():
        return "G"               # Latin (sic, 12a) behaves as LTR
    return "N"


def decode_line(line, drawings):
    toks = []
    big = max(c["size"] for c in line["chars"])
    for c in line["chars"]:
        k = classify(c)
        if k == "H":
            t = HEB.get(c["c"], f"<?{c['c']}>")
            if c["size"] < big * 0.8 and t not in "[]/()":
                t = "\\" + t + "/"          # supralinear letter (Leiden-style \ /)
        elif k == "G" and c["font"].startswith("SuperGreek"):
            t = GRK.get(c["c"], c["c"])
        else:
            t = c["c"]
        toks.append([k, t, c["x0"], c["x1"]])
    for d in drawings:
        r = d["rect"]
        if line["base"] - 12 <= r.y0 <= line["base"] + 3 and 1 < r.width < 60:
            toks.append(["NUM", "⌐", r.x0, r.x1])     # numeral sign drawn as a path (10, 100 ...)
    toks.sort(key=lambda t: t[2])
    # line number: trailing digits (after the text) at far right
    lineno = ""
    while toks and toks[-1][0] in ("D", "DH", "S"):
        k, t, *_ = toks.pop()
        if k in ("D", "DH"):
            lineno = t + lineno
    for t in toks:                      # remaining Hebrew-font digits are numeral signs ("3" = 20-sign)
        if t[0] == "DH":
            t[0] = "NUM"
    L = ("D", "G", "NUM")
    def is_ltr(i):
        return toks[i][0] in L
    def glue(i):   # neutral/space that sits between two LTR tokens, or bracket adjacent to one
        k, t = toks[i][0], toks[i][1]
        prev = next((j for j in range(i - 1, -1, -1) if toks[j][0] != "S"), None)
        nxt = next((j for j in range(i + 1, len(toks)) if toks[j][0] != "S"), None)
        if k == "S":
            return prev is not None and nxt is not None and is_ltr(prev) and is_ltr(nxt) \
                and toks[prev][0] == toks[nxt][0] == "NUM"
        if k == "N" and t in "({":
            return i + 1 < len(toks) and toks[i + 1][0] in ("D", "G")
        if k == "N" and t in ")}":
            return i > 0 and toks[i - 1][0] in ("D", "G")
        return False
    segs, i, n = [], 0, len(toks)
    while i < n:
        if is_ltr(i) or (toks[i][0] == "N" and glue(i)):
            j = i
            while j < n and (is_ltr(j) or glue(j)):
                j += 1
            seg = "".join(t[1] for t in toks[i:j])
            if any(t[0] == "NUM" for t in toks[i:j]):
                seg = "‹" + seg.strip() + "›"
            segs.append(("L", seg))
            i = j
        else:
            j = i
            while j < n and not (is_ltr(j) or (toks[j][0] == "N" and glue(j))):
                j += 1
            s = "".join(MIRROR.get(t[1], t[1]) if t[0] == "N" else t[1] for t in reversed(toks[i:j]))
            segs.append(("R", s))
            i = j
    logical = "".join(s for _, s in reversed(segs))
    logical = re.sub(r"\s+", " ", logical).strip()
    return lineno, logical


if __name__ == "__main__":
    res = []
    for g in range(234, 243):
        p = page(g)
        lines, dr = hebrew_block(p)
        for ln in lines:
            no, txt = decode_line(ln, dr)
            res.append(dict(global_page=g, printed=g - 26, base=round(ln["base"], 1), lineno=no, text=txt))
            print(g, g - 26, no.rjust(3), "|", txt)
    json.dump(res, open(f"{S}/puech_heb_raw.json", "w"), ensure_ascii=False, indent=1)
