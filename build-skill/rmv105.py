# Real Money build, step 108 (after rmv104.py): the Coming-up strip says just "Coin Pick · pick 3 of 5 · free"
# (no category name).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "<b>Coin Pick · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of"
assert s.count(a) == 1; s = s.replace(a, "<b>Coin Pick</b> · pick 3 of")
open(d + 'yofi-real.html', 'w').write(s); print('rm v105 ok')
