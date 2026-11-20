# Real Money build, step 206 (after rmv202.py): one "Welcome back" screen; reopen on Vote; My Photos fixes.
#  - Returning after 20+ minutes: ONE navy "Welcome back" screen listing what's waiting, best first:
#      rematch ready → Final waiting (or steps to the Final) → challenges → today's reward.
#    Each row has its own button. The separate "While you were away" and Daily Rewards popups no longer stack on return.
#    If nothing but the daily reward is waiting, the normal daily popup shows instead.
#  - The app reopens on the Vote tab (where the rematch / Final buttons live).
#  - My Photos: no "$0.00 won" banner before a first win; a photo waiting for its rematch shows the live state
#    ("Rematch ready · race it" or "Free rematch in 1:20").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""window.__awayMs = (() => { try { return S && S.seenAt ? Date.now() - S.seenAt : 0; } catch (e) { return 0; } })();
function wbRows() { const P = S.photos || [], R = [];
  P.filter(p => rmqReady(p)).forEach(p => R.push(`<div class="wbk-r"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}’s rematch is ready</b><small>A new live race for a place in the Final</small></div><button class="btn wbk-b" data-rmg="${p.id}">🏁 Race</button></div>`));
  P.filter(p => p.fin).forEach(p => { const fr = p.fr || { s: 0 }, free = !S.coinFin && (S.gems || 0) >= FIN_COINS;
    R.push(fr.go ? `<div class="wbk-r"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}’s Final is waiting</b><small>${free ? `Your first Final is free with ${FIN_COINS} coins` : '1st wins up to ' + money(20 * QF_PAY[0])}</small></div><button class="btn wbk-b" data-wbf="${p.id}">🏁 Enter</button></div>`
      : `<div class="wbk-r"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))} is qualified</b><small>${Math.min(QS_STEPS, fr.s || 0)} of ${QS_STEPS} steps to the Final</small></div><button class="btn wbk-b nv2" data-wbv>⚖️ Vote</button></div>`); });
  P.filter(p => rmqWait(p) && !rmqReady(p)).forEach(p => R.push(`<div class="wbk-r"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><small>Free rematch in <span class="rm-t" data-until="${p.rmAt}">${rmqFmt(p.rmAt)}</span></small></div><button class="btn wbk-b nv2" data-wbv>⚖️ Vote</button></div>`));
  return R; }
function wbShow() { const R = wbRows(), C = chList(); if (!R.length && !C.length) return false; window.__wbShown = 1; let dr = '';
  try { const ds = dailyState(); if (!ds.doneToday) { ds.D.hello = ds.sk; save(); dr = `<div class="wbk-r day"><span class="wbk-ic">🎁</span><div><b>Today’s reward</b><small>Vote on 3 photos for +15 coins</small></div><button class="btn wbk-b nv2" data-wbv>⚖️ Vote</button></div>`; } } catch (e) {}
  popOpen(`<div class="pp qfx nv chw wbk"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big sm">Welcome back</h2><i class="nv-sw"></i><p class="qw-o">Here’s what’s waiting for you.</p>
    <div class="wbk-l">${R.join('')}</div>${C.length ? `<p class="nv-rule"><span>⚔️ ${C.length} challenge${C.length > 1 ? 's' : ''}</span></p><div class="cg-l">${C.map(chRow).join('')}</div>` : ''}${dr ? `<div class="wbk-l">${dr}</div>` : ''}
    <div style="text-align:center"><button class="link nv-later" id="chL">Later</button></div>${C.length ? '<p class="nv-sim">Demo · challengers are simulated</p>' : ''}</div>`);
  $('#chL').onclick = () => popClose(); return true; }
function chAway() { if (!window.__wbShown) wbShow(); }
document.addEventListener('click', e => { const f = e.target.closest && e.target.closest('[data-wbf]'), v = e.target.closest && e.target.closest('[data-wbv]'); if (!f && !v) return; e.preventDefault(); try { popClose(); } catch (x) {}
  if (f) { const p = (S.photos || []).find(x => x.id === f.dataset.wbf); if (p) qfStart(p); } else { go('judge'); renderJudge(); } });
(() => { const sh = streakHello; streakHello = function () { if (window.__wbShown || (window.__awayMs > 20 * 60000 && Date.now() - (window.__bootAt || 0) < 12000)) return; return sh.apply(this, arguments); }; })();
window.__bootAt = Date.now();
setTimeout(() => { try { if (!S || !S.user || !$('#app').classList.contains('on')) return;
    if (!document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on')) { go('judge'); renderJudge(); }
    if (window.__awayMs > 20 * 60000) { let n = 0; const t = setInterval(() => { if (++n > 12) { clearInterval(t); return; } if (window.__wbShown) { clearInterval(t); return; } if (!$('#app').classList.contains('on') || document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on')) return; clearInterval(t); wbShow(); }, 700); } } catch (e) {} }, 2300);
(() => { const ts = twStatus; twStatus = function (p) { if (rmqWait(p)) return rmqReady(p) ? { t: '🏁 Rematch ready · race it', a: 'v', c: 'q' } : { t: `⏱ Free rematch in ${rmqFmt(p.rmAt)}`, a: 'v', c: 'x' }; return ts.apply(this, arguments); }; })();
(() => { const rm = renderMyShow; renderMyShow = function () { const r = rm.apply(this, arguments); try { const tot = (S.earn || []).reduce((a, e) => a + (e.amt || 0), 0), b = document.querySelector('#gallery .tw-bank');
    if (b && !tot) b.innerHTML = '<span>Your trophy wall</span><small style="display:block;margin-top:4px;font-size:.9rem">Cash your photos win shows here.</small>'; } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.wbk-l{display:grid;gap:8px;margin:10px 0}.wbk-r{display:flex;align-items:center;gap:10px;padding:10px;border-radius:14px;background:#FBF6EE;text-align:left}.wbk-r img{width:52px;height:52px;border-radius:10px;object-fit:cover;flex:none;box-shadow:0 0 0 2px #D9AE4F}
.wbk-ic{width:52px;height:52px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;background:#FFF1C9;flex:none}.wbk-r div{flex:1;min-width:0}.wbk-r b{display:block;font:800 .95rem Nunito,system-ui;color:#14213D}.wbk-r small{font:600 .78rem Nunito,system-ui;color:#5B4A3F}
html body .wbk .btn.wbk-b{width:auto!important;min-height:42px!important;margin:0!important;padding:0 14px!important;border-radius:999px!important;background:linear-gradient(180deg,#2F8A3F,#1F6A2E)!important;color:#fff!important;font:800 .9rem Nunito,system-ui!important;box-shadow:none!important;white-space:nowrap}
html body .wbk .btn.wbk-b.nv2{background:linear-gradient(180deg,#22325A,#14213D)!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v203 ok')
# pass 2: tighter row text
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .wbk-r small{display:block;line-height:1.3!important;margin-top:2px}html body .wbk-r b{line-height:1.2}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v203 pass2 ok')
