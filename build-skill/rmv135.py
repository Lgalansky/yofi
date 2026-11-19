# Real Money build, step 138 (after rmv134.py): Photo Derby, the first 4-player skill race.
#  - Entry: coins (25 🟡, 1st 70 / 2nd 30) or $1 / $2 / $5 / $10. 4 riders, 15% fee shown, prize pool split
#    70% / 30% (e.g. $2: 1st $4.76, 2nd $2.04).
#  - Lobby: "Finding riders at your level…" — 3 opponents join one by one with their Eye score.
#  - Race: everyone plays the same 10 photo pairs (Sprint pairs: same category, crowd result by photo appeal).
#    Right answer = 10 points + up to 5 speed bonus; your horse and the other 3 move after every pair.
#  - Finish: standings, prize to balance, Rematch / Step up / Done. Your Eye score counts these picks.
#  - Entry points: card at the top of the Finals tab, row in the coins menu.
#  Simulated: opponents (accuracy around your Eye level ± 10%, answer times 1.4–4.5 s), clearly labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<p class="fn-s">A new Final whenever 6 finalists are in. Pick for real cash.</p>', '<p class="fn-s">A new Final whenever 6 finalists are in. Pick for real cash.</p>${derbyCardHTML()}')
RA("if (!newbie()) I.push({ ic: '⚡', t: 'Quick Sprint',",
   "if (!newbie()) I.push({ ic: '🏇', t: 'Photo Derby', d: 'Race 3 players on the same 10 photo pairs. Play for coins or cash.', cost: 25, src: (SEED.find(z => z.src && z.cat === 'Pets') || {}).src || '', go: () => { closeSheet(); setTimeout(derbyOpen, 250); } });\n  if (!newbie()) I.push({ ic: '⚡', t: 'Quick Sprint',")
