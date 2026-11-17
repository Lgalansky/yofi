# Real Money build, step 27 (after rmv23.py): "Add a photo" / "Enter your photo" first open a "Choose your Final" page
# (the Final categories with their next Final time and prize pool). Tapping one opens the photo picker for that category.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""function finPick() { let o = document.getElementById('finPick'); if (!o) { o = document.createElement('div'); o.id = 'finPick'; document.body.appendChild(o); }
  const first = ffreeFirst(), L = SHOW_ROT.map(x => ({ k: x.k, sl: finFor(x.k) })).sort((a, b) => a.sl - b.sl);
  o.innerHTML = `<div class="fp-in"><button class="fp-x" aria-label="Close">✕</button><p class="fp-k">📷 Enter your photo</p><h2>Choose your Final</h2>
    <p class="fp-s">Pick the category your photo is for. ${first ? 'Your first photo goes <b>straight into that Final</b> once you improve it.' : 'Photos at 70+ enter its qualifiers free; the top 2 go through to the Final.'}</p>
    ${L.map(x => { const g = ppGame(x.sl); return `<button class="fp-c" data-fpk="${x.k}">${lpImg(x.k) ? `<img src="${lpImg(x.k)}" alt="">` : `<span class="fp-e">${SHOW_IC[x.k] || '🎀'}</span>`}<span class="fp-t"><b>${SHOW_IC[x.k] || ''} ${esc(showName(x.k))}</b><small>Next Final <b>${lpWhen(x.sl)}</b></small><em>${ppPool(g.players)} prize pool</em></span><i aria-hidden="true">›</i></button>`; }).join('')}
    <p class="fp-n">Finals every hour: Pets, Nature &amp; landscapes, Garden &amp; flowers.</p></div>`;
  o.className = 'on'; o.querySelector('.fp-x').onclick = () => { o.className = ''; };
  o.querySelectorAll('[data-fpk]').forEach(b => b.onclick = () => { const k = b.dataset.fpk; o.className = ''; window.__preCat = showHint(k).cats[0];
    if ($('#landing').style.display !== 'none' || !$('#app').classList.contains('on')) yWL(); else pickPhoto(true); }); }
const ffreeFirst = () => !S.firstEntry && !S.ffDone && !Object.values(S.rc || {}).some(r => r.st || (r.f && r.f.length));
window.finPick = finPick;
function fcNotify() {""", 1)
RA("function rmEnterOwn() { window.__preCat = null; yWL(); }", "function rmEnterOwn() { finPick(); }")
RA("if ($('#ppUp')) $('#ppUp').onclick = () => { popClose(); S.frameHint = showHint(finNext(1)[0].k); save(); pickPhoto(true); };",
   "if ($('#ppUp')) $('#ppUp').onclick = () => { popClose(); finPick(); };")
RA("$('#msAdd').onclick = () => { S.frameHint = { cats: ['pets'], lab: 'Pets', frame: 'Pets' }; save(); pickPhoto(true); };",
   "$('#msAdd').onclick = () => finPick();")
s = s.replace('</style>', """#finPick{position:fixed;inset:0;z-index:2147483000;background:rgba(43,35,32,.55);display:none;align-items:flex-end;justify-content:center}#finPick.on{display:flex}
#finPick .fp-in{background:#FBF3EA;color:#2B2320;width:100%;max-width:520px;max-height:92vh;overflow:auto;border-radius:24px 24px 0 0;padding:18px 16px 22px;position:relative;box-sizing:border-box}
#finPick .fp-x{position:absolute;right:12px;top:10px;border:0;background:none;font-size:1.4rem;color:#7A1638;cursor:pointer}#finPick .fp-k{margin:0;font-size:.74rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#9A2F4E}
#finPick h2{font:800 1.7rem/1.1 Fraunces,Georgia,serif;color:#7A1638;margin:4px 0 6px}#finPick .fp-s{margin:0 0 12px;font-size:.92rem}
#finPick .fp-c{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;background:#FFFFFF;border-radius:16px;padding:8px;margin:0 0 10px;box-shadow:inset 0 0 0 1px #EADCC6;cursor:pointer;font:inherit;color:inherit}
#finPick .fp-c img{width:84px;height:84px;object-fit:cover;border-radius:12px;flex:none}#finPick .fp-e{width:84px;height:84px;display:flex;align-items:center;justify-content:center;font-size:2.2rem;flex:none}
#finPick .fp-t{flex:1;display:flex;flex-direction:column;gap:2px}#finPick .fp-t>b{font:800 1.12rem Fraunces,Georgia,serif;color:#7A1638}#finPick .fp-t small{font-size:.86rem}#finPick .fp-t em{font-style:normal;font-weight:900;color:#2F6B3F}
#finPick .fp-c i{font-style:normal;font-size:1.6rem;color:#9A2F4E;padding-right:6px}#finPick .fp-n{font-size:.78rem;opacity:.75;text-align:center;margin:4px 0 0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v24 ok')
