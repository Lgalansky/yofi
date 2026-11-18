# Real Money build, step 104 (after rmv100.py): the coin game is "Coin Pick" again (user's choice): strip
# "Coin Pick · Nature & landscapes · pick 3 of 5 · free", "Coin Pick · Round 1 of 3", "Coin Pick win".
# Photo side keeps "qualifiers". Vote tiles stay clean (result in the banner).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('g2-chip">Qualifier · Round ${G.gi + 1} of 3', 'g2-chip">Coin Pick · Round ${G.gi + 1} of 3')
RA("kicker: `Qualifier · Round ${G.gi + 1} of 3`", "kicker: `Coin Pick · Round ${G.gi + 1} of 3`")
RA("Qualifier · Round ${G.gi + 1} of 3", "Coin Pick · Round ${G.gi + 1} of 3")
s = s.replace("label: 'Qualifier win'", "label: 'Coin Pick win'")
RA("<b>Upcoming qualifier · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of", "<b>Coin Pick · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of")
open(d + 'yofi-real.html', 'w').write(s); print('rm v101 ok')
