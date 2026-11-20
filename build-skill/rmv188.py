# Real Money build, step 191 (after rmv187.py): from the newbie play-through.
#  - The qualifier is a real 2-horse race: a navy track with two lanes, each photo is a horse that gallops toward a
#    gold-chequered finish line (11 votes), live counts at the line, a lead badge, the leader's lane glows.
#  - 3-2-1 overlay covers the whole screen (it was cut off at the bottom).
#  - Streak card label reads "0 of 3 steps · 2 in a row = 1 step" instead of "Step 0 of 3".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
A1 = '''<div class="qr2-c me" id="qrCA"><div class="qr2-im"><img src="${p.src}" alt=""><span class="qr2-n">${nm} · <b>You</b></span></div><div class="qr2-r"><b id="qrAv">0</b><small>of ${QR_WIN} votes</small><span class="qr2-p" id="qrAp">${nvPips(0, 'on')}</span></div></div>'''
i = s.index(A1); j = s.index('<p class="qr2-v" id="qrV">', i)
s = s[:i] + '''<div class="hr-trk"><div class="hr-fin"><span>🏁</span></div>
      <div class="hr-ln me" id="qrCA"><span class="hr-nm">${nm} · <b>You</b></span><div class="hr-rail"><i class="hr-dust"></i><img id="qrHA" src="${p.src}" alt=""></div><b class="hr-v" id="qrAv">0</b></div>
      <div class="hr-ln" id="qrCB"><span class="hr-nm">${esc(o.t)}</span><div class="hr-rail"><i class="hr-dust"></i><img id="qrHB" src="${o.src}" alt=""></div><b class="hr-v" id="qrBv">0</b></div>
      <div class="hr-ticks">${Array.from({ length: QR_WIN - 1 }, (_, k) => `<i style="left:calc(${(k + 1) / QR_WIN} * (100% - 120px) + 40px)"></i>`).join('')}</div></div><span hidden id="qrAp"></span><span hidden id="qrBp"></span>
    ''' + s[j:]
RA("$('#qrAp').innerHTML = nvPips(A, 'on'); $('#qrBp').innerHTML = nvPips(B, 'on');",
   "$('#qrAp').innerHTML = nvPips(A, 'on'); $('#qrBp').innerHTML = nvPips(B, 'on'); { const mv = (id, v) => { const h = document.getElementById(id); if (h) h.style.left = `calc(${Math.min(1, v / QR_WIN)} * (100% - 52px))`; }; mv('qrHA', A); mv('qrHB', B); const la = document.getElementById('qrCA'), lb = document.getElementById('qrCB'); la.classList.toggle('lead', A > B); lb.classList.toggle('lead', B > A); }")
RA("Step ${Math.min(QS_STEPS, s)} of ${QS_STEPS}${fin ? ' to the Final' : ''}", "${Math.min(QS_STEPS, s)} of ${QS_STEPS} steps · 2 in a row = 1 step")
s = s.replace('</style>', """.hr-trk{position:relative;margin:4px 0 10px;padding:10px 10px 8px;border-radius:18px;background:linear-gradient(180deg,#1B2B52,#14213D);box-shadow:inset 0 0 0 2px #D9AE4F,0 8px 20px rgba(0,0,0,.35);text-align:left}
.hr-fin{position:absolute;top:8px;bottom:8px;right:52px;width:10px;background:repeating-linear-gradient(0deg,#fff 0 8px,#14213D 8px 16px);border-radius:2px;z-index:2}.hr-fin span{position:absolute;top:-14px;left:-6px;font-size:1.1rem}
.hr-ln{position:relative;display:grid;grid-template-columns:1fr 44px;align-items:center;gap:6px;padding:6px 0;transition:background .3s}.hr-ln+.hr-ln{border-top:1px dashed rgba(255,255,255,.18)}
.hr-nm{grid-column:1/-1;font:700 .8rem Nunito,system-ui;color:#C9D3E6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.hr-nm b{color:#F3D98B}
.hr-rail{position:relative;height:60px;border-radius:30px;background:rgba(255,255,255,.05)}.hr-rail img{position:absolute;top:4px;left:0;width:52px;height:52px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #fff;transition:left .55s cubic-bezier(.3,1.3,.5,1);z-index:3}
.hr-ln.me .hr-rail img{box-shadow:0 0 0 3px #F3D98B,0 0 16px rgba(243,217,139,.7)}.hr-ln.lead .hr-rail img{animation:hrGal .35s ease-in-out infinite alternate}@keyframes hrGal{to{transform:translateY(-4px) rotate(-4deg)}}
.hr-ln.lead .hr-rail{background:rgba(233,185,73,.12)}.hr-ln.lead .hr-nm::after{content:' · leads';color:#9FE3AE;font-weight:900}
.hr-v{font:900 2rem/1 Fraunces,Georgia,serif;color:#FBF3DC;text-align:center}.hr-ln.me .hr-v{color:#F3D98B}.hr-ln.hit .hr-v{animation:qmBp .45s ease-out}
.hr-ticks{position:absolute;inset:0;pointer-events:none}.hr-ticks i{position:absolute;bottom:6px;width:1px;height:6px;background:rgba(255,255,255,.25)}
html body #coach.on .qrx>.qr-cd.cd2{position:fixed!important;inset:0!important;z-index:9999!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v188 ok')
