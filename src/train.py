"""M4: line-level CTC recogniser (small CRNN, CPU).

Data: data/m3/manifest.jsonl + data/m3/lines/*.png, split from reports/M4_split.json.
Labels are stored in reading order (right to left); the network reads the
image left to right, so labels are reversed for training and decoding.
Pixels equal to 0 lie outside the parchment mask; they are filled with the
line's parchment tone so fragment edges do not look like ink.

Usage: python3 src/train.py [--epochs N] [--out data/m4/run1] [--tiers AB] [--gaps]
"""
import argparse, json, math, os, random, time
import numpy as np, cv2, torch, torch.nn as nn, torch.nn.functional as F

H = 64
MAXW = 1200
ALPHABET = ' אבגדהוזחטיכךלמםנןסעפףצץקרשת'   # index + 1; 0 is the CTC blank
C2I = {c: i + 1 for i, c in enumerate(ALPHABET)}


# ------------------------------------------------------------------ data
def load_line(path):
    g = cv2.imread(path, 0)
    if g is None or g.size == 0:
        return None
    inside = g > 0
    fill = np.median(g[inside]) if inside.any() else 200
    g = np.where(inside, g, fill).astype(np.uint8)
    s = H / g.shape[0]
    w = int(min(MAXW, max(8, round(g.shape[1] * s))))
    return cv2.resize(g, (w, H), interpolation=cv2.INTER_AREA)


def augment(g, rnd):
    g = g.astype(np.float32)
    # ink fade / contrast / brightness
    a, b = rnd.uniform(0.6, 1.3), rnd.uniform(-30, 30)
    g = (g - g.mean()) * a + g.mean() + b
    # stroke thickness
    if rnd.random() < 0.4:
        k = np.ones((rnd.choice([2, 3]),) * 2, np.uint8)
        g = cv2.dilate(g, k) if rnd.random() < 0.5 else cv2.erode(g, k)   # dilate = thinner ink
    # blur / noise
    if rnd.random() < 0.3:
        g = cv2.GaussianBlur(g, (0, 0), rnd.uniform(0.5, 1.5))
    g = g + rnd.normal(0, rnd.uniform(0, 8), g.shape)
    # holes: dark blobs like wormholes and dirt, or bright patches like flaking
    for _ in range(rnd.integers(0, 3)):
        cx, cy = rnd.integers(0, g.shape[1]), rnd.integers(0, H)
        r = int(rnd.integers(3, 12))
        cv2.circle(g, (int(cx), int(cy)), r, float(rnd.choice([10, 235])), -1)
    # small rotation / shear / vertical shift
    if rnd.random() < 0.5:
        M = np.float32([[1, rnd.uniform(-0.15, 0.15), 0], [rnd.uniform(-0.03, 0.03), 1, rnd.uniform(-4, 4)]])
        g = cv2.warpAffine(g, M, (g.shape[1], H), borderMode=cv2.BORDER_REPLICATE)
    # horizontal scale
    if rnd.random() < 0.5:
        w = max(8, int(g.shape[1] * rnd.uniform(0.8, 1.2)))
        g = cv2.resize(g, (min(w, MAXW), H))
    return np.clip(g, 0, 255)


def encode(label):
    return [C2I[c] for c in reversed(label) if c in C2I]


class Lines(torch.utils.data.Dataset):
    def __init__(self, recs, train):
        self.recs, self.train = recs, train
        self.rnd = np.random.default_rng()
        self.cache = {}

    def __len__(self):
        return len(self.recs)

    def __getitem__(self, i):
        r = self.recs[i]
        if i not in self.cache:
            self.cache[i] = load_line(f'data/m3/lines/{r["id"]}.png')
        g = self.cache[i]
        if self.train:
            g = augment(g, self.rnd)
        x = torch.from_numpy((255.0 - g.astype(np.float32)) / 255.0)   # ink high
        return x, torch.tensor(encode(r['label']), dtype=torch.long), i


