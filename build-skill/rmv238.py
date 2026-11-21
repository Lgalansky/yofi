# Real Money build, step 241 (after rmv237.py): Stable card = progression track + "Real games" / "Coin games" (user spec).
#  - Track with 5 stops: 🖼️ Framed → 🎀 Qualifier → 🏋️ Training → 💵 Cash games → 🏁 Final. Done stops are green ticks,
#    a lost qualifier is a red cross, a skipped training stop is dimmed, the current stop glows gold, future stops are grey.
#  - "Now" card under the track says the next step; tapping it goes to voting when the next step is voting (free).
#  - Two buttons: "💵 Real games" (green; cash-ready photos) opens a sheet of the cash games this photo can play now
#    (its Final, waiting challenges, head-to-head); "🪙 Coin games" (gold) opens the Coin games tab.
#    Photos not yet cash-ready keep their own main step (vote / train) instead of Real games.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""stLadder = function (p) { const q = p.ql || {}, inQ = !!(p.ql && !q.done), ok = isCashOK(p), lost = q.done === 'x', T = p.tq || { w: 0, l: 0 }, trained = lost && (ok || T.w || T.l), R = p.raced;
  const fs = Math.min(QS_STEPS, (p.fr && p.fr.s) || 0), qs = Math.min(QS_STEPS, q.got || 0);
  const st = { f: 'd', q: inQ ? 'n' : lost ? 'x' : (q.done === 'q' || ok) ? 'd' : 'n', t: !lost ? (ok ? 's' : '') : ok ? 'd' : 'n', c: ok ? 'd' : '', fi: R && !p.fin ? 'd' : ok ? 'n' : '' };
  const sub = { f: 'Done', q: inQ ? `${qs}/${QS_STEPS} steps` : lost ? `Lost ${q.w || 0}–${q.l || 0}` : st.q === 'd' ? 'Won' : 'Next', t: !lost ? (ok ? 'Not needed' : '') : ok ? `${TQ_WIN} wins` : `${T.w}/${TQ_WIN} wins`, c: ok ? 'Unlocked' : 'Locked', fi: R && !p.fin ? ppOrd(R.rank) : ok ? (p.fr && p.fr.go ? 'Ready!' : `${fs}/${QS_STEPS} steps`) : 'Locked' };
  const stops = [['f', '🖼️', 'Framed'], ['q', '🎀', 'Qualifier'], ['t', '🏋️', 'Training'], ['c', '💵', 'Cash games'], ['fi', '🏁', 'Final']];
  const idx = stops.reduce((m, x, i) => (st[x[0]] === 'd' || st[x[0]] === 'x' || st[x[0]] === 's') ? i : m, 0), pct = Math.round(idx / (stops.length - 1) * 100);
  let now;
  if (inQ) now = { t: q.live ? 'Qualifier race · live now' : `Qualifier · ${qs} of ${QS_STEPS} steps`, s: 'Vote 2 in a row with the crowd = 1 step', v: 1, p: qs / QS_STEPS };
  else if (lost && !ok) now = { t: `Training · ${T.w} of ${TQ_WIN} wins`, s: `${TQ_COST} coins a match · win ${TQ_WIN} to unlock cash games`, p: T.w / TQ_WIN };
  else if (p.fin && p.fr && p.fr.go) now = { t: 'Your Final is ready', s: 'Enter it from Real games', p: 1 };
  else if (p.fin) now = { t: `Final · ${fs} of ${QS_STEPS} steps`, s: 'Vote 2 in a row with the crowd = 1 step', v: 1, p: fs / QS_STEPS };
  else if (p.runEnd) now = { t: 'Run complete', s: 'Race it again from Real games', p: 1 };
  else now = { t: 'Cash games unlocked', s: 'Play real games below', p: 1 };
  return `<div class="pg2"><div class="tk"><i class="tk-l"><u style="width:${pct}%"></u></i>${stops.map(([k, ic, lab]) => `<div class="tk-s ${st[k] || 'f'}"><span>${st[k] === 'd' ? '✓' : st[k] === 'x' ? '✕' : ic}</span><b>${lab}</b><small>${sub[k] || ''}</small></div>`).join('')}</div>
    <div class="pg2-now ${now.v ? 'tap' : ''}" ${now.v ? 'data-stv' : ''}><div><p>▶ Now</p><b>${now.t}</b><small>${now.s}</small><span class="pg-bar"><u style="width:${Math.round(now.p * 100)}%"></u></span></div>${now.v ? '<em>Vote ›</em>' : ''}</div></div>`; };