s = s.replace("function fcNotify() {", r"""const DB_TIERS = [{ fee: 25, coins: 1 }, { fee: 1 }, { fee: 2 }, { fee: 5 }, { fee: 10 }], DB_N = 10;
function dbPrize(t) { if (t.coins) return [70, 30]; const pool = +(4 * t.fee * .85).toFixed(2), a = +(pool * .7).toFixed(2); return [a, +(pool - a).toFixed(2)]; }
const dbAmt = (t, v) => t.coins ? `${v} 🟡` : money(v);
function dbEye() { return (S.eyeN || 0) >= 10 ? Math.max(.4, Math.min(.92, (S.eyeOk || 0) / S.eyeN)) : .64; }
function derbyCardHTML() { return `<button class="dbc" data-derby><span class="dbc-ic">🏇</span><span class="dbc-t"><b>Photo Derby</b><small>Race 3 players · same 10 photo pairs · 2 min</small></span><em>from $1 ›</em></button>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-derby]'); if (b) { e.preventDefault(); derbyOpen(); } });
function derbyOpen(ti0) { let ti = ti0 == null ? 2 : ti0; const draw = () => { const t = DB_TIERS[ti], [p1, p2] = dbPrize(t);
    popOpen(`<div class="pp dbx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 Photo Derby</p><h2 class="db-h">Race 3 players</h2>
      <p class="db-s">All 4 riders get the <b>same 10 photo pairs</b>. Pick the photo the crowd chose. Right and fast moves your horse.</p>
      <div class="rc-st db-tier" role="group" aria-label="Entry">${DB_TIERS.map((x, i) => `<button data-dbt="${i}" aria-pressed="${i === ti}">${x.coins ? `${x.fee} 🟡` : '$' + x.fee}</button>`).join('')}</div>
      <div class="db-pz"><div><small>🥇 1st</small><b>${dbAmt(t, p1)}</b></div><div><small>🥈 2nd</small><b>${dbAmt(t, p2)}</b></div><div><small>Entry</small><b>${dbAmt(t, t.fee)}</b></div></div>
      <p class="db-fee">${t.coins ? 'Coin race · practise your eye for free' : `4 riders · ${money(p1 + p2)} prize pool · ${money(+(4 * t.fee - p1 - p2).toFixed(2))} PhotoPicks fee (15%)`}</p>
      <button class="btn block db-go ${t.coins ? '' : 'cashb'}" id="dbGo">${t.coins ? `🏇 Race for coins · ${t.fee} 🟡` : `🏇 Race for ${money(t.fee)}`}</button>
      <p class="db-eye">👁️ Your eye: <b>${Math.round(dbEye() * 100)}%</b> · you’ll race players at your level</p><p class="db-sim">Prototype: opponents are simulated</p></div>`);
    document.querySelectorAll('#coach [data-dbt]').forEach(b => b.onclick = () => { ti = +b.dataset.dbt; window.__keepScroll = 1; draw(); });
    document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#dbGo').onclick = () => { const t = DB_TIERS[ti]; window.__dbTi = ti;
      if (t.coins) { if ((S.gems || 0) < t.fee) { toast(`You need ${t.fee} coins · vote to earn more`); return; } S.gems -= t.fee; save(); paintGems(); derbyMatch(t); }
      else { popClose(); payCash(t.fee, 'A Photo Derby entry', () => setTimeout(() => derbyMatch(t), 250)); } }; };
  draw(); }
function derbyMatch(t) { const seed = Date.now() % 1e7, r = cpRng(seed), eye = dbEye(), names = ppShuffle(QS_NAMES.slice(), r).slice(0, 3), col = ['#C0392B', '#2E86C1', '#8E44AD'];
  const O = names.map((h, i) => ({ h, acc: Math.max(.45, Math.min(.9, eye + (r() - .5) * .2)), c: col[i] })), me = ((S.user && S.user.h) || 'you');
  popOpen(`<div class="pp dbx"><p class="pp-k">🏇 Photo Derby · ${dbAmt(t, t.fee)}</p><h2 class="db-h" id="dbMh">Finding riders at your level…</h2>
    <div class="db-lobby"><div class="db-rd in me"><i>${esc(me[0].toUpperCase())}</i><b>You</b><small>Eye ${Math.round(eye * 100)}%</small></div>${O.map((o, i) => `<div class="db-rd" id="dbR${i}"><i>?</i><b>Searching…</b><small>&nbsp;</small></div>`).join('')}</div>
    <p class="db-sim">Prototype: opponents are simulated</p></div>`);
  O.forEach((o, i) => setTimeout(() => { const el = document.getElementById('dbR' + i); if (!el) return; el.classList.add('in'); el.innerHTML = `<i style="background:${o.c}">${esc(o.h[0].toUpperCase())}</i><b>@${esc(o.h)}</b><small>Eye ${Math.round(o.acc * 100)}%</small>`; }, 700 + i * 650));
  setTimeout(() => { const h = document.getElementById('dbMh'); if (h) h.textContent = '3 riders found · gates opening…'; }, 700 + 3 * 650);
  setTimeout(() => derbyRun(t, O, seed), 700 + 3 * 650 + 1100); }
function derbyRun(t, O, seed) { const r = cpRng(seed * 7 + 11), pairs = cpPairs(DB_N, seed * 7 + 11, true), me = { h: 'You', c: '#D9AE4F', sc: 0, tm: 0, ok: 0, me: 1 };
  O.forEach(o => { o.sc = 0; o.tm = 0; o.res = pairs.map(() => { const okk = r() < o.acc, tm = 1.4 + r() * 3.1; return { okk, tm, pts: okk ? 10 + Math.max(0, 5 - Math.floor(tm)) : 0 }; }); });
  const R = [me].concat(O), MAX = DB_N * 15;
  popOpen(`<div class="pp dbx dbr"><div class="db-top"><b id="dbQ">Pair 1 of ${DB_N}</b><span id="dbClk">0.0s</span></div>
    <div class="db-trk">${R.map((x, i) => `<div class="db-ln ${x.me ? 'me' : ''}"><span class="db-nm">${x.me ? 'You' : '@' + esc(x.h)}</span><span class="db-rail"><i class="db-hs" id="dbH${i}" style="left:0%"><u style="background:${x.c}"></u>🏇</i></span><b class="db-sc" id="dbS${i}">0</b></div>`).join('')}<i class="db-fin"></i></div>
    <h3 class="db-qh">Which photo did the crowd pick?</h3><div class="db-pair" id="dbPair"></div><p class="db-fb" id="dbFb">Tap a photo · faster = more points</p></div>`);
  let i = 0, tq = 0, lock = false; const clk = setInterval(() => { const c = document.getElementById('dbClk'); if (!c) { clearInterval(clk); return; } c.textContent = `${((Date.now() - tq) / 1000).toFixed(1)}s`; }, 100);
  const paint = () => R.forEach((x, k) => { const h = document.getElementById('dbH' + k), sc = document.getElementById('dbS' + k); if (h) h.style.left = `${Math.min(86, x.sc / MAX * 86 * 1.25)}%`; if (sc) sc.textContent = x.sc; });
  const show = () => { const p = pairs[i]; lock = false; tq = Date.now(); $('#dbQ').textContent = `Pair ${i + 1} of ${DB_N}`;
    $('#dbPair').innerHTML = ['a', 'b'].map(k => `<button class="db-ph" data-dp="${k}"><img src="${p[k].src}" alt=""><span class="db-pc"></span></button>`).join('');
    document.querySelectorAll('#dbPair [data-dp]').forEach(b => b.onclick = () => { if (lock) return; lock = true; const tm = (Date.now() - tq) / 1000, okk = (b.dataset.dp === 'a') === (p.pa >= 50), pts = okk ? 10 + Math.max(0, 5 - Math.floor(tm)) : 0;
      me.sc += pts; me.tm += tm; if (okk) me.ok++; O.forEach(o => { o.sc += o.res[i].pts; o.tm += o.res[i].tm; });
      document.querySelectorAll('#dbPair [data-dp]').forEach(x => { const a = x.dataset.dp === 'a', pc = a ? p.pa : 100 - p.pa; x.classList.add(pc >= 50 ? 'crowd' : 'not'); x.querySelector('.db-pc').textContent = pc + '%'; });
      b.classList.add(okk ? 'ok' : 'bad'); const F = $('#dbFb'); F.className = 'db-fb ' + (okk ? 'ok' : 'bad'); F.innerHTML = okk ? `✓ Crowd pick · <b>+${pts}</b>${pts > 10 ? ` (speed +${pts - 10})` : ''}` : '✕ The crowd picked the other photo';
      try { navigator.vibrate && navigator.vibrate(okk ? 12 : [25, 30, 25]); } catch (e) {} paint(); i++;
      setTimeout(() => { if (i < DB_N) { F.className = 'db-fb'; F.textContent = 'Tap a photo · faster = more points'; show(); } else { clearInterval(clk); derbyEnd(t, R); } }, 1100); }); };
  show(); }
function derbyEnd(t, R) { const ord = R.slice().sort((a, b) => b.sc - a.sc || a.tm - b.tm), pl = ord.findIndex(x => x.me) + 1, [p1, p2] = dbPrize(t), prize = pl === 1 ? p1 : pl === 2 ? p2 : 0, me = R[0];
  S.eyeN = (S.eyeN || 0) + DB_N; S.eyeOk = (S.eyeOk || 0) + me.ok;
  if (prize) { if (t.coins) { S.gems = (S.gems || 0) + prize; } else { S.cash = +((S.cash || 0) + prize).toFixed(2); } } save();
  const ti = window.__dbTi == null ? 2 : window.__dbTi, up = Math.min(DB_TIERS.length - 1, ti + 1);
  popOpen(`<div class="pp dbx dbe ${prize ? 'won' : ''}"><p class="pp-k">🏇 Photo Derby · ${dbAmt(t, t.fee)}</p><h2 class="db-h">${pl === 1 ? 'You won the Derby!' : pl === 2 ? 'Second place, paid!' : `You finished ${ppOrd(pl)}`}</h2>
    ${prize ? `<div class="rv-won"><span>${t.coins ? 'You won' : 'Cash won'}</span><b>${dbAmt(t, prize)}</b></div>` : `<p class="db-s">${ord[1].sc - me.sc <= 15 ? `Just <b>${ord[1].sc - me.sc} points</b> off 2nd place. One more?` : 'Top 2 get paid. One more race?'}</p>`}
    <div class="db-res">${ord.map((x, k) => `<div class="${x.me ? 'me' : ''}"><em>${['🥇', '🥈', '3rd', '4th'][k]}</em><b>${x.me ? 'You' : '@' + esc(x.h)}</b><span>${x.sc} pts · ${x.tm.toFixed(1)}s</span><i>${k === 0 ? dbAmt(t, p1) : k === 1 ? dbAmt(t, p2) : ''}</i></div>`).join('')}</div>
    <p class="db-eye">You matched the crowd on <b>${me.ok} of ${DB_N}</b> · 👁️ Eye now ${Math.round(dbEye() * 100)}%</p>
    <button class="btn block db-go ${t.coins ? '' : 'cashb'}" id="dbRe">🔁 Rematch · ${dbAmt(t, t.fee)}</button>${up !== ti ? `<button class="btn block quiet db-up" id="dbUp">Step up · ${dbAmt(DB_TIERS[up], DB_TIERS[up].fee)} race</button>` : ''}
    <div style="text-align:center"><button class="link pc-later" id="dbDone">Done</button></div><p class="db-sim">Prototype: opponents are simulated</p></div>`);
  if (prize) setTimeout(() => { try { t.coins ? (paintGems(), gemExplosion(prize, { label: 'Photo Derby' })) : (paintWallet(), cashExplosion(prize, { label: 'Photo Derby' })); } catch (e) {} }, 350); else { try { paintGems(); paintWallet(); } catch (e) {} }
  if (pl === 1) setTimeout(() => { try { rvConfetti(document.querySelector('.dbe'), 50); } catch (e) {} }, 200);
  $('#dbRe').onclick = () => { $('#dbGo') ; popClose(); setTimeout(() => { derbyOpen(ti); setTimeout(() => { const g = document.getElementById('dbGo'); g && g.click(); }, 60); }, 200); };
  if ($('#dbUp')) $('#dbUp').onclick = () => { popClose(); setTimeout(() => derbyOpen(up), 200); }; $('#dbDone').onclick = () => popClose(); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.dbc{display:flex;align-items:center;gap:12px;width:100%;margin:10px 0 14px;padding:12px 14px;border:0;border-radius:16px;background:linear-gradient(135deg,#14213D,#1E3A6E);color:#fff;text-align:left;cursor:pointer;box-shadow:0 6px 18px rgba(20,33,61,.25),inset 0 0 0 1.5px #D9AE4F;font:inherit}
.dbc-ic{font-size:2rem;flex:none}.dbc-t{flex:1;display:flex;flex-direction:column}.dbc-t b{font:800 1.15rem Fraunces,Georgia,serif;color:#F3D98B}.dbc-t small{font-size:.8rem;opacity:.85}.dbc em{font-style:normal;font-weight:900;color:#F3D98B;white-space:nowrap}
html body .ppop .db-h{font:800 1.7rem/1.1 Fraunces,Georgia,serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:2px 0 6px}
.db-s{margin:0 0 10px;font-size:.92rem;line-height:1.45}.db-tier{margin:6px 0 10px}
.db-pz{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:0 0 6px}.db-pz div{background:#fff;border-radius:12px;padding:8px 4px;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:center}.db-pz small{display:block;font-size:.72rem;font-weight:800;color:#5B4A3F}.db-pz b{font:900 1.15rem Nunito,system-ui,sans-serif;color:#2F6B3F}
.db-fee,.db-eye{font-size:.78rem;opacity:.85;margin:4px 0 10px;text-align:center}.db-sim{font-size:.7rem;opacity:.55;text-align:center;margin:8px 0 0}
.db-lobby{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:14px 0}.db-rd{display:flex;flex-direction:column;align-items:center;gap:3px;padding:10px 2px;border-radius:14px;background:#F3EEE5;opacity:.5;transition:all .3s}.db-rd.in{opacity:1;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;animation:qsPlus .35s ease-out}.db-rd.me{box-shadow:inset 0 0 0 2px #D9AE4F}
.db-rd i{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-weight:900;color:#fff;background:#B9AE9C}.db-rd.me i{background:#D9AE4F;color:#14213D}.db-rd b{font-size:.72rem;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.db-rd small{font-size:.66rem;opacity:.7}
.db-top{display:flex;justify-content:space-between;align-items:center;margin:0 0 6px;font-weight:900;color:#14213D}.db-top span{font-variant-numeric:tabular-nums;color:#5B4A3F}
.db-trk{position:relative;background:#14213D;border-radius:14px;padding:8px 10px;box-shadow:inset 0 0 0 1.5px #D9AE4F}
.db-ln{display:grid;grid-template-columns:76px 1fr 30px;align-items:center;gap:6px;height:30px}.db-nm{font-size:.7rem;font-weight:800;color:#C9D3E6;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.db-ln.me .db-nm{color:#F3D98B}
.db-rail{position:relative;height:24px;border-bottom:1px dashed rgba(255,255,255,.18)}.db-hs{position:absolute;bottom:-2px;font-style:normal;font-size:1.25rem;transform:scaleX(-1);transition:left .7s cubic-bezier(.3,1.3,.5,1)}.db-hs u{position:absolute;left:4px;top:2px;width:8px;height:8px;border-radius:50%}
.db-ln.me .db-hs{filter:drop-shadow(0 0 4px #F3D98B)}.db-sc{font-size:.78rem;font-weight:900;color:#fff;text-align:right}
.db-fin{position:absolute;top:8px;bottom:8px;right:44px;width:6px;background:repeating-linear-gradient(0deg,#fff 0 6px,#14213D 6px 12px)}
.db-qh{margin:12px 0 6px;font:800 1.05rem Nunito,system-ui,sans-serif;color:#14213D;text-align:center}
.db-pair{display:grid;grid-template-columns:1fr 1fr;gap:8px}.db-ph{position:relative;border:0;padding:0;border-radius:14px;overflow:hidden;cursor:pointer;aspect-ratio:3/4;background:#EEE}.db-ph img{width:100%;height:100%;object-fit:cover;display:block}
.db-ph.crowd{box-shadow:0 0 0 3px #2F6B3F}.db-ph.not{opacity:.6}.db-ph.bad{box-shadow:0 0 0 3px #B03A2E}.db-pc{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);font:900 1.1rem Nunito,system-ui,sans-serif;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.6)}
.db-fb{margin:8px 0 0;text-align:center;font-weight:800;font-size:.9rem;color:#5B4A3F;min-height:1.3em}.db-fb.ok{color:#2F6B3F}.db-fb.bad{color:#B03A2E}
.db-res{display:grid;gap:5px;margin:8px 0}.db-res div{display:grid;grid-template-columns:34px 1fr auto auto;gap:8px;align-items:center;padding:8px 10px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.db-res div.me{box-shadow:inset 0 0 0 2px #D9AE4F;background:#FFF8E6}.db-res em{font-style:normal;font-weight:900}.db-res span{font-size:.75rem;opacity:.75}.db-res i{font-style:normal;font-weight:900;color:#2F6B3F}
html body .ppop .btn.db-up{margin-top:8px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v135 ok')
