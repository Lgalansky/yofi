# Skill preview: choose your next collection.
#  When a collection reaches Gold (3 photos at 70+), the celebration pop says "Pick any collection
#  to open next" and its button is "Choose your next collection". That opens a picker with every
#  locked collection; each shows "4 of your photos fit" (sorted so the ones you can fill come first).
#  Picking one moves it into the next spot on the path and plays the usual map unlock reveal.
#  If you close the pop, the choice waits: the map's button becomes "Choose your next collection"
#  and tapping any locked stop opens the picker. The chosen order is saved (S.galPath).
#  Tapping a locked category in the Gallery opens the map (or the picker when a choice is waiting).
# usage: python3 build-skill/choose.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- choose your next collection ----
(() => { const P = S.galPath; if (Array.isArray(P) && P.length === GAL.PATH.length && P.every(c => GAL.PATH.includes(c))) GAL.PATH.splice(0, GAL.PATH.length, ...P); })();
const chFits = c => S.photos.filter(p => p.s && p.cat === c).length;
const chPending = () => { const c = S.galPick; if (!c || !GAL.PATH.includes(c)) return null; if (chFits(c) || galRoom(c).ph.length) { S.galPick = null; save(); return null; } return c; };
function chPicker() { const slot = chPending(); if (!slot) return; const i = GAL.PATH.indexOf(slot);
  const list = GAL.PATH.slice(i).map(c => ({ c, n: chFits(c) })).sort((a, b) => b.n - a.n);
  openSheet(`<div class="pj gs chp"><div class="pj-top"><span class="pj-t">🗺 Your next collection</span><button class="pj-x" data-shclose aria-label="Close">✕</button></div>
    <p class="gs-what">Get 3 photos to 🥇 Gold to finish it · every photo earns coins per vote</p>
    <div class="chp-grid">${list.map(x => `<button class="chp-t ${x.n ? 'fit' : ''}" data-chc="${x.c}"><span class="chp-ic">${MAP_IC[x.c] || '📷'}</span><b>${esc(galNm(x.c))}</b><small>${x.n ? `${x.n} of your photo${x.n === 1 ? '' : 's'} fit${x.n === 1 ? 's' : ''}` : 'Add new photos'}</small></button>`).join('')}</div></div>`);
  document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
  document.querySelectorAll('#sheetBody [data-chc]').forEach(b => b.onclick = () => chChoose(b.dataset.chc)); }
function chChoose(c) { const slot = S.galPick, i = GAL.PATH.indexOf(slot), j = GAL.PATH.indexOf(c); if (i < 0 || j < 0) return;
  GAL.PATH.splice(j, 1); GAL.PATH.splice(i, 0, c); S.galPath = GAL.PATH.slice(); S.galPick = null; S.galCat = c; save(); closeSheet();
  document.querySelectorAll('#gmap').forEach(e => e.remove()); setTimeout(() => { try { showMap({ unlock: c }); } catch (e) {} try { renderStudio(); } catch (e) {} }, 300); }
const _galCeleCh = galCele;
galCele = function (ev) { const r = _galCeleCh.apply(this, arguments); if (!ev || !ev.opened) return r;
  S.galPick = ev.opened; save(); const p = document.querySelector('#coach .gl-pop p b:last-child'); if (p && /unlocked/.test(p.textContent)) p.textContent = 'Pick any collection to open next.';
  document.querySelectorAll('#coach .gl-pop button').forEach(b => { if (/^See .+ on the map$/.test(b.textContent.trim())) b.textContent = 'See the map'; });
  const g = $('#glpGo'); if (g) { g.textContent = 'Choose your next collection'; g.classList.add('chp-go'); g.onclick = () => { const co = $('#coach'); co.classList.remove('on', 'cr'); co.innerHTML = ''; chPicker(); }; }
  return r; };
// a locked category (gallery tabs, "Next" sleeve) opens the map, or the picker when a choice is waiting
function chLockTap(e) { const b = e.target.closest('#studio [data-gc]'); if (!b || galOpen(b.dataset.gc)) return; e.stopImmediatePropagation(); e.preventDefault();
  if (chPending()) chPicker(); else { try { showMap({}); } catch (x) {} } }
document.addEventListener('click', chLockTap, true);
const _showMapCh = showMap;
showMap = function (o) { const r = _showMapCh.apply(this, arguments); const slot = chPending(); const el = $('#gmap'); if (!el) return r;
  const sb = el.querySelector('.gm-sub'); if (sb && /open the next/.test(sb.textContent)) sb.innerHTML = sb.innerHTML.replace('open the next', 'choose the next');
  if (!slot) return r;
  const sub = el.querySelector('.gm-sub'); if (sub) sub.innerHTML = 'Collection finished! <b>Pick any locked stop</b> to open it next';
  const go = el.querySelector('.gm-go'); if (go) { go.textContent = 'Choose your next collection'; go.onclick = () => chPicker(); }
  const i = GAL.PATH.indexOf(slot); el.querySelectorAll('.gm-n[data-mc]').forEach(n => { if (GAL.PATH.indexOf(n.dataset.mc) >= i) { n.classList.add('chp-pick'); n.onclick = e => { e.stopPropagation(); chPicker(); }; } });
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* choose your next collection */
html body #coach .gl-pop #glpGo.chp-go{background:#2D4E86!important;color:#fff!important;box-shadow:0 8px 18px -8px rgba(45,78,134,.7)!important}
.chp-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0 4px}
.chp-t{display:flex;flex-direction:column;align-items:center;gap:2px;padding:14px 8px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;font-family:inherit;cursor:pointer}
.chp-t.fit{background:#FFF3D6;box-shadow:inset 0 0 0 2px #E0A82E}
.chp-ic{font-size:2.2rem;line-height:1.1}.chp-t b{font:900 1.1rem Fraunces,serif;color:#2D2521}.chp-t small{font:700 .78rem "Nunito Sans";color:#4E433C;white-space:nowrap}.chp-t.fit small{color:#8A5A0A;font-weight:800}
#gmap .gm-n.chp-pick .gm-d{box-shadow:0 0 0 3px #E0A82E,0 0 18px rgba(224,168,46,.6);animation:chpPulse 1.6s ease-in-out infinite}
@keyframes chpPulse{50%{box-shadow:0 0 0 5px #F3D27A,0 0 26px rgba(224,168,46,.8)}}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('choose ok')
