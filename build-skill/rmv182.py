# Real Money build, step 185 (after rmv181.py): every race has a goal, a 3-2-1, suspense and a celebration.
#  - Stable head-to-heads (cash and training) rebuilt in the navy race style: "Race to 8" (15 votes, first to 8),
#    a clear goal ("Win $8.50" / "1 training win · 2 of 3"), 3-2-1 · GO!, one crowd vote a second with the voter shown,
#    gold goal pill "3 more votes to win $8.50", photo finish, then a big result:
#      cash win → "You won $8.50!" (cash burst + confetti); training win → "Training win! 2 of 3" (or
#      "Ready for Cash Races!" at 3); loss → "So close · 6–8" with what's next.
#  - The 6-photo Final now starts with a 3-2-1 too, showing all six finalists.
#  Simulated: rivals and crowd votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const H2_WIN = 8, pipsN = (n, t) => Array.from({ length: t }, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('');
function qrCount(p, o, oh, run, kick, sub) { const box = document.querySelector('.qrx'); if (!box) { run(); return; }
  box.insertAdjacentHTML('beforeend', `<div class="qr-cd" id="qrCd"><p class="pp-k">${kick || '🎀 Qualifier race'}</p><div class="qr-vs"><div><img src="${p.src}" alt=""><b>${esc(rcName(p))}</b><small>You</small></div><span>VS</span><div><img src="${o.src}" alt=""><b>${esc(o.t)}</b><small>${esc(oh)}</small></div></div><b class="qr-num" id="qrNum">3</b><p class="qr-sub">${sub || `First to ${QR_WIN} votes goes to the Final`}</p></div>`);
  let n = 3; const t = setInterval(() => { const e = document.getElementById('qrNum'); if (!e) { clearInterval(t); return; } n--; e.textContent = n > 0 ? n : 'GO!'; e.classList.remove('go'); void e.offsetWidth; e.classList.add('go');
    if (n <= 0) { clearInterval(t); setTimeout(() => { const c = document.getElementById('qrCd'); if (c) { c.classList.add('bye'); setTimeout(() => c.remove(), 350); } run(); }, 650); } }, 900); }
