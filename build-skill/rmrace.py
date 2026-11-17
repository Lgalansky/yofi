# Real Money build, step 3 (after realmoney.py): the horse-racing game.
#  - Hourly race: 9 runners, pick the top 3. Cash bets $1-$20, payouts by stake (top 10% share the pool).
#    Perfect 1-2-3 shares a jackpot. Coin players get one free $1 bet per race for 500 coins (we pay only if it wins).
#  - Qualification gates every 10 votes: 5 photos, pick the top 3, free (coins), upsell "Play this gate for real · $1".
#    The top 3 of each gate qualify for the next race (3 gates x 3 = 9 runners).
#  - Voting focus: no cash prize-pot challenges, no Podium/Quick Sprint alternation, no Freeroll pop.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# ---------- race: 9 runners ----------
RA("RACE_FIN = [.31, .24, .19, .15, .11];", "RACE_FIN = [.2, .16, .13, .11, .1, .09, .08, .07, .06], RACE_N = 9, RACE_ST = [1, 2, 5, 10, 20], RACE_AVG = 3, FREE_BET_COINS = 500;\nconst raceJP = sl => 250 + ((sl * 37) % 900);")
RA("list = ppShuffle((pool.length >= 5 ? pool : SEED.filter(x => x.src)).slice(), r);\n  const ph = list.slice(0, 5).map(",
   "list = ppShuffle(pool.slice(), r).concat(ppShuffle(SEED.filter(x => x.src && !pool.includes(x)), r));\n  const ph = list.slice(0, RACE_N).map(")
RA("if (mp) ph[4] = {", "if (mp) ph[RACE_N - 1] = {")
# pool is always the cash betting pool
RA("const ppPool = (n, cur) => cur === 'cash' ? `$${Math.round(n * PP_CASH * .8).toLocaleString()}` : `${Math.round(n * PP_COIN * .8).toLocaleString()} 🟡`;",
   "const ppPool = (n, cur) => `$${Math.round(n * RACE_AVG * .8).toLocaleString()}`;")
# compact live board for 9 runners
s = s.replace('</style>', """.rb-r{grid-template-columns:16px 30px 1fr auto!important;gap:6px!important;padding:2px 0!important}.rb-r img{width:30px!important;height:30px!important;border-radius:7px!important}.rb-t b{font-size:.8rem!important}.rb-t small{font-size:.66rem!important}
.pp-g.g9{grid-template-columns:repeat(3,1fr)!important;gap:6px!important}.pp-g.g9 .pp-t{grid-column:auto!important}.pp-g.g9 .pp-cap{font-size:.62rem!important;padding:2px 3px 3px!important}.pp-g.g9 .rf b{min-width:12px!important;height:12px!important;font-size:.56rem!important}.pp-g.g9 .pp-b{font-size:1.7rem!important}.pp-g.g9 .pp-im img{aspect-ratio:5/4!important;height:auto!important}
.rc-nx div{grid-template-columns:repeat(9,1fr)!important;gap:3px!important}.rc-fin{grid-template-columns:repeat(5,1fr)!important}
.rc-st{display:flex;gap:6px;justify-content:center;margin:2px 0 8px}.rc-st button{flex:1;border:0;border-radius:12px;padding:9px 0;font:inherit;font-weight:900;cursor:pointer}
html:not(.yg) .rc-st button{background:#F3ECDF;color:#2B2320;box-shadow:inset 0 0 0 1.5px #E6D9C4}html:not(.yg) .rc-st button[aria-pressed=true]{background:#F2C14E;box-shadow:none}
html.yg .rc-st button{background:#2A1A52;color:#fff}html.yg .rc-st button[aria-pressed=true]{background:#FFC93C;color:#14092B}
.rc-jp{margin:0 0 8px;padding:6px 10px;border-radius:12px;font-size:.86rem;font-weight:800}html:not(.yg) .rc-jp{background:#FFF4D6;color:#5A3E00}html.yg .rc-jp{background:#3A2766;color:#FFE27A}
.gt-q{margin:4px 0 8px;font-size:.86rem;font-weight:700}
</style>""", 1)

