"""Check the strongest forward-audit other_frag flags: does SQE's own text for the
linked text fragment equal the linked ETCBC fragment (then the photo really shows
other text) or the hit fragment (then SQE and ETCBC number columns differently)?
Output: data/audit/colcheck.json"""
import json, sys, collections
sys.path.insert(0, 'src')
from sqe_harvest import get
from align_self import semiglobal, fold
f = json.load(open('data/audit/forward_flags.json'))
pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
et = collections.defaultdict(str)
for s_, fr, l, t, mk in json.load(open('data/m0/etcbc_lines.json')):
    et[(s_, fr)] += ''.join(c for c, k in zip(t, mk) if k in '.u' and c != ' ')
def sqe_text(eid, tf):
    s = ''
    for ln in get(f'/editions/{eid}/text-fragments/{tf}/lines')['lines']:
        d = get(f'/editions/{eid}/lines/{ln["lineId"]}')
        for sg in d['signs']:
            si = sg['signInterpretations'][0]
            at = {(a['attributeString'], a['attributeValueString']) for a in si['attributes']}
            if ('sign_type', 'LETTER') in at and si['character'] and not any(k == 'is_reconstructed' and v == 'TRUE' for k, v in at):
                s += si['character']
    return s
def sim(a, b):
    a, b = fold(a[:60]), fold(b)
    if not a or not b: return None
    e, _, _ = semiglobal(a, b); return round(1 - e / len(a), 2)
strong = [r for r in f if r['verdict2'] == 'other_frag' and r.get('evidence') and r['full_hits'][0][0] >= 100]
res = []
for r in strong:
    tf = inv[r['name']]['text_fragments'][0]
    sq = sqe_text(tf['edition'], tf['text_fragment'])
    sc, frag = r['full_hits'][0][2].split(' ', 1); frag = frag.split(':')[0]
    linked = tuple(r['links'][0][:2])
    a, b = sim(sq, et[linked]), sim(sq, et[(sc, frag)])
    verdict = 'numbering (SQE text = hit fragment)' if (b or 0) > (a or 0) + 0.2 else 'catalogue (SQE text = linked fragment)' if (a or 0) > (b or 0) + 0.2 else 'unclear'
    res.append(dict(name=r['name'], sqe_tf=tf['tf_name'], linked=' '.join(linked), hit=f'{sc} {frag}', sqe_letters=len(sq), sim_linked=a, sim_hit=b, verdict=verdict))
    print(res[-1], flush=True)
json.dump(res, open('data/audit/colcheck.json', 'w'), ensure_ascii=False, indent=1)
