# Real Money build, step 158 (after rmv154.py): the Final is a $2 one-on-one duel, watched live while you vote.
#  - Finalist → "🥊 Duel · $2": your photo vs another finalist of similar strength. Both pay $2; winner takes $3.40
#    (2 × $2 less our 15%). Decided by the next 15 crowd votes, shown live in the box at the top of the Vote screen.
#  - Win: $3.40 cash, gold rosette, the photo stays a finalist with a win streak ("🔥 2-duel streak · duel again?").
#  - Lose: the photo keeps its finalist rosette and goes back to your Gallery; enter another photo.
#  - The 6-photo race Final is retired from the path. Wording everywhere says "duel" and $2 / $3.40.
#  Simulated: the opponent and the crowd's votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# wording
RA("Win 8 and it races in a Final for real cash.", "Win 8 and it reaches a Final: a one-on-one duel for real cash.")
RA("Win 8 and it races in a Final for cash.${first ? ' Your first entry is free.' : ''}", "Win 8 and it reaches a Final: a $2 duel, winner takes $3.40.${first ? ' Your first entry is free.' : ''}")
RA("win 8 and it races in a Final for cash.", "win 8 and it reaches a Final: a $2 duel for cash.")
RA("Enter another photo. Win 8 of 15 head-to-heads and it races in a Final.", "Enter another photo. Win 8 of 15 head-to-heads and it reaches a cash Final duel.")
RA('<div class="qf-box">🏁 <b>Race it in a Final</b><br>6 finalists · $1 each · 1st <b>$3.50</b> · 2nd <b>$1.60</b></div>',
   '<div class="qf-box">🥊 <b>Final duel</b><br>Your photo vs another finalist · $2 each · winner takes <b>$3.40</b><br><small>Decided by the next 15 crowd votes. Watch it live while you judge.</small></div>')