# ---------- race: pick screen with bets ----------
a = s.index("function ppOpen() {"); b = s.index("function raceCard() {")
s = s[:a] + r"""function ppOpen() { const g = ppGame(), e = (S.pp || {})[g.sl], own = g.ph.some(p => p.mine), cash = isCash(), y = isYoungW(), cn = esc(crownName(g.k)), bk = ppBack(g), jp = raceJP(g.sl); let picks = e ? e.picks.slice() : [], stake = RACE_ST.includes(S.raceSt) ? S.raceSt : 2; window.__rbSl = g.sl;
  const head = `<button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 The ${raceName(g.sl)} race · ${cn}</p>`, keep = $('#panes').dataset.at === 'judge' ? (y ? 'Keep judging' : 'Keep voting') : 'Close';
  const bind = () => { if ($('#ppLater')) $('#ppLater').onclick = () => popClose(); if ($('#ppCard')) $('#ppCard').onclick = () => raceCard(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); };
  if (e || own) { popOpen(`<div class="pp">${head}<h2 class="pp-h">${e ? (e.free ? 'Your free $1 bet is in!' : `Your ${money(e.stake || 1)} bet is in!`) : 'Your photo is running!'}</h2><p class="pp-m"><b>${ppPool(g.players)}</b> pool · ${g.players} players · ends ${frTime(g.end)}</p>
      ${ppBoard(g, e)}<p class="pp-i">${e ? `Results at ${frTime(ppDue(e))} <small>(demo: about 2 min)</small>` : `Top 3 photos win <b>${ownTxt(true)}</b>. Owners can’t pick in their own race.`}</p>
      ${e && e.free && !cash ? `<button class="btn block pc-real" id="ppMore">💵 Bet more on this race · from $1</button>` : ''}
      <button class="btn block pc-go" id="ppLater">${keep}</button><div style="text-align:center"><button class="link pc-later" id="ppCard">🏇 Race card</button></div></div>`); bind();
    if ($('#ppMore')) $('#ppMore').onclick = () => { popClose(); payCash(5, 'A race bet', () => { S.pp[g.sl].stake = (S.pp[g.sl].stake || 1) + 5; S.pp[g.sl].free = 0; save(); toast('🏇 $5 more on your picks'); setTimeout(ppOpen, 300); }); };
    return; }
  const freeOk = (S.gems || 0) >= FREE_BET_COINS;
  const draw = () => { const n3 = picks.length === 3;
    popOpen(`<div class="pp">${head}<h2 class="pp-h">Pick the top 3 of 9</h2>
      <p class="pp-m"><b>${ppPool(g.players)}</b> pool · ${g.players} players · closes ${frTime(g.end)}</p>
      <p class="rc-jp">🎯 Perfect 1-2-3 jackpot · <b>$${jp.toLocaleString()}</b></p>
      <div class="pp-g g9">${g.ph.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on' : ''}" data-pp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-b">${PP_MED[n]}</i>` : ''}</span><span class="pp-cap"><span class="rf">${formHTML(p.form)}</span><b>${bk[i]}%</b></span></button>`; }).join('')}</div>
      <p class="pp-i">${n3 ? 'Your podium is set. Tap a photo to change it.' : `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo`}</p>
      ${cash ? `<div class="rc-st" role="group" aria-label="Bet">${RACE_ST.map(v => `<button data-rst="${v}" aria-pressed="${v === stake}">$${v}</button>`).join('')}</div>
        <button class="btn block pc-go" id="ppGo" ${n3 ? '' : 'disabled'}>🏇 Bet ${money(stake)} on my 1-2-3</button>`
      : `<button class="btn block pc-go" id="ppFree" ${n3 && freeOk ? '' : 'disabled'}>🎟️ Free $1 bet · ${FREE_BET_COINS} 🟡</button>
        <button class="btn block pc-real" id="ppReal" ${n3 ? '' : 'disabled'}>💵 Bet for real · from $1</button>${freeOk ? '' : `<p class="pp-r">You need ${(FREE_BET_COINS - Math.floor(S.gems || 0)).toLocaleString()} more 🟡 for the free bet. ${y ? 'Judge' : 'Vote'} to earn them.</p>`}`}
      <p class="pp-r">10 pts for each photo in the right place · 5 if it made the top 3 in a different place. Top 10% share the pool by stake. ${y ? 'Judges' : 'Voters'} decide.</p>
      <div style="text-align:center"><button class="link pc-later" id="ppCard">🏇 Race card</button> · <button class="link pc-later" id="ppLater">${keep}</button></div></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, n = picks.indexOf(i); if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); draw(); });
    document.querySelectorAll('#coach [data-rst]').forEach(b => b.onclick = () => { stake = +b.dataset.rst; S.raceSt = stake; save(); draw(); });
    const rec = (st, free) => { S.pp = S.pp || {}; S.pp[g.sl] = { sl: g.sl, picks: picks.slice(), cur: 'cash', stake: st, free: free ? 1 : 0, at: Date.now(), players: g.players }; save(); toast(free ? '🎟️ Free $1 bet placed! Watch it live.' : `🏇 ${money(st)} bet placed! Watch it live.`); setTimeout(ppOpen, 300); };
    if ($('#ppGo')) $('#ppGo').onclick = () => { if (picks.length < 3) return; popClose(); payCash(stake, 'A race bet', () => rec(stake)); };
    if ($('#ppFree')) $('#ppFree').onclick = () => { if (picks.length < 3 || (S.gems || 0) < FREE_BET_COINS) return; if (S.user && S.user.guest) { popClose(); openSignup(() => ppOpen(), { locked: false }); return; } S.gems -= FREE_BET_COINS; paintGems(); rec(1, true); };
    if ($('#ppReal')) $('#ppReal').onclick = () => { if (picks.length < 3) return; popClose(); payCash(2, 'A race bet', () => rec(2)); };
    bind(); };
  draw(); }
""" + s[b:]

