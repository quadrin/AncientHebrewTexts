"""M3 check: sheet of line crops with their labels, for inspection by eye (local only).

Usage: python3 src/line_sheet.py TIER N SEED OUT [MANIFEST]
"""
import json, random, sys
from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
SMALL = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

if __name__ == '__main__':
    tier, n, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    man = [json.loads(l) for l in open(sys.argv[5] if len(sys.argv) > 5 else 'data/m3/manifest.jsonl')]
    rs = [r for r in man if r['tier'] == tier and r['letters'] >= 3]
    random.seed(seed)
    rs = random.sample(rs, n)
    W, rowh = 900, 120
    sheet = Image.new('L', (W, rowh * n), 0)
    d = ImageDraw.Draw(sheet)
    for k, r in enumerate(rs):
        im = Image.open(f'data/m3/lines/{r["id"]}.png')
        s = min(70 / im.height, (W - 10) / im.width)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
        y = k * rowh
        sheet.paste(im, (W - im.width - 5, y + 2))
        # PIL (with raqm) applies right-to-left layout itself
        d.text((W - 5, y + 76), r['label'], font=FONT, fill=255, anchor='ra')
        d.text((5, y + 80), f'{r["id"]} {r["manuscript"]} l.{r["line"]} misfit {r["width_misfit"]}', font=SMALL, fill=160)
    sheet.save(out, quality=90)
    json.dump(rs, open(out + '.json', 'w'), ensure_ascii=False)
