# Real Money build, step 46 (after rmv42.py): turn judges into creators, only after their first Final pick.
#  - Vote screen line under Coming up: "🏆 @luna_loves earned $31.40 with "Golden boy" in the 3pm Pets Final" (last Final's winner).
#  - If the player has no photo in play: "📷 Got a pet photo? The 4pm Pets Final pays creators 10% of a $1,050 pool · Enter it ›"
#    (next Final's category; tap opens the photo picker for it; ✕ hides it for 20 votes).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""const CR_NOUN = { pets: 'pet', nature: 'nature', garden: 'garden', food: 'food' };
function crLineHTML() { if (!S || (S.tut || 9) < 3 || isYoungW()) return ''; const sl = ppSlot() - 1, g = ppGame(sl), w = g.ph[g.ord[0]]; if (!w) return '';
  let h = `<p class="cr-earn">🏆 @${esc(w.h)} earned <b>${money(finShare(sl, 1))}</b> with “${esc(w.t)}” in the ${raceName(sl)} ${esc(showName(g.k))} Final</p>`;
  if (!inPlay() && (S.votes || 0) >= (S.crHide || 0)) { const n = finNext(1)[0], ng = ppGame(n.sl);
    h += `<div class="cr-ask"><button class="cr-go" data-crk="${n.k}"><span class="cr-ic">📷</span><span><b>Got a ${CR_NOUN[n.k] || ''} photo?</b><small>The ${raceName(n.sl)} ${esc(showName(n.k))} Final pays creators 10% of a ${ppPool(ng.players)} pool</small></span><em>Enter it ›</em></button><button class="cr-x" aria-label="Not now">✕</button></div>`; }
  return `<div class="cr-wrap" id="crWrap">${h}</div>`; }
setInterval(() => { try { const el = document.getElementById('crWrap'); if (!el || !S) return; const t = document.createElement('div'); t.innerHTML = crLineHTML(); const n = t.firstElementChild; if (!n) { el.remove(); return; } if (n.innerHTML !== el.innerHTML) el.innerHTML = n.innerHTML; } catch (e) {} }, 3000);
document.addEventListener('click', e => { const g = e.target.closest('[data-crk]'); if (g) { e.preventDefault(); e.stopPropagation(); window.__preCat = showHint(g.dataset.crk).cats[0]; pickPhoto(true); return; }
  if (e.target.closest('.cr-x')) { e.preventDefault(); e.stopPropagation(); S.crHide = (S.votes || 0) + 20; save(); const a = document.querySelector('.cr-ask'); if (a) a.remove(); } }, true);
function fcNotify() {""", 1)
RA('${qsChipHTML()}<div class="tot-h">', '${qsChipHTML()}${crLineHTML()}<div class="tot-h">')
s = s.replace('</style>', """.cr-wrap{margin:4px 0 8px}.cr-earn{margin:0 0 6px;font-size:.84rem;text-align:center;opacity:.9}.cr-earn b{color:#2F6B3F}
.cr-ask{display:flex;align-items:stretch;gap:6px}.cr-go{flex:1;display:flex;align-items:center;gap:10px;text-align:left;border:0;border-radius:14px;padding:9px 12px;background:#FBDDE3;color:#2B2320;font:inherit;cursor:pointer;box-shadow:inset 0 0 0 1.5px #E7A9B8}
.cr-go .cr-ic{font-size:1.5rem}.cr-go b{display:block;font-size:.95rem;color:#7A1638}.cr-go small{display:block;font-size:.78rem;opacity:.85}.cr-go em{font-style:normal;font-weight:900;color:#9A2F4E;white-space:nowrap;margin-left:auto}
.cr-x{border:0;background:none;font-size:1rem;opacity:.5;cursor:pointer;padding:0 4px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v43 ok')
