# Real Money build, step 217 (after rmv213.py): clearer journey, buttons that fit, head-to-heads as horse races.
#  - Vote screen photo cards: one route per photo. Start → 3 steps → 🎀 Qualifier race → 3 steps → 🏁 Final.
#    The photo sits at its spot; checkpoints are labelled; the line below names the current goal.
#  - Stable cash card: buttons stacked full width (they overflowed side by side on a phone).
#  - Head-to-heads (cash and training) run live as a two-lane horse race on the qualifier track: "Race to 8",
#    first to 8 of 15 crowd votes wins, 3-2-1 start. The result screen stays. A voter is never the rival themself.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("All ${H3_V} votes counted", "First to ${H3_WIN} votes wins", 2)
RA("function fcNotify() {", r"""function pvStep(p, s, fin) { s = Math.min(QS_STEPS, s || 0); const idx = fin ? QS_STEPS + s : s, N = QS_STEPS * 2, pos = idx / N, k = S.stk || 0, live = !fin && p.ql && p.ql.live;
  const node = i => { const x = i / N * 100, cp = i === QS_STEPS || i === N, done = i <= idx;
    return cp ? `<span class="jc ${done ? 'd' : ''} ${i === N ? 'f' : 'q'}" style="left:${x}%">${i === N ? '🏁' : '🎀'}</span>` : i ? `<i class="jn ${done ? 'd' : ''} ${i > QS_STEPS ? 'g' : ''}" style="left:${x}%"></i>` : ''; };
  const goal = live ? '<b class="jg live">🔴 Qualifier race · live now</b>' : fin ? `<b class="jg">${s >= QS_STEPS ? '🏁 Your Final is ready' : `${s} of ${QS_STEPS} steps to the <u>Final</u>`}</b>` : `<b class="jg">${s} of ${QS_STEPS} steps to the <u>qualifier race</u></b>`;
  return `<div class="pv-tr jr ${fin ? 'fin' : ''}"><div class="pv-rail"><u style="width:${pos * 100}%"></u>${Array.from({ length: N + 1 }, (_, i) => node(i)).join('')}</div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"></div>
    <div class="jl"><span class="a ${fin ? 'ok' : 'on'}">${fin ? '✓ Qualified' : 'Qualifying'}</span><span class="b ${fin ? 'on' : ''}">Qualifier race</span><span class="c">Final</span></div>
    <div class="pv-k"><span class="pv-dots">${Array.from({ length: QS_RUN }, (_, i) => `<i class="${i < k ? 'on' : i === QS_RUN - 1 && k === QS_RUN - 1 ? 'next' : ''}"></i>`).join('')}</span>${k === QS_RUN - 1 ? '<em class="pv-1m">1 more for a step!</em>' : ''}${goal}</div>`; }
function h2hLive(p, R, fee) { const cash = fee > 0, prize = +(fee * H2H_PAY).toFixed(2), o = { src: R.src, t: R.title || R.t || 'A rival' }, oh = R.h || '@rival', T = p.tq || { w: 0, l: 0 }, nm = esc(rcName(p));
  const st = qlStrength(p), rs = cash ? st + (Math.random() - .5) * 14 : st - 4 - Math.random() * 8, pv = Math.max(.3, Math.min(.72, .5 + (st - rs) / 60)), won = Math.random() < (cash ? Math.max(.35, Math.min(.62, pv)) : pv);
  const wv = H3_WIN + Math.floor(Math.random() * 4), seq = [...Array(wv).fill(won ? 1 : 0), ...Array(H3_V - wv).fill(won ? 0 : 1)];
  for (let i = seq.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; }
  popOpen(`<div class="pp qfx qrx nv qr2 h2r"><div class="nv-bg" style="background-image:url('${p.src}')"></div><button class="h3-x h2r-x" data-h3x aria-label="Close">✕</button><p class="nv-brand">PhotoPicks</p>
    <div class="nv-pillrow"><span class="nv-pill">${cash ? `Live · $${fee} head-to-head` : 'Live · training match'}</span></div><h2 class="nv-h">Race to ${H3_WIN}</h2><p class="nv-s">${cash ? `Winner takes <b class="gold">${money(prize)}</b>` : `Win = training win ${Math.min(TQ_WIN, T.w + 1)} of ${TQ_WIN}`}</p>
    <div class="hr-trk"><div class="hr-fin"><span>🏁</span></div>
      <div class="hr-ln me" id="qrCA"><span class="hr-nm">${nm} · <b>You</b></span><div class="hr-rail"><i class="hr-dust"></i><img id="qrHA" src="${p.src}" alt=""></div><b class="hr-v" id="qrAv">0</b></div>
      <div class="hr-ln" id="qrCB"><span class="hr-nm">${esc(oh)}</span><div class="hr-rail"><i class="hr-dust"></i><img id="qrHB" src="${o.src}" alt=""></div><b class="hr-v" id="qrBv">0</b></div>
      <div class="hr-ticks">${Array.from({ length: H3_WIN - 1 }, (_, k) => `<i style="left:calc(${(k + 1) / H3_WIN} * (100% - 120px) + 40px)"></i>`).join('')}</div></div>
    <p class="qr2-v" id="qrV">🗳️ The crowd is voting…</p><div class="nv-goal" id="h3N">First to <b>${H3_WIN}</b> crowd votes wins</div><p class="nv-sim">Demo · simulated votes</p></div>`);
  document.querySelectorAll('[data-h3x]').forEach(b => b.onclick = () => { popClose(); finalsTab(); });
  const run = () => { let i = 0, A = 0, B = 0; const step = () => { if (!document.getElementById('h3N')) return;
      const me = seq[i++]; if (me) A++; else B++; let vh; do { vh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)]; } while (vh === oh);
      $('#qrAv').textContent = A; $('#qrBv').textContent = B;
      const mv = (id, v) => { const h = document.getElementById(id); if (h) h.style.left = `calc(${Math.min(1, v / H3_WIN)} * (100% - 52px))`; }; mv('qrHA', A); mv('qrHB', B);
      $('#qrCA').classList.toggle('lead', A > B); $('#qrCB').classList.toggle('lead', B > A);
      const c = document.getElementById(me ? 'qrCA' : 'qrCB'); c.classList.remove('hit'); void c.offsetWidth; c.classList.add('hit');
      $('#qrV').innerHTML = `🗳️ <b>${vh}</b> voted for <b class="${me ? 'me' : ''}">${me ? nm : esc(oh)}</b>`;
      const g = $('#h3N'); g.innerHTML = A >= H3_WIN ? '<b>🏁</b> You win!' : B >= H3_WIN ? `<b>🏁</b> ${esc(oh)} wins` : A === H3_WIN - 1 && B === H3_WIN - 1 ? '<b>Next vote wins it!</b>' : A === H3_WIN - 1 ? '<b>One vote</b> from victory' : B === H3_WIN - 1 ? 'They need <b>one more</b>…' : A === B ? 'Neck and neck' : A > B ? `You lead by <b>${A - B}</b>` : `Behind by <b>${B - A}</b> · come on!`;
      g.classList.toggle('hot', A === H3_WIN - 1 || B === H3_WIN - 1);
      if (A < H3_WIN && B < H3_WIN && i < seq.length) { setTimeout(step, 1000); return; } setTimeout(() => photoFinish(() => h3Done(p, o, oh, fee, A > B, A, B)), 600); };
    step(); };
  qrCount(p, o, oh, run, cash ? `💵 $${fee} head-to-head` : '🏋️ Training match', cash ? `First to ${H3_WIN} votes wins ${money(prize)}` : `First to ${H3_WIN} votes wins`); }
function fcNotify() {""")
s = s.replace('</style>', """.pv-tr.jr{height:50px;margin:8px 0 0}.jr .pv-rail{left:20px;right:20px;height:8px;margin-top:-4px;background:#E6EFE2;border-radius:4px}
.jr .pv-rail u{background:linear-gradient(90deg,#8CC79A,#2F7A3F);border-radius:4px;transition:width .6s}.jr.fin .pv-rail u{background:linear-gradient(90deg,#2F7A3F 0,#2F7A3F 48%,#E8C766 52%,#C9952D 100%)}
.jr .jn{position:absolute;top:50%;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;background:#fff;box-shadow:inset 0 0 0 2px #B9CDB2;z-index:1}.jr .jn.d{background:#2F7A3F;box-shadow:0 0 0 2px #fff}.jr .jn.g.d{background:#C9952D}
.jr .jc{position:absolute;top:50%;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;display:grid;place-items:center;font-size:15px;background:#fff;box-shadow:inset 0 0 0 2px #D9AE4F,0 2px 6px rgba(20,33,61,.15);z-index:1}
.jr .jc.d{background:#FBF3DC;box-shadow:inset 0 0 0 2px #C9952D,0 0 0 3px rgba(217,174,79,.3)}.jr .pv-hz{z-index:2;transition:left .6s}.jr .pv-fl{display:none}
.jl{position:relative;height:16px;margin:2px 0 6px;font:800 .64rem Nunito,system-ui;letter-spacing:.05em;text-transform:uppercase;color:#8A7A6A}.jl span{position:absolute;top:0;white-space:nowrap}
.jl .a{left:0}.jl .b{left:50%;transform:translateX(-50%)}.jl .c{right:0}.jl .on{color:#14213D}.jl .ok{color:#2F7A3F}.pv-c.fin .jl .c{color:#9A6B12}
html body #qlS .pv-k{flex-wrap:wrap;row-gap:4px}.pv-k .jg{order:-1;flex-basis:100%;margin:0;font:800 .9rem Nunito,system-ui;color:#14213D;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pv-k .jg u{text-decoration:none;color:#9A6B12}.pv-c:not(.fin) .pv-k .jg u{color:#2F7A3F}.pv-k .jg.live{color:#B3261E}
html body #flow .sx .sx-btns:not(.one):not(.two){grid-template-columns:1fr!important;gap:8px!important}html body #flow .sx .sx-h2{width:100%;align-items:stretch}html body #flow .sx .sx-h2 .btn{width:100%!important;margin:0!important}html body #flow .sx .sx-h2 small{text-align:center}
.h2r{position:relative}.h2r .h2r-x{position:absolute;top:12px;right:14px;z-index:3;border:0;background:none;color:#C9D3E6;font-size:1.2rem;cursor:pointer}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v214 ok')
