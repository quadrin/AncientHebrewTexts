"""M3 cleaning step: per-line CTC loss with a trained model; drop the worst lines.

Usage: python3 src/ctc_clean.py MODEL OUT_DIR [DROP_FRACTION]
Writes OUT_DIR/line_loss.json ({id: loss per label symbol}) and
OUT_DIR/exclude.json (ids of the worst DROP_FRACTION of train lines), and
prints how the loss relates to tier, width misfit and editor uncertainty.
"""
import json, os, sys, collections
import numpy as np, torch

sys.path.insert(0, os.path.dirname(__file__))
from train import Lines, collate, Bucket, CRNN, H, select, evaluate  # noqa: E402
import cv2  # noqa: E402

if __name__ == '__main__':
    model_path, out = sys.argv[1], sys.argv[2]
    frac = float(sys.argv[3]) if len(sys.argv) > 3 else 0.15
    torch.set_num_threads(2)
    man = [json.loads(l) for l in open('data/m3/manifest.jsonl')]
    split = json.load(open('reports/M4_split.json'))
    tr = select(man, split, 'train', 'AB', False)
    w = []
    for r in tr:
        h, ww = cv2.imread(f'data/m3/lines/{r["id"]}.png', 0).shape
        w.append(ww * H / h)
    ld = torch.utils.data.DataLoader(Lines(tr, False), batch_sampler=Bucket(w, 32, False), collate_fn=collate)
    m = CRNN()
    m.load_state_dict(torch.load(model_path, map_location='cpu'))
    cer, cer_ns, losses = evaluate(m, ld, tr)
    json.dump(losses, open(f'{out}/line_loss.json', 'w'))
    ids = sorted(losses, key=lambda k: -losses[k])
    drop = ids[:int(frac * len(ids))]
    json.dump(drop, open(f'{out}/exclude.json', 'w'))
    by = {r['id']: r for r in tr}
    print(f'train lines {len(tr)}, train CER (no augmentation) {cer:.3f}; dropping {len(drop)} '
          f'(loss >= {losses[drop[-1]]:.2f}), {sum(by[i]["letters"] for i in drop)} letters')
    for key, f in [('tier', lambda r: r['tier']),
                   ('misfit>0.3', lambda r: r['width_misfit'] > 0.3),
                   ('uncertain share>0.3', lambda r: r['uncertain'] / max(r['letters'], 1) > 0.3),
                   ('letters<=3', lambda r: r['letters'] <= 3)]:
        g = collections.defaultdict(list)
        for i, l in losses.items():
            g[f(by[i])].append(l)
        dropped = collections.Counter(f(by[i]) for i in drop)
        print(key, {k: dict(n=len(v), median_loss=round(float(np.median(v)), 3),
                             dropped=round(dropped[k] / len(v), 3)) for k, v in sorted(g.items(), key=str)})
