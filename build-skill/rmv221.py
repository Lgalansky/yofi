# Real Money build, step 224 (after rmv220.py): vote reveal starts at 50/50.
#  - After a vote both photos show 50%, hold for a beat, then the bars slide and the numbers count to the real split.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""(() => { const cf = callFx; callFx = function () { const r = cf.apply(this, arguments); try { const B = [...document.querySelectorAll('#judge .tot-c .cfx-fill b')], T = B.map(b => parseInt(b.textContent, 10) || 50), t0 = performance.now() + 350, dur = 900;
    B.forEach(b => b.textContent = '50%'); const ease = x => 1 - Math.pow(1 - x, 3);
    const tick = now => { const k = Math.max(0, Math.min(1, (now - t0) / dur)); B.forEach((b, i) => { if (b.isConnected) b.textContent = Math.round(50 + (T[i] - 50) * ease(k)) + '%'; }); if (k < 1 && B.some(b => b.isConnected)) requestAnimationFrame(tick); };
    requestAnimationFrame(tick); } catch (e) {} return r; }; })();
function fcNotify() {""")
s = s.replace('</style>', """@keyframes cfxUp{from{height:50%}to{height:var(--h)}}html body #judge .tot-c .cfx-fill i{height:50%;animation:cfxUp .9s cubic-bezier(.2,.9,.3,1) .35s both!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v221 ok')
