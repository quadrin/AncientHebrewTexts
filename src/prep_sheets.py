"""M2 check: contact sheets of segmentation overlays for inspection by eye.

Usage: python3 src/prep_sheets.py N SEED
Picks N random processed images from data/m2/batch_parchment.json and writes
data/m2/sheets/sheet_XX.jpg (4 per sheet, local only) plus sheets.json with
the transcription line counts shown on each tile.
"""
import json, os, random, sys
import numpy as np, cv2

sys.path.insert(0, os.path.dirname(__file__))
import prep  # noqa: E402

D2 = 'data/m2'

if __name__ == '__main__':
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    batch = [b for b in json.load(open(f'{D2}/batch_parchment.json')) if b['detected'] is not None]
    random.seed(seed)
    pick = random.sample(batch, n)
    os.makedirs(f'{D2}/sheets', exist_ok=True)
    tiles = []
    for b in pick:
        path = f'{D2}/sheets/tile_{b["name"]}.jpg'
        prep.overlay(b['name'], path, maxw=600)
        t = cv2.imread(path)
        s = min(600 / t.shape[1], 600 / t.shape[0])
        t = cv2.resize(t, (int(t.shape[1] * s), int(t.shape[0] * s)))
        tile = np.zeros((630, 600, 3), np.uint8)
        tile[30:30 + t.shape[0], :t.shape[1]] = t
        cv2.putText(tile, f'{b["name"]} {b["manuscript"]} exp {b["expected"]} span {b["span"]} det {b["detected"]}',
                    (4, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        tiles.append(tile)
        os.remove(path)
    for i in range(0, len(tiles), 4):
        grp = tiles[i:i + 4] + [np.zeros_like(tiles[0])] * (4 - len(tiles[i:i + 4]))
        sheet = np.vstack([np.hstack(grp[:2]), np.hstack(grp[2:])])
        cv2.imwrite(f'{D2}/sheets/sheet_{i // 4:02d}.jpg', sheet, [cv2.IMWRITE_JPEG_QUALITY, 88])
    json.dump(pick, open(f'{D2}/sheets/sheets.json', 'w'))
    print(len(tiles), 'tiles on', (len(tiles) + 3) // 4, 'sheets')
