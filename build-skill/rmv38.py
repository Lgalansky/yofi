# Real Money build, step 41 (after rmv37.py): new players don't see Quick Sprint or the coin challenge
# until the tutorial is done (their first free Final pick is used).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
s = s.replace("function fcNotify() {", "const newbie = () => S && (S.tut || 9) < 3;\nfunction fcNotify() {", 1)
RA("if (!isCash()) I.push({ ic: '⚡', t: 'Quick Sprint'", "if (!isCash() && !newbie()) I.push({ ic: '⚡', t: 'Quick Sprint'")
RA("if (f && !isCash()) I.push({ ic: '🏅', t: 'Coin challenge'", "if (f && !isCash() && !newbie()) I.push({ ic: '🏅', t: 'Coin challenge'")
RA("  if (S.potSeen) { const per = S.qsTried ? 50 : 20,", "  if (S.potSeen && !newbie()) { const per = S.qsTried ? 50 : 20,")
open(d + 'yofi-real.html', 'w').write(s); print('rm v38 ok')
