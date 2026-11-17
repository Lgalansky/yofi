# Real Money build, step 47 (after rmv43.py): keep the flow judge -> pick -> create.
# The Vote screen pushes picking only: the creator prompts move off it and onto the end of a pick (the Final result card).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('${qsChipHTML()}${crLineHTML()}<div class="tot-h">', '${qsChipHTML()}<div class="tot-h">')
RA('<div class="tut-up"><b>📷 Enter your own photo</b><span>',
   '<div class="tut-up">${(() => { const w = g.ph[g.ord[0]]; return w ? `<p class="cr-earn">🏆 @${esc(w.h)} earned <b>${money(finShare(g.sl, 1))}</b> as the creator of “${esc(w.t)}”, this Final’s winner</p>` : \'\'; })()}<b>📷 Enter your own photo</b><span>')
open(d + 'yofi-real.html', 'w').write(s); print('rm v44 ok')
