# Real Money build, step 13 (after rmv9.py): coin players don't see the cash blue ribbon / pot challenge
# when asked to add a photo for a category (e.g. from "Got a travel photo? · coin challenge").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("""<p>Upload a ${esc(cn.toLowerCase())} photo, get your score, then enhance it to <b>${CFG.QUALIFY}+</b> to challenge for the ${esc(cn)} blue ribbon${L ? ` and today’s <b>${('$' + Math.round(L.jp[k]).toLocaleString())}</b> pot` : ''}.</p>""",
   """<p>${isCash() ? `Upload a ${esc(cn.toLowerCase())} photo, get your score, then enhance it to <b>${CFG.QUALIFY}+</b> to challenge for the ${esc(cn)} blue ribbon${L ? ` and today’s <b>${('$' + Math.round(L.jp[k]).toLocaleString())}</b> pot` : ''}.` : `Upload a ${esc(cn.toLowerCase())} photo, get your score, then enhance it to <b>${CFG.QUALIFY}+</b> to play ${esc(cn.toLowerCase())} coin challenges. Stake <b>25 🟡</b>, win <b>50 🟡</b>.`}</p>""")
open(d + 'yofi-real.html', 'w').write(s); print('rm v10 ok')
