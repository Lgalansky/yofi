# One Compete menu (Skill preview): the bottom menu becomes Vote · Compete · Touch-ups.
# Compete has a tab bar at the top: Challenges (today's photo challenges) | Tournaments (the tournament list).
# Each tab shows the same page as before; the separate Tournaments button is hidden.
# Usage: python3 build-skill/compete.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function cmpBar(' in s: sys.exit('compete already applied')

JS = r'''
/* ---------- one Compete menu with Challenges | Tournaments tabs ---------- */
let CMP_TAB = 'ch';
const cmpBar = t => `<div class="cmp-bar" role="tablist" aria-label="Compete"><button role="tab" data-cmp="ch" aria-selected="${t === 'ch'}">🏅 Challenges</button><button role="tab" data-cmp="tour" aria-selected="${t === 'tour'}">🏆 Tournaments</button></div>`;
const _segTourGo = $('#segCompete').onclick;
function cmpOpen(t) {
  CMP_TAB = t;
  if (t === 'tour') { try { _segTourGo(); } catch (e) {} setTimeout(cmpPaint, 30); }
  else { try { closeSheet(); } catch (e) {} if ($('#flow').classList.contains('on')) { try { closeFlow(); } catch (e) {} } openBattleTab(); setTimeout(cmpPaint, 30); }
  $('#segGallery').setAttribute('aria-pressed', 'true'); $('#segCompete').setAttribute('aria-pressed', 'false');
}
function cmpWire(el) { el.querySelectorAll('[data-cmp]').forEach(b => b.onclick = () => cmpOpen(b.dataset.cmp)); }
function cmpPaint() {
  const fl = $('#flow'), fb = $('#flowBody');
  if (CMP_TAB === 'tour' && fl.classList.contains('on') && fb && !fb.querySelector('.cmp-bar')) { fb.insertAdjacentHTML('afterbegin', cmpBar('tour')); cmpWire(fb); $('#segGallery').setAttribute('aria-pressed', 'true'); $('#segCompete').setAttribute('aria-pressed', 'false'); }
  const g = $('#gallery'); if (g && $('#panes').dataset.at === 'gallery' && GV.tab === 'battle' && !fl.classList.contains('on') && !g.querySelector('.cmp-bar')) { g.insertAdjacentHTML('afterbegin', cmpBar('ch')); cmpWire(g); }
}
const _renderGalleryC = renderGallery;
renderGallery = function () { const r = _renderGalleryC.apply(this, arguments); try { if (GV.tab === 'battle') { CMP_TAB = 'ch'; cmpPaint(); } } catch (e) {} return r; };
$('#segGallery').onclick = () => cmpOpen(CMP_TAB === 'tour' ? 'tour' : 'ch');
$('#segCompete').onclick = () => cmpOpen('tour');
const _closeFlowC = closeFlow; closeFlow = function () { const r = _closeFlowC.apply(this, arguments); if (CMP_TAB === 'tour') CMP_TAB = 'ch'; return r; };
new MutationObserver(() => { try { cmpPaint(); } catch (e) {} }).observe($('#flowBody'), { childList: true });
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]
CSS = r'''
/* one Compete menu */
#segCompete{display:none!important}
.cmp-bar{position:sticky;top:0;z-index:4;display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:4px 14px 12px;padding:4px;border-radius:16px;background:#EFE6D6;box-shadow:inset 0 0 0 1.5px #E2D5BE}
.cmp-bar button{border:0;background:none;border-radius:12px;padding:9px 6px;font:800 1rem "Nunito Sans",sans-serif;color:#5F534A;cursor:pointer}
.cmp-bar button[aria-selected="true"]{background:#2D4E86;color:#fff;box-shadow:0 4px 10px -4px rgba(45,78,134,.6)}
html.yg .cmp-bar{background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.14)}html.yg .cmp-bar button{color:#D8CCF0}
html.yg .cmp-bar button[aria-selected="true"]{background:linear-gradient(95deg,#7B3CFF,#FF2D8E);color:#fff}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('compete ok')
