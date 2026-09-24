"""M7: write the review queue (reports/M7_queue.md) from data/m7/results.json.

Each entry: image name and IAA plate/fragment, the local crop path (the crop
itself is never committed), the reading with per-position probabilities, the
top hits with their passage text, the score, p and E.
Usage: python3 src/m7_queue.py [N] [notes.json]
"""
import json, sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
notes = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}


def passages():
    mt = {ref: t for ref, t in json.load(open('data/ref/bible.json'))}
    dss = {}
    for s, f, l, t, m, _ in json.load(open('data/ref/dss_lines.json')):
        # show preserved letters plain, reconstructed ones in [brackets]
        out, inr = '', False
        for c, k in zip(t, m):
            if k == 'r' and not inr:
                out += '['; inr = True
            elif k != 'r' and inr and c != ' ':
                out += ']'; inr = False
            out += c
        dss[f'{s} {f}:{l}'] = out + (']' if inr else '')
    return mt, dss


def fmt_probs(line):
    cells = []
    for d in line['probs']:
        top = sorted(d.items(), key=lambda kv: -kv[1])[:3]
        cells.append('/'.join(f'{c}{p:.2f}' for c, p in top if p >= 0.05))
    return ' · '.join(cells)


if __name__ == '__main__':
    R = json.load(open('data/m7/results.json'))
    rd = json.load(open('data/m7/readings.json'))
    inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
    mt, dss = passages()
    L = ['# M7 review queue', '',
         f'{len(R)} fragments matched (of {len(rd)} read; the rest had fewer than 10 letters read). '
         'Sorted by p. E = p × fragments matched: treat E < 0.1 as a lead, E ≈ 1 as noise. '
         'Every entry is a lead for a specialist, not a finding. Crops are local only '
         '(Leon Levy images © IAA); paths are given for the reviewer.', '']
    for k, r in enumerate(R[:N], 1):
        x = inv[r['name']]
        L.append(f'## {k}. {r["name"]} ({r["manuscript"]}, IAA plate {x["plate"]} frag. {x["frag"]}) — p = {r["p"]:.4f}, E = {r["E"]:.2f}')
        L.append('')
        if r['name'] in notes:
            L.append(f'**Reviewer note:** {notes[r["name"]]}')
            L.append('')
        L.append(f'- Crop (local): `data/m7/crops/{r["name"]}.jpg`; {r["read_letters"]} letters read on {r["read_lines"]} lines')
        L.append('- Reading (top to bottom; per position the top letters with probability):')
        for l in rd[r['name']]:
            if l['probs']:
                L.append(f'  - `{l["text"]}` — {fmt_probs(l)}')
        L.append('- Top hits:')
        for s, d, ref, o in r['hits'][:3]:
            txt = mt.get(ref) if d.startswith('MT') else dss.get(ref, '')
            L.append(f'  - {s:.1f} {ref}: {txt}')
        L.append('')
    open('reports/M7_queue.md', 'w').write('\n'.join(L) + '\n')
    print('wrote', min(N, len(R)), 'entries')