def collate(batch):
    W = max(x.shape[1] for x, _, _ in batch)
    W = int(math.ceil(W / 4) * 4)
    xs = torch.zeros(len(batch), 1, H, W)
    for k, (x, _, _) in enumerate(batch):
        xs[k, 0, :, :x.shape[1]] = x
    ys = torch.cat([y for _, y, _ in batch])
    xl = torch.tensor([x.shape[1] // 4 for x, _, _ in batch])
    yl = torch.tensor([len(y) for _, y, _ in batch])
    idx = [i for _, _, i in batch]
    return xs, ys, xl, yl, idx


class Bucket(torch.utils.data.Sampler):
    """Batches of similar width, shuffled."""
    def __init__(self, widths, bs, shuffle=True):
        self.w, self.bs, self.shuffle = widths, bs, shuffle

    def __iter__(self):
        order = np.argsort(np.array(self.w) + (np.random.rand(len(self.w)) * 40 if self.shuffle else 0))
        batches = [order[i:i + self.bs].tolist() for i in range(0, len(order), self.bs)]
        if self.shuffle:
            random.shuffle(batches)
        return iter(batches)

    def __len__(self):
        return math.ceil(len(self.w) / self.bs)


# ------------------------------------------------------------------ model
def block(i, o, pool):
    return nn.Sequential(nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o), nn.ReLU(inplace=True),
                         nn.MaxPool2d(pool) if pool else nn.Identity())


class CRNN(nn.Module):
    def __init__(self, n_out=len(ALPHABET) + 1, hid=192, height=64):
        super().__init__()
        self.cnn = nn.Sequential(
            block(1, 32, (2, 2)),            # 32 x W/2
            block(32, 64, (2, 2)),           # 16 x W/4
            block(64, 128, None), block(128, 128, (2, 1)),     # 8
            block(128, 192, None), block(192, 192, (2, 1)),    # 4
            block(192, 256, (height // 16, 1)),   # 1
            nn.Dropout2d(0.1))
        self.rnn = nn.LSTM(256, hid, num_layers=2, bidirectional=True, batch_first=True, dropout=0.25)
        self.out = nn.Linear(2 * hid, n_out)

    def forward(self, x):
        f = self.cnn(x).squeeze(2).transpose(1, 2)   # B x T x 256
        f, _ = self.rnn(f)
        return self.out(f)                           # B x T x C (logits)


# ------------------------------------------------------------------ decode / metrics
def greedy(logits, lens):
    out = []
    best = logits.argmax(-1)
    for b in range(best.shape[0]):
        seq, prev = [], 0
        for t in range(int(lens[b])):
            k = int(best[b, t])
            if k != prev and k != 0:
                seq.append(k)
            prev = k
        out.append(''.join(ALPHABET[k - 1] for k in seq)[::-1])   # back to reading order
    return out


def edit(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[len(b)]


def evaluate(model, loader, recs):
    model.eval()
    errs = n = 0
    errs_ns = n_ns = 0
    losses = {}
    with torch.no_grad():
        for xs, ys, xl, yl, idx in loader:
            lg = model(xs)
            lp = F.log_softmax(lg, -1).transpose(0, 1)
            l = F.ctc_loss(lp, ys, xl, yl, reduction='none', zero_infinity=True)
            for k, i in enumerate(idx):
                losses[recs[i]['id']] = float(l[k] / max(int(yl[k]), 1))
            for k, hyp in enumerate(greedy(lg, xl)):
                ref = recs[idx[k]]['label']
                errs += edit(hyp, ref)
                n += len(ref)
                a, b = hyp.replace(' ', ''), ref.replace(' ', '')
                errs_ns += edit(a, b)
                n_ns += len(b)
    return errs / max(n, 1), errs_ns / max(n_ns, 1), losses


# ------------------------------------------------------------------ main
def select(man, split, which, tiers, gaps):
    ms = set(split[which])
    return [r for r in man if r['tier'] and r['tier'] in tiers and r['manuscript'] in ms
            and (gaps or not r['has_gap']) and r['letters'] >= 1
            and os.path.exists(f'data/m3/lines/{r["id"]}.png')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--epochs', type=int, default=40)
    ap.add_argument('--out', default='data/m4/run1')
    ap.add_argument('--tiers', default='AB')
    ap.add_argument('--gaps', action='store_true')
    ap.add_argument('--bs', type=int, default=16)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--exclude', default='', help='file with line ids to leave out (CTC cleaning)')
    ap.add_argument('--extra', default='', help='comma-separated extra manifests (e.g. data/m3/manifest_self.jsonl)')
    ap.add_argument('--height', type=int, default=64)
    ap.add_argument('--init', default='', help='start from these weights')
    a = ap.parse_args()
    torch.set_num_threads(4)
    torch.manual_seed(0); random.seed(0); np.random.seed(0)
    os.makedirs(a.out, exist_ok=True)
    global H
    H = a.height
    man = [json.loads(l) for l in open('data/m3/manifest.jsonl')]
    for f in filter(None, a.extra.split(',')):
        man += [json.loads(l) for l in open(f)]
    # one label per band: prefer width-aligned tiers A/B over self-aligned S
    rank = {'A': 0, 'B': 1, 'S': 2}
    best = {}
    for r in man:
        if not r.get('tier'):
            continue
        k = (r['name'], r['band'])
        if k not in best or rank[r['tier']] < rank[best[k]['tier']]:
            best[k] = r
    man = list(best.values())
    if a.exclude:
        drop = set(json.load(open(a.exclude)))
        man = [r for r in man if r['id'] not in drop]
    split = json.load(open('reports/M4_split.json'))
    tr = select(man, split, 'train', a.tiers, a.gaps)
    va = select(man, split, 'val', a.tiers, a.gaps)
    print(f'train {len(tr)} lines / {sum(r["letters"] for r in tr)} letters; '
          f'val {len(va)} lines / {sum(r["letters"] for r in va)} letters', flush=True)

    def widths(recs):
        out = []
        for r in recs:
            h, w = cv2.imread(f'data/m3/lines/{r["id"]}.png', 0).shape
            out.append(w * H / h)
        return out
    dtr, dva = Lines(tr, True), Lines(va, False)
    ltr = torch.utils.data.DataLoader(dtr, batch_sampler=Bucket(widths(tr), a.bs), collate_fn=collate, num_workers=0)
    lva = torch.utils.data.DataLoader(dva, batch_sampler=Bucket(widths(va), 32, False), collate_fn=collate)
    model = CRNN(height=H)
    if a.init:
        model.load_state_dict(torch.load(a.init, map_location='cpu'))
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=1e-4)
    steps = a.epochs * len(ltr)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=a.lr, total_steps=steps, pct_start=0.1)
    best, log = 9.9, []
    for ep in range(a.epochs):
        model.train()
        t0, tot, nb = time.time(), 0.0, 0
        for xs, ys, xl, yl, _ in ltr:
            lp = F.log_softmax(model(xs), -1).transpose(0, 1)
            loss = F.ctc_loss(lp, ys, xl, yl, zero_infinity=True)
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            sched.step()
            tot += float(loss.detach()); nb += 1
        cer, cer_ns, _ = evaluate(model, lva, va)
        rec = dict(epoch=ep + 1, loss=round(tot / nb, 4), val_cer=round(cer, 4), val_cer_letters=round(cer_ns, 4),
                   sec=round(time.time() - t0))
        log.append(rec)
        print(json.dumps(rec), flush=True)
        if cer < best:
            best = cer
            torch.save(model.state_dict(), f'{a.out}/best.pt')
        json.dump(log, open(f'{a.out}/log.json', 'w'))
    torch.save(model.state_dict(), f'{a.out}/last.pt')
    json.dump(dict(args=vars(a), best_val_cer=best, n_train=len(tr), n_val=len(va),
                   train_letters=sum(r['letters'] for r in tr)), open(f'{a.out}/run.json', 'w'))


if __name__ == '__main__':
    main()
