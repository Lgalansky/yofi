# Skill preview: fixes from the full play-through audit (style guide in CLAUDE.md).
#  1. Pop-up buttons (Gold level-up, add profile photo, Payday, ...) use the shared button font (Nunito Sans bold,
#     sentence case) instead of serif capitals.
#  2. Age question: the Continue button is navy like every other free action (was a pink/purple gradient).
#  3. Payday receipt says "+22 · Earned by your photos in the last 2h 41m" (was "Voters picked your photos ...");
#     its button is shorter: "Steal a card · 3 free tries".
#  4. Add cash: no duplicate "Shop" heading; copy no longer mentions "blue ribbon challenges".
#  5. Sign-up: the repeated "Create your account so nothing gets lost." sentence is gone.
#  6. The jackpot game screen is titled "Pet challenge" like its Live games tile (was "Pet jackpot").
#  7. Judge words: "You vs another judge" (was "Your eye vs a rival"), "Similar judge" (was "Similar eye").
#  8. Profile: "Spend coins" (was "Coin store": coins are earned, never sold).
#  9. Crowd Championship screen: "You" shows your judge avatar, like Judge Duel.
# Usage: python3 build-skill/audit1.py in.html out.html  (run after galfix.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
def R(a, b, n=None):
    global s
    c = s.count(a); assert c >= 1 and (n is None or c == n), (a[:70], c); s = s.replace(a, b)
R('<p class="jp-sub">🗳 Voters picked your photos in the last <b>${ago}</b></p>', '<p class="jp-sub">Earned by your photos in the last <b>${ago}</b></p>', 1)
R("`Steal a card · ${lt} free tr${lt === 1 ? 'y' : 'ies'} left`", "`Steal a card · ${lt} free tr${lt === 1 ? 'y' : 'ies'}`", 1)
R("Play blue ribbon challenges, friends and tournaments. Coins can’t be bought: earn the", "Play Photo Duels, Judge Duels and daily challenges. Coins can’t be bought: earn the", 1)
R('<div class="sp-top"><h2>Shop</h2>', '<div class="sp-top"><h2 class="sp-hide">Add cash</h2>', 1)
R("Create your account so nothing gets lost.</p>", "</p>", 1)
R("${LG_IC[k] || '⭐'} ${esc(cn)} jackpot</span>", "${LG_IC[k] || '⭐'} ${esc(cn)} challenge</span>", 1)
R("'Your eye vs a rival'", "'You vs another judge'")
R("'A rival<small>Similar eye</small>'", "'A rival<small>Similar judge</small>'", 1)
R('id="mS">Coin store</button>', 'id="mS">Spend coins</button>', 1)
JS = r'''
// ---- Crowd Championship: your judge avatar for "You" ----
function auCrowd() { const w = document.querySelector('#sheetBody .pj.gs'); if (!w || w.dataset.auc) return;
  if (!/Crowd Championship/.test((w.querySelector('.pj-t') || {}).textContent || '')) return; const f = w.querySelector('.pj-vs .pj-me'); if (!f) return;
  const ph = [...f.children].find(x => x.tagName !== 'FIGCAPTION'); if (!ph) return; w.dataset.auc = 1;
  const lab = ((ph.innerText || '').match(/\d+\s*\/\s*\d+|\d+%|\?/) || ['?'])[0].replace(/\s/g, '');
  try { ph.outerHTML = `<span class="qs-av me"><img src="${(S.user && S.user.pic) || AV_YOU}" alt=""><i>${esc(lab)}</i></span>`; f.parentNode.classList.add('qs-avs'); } catch (e) {} }
new MutationObserver(() => { try { auCrowd(); } catch (e) {} }).observe($('#sheetBody'), { childList: true, subtree: true });
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
html body #coach .bt-cta,html body #coach .btn,html body #coach button.btn,html body #coach .pp .btn{font-family:"Nunito Sans",Nunito,sans-serif!important;text-transform:none!important;letter-spacing:0!important;font-weight:800!important}
html body #obGo1{background:#2D4E86!important;background-image:none!important;color:#fff!important;font-family:"Nunito Sans",Nunito,sans-serif!important}html body #obGo1[disabled]{opacity:.45}
html body .shop2 .sp-top h2.sp-hide{visibility:hidden}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('audit1 ok')
