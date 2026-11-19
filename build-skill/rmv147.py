# Real Money build, step 150 (after rmv146.py): creative-director fun pass.
#  1. Race theatre: "3 · 2 · 1 · GO!" on the track before pair 1; a live caller line under the track ("You take the
#     lead!", "Neck and neck with @tom!", "Final stretch!"); bigger horses; a white "📸 PHOTO FINISH" flash before the
#     result.
#  2. Verdict drama: the % counts up from 0 with a meter that shows the 60% Play Pool line; the "better than" line and
#     the Play Pool result appear after the count, then confetti.
#  3. My Photos: a brand-new photo no longer shows four boxes of zeros ("🆕 Fresh entry · its record starts with its
#     first contest"); Play Pool photos show a pulsing live dot.
#  4. Play tab: each game shows a live "● 142 playing" count (simulated).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# 1 race
RA('id="dbTrk">${lanes()}<i class="db-fin"></i></div>', 'id="dbTrk">${lanes()}<i class="db-fin"></i><b class="db-cd" id="dbCd"></b></div><p class="db-com" id="dbCom">🏁 Under starter’s orders…</p>')
RA("show(); }\nfunction gmStreak(", "raceGo(show); }\nfunction gmStreak(")
RA("try { navigator.vibrate && navigator.vibrate(okk ? 12 : [25, 30, 25]); } catch (e) {} paint(); i++;",
   "try { navigator.vibrate && navigator.vibrate(okk ? 12 : [25, 30, 25]); } catch (e) {} paint(); i++; try { raceCall(R, me, i, DB_N); } catch (e) {}", 2)
RA("clearInterval(clk); gmEnd(mode, t, R, me.ok, DB_N); }", "clearInterval(clk); photoFinish(() => gmEnd(mode, t, R, me.ok, DB_N)); }")
# 2 verdict
RA('<div class="vd-big"><b>${pct}%</b>', '<div class="vd-big"><b class="vd-n" data-to="${pct}">0%</b>')
RA("<p class=\"vd-beat\">Better than", "<div class=\"vd-meter\"><i style=\"--w:${pct}%\"></i><u title=\"Play Pool\"></u></div><p class=\"vd-beat\">Better than")
RA("setTimeout(() => { try { rvConfetti(document.querySelector('.vdx'), 30); } catch (e) {} }, 300);",
   "vdCount(); setTimeout(() => { try { if (p.pool) rvConfetti(document.querySelector('.vdx'), 40); } catch (e) {} }, 1450);")