(() => { const pt = pkTag; pkTag = function (b) { pt.apply(this, arguments); try { if (b && b.matches && b.matches('[data-rg], [data-rgf], [data-rga], [data-rgh]')) { b.classList.remove('pk-free', 'pk-coin', 'pk-dark'); b.classList.add('pk-cash'); } } catch (e) {} }; })();
(() => { const sh = stHero; stHero = function (p) { let h = sh.apply(this, arguments); try { const t = document.createElement('div'); t.innerHTML = h; const b = t.querySelector('.sx-btns'); if (b) { b.className = 'sx-btns sx-btns-now sx-two';
      b.innerHTML = `<button class="btn rg-b" data-rg="${p.id}">💵 Real games</button><button class="btn cg-b2" data-pt="coins">${gemIcon('cn-ic')} Coin games</button>`; const pg = t.querySelector('.pg2'); if (pg) pg.insertAdjacentElement('afterend', b); }
    h = t.innerHTML; } catch (e) {} return h; }; })();
function realGames(p) { if (!p) return; const C = (() => { try { return chList().filter(c => c.pid === p.id); } catch (e) { return []; } })(), nm = esc(rcName(p)), fs = Math.min(QS_STEPS, (p.fr && p.fr.s) || 0);
  const row = (ic, t, s, btn) => `<div class="rg-r"><span>${ic}</span><div><b>${t}</b><small>${s}</small></div>${btn}</div>`;
  const rows = [];
  if (p.fin && p.fr && p.fr.go) rows.push(row('🏁', 'Your Final', `6 photos · $2–$20 entry · 1st wins up to ${money(20 * QF_PAY[0]).replace('.00', '')}`, `<button class="btn rg-go" data-rgf="${p.id}">Enter</button>`));
  else if (p.runEnd) rows.push(row('🏁', 'Race it again', 'Back to the qualifier, then a new Final', `<button class="btn rg-go" data-rga="${p.id}">Start</button>`));
  else if (p.fin) rows.push(row('🏁', 'Final', `${QS_STEPS - fs} voting step${QS_STEPS - fs === 1 ? '' : 's'} to go · vote to unlock`, `<button class="btn rg-v" data-stv>Vote</button>`));
  C.forEach(c => rows.push(row('⚔️', `${esc(c.h)} challenged ${nm}`, `$${c.fee} entry · winner takes ${money(c.fee * H2H_PAY)}`, `<button class="btn rg-go" data-chy="${c.id}">Accept</button>`)));
  rows.push(row('⚔️', 'Head-to-head', `1 on 1 · $2–$20 · winner takes up to ${money(20 * H2H_PAY)}`, `<button class="btn rg-go" data-rgh="${p.id}">Play</button>`));
  popOpen(`<div class="pp qfx nv rgp"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Real games · ${nm}</span></div><h2 class="nv-h2">Play for real cash</h2>
    <div class="rg-l">${rows.join('')}</div><div style="text-align:center"><button class="link nv-later" id="rgX">Back to your stable</button></div><p class="nv-sim">Entry fees are real cash · demo: rivals simulated</p></div>`);
  $('#rgX').onclick = () => popClose(); }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-rg], [data-rgf], [data-rga], [data-rgh]'); if (!b) return; e.preventDefault(); const P = id => (S.photos || []).find(x => x.id === id);
  if (b.dataset.rg) { try { closeFlow(); } catch (x) {} realGames(P(b.dataset.rg)); } else if (b.dataset.rgf) { popClose(); qfStart(P(b.dataset.rgf)); } else if (b.dataset.rga) { popClose(); runAgain(P(b.dataset.rga)); } else if (b.dataset.rgh) { popClose(); h2hOpen(P(b.dataset.rgh), H2H_FEES[0]); } });
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('#coach [data-stv]'); if (!b) return; e.preventDefault(); try { popClose(); } catch (x) {} try { closeFlow(); } catch (x) {} go('judge'); renderJudge(); }, true);
function fcNotify() {""")
s = s.replace('</style>', """.pg2{margin:10px 14px 4px}.tk{position:relative;display:grid;grid-template-columns:repeat(5,1fr);margin:4px 0 12px}.tk-l{position:absolute;left:10%;right:10%;top:17px;height:4px;border-radius:2px;background:#E2D9C6}.tk-l u{display:block;height:100%;border-radius:2px;background:#2F7A3F}
.tk-s{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;text-align:center}.tk-s span{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font:900 1rem Nunito,system-ui;background:#fff;box-shadow:inset 0 0 0 2px #E2D9C6;color:#8A7A6A}
.tk-s b{margin-top:5px;font:900 .7rem Nunito,system-ui;color:#14213D;line-height:1.1}.tk-s small{font:700 .64rem Nunito,system-ui;color:#8A7A6A}
.tk-s.d span{background:#2F7A3F;color:#fff;box-shadow:none}.tk-s.x span{background:#F4E4DF;color:#B3261E;box-shadow:inset 0 0 0 2px #D9A497}.tk-s.n span{background:#FBF3DC;box-shadow:0 0 0 4px rgba(217,174,79,.35),inset 0 0 0 2px #D9AE4F}.tk-s.n b,.tk-s.n small{color:#9A6B12}.tk-s.s{opacity:.45}.tk-s.f{opacity:.6}
.pg2-now{display:flex;align-items:center;gap:10px;padding:12px;border-radius:16px;background:#FFF6DA;box-shadow:inset 0 0 0 2px #D9AE4F}.pg2-now>div{flex:1}.pg2-now p{margin:0;font:900 .66rem Nunito,system-ui;letter-spacing:.12em;text-transform:uppercase;color:#9A6B12}.pg2-now b{display:block;font:900 1.02rem Nunito,system-ui;color:#14213D}.pg2-now small{display:block;font:600 .78rem Nunito,system-ui;color:#6B5B4B}
.pg2-now.tap{cursor:pointer}.pg2-now em{flex:none;padding:7px 12px;border-radius:999px;background:#14213D;color:#fff;font:900 .82rem Nunito,system-ui;font-style:normal}
html body #flow .sx .sx-btns.sx-two{display:grid!important;grid-template-columns:1fr 1fr!important;gap:10px!important;margin:12px 14px 14px!important;padding:0!important}html body #flow .sx .sx-two .btn{width:100%!important;min-width:0!important;margin:0!important;min-height:52px!important;border-radius:16px!important;font:900 1rem Nunito,system-ui!important;white-space:nowrap}
.sx-hero .pg,.sx-card .pg{display:none}
.rg-l{display:grid;gap:8px;margin:12px 0 14px}.rg-r{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 1.5px rgba(217,174,79,.5);text-align:left}.rg-r>span{font-size:1.4rem}.rg-r>div{flex:1;min-width:0}.rg-r b{display:block;font:900 .98rem Nunito,system-ui;color:#FBF3DC}.rg-r small{font:600 .78rem Nunito,system-ui;color:#C9D3E6}
html body .rgp .rg-r .btn{flex:none;min-width:76px;min-height:40px!important;margin:0!important;padding:0 14px!important;border-radius:999px!important;font:900 .9rem Nunito,system-ui!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v238 ok')
