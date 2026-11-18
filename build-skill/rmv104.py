# Real Money build, step 107 (after rmv103.py): a winning effect on every vote you call right.
#  Your photo gets a pulsing gold glow and a sparkle burst, a big "+5" (or "+15 · streak ×3") floats up from it, and the
#  coins fly from the photo to your balance with the coin burst. A miss stays quiet (fill + percentages only).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (earn) setTimeout(() => paintGems(), 500);", "if (earn) setTimeout(() => gemExplosion(earn, { mid: true, from: mc }), 450);")
RA("  try { if (agree && navigator.vibrate) navigator.vibrate(18); } catch (e) {}",
   """  try { if (agree && navigator.vibrate) navigator.vibrate(18); } catch (e) {}
  if (agree) { const mc = cards[pick]; mc.classList.add('cfx-win'); mc.insertAdjacentHTML('beforeend', `<span class="cfx-sp">${[...Array(14)].map((_, k) => `<i style="--a:${k * 26}deg;--d:${(k % 3) * .06}s"></i>`).join('')}</span>${combo >= 2 ? `<span class="cfx-plus"><small>🔥 ${combo} in a row</small></span>` : ''}`); }""")
s = s.replace('</style>', """html body #judge .tot-c.cfx-win{box-shadow:0 0 0 4px #E9B949,0 0 26px 4px rgba(233,185,73,.75)!important;animation:cfxGlow .9s ease-in-out 2}
@keyframes cfxGlow{50%{box-shadow:0 0 0 5px #F3D98B,0 0 40px 10px rgba(243,217,139,.85)}}
.cfx-sp{position:absolute;left:50%;top:45%;width:0;height:0;z-index:7;pointer-events:none}.cfx-sp i{position:absolute;width:9px;height:9px;margin:-4px;border-radius:2px;background:#F3D98B;box-shadow:0 0 8px #FFE9A8;transform:rotate(var(--a)) translateY(0) scale(.4);opacity:0;animation:cfxSp .8s var(--d) ease-out forwards}
.cfx-sp i:nth-child(3n){background:#fff;width:6px;height:6px}.cfx-sp i:nth-child(4n){background:#E9B949;border-radius:50%}
@keyframes cfxSp{15%{opacity:1}100%{transform:rotate(var(--a)) translateY(-95px) scale(1);opacity:0}}
.cfx-plus{position:absolute;left:0;right:0;top:74%;z-index:8;text-align:center;pointer-events:none;font:900 2.6rem/1 Fraunces,Georgia,serif;color:#F3D98B;-webkit-text-fill-color:#F3D98B;text-shadow:0 2px 0 #8A5E16,0 4px 14px rgba(0,0,0,.55);opacity:0;animation:cfxPlus 1.3s .15s ease-out forwards}
.cfx-plus small{display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(20,33,61,.75);font:800 1rem Nunito,system-ui,sans-serif;color:#fff;-webkit-text-fill-color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.6)}
@keyframes cfxPlus{0%{opacity:0;transform:translateY(16px) scale(.6)}25%{opacity:1;transform:translateY(0) scale(1.15)}45%{transform:scale(1)}100%{opacity:0;transform:translateY(-38px)}}
@media (prefers-reduced-motion:reduce){.cfx-sp{display:none}.cfx-plus,html body #judge .tot-c.cfx-win{animation:none}.cfx-plus{opacity:1}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v104 ok')