# ---------- race: results paid by stake, jackpot, free bet ----------
a = s.index("function ppResult(e) {"); b = s.index("setInterval(() => { if (!S || !S.pp ||")
s = s[:a] + r"""function ppResult(e) { const g = ppGame(e.sl), r = cpRng(e.sl * 31 + 5), sc = ppScore(e.picks, g.ord), n = e.players || g.players, st = e.stake || 1, jp = raceJP(e.sl); let better = 0;
  for (let i = 0; i < n - 1; i++) { const a = ppShuffle([...Array(RACE_N).keys()], r); if (r() < .45) { const w = a.indexOf(g.ord[0]); [a[0], a[w]] = [a[w], a[0]]; } if (ppScore(a.slice(0, 3), g.ord) > sc) better++; }
  const rank = better + 1, paid = Math.max(3, Math.ceil(n * .1)), win = rank <= paid, net = n * RACE_AVG * .8, perfect = sc === 30;
  let prize = win ? +(net * st / ((paid - 1) * RACE_AVG + st)).toFixed(2) : 0; const jpWin = perfect ? +(jp / (1 + (e.sl % 2))).toFixed(2) : 0; prize = +(prize + jpWin).toFixed(2);
  const amt = money(prize), cashP = isCash(), y = isYoungW();
  Object.assign(e, { done: 1, score: sc, rank, prize }); if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); paintWallet(); } save();
  const top = g.ord.slice(0, 3), mk = (p, i) => top[i] === p ? '✅' : top.includes(p) ? '↕️' : '❌';
  popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pp-k">🏇 The ${raceName(g.sl)} race · ${esc(crownName(g.k))} · results</p><p class="pp-win">🏆 Won by <b>“${esc(g.ph[g.ord[0]].t)}”</b> · @${esc(g.ph[g.ord[0]].h)}<small>Photo owners won ${ownTxt(true)}</small></p><h2 class="pp-h">${prize ? `You won ${amt}!` : `${sc} points`}</h2>
    <p class="pp-m"><b>${sc} points</b> · ${ppOrd(rank)} of ${n} · ${e.free ? 'free $1 bet' : `${money(st)} bet`}${prize ? '' : ` · top ${paid} paid`}</p>${jpWin ? `<p class="rc-jp">🎯 Perfect 1-2-3! Jackpot share <b>${money(jpWin)}</b></p>` : ''}
    <div class="pp-cmp"><small>Crowd’s top 3</small><div>${top.map((p, i) => `<figure><img src="${g.ph[p].src}" alt=""><i>${PP_MED[i]}</i></figure>`).join('')}</div>
      <small>Your picks</small><div>${e.picks.map((p, i) => `<figure><img src="${g.ph[p].src}" alt=""><i>${mk(p, i)}</i></figure>`).join('')}</div></div>
    <p class="pp-r">✅ right place · ↕️ in the top 3, different place · ❌ not in the top 3</p>
    <button class="btn block ${cashP ? 'pc-go' : 'pc-real'}" id="ppNext">🏇 ${cashP ? 'Bet on the next race' : 'Bet for real on the next race'}</button>
    <div style="text-align:center"><button class="link pc-later" id="ppOk">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  if (prize) setTimeout(() => cashExplosion && cashExplosion(prize, { label: 'Hourly race' }), 500);
  $('#ppNext').onclick = () => { popClose(); raceCard(); }; $('#ppOk').onclick = () => { popClose(); go('judge'); }; document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
""" + s[b:]

