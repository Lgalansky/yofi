# Real Money build, step 90 (after rmv86.py): the free pick unlock goes through a guided coins menu.
#  "🎟️ Free pick unlocked!" → "Open my coins" → the coins menu opens with a one-line intro
#  ("This is your coins menu. Coins get you free Final picks and frame your photos."), the Free Final pick row first with a
#  gold highlight and gentle pulse, other rows dimmed → tap the row → pick screen. Two taps, and the player learns where
#  free picks come from.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("cta: '🎟️ Make my free pick', onCta: () => { closeFlow(); ppOpen(); }",
   "cta: '🟡 Open my coins', onCta: () => { closeFlow(); coinTour(); }")
s = s.replace("function fcNotify() {", r"""function coinTour() { useGems(); setTimeout(() => { const B = document.getElementById('sheetBody'); if (!B) return; const rows = [...B.querySelectorAll('.ug-r')], hl = rows.find(r => /Free (ticket|Final pick)/i.test(r.innerText));
    const sub = B.querySelector('.ug .sub'); if (sub) sub.insertAdjacentHTML('afterend', '<p class="ug-tour">👋 This is your coins menu. Coins get you <b>free Final picks</b> and <b>frame your photos</b>. Tap your free pick to use it.</p>');
    if (hl) { const box = hl.parentElement, first = box.querySelector('.ug-r'); if (first && first !== hl) box.insertBefore(hl, first); hl.classList.add('ug-hl'); rows.forEach(r => { if (r !== hl) r.classList.add('ug-dim'); }); } }, 60); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.ug-tour{margin:4px 0 12px;padding:10px 12px;border-radius:14px;background:#E3EAF5;color:#1E3A6E;font-size:.92rem;line-height:1.35}.ug-tour b{color:#14213D}
html body #sheetBody .ug-r.ug-hl{box-shadow:inset 0 0 0 2.5px #D9AE4F,0 8px 18px -10px rgba(217,174,79,.8)!important;background:#FFF8E6!important;animation:ugPulse 1.6s ease-in-out infinite}
@keyframes ugPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}html body #sheetBody .ug-r.ug-dim{opacity:.45}
@media (prefers-reduced-motion:reduce){html body #sheetBody .ug-r.ug-hl{animation:none}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v87 ok')
