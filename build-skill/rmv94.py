# Real Money build, step 97 (after rmv93.py): three-game rotation, less often.
#  Every 15 votes (was 10) the next game in the cycle qualifier → Quick Sprint → free Final pick comes up.
#  Games you can't afford are skipped (Sprint 100 coins, free pick 250 coins and 2 per hour), and a qualifier never
#  comes twice in a row; short of coins, qualifiers alternate with a quiet slot (strip shows progress to a free pick).
#  The Coming-up strip names the next game, or while saving up shows "Free Final pick · 180/250 coins".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("var GATE_EVERY = 10", "var GATE_EVERY = 15")
RA("S.rotN = (S.rotN || 0) + 1; save(); if (S.rotN % 2 === 0 && (S.gems || 0) >= QS_COIN) sprintUp(); else gateOpen(false);",
   "const nx = rotPeek(); S.rotLast = nx || 'x'; save(); if (nx === 's') sprintUp(); else if (nx === 'p') freePickUp(); else if (nx === 'g') gateOpen(false);")
RA("it.push(sprNext() ? { ic: '🎯', t: `<b>Quick Sprint</b> · 1 v 1 · win ${QS_COIN_PAY[0]} coins`, k: 'g', need: Math.max(1, GATE_EVERY - (S.gtN || 0)), per: GATE_EVERY } : ",
   """it.push((S.tut || 9) >= 4 && rotPeek() !== 'g' ? (() => { const r = rotPeek(), need = Math.max(1, GATE_EVERY - (S.gtN || 0)); return r === 's' ? { ic: '🎯', t: `<b>Quick Sprint</b> · 1 v 1 · win ${QS_COIN_PAY[0]} coins`, k: 'g', need, per: GATE_EVERY } : r === 'p' ? { ic: '🎟️', t: `<b>Free Final pick</b> · pick the top 3 · real cash prizes`, k: 'g', need, per: GATE_EVERY } : { ic: '🎟️', t: `<b>Free Final pick</b> · ${Math.floor(S.gems || 0)}/${FREE_BET_COINS} coins · keep voting`, k: 'g', need: 0, per: 1, em: `${Math.max(0, FREE_BET_COINS - Math.floor(S.gems || 0))} to go` }; })() : """)
s = s.replace("function fcNotify() {", r"""function rotPeek() { if ((S.tut || 9) < 4) return 'g'; const ok = { g: S.rotLast !== 'g', s: (S.gems || 0) >= QS_COIN, p: !isCash() && fqLeft() && (S.gems || 0) >= FREE_BET_COINS }, O = ['g', 's', 'p'], i = O.indexOf(S.rotLast);
  for (let k = 1; k <= 3; k++) { const c = O[(i + k + 3) % 3]; if (ok[c]) return c; } return null; }
function freePickUp() { const g = ppGame(); celebrate({ src: (g.ph[0] || {}).src || '', score: '🎟️', title: 'Free Final pick is up', text: `Use <b>${FREE_BET_COINS} coins</b> for a free pick in the <b>${raceName(g.sl)} ${esc(showName(g.k))} Final</b>: pick the top 3 for real cash prizes.`,
  cta: '🎟️ Make my free pick', onCta: () => { closeFlow(); fqStart(); }, later: 'Keep voting' }); }
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v94 ok')
