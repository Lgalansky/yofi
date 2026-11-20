# Real Money build, step 209 (after rmv205.py): the Daily Cup — coins buy a daily shot at a fixed cash pot.
#  - Lives at the top of the Stable (Play tab): navy banner "🏆 Daily Cup · Tonight 8pm · $100 in prizes · top 25 win".
#  - Enter one race-ready photo for 100 coins (account required). While entered: "Cliff top is 14th of 120 ·
#    top 25 win", moving as you vote.
#  - Prizes (fixed pot, funded by PhotoPicks, not by entries): 1st $30 · 2nd $20 · 3rd $15 · 4th–10th $5 cash ($100);
#    the rest of the top 10% (at least 25 winners in total) win a free $2 Final entry (Bonus Cash).
#  - At 8pm: results. Top 6 race a live Cup Final for their places; everyone else is paid from the leaderboard.
#    Results wait for you on Welcome back. Cup winnings show on My Photos.
#  - Pointers: Welcome back row; a line on the coins sheet.
#  - Demo: "run tonight's Cup now" link so it can be tried without waiting. The field and leaderboard are simulated.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const CUP_COST = 100, CUP_HOUR = 20, CUP_CASH = [30, 20, 15, 5, 5, 5, 5, 5, 5, 5];
const cupDl = () => { const t = new Date(); t.setHours(CUP_HOUR, 0, 0, 0); if (Date.now() >= t.getTime()) t.setDate(t.getDate() + 1); return t.getTime(); };
const cupWin = n => Math.max(25, Math.ceil(n * .1));
const cupPrize = (pl, n) => pl <= CUP_CASH.length ? { cash: CUP_CASH[pl - 1] } : pl <= cupWin(n) ? { bonus: 2 } : null;
const cupSt = () => { const C = S.cup; return !C || C.done ? 'open' : Date.now() >= C.dl ? 'ready' : 'in'; };
const cupLeft = t => { const m = Math.max(0, Math.round((t - Date.now()) / 60000)); return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`; };
function cupMove() { const C = S.cup; if (!C || C.done) return; const p = (S.photos || []).find(x => x.id === C.pid); if (!p) return; C.n = Math.min(180, C.n + Math.floor(Math.random() * 2));
  const tgt = Math.max(.03, Math.min(.92, (88 - qlStrength(p)) / 45)) * C.n; C.pl = Math.max(1, Math.min(C.n, Math.round(C.pl + (tgt - C.pl) * .25 + (Math.random() - .5) * 6))); }
function cupCard() { const st = cupSt(), C = S.cup, R = (S.photos || []).filter(p => isCashOK(p) && !p.starter), g = Math.floor(S.gems || 0); let body;
  if (st === 'ready') body = `<p class="cup-s"><b>Results are in!</b> See where ${esc(rcName((S.photos || []).find(x => x.id === C.pid) || {}))} finished.</p><button class="btn cup-b" data-cup="res">🏆 See your result</button>`;
  else if (st === 'in') { const p = (S.photos || []).find(x => x.id === C.pid) || {}, w = cupWin(C.n), inP = C.pl <= w;
    body = `<div class="cup-in"><img src="${p.src || ''}" alt=""><div><b>${esc(rcName(p))} is ${ppOrd(C.pl)} of ${C.n}</b><small class="${inP ? 'ok' : ''}">${inP ? '✓ In the prizes' : `${C.pl - w} place${C.pl - w === 1 ? '' : 's'} off the prizes`} · top ${w} win · results in ${cupLeft(C.dl)}</small></div></div>
      <button class="cup-demo" data-cup="demo">Demo: run tonight’s Cup now</button>`; }
  else body = `<p class="cup-s">Enter one photo for <b>${CUP_COST} coins</b>. The crowd ranks it all day. 1st <b>$30</b> · 2nd <b>$20</b> · 3rd <b>$15</b> · top 10 win cash · top 25 win a prize.</p>
      ${!R.length ? '<button class="btn cup-b off" disabled>Qualify a photo to enter</button>' : g < CUP_COST ? `<button class="btn cup-b off" disabled>${CUP_COST - g} more coins to enter</button>` : `<button class="btn cup-b" data-cup="enter">🏆 Enter a photo · ${CUP_COST} coins</button>`}`;
  return `<div class="cup" id="cupC"><div class="cup-h"><span>🏆</span><div><b>Daily Cup</b><small>${st === 'ready' ? 'Tonight’s Cup has finished' : `Tonight ${CUP_HOUR > 12 ? CUP_HOUR - 12 : CUP_HOUR}pm · closes in ${cupLeft(st === 'in' ? C.dl : cupDl())}`}</small></div><em>$100<small>in prizes</small></em></div>${body}<p class="cup-f">Fixed prize pot paid by PhotoPicks · demo: other entrants are simulated</p></div>`; }
function cupEnter() { const R = (S.photos || []).filter(p => isCashOK(p) && !p.starter); if (!R.length || (S.gems || 0) < CUP_COST || cupSt() !== 'open') return;
  if (S.user && S.user.guest) { try { closeFlow(); } catch (e) {} openSignup(() => setTimeout(finalsTab, 250), { locked: false, real: 1 }); return; }
  if (R.length === 1) return cupJoin(R[0]);
  popOpen(`<div class="pp qfx nv"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Daily Cup</span></div><h2 class="nv-h2">Which photo?</h2><div class="qf2-g">${R.slice(0, 6).map(p => `<div class="qf2-t" data-cupp="${p.id}" style="cursor:pointer"><img src="${p.src}" alt=""><span>${esc(rcName(p))}</span></div>`).join('')}</div><div style="text-align:center"><button class="link nv-later" id="cupX">Cancel</button></div></div>`);
  $('#cupX').onclick = () => popClose(); document.querySelectorAll('[data-cupp]').forEach(b => b.onclick = () => { popClose(); cupJoin(S.photos.find(x => x.id === b.dataset.cupp)); }); }
function cupJoin(p) { if (!p || (S.gems || 0) < CUP_COST) return; S.gems -= CUP_COST; const n = 84 + Math.floor(Math.random() * 40); S.cup = { dl: cupDl(), pid: p.id, n, pl: Math.round(n * (.35 + Math.random() * .3)), at: Date.now() }; save(); try { paintGems(); } catch (e) {}
  toast(`🏆 ${rcName(p)} is in tonight’s Daily Cup · −${CUP_COST} coins`); try { if (document.querySelector('#flow .sx')) finalsTab(); } catch (e) {} }
function cupFinish() { const C = S.cup; if (!C || C.done) return; const p = (S.photos || []).find(x => x.id === C.pid); if (!p) { C.done = 1; save(); return; } try { closeFlow(); } catch (e) {} try { popClose(); } catch (e) {}
  for (let i = 0; i < 6; i++) cupMove(); if (C.pl <= 6) return cupRace(p); cupResult(p); }
function cupRace(p) { const C = S.cup, k = photoShow(p) || finCatOf(p) || 'pets', N = ppShuffle(QS_NAMES.slice(), Math.random), pool = ppShuffle(SEED.filter(x => x.src && x.src !== p.src), Math.random).slice(0, 5);
  const fin = Math.max(1, Math.min(6, C.pl + (Math.random() < .5 ? -1 : Math.random() < .5 ? 0 : 1))), L = [{ src: p.src, h: 'You', me: 1 }].concat(pool.map((x, i) => ({ src: x.src, h: '@' + N[i] })));
  const others = ppShuffle([1, 2, 3, 4, 5], Math.random), ord = []; let oi = 0; for (let r = 1; r <= 6; r++) ord.push(r === fin ? 0 : others[oi++]); const rank = i => ord.indexOf(i);
  popOpen(`<div class="pp qfx nv"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Daily Cup · live Final</span></div><h2 class="nv-h2">The top 6 race for $30</h2>
    <div class="qf-trk">${L.map((x, i) => `<div class="qf-ln ${x.me ? 'me' : ''}"><span class="qf-nm">${x.me ? 'You' : esc(x.h)}</span><span class="qf-rail"><img id="cpH${i}" src="${x.src}" alt="" style="left:0%"></span></div>`).join('')}<i class="qf-fin"></i></div><p class="qw-o" id="cpC">🏁 And they’re off!</p><p class="nv-sim">Demo · entrants and votes are simulated</p></div>`);
  const T = 24; let t = 0; const iv = setInterval(() => { if (!document.getElementById('cpC')) { clearInterval(iv); return; } t++; const kk = t / T, pos = L.map((x, i) => Math.min(100, (100 - rank(i) * 7) * (1 - Math.pow(1 - kk, 1.6)) + Math.sin(t * .9 + i * 1.7) * 5 * (1 - kk)));
    L.forEach((x, i) => { const e = document.getElementById('cpH' + i); if (e) e.style.left = `calc(${pos[i] * .86}%)`; }); const my = [...pos].sort((a, b) => b - a).indexOf(pos[0]) + 1; $('#cpC').textContent = t >= T ? '📸 Across the line…' : my === 1 ? '🔥 You’re in front!' : `You’re ${ppOrd(my)}`;
    if (t >= T) { clearInterval(iv); C.pl = fin; photoFinish(() => cupResult(p)); } }, 450); }
function cupResult(p) { const C = S.cup, pz = cupPrize(C.pl, C.n), w = cupWin(C.n), nm = esc(rcName(p)); C.done = 1; C.res = { pl: C.pl, n: C.n };
  if (pz && pz.cash) { S.cash = +((S.cash || 0) + pz.cash).toFixed(2); try { earnAdd({ kind: 'cup', pid: p.id, t: p.title, amt: pz.cash, place: C.pl }); } catch (e) {} if (C.pl <= 3) rzAdd(p, C.pl - 1); }
  else if (pz) S.bonus = +((S.bonus || 0) + pz.bonus).toFixed(2); save(); try { paintWallet(); } catch (e) {}
  const N = ppShuffle(QS_NAMES.slice(), Math.random), top = [1, 2, 3].map(r => `<div class="${r === C.pl ? 'me' : ''}"><em>${['🥇', '🥈', '🥉'][r - 1]}</em><b>${r === C.pl ? nm + ' · You' : '@' + N[r]}</b><i>${money(CUP_CASH[r - 1])}</i></div>`).join('');
  popOpen(`<div class="pp qfx nv qw"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Daily Cup · result</span></div><h2 class="nv-big sm">${nm} finished ${ppOrd(C.pl)}</h2><p class="qw-o">of ${C.n} photos · top ${w} won a prize</p>
    ${pz && pz.cash ? `<div class="h2w-amt">${money(pz.cash)}</div><p class="qw-o">cash · added to your balance</p>` : pz ? `<div class="h2w-amt" style="font-size:2rem">Free $2 Final entry</div><p class="qw-o">added as Bonus Cash · use it in any Final</p>` : `<p class="qw-r" style="font-size:1.3rem">${C.pl - w} place${C.pl - w === 1 ? '' : 's'} off the prizes</p><p class="qw-o">Tomorrow’s Cup is open now.</p>`}
    <div class="qf-res cup-top">${top}${C.pl > 3 ? `<div class="me"><em>${ppOrd(C.pl)}</em><b>${nm} · You</b><i>${pz ? (pz.cash ? money(pz.cash) : 'Free entry') : ''}</i></div>` : ''}</div>
    <button class="btn block nv-go" id="cupOk">${pz && !pz.cash ? '🏁 Use it in a Final' : '🏆 Back to your stable'}</button><p class="nv-sim">Fixed prize pot paid by PhotoPicks · demo: entrants simulated</p></div>`);
  if (pz) setTimeout(() => { try { if (pz.cash) cashExplosion(pz.cash, { label: 'Daily Cup' }); rvConfetti(document.querySelector('.qw'), pz.cash ? 110 : 50); } catch (e) {} }, 300);
  $('#cupOk').onclick = () => { popClose(); if (pz && !pz.cash) qfStart(p); else finalsTab(); }; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-cup]'); if (!b) return; e.preventDefault(); const k = b.dataset.cup; if (k === 'enter') cupEnter(); else if (k === 'demo') { S.cup.dl = Date.now(); save(); cupFinish(); } else if (k === 'res') cupFinish(); else if (k === 'open') { try { popClose(); } catch (x) {} finalsTab(); } });
(() => { const ft = finalsTab; finalsTab = function () { const r = ft.apply(this, arguments); try { const sub = document.querySelector('#flow .sx .sx-sub'); if (sub && !document.getElementById('cupC')) sub.insertAdjacentHTML('afterend', cupCard()); } catch (e) {} return r; }; })();
(() => { const cf = callFx; callFx = function () { const r = cf.apply(this, arguments); try { if (cupSt() === 'in') { cupMove(); save(); } } catch (e) {} return r; }; })();
(() => { const wr = wbRows; wbRows = function () { const R = wr.apply(this, arguments); try { const st = cupSt(), C = S.cup;
    if (st === 'ready') { const p = (S.photos || []).find(x => x.id === C.pid) || {}; R.unshift(`<div class="wbk-r"><span class="wbk-ic">🏆</span><div><b>Daily Cup results are in</b><small>See where ${esc(rcName(p))} finished</small></div><button class="btn wbk-b" data-cup="res">See</button></div>`); }
    else if (st === 'open' && (S.photos || []).some(p => isCashOK(p)) && (S.gems || 0) >= CUP_COST) R.push(`<div class="wbk-r"><span class="wbk-ic">🏆</span><div><b>Tonight’s Daily Cup is open</b><small>$100 in prizes · ${CUP_COST} coins to enter</small></div><button class="btn wbk-b nv2" data-cup="open">Enter</button></div>`); } catch (e) {} return R; }; })();
(() => { const ug = useGems; useGems = function () { const r = ug.apply(this, arguments); try { const per = document.querySelector('.t2 .t2-per'); if (per) per.insertAdjacentHTML('afterend', `<div class="t2-tk"><b>🏆 ${CUP_COST} coins = tonight’s Daily Cup</b><small>$100 in prizes · top 25 win · enter from your Stable</small></div>`); } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace("e.kind === 'du' ? '🥊 Duel win' : '🏆 Prize'", "e.kind === 'du' ? '🥊 Duel win' : e.kind === 'cup' ? `🏆 Daily Cup · ${ppOrd(e.place || 1)}` : '🏆 Prize'")
s = s.replace('</style>', """.cup{margin:0 0 14px;padding:14px;border-radius:18px;background:radial-gradient(120% 80% at 50% 0%,#1F2F58,#14213D 60%,#0E1830);box-shadow:0 0 0 2px #D9AE4F,0 6px 18px rgba(20,33,61,.2);color:#EEF1F8;text-align:left}
.cup-h{display:flex;align-items:center;gap:10px;margin-bottom:8px}.cup-h>span{font-size:2rem}.cup-h div{flex:1}.cup-h b{display:block;font:900 1.4rem Fraunces,Georgia,serif;color:#FBF3DC}.cup-h small{font:700 .78rem Nunito,system-ui;color:#C9D3E6}
.cup-h em{font-style:normal;text-align:right;font:900 1.7rem/1 Fraunces,Georgia,serif;color:#F3D98B}.cup-h em small{display:block;font:800 .62rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#F3D98B}
.cup-s{margin:0 0 10px;font:600 .88rem/1.45 Nunito,system-ui;color:#EEF1F8}.cup-s b{color:#F3D98B}
html body #flow .sx .btn.cup-b{width:100%!important;min-height:48px!important;margin:0!important;border-radius:999px!important;background:linear-gradient(180deg,#F3D98B,#D9AE4F)!important;color:#14213D!important;font:900 1.02rem Nunito,system-ui!important;box-shadow:none!important}
html body #flow .sx .btn.cup-b.off{background:#3A4766!important;color:#B9C3DA!important}
.cup-in{display:flex;align-items:center;gap:10px;padding:10px;border-radius:14px;background:#FBF6EE}.cup-in img{width:52px;height:52px;border-radius:10px;object-fit:cover;box-shadow:0 0 0 2px #D9AE4F}.cup-in b{display:block;font:800 1rem Nunito,system-ui;color:#14213D}.cup-in small{font:700 .78rem Nunito,system-ui;color:#5B4A3F}.cup-in small.ok{color:#1F6A2E}
.cup-demo{display:block;margin:8px auto 0;border:0;background:none;font:700 .8rem Nunito,system-ui;color:#C9D3E6;text-decoration:underline;cursor:pointer}.cup-f{margin:8px 0 0;font:600 .68rem Nunito,system-ui;color:#8C9AB5;text-align:center}
html body .nv .qf-res.cup-top{margin:10px 0}html body .nv .qf-res.cup-top b,html body .nv .qf-res.cup-top em{color:#14213D!important;-webkit-text-fill-color:#14213D!important}html body .nv .qf-res.cup-top div{grid-template-columns:44px 1fr auto}html body .nv .qf-res.cup-top i{color:#1F6A2E}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v206 ok')