# ---------- race card, rows, owner result: 9 runners, bets ----------
RA("<button class=\"btn block pc-go\" id=\"rcGo\">${e ? '🔴 Watch live' : own ? '🔴 Watch your photo run' : `🏅 Pick the top 3 · ${cash ? '$' + PP_CASH : PP_COIN + ' 🟡'}`}</button>",
   "<p class=\"rc-jp\">🎯 Perfect 1-2-3 jackpot · <b>$${raceJP(cur).toLocaleString()}</b></p><button class=\"btn block pc-go\" id=\"rcGo\">${e ? '🔴 Watch live' : own ? '🔴 Watch your photo run' : `🏇 Pick the top 3 · ${cash ? 'bet from $1' : 'free $1 bet'}`}</button>")
RA("<b>${ppPool(g.players, (e ? e.cur === 'cash' : cash) ? 'cash' : 'gems')}</b> pool", "<b>${ppPool(g.players)}</b> pool")
RA("const pl = i < 0 ? 5 : g.ord.indexOf(i) + 1,", "const pl = i < 0 ? RACE_N : g.ord.indexOf(i) + 1,")
RA("<span class=\"tsr2-p\">${ppPool(g.players, cash ? 'cash' : 'gems')}</span>", "<span class=\"tsr2-p\">${ppPool(g.players)}</span>")
RA("<span class=\"tsr2-e\">${e ? 'View' : cash ? `$${PP_CASH}` : `${PP_COIN} 🟡`}</span>", "<span class=\"tsr2-e\">${e ? 'View' : cash ? 'Bet' : 'Free $1'}</span>")

