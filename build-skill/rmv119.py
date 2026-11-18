# Real Money build, step 122 (after rmv118.py): three fixes from play-testing.
#  1. "View next Final" after a result used to reopen the race you just watched. It now opens an "Up next" card for the
#     next Final: category, prize pool, "Starts when 6 finalists are in · 3 of 6 in" with a progress bar, the finalists
#     already through, and "Keep voting to choose the finalists" / "Enter your photo".
#  2. Results show as soon as a Final ends: any open pop or the Vote screen is interrupted (only blocked while you're
#     mid-pick, mid-upload or already watching a reveal), checked every second instead of every 3.
#  3. "Enter your photo" from the landing page opens the app's Gallery first, so the iPhone photo picker appears over
#     PhotoPicks, not over the landing page.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("$('#ppNext').onclick = () => { popClose(); raceCard(); };", "$('#ppNext').onclick = () => { popClose(); setTimeout(nextFinalPop, 150); };")
RA("if (!S || !S.pp || busyUI()) return; const now = Date.now();\n  const e = Object.values(S.pp).find(x => !x.done && now >= ppDue(x)); if (e) ppResult(e); }, 3000);",
   "if (!S || !S.pp || resBlocked()) return; const now = Date.now();\n  const e = Object.values(S.pp).find(x => !x.done && now >= ppDue(x)); if (e) { popClose(); try { closeSheet(); } catch (x) {} window.__uiT = 0; ppResult(e); } }, 1000);")
RA("if (!S || !S.races || busyUI()) return;", "if (!S || !S.races || resBlocked()) return;")
RA("if (busyUI() && !document.querySelector('#coach.on .wlv')) return;", "if (resBlocked()) return;")
RA("if ($('#landing').style.display !== 'none' || !$('#app').classList.contains('on')) yWL(); else pickPhoto(true); }); }",
   "if ($('#landing').style.display !== 'none' || !$('#app').classList.contains('on')) { if (!S.user) { S.user = { h: 'guest' + Math.floor(1000 + Math.random() * 9000), guest: 1 }; tutInit(); save(); } openApp(); go('gallery'); try { renderMyShow(); } catch (e) {} } pickPhoto(true); }); }")
s = s.replace("function fcNotify() {", r"""function resBlocked() { return !!document.querySelector('#coach.on #ppGo, #coach.on #ppFree, #coach.on #wpGo, #coach.on #wpFree, #coach.on #gtGo, #coach.on .rv, #coach.on .frv, #coach.on .qs2, #flow.on, #finPick.on, #sheet.on input') || (typeof judging !== 'undefined' && judging); }
function nextFinalPop() { const nx = ppSlot() + 1, G = ppGame(nx), cur = ppSlot(), p = (Date.now() - cur * PP_MS) / PP_MS, n = Math.max(0, Math.min(6, Math.floor(2 + 4 * p)));
  popOpen(`<div class="pp nfx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🎀 Up next</p><h2 class="nfx-h">The ${esc(showName(G.k))} Final</h2>
    <div class="lk-row"><div class="lk-pz"><small>Prize pool so far</small><b>${ppPool(G.players)}</b><span>${G.players} players</span></div><div class="lk-cd"><small>Finalists in</small><b>${n} of 6</b><span>${n >= 6 ? 'starting soon' : 'starts at 6'}</span></div></div>
    <div class="nfx-bar"><i style="width:${Math.round(100 * n / 6)}%"></i></div>
    <div class="nfx-ph">${G.ph.map((ph, i) => i < n ? `<img src="${ph.src}" alt="">` : '<span>?</span>').join('')}</div>
    <p class="pp-i">It starts as soon as 6 photos win their qualifiers. Picks open then.</p>
    <button class="btn block nfx-v" id="nfVote">⚖️ Vote to choose the finalists</button><div style="text-align:center"><button class="link pc-later" id="nfUp">📷 Enter your photo</button></div></div>`);
  $('#nfVote').onclick = () => { popClose(); go('judge'); renderJudge(); }; $('#nfUp').onclick = () => { popClose(); finPick(); }; document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .ppop .nfx-h{font:800 1.8rem/1.1 Fraunces,Georgia,serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:2px 0 10px}
.nfx-bar{height:9px;border-radius:5px;background:#EEE6D8;overflow:hidden;margin:0 0 10px}.nfx-bar i{display:block;height:100%;background:linear-gradient(90deg,#E9B949,#C9962E)}
.nfx-ph{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin:0 0 8px}.nfx-ph img,.nfx-ph span{width:100%;aspect-ratio:1;border-radius:8px;object-fit:cover}.nfx-ph span{display:grid;place-items:center;background:#E3EAF5;color:#1E3A6E;font-weight:900}
html body .ppop .btn.nfx-v{background:#1E3A6E!important;color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v119 ok')
