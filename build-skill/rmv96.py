# Real Money build, step 99 (after rmv95.py):
#  - Quick Sprint costs 25 coins and wins 40 (was 100 → 160), so players with a few coins get it in the rotation.
#  - Rotation slot 3 is the "You have unused coins" pop: "You've got 280 coins: enough for a free pick in the 9am Pets
#    Final" → Open my coins → guided coins menu with the Free Final pick row highlighted → pick screen.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const QS_COIN = 100, QS_COIN_PAY = [160];", "const QS_COIN = 25, QS_COIN_PAY = [40];")
i = s.index("function freePickUp() {"); j = s.index("function fcNotify() {", i)
s = s[:i] + r"""function freePickUp() { const g = ppGame(); celebrate({ src: (g.ph[0] || {}).src || '', score: '🎟️', title: 'You have unused coins', text: `You’ve got <b>${Math.floor(S.gems).toLocaleString()} coins</b>: enough for a free pick in the <b>${raceName(g.sl)} ${esc(showName(g.k))} Final</b>, with real cash prizes. Open your coins to use them.`,
  cta: '🟡 Open my coins', onCta: () => { closeFlow(); coinTour(); }, later: 'Later' }); }
""" + s[j:]
open(d + 'yofi-real.html', 'w').write(s); print('rm v96 ok')
