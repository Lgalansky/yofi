# Real Money build, step 20 (after rmv16.py): landing page category tiles = the Final categories,
# each showing its next Final time and the expected prize pool. Replaces the Skill tiles (Family, Home, Baking...).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA('<div id="caSched"></div>', '<div id="caFin" class="ca-fin"></div>')
s = s.replace("function fcNotify() {", r"""function finFor(k) { const cur = ppSlot(); for (let sl = cur + 1; sl <= cur + 6; sl++) if (ppGame(sl).k === k) return sl; return cur + 1; }
function caFinHTML() { const img = c => { const t = document.querySelector(`#landing .ca-grid .ca-t[onclick*="'${c}'"] img`); return t ? t.src : ''; };
  return `<p class="caf-h">Next Finals · tap one to add your photo</p><div class="caf-g">${SHOW_ROT.map(x => ({ k: x.k, sl: finFor(x.k) })).sort((a, b) => a.sl - b.sl).map(x => { const h = showHint(x.k), c = h.cats[0], src = img(x.k === 'pets' ? 'pets' : x.k === 'garden' ? 'fitness' : 'night');
    return `<button class="ca-t caf-t" data-caf="${c}">${src ? `<img src="${src}" alt="">` : ''}<span><b>${SHOW_IC[x.k] || ''} ${esc(showName(x.k))}</b><small>Final at <b>${raceName(x.sl)}</b></small><em>${ppPool(ppGame(x.sl).players)} pool</em></span></button>`; }).join('')}</div>`; }
setInterval(() => { try { const el = document.getElementById('caFin'); if (!el || !S || $('#landing').style.display === 'none') return; const h = caFinHTML(); if (el.dataset.h !== h) { el.dataset.h = h; el.innerHTML = h; } } catch (e) {} }, 1000);
document.addEventListener('click', e => { const t = e.target.closest('[data-caf]'); if (!t) return; e.preventDefault(); window.__preCat = t.dataset.caf; yWL(); }, true);
function fcNotify() {""", 1)
s = s.replace('</style>', """#landing .ca-grid{display:none!important}.ca-fin{margin:4px 0 6px}.caf-h{font-size:.74rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;opacity:.75;margin:0 0 8px;text-align:center}
.caf-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.caf-t span{display:flex!important;flex-direction:column;align-items:flex-start!important;gap:2px;padding:8px 9px 9px!important;font:inherit!important}
.caf-t span>b{font:800 .92rem Fraunces,Georgia,serif;line-height:1.15}.caf-t small{font-size:.74rem;opacity:.85}.caf-t em{font-style:normal;font-weight:900;font-size:.86rem;color:#2F6B3F}html.yg .caf-t em{color:#21C77A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v17 ok')
