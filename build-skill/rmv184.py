# Real Money build, step 187 (after rmv183.py): the 3-2-1 before every race, rebuilt to build excitement.
#  Full screen navy: PhotoPicks bar, gold race label, "Get ready" headline, the prize in gold italic
#  ("Winner takes $8.50" / "Winner goes to the Nature & landscapes Final"), both photos large with names and handles
#  and a glowing VS, a big countdown inside a gold ring that drains each second, then "GO!" with a flash.
#  Rule line underneath ("15 crowd votes · most votes wins" / "First to 11 votes"). No empty space at the bottom.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function qrCount(p, o, oh, run, kick, sub) { const box = document.querySelector('.qrx'); if (!box) { run(); return; }
  const cash = /\$/.test(sub || ''), quali = !kick, prize = quali ? `Winner goes to the ${esc(showName(photoShow(p) || finCatOf(p) || 'pets'))} Final` : (sub || '').replace(/^Most votes of \d+ wins /, 'Winner takes ');
  const rule = quali ? `First to ${QR_WIN} crowd votes wins` : `${H3_V} crowd votes · most votes wins`;
  box.insertAdjacentHTML('beforeend', `<div class="qr-cd cd2" id="qrCd"><div class="cd2-top"><span>🖼️ PhotoPicks</span></div>
    <p class="cd2-k">${kick || '🎀 Live qualifier'}</p><h2 class="cd2-h">Get ready</h2><p class="cd2-p">${prize}</p>
    <div class="cd2-vs"><div class="me"><img src="${p.src}" alt=""><b>${esc(rcName(p))}</b><small>You</small></div><span class="cd2-x">VS</span><div><img src="${o.src}" alt=""><b>${esc(o.t)}</b><small>${esc(oh)}</small></div></div>
    <div class="cd2-ring" id="cdR"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44" class="bg"/><circle cx="50" cy="50" r="44" class="fg" id="cdArc"/></svg><b class="qr-num" id="qrNum">3</b></div>
    <p class="cd2-r">${rule}</p></div>`);
  const arc = () => { const a = document.getElementById('cdArc'); if (!a) return; a.style.transition = 'none'; a.style.strokeDashoffset = '0'; void a.getBoundingClientRect(); a.style.transition = 'stroke-dashoffset .88s linear'; a.style.strokeDashoffset = '276'; };
  arc(); let n = 3; const t = setInterval(() => { const e = document.getElementById('qrNum'); if (!e) { clearInterval(t); return; } n--; e.textContent = n > 0 ? n : 'GO!'; e.classList.remove('go'); void e.offsetWidth; e.classList.add('go');
    if (n > 0) arc(); else { document.getElementById('cdR').classList.add('go'); try { navigator.vibrate && navigator.vibrate(30); } catch (x) {} }
    if (n <= 0) { clearInterval(t); setTimeout(() => { const c = document.getElementById('qrCd'); if (c) { c.classList.add('bye'); setTimeout(() => c.remove(), 350); } run(); }, 700); } }, 900); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .qrx>.qr-cd.cd2{position:absolute!important;inset:-12px -16px -28px!important;z-index:30!important;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:calc(env(safe-area-inset-top) + 12px) 16px 24px;background:radial-gradient(120% 60% at 50% 0%,#1A2B58 0%,#0B1530 60%,#08102A 100%)!important;text-align:center;overflow:hidden}
.cd2-top{align-self:stretch;text-align:left;margin-bottom:18px}.cd2-top span{font:800 1.3rem Fraunces,Georgia,serif;color:#FBF3DC}
html body .cd2 .cd2-k{margin:0 0 6px;font:900 .82rem Nunito,system-ui;letter-spacing:.14em;text-transform:uppercase;color:#F3D98B!important;-webkit-text-fill-color:#F3D98B!important}
html body .cd2 h2.cd2-h{margin:0;font:900 2.8rem/1 Fraunces,Georgia,serif;color:#FBF3DC!important;-webkit-text-fill-color:#FBF3DC!important}
.cd2-p{margin:6px 0 18px;font:italic 600 1.3rem/1.25 Fraunces,Georgia,serif;color:#F3D98B}
.cd2-vs{display:grid;grid-template-columns:1fr 44px 1fr;align-items:center;gap:6px;width:100%}.cd2-vs>div{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:0;animation:cd2In .5s ease-out both}.cd2-vs>div:last-child{animation-delay:.12s}
@keyframes cd2In{0%{opacity:0;transform:translateY(14px) scale(.96)}100%{opacity:1;transform:none}}
.cd2-vs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px;box-shadow:0 0 0 2px rgba(255,255,255,.3)}.cd2-vs .me img{box-shadow:0 0 0 3px #E9B949,0 0 20px rgba(233,185,73,.4)}
.cd2-vs b{margin-top:4px;font:800 1rem Fraunces,Georgia,serif;color:#FBF3DC;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cd2-vs small{font:700 .8rem Nunito,system-ui;color:#B9C3DA}
.cd2-x{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#0B1530;box-shadow:0 0 0 2px #E9B949,0 0 16px rgba(233,185,73,.5);font:900 .95rem Fraunces,Georgia,serif;color:#FBF3DC;margin-top:-40px}
.cd2-ring{position:relative;width:150px;height:150px;margin:22px 0 10px}.cd2-ring svg{position:absolute;inset:0;transform:rotate(-90deg)}.cd2-ring circle{fill:none;stroke-width:6}.cd2-ring .bg{stroke:rgba(255,255,255,.12)}.cd2-ring .fg{stroke:#E9B949;stroke-linecap:round;stroke-dasharray:276;stroke-dashoffset:0}
html body .cd2 .qr-num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;margin:0;font:900 5rem/1 Fraunces,Georgia,serif;color:#F3D98B!important}html body .cd2 .qr-num.go{animation:cdPop .6s ease-out both}
.cd2-ring.go{animation:cd2Go .7s ease-out both}.cd2-ring.go .fg{stroke:#3FC25A}html body .cd2-ring.go .qr-num{color:#7EE08F!important;font-size:3.6rem}@keyframes cd2Go{50%{transform:scale(1.15);filter:drop-shadow(0 0 24px rgba(63,194,90,.7))}}
.cd2-r{margin:0;font:700 1rem Nunito,system-ui;color:#C9D3E6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v184 ok')
# pass 2: on GO! the ring fills green
s = open(d + 'yofi-real.html').read()
s = s.replace("else { document.getElementById('cdR').classList.add('go');", "else { document.getElementById('cdR').classList.add('go'); const a = document.getElementById('cdArc'); if (a) { a.style.transition = 'stroke-dashoffset .35s ease-out'; a.style.strokeDashoffset = '0'; }", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v184 pass2 ok')
