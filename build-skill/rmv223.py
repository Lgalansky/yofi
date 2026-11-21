# Real Money build, step 226 (after rmv222.py): ideas A + B + C (user approved).
#  B. Missed qualifier: no free rematch, no timer. The only way back is training: 3 wins at 50 coins a match.
#     "So close" screen, Vote card and Stable all show "Training · N of 3 wins" with one button. Old rematch timers removed.
#  C. Save judge votes: training is a replay drawn from the photo's real share of crowd votes ("Replay of N crowd votes"),
#     fast and labelled, using no new votes. Live votes go to qualifiers and cash races.
#     Shorter races: qualifier first to 7 (was 11); head-to-heads first to 5 of 9 (was 8 of 15).
#  A. Play tab: each photo shows its road: Entered -> Qualifier -> (Training) -> Cash-ready -> ⚔️ Cash challenges (the goal).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("const QV_NEED = 10, QR_WIN = 11;", "const QV_NEED = 10, QR_WIN = 7;")
RA("const loseV = 6 + Math.floor(Math.random() * 5)", "const loseV = 2 + Math.floor(Math.random() * 5)", 2)
RA("const loseV = 3 + Math.floor(Math.random() * 5)", "const loseV = 2 + Math.floor(Math.random() * 5)")
RA("const H3_V = 15, H3_WIN = 8;", "const H3_V = 9, H3_WIN = 5;")
RA("const H2H_V = 15,", "const H2H_V = 9,")
RA("function fcNotify() {", r"""const missed = p => !!(p && p.ql && p.ql.done === 'x' && !isCashOK(p));
function rmqWait(p) { return missed(p) && !p.runEnd; }
try { (S.photos || []).forEach(p => { if (missed(p)) { delete p.rmAt; p.rmTold = 1; } }); save(); } catch (e) {}
function trBtn(p, cls) { const g = Math.floor(S.gems || 0); return g >= TQ_COST ? `<button class="btn ${cls}" data-trn="${p.id}">🏋️ Train · ${TQ_COST} 🪙</button>` : `<button class="btn ${cls}" data-stv>⚖️ Vote to earn · ${TQ_COST - g} more 🪙</button>`; }
const trBars = p => { const T = p.tq || { w: 0, l: 0 }; return `<span class="trb">${[0, 1, 2].map(i => `<i class="${i < T.w ? 'on' : ''}"></i>`).join('')}</span>`; };
(() => { const pc = pvCard; pvCard = function (p) { if (!missed(p) || (p.tr && !p.tr.done)) return pc.apply(this, arguments); const T = p.tq || { w: 0, l: 0 }, g = Math.floor(S.gems || 0);
  return `<div class="pv-c trn2" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="jr-nx">🏋️ Training</span></div>
    <div class="pv-fn"><img src="${p.src}" alt=""><div><b>${T.w} of ${TQ_WIN} wins to cash races</b>${trBars(p)}</div></div>
    ${g >= TQ_COST ? `<button class="btn block pv-go" data-trn="${p.id}">🏋️ Train · ${TQ_COST} 🪙</button>` : `<p class="pv-l">⚖️ Vote to earn ${TQ_COST - g} more coins to train</p>`}</div>`; }; })();
(() => { const ql = qlLost; qlLost = function (p) { const r = ql.apply(this, arguments); try { if (isCashOK(p)) return r; delete p.rmAt; p.rmTold = 1; save(); const box = document.querySelector('#coach.on .qw'); if (!box) return r;
    const gone = x => x && x.parentNode && x.parentNode.removeChild(x); ['.rm-box', '.mq-or', '.mq-n', '#qlvE', '[data-trn]', '#qlvV', '.nv-sim'].forEach(q => box.querySelectorAll(q).forEach(gone));
    const T = p.tq || { w: 0, l: 0 }, g = Math.floor(S.gems || 0), n = Math.floor(g / TQ_COST), L = box.querySelector('#qlvL'), anchor = L ? L.parentNode : null; const qr = box.querySelector('.qw-r'); if (qr) qr.innerHTML = qr.innerHTML.replace(/(\d+–\d+)/, '<span style="white-space:nowrap">$1</span>');
    const html = `<div class="trk-box"><p class="k">🏋️ Train it back</p><h4>${TQ_WIN} training wins = Cash-ready</h4>${trBars(p)}<p>${TQ_COST} 🪙 a match · lose ${TQ_WIN} and the run resets<br>You have <b>${g} 🪙</b>${n ? `: enough for <b>${n} match${n === 1 ? '' : 'es'}</b>` : ''}</p></div>
      ${g >= TQ_COST ? `<button class="btn block nv-go" data-trn="${p.id}">🏋️ Start training · ${TQ_COST} 🪙</button>` : `<button class="btn block nv-go" id="qlvV">⚖️ Vote to earn · ${TQ_COST - g} more 🪙</button>`}`;
    if (anchor) anchor.insertAdjacentHTML('beforebegin', html); else box.insertAdjacentHTML('beforeend', html); } catch (e) {} return r; }; })();
(() => { const wr = wbRows; wbRows = function () { return wr.apply(this, arguments).filter(x => !/rematch/i.test(x)); }; })();
function stLadder(p) { const q = p.ql || {}, inQ = q && !q.done && p.ql, won = isCashOK(p) && !missed(p) && (q.done === 'q' || p.fin || p.raced || p.qok), lost = q.done === 'x', T = p.tq || { w: 0, l: 0 }, ok = isCashOK(p);
  const C = (() => { try { return chList().filter(c => c.pid === p.id); } catch (e) { return []; } })();
  const st = (cls, ic, t, sub) => `<div class="ld ${cls}"><i>${ic}</i><div><b>${t}</b>${sub ? `<small>${sub}</small>` : ''}</div></div>`;
  const rows = [st('d', '📷', 'Entered', esc(showName(photoShow(p) || finCatOf(p) || 'pets')))];
  rows.push(inQ ? st('n', '🎀', 'Qualifier', `${Math.min(QS_STEPS, q.got || 0)} of ${QS_STEPS} steps to its race`) : lost ? st('x', '🎀', 'Qualifier', `Lost ${q.w || 0}–${q.l || 0}`) : st('d', '🎀', 'Qualifier', won ? 'Won' : ''));
  if (lost || T.w || T.l) rows.push(ok ? st('d', '🏋️', 'Training', `${T.w} of ${TQ_WIN} wins`) : st('n', '🏋️', `Training · ${T.w} of ${TQ_WIN} wins`, `${TQ_COST} 🪙 a match`));
  rows.push(st(ok ? 'd' : 'l', '💵', 'Cash-ready', ok ? 'Finals and head-to-heads open' : 'Unlocks Finals and challenges'));
  rows.push(`<div class="ld goal ${ok ? '' : 'l'}"><i>⚔️</i><div><b>Cash challenges</b><small>${!ok ? 'Other players challenge cash-ready photos' : C.length ? `${C.length} player${C.length === 1 ? '' : 's'} want${C.length === 1 ? 's' : ''} to race ${esc(rcName(p))}` : 'Challengers arrive while you’re away'}</small></div>${ok && C.length ? '<button class="ld-b" data-ldc>See</button>' : ''}</div>`);
  return `<div class="ldr">${rows.join('')}</div>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-ldc]'); if (!b) return; e.preventDefault(); const c = document.querySelector('#flow .cg, #flow [class*="cg-"]'); if (c) c.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
function stTrain(p) { const q = p.ql || {}, inQ = p.ql && !q.done, T = p.tq || { w: 0, l: 0 };
  const stt = inQ ? `🎀 Qualifying · ${Math.min(QS_STEPS, q.got || 0)} of ${QS_STEPS} steps` : missed(p) ? `🏋️ Training · ${T.w} of ${TQ_WIN} wins` : '📷 Ready to start';
  return `<div class="sx-card"><div class="sx-row"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><span class="sx-st">${stt}</span></div></div>${stLadder(p)}
    <div class="sx-btns one">${inQ ? '<button class="btn sx-nv" data-stv>⚖️ Vote to move it</button>' : missed(p) ? trBtn(p, 'sx-nv') : '<button class="btn sx-nv" data-stv>⚖️ Vote to move it</button>'}</div></div>`; }
(() => { const sh = stHero; stHero = function (p) { const h = sh.apply(this, arguments); try { const i = h.indexOf('<div class="sx-btns'); if (i > 0) return h.slice(0, i) + stLadder(p) + h.slice(i); return h.replace(/<\/div>\s*$/, `${stLadder(p)}</div>`); } catch (e) { return h; } }; })();
function h2hLive(p, R, fee) { const cash = fee > 0, prize = +(fee * H2H_PAY).toFixed(2), o = { src: R.src, t: R.title || R.t || 'A rival' }, oh = R.h || '@rival', T = p.tq || { w: 0, l: 0 }, nm = esc(rcName(p));
  const pct = Math.max(30, Math.min(80, (p.vd && p.vd.pct) || 55)), nv = Math.max(20, Math.min(60, (p.s && p.s.total) || 40));
  let won; if (cash) { const st = qlStrength(p), rs = st + (Math.random() - .5) * 14, pv = Math.max(.3, Math.min(.72, .5 + (st - rs) / 60)); won = Math.random() < Math.max(.35, Math.min(.62, pv)); } else won = Math.random() < pct / 100;
  const wv = H3_WIN + Math.floor(Math.random() * 4), seq = [...Array(wv).fill(won ? 1 : 0), ...Array(H3_V - wv).fill(won ? 0 : 1)];
  for (let i = seq.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; }
  popOpen(`<div class="pp qfx qrx nv qr2 h2r"><div class="nv-bg" style="background-image:url('${p.src}')"></div><button class="h3-x h2r-x" data-h3x aria-label="Close">✕</button><p class="nv-brand">PhotoPicks</p>
    <div class="nv-pillrow"><span class="nv-pill">${cash ? `Live · $${fee} head-to-head` : 'Training replay'}</span></div><h2 class="nv-h">Race to ${H3_WIN}</h2><p class="nv-s">${cash ? `Winner takes <b class="gold">${money(prize)}</b>` : `Training win ${Math.min(TQ_WIN, T.w + 1)} of ${TQ_WIN} · replay of ${nm}’s last ${nv} crowd votes`}</p>
    <div class="hr-trk"><div class="hr-fin"><span>🏁</span></div>
      <div class="hr-ln me" id="qrCA"><span class="hr-nm">${nm} · <b>You</b></span><div class="hr-rail"><i class="hr-dust"></i><img id="qrHA" src="${p.src}" alt=""></div><b class="hr-v" id="qrAv">0</b></div>
      <div class="hr-ln" id="qrCB"><span class="hr-nm">${esc(oh)}</span><div class="hr-rail"><i class="hr-dust"></i><img id="qrHB" src="${o.src}" alt=""></div><b class="hr-v" id="qrBv">0</b></div>
      <div class="hr-ticks">${Array.from({ length: H3_WIN - 1 }, (_, k) => `<i style="left:calc(${(k + 1) / H3_WIN} * (100% - 120px) + 40px)"></i>`).join('')}</div></div>
    <p class="qr2-v" id="qrV">${cash ? '🗳️ The crowd is voting…' : `🔁 Replaying ${nm}’s crowd record (wins ${pct}% of votes)`}</p><div class="nv-goal" id="h3N">First to <b>${H3_WIN}</b> votes wins</div><p class="nv-sim">${cash ? 'Demo · simulated votes' : 'Training uses votes your photo already earned · no new votes needed'}</p></div>`);
  document.querySelectorAll('[data-h3x]').forEach(b => b.onclick = () => { popClose(); finalsTab(); });
  const run = () => { let i = 0, A = 0, B = 0; const step = () => { if (!document.getElementById('h3N')) return;
      const me = seq[i++]; if (me) A++; else B++; let vh; do { vh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)]; } while (vh === oh);
      $('#qrAv').textContent = A; $('#qrBv').textContent = B;
      const mv = (id, v) => { const h = document.getElementById(id); if (h) h.style.left = `calc(${Math.min(1, v / H3_WIN)} * (100% - 52px))`; }; mv('qrHA', A); mv('qrHB', B);
      $('#qrCA').classList.toggle('lead', A > B); $('#qrCB').classList.toggle('lead', B > A);
      const c = document.getElementById(me ? 'qrCA' : 'qrCB'); c.classList.remove('hit'); void c.offsetWidth; c.classList.add('hit');
      if (cash) $('#qrV').innerHTML = `🗳️ <b>${vh}</b> voted for <b class="${me ? 'me' : ''}">${me ? nm : esc(oh)}</b>`;
      const g = $('#h3N'); g.innerHTML = A >= H3_WIN ? '<b>🏁</b> You win!' : B >= H3_WIN ? `<b>🏁</b> ${esc(oh)} wins` : A === H3_WIN - 1 && B === H3_WIN - 1 ? '<b>Next vote wins it!</b>' : A === H3_WIN - 1 ? '<b>One vote</b> from victory' : B === H3_WIN - 1 ? 'They need <b>one more</b>…' : A === B ? 'Neck and neck' : A > B ? `You lead by <b>${A - B}</b>` : `Behind by <b>${B - A}</b>`;
      if (A < H3_WIN && B < H3_WIN && i < seq.length) { setTimeout(step, cash ? 1000 : 420); return; } setTimeout(() => photoFinish(() => h3Done(p, o, oh, fee, A > B, A, B)), cash ? 600 : 300); };
    step(); };
  if (cash) qrCount(p, o, oh, run, `💵 $${fee} head-to-head`, `First to ${H3_WIN} votes wins ${money(prize)}`); else setTimeout(run, 500); }
function fcNotify() {""")
s = s.replace('</style>', """.trb{display:flex;gap:5px;margin-top:5px}.trb i{width:26px;height:9px;border-radius:3px;background:#E2D9C6}.trb i.on{background:#C9952D}
.nv .trb i{background:rgba(255,255,255,.18)}.nv .trb i.on{background:#F3D98B}
.trk-box{margin:12px 0 14px;padding:12px 14px;border-radius:16px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(10,16,32,.35);text-align:left}.trk-box .k{margin:0;font:900 .74rem Nunito,system-ui;letter-spacing:.1em;text-transform:uppercase;color:#F3D98B}
.trk-box h4{margin:3px 0 4px;font:900 1.1rem Fraunces,Georgia,serif;color:#fff}.trk-box p{margin:8px 0 0;font:600 .84rem/1.4 Nunito,system-ui;color:#C9D3E6}.trk-box p b{color:#F3D98B}.trk-box .trb i{flex:1;height:11px}
.ldr{margin:8px 14px 10px;position:relative}.ldr:before{content:"";position:absolute;left:15px;top:14px;bottom:20px;width:3px;background:#E2D9C6}
.ld{position:relative;display:flex;align-items:center;gap:10px;padding:4px 0}.ld>i{flex:none;width:33px;height:33px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:.95rem;background:#fff;box-shadow:inset 0 0 0 2px #E2D9C6;z-index:1}
.ld.d>i{background:#2F7A3F;box-shadow:none}.ld.x>i{background:#F4E4DF;box-shadow:inset 0 0 0 2px #D9A497}.ld.n>i{background:#FBF3DC;box-shadow:0 0 0 4px rgba(217,174,79,.3),inset 0 0 0 2px #D9AE4F}
.ld b{display:block;font:800 .9rem Nunito,system-ui;color:#14213D}.ld small{display:block;font:600 .76rem Nunito,system-ui;color:#6B5B4B}.ld.n b{color:#9A6B12}.ld.l{opacity:.5}.ld>div{flex:1}
.ld.goal{margin-top:4px;padding:8px 10px 8px 0;border-radius:14px}.ld.goal:not(.l){background:linear-gradient(90deg,rgba(217,174,79,.0),rgba(217,174,79,.18))}.ld.goal>i{background:#14213D;box-shadow:0 0 0 2px #D9AE4F}
html body #flow .sx .ld-b,.ld-b{flex:none;margin:0!important;min-height:0!important;padding:6px 14px;border:0;border-radius:999px;background:linear-gradient(#F3D98B,#D9AE4F)!important;color:#14213D!important;font:900 .82rem Nunito,system-ui!important;cursor:pointer}
html body #qlS .pv-c.trn2 .pv-fn b{font-size:.95rem!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v223 ok')
