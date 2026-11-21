# Real Money build, step 240 (after rmv236.py): simpler "Ready for Cash Races" + clearer Stable card (user request).
#  - Training complete popup: "Congratulations!", the photo with its rosette, "Sterling is ready for cash races", one button
#    "🐎 Go to your stable" (opens the Stable on that photo).
#  - Stable card progress: a photo that lost its qualifier and trained shows "Qualifier lost" + "Trained" (was "Qualified").
#  - The card's two buttons sit right under "Now". The green button is the waiting cash challenge when there is one
#    ("⚔️ Accept @name's $2 challenge"), otherwise "⚔️ Head-to-head · $2–$20". The challenge row keeps its text, no extra button.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""function crReady(p) { if (!p || p.crSeen) return; p.crSeen = 1; save(); const nm = esc(rcName(p));
  popOpen(`<div class="pp qfx nv qw crr2"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big">Congratulations!</h2><i class="nv-sw"></i>
    <div class="qw-ph"><img src="${p.src}" alt=""></div>
    <p class="crr2-t">${nm} is ready for<br><b>cash races</b></p><p class="qw-o">${TQ_WIN} training wins · it’s in your stable</p>
    <button class="btn block nv-go" id="crrS">🐎 Go to your stable</button></div>`);
  try { rvConfetti(document.querySelector('.crr2'), 140); } catch (e) {}
  $('#crrS').onclick = () => { popClose(); window.__ptab = 'stable'; window.__stFocus = p.id; window.__stNote = `🎉 ${nm} is ready for cash races`; finalsTab(); }; }
(() => { const sl = stLadder; stLadder = function (p) { let h = sl.apply(this, arguments); try { const q = p.ql || {}, T = p.tq || { w: 0, l: 0 };
    if (q.done === 'x' && isCashOK(p)) h = h.replace('<span class="">✓ 🎀 Qualified</span>', `<span class="x">✕ 🎀 Qualifier lost ${q.w || 0}–${q.l || 0}</span><span class="">✓ 🏋️ Trained</span>`);
    h = h.replace(/<button class="ld-b" data-ldc>See<\/button>/, '<em>WAITING</em>'); } catch (e) {} return h; }; })();
(() => { const sh = stHero; stHero = function (p) { let h = sh.apply(this, arguments); try { const C = (() => { try { return chList().filter(c => c.pid === p.id); } catch (e) { return []; } })(), c = C[0];
    if (c) h = h.replace(/<button class="btn sx-ol" data-sth="[^"]*" data-m="c">[\s\S]*?<\/button>/, `<button class="btn sx-ol" data-chy="${c.id}">⚔️ Accept ${esc(c.h)}’s $${c.fee} challenge</button>`);
    const t = document.createElement('div'); t.innerHTML = h; const now = t.querySelector('.pg-now'), btns = t.querySelector('.sx-btns'); if (now && btns) { btns.classList.add('sx-btns-now'); now.insertAdjacentElement('afterend', btns); } if (c) { const g = t.querySelector('.pg-goal'); if (g) g.parentNode.removeChild(g); } h = t.innerHTML; } catch (e) {} return h; }; })();
function fcNotify() {""")
s = s.replace('</style>', """.crr2{text-align:center}.crr2 .nv-big{font-size:2.1rem!important}html body .nv.qw.crr2 .qw-ph{width:62%!important;margin-left:auto!important;margin-right:auto!important}
.crr2-t{margin:14px 0 4px;font:800 1.25rem/1.25 Nunito,system-ui;color:#FBF3DC}.crr2-t b{font:900 2rem/1.1 Fraunces,Georgia,serif;color:#F3D98B}.crr2 #crrS{margin-top:18px!important}
html body #flow .sx .sx-btns.sx-btns-now{margin:10px 0 4px!important;padding:0!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v237 ok')
