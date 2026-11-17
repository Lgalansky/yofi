# Real Money build, step 32 (after rmv28.py): "You've got N coins!" nudge.
#  - Quick Sprint idea has a photo (no broken image).
#  - With 250+ coins and a free pick left this hour, the nudge offers the free Final pick first.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("cost: QS_COIN, go: () => { closeSheet(); window.__qsGame = 'qs'; sprPractice(); } });",
   "cost: QS_COIN, src: (fighters()[0] || SEED.find(z => z.src) || {}).src || '', go: () => { closeSheet(); window.__qsGame = 'qs'; sprPractice(); } });")
RA("  const I = gemIdeas(); if (!I.length) return false; S.gnMark = mark; S.gnVote = S.votes || 0; save(); paintGemGlow(); const x = I.find(i => S.gems >= i.cost) || I[0];",
   "  if (!isCash() && (S.tut || 9) >= 3 && fqLeft() && (S.gems || 0) >= FREE_BET_COINS) { S.gnMark = mark; S.gnVote = S.votes || 0; save(); paintGemGlow(); const g = ppGame();\n    celebrate({ src: (g.ph[0] || {}).src || '', score: '🎟️', title: `You’ve got ${Math.floor(S.gems).toLocaleString()} coins!`, text: `Use <b>${FREE_BET_COINS} 🟡</b> for a free pick in the <b>${raceName(g.sl)} ${esc(showName(g.k))} Final</b>. Top scores share the <b>${ppPool(g.players)}</b> prize pool in real cash.`, cta: '🎟️ Make a free Final pick', onCta: () => { closeFlow(); ppOpen(); }, later: 'Later' }); return true; }\n  const I = gemIdeas(); if (!I.length) return false; S.gnMark = mark; S.gnVote = S.votes || 0; save(); paintGemGlow(); const x = I.find(i => S.gems >= i.cost && i.src) || I.find(i => i.src) || I[0];")
open(d + 'yofi-real.html', 'w').write(s); print('rm v29 ok')
