# Real Money build, step 182 (after rmv178.py): "cash-ready (for good)" is now "Ready for Cash Races" everywhere.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
R = [("train it to make it cash-ready.", "train it to get it Ready for Cash Races."),
     ("to cash-ready", "to Ready for Cash Races"),
     ("your photo is <b>💵 cash-ready for good</b>", "your photo is <b>💵 Ready for Cash Races</b>"),
     ("💵 Cash-ready ✓", "💵 Ready for Cash Races ✓"),
     ("'🏆 Finalist · 💵 Cash-ready' : '💵 Cash-ready'", "'🏆 Finalist · 💵 Ready for Cash Races' : '💵 Ready for Cash Races'"),
     ("+50 🟡 · 💵 cash-ready", "+50 🟡 · 💵 Ready for Cash Races"),
     ("losses to go 💵 cash-ready", "losses to be 💵 Ready for Cash Races"),
     ("is cash-ready for good: Finals and cash head-to-heads", "is Ready for Cash Races: Finals and cash head-to-heads"),
     ("Once a photo is 💵 cash-ready, it races for real money for good.", "Once a photo is 💵 Ready for Cash Races, it stays that way."),
     ("'Resting · train it to go cash-ready'", "'Resting · train it for Cash Races'")]
for a, b in R:
    assert a in s, a; s = s.replace(a, b)
s = s.replace("<span>${esc(rcName(p))} is</span><b>💵 Cash-ready</b>", "<span>${esc(rcName(p))} is</span><b>💵 Ready for Cash Races</b>")
s = s.replace("For good: it can enter Finals", "It can enter Finals")
open(d + 'yofi-real.html', 'w').write(s); print('rm v179 ok')
