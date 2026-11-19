# Real Money build, step 141 (after rmv137.py): Stage 2 — the real-play funnel.
#  - Coin player (not yet real): Photo games are coins only (25 🟡). Each game screen and the Play row carry
#    "🎟️ Your first real game is on us · $1 Match Race". After the first coin game, the results lead with it.
#  - Taking it gives a free $1 ticket and switches the player to real play for good (real players only see real games).
#  - Real player: entries $0.50 / $1 / $2 / $5 / $10 (default $1). Bonus Cash is spent first, then a free ticket on $1,
#    then cash. Winnings are always cash.
#  - Straight after the first real game: "Add $5, get $10 Bonus Cash" on the results (once).
#  - Out of money: one screen with Add cash (and the Bonus offer if unused) and the free ticket (500 🟡, 1 a day).
#  - Coins menu for real players: "Free $1 game ticket · 500 🟡 · 1 a day".
#  - Winners feed on the Play tab and the games menu (simulated, labelled).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (!newbie()) I.push({ ic: '🏇', t: 'Photo games', d: 'Derby, Match Race, Grand National, Hot Streak. Play for coins or cash.', cost: 25,",
   "if (isCash()) I.push({ ic: '🎟️', t: 'Free $1 game ticket', d: 'Play any $1 Photo game for free. 1 a day.', cost: 500, src: (SEED.find(z => z.src && z.cat === 'Pets') || {}).src || '', go: () => { closeSheet(); setTimeout(() => tixClaim(true), 200); } });\n  if (!newbie()) I.push({ ic: '🏇', t: 'Photo games', d: isCash() ? 'Race real players for cash, from $0.50.' : 'Race players for coins. Your first real game is free.', cost: isCash() ? 0 : 25,")
