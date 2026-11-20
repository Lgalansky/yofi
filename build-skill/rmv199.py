# Real Money build, step 202 (after rmv198.py): every photo you pick gets named and framed.
#  Picking 2+ photos: the first goes through the normal flow; then each extra photo gets its own step —
#  "📷 Photo 2 of 2 · Name and frame it" (photo in the gold frame, a name field, "Frame & enter · free"),
#  the "Framed!" reveal, and only then does it join the race. After the last one you land on the Vote screen
#  ("2 photos in play"). Extra photos are no longer auto-named "Photo 2" and entered silently.
#  Extra photos wait in memory until named; if you stay in the app the Vote screen shows "Name and frame your photo".
#  Closing the app before naming drops the unnamed extras (they were never entered).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("framed: Date.now(), title: `Photo ${S.photos.length + 1}` };\n        S.photos.push(p); qlStart(p); n++;",
   "framed: 0, xq: 1, title: '' };\n        (window.__xq = window.__xq || []).push(p); n++;")
RA("toast(`📷 ${n} more photo${n > 1 ? 's' : ''} added to your stable and entered`)", "toast(`📷 ${n} more photo${n > 1 ? 's' : ''} to name and frame next`)")
s = s.replace("function fcNotify() {", r"""const xqList = () => (window.__xq || []).filter(p => !p.framed);
function xqNext() { const Q = xqList(); if (!Q.length) { try { popClose(); } catch (e) {} go('judge'); renderJudge(); const n = pvList().length; if (n > 1) toast(`📷 ${n} photos in play`); return; }
  const p = Q[0], total = (window.__xqTot = Math.max(window.__xqTot || 0, Q.length)), idx = total - Q.length + 2;
  popOpen(`<div class="pp qfx qlv xq"><p class="pp-k">📷 Photo ${idx} of ${total + 1}</p><h2 class="db-h">Name and frame it</h2><div class="qlv-ph"><img src="${p.src}" alt=""></div>
    <input class="xq-in" id="xqN" maxlength="28" placeholder="Give it a name" autocomplete="off">
    <button class="btn block db-go" id="xqGo">🖼️ Frame & enter · free</button><div style="text-align:center"><button class="link pc-later" id="xqSkip">Not this photo</button></div></div>`);
  $('#xqGo').onclick = () => { const t = ($('#xqN').value || '').trim().slice(0, 28); p.title = t || `Photo ${S.photos.length + 1}`; p.framed = Date.now(); p.xq = 0; S.photos.push(p); save();
    frameReveal(p, () => { qlStart(p); xqNext(); }); };
  $('#xqSkip').onclick = () => { window.__xq = window.__xq.filter(x => x !== p); xqNext(); }; }
(() => { const ud = upDone; upDone = function (p) { const has = xqList().length; if (has) S.ask2 = 1; const r = ud.apply(this, arguments);
  try { if (has) { window.__xqTot = xqList().length; const b = document.getElementById('qsJ'); if (b) { b.textContent = `📷 Next: name photo 2`; b.onclick = () => { popClose(); setTimeout(xqNext, 200); }; } } } catch (e) {} return r; }; })();
(() => { const qs = qlStripHTML; qlStripHTML = function () { let h = qs.apply(this, arguments); try { const Q = xqList(); if (Q.length && !document.querySelector('#coach.on')) { const card = `<button class="xq-card" data-xqn><img src="${Q[0].src}" alt=""><span><b>Name and frame your photo</b><small>${Q.length > 1 ? `${Q.length} photos are waiting` : 'It joins the race once it’s framed'}</small></span><em>›</em></button>`;
    h = h.replace(/<\/div>\s*$/, card + '</div>'); } } catch (e) {} return h; }; })();
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-xqn]'); if (b) { e.preventDefault(); window.__xqTot = xqList().length; xqNext(); } });
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .xq-in{display:block;width:100%;box-sizing:border-box;margin:4px 0 12px;padding:13px 14px;border:0;border-radius:14px;background:#FBF6EE;box-shadow:inset 0 0 0 2px #D9AE4F;font:700 1.05rem Nunito,system-ui;color:#14213D;text-align:center}
.xq-card{display:flex;align-items:center;gap:10px;width:100%;margin:8px 0 0;padding:8px 12px;border:0;border-radius:14px;background:#FFF8E6;box-shadow:inset 0 0 0 2px #D9AE4F;cursor:pointer;text-align:left;font:inherit}
.xq-card img{width:46px;height:46px;border-radius:10px;object-fit:cover}.xq-card span{flex:1}.xq-card b{display:block;font:800 .95rem Nunito,system-ui;color:#14213D}.xq-card small{font:600 .78rem Nunito,system-ui;color:#5B4A3F}.xq-card em{font-style:normal;font-size:1.4rem;color:#14213D}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v199 ok')
