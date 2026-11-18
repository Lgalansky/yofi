# Real Money build, step 64 (after rmv60.py): Final result creator card from the user's mock-up.
#  "Your photo could win real cash" / "Enter your photo. Reach the Final. Get paid." / winner card (photo, @handle, $ earned,
#  "earned with “title”") / "6 photo creators shared $93 in this Final" / two steps / navy "Enter your photo — free".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
I = lambda p: '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>'
PIC = I('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="15.5" cy="9.5" r="1.6"/><path d="M4 17l5-5 4 4 2.5-2.5L20 17"/>')
CUP = I('<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8.5 20h7M9.5 17h5"/>')
CAM = '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2.5L9 5h5"/><circle cx="11.5" cy="13" r="3.2"/><path d="M19 3v5M16.5 5.5h5"/></svg>'
RA('<p class="fr2-cr">6 photo creators shared ${money(n * RACE_AVG * .1)}</p>\n', '')
i = s.index('<div class="tut-up">${(() => { const w = g.ph[g.ord[0]];'); j = s.index('</div>` : \'\'}', i) + len('</div>')
s = s[:i] + r"""<div class="cw2"><h3 class="cw2-h">Your photo could win real cash</h3><p class="cw2-t"><span></span>Enter your photo. Reach the Final. Get paid.<span></span></p>
      ${(() => { const w = g.ph[g.ord[0]]; return w ? `<div class="cw2-win"><img src="${w.src}" alt=""><div><p class="cw2-k">🏆 This Final’s winner</p><p class="cw2-hd">@${esc(w.h)}</p><b class="cw2-amt">${money(finShare(g.sl, 1))}</b><p class="cw2-by">earned with “${esc(w.t)}”</p></div></div>` : ''; })()}
      <p class="cw2-t"><span></span>6 photo creators shared ${money(n * RACE_AVG * .1).replace('.00', '')} in this Final<span></span></p>
      <div class="cw2-st"><div>""" + PIC + r"""<p><b>Finish in the top 2</b>in your category’s qualifier.</p></div><div>""" + CUP + r"""<p><b>Every finalist gets paid</b>Your photo doesn’t have to finish first.</p></div></div>
      <button class="btn block cw2-go" id="ppUp">""" + CAM + r""" Enter your photo${frameFree() ? ' — free' : ''}</button><p class="cw2-f">${frameFree() ? 'Your first photo entry is free.' : `Framing a photo costs ${FRAME_COINS} coins.`}</p></div>""" + s[j:]
s = s.replace('</style>', """html body .ppop .cw2{background:#FBF6EE!important;border-radius:22px;box-shadow:inset 0 0 0 1.5px #E2C27A;padding:20px 14px 14px;margin:14px 0 10px;text-align:center}
html body .ppop .cw2-h{font:800 2rem/1.05 Fraunces,Georgia,serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:0 0 8px}
.cw2-t{display:flex;align-items:center;gap:10px;font-style:italic;color:#1E3A6E;margin:0 0 12px;font-size:.84rem;white-space:nowrap}.cw2-t span{flex:1;min-width:12px;height:1.5px;background:#D9B25E}.cw2-t+.cw2-st{margin-top:0}
.cw2-win{display:flex;gap:12px;align-items:center;background:#FFFDF8;border-radius:16px;box-shadow:inset 0 0 0 1.5px #EAD7A8;padding:10px;margin:0 0 14px;text-align:left}.cw2-win img{width:44%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;flex:none}
.cw2-k{margin:0;font-weight:900;font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:#14213D}.cw2-hd{margin:2px 0 0;font-size:.95rem}html body .ppop .cw2-amt{display:block;font:900 2.1rem/1.05 Fraunces,Georgia,serif;color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}.cw2-by{margin:0;font-style:italic;font-size:.84rem}
.cw2-st{text-align:left;margin:0 0 14px}.cw2-st>div{display:flex;align-items:center;gap:14px;padding:10px 4px;color:#14213D}.cw2-st>div+div{border-top:1px solid #EAD7A8}.cw2-st svg{flex:none}.cw2-st p{margin:0;padding-left:14px;border-left:2px solid #D9B25E;font-size:.9rem}.cw2-st b{display:block;font:800 1.15rem Fraunces,Georgia,serif;color:#14213D}
html body .ppop .btn.cw2-go{display:flex;align-items:center;justify-content:center;gap:10px;background:#1E3A6E!important;color:#fff!important;font-size:1.1rem!important}.cw2-f{margin:8px 0 0;font-style:italic;font-size:.88rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v61 ok')
