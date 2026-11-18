# Real Money build, step 92 (after rmv88.py):
#  - Vote screen: the leftover "Your photo · 58 / 70 goal · Touch up" card is gone (no scores, no touch-ups).
#  - The Gallery tab always shows the new Gallery. The old "Today's photo challenges" page could appear when a path sent
#    the player to the Gallery pane through the old renderer.
#  - Framing is a big reveal: dark stage, the photo fades in, a thick carved gold frame closes round it, a brass plaque
#    with the photo's name and category slides up, a shine sweeps across, confetti. "See your photo framed" →
#    Continue → "<name> is in the qualifiers!".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const waitingPhoto = () =>", "const waitingPhoto = () => null; const waitingPhotoOld = () =>")
RA("function renderGallery()", "function renderGallery() { if (typeof renderMyShow === 'function') return renderMyShow(); return renderGalleryOld(); }\nfunction renderGalleryOld()")
RA("p.title = nm; p.framed = Date.now(); S.ffDone = 1; save(); popClose(); showEnter(p.id, 1); if (then) then(); };",
   "p.title = nm; p.framed = Date.now(); S.ffDone = 1; save(); popClose(); setTimeout(() => frameReveal(p, () => { showEnter(p.id, 1); if (then) then(); }), 200); };")
s = s.replace("function fcNotify() {", r"""function frameReveal(p, done) { const SH = SHOWS.find(z => z.k === photoShow(p));
  popOpen(`<div class="pp frv"><p class="frv-k">🖼️ Framed!</p><h2 class="frv-h">See your photo framed</h2>
    <div class="frv-stage"><div class="frv-frame"><div class="frv-mat"><img src="${p.src}" alt=""></div><i class="frv-shine"></i></div>
      <div class="frv-plaque"><b>${esc(p.title || rcName(p))}</b><small>${SH ? esc(SH.n) : ''} · ${new Date().toLocaleDateString([], { day: 'numeric', month: 'short', year: 'numeric' })}</small></div></div>
    <p class="frv-s">Your photo is ready to race in the qualifiers.</p><button class="btn block frv-go" id="frvGo">Continue →</button></div>`);
  const box = document.querySelector('#coach .frv'); setTimeout(() => { if (box) rvConfetti(box, 60); }, 1700);
  $('#frvGo').onclick = () => { popClose(); setTimeout(done, 200); }; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #coach .cpr:has(.frv){background:#14213D!important;box-shadow:0 0 0 2.5px #D9AE4F,0 20px 40px -18px rgba(0,0,0,.6)!important}html body #coach .pp.frv{text-align:center;background:radial-gradient(circle at 50% 38%,#2A3F6B 0,#14213D 70%)!important;color:#fff;overflow:hidden;position:relative}
.frv-k{margin:2px 0 0;font-weight:900;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem;color:#F3D98B}html body #coach .frv .frv-h{font:800 1.9rem/1.1 Fraunces,Georgia,serif;color:#fff!important;-webkit-text-fill-color:#fff;margin:4px 0 14px;opacity:0;animation:frvIn .5s 2s forwards}
.frv-stage{position:relative;width:min(78vw,280px);margin:0 auto 14px}
.frv-frame{position:relative;padding:18px;border-radius:6px;background:linear-gradient(135deg,#F6E3A1 0%,#C9962E 22%,#8A5E16 38%,#E9C46A 52%,#A9771F 70%,#F3D98B 86%,#9B6B1A 100%);box-shadow:inset 0 0 0 3px #6E4A10,inset 0 0 0 7px #E8C46A,inset 0 0 0 9px #7A5212,0 18px 40px -12px rgba(0,0,0,.7);transform:scale(1.25);opacity:0;animation:frvFrame .8s .6s cubic-bezier(.2,1.3,.4,1) forwards}
.frv-mat{padding:10px;background:#F6EEDC;box-shadow:inset 0 2px 6px rgba(0,0,0,.35)}.frv-mat img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;opacity:0;animation:frvIn .5s .1s forwards}
.frv-shine{position:absolute;inset:0;border-radius:6px;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.55) 50%,transparent 65%);background-size:250% 100%;background-position:150% 0;pointer-events:none;animation:frvShine 1.1s 1.7s ease-in-out forwards}
.frv-plaque{position:relative;margin:-14px auto 0;display:inline-block;min-width:62%;padding:8px 18px 7px;border-radius:5px;background:linear-gradient(#F0D88F,#C9A24E 55%,#B08A36);box-shadow:inset 0 0 0 1.5px #8A6420,inset 0 1px 0 rgba(255,255,255,.6),0 6px 14px -6px rgba(0,0,0,.6);transform:translateY(24px);opacity:0;animation:frvPlq .5s 1.3s cubic-bezier(.2,1.4,.4,1) forwards}
.frv-plaque b{display:block;font:800 1.15rem Fraunces,Georgia,serif;color:#3B2A12}.frv-plaque small{font-size:.74rem;color:#5A4220;letter-spacing:.03em}
.frv-s{color:#DCE5F4;margin:0 0 12px;opacity:0;animation:frvIn .5s 2.1s forwards}html body #coach .frv .btn.frv-go{background:#D9AE4F!important;color:#14213D!important;opacity:0;animation:frvIn .4s 2.3s forwards}
@keyframes frvIn{to{opacity:1}}@keyframes frvFrame{to{transform:scale(1);opacity:1}}@keyframes frvPlq{to{transform:none;opacity:1}}@keyframes frvShine{to{background-position:-50% 0}}
@media (prefers-reduced-motion:reduce){.frv *{animation-duration:.01s!important;animation-delay:0s!important}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v89 ok')
