# Real Money build, step 86 (after rmv82.py): a new player's first Final result pushes "add your photo and win".
#  On the first free-pick result (and the guarantee pick's result) the "Your photo could win real cash" card moves up,
#  straight under the result line, with the next Final for their photo ("Your first frame is free · next: 7am Pets,
#  $912 pool"). The cash upsell is held back on that screen. If the guarantee pick is offered, it stays on top.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (S.tut === 3 && e.free && !prize && !S.fg)",
   """if (S.tut === 3) { const cw = document.querySelector('#coach .cw2'), cb = document.querySelector('#coach .fr2-cash'); if (cw && cb) { cb.insertAdjacentElement('afterend', cw); cw.classList.add('cw2-first'); const nx = ppSlot() + 1, G = ppGame(nx);
      cw.querySelector('.cw2-h').insertAdjacentHTML('beforebegin', `<span class="cw2-pill">📷 Your turn: add a photo</span>`);
      cw.querySelector('.cw2-go').insertAdjacentHTML('beforebegin', `<p class="cw2-nx">Next Final for your photo: <b>${raceName(nx)} ${esc(showName(G.k))}</b> · <b class="g">${ppPool(G.players)} pool</b></p>`); }
    document.querySelectorAll('#coach .up-box, #coach #ppReal1, #coach #ppReal2').forEach(x => x.remove()); }
  if (S.tut === 3 && e.free && !prize && !S.fg)""")
RA('function rvConfetti(el, n) {', 'function rvConfetti(el, n) { if (!el) return;')
s = s.replace('</style>', """.cw2-first{box-shadow:inset 0 0 0 2.5px #D9AE4F,0 10px 24px -14px rgba(20,33,61,.45)!important}.cw2-pill{display:inline-block;margin:0 0 8px;padding:4px 14px;border-radius:999px;background:#1E3A6E;color:#fff;font-weight:800;font-size:.8rem;letter-spacing:.04em}
html body .ppop .cw2-pill{color:#fff!important;-webkit-text-fill-color:#fff}.cw2-nx{margin:0 0 10px;font-size:.92rem}html body .ppop .cw2-nx b.g{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v83 ok')