function h2hLive(p, R, fee) { const cash = fee > 0, nm = esc(rcName(p)), prize = +(fee * H2H_PAY).toFixed(2), T = p.tq || { w: 0, l: 0 }, o = { src: R.src, t: R.title || R.t || 'A rival' }, oh = R.h || '@rival';
  const st = qlStrength(p), rs = cash ? st + (Math.random() - .5) * 14 : st - 4 - Math.random() * 8, pv = Math.max(.3, Math.min(.72, .5 + (st - rs) / 60)), won = Math.random() < (cash ? Math.max(.35, Math.min(.62, pv)) : pv);
  const loseV = 3 + Math.floor(Math.random() * 5), W = won ? 1 : 0, seq = [...Array(H2_WIN - 1).fill(W), ...Array(loseV).fill(1 - W)];
  for (let i = seq.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; } seq.push(W);
  const goal = cash ? `Win ${money(prize)}` : `1 training win · ${Math.min(TQ_WIN, T.w + 1)} of ${TQ_WIN}`, kick = cash ? `💵 Cash head-to-head · $${fee}` : '🏋️ Training match';
  popOpen(`<div class="pp qfx qrx nv qr2"><div class="nv-bg" style="background-image:url('${p.src}')"></div><p class="nv-brand">PhotoPicks</p>
    <div class="nv-pillrow"><span class="nv-pill">${cash ? `Cash race · $${fee}` : 'Training race'}</span></div><h2 class="nv-h">Race to ${H2_WIN}</h2><p class="nv-s">${cash ? `First to ${H2_WIN} votes wins <b class="gold">${money(prize)}</b>` : `First to ${H2_WIN} votes · ${goal}`}</p>
    <div class="qr2-c me" id="qrCA"><div class="qr2-im"><img src="${p.src}" alt=""><span class="qr2-n">${nm} · <b>You</b></span></div><div class="qr2-r"><b id="qrAv">0</b><small>of ${H2_WIN} votes</small><span class="qr2-p" id="qrAp">${pipsN(0, H2_WIN)}</span></div></div>
    <div class="qr2-c" id="qrCB"><div class="qr2-im"><img src="${o.src}" alt=""><span class="qr2-n">${esc(o.t)}</span></div><div class="qr2-r"><b id="qrBv">0</b><small>of ${H2_WIN} votes</small><span class="qr2-p" id="qrBp">${pipsN(0, H2_WIN)}</span></div></div>
    <p class="qr2-v" id="qrV">🗳️ The crowd is voting…</p><div class="nv-goal" id="qrG"><b>${H2_WIN}</b> votes to ${cash ? `win ${money(prize)}` : 'win'}</div><p class="nv-sim">Demo · simulated votes · rival ${esc(oh)}</p></div>`);
  const run = () => { let i = 0, A = 0, B = 0; const iv = setInterval(() => { if (!document.getElementById('qrG')) { clearInterval(iv); return; }
      const me = seq[i++]; if (me) A++; else B++; const vh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)];
      $('#qrAv').textContent = A; $('#qrBv').textContent = B; $('#qrAp').innerHTML = pipsN(A, H2_WIN); $('#qrBp').innerHTML = pipsN(B, H2_WIN);
      const c = document.getElementById(me ? 'qrCA' : 'qrCB'); c.classList.remove('hit'); void c.offsetWidth; c.classList.add('hit');
      $('#qrV').innerHTML = `🗳️ <b>${vh}</b> voted for <b class="${me ? 'me' : ''}">${me ? nm : esc(o.t)}</b>`;
      const g = $('#qrG'), left = H2_WIN - A, bl = H2_WIN - B; g.innerHTML = left > 0 ? `<b>${left}</b> more vote${left === 1 ? '' : 's'} to ${cash ? `win ${money(prize)}` : 'win'}` : '<b>🏁</b> Across the line!';
      g.classList.toggle('hot', left <= 2 || bl <= 2);
      if (i < seq.length) return; clearInterval(iv); setTimeout(() => photoFinish(() => h2hDone(p, o, fee, won, A, B)), 600); }, 1000); };
  qrCount(p, o, oh, run, kick, cash ? `First to ${H2_WIN} votes wins ${money(prize)}` : `First to ${H2_WIN} votes · ${goal}`); }
function h2hDone(p, o, fee, won, A, B) { const cash = fee > 0, nm = esc(rcName(p)), prize = +(fee * H2H_PAY).toFixed(2), H = p.h2h = p.h2h || { w: 0, l: 0, cash: 0 }, T = p.tq = p.tq || { w: 0, l: 0 }; let big, line, extra = '', fresh = false;
  if (won) H.w++; else H.l++;
  if (cash) { if (won) { H.cash = +(H.cash + prize).toFixed(2); S.cash = +((S.cash || 0) + prize).toFixed(2); try { earnAdd({ kind: 'h2', pid: p.id, t: p.title, amt: prize }); } catch (e) {} }
    big = won ? 'You won!' : 'So close'; line = won ? `${nm} wins ${A}–${B}` : `${esc(o.t)} wins ${B}–${A}`; extra = won ? `<div class="h2w-amt">${money(prize)}</div><p class="qw-o">added to your cash · record ${H.w}–${H.l}</p>` : `<p class="qw-o">You lost $${fee} · record ${H.w}–${H.l}</p>`; }
  else { if (won) { T.w++; p.form = Math.min(10, (p.form || 0) + 1); qlStrength(p); p.vd.pct = Math.min(85, p.vd.pct + 1); } else T.l++;
    if (T.w >= TQ_WIN) { p.cashOK = 1; fresh = true; } const dots = `<div class="h2w-dots">${[0, 1, 2].map(i => `<i class="${i < T.w ? 'w' : ''}"></i>`).join('')}</div>`;
    big = fresh ? 'Ready for Cash Races!' : won ? 'Training win!' : 'So close'; line = won ? `${nm} wins ${A}–${B}` : `${esc(o.t)} wins ${B}–${A}`;
    extra = fresh ? `<p class="qw-o">${nm} can now race in Finals ($2–$20) and cash head-to-heads.</p>` : T.l >= TQ_WIN ? `<p class="qw-o">Training over at ${T.w}–${T.l}. Start a fresh run or try another photo.</p>` : `${dots}<p class="qw-o">${T.w} of ${TQ_WIN} training wins · ${TQ_WIN - T.w} more to be Ready for Cash Races</p>`;
    if (T.l >= TQ_WIN && !fresh) p.tq = { w: 0, l: 0 }; }
  save(); try { paintWallet(); paintGems(); } catch (e) {}
  popOpen(`<div class="pp qfx nv qw"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big ${big.length > 12 ? 'sm' : ''}">${big}</h2><i class="nv-sw"></i>
    <div class="qw-ph ${won ? '' : 'out'}"><img src="${p.src}" alt="">${fresh ? `<i class="qw-rz">${rosette(0)}</i>` : ''}</div><p class="qw-r">${line}</p>${extra}
    ${p.cashOK ? `<button class="btn block nv-go" id="h2Ag">${cash ? `💵 Race again · $${fee}` : '🏁 Enter a Final'}</button>` : `<button class="btn block nv-go" id="h2Ag">🏋️ Train again · ${TQ_COST} 🟡</button>`}
    <div style="text-align:center"><button class="link nv-later" id="h2Bk">Back to stable</button></div></div>`);
  if (won) setTimeout(() => { try { cash ? cashExplosion(prize, { label: 'Head-to-head win' }) : gemExplosion(0, { label: fresh ? 'Ready for Cash Races!' : 'Training win!' }); rvConfetti(document.querySelector('.qw'), fresh || cash ? 110 : 60); } catch (e) {} }, 300);
  $('#h2Ag').onclick = () => { if (p.cashOK && !cash) { popClose(); qfStart(p); } else h2hOpen(p, fee); }; $('#h2Bk').onclick = () => { popClose(); finalsTab(); }; }