# ---------- gates ----------
s = s.replace("function fcNotify() {", r"""var GATE_EVERY = 10, GATE_COINS = [0, 0, 20, 50], GATE_CASH = [0, 0, 1.5, 5], GATE_FEE = 1;
function gateGame() { const ns = ppSlot() + 1, R = ppGame(ns); let gi = (S.gateI || 0) % 3; for (let t = 0; t < 3 && [0, 1, 2].some(j => R.ph[3 * gi + j] && R.ph[3 * gi + j].mine); t++) gi = (gi + 1) % 3;
  const q = [0, 1, 2].map(j => R.ph[3 * gi + j]).sort((a, b) => b.st - a.st), used = new Set(R.ph.map(p => p.src)), rr = cpRng(ns * 17 + gi * 5 + (S.gateN || 0));
  const fill = ppShuffle(SEED.filter(x => x.src && !used.has(x.src)), rr).slice(0, 2).map((x, i) => ({ src: x.src, t: x.title || 'Untitled', h: QS_NAMES[(ns + i + 3) % QS_NAMES.length] }));
  const all = q.concat(fill), disp = ppShuffle([0, 1, 2, 3, 4], rr); return { ns, gi, ph: disp.map(i => all[i]), ord: [0, 1, 2, 3, 4].map(k => disp.indexOf(k)) }; }
function gateOpen(real) { const G = gateGame(), y = isYoungW(), keep = y ? 'Keep judging' : 'Keep voting'; let picks = [];
  const draw = () => { const n3 = picks.length === 3;
    popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🚦 Qualification gate ${G.gi + 1} of 3 · the ${raceName(G.ns)} race</p><h2 class="pp-h">Pick the top 3 of 5</h2>
      <p class="pp-m">${real ? `Real gate · <b>$${GATE_FEE}</b> · perfect 1-2-3 wins <b>$${GATE_CASH[3]}</b>` : `Free · perfect 1-2-3 wins <b>${GATE_COINS[3]} 🟡</b> · 2 right <b>${GATE_COINS[2]} 🟡</b>`}</p>
      <div class="pp-g">${G.ph.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on' : ''}" data-pp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-b">${PP_MED[n]}</i>` : ''}</span></button>`; }).join('')}</div>
      <p class="pp-i">${n3 ? 'Your podium is set. Tap a photo to change it.' : `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo`}</p>
      <button class="btn block pc-go" id="gtGo" ${n3 ? '' : 'disabled'}>${real ? `🚦 Play for real · $${GATE_FEE}` : '🚦 Lock in · free'}</button>
      <p class="pp-r">${y ? 'Judges' : 'Voters'} already ranked this gate. Its top 3 photos qualify for the ${raceName(G.ns)} race.</p>
      <div style="text-align:center"><button class="link pc-later" id="gtNo">${keep}</button></div></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, n = picks.indexOf(i); if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); draw(); });
    $('#gtNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#gtGo').onclick = () => { if (picks.length < 3) return; if (real) { popClose(); payCash(GATE_FEE, 'A real gate', () => gateResult(G, picks, true)); } else gateResult(G, picks, false); }; };
  draw(); }
function gateResult(G, picks, real) { const y = isYoungW(), top = G.ord.slice(0, 3), right = picks.filter((p, i) => top[i] === p).length, pay = real ? GATE_CASH[right] : GATE_COINS[right];
  S.gateI = (S.gateI || 0) + 1; S.gateN = (S.gateN || 0) + 1; if (pay) { if (real) { S.cash = +((S.cash || 0) + pay).toFixed(2); setTimeout(paintWallet, 300); } else { S.gems = (S.gems || 0) + pay; setTimeout(paintGems, 300); } } save();
  const mk = (p, i) => top[i] === p ? '✅' : top.includes(p) ? '↕️' : '❌', amt = real ? money(pay) : `${pay} 🟡`;
  popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🚦 Gate ${G.gi + 1} of 3 · result</p>
    <h2 class="pp-h">${pay ? `You won ${amt}!` : right === 1 ? '1 in the right place' : 'Not this time'}</h2><p class="pp-m">${right} of 3 in the right place</p>
    <div class="pp-cmp"><small>Crowd’s top 3 · qualified ✓</small><div>${top.map((p, i) => `<figure><img src="${G.ph[p].src}" alt=""><i>${PP_MED[i]}</i></figure>`).join('')}</div>
      <small>Your picks</small><div>${picks.map((p, i) => `<figure><img src="${G.ph[p].src}" alt=""><i>${mk(p, i)}</i></figure>`).join('')}</div></div>
    <p class="gt-q">✅ These 3 run in the <b>${raceName(G.ns)} race</b></p>
    ${real ? `<button class="btn block pc-go" id="gtAgain">🚦 Next gate for real · $${GATE_FEE}</button>` : `<button class="btn block pc-real" id="gtReal">💵 Real gate · $${GATE_FEE} · win $${GATE_CASH[3]}</button>`}
    <button class="btn block pc-go" id="gtRace">🏇 Bet on the ${raceName(G.ns)} race</button>
    <div style="text-align:center"><button class="link pc-later" id="gtNo">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  if (pay) setTimeout(() => real ? cashExplosion && cashExplosion(pay, { label: 'Gate win' }) : gemExplosion(pay, { label: 'Gate win' }), 400);
  if ($('#gtReal')) $('#gtReal').onclick = () => gateOpen(true); if ($('#gtAgain')) $('#gtAgain').onclick = () => gateOpen(true);
  $('#gtRace').onclick = () => raceCard(); $('#gtNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
setInterval(() => { if (!S || !S.gatePend || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || $('#panes').dataset.at !== 'judge') return; S.gatePend = 0; save(); gateOpen(false); }, 1200);
function raceBetRowHTML() { const g = ppGame(), e = (S.pp || {})[g.sl], ok = !e && (S.gems || 0) >= FREE_BET_COINS;
  return `<button class="ug-r ug-swap" id="rbBet"><span class="ug-i">🏇</span><span class="ug-t"><b>Free $1 race bet</b><small>${e ? `You’re in the ${raceName(g.sl)} race` : `The ${raceName(g.sl)} race · pick the top 3 of 9`}</small></span><em class="${ok ? '' : 'need'}">${FREE_BET_COINS} 🟡</em></button>`; }
document.addEventListener('click', e => { if (e.target.closest('#rbBet')) { e.preventDefault(); e.stopPropagation(); try { closeSheet(); } catch (x) {} ppOpen(); } }, true);
function fcNotify() {""", 1)
# a gate every 10 votes
RA("S.votes++; S.cpN = (S.cpN || 0) + 1;", "S.votes++; S.cpN = (S.cpN || 0) + 1; S.gtN = (S.gtN || 0) + 1; if (S.gtN >= GATE_EVERY && S.photos && S.photos.length) { S.gtN = 0; S.gatePend = 1; }")
# Coming up: the next gate
RA("return it.sort((p, q) => p.need - q.need)[0] || null; }", "it.push({ ic: '🚦', t: `<b>Qualification gate</b> · pick 3 of 5 · free`, k: 'g', need: Math.max(1, GATE_EVERY - (S.gtN || 0)), per: GATE_EVERY });\n  return it.sort((p, q) => p.need - q.need)[0] || null; }")
RA("function upNow() { const x = upNext(); if (!x) return;", "function upNow() { const x = upNext(); if (!x) return; if (x.k === 'g') { S.gtN = 0; save(); gateOpen(false); return; }")
# Quick Sprint no longer alternates with the old Podium Pick
RA("function qgPop() {", "function qgPop() { window.__qsGame = 'qs'; qsPop(); return;")
RA("window.__qsGame = S.qgAlt ? 'pp' : 'qs'; S.qgAlt = !S.qgAlt;", "window.__qsGame = 'qs'; S.qgAlt = false;")
RA("it.push(S.qgAlt ? {", "it.push(false ? {")

