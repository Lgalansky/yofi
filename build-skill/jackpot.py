# Skill preview: the daily jackpot challenges (Today's photo challenges, the pots that pay at
# midnight) take every other turn in the green real-money card under the photos on Vote.
# "$2,375 Pet jackpot · Daily challenge · You 1/3 ⭐ · from $1" → opens that category's challenge.
# Every 4th turn is Quick Sprint, sold with your judge score: "Your 74% eye vs a 71% rival".
# An incoming friend challenge still comes first. Categories you have a 70+ photo for rotate.
# usage: python3 build-skill/jackpot.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- jackpot challenges in the green card on Vote ----
function vcJackpot(turn) { const L = lgS(), ks = CATS8.filter(k => k !== 'any' && lgMine(k));
  const list = ks.length ? ks : CATS8.filter(k => k !== 'any' && S.photos.some(p => fitsTheme(p, k))); if (!list.length) return null;
  const k = list[Math.floor(turn / 2) % list.length], y = L.you[k] || 0, mine = lgMine(k), pot = Math.round(L.jp[k] || 0);
  return { img: mine ? mine.src : lgPhoto(lgHold(k).h, k), t: `$${pot.toLocaleString()} ${crownName(k)} jackpot`,
    s: mine ? `You ${Math.min(y, LG_SHARE)}/${LG_SHARE} ⭐ · from $1 · daily` : `Get a ${crownName(k).toLowerCase()} photo to 70 to play`,
    cta: 'Play', jp: 1, go: () => { goCash(); openBattleTab(); setTimeout(() => lgCat(k), 300); } }; }
const _vcCardJ = vcCard;
vcCard = function () { const fr = S.fr && (S.fr.ch || []).find(c => c.st === 'yours'); if (fr) return _vcCardJ.apply(this, arguments);
  const turn = Math.floor(((S.votes || 0) + (S.vcOff || 0)) / 3);
  if (turn % 2 === 0) { const j = vcJackpot(turn); if (j) return j; }
  if (turn % 4 === 1) return vcSprint();
  return _vcCardJ.apply(this, arguments); };
// your judge score sells the 1 v 1 Quick Sprint (pick the crowd's photo in 10 pairs)
function vcSprint() { const has = typeof jgLv === 'function' && jgLv(), a = has ? jgAcc() : 0, rv = has ? Math.max(50, a - 1 - hsh(dayKey() + 'qs') % 4) : 0;
  return { art: '🎯', t: has ? `Your ${a}% eye vs a ${rv}% rival` : 'Who has the better eye? 1 v 1', s: 'Quick Sprint · $2 wins $3.20', cta: 'Play', go: () => { window.__qsReal = 1; sprEnter(); } }; }
setTimeout(() => { try { vcPaint(); } catch (e) {} }, 450);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
open(p, 'w', encoding='utf-8').write(s); print('jackpot ok')
