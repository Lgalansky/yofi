# Real Money build, step 76 (after rmv72.py):
#  - Qualifier result no longer repeats the reveal (crowd's top 3 and your picks removed).
#  - It gains the photo-entry card: "Your photo could win real cash" + two steps + Enter your photo (→ Choose your Final).
#  - Qualifier pick screen: the 1st/2nd/3rd slot row under the photos is gone (the medals on the photos already show your picks).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
def I(p, w=40): return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
PIC = I('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="15.5" cy="9.5" r="1.6"/><path d="M4 17l5-5 4 4 2.5-2.5L20 17"/>')
CUP = I('<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8.5 20h7M9.5 17h5"/>')
CAM = I('<path d="M20 12v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2.5L9 5h5"/><circle cx="11.5" cy="13" r="3.2"/><path d="M19 3v5M16.5 5.5h5"/>', 28)
# remove repeat
i = s.index('<p class="rv-lab rv-rule"><span>${cw} top 3</span></p>'); j = s.index('<div class="g2-thru">', i); s = s[:i] + s[j:]
# photo card before the actions
RA('    ${g2Act(pay)}</div>`);', r"""    <div class="cw2 gq-cw"><h3 class="cw2-h">Your photo could win real cash</h3><p class="cw2-t"><span></span>Enter your photo. Reach the Final. Get paid.<span></span></p>
      <div class="cw2-st"><div>""" + PIC + r"""<p><b>Finish in the top 2</b>in your category’s qualifier, like these two.</p></div><div>""" + CUP + r"""<p><b>Every finalist gets paid</b>Creators share 10% of the Final’s prize pool.</p></div></div>
      <button class="btn block cw2-go" id="gqUp">""" + CAM + r""" ${frameFree() ? 'Enter your photo — free' : (S.photos || []).some(p => p.framed) ? 'Enter another photo' : 'Enter your photo'}</button><p class="cw2-f">${frameFree() ? 'Your first photo entry is free.' : `Framing a photo costs ${FRAME_COINS} coins.`}</p></div>
    ${g2Act(pay)}</div>`); if ($('#gqUp')) $('#gqUp').onclick = () => { popClose(); finPick(); };""")
# pick screen slot row
i = s.index('<div class="g2-sl">'); j = s.index('</div>', s.index('.join(\'\')}', i)) + 6; assert j - i < 600, j - i; s = s[:i] + s[j:]
s = s.replace('</style>', """html body .ppop .gq-cw .cw2-h{font-size:1.7rem!important}.gq-cw{margin-top:12px!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v73 ok')
