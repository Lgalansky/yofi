# Real Money build, step 109 (after rmv105.py): Coin Pick screen drops the "Win up to · 50 coins" headline;
# the three prize cards (50 / 25 / 10 coins) already show what you can win.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = '<div class="qz3-win"><span class="qz3-pill">Win up to</span><b class="qz3-big"><i class="qz3-coin" aria-hidden="true"></i>${GATE_COINS[3]} coins</b></div>'
assert s.count(a) == 1; s = s.replace(a, '')
open(d + 'yofi-real.html', 'w').write(s); print('rm v106 ok')
