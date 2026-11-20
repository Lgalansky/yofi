# Real Money build, step 211 (after rmv207.py): cash entries with too little cash open "Add cash", not the coins pop.
#  - payCash (rmv201) dropped the word "cash" from its reason, so openStore sent every short cash entry
#    (challenges, head-to-heads, Finals) to "Need more coins?". Restored.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "if (tot() < amt) { openStore(`${what} costs ${money(amt)}.`,"
assert s.count(a) == 1
s = s.replace(a, "if (tot() < amt) { openStore(`${what} costs ${money(amt)} cash.`,")
open(d + 'yofi-real.html', 'w').write(s); print('rm v208 ok')
