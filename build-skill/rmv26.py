# Real Money build, step 29 (after rmv25.py): qualifier "Coming up" item says "Upcoming qualifier" (no time) with a scales icon;
# the qualifier pick/result pops use the scales icon and no time either.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("ic: '🎀', t: `<b>Qualifiers · ${raceName(ppSlot() + 1)} ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of 5 · free`",
   "ic: '⚖️', t: `<b>Upcoming qualifier · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of 5 · free`")
RA('<p class="pp-k">🎀 Qualifiers · ${fin} ${esc(showName(ppGame(G.ns).k))}</p>', '<p class="pp-k">⚖️ Upcoming qualifier · ${esc(showName(ppGame(G.ns).k))}</p>')
RA('<p class="pp-k">🎀 Group ${G.gi + 1} of 3 · results</p>', '<p class="pp-k">⚖️ Group ${G.gi + 1} of 3 · results</p>')
open(d + 'yofi-real.html', 'w').write(s); print('rm v26 ok')
