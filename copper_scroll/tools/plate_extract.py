"""Extract the 3Q15 column plates from Puech 2006 vol. II at native resolution.

The PDFs are the local copies in the repository root
("Le Rouleau de Cuivre ... Puech-{part}.pdf"). Output goes to a scratch
directory given on the command line. The images are copyrighted plates
(Puech / EDF / Brill): never commit the output to git.

Plate series used (plate numbers read from each page's caption):
  radio   CCCXXXIII-CCCLVI   radiographs, two plates per column  (part 10)
  galvA   CCCLIX-CCCLXXXI    colour photograph of the galvanoplastic copy (odd plates)
  fac     CCCLX-CCCLXXXII    Puech's facsimile drawing (even plates; editorial, not for blind reading)
  galvB   CCXCVI-CCCVII      second photograph of the galvanoplastic copy (part 9)

    python copper_scroll/tools/plate_extract.py OUTDIR [COL ...]

Writes, per column: {col}_{kind}_{k}.png (each embedded image at native size) and,
for the radiographs, {col}_radio1_page.png / {col}_radio2_page.png (the whole
plate rendered at scale 2.08 and cropped to the image area, so that overlapping
strips keep their printed arrangement). tools/plate_check_items.py cuts the
blind line crops from these files.
"""
import glob, os, sys
import pypdfium2 as pdfium
import pypdfium2.raw as raw

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SCALE = 2.08   # radiograph page render scale used for the plate check
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII',
         9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'}


def pages(col):
    """(kind, part, page index, plate number) for one column."""
    p = []
    base = 23 + 2 * (col - 1)                       # radiographs: part 10, pp. 23-46
    p += [('radio1', 10, base, 333 + 2 * (col - 1)), ('radio2', 10, base + 1, 334 + 2 * (col - 1))]
    g = 51 + 2 * (col - 1)                          # galvanoplasty photo + facsimile
    if g <= 69:
        p.append(('galvA', 10, g, 359 + 2 * (col - 1)))
    else:
        p.append(('galvA', 11, g - 70, 359 + 2 * (col - 1)))
    f = g + 1
    p.append(('fac', 10, f, 360 + 2 * (col - 1)) if f <= 69 else ('fac', 11, f - 70, 360 + 2 * (col - 1)))
    p.append(('galvB', 9, 50 + col - 1, 296 + col - 1))
    return p


def pdf(part):
    return pdfium.PdfDocument(glob.glob(os.path.join(ROOT, f'Le Rouleau*-{part}.pdf'))[0])


def roman(n):
    vals = [(100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    s = ''
    for v, r in vals:
        while n >= v:
            s += r; n -= v
    return s


def main():
    out = sys.argv[1]
    cols = [int(c) for c in sys.argv[2:]] or list(range(1, 13))
    os.makedirs(out, exist_ok=True)
    docs = {}
    for col in cols:
        for kind, part, idx, plate in pages(col):
            d = docs.setdefault(part, pdf(part))
            page = d[idx]
            text = ''.join(page.get_textpage().get_text_range().split())
            assert f'Planche{roman(plate)}' in text.replace('PLANCHE', 'Planche'), (col, kind, plate, text[:80])
            objs = [o for o in page.get_objects(max_depth=3) if o.type == raw.FPDF_PAGEOBJ_IMAGE]
            objs.sort(key=lambda o: o.get_bounds()[0])     # left to right on the page
            for k, o in enumerate(objs):
                img = o.get_bitmap(render=False).to_pil()
                name = f'{col:02d}_{kind}_{k}.png'
                img.save(os.path.join(out, name))
                print(name, f'pl. {roman(plate)}', img.size, [round(v) for v in o.get_bounds()])
            if kind.startswith('radio'):
                W, H = page.get_size()
                b = [o.get_bounds() for o in objs]
                l, r = min(x[0] for x in b), max(x[2] for x in b)
                bot, top = min(x[1] for x in b), max(x[3] for x in b)
                full = page.render(scale=SCALE).to_pil()
                box = (int(l * SCALE), int((H - top) * SCALE), int(r * SCALE), int((H - bot) * SCALE))
                full.crop(box).save(os.path.join(out, f'{col:02d}_{kind}_page.png'))


if __name__ == '__main__':
    main()
