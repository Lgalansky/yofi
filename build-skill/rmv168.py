# Real Money build, step 171 (after rmv167.py): the Play tab becomes your Stable.
#  Vote = the road to the Final (your votes move photos through the qualifier). Stable = play with your photos any time.
#  - Every entered photo is a horse in your stable: status, 💪 form, head-to-head record, cash won.
#  - 🏋️ Train · free: instant head-to-head vs a rival photo, 15 crowd votes play out live (~6 s). Win = +10 🟡, form +1.
#  - 💵 Head-to-head · $2 / $5: same, winner takes 1.7× ($3.40 / $8.50). Only for photos that have qualified once.
#  - Finalist → 🏁 Race the Final. Qualifying → ⚖️ Vote to move it. Missed the cut → train 5 wins, then re-enter free.
#    Resting after a Final → re-enter for 100 🟡.
#  - Tune-up after a miss now leads to the Stable; the old Play games (Match Race, Derby, …) are gone from the path.
#  Simulated: rivals and crowd votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("Train it to race again: a free tune-up, then win 5 head-to-heads for coins.", "Send it to your stable: a free tune-up, then win 5 training head-to-heads to race again.", 2)
s = s.replace("function fcNotify() {", r"""const H2H_V = 15, H2H_FEES = [2, 5], H2H_PAY = 1.7, TRN_COINS = 10;
const stHorses = () => (S.photos || []).filter(p => p.ql || p.raced || p.fin);
const stProven = p => !!(p.fin || p.raced || p.qok || (p.ql && p.ql.done === 'q'));
function stStatus(p) { const q = p.ql;
  if (p.fin) return { k: 'fin', t: '🏆 Finalist', btn: `<button class="btn st-b cash" data-stf="${p.id}">🏁 Race the Final</button>` };
  if (q && !q.done) return { k: 'q', t: `🎀 Qualifying · ${q.w}–${q.l}`, btn: '<button class="btn st-b" data-stv>⚖️ Vote to move it</button>' };
  if (q && q.done === 'x') { const n = TR_WIN - (p.trw || 0); return n > 0 ? { k: 'x', t: `💪 Train ${n} more win${n === 1 ? '' : 's'} to re-enter`, btn: '' } : { k: 'x', t: '✓ Race fit', btn: `<button class="btn st-b cash" data-str="${p.id}" data-free="1">🎀 Re-enter · free</button>` }; }
  return { k: 'r', t: p.raced ? `Resting · Final ${ppOrd(p.raced.rank)}` : 'Resting', btn: `<button class="btn st-b" data-str="${p.id}">🎀 Re-enter · ${ENTRY_COINS} 🟡</button>` }; }
function stCard(p) { const st = stStatus(p), H = p.h2h || { w: 0, l: 0, cash: 0 }, pr = stProven(p);
  return `<div class="st-c ${st.k}"><div class="st-top"><img src="${p.src}" alt=""><div class="st-i"><b>${esc(rcName(p))}</b><span class="st-s">${st.t}</span>
      <span class="st-m"><em>💪 Form +${p.form || 0}</em><em>H2H ${H.w}–${H.l}</em>${H.cash ? `<em class="cash">${money(H.cash)} won</em>` : ''}</span></div></div>
    <div class="st-a"><button class="btn st-b tr" data-sth="${p.id}" data-m="t">🏋️ Train · free</button>${pr ? `<button class="btn st-b cash" data-sth="${p.id}" data-m="c">💵 Head-to-head · $2</button>` : '<button class="btn st-b lock" disabled>🔒 Cash H2H · qualify once</button>'}</div>${st.btn ? `<div class="st-a one">${st.btn}</div>` : ''}</div>`; }
function finalsTab() { const H = stHorses();
  openFlow(`<div class="fnx stx"><h1 class="fn-h">🐎 Your stable</h1><p class="fn-s">Your photos are your horses. Train them for coins, race them head-to-head for cash. ${isYoungW() ? 'Judging' : 'Voting'} gets them to the Final.</p>
    ${H.length ? H.map(stCard).join('') : '<div class="st-e"><p>Your stable is empty.</p></div>'}
    <button class="btn block db-go st-new" data-stn>📷 Enter a new photo${qlReal().length ? ` · ${ENTRY_COINS} 🟡` : ' · free'}</button><p class="db-sim">Prototype: rivals and crowd votes are simulated</p></div>`, false);
  $('#flow').classList.add('astab'); ['segJudge', 'segStudio', 'segGallery'].forEach(id => $('#' + id).setAttribute('aria-pressed', 'false')); $('#segCompete').setAttribute('aria-pressed', 'true'); setTimeout(() => { $('#ptitle').textContent = 'Stable'; }, 0); }
function gmHub() { try { popClose(); } catch (e) {} finalsTab(); }
document.addEventListener('click', e => { const t = e.target.closest && e.target.closest('[data-sth],[data-stf],[data-stv],[data-str],[data-stn]'); if (!t || !t.closest('#flow')) return; e.preventDefault();
  const P = id => (S.photos || []).find(x => x.id === id);
  if (t.dataset.sth) h2hOpen(P(t.dataset.sth), t.dataset.m === 'c' ? 2 : 0);
  else if (t.dataset.stf) { closeFlow(); qfStart(P(t.dataset.stf)); }
  else if (t.hasAttribute('data-stv')) { closeFlow(); go('judge'); renderJudge(); }
  else if (t.dataset.str) { const p = P(t.dataset.str), free = t.dataset.free === '1'; if (!free && (S.gems || 0) < ENTRY_COINS) { toast(`🟡 You need ${ENTRY_COINS} coins · vote to earn them`); return; }
    if (free) S.freeRe = 1; p.fin = 0; p.ql = null; p.trw = 0; p.rq = (p.rq || 0) + 1; save(); closeFlow(); setTimeout(() => upDone(p), 200); }
  else if (t.hasAttribute('data-stn')) { closeFlow(); setTimeout(finPick, 200); } });
function trBegin(p, tuned) { p.tr = null; p.trw = p.trw || 0; save(); try { popClose(); } catch (e) {} toast(tuned ? `✨ ${rcName(p)} tuned up · train it in your stable` : `🐎 ${rcName(p)} is in your stable`); setTimeout(finalsTab, 250); }
// head-to-head (training or cash), full screen, plays out instantly
function h2hOpen(p, fee, rv) { if (!p) return; const k = photoShow(p) || 'pets', pool = SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src), o = rv || pool[Math.floor(Math.random() * pool.length)] || { src: p.src, title: 'A rival' };
  const h = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)], cash = fee > 0, nm = esc(rcName(p)), R = rv ? rv : { src: o.src, title: o.title || 'A rival', h };
  popOpen(`<div class="pp qfx h2x"><p class="pp-k">${cash ? `💵 Cash head-to-head` : '🏋️ Training head-to-head'} · ${esc(showName(k))}</p><h2 class="db-h">${nm} vs ${esc(R.title)}</h2>
    <div class="h2-vs"><div class="me"><img src="${p.src}" alt=""><small>You · 💪 +${p.form || 0}</small></div><b class="h2-x">VS</b><div><img src="${R.src}" alt=""><small>${esc(R.h)}</small></div></div>
    ${cash ? `<div class="qfp-f h2-f">${H2H_FEES.map(f => `<button data-h2f="${f}" class="${f === fee ? 'on' : ''}"><b>$${f}</b><small>win ${money(f * H2H_PAY)}</small></button>`).join('')}</div>
      <div class="qfp-p">Winner takes <b>${money(fee * H2H_PAY)}</b><small>You both pay $${fee}. ${H2H_V} crowd votes decide it.</small></div>`
    : `<div class="qfp-p">Win: <b>+${TRN_COINS} 🟡</b> and 💪 form +1<small>Free. ${H2H_V} crowd votes decide it. Losing costs nothing.</small></div>`}
    <button class="btn block db-go ${cash ? 'cashb' : ''}" id="h2Go">${cash ? `💵 Play · $${fee}` : '🏋️ Start training'}</button><div style="text-align:center"><button class="link pc-later" id="h2L">Back to stable</button></div>
    <p class="db-sim">Prototype: rival and votes are simulated</p></div>`);
  document.querySelectorAll('[data-h2f]').forEach(b => b.onclick = () => h2hOpen(p, +b.dataset.h2f, R));
  $('#h2L').onclick = () => { popClose(); finalsTab(); };
  $('#h2Go').onclick = () => cash ? payCash(fee, `A $${fee} head-to-head`, () => h2hLive(p, R, fee)) : h2hLive(p, R, 0); }
function h2hLive(p, R, fee) { const cash = fee > 0, st = qlStrength(p), rs = cash ? st + (Math.random() - .5) * 14 : st - 4 - Math.random() * 8, pv = Math.max(.3, Math.min(.72, .5 + (st - rs) / 60));
  const won = Math.random() < (cash ? Math.max(.35, Math.min(.62, pv)) : pv), mv = won ? 8 + Math.floor(Math.random() * 4) : 3 + Math.floor(Math.random() * 5), seq = [...Array(H2H_V)].map((_, i) => i < mv);
  for (let i = H2H_V - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; }
  const nm = esc(rcName(p)), prize = +(fee * H2H_PAY).toFixed(2);
  popOpen(`<div class="pp qfx h2x"><p class="pp-k">${cash ? `💵 $${fee} head-to-head` : '🏋️ Training'} · live</p><h2 class="db-h">The crowd is voting…</h2>
    <div class="h2-vs"><div class="me" id="h2A"><img src="${p.src}" alt=""><small>You</small><b id="h2a">0</b></div><b class="h2-x">VS</b><div id="h2B"><img src="${R.src}" alt=""><small>${esc(R.h)}</small><b id="h2b">0</b></div></div>
    <div class="h2-bar"><i id="h2i" style="width:50%"></i></div><p class="db-com" id="h2n">0 of ${H2H_V} votes</p><div id="h2R"></div><p class="db-sim">Prototype: votes are simulated</p></div>`);
  let v = 0, m = 0; const iv = setInterval(() => { if (!document.getElementById('h2n')) { clearInterval(iv); return; } if (seq[v]) m++; v++;
    $('#h2a').textContent = m; $('#h2b').textContent = v - m; $('#h2i').style.width = (m / v * 100) + '%'; $('#h2n').textContent = `${v} of ${H2H_V} votes${v < H2H_V ? (m > v - m ? ' · you lead' : m < v - m ? ' · you trail' : ' · level') : ''}`;
    if (v < H2H_V) return; clearInterval(iv); const H = p.h2h = p.h2h || { w: 0, l: 0, cash: 0 };
    if (won) { H.w++; if (cash) { H.cash = +(H.cash + prize).toFixed(2); S.cash = +((S.cash || 0) + prize).toFixed(2); try { earnAdd({ kind: 'h2', pid: p.id, t: p.title, amt: prize }); } catch (e) {} }
      else { S.gems = (S.gems || 0) + TRN_COINS; p.form = Math.min(10, (p.form || 0) + 1); qlStrength(p); p.vd.pct = Math.min(85, p.vd.pct + 1); if (p.ql && p.ql.done === 'x') p.trw = (p.trw || 0) + 1; } }
    else H.l++; save();
    document.getElementById(won ? 'h2A' : 'h2B').classList.add('win'); document.querySelector('.h2x .db-h').textContent = won ? `${rcName(p)} wins ${m}–${H2H_V - m}!` : `${R.title} wins ${H2H_V - m}–${m}`;
    const fit = !cash && won && p.ql && p.ql.done === 'x' && (p.trw || 0) >= TR_WIN;
    $('#h2R').innerHTML = `${won ? (cash ? `<div class="rv-won"><span>Cash won</span><b>${money(prize)}</b></div>` : `<p class="re-rzl">+${TRN_COINS} 🟡 · 💪 form +1${p.ql && p.ql.done === 'x' ? ` · ${Math.min(TR_WIN, p.trw)}/${TR_WIN} training wins` : ''}</p>`) : `<p class="db-s">${cash ? `You lost $${fee}.` : 'No harm done in training.'} Record ${H.w}–${H.l}.</p>`}
      ${fit ? `<p class="re-rzl">✓ ${nm} is race fit! Re-enter it free from your stable.</p>` : ''}
      <button class="btn block db-go ${cash ? 'cashb' : ''}" id="h2Ag">${cash ? `💵 Again · $${fee}` : '🏋️ Train again'}</button><div style="text-align:center"><button class="link pc-later" id="h2Bk">Back to stable</button></div>`;
    if (won) setTimeout(() => { try { cash ? (paintWallet(), cashExplosion(prize, { label: 'Head-to-head' })) : (paintGems(), gemExplosion(TRN_COINS, { label: 'Training win' })); rvConfetti(document.querySelector('.h2x'), 40); } catch (e) {} }, 250);
    $('#h2Ag').onclick = () => h2hOpen(p, fee); $('#h2Bk').onclick = () => { popClose(); finalsTab(); }; }, 400); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.stx .fn-s{margin-bottom:12px}.st-c{margin:0 0 10px;padding:12px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.st-c.fin{box-shadow:inset 0 0 0 2px #D9AE4F;background:#FFFCF3}.st-c.q{box-shadow:inset 0 0 0 2px #2F6B3F}
.st-top{display:flex;gap:12px;align-items:center}.st-top img{width:72px;height:72px;border-radius:12px;object-fit:cover;box-shadow:0 0 0 3px #E5C987;flex:none}.st-i{min-width:0;flex:1}
.st-i b{display:block;font:800 1.08rem Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.st-s{display:block;margin:2px 0 5px;font:800 .8rem Nunito,system-ui;color:#3D4A5C}
.st-m{display:flex;flex-wrap:wrap;gap:5px}.st-m em{font-style:normal;font:800 .7rem Nunito,system-ui;padding:2px 8px;border-radius:999px;background:#F3EEE5;color:#5B4A3F}.st-m em.cash{background:#E5F2E4;color:#2F6B3F}
.st-a{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px}.st-a.one{grid-template-columns:1fr;margin-top:6px}
html body .st-b{width:100%!important;min-height:40px!important;margin:0!important;padding:6px 8px!important;border-radius:999px!important;font:800 .8rem Nunito,system-ui!important;background:#14213D!important;color:#fff!important;box-shadow:none!important}
html body .st-b.tr{background:#2E4F8A!important}html body .st-b.cash{background:#2F6B3F!important}html body .st-b.lock{background:#EEE6D8!important;color:#8A7B6C!important}
.st-e{padding:20px;text-align:center;color:#5B4A3F}html body .st-new{margin-top:6px!important}
.h2-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;margin:12px 0}.h2-vs>div{position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;transition:transform .3s}
.h2-vs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:14px;box-shadow:0 0 0 3px #EADCC6}.h2-vs .me img{box-shadow:0 0 0 3px #2F6B3F}.h2-vs small{font:800 .76rem Nunito,system-ui;color:#5B4A3F}
.h2-vs>div>b{font:900 2rem/1 Fraunces,Georgia,serif;color:#14213D}.h2-vs>div.win{transform:scale(1.05)}.h2-vs>div.win img{box-shadow:0 0 0 4px #D9AE4F,0 0 18px rgba(217,174,79,.6)}
.h2-vs>div.win::after{content:'🏆 WINNER';position:absolute;top:8px;left:50%;transform:translateX(-50%);padding:3px 10px;border-radius:999px;background:#14213D;color:#F3D98B;font:900 .7rem Nunito,system-ui;letter-spacing:.05em;white-space:nowrap}
.h2-x{font:900 1.1rem Fraunces,Georgia,serif;color:#fff;background:#14213D;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #D9AE4F}
.h2-bar{height:14px;border-radius:7px;background:#E7A595;overflow:hidden;margin:4px 0}.h2-bar i{display:block;height:100%;background:linear-gradient(90deg,#7FC48E,#2F6B3F);transition:width .35s;border-right:2px solid #fff}
.h2-f{grid-template-columns:1fr 1fr;margin-bottom:8px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v168 ok')
