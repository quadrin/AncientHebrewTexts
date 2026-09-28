"""Build an offline source-plan comparison from the candidate register (stdlib only)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'research/entry21_candidates.json').read_text())

def marks(plan):
    out=[]
    for candidate in data['candidates']:
        for point in candidate['positions']:
            if point['plan'] != plan: continue
            x,y=point['x'],point['y']
            out.append(f'<g class="mark" data-id="{candidate["id"]}" role="button" tabindex="0" aria-label="Select candidate {candidate["id"]}"><circle class="halo" cx="{x}" cy="{y}" r="19"/><circle class="dot" cx="{x}" cy="{y}" r="8"/><text x="{x}" y="{y+4}">{candidate["id"]}</text></g>')
    return ''.join(out)

ilan=f'''<svg viewBox="0 0 650 300" aria-labelledby="ilan-title" role="img"><title id="ilan-title">Ilan–Amit upstream plan: intake A, branch C, long tunnel D</title>
<g transform="translate(-120 -1080)">
<path class="basin" d="M160 1220 Q140 1245 169 1280 L215 1285 241 1258 234 1214Z"/>
<path class="reconstruction" d="M234 1214 L250 1268"/>
<path class="channel" d="M253 1200 L272 1209 295 1212 305 1220 330 1235 348 1249 360 1241 376 1255 385 1271 401 1268 410 1263 433 1263 450 1255 472 1271 498 1252 552 1215 574 1172 605 1147"/>
<path class="channel" d="M305 1220 L318 1247 335 1262 355 1243"/>
<path class="tunnel" d="M356 1244 L364 1243 M401 1268 L433 1263"/>
<text class="annotation" x="162" y="1250">Basin 2</text>
<text class="annotation" x="210" y="1314">Proposed dam 4</text>
<path class="leader" d="M263 1298 L245 1257"/>
<text class="annotation" x="470" y="1150">To cliff channel</text>
{marks('ilan1989')}</g>
<path class="scale" d="M422 263 H602 M422 259 V267 M602 259 V267"/><text class="annotation" x="484" y="287">≈ 50 m</text>
<path class="scale" d="M600 76 V28 L594 40 M600 28 L606 40"/><text class="annotation" x="594" y="20">N</text></svg>'''
reeder=f'''<svg viewBox="0 0 650 330" aria-labelledby="reeder-title" role="img"><title id="reeder-title">Reeder–Jol upstream plan: collection works and rock B, short tunnel C and long tunnel D</title>
<g transform="translate(-40 -800) scale(1.45)">
<path class="basin" d="M68 570 Q95 564 124 580 L100 602 Q69 608 63 593Z M68 608 Q53 633 64 650 L80 659 91 646 85 628 98 607Z"/>
<path class="channel" d="M94 585 L90 615 70 627 70 648 92 653 130 661 151 665 176 668 187 677 206 689 217 701 233 694 254 701 268 700 302 713 325 694 347 677 384 665 390 641 400 600"/>
<path class="reconstruction" d="M151 665 L155 684 171 706 204 719 244 723 262 714 268 700"/>
<path class="tunnel" d="M179 668 L194 685 M218 701 L234 695 256 702"/>
<path class="wall" d="M79 601 L102 604"/>
<circle class="rock" cx="74" cy="650" r="8"/>
<circle class="rock" cx="94" cy="638" r="6"/>
<text class="annotation" x="139" y="587">Collection works</text>
<text class="annotation" x="133" y="611">Stone wall / dam</text>
<path class="leader" d="M125 606 L101 604"/>
<text class="annotation" x="118" y="640">Pothole</text>
<text class="annotation" x="301" y="622">To slumps</text>
{marks('reeder2006')}</g>
<path class="scale" d="M350 285 H600.85 M350 281 V289 M600.85 281 V289"/><text class="annotation" x="453" y="310">≈ 50 m</text>
<path class="scale" d="M600 76 V28 L594 40 M600 28 L606 40"/><text class="annotation" x="594" y="20">N</text></svg>'''
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Entry 21 · The head of the conduit</title>
<style>
:root{color-scheme:light;--ink:#342920;--muted:#6b5949;--paper:#f1e7d2;--copper:#9a4528;--blue:#446b75}*{box-sizing:border-box}body{margin:0;background:#302a24;color:var(--ink);font:16px/1.55 system-ui,sans-serif}main{max-width:1440px;margin:28px auto;background:var(--paper);padding:clamp(20px,4vw,56px);box-shadow:0 12px 55px #0007;border:1px solid #b5a282}h1{font:clamp(32px,4vw,52px)/1.1 Georgia,serif;margin:10px 0 18px}h2{font:24px Georgia,serif;margin:0 0 12px}.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--copper);font-weight:700}.intro{max-width:820px}.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:24px 0}select,button{font:inherit;border:1px solid #9c876f;background:#faf4e7;color:var(--ink);padding:10px 14px;border-radius:4px}button{cursor:pointer}button[aria-pressed=true]{background:var(--ink);color:#fff6e7}a{color:#75371f}#candidates{display:flex;flex-wrap:wrap;gap:8px}.maps{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:24px 0}.plan{min-width:0;background:#fbf6e9;border:1px solid #b9a489;padding:16px;box-shadow:inset 0 0 22px #94795314}.plan p{font-size:13px;color:var(--muted);margin:8px 0 0}svg{width:100%;height:auto;display:block;overflow:visible}.channel{fill:none;stroke:#5c645c;stroke-width:3;stroke-linejoin:round}.tunnel{fill:none;stroke:#343a35;stroke-width:9}.reconstruction{fill:none;stroke:#947953;stroke-width:2;stroke-dasharray:6 4}.basin{fill:#d6e2dd;stroke:#81948c;stroke-width:1.5}.wall{fill:none;stroke:#615647;stroke-width:5}.rock{fill:#c3af90;stroke:#786c59}.annotation{font:14px system-ui;fill:#554a3d}.leader,.scale{fill:none;stroke:#766957;stroke-width:1}.mark{cursor:pointer}.halo{fill:#c55a26;fill-opacity:0;stroke:none}.dot{fill:#f6e6c7;stroke:#9a4528;stroke-width:1.5}.mark text{font:bold 11px system-ui;text-anchor:middle;fill:#79361e;pointer-events:none}.mark.active .halo{fill-opacity:.25}.mark.active .dot{fill:#9a4528}.mark.active text{fill:#fff}.mark:focus{outline:none}.mark:focus .halo{stroke:#263f47;stroke-width:2}.detail{border-top:2px solid #aa7656;border-bottom:1px solid #b6a087;padding:24px 0;margin:24px 0;display:grid;grid-template-columns:1fr 2fr;gap:30px}dl{margin:0}dt{font-weight:650;margin-top:12px}dt:first-child{margin-top:0}dd{margin:3px 0 0}.meta{font-size:13px;color:var(--muted)}.legend{display:flex;gap:22px;flex-wrap:wrap;font-size:13px;color:var(--muted)}.line{display:inline-block;width:30px;border-top:3px solid #5c645c;vertical-align:middle;margin-right:6px}.line.dashed{border-top:2px dashed #947953}.line.bold{border-top:7px solid #343a35}.foot{font-size:14px;max-width:1050px}details{margin-top:20px}summary{cursor:pointer;font-weight:600}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #446b75;outline-offset:3px}@media(max-width:800px){main{margin:0}.maps,.detail{grid-template-columns:1fr}.detail{gap:10px}}@media(max-width:440px){.plan{padding:10px}.maps{margin-left:-8px;margin-right:-8px}.annotation{font-size:19px}.mark text{font-size:15px}.dot{r:11px}.halo{r:23px}}
</style></head><body><main>
<div class="eyebrow">Copper Scroll · Research comparison · 28 September 2026</div>
<h1>The head of the conduit</h1>
<p class="intro">Four specific candidates for entry 21, conditional on Sekakah being Qumran or its wadi. The visible intake leads on function; the upstream boulder leads on the restored stone description. Their precise correspondence is still open.</p>
<div class="controls"><label for="sort">Order</label><select id="sort"><option value="rank">Investigative priority</option><option value="name">Alphabetical</option></select><span class="meta">Exact-feature confidence: low for all four</span></div>
<div id="candidates" aria-label="Select a candidate"></div>
<div class="maps"><section class="plan"><h2>Ilan–Amit · 1989</h2>ILAN_SVG<p>Fig. 1, p. 283 · upstream crop, source-relative redrawing. The long tunnel is point 11; the short tunnel is point 10.</p></section><section class="plan"><h2>Reeder–Jol · 2006</h2>REEDER_SVG<p>Fig. 4, p. 229 · survey of 2002. The long tunnel is Tunnel 1; the short tunnel is Tunnel 2. Different display scale from left panel.</p></section></div>
<div class="legend"><span><i class="line"></i>Channel route</span><span><i class="line bold"></i>Tunnel</span><span><i class="line dashed"></i>Proposed dam / former route</span><span>Shading = selected feature; not a confidence radius</span></div>
<section class="detail" aria-live="polite"><div><div class="eyebrow" id="priority"></div><h2 id="name"></h2><p class="meta" id="source"></p></div><dl><dt>Support</dt><dd id="support"></dd><dt>Unresolved</dt><dd id="limit"></dd><dt>Next discriminating check</dt><dd id="test"></dd></dl></section>
<div class="foot"><p><strong>How to read the match:</strong> C and D appear in both plans because their correspondences are probable. A and B appear only in their own source plan. We have not assumed that the two upstream features occupy the same ground position.</p><details><summary>Reading alternatives and spatial limits</summary><p>If “head” means a branch’s beginning, C becomes more competitive. If “north” describes the aqueduct’s approach to Sekakah, the settlement approach must be tested; the intake’s northern bank is insufficient. If the restored landmark was a monument rather than a stone, B loses its distinctive advantage.</p><p>Paths and points are manually sampled from the publications. Each panel retains its own pixel frame; neither is geographically registered. Scales are approximate reproduction scales, not position-accuracy estimates. Lost or proposed structures remain distinct from surviving observations. The compressed section near Ilan point 18 and Reeder’s settlement inset are excluded.</p><p>The two openings in the long tunnel also deserve comparison with entry 22 under a separate hypothesis that basin 2 is its named reservoir. Their eastern position fits that relation; the reservoir name and ancient context remain unproved.</p></details><p><a href="https://github.com/quadrin/AncientHebrewTexts/blob/main/copper_scroll/entry21_feature_comparison.md">Full comparison, measurements and source notes</a></p></div>
<noscript><p>Candidate selection requires JavaScript. A: visible intake, first priority. B: large rock, second. C: branch and short tunnel, third. D: long tunnel mouth, fourth. All exact-feature matches remain low confidence.</p></noscript>
</main><script>
const data=DATA_JSON;let selected='A';const byId=id=>document.getElementById(id);
function select(id){selected=id;const c=data.candidates.find(c=>c.id===id);for(const key of ['name','support','limit','test'])byId(key).textContent=c[key];byId('priority').textContent=`Candidate ${id} · Priority ${c.rank} · ${c.confidence} feature confidence`;byId('source').textContent=c.sources.join(' · ');document.querySelectorAll('.mark').forEach(el=>{el.classList.toggle('active',el.dataset.id===id);el.setAttribute('aria-pressed',String(el.dataset.id===id))});document.querySelectorAll('#candidates button').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.id===id)))}
function buttons(){const rows=[...data.candidates].sort((a,b)=>byId('sort').value==='name'?a.name.localeCompare(b.name):a.rank-b.rank);byId('candidates').replaceChildren(...rows.map(c=>{const b=document.createElement('button');b.type='button';b.dataset.id=c.id;b.textContent=`${c.id} · ${c.name}`;b.onclick=()=>select(c.id);return b}));select(selected)}
byId('sort').onchange=buttons;document.querySelectorAll('.mark').forEach(el=>{el.onclick=()=>select(el.dataset.id);el.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(el.dataset.id)}}});buttons();
</script></body></html>'''
html=html.replace('ILAN_SVG',ilan).replace('REEDER_SVG',reeder).replace('DATA_JSON',json.dumps(data,ensure_ascii=False).replace('<','\\u003c'))
out=ROOT/'public/research/entry21-comparison.html'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(html)
print(out)