RA('<button class="btn block db-go cashb" id="qfGo">🏁 Race ${nm} · $1</button>', '<button class="btn block db-go cashb" id="qfGo">🥊 Duel · $2</button>')
s = s.replace("function fcNotify() {", r"""const DU_FEE = 2, DU_PRIZE = 3.4, DU_V = 15;
const duLive = () => (S.photos || []).find(p => p.du && !p.du.done);
function qfStart(p) { if (duLive()) { toast('🥊 One duel at a time · watch it on the Vote screen'); return; }
  needAge(() => { try { popClose(); } catch (e) {} payCash(DU_FEE, 'A $2 Final duel', () => setTimeout(() => duLobby(p), 250)); }); }
function duLobby(p) { const k = photoShow(p), me = qlStrength(p), pool = ppShuffle(SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src), Math.random).slice(0, 8);
  const pick = pool[0] || { src: p.src, title: 'A rival' }, o = { src: pick.src, t: pick.title || 'A rival', h: '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)], st: me + Math.round((Math.random() - .5) * 12) };
  p.du = { o, a: 0, b: 0, at: Date.now() }; save();
  popOpen(`<div class="pp qfx du-lob"><p class="pp-k">🥊 ${esc(showName(k))} Final · $2 duel</p><h2 class="db-h" id="duH">Finding a finalist to face…</h2>
    <div class="du-vs"><div class="du-c me"><img src="${p.src}" alt=""><b>${esc(rcName(p))}</b><small>You</small></div><span class="du-x">VS</span>
      <div class="du-c" id="duO"><img src="${pool[1] ? pool[1].src : o.src}" alt="" class="spin"><b>…</b><small>&nbsp;</small></div></div>
    <div class="du-pot">Pot <b>$4.00</b> · winner takes <b>${money(DU_PRIZE)}</b></div>
    <button class="btn block db-go" id="duW" disabled>⚖️ Watch it live while you judge</button><p class="db-sim">Prototype: your opponent and the votes are simulated</p></div>`);
  let i = 0; const iv = setInterval(() => { const e = document.querySelector('#duO img'); if (!e) { clearInterval(iv); return; } i++; e.src = (pool[i % pool.length] || o).src;
    if (i >= 9) { clearInterval(iv); e.src = o.src; e.classList.remove('spin'); const c = document.getElementById('duO'); c.classList.add('in'); c.querySelector('b').textContent = o.t; c.querySelector('small').textContent = o.h;
      $('#duH').textContent = `${rcName(p)} vs ${o.t}`; const w = $('#duW'); w.disabled = false; w.onclick = () => { popClose(); go('judge'); renderJudge(); }; } }, 160); }
function duStep(p, n) { const u = p.du; if (!u || u.done) return; const pv = Math.max(.4, Math.min(.6, .5 + (qlStrength(p) - u.o.st) / 150));
  for (let i = 0; i < (n || 2) && u.a + u.b < DU_V; i++) { if (Math.random() < pv) u.a++; else u.b++; }
  if (u.a + u.b >= DU_V) { u.done = 1; save(); setTimeout(function tr() { if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx')) { setTimeout(tr, 1200); return; } duResult(p); }, 1300); }
  save(); }
function duLiveHTML(p) { const u = p.du, tot = u.a + u.b, pa = tot ? Math.round(u.a / tot * 100) : 50, lead = u.a > u.b ? 'me' : u.b > u.a ? 'them' : '';
  return `<div class="qm du" id="du-${p.id}"><div class="qm-h"><span class="qm-live">● LIVE</span><b>🥊 Final duel</b><em class="du-em">Winner takes ${money(DU_PRIZE)}</em></div>
    <div class="qm-vs"><div class="qm-p me"><img src="${p.src}" alt=""><small>${esc(rcName(p))}</small></div>
      <div class="qm-mid"><div class="qm-sc"><b class="qm-a">${u.a}</b><span>votes</span><b class="qm-b">${u.b}</b></div>
        <div class="qm-bar"><i class="qm-ba" style="width:${pa}%"></i></div><p class="qm-left">${u.done ? '📸 Counting the last votes…' : `⏱ <b>${DU_V - tot}</b> vote${DU_V - tot === 1 ? '' : 's'} to go${lead ? ` · ${lead === 'me' ? 'you lead' : 'you trail'}` : ''}`}</p></div>
      <div class="qm-p"><img src="${u.o.src}" alt=""><small>${esc(u.o.t)}</small></div></div>
    <p class="qm-sim">vs ${esc(u.o.h)} · Prototype: opponent and votes simulated</p></div>`; }
(() => { const qs = qlStripHTML; qlStripHTML = function () { const D = duLive() || (S.photos || []).find(p => p.du && p.du.done && !p.du.shown);
  if (!D) return qs.apply(this, arguments); let h = qs.apply(this, arguments); const div = document.createElement('div'); div.innerHTML = h; let box = div.firstElementChild;
  if (!box.classList.contains('qv')) { box.className = 'qv'; }
  const row = [...box.querySelectorAll('.qv-r')].find(r => r.querySelector('img') && r.querySelector('img').getAttribute('src') === D.src);
  if (row) row.outerHTML = duLiveHTML(D); else box.insertAdjacentHTML('afterbegin', duLiveHTML(D));
  const hd = box.querySelector('.qv-h'); if (hd) hd.remove(); box.classList.remove('cmp'); if (box.querySelectorAll('.qv-r').length) box.classList.add('cmp', 'has-l'); return box.outerHTML; }; })();
(() => { const qp = qlPaint; qlPaint = function () { const D = duLive(), x = D && document.getElementById('du-' + D.id);
  if (x && !D.du.done) { const u = D.du, tot = u.a + u.b, A = x.querySelector('.qm-a'), B = x.querySelector('.qm-b');
    if (A.textContent != u.a) { A.textContent = u.a; A.classList.remove('bp'); void A.offsetWidth; A.classList.add('bp'); }
    if (B.textContent != u.b) { B.textContent = u.b; B.classList.remove('bp'); void B.offsetWidth; B.classList.add('bp'); }
    x.querySelector('.qm-ba').style.width = (tot ? Math.round(u.a / tot * 100) : 50) + '%';
    x.querySelector('.qm-left').innerHTML = `⏱ <b>${DU_V - tot}</b> vote${DU_V - tot === 1 ? '' : 's'} to go${u.a !== u.b ? ` · ${u.a > u.b ? 'you lead' : 'you trail'}` : ''}`;
    const L = (S.photos || []).find(p => p.ql && !p.ql.done); if (!L) return; }
  return qp.apply(this, arguments); }; })();
(() => { const cf = callFx; callFx = function () { const r = cf.apply(this, arguments); try { const D = duLive(); if (D) { duStep(D, 2); qlPaint(); } } catch (e) {} return r; }; })();
setInterval(() => { try { if (!S || !$('#app').classList.contains('on') || document.querySelector('#coach.on')) return; const e = document.getElementById('qlS'); if (!e || !e.offsetParent) return;
  const D = duLive(); if (D) { duStep(D, 1); qlPaint(); } } catch (e) {} }, 2200);
function duResult(p) { const u = p.du; if (u.shown) return; u.shown = 1; const win = u.a > u.b, nm = esc(rcName(p)); window.__nudgeAt = Date.now();
  const R = p.dr = p.dr || { w: 0, l: 0, cash: 0, st: 0 }; R.last = { win, t: u.o.t, src: u.o.src, a: u.a, b: u.b, at: Date.now() };
  if (win) { R.w++; R.st++; R.cash = +(R.cash + DU_PRIZE).toFixed(2); rzAdd(p, 0); p.fin = 1; S.cash = +((S.cash || 0) + DU_PRIZE).toFixed(2); try { earnAdd({ kind: 'f', pid: p.id, t: p.title, amt: DU_PRIZE, place: 1 }); } catch (e) {} }
  else { R.l++; R.st = 0; p.fin = 0; p.raced = { rank: 2, prize: 0, at: Date.now() }; }
  p.du = null; save(); try { qlPaint(); } catch (e) {}
  popOpen(`<div class="pp qfx ${win ? 'won' : ''}"><p class="pp-k">🥊 Final duel · ${u.a}–${u.b}</p><h2 class="db-h">${win ? `${nm} won the duel!` : `“${esc(u.o.t)}” took it`}</h2>
    <div class="du-res"><div class="${win ? 'w' : ''}"><img src="${p.src}" alt="">${win ? `<i class="re-rz">${rosette(0)}</i>` : ''}<b>${u.a}</b></div><span>–</span><div class="${win ? '' : 'w'}"><img src="${u.o.src}" alt=""><b>${u.b}</b></div></div>
    ${win ? `<div class="rv-won"><span>Cash won</span><b>${money(DU_PRIZE)}</b></div><p class="db-s">${R.st >= 2 ? `🔥 <b>${R.st}-duel win streak!</b> ` : ''}${nm} is still a finalist · record <b>${R.w}–${R.l}</b> · <b>${money(R.cash)}</b> won</p>
      <button class="btn block db-go cashb" id="duA">🥊 Duel again · $2</button><div style="text-align:center"><button class="link pc-later" id="duJ">⚖️ Keep judging</button></div>`
    : `<p class="db-s">${u.b - u.a <= 3 ? `So close: decided by <b>${u.b - u.a} vote${u.b - u.a === 1 ? '' : 's'}</b>. ` : ''}${nm} keeps its 🎀 finalist rosette in your Gallery${R.w ? ` · duel record <b>${R.w}–${R.l}</b>` : ''}.</p>
      <button class="btn block db-go" id="duE">📷 Enter another photo</button><div style="text-align:center"><button class="link pc-later" id="duJ">⚖️ Keep judging</button></div>`}
    <p class="db-sim">Prototype: opponent and votes are simulated</p></div>`);
  if (win) setTimeout(() => { try { paintWallet(); cashExplosion(DU_PRIZE, { label: 'Duel won' }); rvConfetti(document.querySelector('.qfx'), 60); } catch (e) {} }, 300);
  if ($('#duA')) $('#duA').onclick = () => qfStart(p); if ($('#duE')) $('#duE').onclick = () => { popClose(); setTimeout(finPick, 200); };
  $('#duJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; }
function vdLine(p) { const q = p.ql, R = p.dr; let st = '';
  if (p.du) st = `🥊 <b>Duel live</b> · watch it on the Vote screen`;
  else if (p.fin) st = `🎀 <b>Finalist</b>${R && R.w ? ` · duels ${R.w}–${R.l} · ${money(R.cash)} won` : ''} <button class="btn db-go cashb ql-btn" data-qfr="${p.id}">🥊 Duel · $2</button>`;
  else if (R) st = `🥊 Duels <b>${R.w}–${R.l}</b>${R.cash ? ` · won <b>${money(R.cash)}</b>` : ''}`;
  else if (q && q.done === 'x') st = `Qualifier ${q.w}–${q.l} · out this time`;
  else if (q) st = `🎀 Qualifier <b>${q.w}–${q.l}</b> · ${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'} to a Final`;
  return `<p class="vd-l">${st || 'Not entered yet'}${p.starter ? ' · <em>Starter photo</em>' : ''}</p>`; }
function fcNotify() {""", 1)
# panel rows: finalist / duel record wording
RA("if (p.raced) info = `🏁 Final: <b>${ppOrd(p.raced.rank)}</b>${p.raced.prize ? ` · won <b class=\"cash\">${money(p.raced.prize)}</b>` : ' · rosette kept'}`;\n    else if (p.fin || q.done === 'q') info = `🎀 <b>Finalist!</b> Race it in a Final <button class=\"btn db-go cashb ql-btn\" data-qfr=\"${p.id}\">🏁 Race · $1</button>`;",
   "const R = p.dr;\n    if (p.fin || (q.done === 'q' && !R)) info = `🎀 <b>Finalist${R && R.st ? ` · 🔥 ${R.st} win${R.st > 1 ? 's' : ''} in a row` : '!'}</b> <button class=\"btn db-go cashb ql-btn\" data-qfr=\"${p.id}\">🥊 Duel · $2</button>`;\n    else if (R) info = `🥊 Lost its duel ${R.last ? `${R.last.a}–${R.last.b}` : ''}${R.cash ? ` · won <b class=\"cash\">${money(R.cash)}</b> in total` : ' · rosette kept'}`;\n    else if (p.raced) info = `🏁 Final: <b>${ppOrd(p.raced.rank)}</b>${p.raced.prize ? ` · won <b class=\"cash\">${money(p.raced.prize)}</b>` : ' · rosette kept'}`;")