# 4 play
RA("<small>${g.sub}</small></button>", "<small>${g.sub}</small><em class=\"gmc-live\">${gmLive(k)} playing</em></button>", 2)
s = s.replace("function fcNotify() {", r"""function raceGo(go) { const el = document.getElementById('dbCd'), com = document.getElementById('dbCom'), P = document.getElementById('dbPair'); if (!el) { go(); return; }
  if (P) P.style.visibility = 'hidden'; const seq = ['3', '2', '1', 'GO!']; let k = 0;
  const step = () => { const e2 = document.getElementById('dbCd'); if (!e2) return; if (k < seq.length) { e2.textContent = seq[k]; e2.className = 'db-cd on' + (k === 3 ? ' go' : ''); try { navigator.vibrate && navigator.vibrate(k === 3 ? 30 : 8); } catch (e) {} k++; setTimeout(step, k === 4 ? 450 : 520); }
    else { e2.className = 'db-cd'; if (P) P.style.visibility = ''; if (com) com.textContent = '🏇 And they’re off!'; go(); } };
  step(); }
function raceCall(R, me, i, N) { const c = document.getElementById('dbCom'); if (!c) return; const o = R.slice().sort((a, b) => b.sc - a.sc || a.tm - b.tm), rk = o.indexOf(me) + 1, lead = o[0] === me ? o[1] : o[0], gap = Math.abs(me.sc - lead.sc), nm = x => x.me ? 'You' : '@' + esc(x.h);
  const prev = c.dataset.rk ? +c.dataset.rk : 0; c.dataset.rk = rk; let t;
  if (i >= N) t = '📸 Across the line…'; else if (prev && rk < prev && rk === 1) t = '🔥 You take the lead!'; else if (rk === 1 && gap >= 25) t = `🏇 You’re clear by ${gap} points!`;
  else if (gap <= 6) t = `⚡ Neck and neck with ${nm(lead)}!`; else if (prev && rk < prev) t = `▲ Up to ${ppOrd(rk)}!`; else if (prev && rk > prev) t = `▼ ${nm(o[rk - 2])} slips past you`;
  else if (i === N - 2) t = '🏁 Final stretch: 2 pairs to go!'; else t = rk === 1 ? '🏇 Holding the lead…' : `${nm(o[0])} leads · you’re ${ppOrd(rk)}, ${gap} behind`;
  c.innerHTML = t; c.classList.remove('pop'); void c.offsetWidth; c.classList.add('pop'); }
function photoFinish(then) { const f = document.createElement('div'); f.className = 'pfx'; f.innerHTML = '<b>📸 PHOTO FINISH</b>'; document.body.appendChild(f); try { navigator.vibrate && navigator.vibrate([20, 60, 20]); } catch (e) {}
  setTimeout(() => { then(); }, 900); setTimeout(() => f.remove(), 1400); }
function vdCount() { const el = document.querySelector('#coach .vd-n'); if (!el) return; const to = +el.dataset.to, t0 = Date.now(), D = 1200;
  const tick = () => { const e2 = document.querySelector('#coach .vd-n'); if (!e2) return; const k = Math.min(1, (Date.now() - t0) / D), v = Math.round(to * (1 - Math.pow(1 - k, 3))); e2.textContent = v + '%'; if (k < 1) requestAnimationFrame(tick); else { e2.classList.add('done'); try { navigator.vibrate && navigator.vibrate(15); } catch (e) {} } };
  requestAnimationFrame(tick); }
function gmLive(k) { const r = cpRng(ppHash(k + Math.floor(Date.now() / 90000))), base = { derby: 140, match: 210, gn: 380, streak: 95 }[k] || 100; return Math.round(base * (.8 + r() * .4)); }
(() => { const rm = renderMyShow; renderMyShow = function () { const out = rm.apply(this, arguments);
  try { document.querySelectorAll('#gallery .gx-rec').forEach(x => { const v = [...x.querySelectorAll('b')].map(b => b.textContent.trim()); if (v.every(t => ['$0.00', '0', '–', '-'].includes(t))) x.outerHTML = '<p class="gx-new">🆕 Fresh entry<br><small>Its record starts with its first contest</small></p>'; }); } catch (e) {}
  return out; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.db-trk{position:relative}
html body .db-ln{height:38px!important}html body .db-hs{font-size:1.7rem!important}
.db-cd{position:absolute;inset:0;display:grid;place-items:center;font:900 3.4rem/1 Fraunces,Georgia,serif;color:#F3D98B;-webkit-text-fill-color:#F3D98B;opacity:0;pointer-events:none;text-shadow:0 4px 16px rgba(0,0,0,.5)}
.db-cd.on{animation:cdPop .5s ease-out both}.db-cd.go{color:#7FE08A;-webkit-text-fill-color:#7FE08A}
@keyframes cdPop{0%{opacity:0;transform:scale(2.2)}30%{opacity:1;transform:scale(1)}100%{opacity:.9;transform:scale(.95)}}
.db-com{margin:8px 0 0;text-align:center;font:900 .95rem Nunito,system-ui,sans-serif;color:#14213D;min-height:1.3em}.db-com.pop{animation:stkBump .35s ease-out}
.pfx{position:fixed;inset:0;z-index:2147483600;display:grid;place-items:center;background:#fff;animation:pfx 1.4s ease-out both;pointer-events:none}
.pfx b{font:900 2rem Fraunces,Georgia,serif;color:#14213D;letter-spacing:.04em;animation:pfxT 1.4s ease-out both}
@keyframes pfx{0%{opacity:0}8%{opacity:1}40%{opacity:.92}100%{opacity:0}}@keyframes pfxT{0%{transform:scale(1.4);opacity:0}20%{transform:scale(1);opacity:1}80%{opacity:1}100%{opacity:0}}
.vd-n.done{animation:stkBump .4s ease-out}
.vd-meter{position:relative;height:12px;margin:8px 8% 6px;border-radius:6px;background:#EEE6D8;overflow:visible}.vd-meter i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:6px;background:linear-gradient(90deg,#E9B949,#2F6B3F);animation:vdM 1.2s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes vdM{to{width:var(--w)}}.vd-meter u{position:absolute;left:60%;top:-5px;bottom:-5px;width:3px;border-radius:2px;background:#14213D}
.vd-meter u::after{content:'Play Pool';position:absolute;top:-17px;left:50%;transform:translateX(-50%);font:900 .62rem Nunito,system-ui,sans-serif;color:#14213D;white-space:nowrap;text-decoration:none}
.vdx .vd-beat,.vdx .vd-pool{animation:vdIn .45s ease-out 1.3s both}@keyframes vdIn{from{opacity:0;transform:translateY(8px)}}
.gx-new{margin:0;padding:12px;border-radius:12px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #EADCC6;font-weight:900;color:#14213D;text-align:center}.gx-new small{font-weight:600;font-size:.76rem;color:#5B4A3F}
.vd-e::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:#2F9E4F;margin-right:6px;vertical-align:1px;animation:liveDot 1.4s ease-in-out infinite}
@keyframes liveDot{50%{opacity:.25;transform:scale(.7)}}
html body .gmc .gmc-live{font-style:normal;font-size:.7rem;font-weight:800;color:#9FE3AE!important;-webkit-text-fill-color:#9FE3AE;margin-top:4px}
html body .gmc .gmc-live::before{content:'';display:inline-block;width:7px;height:7px;border-radius:50%;background:#5FD37A;margin-right:5px;animation:liveDot 1.4s ease-in-out infinite}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v147 ok')
# pass 2: verdict meter clear of the label; photo stats move out of the narrow plaque into the card's side panel;
#  "Fresh entry" only when a photo has no plays yet (an earning photo just drops the zero boxes).
s = open(d + 'yofi-real.html').read()
RA("x.outerHTML = '<p class=\"gx-new\">🆕 Fresh entry<br><small>Its record starts with its first contest</small></p>'; }); } catch (e) {}",
   "{ const card = x.closest('.gx-card'); x.outerHTML = card && card.querySelector('.vd-e') ? '' : '<p class=\"gx-new\">🆕 Fresh entry<br><small>Its record starts with its first contest</small></p>'; } }); document.querySelectorAll('#gallery .gx-card').forEach(card => { const side = card.querySelector('.gx-side'), L = card.querySelectorAll('.gx-plq .vd-l'); if (side && L.length) { const box = document.createElement('div'); box.className = 'vd-box'; L.forEach(l => box.appendChild(l)); side.prepend(box); } }); } catch (e) {}")
s = s.replace('</style>', """html body .vd-meter{margin-top:24px}
.vd-box{margin:0 0 8px;padding:10px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.vd-box .vd-l{margin:2px 0;font-size:.8rem;line-height:1.35}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v147 pass2 ok')
