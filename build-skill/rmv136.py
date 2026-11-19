# Real Money build, step 139 (after rmv135.py): three more skill games on the Derby engine.
#  All use the same photo pairs (same category, crowd result by photo appeal), coins or $1/$2/$5/$10 entry, a 15% fee
#  shown on entry, prizes as fixed multiples of the entry, Rematch / Step up, simulated opponents (labelled).
#  - ⚔️ Match Race: 1 v 1, same 10 pairs, winner gets 1.7×.
#  - 🏆 Grand National: 50 riders, same 10 pairs. 1st 15×, 2nd 8×, 3rd 5.5×, 4th–10th 2×. Race shows you + the
#    leaders and your position ("12th of 50").
#  - 🔥 Hot Streak: 4 players, same pairs (up to 25). Keep picking the crowd's choice; one wrong ends your run.
#    Opponents' streaks are shown as targets ("Beat @coco.pup's 7"). Longest run wins; top 2 paid (2.38× / 1.02×).
#  - Photo Derby unchanged in rules (1st 2.38×, 2nd 1.02×).
#  Entry points: a games row on the Finals tab (replaces the single Derby card) and "Photo games" in the coins menu.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("${derbyCardHTML()}", "${gmCardsHTML()}")
RA("if (!newbie()) I.push({ ic: '🏇', t: 'Photo Derby', d: 'Race 3 players on the same 10 photo pairs. Play for coins or cash.', cost: 25,",
   "if (!newbie()) I.push({ ic: '🏇', t: 'Photo games', d: 'Derby, Match Race, Grand National, Hot Streak. Play for coins or cash.', cost: 25,")
