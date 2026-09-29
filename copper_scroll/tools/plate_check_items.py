"""Cut the blind plate-check crops (P01-P30) from the output of plate_extract.py.

For each code in registration/plate_check/key.json, writes three images:
  Pxx_A.png  the galvanoplastic-copy photograph band (copy plate)
  Pxx_B.png  the first radiograph plate band
  Pxx_C.png  the second radiograph plate band
with green triangles marking the target line in both margins. The crops are
copyrighted plate material: keep them outside git.

    python copper_scroll/tools/plate_check_items.py PLATEDIR OUTDIR
"""
import json, os, sys
from PIL import Image, ImageDraw

KEY = os.path.join(os.path.dirname(__file__), '..', 'registration', 'plate_check', 'key.json')
M = 36          # margin carrying the triangles
K = 1.25        # line-spacings kept above and below the target


def band(path, y, sp):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    a, b = max(0, int(y - K * sp)), min(H, int(y + K * sp))
    c = im.crop((0, a, W, b))
    out = Image.new('RGB', (W + 2 * M, c.size[1]), 'white')
    out.paste(c, (M, 0))
    d, yy = ImageDraw.Draw(out), y - a
    d.polygon([(4, yy - 12), (4, yy + 12), (M - 4, yy)], fill=(0, 170, 0))
    d.polygon([(W + 2 * M - 4, yy - 12), (W + 2 * M - 4, yy + 12), (W + M + 4, yy)], fill=(0, 170, 0))
    return out


def main():
    plates, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for code, it in json.load(open(KEY))['items'].items():
        col = it['column']
        band(os.path.join(plates, f'{col:02d}_galvA_0.png'), it['copy_centre_y'], it['copy_line_spacing']).save(os.path.join(out, f'{code}_A.png'))
        band(os.path.join(plates, f'{col:02d}_radio1_page.png'), it['radio1_centre_y'], it['radio_line_spacing']).save(os.path.join(out, f'{code}_B.png'))
        band(os.path.join(plates, f'{col:02d}_radio2_page.png'), it['radio2_centre_y'], it['radio_line_spacing']).save(os.path.join(out, f'{code}_C.png'))
        print(code, it['line'])


if __name__ == '__main__':
    main()