RA("const q = p.ql, st = p.raced ? 3 : p.fin || q.done === 'q' ? 2 : 1, out = q.done === 'x';", "const q = p.ql, st = (p.dr && p.dr.w) || (p.raced && !p.dr) ? 3 : p.fin || q.done === 'q' ? 2 : 1, out = q.done === 'x';")
RA("<em>🟡 +${p.qc || 0}</em></div>\n      <div class=\"qv-st\">", "<em>${p.dr && p.dr.cash ? `<span class=\"cash\">${money(p.dr.cash)}</span> · ` : ''}🟡 +${p.qc || 0}</em></div>\n      <div class=\"qv-st\">")
RA("${A.filter(p => p.fin).length} ready to race · ${A.filter(p => p.raced).length} raced", "${A.filter(p => p.fin).length} finalist${A.filter(p => p.fin).length === 1 ? '' : 's'} · ${A.filter(p => p.dr).length} duelled")
s = s.replace('</style>', """.qf-box small{display:block;margin-top:3px;font-size:.78rem;color:#3D4A5C}
.du-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;margin:12px 0 8px}.du-c{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 6px;border-radius:14px;background:#F3EEE5;min-width:0}
.du-c img{width:84px;height:84px;border-radius:14px;object-fit:cover;box-shadow:0 0 0 2px #EADCC6}.du-c.me img{box-shadow:0 0 0 3px #2F6B3F}.du-c.in{background:#fff;box-shadow:inset 0 0 0 1.5px #D9AE4F;animation:qsPlus .35s ease-out}
.du-c img.spin{filter:blur(1.5px) saturate(.6)}.du-c b{font:800 .86rem Fraunces,Georgia,serif;color:#14213D;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.du-c small{font:800 .7rem Nunito,system-ui;color:#8A7B6C}
.du-x{font:900 1.3rem Fraunces,Georgia,serif;color:#fff;background:#14213D;border-radius:50%;width:46px;height:46px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #D9AE4F}
.du-pot{margin:4px 0 10px;padding:8px;border-radius:12px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #D9AE4F;font:700 .9rem Nunito,system-ui;color:#5B4A3F}.du-pot b{color:#2F6B3F}
html body .qm.du{background:#14213D;border-radius:14px;padding:8px 10px 6px;margin:0 -4px 4px;box-shadow:0 0 0 2px #D9AE4F}.qm.du .qm-h b{color:#F3D98B}.qm.du .du-em{background:#2F6B3F;color:#fff}
.qm.du .qm-p small,.qm.du .qm-left{color:#C9D3E6}.qm.du .qm-left b{color:#fff}.qm.du .qm-a{color:#9FE3AE}.qm.du .qm-b{color:#F2A08E}.qm.du .qm-sc span{color:#8C9AB5}.qm.du .qm-sim{color:#8C9AB5}.qm.du .qm-p.me img{box-shadow:0 0 0 3px #F3D98B}
.du-res{display:flex;align-items:center;justify-content:center;gap:12px;margin:10px 0}.du-res div{position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;opacity:.6}.du-res div.w{opacity:1}
.du-res img{width:96px;height:96px;border-radius:14px;object-fit:cover;box-shadow:0 0 0 2px #EADCC6}.du-res div.w img{box-shadow:0 0 0 3px #D9AE4F,0 6px 18px rgba(217,174,79,.45)}.du-res b{font:900 1.4rem Fraunces,Georgia,serif;color:#14213D}.du-res>span{font:900 1.3rem Fraunces;color:#B9AE9C}
.du-res .re-rz{position:absolute;top:-14px;right:-14px;width:44px}
.qv-t em .cash{color:#2F6B3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v155 ok')
# pass 2: clearer stake line; the live duel box isn't double-framed when it's the only thing in the panel
s = open(d + 'yofi-real.html').read()
RA('<div class="du-pot">Pot <b>$4.00</b> · winner takes <b>${money(DU_PRIZE)}</b></div>', '<div class="du-pot">You both pay <b>$2</b> · winner takes <b>${money(DU_PRIZE)}</b></div>')
s = s.replace('</style>', """html body .qv:not(:has(.qv-r)):has(.qm.du){background:none;box-shadow:none;padding:0;margin:8px 2px}html body .qv:not(:has(.qv-r)) .qm.du{margin:0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v155 pass2 ok')