RA("go: () => { closeSheet(); setTimeout(derbyOpen, 250); } });", "go: () => { closeSheet(); setTimeout(gmHub, 250); } });")
s = s.replace("function fcNotify() {", r"""const GM = {
  derby: { n: 4, ic: '🏇', t: 'Photo Derby', sub: 'Race 3 players · top 2 paid', how: 'All 4 riders get the <b>same 10 photo pairs</b>. Pick the photo the crowd chose. Right and fast moves your horse.', mult: [2.38, 1.02] },
  match: { n: 2, ic: '⚔️', t: 'Match Race', sub: 'You vs 1 player · win 1.7×', how: 'You and 1 player get the <b>same 10 photo pairs</b>. Most points wins: right answers, plus a bonus for speed.', mult: [1.7] },
  gn: { n: 50, ic: '🏆', t: 'Grand National', sub: '50 riders · win 15× · top 10 paid', how: 'A big field of 50 on the <b>same 10 photo pairs</b>. Finish in the top 10 to get paid. Win it for 15× your entry.', mult: [15, 8, 5.5, 2, 2, 2, 2, 2, 2, 2] },
  streak: { n: 4, ic: '🔥', t: 'Hot Streak', sub: 'Longest run wins · top 2 paid', how: 'Everyone gets the <b>same pairs</b>. Keep picking the crowd’s choice. <b>One wrong ends your run.</b> Longest run wins (max 25).', mult: [2.38, 1.02], streak: 1 } };
const GM_FEES = [{ fee: 25, coins: 1 }, { fee: 1 }, { fee: 2 }, { fee: 5 }, { fee: 10 }];
const gmPay = (g, t, k) => { const m = g.mult[k]; if (!m) return 0; return t.coins ? Math.round(m * t.fee) : +(m * t.fee).toFixed(2); };
const gmAmt = (t, v) => t.coins ? `${v} 🟡` : money(v);
function gmCardsHTML() { return `<div class="gmr"><p class="gmr-h">Photo games · race real players</p><div class="gmr-g">${Object.entries(GM).map(([k, g]) => `<button class="gmc" data-gm="${k}"><span class="gmc-ic">${g.ic}</span><b>${g.t}</b><small>${g.sub}</small></button>`).join('')}</div></div>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-gm]'); if (b) { e.preventDefault(); popClose(); setTimeout(() => gmOpen(b.dataset.gm), 120); } });
function gmHub() { popOpen(`<div class="pp gmx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🎮 Photo games</p><h2 class="db-h">Race real players</h2><p class="db-s">Same photo pairs for everyone. Read the crowd better, win.</p>${gmCardsHTML()}<p class="db-sim">Prototype: opponents are simulated</p></div>`);
  document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function derbyOpen(ti0) { gmOpen('derby', ti0); }
function gmOpen(mode, ti0) { const g = GM[mode] || GM.derby; let ti = ti0 == null ? 2 : ti0; const draw = () => { const t = GM_FEES[ti], pool = g.mult.reduce((a, m) => a + m, 0) * t.fee, fee = g.n * t.fee - pool;
    const rows = g.mult.length > 3 ? [[0, '🥇 1st'], [1, '🥈 2nd'], [2, '🥉 3rd'], [3, '4th–10th']] : g.mult.map((m, k) => [k, ['🥇 1st', '🥈 2nd', '🥉 3rd'][k]]);
    popOpen(`<div class="pp dbx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">${g.ic} ${g.t}</p><h2 class="db-h">${g.sub.split(' · ')[0]}</h2>
      <p class="db-s">${g.how}</p>
      <div class="rc-st db-tier" role="group" aria-label="Entry">${GM_FEES.map((x, i) => `<button data-dbt="${i}" aria-pressed="${i === ti}">${x.coins ? `${x.fee} 🟡` : '$' + x.fee}</button>`).join('')}</div>
      <div class="db-pz gm-pz${rows.length}">${rows.map(([k, l]) => `<div><small>${l}</small><b>${gmAmt(t, gmPay(g, t, k))}</b><em>${g.mult[k]}×</em></div>`).join('')}</div>
      <p class="db-fee">${t.coins ? 'Coin game · practise your eye for free' : `${g.n} players · ${money(+pool.toFixed(2))} prize pool · ${money(+fee.toFixed(2))} PhotoPicks fee (15%)`}</p>
      <button class="btn block db-go ${t.coins ? '' : 'cashb'}" id="dbGo">${g.ic} ${t.coins ? `Play for coins · ${t.fee} 🟡` : `Play for ${money(t.fee)}`}</button>
      <p class="db-eye">👁️ Your eye: <b>${Math.round(dbEye() * 100)}%</b> · you’ll play people at your level</p><p class="db-sim">Prototype: opponents are simulated</p></div>`);
    document.querySelectorAll('#coach [data-dbt]').forEach(b => b.onclick = () => { ti = +b.dataset.dbt; window.__keepScroll = 1; draw(); });
    document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#dbGo').onclick = () => { const t = GM_FEES[ti]; window.__gmTi = ti; window.__gmMode = mode;
      if (t.coins) { if ((S.gems || 0) < t.fee) { toast(`You need ${t.fee} coins · vote to earn more`); return; } S.gems -= t.fee; save(); paintGems(); gmMatch(mode, t); }
      else { popClose(); payCash(t.fee, `A ${g.t} entry`, () => setTimeout(() => gmMatch(mode, t), 250)); } }; };
  draw(); }
function gmOpps(k, eye, r) { const col = ['#C0392B', '#2E86C1', '#8E44AD', '#16A085', '#D35400', '#7F8C8D'], nm = ppShuffle(QS_NAMES.slice(), r);
  return Array.from({ length: k }, (_, i) => ({ h: i < nm.length ? nm[i] : nm[i % nm.length].replace(/[._]?\w*$/, '') + (10 + Math.floor(r() * 89)), acc: Math.max(.45, Math.min(.9, eye + (r() - .5) * .22)), c: col[i % col.length] })); }
function gmMatch(mode, t) { const g = GM[mode], seed = Date.now() % 1e7, r = cpRng(seed), eye = dbEye(), O = gmOpps(g.n - 1, eye, r), me = ((S.user && S.user.h) || 'you');
  const big = g.n > 4, done = () => setTimeout(() => (g.streak ? gmStreak : gmRace)(mode, t, O, seed), 1100);
  popOpen(`<div class="pp dbx"><p class="pp-k">${g.ic} ${g.t} · ${gmAmt(t, t.fee)}</p><h2 class="db-h" id="dbMh">Finding players at your level…</h2>
    ${big ? `<div class="gm-cnt"><b id="gmCn">1</b><span>of ${g.n} riders</span><div class="nfx-bar"><i id="gmCb" style="width:2%"></i></div></div>` : `<div class="db-lobby gm-l${g.n}"><div class="db-rd in me"><i>${esc(me[0].toUpperCase())}</i><b>You</b><small>Eye ${Math.round(eye * 100)}%</small></div>${O.map((o, i) => `<div class="db-rd" id="dbR${i}"><i>?</i><b>Searching…</b><small>&nbsp;</small></div>`).join('')}</div>`}
    <p class="db-sim">Prototype: opponents are simulated</p></div>`);
  if (big) { let n = 1; const iv = setInterval(() => { n = Math.min(g.n, n + 3 + Math.floor(Math.random() * 5)); const a = document.getElementById('gmCn'), b = document.getElementById('gmCb'); if (!a) { clearInterval(iv); return; } a.textContent = n; b.style.width = (n / g.n * 100) + '%'; if (n >= g.n) { clearInterval(iv); const h = document.getElementById('dbMh'); if (h) h.textContent = 'Field full · gates opening…'; done(); } }, 160); return; }
  O.forEach((o, i) => setTimeout(() => { const el = document.getElementById('dbR' + i); if (!el) return; el.classList.add('in'); el.innerHTML = `<i style="background:${o.c}">${esc(o.h[0].toUpperCase())}</i><b>@${esc(o.h)}</b><small>Eye ${Math.round(o.acc * 100)}%</small>`; }, 700 + i * 650));
  setTimeout(() => { const h = document.getElementById('dbMh'); if (h) h.textContent = `${O.length === 1 ? 'Opponent' : O.length + ' players'} found · gates opening…`; done(); }, 700 + O.length * 650); }
function gmRace(mode, t, O, seed) { const g = GM[mode], r = cpRng(seed * 7 + 11), pairs = cpPairs(DB_N, seed * 7 + 11, true), me = { h: 'You', c: '#D9AE4F', sc: 0, tm: 0, ok: 0, me: 1 }, big = g.n > 4;
  O.forEach(o => { o.sc = 0; o.tm = 0; o.res = pairs.map(() => { const okk = r() < o.acc, tm = 1.4 + r() * 3.1; return { okk, tm, pts: okk ? 10 + Math.max(0, 5 - Math.floor(tm)) : 0 }; }); });
  const R = [me].concat(O), MAX = DB_N * 15;
  const lanes = () => { const L = big ? (() => { const s2 = R.slice().sort((a, b) => b.sc - a.sc || a.tm - b.tm), top = s2.slice(0, 4); if (!top.includes(me)) top.push(me); return top.map(x => [x, s2.indexOf(x) + 1]); })() : R.map(x => [x, 0]);
    return L.map(([x, rk], k) => `<div class="db-ln ${x.me ? 'me' : ''}"><span class="db-nm">${rk ? `<em>${rk}</em> ` : ''}${x.me ? 'You' : '@' + esc(x.h)}</span><span class="db-rail"><i class="db-hs" id="dbH${big ? 'b' + k : R.indexOf(x)}" style="left:${Math.min(86, x.sc / MAX * 86 * 1.25)}%"><u style="background:${x.c}"></u>🏇</i></span><b class="db-sc">${x.sc}</b></div>`).join(''); };
  popOpen(`<div class="pp dbx dbr"><div class="db-top"><b id="dbQ">Pair 1 of ${DB_N}</b>${big ? `<span id="gmPos">— of ${g.n}</span>` : ''}<span id="dbClk">0.0s</span></div>
    <div class="db-trk" id="dbTrk">${lanes()}<i class="db-fin"></i></div>
    <h3 class="db-qh">Which photo did the crowd pick?</h3><div class="db-pair" id="dbPair"></div><p class="db-fb" id="dbFb">Tap a photo · faster = more points</p></div>`);
  let i = 0, tq = 0, lock = false; const clk = setInterval(() => { const c = document.getElementById('dbClk'); if (!c) { clearInterval(clk); return; } c.textContent = `${((Date.now() - tq) / 1000).toFixed(1)}s`; }, 100);
  const paint = () => { if (big) { const T = document.getElementById('dbTrk'); if (T) T.innerHTML = lanes() + '<i class="db-fin"></i>'; const s2 = R.slice().sort((a, b) => b.sc - a.sc || a.tm - b.tm), P = document.getElementById('gmPos'); if (P) P.textContent = `${ppOrd(s2.indexOf(me) + 1)} of ${g.n}`; return; }
    R.forEach((x, k) => { const h = document.getElementById('dbH' + k); if (h) { h.style.left = `${Math.min(86, x.sc / MAX * 86 * 1.25)}%`; const sc = h.closest('.db-ln').querySelector('.db-sc'); if (sc) sc.textContent = x.sc; } }); };
  const show = () => { const p = pairs[i]; lock = false; tq = Date.now(); $('#dbQ').textContent = `Pair ${i + 1} of ${DB_N}`;
    $('#dbPair').innerHTML = ['a', 'b'].map(k => `<button class="db-ph" data-dp="${k}"><img src="${p[k].src}" alt=""><span class="db-pc"></span></button>`).join('');
    document.querySelectorAll('#dbPair [data-dp]').forEach(b => b.onclick = () => { if (lock) return; lock = true; const tm = (Date.now() - tq) / 1000, okk = (b.dataset.dp === 'a') === (p.pa >= 50), pts = okk ? 10 + Math.max(0, 5 - Math.floor(tm)) : 0;
      me.sc += pts; me.tm += tm; if (okk) me.ok++; O.forEach(o => { o.sc += o.res[i].pts; o.tm += o.res[i].tm; });
      document.querySelectorAll('#dbPair [data-dp]').forEach(x => { const a = x.dataset.dp === 'a', pc = a ? p.pa : 100 - p.pa; x.classList.add(pc >= 50 ? 'crowd' : 'not'); x.querySelector('.db-pc').textContent = pc + '%'; });
      b.classList.add(okk ? 'ok' : 'bad'); const F = $('#dbFb'); F.className = 'db-fb ' + (okk ? 'ok' : 'bad'); F.innerHTML = okk ? `✓ Crowd pick · <b>+${pts}</b>${pts > 10 ? ` (speed +${pts - 10})` : ''}` : '✕ The crowd picked the other photo';
      try { navigator.vibrate && navigator.vibrate(okk ? 12 : [25, 30, 25]); } catch (e) {} paint(); i++;
      setTimeout(() => { if (i < DB_N) { F.className = 'db-fb'; F.textContent = 'Tap a photo · faster = more points'; show(); } else { clearInterval(clk); gmEnd(mode, t, R, me.ok, DB_N); } }, 1100); }); };
  show(); }
function gmStreak(mode, t, O, seed) { const g = GM[mode], r = cpRng(seed * 5 + 3), MAXS = 25, pairs = cpPairs(MAXS, seed * 5 + 3, true), me = { h: 'You', c: '#D9AE4F', sc: 0, tm: 0, ok: 0, me: 1 };
  O.forEach(o => { let n = 0; while (n < MAXS && r() < o.acc) n++; o.sc = n; o.tm = n * (1.6 + r() * 2.4); });
  const board = () => O.slice().sort((a, b) => b.sc - a.sc).map(o => `<div class="${me.sc > o.sc ? 'pass' : ''}"><i style="background:${o.c}">${esc(o.h[0].toUpperCase())}</i><b>@${esc(o.h)}</b><em>🔥 ${o.sc}</em>${me.sc > o.sc ? '<u>passed ✓</u>' : ''}</div>`).join('');
  const target = () => { const nx = O.filter(o => o.sc >= me.sc).sort((a, b) => a.sc - b.sc)[0]; return nx ? `Beat @${esc(nx.h)}’s <b>${nx.sc}</b> · ${nx.sc - me.sc + 1} more` : '<b>You’re in front!</b> Keep going for the top score'; };
  popOpen(`<div class="pp dbx dbr hsx"><div class="db-top"><b>🔥 Hot Streak · ${gmAmt(t, t.fee)}</b><span id="dbClk">0.0s</span></div>
    <div class="hs-big"><b id="hsN">0</b><span>in a row</span></div><p class="hs-tg" id="hsTg">${target()}</p><div class="hs-bd" id="hsBd">${board()}</div>
    <h3 class="db-qh">Which photo did the crowd pick?</h3><div class="db-pair" id="dbPair"></div><p class="db-fb" id="dbFb">One wrong pick ends your run</p></div>`);
  let i = 0, tq = 0, lock = false; const clk = setInterval(() => { const c = document.getElementById('dbClk'); if (!c) { clearInterval(clk); return; } c.textContent = `${((Date.now() - tq) / 1000).toFixed(1)}s`; }, 100);
  const show = () => { const p = pairs[i]; lock = false; tq = Date.now();
    $('#dbPair').innerHTML = ['a', 'b'].map(k => `<button class="db-ph" data-dp="${k}"><img src="${p[k].src}" alt=""><span class="db-pc"></span></button>`).join('');
    document.querySelectorAll('#dbPair [data-dp]').forEach(b => b.onclick = () => { if (lock) return; lock = true; const tm = (Date.now() - tq) / 1000, okk = (b.dataset.dp === 'a') === (p.pa >= 50), before = O.filter(o => me.sc > o.sc).length;
      document.querySelectorAll('#dbPair [data-dp]').forEach(x => { const a = x.dataset.dp === 'a', pc = a ? p.pa : 100 - p.pa; x.classList.add(pc >= 50 ? 'crowd' : 'not'); x.querySelector('.db-pc').textContent = pc + '%'; });
      b.classList.add(okk ? 'ok' : 'bad'); const F = $('#dbFb'); i++;
      if (okk) { me.sc++; me.ok++; me.tm += tm; const N = $('#hsN'); N.textContent = me.sc; N.classList.remove('bump'); void N.offsetWidth; N.classList.add('bump'); const passed = O.filter(o => me.sc > o.sc).length > before;
        F.className = 'db-fb ok'; F.innerHTML = passed ? `🔥 You passed ${O.filter(o => me.sc > o.sc).sort((a, b) => b.sc - a.sc)[0] ? '@' + esc(O.filter(o => me.sc > o.sc).sort((a, b) => b.sc - a.sc)[0].h) : 'a player'}!` : '✓ Crowd pick · keep going';
        $('#hsTg').innerHTML = target(); $('#hsBd').innerHTML = board(); try { navigator.vibrate && navigator.vibrate(passed ? [15, 40, 15] : 10); } catch (e) {}
        setTimeout(() => { if (i < MAXS) { F.className = 'db-fb'; F.textContent = 'One wrong pick ends your run'; show(); } else { clearInterval(clk); gmEnd(mode, t, [me].concat(O), me.ok, i); } }, 900); }
      else { F.className = 'db-fb bad'; F.innerHTML = `✕ The crowd picked the other photo · <b>run over at ${me.sc}</b>`; try { navigator.vibrate && navigator.vibrate([30, 40, 30]); } catch (e) {} clearInterval(clk); setTimeout(() => gmEnd(mode, t, [me].concat(O), me.ok, i), 1400); } }); };
  show(); }
function gmEnd(mode, t, R, ok, nPicks) { const g = GM[mode], ord = R.slice().sort((a, b) => b.sc - a.sc || a.tm - b.tm), me = R[0], pl = ord.indexOf(me) + 1, prize = gmPay(g, t, pl - 1);
  S.eyeN = (S.eyeN || 0) + nPicks; S.eyeOk = (S.eyeOk || 0) + ok;
  if (prize) { if (t.coins) S.gems = (S.gems || 0) + prize; else S.cash = +((S.cash || 0) + prize).toFixed(2); } save();
  const ti = window.__gmTi == null ? 2 : window.__gmTi, up = Math.min(GM_FEES.length - 1, ti + 1), paid = g.mult.length, unit = g.streak ? 'in a row' : 'pts';
  const show = ord.slice(0, Math.min(ord.length, g.n > 4 ? 5 : 4)); if (!show.includes(me)) show.push(me);
  const gap = pl > paid ? ord[paid - 1].sc - me.sc : 0;
  popOpen(`<div class="pp dbx dbe ${prize ? 'won' : ''}"><p class="pp-k">${g.ic} ${g.t} · ${gmAmt(t, t.fee)}</p><h2 class="db-h">${pl === 1 ? (g.n === 2 ? 'You won the match!' : `You won the ${g.t}!`) : prize ? `${ppOrd(pl)} place, paid!` : `You finished ${ppOrd(pl)}${g.n > 4 ? ` of ${g.n}` : ''}`}</h2>
    ${prize ? `<div class="rv-won"><span>${t.coins ? 'You won' : 'Cash won'}</span><b>${gmAmt(t, prize)}</b></div>` : `<p class="db-s">${gap <= (g.streak ? 2 : 15) ? `Just <b>${gap || 1} ${g.streak ? (gap === 1 ? 'pick' : 'picks') : 'points'}</b> off the paid places. One more?` : `Top ${paid} get paid. One more?`}</p>`}
    <div class="db-res">${show.map(x => { const k = ord.indexOf(x); return `<div class="${x.me ? 'me' : ''}"><em>${['🥇', '🥈', '🥉'][k] || ppOrd(k + 1)}</em><b>${x.me ? 'You' : '@' + esc(x.h)}</b><span>${x.sc} ${unit}</span><i>${gmPay(g, t, k) ? gmAmt(t, gmPay(g, t, k)) : ''}</i></div>`; }).join('')}</div>
    <p class="db-eye">You matched the crowd on <b>${ok} of ${nPicks}</b> · 👁️ Eye now ${Math.round(dbEye() * 100)}%</p>
    <button class="btn block db-go ${t.coins ? '' : 'cashb'}" id="dbRe">🔁 Rematch · ${gmAmt(t, t.fee)}</button>${up !== ti ? `<button class="btn block quiet db-up" id="dbUp">Step up · ${gmAmt(GM_FEES[up], GM_FEES[up].fee)}</button>` : ''}
    <div style="text-align:center"><button class="link pc-later" id="dbOther">Other games</button> · <button class="link pc-later" id="dbDone">Done</button></div><p class="db-sim">Prototype: opponents are simulated</p></div>`);
  if (prize) setTimeout(() => { try { t.coins ? (paintGems(), gemExplosion(prize, { label: g.t })) : (paintWallet(), cashExplosion(prize, { label: g.t })); } catch (e) {} }, 350); else { try { paintGems(); paintWallet(); } catch (e) {} }
  if (pl === 1) setTimeout(() => { try { rvConfetti(document.querySelector('.dbe'), g.n > 4 ? 90 : 50); } catch (e) {} }, 200);
  $('#dbRe').onclick = () => { popClose(); setTimeout(() => { gmOpen(mode, ti); setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 60); }, 200); };
  if ($('#dbUp')) $('#dbUp').onclick = () => { popClose(); setTimeout(() => gmOpen(mode, up), 200); };
  $('#dbOther').onclick = () => { popClose(); setTimeout(gmHub, 200); }; $('#dbDone').onclick = () => popClose(); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.gmr{margin:10px 0 14px}.gmr-h{margin:0 0 6px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;font-size:.74rem;color:#14213D}
.gmr-g{display:grid;grid-template-columns:1fr 1fr;gap:8px}.gmc{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:12px;border:0;border-radius:16px;background:linear-gradient(135deg,#14213D,#1E3A6E);color:#fff;text-align:left;cursor:pointer;font:inherit;box-shadow:0 5px 14px rgba(20,33,61,.22),inset 0 0 0 1.5px #D9AE4F}
.gmc-ic{font-size:1.6rem}.gmc b{font:800 1.02rem Fraunces,Georgia,serif;color:#F3D98B;-webkit-text-fill-color:#F3D98B}.gmc small{font-size:.74rem;line-height:1.3;opacity:.88;color:#fff}
.db-pz em{display:block;font-style:normal;font-size:.7rem;font-weight:800;color:#9A6B12}.gm-pz4{grid-template-columns:repeat(4,1fr)!important}.gm-pz1{grid-template-columns:1fr!important}
.gm-l2{grid-template-columns:1fr 1fr!important}
.gm-cnt{margin:14px 0;text-align:center}.gm-cnt b{font:900 3rem/1 Fraunces,Georgia,serif;color:#14213D}.gm-cnt span{display:block;font-weight:800;color:#5B4A3F;margin:2px 0 10px}
.db-nm em{font-style:normal;color:#F3D98B;font-weight:900}
.hs-big{text-align:center;margin:4px 0 0}.hs-big b{display:inline-block;font:900 3.4rem/1 Fraunces,Georgia,serif;color:#E07B24}.hs-big b.bump{animation:stkBump .35s ease-out}.hs-big span{display:block;font-weight:800;color:#5B4A3F;font-size:.85rem}
.hs-tg{text-align:center;margin:4px 0 8px;font-size:.9rem;color:#14213D}.hs-bd{display:grid;gap:4px}.hs-bd div{display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:10px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;font-size:.84rem}
.hs-bd i{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;color:#fff;font-style:normal;font-weight:900;font-size:.75rem;flex:none}.hs-bd b{flex:1}.hs-bd em{font-style:normal;font-weight:900}.hs-bd u{text-decoration:none;font-weight:900;color:#2F6B3F;font-size:.75rem}.hs-bd div.pass{opacity:.6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v136 ok')
# pass 2: fixes from the play-through
#  - Finals-tab game cards kept the navy look (old button styles turned them cream).
#  - Big-field opponent names: "@79" → "@coco33" (base name + number).
#  - Hot Streak: pairs with a clearer crowd favourite and opponents scaled to them, so good judges build runs of 5–10.
s = open(d + 'yofi-real.html').read()
RA("h: i < nm.length ? nm[i] : nm[i % nm.length].replace(/[._]?\\w*$/, '') + (10 + Math.floor(r() * 89))",
   "h: i < nm.length ? nm[i] : nm[i % nm.length].split(/[._]/)[0] + (10 + Math.floor(r() * 89))")
RA("const g = GM[mode], r = cpRng(seed * 5 + 3), MAXS = 25, pairs = cpPairs(MAXS, seed * 5 + 3, true),",
   "const g = GM[mode], r = cpRng(seed * 5 + 3), MAXS = 25, pairs = hsPairs(MAXS, seed * 5 + 3),")
RA("O.forEach(o => { let n = 0; while (n < MAXS && r() < o.acc) n++;", "O.forEach(o => { let n = 0; const p = Math.min(.93, o.acc + .17); while (n < MAXS && r() < p) n++;")
s = s.replace("function fcNotify() {", r"""function hsPairs(n, seed) { const r = cpRng(seed), P = SEED.filter(x => x.src && finCatOf(x)), out = [];
  for (let i = 0; i < n; i++) { const a = P[Math.floor(r() * P.length)], same = P.filter(x => x !== a && finCatOf(x) === finCatOf(a)), b = same[Math.floor(r() * same.length)] || P.find(x => x !== a);
    let share = 50 + (cpAppeal(a) - cpAppeal(b)) * 70 + (r() - .5) * 18; if (Math.abs(share - 50) < 8) share = share < 50 ? 40 : 60;
    out.push({ a, b, pa: Math.round(Math.max(18, Math.min(82, share))) }); } return out; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .gmr .gmc,html body .ppop .gmc{background:linear-gradient(135deg,#14213D,#1E3A6E)!important;color:#fff!important;border:0!important;box-shadow:0 5px 14px rgba(20,33,61,.22),inset 0 0 0 1.5px #D9AE4F!important}
html body .gmc b{color:#F3D98B!important}html body .gmc small{color:#E6ECF7!important;-webkit-text-fill-color:#E6ECF7}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v136 pass2 ok')