# ---------- focus: no cash prize-pot challenges, no first-pot intro ----------
RA("function openBattle() {", "function openBattle() { if (!S.potSeen) { S.potSeen = 1; save(); }")
RA("S.btAlt = !S.btAlt; save();", "S.btAlt = false; save(); if (!fighters().length) return;")
RA("if (!S.potSeen) { const pp = fighters()[0]", "if (false) { const pp = fighters()[0]")
RA("else if (S.btAlt) { if (!S.nextBth", "else if (true) { if (!S.nextBth")
# Freeroll pop when a photo reaches 80 now points to racing
a = s.index("title: 'Freeroll ready!'"); b = s.index("later: 'Later' })", a)
s = s[:a] + "title: 'Ready to race!', text: `Your photo reached <b>${tot}</b>. Enter it in the <b>qualification gates</b>, free. Top 3 in a gate run in the hourly race, and the top 3 photos win <b>$10 · $5 · $2</b>.`, cta: '🏇 My stable', onCta: () => { closeFlow(); stableOpen(); }, " + s[b:]
# coins menu: the free $1 race bet replaces the Freeroll row
RA("${swapRowHTML()}", "${raceBetRowHTML()}")

RA("Practice · no blue ribbons at stake.", "Coins only.")
# ---------- creators: heats are called gates ----------
for a2, b2 in [("`Heats: ${hs}` : 'In the heats'", "`Gates: ${hs}` : 'In the gates'"), ("`Next heat in <b>", "`Next gate in <b>"), ("to enter the heats`", "to enter the gates`"),
               ("'Enter the heats again to race'", "'Enter the gates again to race'"), ("`Enter the heats free · top 3 win", "`Enter the gates free · top 3 win"),
               ("Heats are free. Top 3 in a heat qualifies for an hourly race.", "Gates are free. Top 3 in a gate qualify for the hourly race."),
               ("Enter heats<small>free</small>", "Enter gates<small>free</small>"), ("decide every heat and race. Heat winners get", "decide every gate and race. Gate winners get"),
               ("`🏇 In the heats! First heat in", "`🏇 In the gates! First gate in"), ("in a heat. Next heat in", "in a gate. Next gate in"), ("🏇 Heat result", "🚦 Gate result"),
               ("in its heat", "in its gate"), ("🏇 Back to the heats · free", "🚦 Back to the gates · free"), ("toast('🏇 Back in the heats!')", "toast('🚦 Back in the gates!')"),
               ("Top 3 in a heat qualifies.", "Top 3 in a gate qualify."), ("in the heats` : ''}", "in the gates` : ''}")]:
    RA(a2, b2)
s = s.replace("Race top 3 win <b>${ownTxt(cash)}</b>", "Race top 3 win <b>${ownTxt(true)}</b>").replace("Top 3 win <b>${ownTxt(cash)}</b>", "Top 3 win <b>${ownTxt(true)}</b>")
open(d + 'yofi-real.html', 'w').write(s); print('rm race ok')
