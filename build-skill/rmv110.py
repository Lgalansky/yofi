# Real Money build, step 113 (after rmv109.py): "Your photo could win real cash" after every quick game.
#  Quick Sprint results now end with the same card as Coin Pick and Final results: headline, "Qualify for the Final" and
#  "Earn a share of 10%" steps, and Enter your photo (free first frame / Enter another photo), above Play again.
#  The Sprint result pop now scrolls when it is taller than the screen.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("${up}<button class=\"bt-cta qs2-go\" id=\"qsAgain\">", "${up}${photoPushHTML('qsUp')}<button class=\"bt-cta qs2-go\" id=\"qsAgain\">")
RA("$('#cpBack').onclick = shut; $('#qsX').onclick = shut; }", "$('#cpBack').onclick = shut; $('#qsX').onclick = shut; if ($('#qsUp')) $('#qsUp').onclick = () => { shut(); finPick(); }; }")
s = s.replace("function fcNotify() {", r"""function photoPushHTML(id) { const I = p => `<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
  return `<div class="cw2 cwq"><h3 class="cw2-h">Your photo could win real cash</h3><p class="cw2-t"><span></span>Qualify for the Final. Earn a share of the prize.<span></span></p>
    <div class="cw2-st"><div>${I('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="15.5" cy="9.5" r="1.6"/><path d="M4 17l5-5 4 4 2.5-2.5L20 17"/>')}<p><b>Qualify for the Final</b>Your photo races the qualifiers to reach the hourly Final.</p></div><div>${I('<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8.5 20h7M9.5 17h5"/>')}<p><b>Earn a share of 10%</b>Every finalist’s creator shares 10% of the Final’s prize pool.</p></div></div>
    <button class="btn block cw2-go" id="${id}">📷 ${frameFree() ? 'Enter your photo — free' : (S.photos || []).some(p => p.framed) ? 'Enter another photo' : 'Enter your photo'}</button><p class="cw2-f">${frameFree() ? 'Your first photo entry is free.' : `Framing a photo costs ${FRAME_COINS} coins.`}</p></div>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #coach .cpr.qs3{max-height:calc(100% - 24px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
html body #coach .qs3 .cwq{background:#FBF6EE!important;border-radius:22px;box-shadow:inset 0 0 0 1.5px #E2C27A;padding:18px 14px 14px;margin:14px 0 12px;text-align:center}
html body #coach .qs3 .cwq .cw2-h{font:800 1.6rem/1.08 Fraunces,Georgia,serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:0 0 8px;text-transform:none!important;background:none!important}
html body #coach .qs3 .cwq p,html body #coach .qs3 .cwq b{color:#14213D!important;-webkit-text-fill-color:#14213D}html body #coach .qs3 .cwq .cw2-st p{color:#2B2320!important;-webkit-text-fill-color:#2B2320}
html body #coach .qs3 .cwq .btn.cw2-go{background:#1E3A6E!important;color:#fff!important;-webkit-text-fill-color:#fff;font:800 1.05rem Fraunces,Georgia,serif!important;border-radius:999px;min-height:52px;width:100%;border:0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v110 ok')
