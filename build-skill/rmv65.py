# Real Money build, step 68 (after rmv64.py): make clear the podium is the CROWD'S result, not your picks.
#  - Label above the podium: "The crowd’s top 3" (Judges’ for the young look).
#  - A podium photo you picked gets a tag "Your 1st pick" (green if it is in that exact spot, muted otherwise).
#  - Label above your picks already reads "Your picks".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<div class="rv-pod" id="rvPod">', '<p class="rv-lab">${isYoungW() ? \'The judges’\' : \'The crowd’s\'} top 3</p><div class="rv-pod" id="rvPod">')
RA('el.innerHTML = `<img src="${p.src}" alt=""><b>${RV_MED[k]} ${RV_ORD[k]}</b>`;',
   'const yi = picks.indexOf(ord[k]); el.innerHTML = `<img src="${p.src}" alt="">${yi >= 0 ? `<i class="rv-you ${yi === k ? \'ok\' : \'\'}">Your ${[\'1st\', \'2nd\', \'3rd\'][yi]} pick</i>` : \'\'}<b>${RV_MED[k]} ${RV_ORD[k]}</b>`;')
s = s.replace('</style>', """.rv-lab{margin:0 0 6px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:.78rem;color:#1E3A6E}
.rv-you{position:absolute;top:6px;left:50%;transform:translateX(-50%);white-space:nowrap;font-style:normal;font-weight:800;font-size:.72rem;padding:2px 8px;border-radius:999px;background:rgba(255,255,255,.92);color:#8A3B32;z-index:2}.rv-you.ok{background:#1E3A6E;color:#fff}
html body .ppop .rv-you{-webkit-text-fill-color:currentColor}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v65 ok')