s = s.replace("function fcNotify() {", r"""const GM_C = [{ fee: 25, coins: 1 }], GM_R = [{ fee: .5 }, { fee: 1 }, { fee: 2 }, { fee: 5 }, { fee: 10 }];
const gmTiers = () => isCash() ? GM_R : GM_C;
const todayK = () => new Date().toDateString();
function tixClaim(go2) { if (S.tixDay === todayK()) { toast('You’ve claimed today’s free ticket · back tomorrow'); return false; } if ((S.gems || 0) < 500) { toast(`${500 - Math.floor(S.gems || 0)} more 🟡 for a free ticket · vote to earn`); return false; }
  S.gems -= 500; S.cashTix = (S.cashTix || 0) + 1; S.tixDay = todayK(); save(); paintGems(); toast('🎟️ Free $1 game ticket added'); if (go2) setTimeout(gmHub, 300); return true; }
function gmFeedHTML() { const r = cpRng(Math.floor(Date.now() / 90000)), G = ['Grand National', 'Photo Derby', 'Match Race', 'Hot Streak'], M = [15, 2.38, 1.7, 2.38], F = [1, 2, 5, 10, 2, 1];
  return `<div class="gmf"><p class="gmf-h">🏆 Recent winners <small>(simulated)</small></p>${[0, 1, 2].map(k => { const gi = Math.floor(r() * 4), f = F[Math.floor(r() * F.length)], nm = QS_NAMES[Math.floor(r() * QS_NAMES.length)];
    return `<div><b>@${esc(nm)}</b><span>won <em>${money(+(f * M[gi]).toFixed(2))}</em> in the ${G[gi]}</span><small>${1 + Math.floor(r() * 9)} min ago</small></div>`; }).join('')}</div>`; }
function gmFreeRealHTML() { return !isCash() ? `<button class="gmfr" data-freereal><span>🎟️</span><b>Your first real game is on us</b><small>$1 Match Race · win $1.70 real cash</small></button>` : ''; }
function gmCardsHTML() { const real = isCash();
  return `<div class="gmr"><p class="gmr-h">Photo games · ${real ? 'real cash' : 'coin games'}</p>${real && (S.bonus || 0) > 0 ? `<p class="gmr-b">🎁 Bonus Cash <b>${money(S.bonus)}</b> · used first on entries</p>` : ''}${real && (S.cashTix || 0) > 0 ? `<p class="gmr-b">🎟️ ${S.cashTix} free $1 ticket${S.cashTix > 1 ? 's' : ''}</p>` : ''}${gmFreeRealHTML()}
    <div class="gmr-g">${Object.entries(GM).map(([k, g]) => `<button class="gmc" data-gm="${k}"><span class="gmc-ic">${g.ic}</span><b>${g.t}</b><small>${g.sub}</small></button>`).join('')}</div>${real ? gmFeedHTML() : ''}</div>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-freereal]'); if (b) { e.preventDefault(); freeRealStart(); } });
function freeRealStart() { if (isCash()) { gmHub(); return; } try { popClose(); closeFlow(); } catch (e) {} S.cashTix = (S.cashTix || 0) + 1; S.frGiven = 1; S.cashMode = 1; save(); try { paintWallet(); } catch (e) {}
  setTimeout(() => { gmOpen('match', 1); setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 80); }, 250); }
function depositOffer() { try { popClose(); } catch (e) {} setTimeout(() => openStore('Add $5 cash · get $10 Bonus Cash', () => { if (!S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + 10).toFixed(2); save(); toast('🎁 $10 Bonus Cash added · used first on entries'); } }), 200); }
function gmZero(t, mode) { const can = S.tixDay !== todayK(), g = Math.floor(S.gems || 0);
  popOpen(`<div class="pp dbx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">💵 ${money(t.fee)} game</p><h2 class="db-h">Top up to play</h2>
    <p class="db-s">You have <b>${money(S.cash || 0)}</b>${(S.bonus || 0) ? ` + ${money(S.bonus)} Bonus Cash` : ''}.</p>
    <button class="btn block cashb db-go" id="gzAdd">💵 Add cash${S.bonusGot ? '' : ' · get $10 Bonus Cash'}</button>
    <button class="btn block quiet db-up" id="gzTix">🎟️ ${can ? (g >= 500 ? 'Claim your free $1 ticket · 500 🟡' : `Free $1 ticket at 500 🟡 · you have ${g}`) : 'Free ticket claimed today · back tomorrow'}</button>
    <p class="db-eye">Vote to earn coins towards tomorrow’s free ticket.</p></div>`);
  document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
  $('#gzAdd').onclick = () => S.bonusGot ? (popClose(), setTimeout(() => openStore('Add cash to play'), 200)) : depositOffer();
  $('#gzTix').onclick = () => { if (tixClaim(false)) { popClose(); setTimeout(() => gmOpen(mode, 1), 200); } }; }
function gmPayEntry(t, mode, go) { if (t.coins) { if ((S.gems || 0) < t.fee) { toast(`You need ${t.fee} coins · vote to earn more`); return; } S.gems -= t.fee; save(); paintGems(); go(); return; }
  if (S.user && S.user.guest) { popClose(); payCash(t.fee, 'A Photo game entry', () => setTimeout(go, 250)); return; }
  if ((S.bonus || 0) >= t.fee) { S.bonus = +(S.bonus - t.fee).toFixed(2); save(); toast(`🎁 ${money(t.fee)} Bonus Cash used`); go(); return; }
  if (t.fee === 1 && (S.cashTix || 0) > 0) { S.cashTix--; save(); toast(`🎟️ Free ticket used${S.cashTix ? ` · ${S.cashTix} left` : ''}`); go(); return; }
  if ((S.cash || 0) >= t.fee) { S.cash = +((S.cash || 0) - t.fee).toFixed(2); save(); paintWallet(); go(); return; }
  gmZero(t, mode); }
function gmOpen(mode, ti0) { const g = GM[mode] || GM.derby, T = gmTiers(); let ti = Math.min(T.length - 1, ti0 == null ? (T.length > 1 ? 1 : 0) : ti0); const draw = () => { const t = T[ti], pool = g.mult.reduce((a, m) => a + m, 0) * t.fee, fee = g.n * t.fee - pool, real = !t.coins;
    const rows = g.mult.length > 3 ? [[0, '🥇 1st'], [1, '🥈 2nd'], [2, '🥉 3rd'], [3, '4th–10th']] : g.mult.map((m, k) => [k, ['🥇 1st', '🥈 2nd', '🥉 3rd'][k]]);
    const pay = real ? ((S.bonus || 0) >= t.fee ? ' · Bonus Cash' : t.fee === 1 && (S.cashTix || 0) > 0 ? ' · free ticket' : '') : '';
    popOpen(`<div class="pp dbx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">${g.ic} ${g.t}${real ? ' · real cash' : ' · coin game'}</p><h2 class="db-h">${g.sub.split(' · ')[0]}</h2>
      <p class="db-s">${g.how}</p>
      ${T.length > 1 ? `<div class="rc-st db-tier" role="group" aria-label="Entry">${T.map((x, i) => `<button data-dbt="${i}" aria-pressed="${i === ti}">${money(x.fee)}</button>`).join('')}</div>` : ''}
      <div class="db-pz gm-pz${rows.length}">${rows.map(([k, l]) => `<div><small>${l}</small><b>${gmAmt(t, gmPay(g, t, k))}</b><em>${g.mult[k]}×</em></div>`).join('')}</div>
      <p class="db-fee">${real ? `${g.n} players · ${money(+pool.toFixed(2))} prize pool · ${money(+fee.toFixed(2))} PhotoPicks fee (15%)` : 'Coin game · practise your eye'}</p>
      <button class="btn block db-go ${real ? 'cashb' : ''}" id="dbGo">${g.ic} ${real ? `Play for ${money(t.fee)}${pay}` : `Play for coins · ${t.fee} 🟡`}</button>
      ${real ? '' : gmFreeRealHTML()}
      <p class="db-eye">👁️ Your eye: <b>${Math.round(dbEye() * 100)}%</b> · you’ll play people at your level</p><p class="db-sim">Prototype: opponents are simulated</p></div>`);
    document.querySelectorAll('#coach [data-dbt]').forEach(b => b.onclick = () => { ti = +b.dataset.dbt; window.__keepScroll = 1; draw(); });
    document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#dbGo').onclick = () => { const t = T[ti]; window.__gmTi = ti; window.__gmMode = mode; gmPayEntry(t, mode, () => gmMatch(mode, t)); }; };
  draw(); }
function gmEnd(mode, t, R, ok, nPicks) { const g = GM[mode], ord = R.slice().sort((a, b) => b.sc - a.sc || a.tm - b.tm), me = R[0], pl = ord.indexOf(me) + 1, prize = gmPay(g, t, pl - 1), T = t.coins ? GM_C : GM_R;
  S.eyeN = (S.eyeN || 0) + nPicks; S.eyeOk = (S.eyeOk || 0) + ok; S.gmN = (S.gmN || 0) + 1; const firstReal = !t.coins && !S.depShown; if (!t.coins) S.realN = (S.realN || 0) + 1;
  if (prize) { if (t.coins) S.gems = (S.gems || 0) + prize; else S.cash = +((S.cash || 0) + prize).toFixed(2); } save();
  const ti = Math.min(T.length - 1, window.__gmTi == null ? 0 : window.__gmTi), up = Math.min(T.length - 1, ti + 1), paid = g.mult.length, unit = g.streak ? 'in a row' : 'pts';
  const show = ord.slice(0, Math.min(ord.length, g.n > 4 ? 5 : 4)); if (!show.includes(me)) show.push(me);
  const gap = pl > paid ? ord[paid - 1].sc - me.sc : 0;
  const dep = firstReal && !S.bonusGot ? `<button class="gmdep" id="gmDep"><span>🎁</span><b>Add $5, get $10 Bonus Cash</b><small>Bonus Cash is spent on entries first · winnings are real cash</small></button>` : '';
  const fr = t.coins && !isCash() ? gmFreeRealHTML() : '';
  if (firstReal) { S.depShown = 1; save(); }
  popOpen(`<div class="pp dbx dbe ${prize ? 'won' : ''}"><p class="pp-k">${g.ic} ${g.t} · ${gmAmt(t, t.fee)}</p><h2 class="db-h">${pl === 1 ? (g.n === 2 ? 'You won the match!' : `You won the ${g.t}!`) : prize ? `${ppOrd(pl)} place, paid!` : `You finished ${ppOrd(pl)}${g.n > 4 ? ` of ${g.n}` : ''}`}</h2>
    ${prize ? `<div class="rv-won"><span>${t.coins ? 'You won' : 'Cash won'}</span><b>${gmAmt(t, prize)}</b></div>` : `<p class="db-s">${gap <= (g.streak ? 2 : 15) ? `Just <b>${gap || 1} ${g.streak ? (gap === 1 ? 'pick' : 'picks') : 'points'}</b> off the paid places. One more?` : `Top ${paid} get paid. One more?`}</p>`}
    ${dep}${fr}
    <div class="db-res">${show.map(x => { const k = ord.indexOf(x); return `<div class="${x.me ? 'me' : ''}"><em>${['🥇', '🥈', '🥉'][k] || ppOrd(k + 1)}</em><b>${x.me ? 'You' : '@' + esc(x.h)}</b><span>${x.sc} ${unit}</span><i>${gmPay(g, t, k) ? gmAmt(t, gmPay(g, t, k)) : ''}</i></div>`; }).join('')}</div>
    <p class="db-eye">You matched the crowd on <b>${ok} of ${nPicks}</b> · 👁️ Eye now ${Math.round(dbEye() * 100)}%</p>
    <button class="btn block db-go ${t.coins ? '' : 'cashb'}" id="dbRe">🔁 Rematch · ${gmAmt(t, t.fee)}</button>${up !== ti ? `<button class="btn block quiet db-up" id="dbUp">Step up · ${gmAmt(T[up], T[up].fee)}</button>` : ''}
    <div style="text-align:center"><button class="link pc-later" id="dbOther">Other games</button> · <button class="link pc-later" id="dbDone">Done</button></div><p class="db-sim">Prototype: opponents are simulated</p></div>`);
  if (prize) setTimeout(() => { try { t.coins ? (paintGems(), gemExplosion(prize, { label: g.t })) : (paintWallet(), cashExplosion(prize, { label: g.t })); } catch (e) {} }, 350); else { try { paintGems(); paintWallet(); } catch (e) {} }
  if (pl === 1) setTimeout(() => { try { rvConfetti(document.querySelector('.dbe'), g.n > 4 ? 90 : 50); } catch (e) {} }, 200);
  const sameMode = !!t.coins === !isCash();
  $('#dbRe').onclick = () => { popClose(); setTimeout(() => { if (!sameMode) { gmHub(); return; } gmOpen(mode, ti); setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 60); }, 200); };
  if ($('#dbUp')) $('#dbUp').onclick = () => { popClose(); setTimeout(() => sameMode ? gmOpen(mode, up) : gmHub(), 200); };
  if ($('#gmDep')) $('#gmDep').onclick = depositOffer;
  $('#dbOther').onclick = () => { popClose(); setTimeout(gmHub, 200); }; $('#dbDone').onclick = () => popClose(); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.gmfr{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;margin:0 0 10px;padding:12px 14px;border:0;border-radius:14px;background:linear-gradient(135deg,#2F6B3F,#3E8A52);color:#fff;text-align:left;cursor:pointer;font:inherit;box-shadow:0 5px 14px rgba(47,107,63,.3),inset 0 0 0 1.5px #D9AE4F}
.gmfr span{font-size:1.3rem}.gmfr b{font:800 1.05rem Fraunces,Georgia,serif;color:#fff}.gmfr small{font-size:.8rem;opacity:.92}
html body .ppop .gmfr{margin-top:10px}
.gmdep{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;margin:6px 0 10px;padding:12px 14px;border:0;border-radius:14px;background:#F1F6EC;box-shadow:inset 0 0 0 2px #2F6B3F;text-align:left;cursor:pointer;font:inherit}
.gmdep span{font-size:1.3rem}.gmdep b{font:800 1.05rem Fraunces,Georgia,serif;color:#2F6B3F}.gmdep small{font-size:.78rem;color:#3D5A44}
.gmr-b{margin:0 0 8px;font-size:.84rem;color:#14213D}.gmr-b b{color:#2F6B3F}
.gmf{margin:12px 0 0;padding:10px 12px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.gmf-h{margin:0 0 6px;font-weight:900;font-size:.8rem;color:#14213D}.gmf-h small{font-weight:600;opacity:.6}
.gmf div{display:flex;gap:6px;align-items:baseline;font-size:.82rem;padding:3px 0;border-top:1px solid #F1E9DB}.gmf div:first-of-type{border-top:0}.gmf div b{color:#14213D}.gmf div span{flex:1}.gmf div em{font-style:normal;font-weight:900;color:#2F6B3F}.gmf div small{opacity:.6;white-space:nowrap}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v138 ok')
# pass 2: the add-cash screen matches the offer; coins-menu rows without a coin cost say "Play ›"
s = open(d + 'yofi-real.html').read()
RA("const w = !S.paidCash, cash = w ? 10 : 5, coins = w ? 25 : 10; return { ic: '💵', title: title || 'Add cash to play', tag: w ? 'Welcome offer' : 'Most popular', big: w ? `$${cash} <small class=\"ro-plus\">+ $5 free</small>` : `$${cash}`, sub: w ? 'cash to play · plus $5 free to play with' : 'cash to play', usd: cash,\n      buy: () => checkout(`$${cash} cash`, cash, () => applyOffer(cash + (w ? 5 : 0), 0, w ? 'Welcome offer · $5 free' : '$5 pack', onBuy)), free: 'Not now', freeFn: () => {} };",
   "const w = !S.paidCash && !S.bonusGot, cash = w ? 5 : 10, coins = w ? 25 : 10; return { ic: '💵', title: title || 'Add cash to play', tag: w ? 'Welcome offer' : 'Most popular', big: w ? `$${cash} <small class=\"ro-plus\">+ $10 Bonus Cash</small>` : `$${cash}`, sub: w ? 'cash to play · plus $10 Bonus Cash for entries' : 'cash to play', usd: cash,\n      buy: () => checkout(`$${cash} cash`, cash, () => applyOffer(cash, 0, w ? 'Welcome offer · $10 Bonus Cash' : '$10 pack', () => { if (w && !S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + 10).toFixed(2); save(); toast('🎁 $10 Bonus Cash added · used first on entries'); } if (onBuy) onBuy(); })), free: 'Not now', freeFn: () => {} };")
RA("<em class=\"${S.gems < x.cost ? 'need' : ''}\">${x.cost} 🟡</em></button>`).join('')", "<em class=\"${x.cost && S.gems < x.cost ? 'need' : ''}\">${x.cost ? x.cost + ' 🟡' : 'Play ›'}</em></button>`).join('')")
RA("<small>Play a $1 challenge or tournament free. Win real cash.</small>", "<small>Play any $1 Photo game free. Win real cash.</small>")
open(d + 'yofi-real.html', 'w').write(s); print('rm v138 pass2 ok')
# pass 3: the coins-menu free ticket row opens Photo games
s = open(d + 'yofi-real.html').read()
RA("$('#ugTix').onclick = () => { closeSheet();", "$('#ugTix').onclick = () => { closeSheet(); setTimeout(gmHub, 200); return;")
open(d + 'yofi-real.html', 'w').write(s); print('rm v138 pass3 ok')
# pass 4: the free-real card keeps its green look inside pop-ups; "Top 1 get paid" wording; feed left-aligned
s = open(d + 'yofi-real.html').read()
RA("`Top ${paid} get paid. One more?`}</p>`}\n    ${dep}${fr}", "(paid === 1 ? 'Only 1st place gets paid. One more?' : `Top ${paid} get paid. One more?`)}</p>`}\n    ${dep}${fr}")
s = s.replace('</style>', """html body .gmfr,html body .ppop .gmfr{background:linear-gradient(135deg,#2F6B3F,#3E8A52)!important;color:#fff!important;border:0!important;box-shadow:0 5px 14px rgba(47,107,63,.3),inset 0 0 0 1.5px #D9AE4F!important;text-align:left!important}
html body .gmfr b{color:#fff!important;-webkit-text-fill-color:#fff}html body .gmfr small{color:#EAF4EC!important;-webkit-text-fill-color:#EAF4EC}
html body .gmdep,html body .ppop .gmdep{background:#F1F6EC!important;box-shadow:inset 0 0 0 2px #2F6B3F!important;border:0!important;text-align:left!important}
.gmf div{text-align:left}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v138 pass4 ok')
# pass 5: real-money buttons in Photo games are green (house style), coin buttons stay navy
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .ppop .btn.db-go.cashb{background:#2F6B3F!important;color:#fff!important;-webkit-text-fill-color:#fff}
html body .ppop .dbe .btn.db-up{background:#fff!important;color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F;box-shadow:inset 0 0 0 2px #2F6B3F!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v138 pass5 ok')