(() => { const qr = qfRace; qfRace = function (p, L) { const self = this, args = arguments; const fee = window.__qfFee || 2;
  popOpen(`<div class="pp qfx nv qw"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">The Final · $${fee}</span></div><h2 class="nv-h2">6 finalists · 1st wins ${money(fee * QF_PAY[0])}</h2>
    <div class="qf2-g">${L.map(x => `<div class="qf2-t ${x.me ? 'me' : ''}"><img src="${x.src}" alt="">${x.me ? '<em>YOU</em>' : ''}<span>${esc(x.me ? rcName(p) : x.t)}</span></div>`).join('')}</div>
    <b class="qr-num nvn" id="qfN">3</b><p class="qw-o">The crowd’s votes decide the order</p></div>`);
  let n = 3; const t = setInterval(() => { const e = document.getElementById('qfN'); if (!e) { clearInterval(t); return; } n--; e.textContent = n > 0 ? n : 'GO!'; e.classList.remove('go'); void e.offsetWidth; e.classList.add('go');
    if (n <= 0) { clearInterval(t); setTimeout(() => qr.apply(self, args), 650); } }, 900); }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.nv-s b.gold{color:#F3D98B;font-weight:900}.h2w-amt{margin:2px 0;font:900 3.2rem/1 Fraunces,Georgia,serif;color:#F3D98B;text-shadow:0 0 18px rgba(243,217,139,.45);animation:cdPop .6s ease-out both}
.h2w-dots{display:flex;justify-content:center;gap:10px;margin:8px 0 2px}.h2w-dots i{width:20px;height:20px;border-radius:50%;background:#3A4766;box-shadow:inset 0 0 0 2px #8C9AB5}.h2w-dots i.w{background:#E9B949;box-shadow:0 0 10px rgba(233,185,73,.6)}
html body .nv .qr-num.nvn{display:block;margin:14px 0 2px;font:900 4.5rem/1 Fraunces,Georgia,serif;color:#F3D98B}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v182 ok')
# pass 2: the 3-2-1 covers the whole race screen
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .nv>.qr-cd{position:absolute!important;inset:-12px -16px -28px!important;z-index:20!important;justify-content:center;padding:0 16px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v182 pass2 ok')
# pass 3: gold label on the navy countdown
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .nv .qr-cd .pp-k{color:#F3D98B!important;-webkit-text-fill-color:#F3D98B!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v182 pass3 ok')
