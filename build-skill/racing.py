# Real Money only: Podium Pick, instant Podium Pick, hourly race, heats, My stable.
# Run by simplify.py when YOFI_BUILD=real (see README).
# ---------- Podium Pick: hourly, 5 photos, pick the crowd's 1st/2nd/3rd; coin or cash pool; voters decide ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
s=s.replace("function fcNotify() {",r"""const PP_COIN = 50, PP_CASH = 2, PP_DEMO = 120000, PP_MED = ['🥇', '🥈', '🥉'];
const ppSlot = (t = Date.now()) => Math.floor(t / 3600e3);
const ppOrd = n => n + (n % 10 === 1 && n % 100 !== 11 ? 'st' : n % 10 === 2 && n % 100 !== 12 ? 'nd' : n % 10 === 3 && n % 100 !== 13 ? 'rd' : 'th');
function ppShuffle(a, r) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function ppGame(sl = ppSlot()) { const ks = CATS8.filter(k => k !== 'any'), k = ks[sl % ks.length], r = cpRng(sl * 13 + 7);
  const pool = SEED.filter(x => x.src && x.cat === BATTLE_POOL[k]), list = ppShuffle((pool.length >= 5 ? pool : SEED.filter(x => x.src)).slice(), r);
  const ph = list.slice(0, 5).map((x, i) => ({ src: x.src, h: (x.owner && x.owner.h) || QS_NAMES[(sl + i) % QS_NAMES.length] }));
  const ord = ppShuffle([0, 1, 2, 3, 4], r), players = 140 + Math.floor(r() * 120) + Math.floor((Date.now() % 3600e3) / 60000) * 2;
  return { sl, k, ph, ord, players, end: (sl + 1) * 3600e3 }; }
const ppScore = (p, ord) => { const t = ord.slice(0, 3); return p.reduce((a, x, i) => a + (t[i] === x ? 10 : t.includes(x) ? 5 : 0), 0); };
const ppPool = (n, cur) => cur === 'cash' ? `$${Math.round(n * PP_CASH * .8).toLocaleString()}` : `${Math.round(n * PP_COIN * .8).toLocaleString()} 🟡`;
const ppDue = e => Math.min((e.sl + 1) * 3600e3, e.at + PP_DEMO);
function ppOpen() { const g = ppGame(), e = (S.pp || {})[g.sl], cash = e ? e.cur === 'cash' : isCash(), y = isYoungW(), cn = esc(crownName(g.k)); let picks = e ? e.picks.slice() : [];
  const draw = () => { const n3 = picks.length === 3;
    popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
      <p class="pp-k">🏅 Podium Pick · ${cn}</p><h2 class="pp-h">Pick the crowd’s top 3</h2>
      <p class="pp-m"><b>${ppPool(g.players, cash ? 'cash' : 'gems')}</b> pool · ${g.players} players · closes ${frTime(g.end)}</p>
      <div class="pp-g">${g.ph.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on' : ''}" data-pp="${i}" ${e ? 'disabled' : ''}><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-b">${PP_MED[n]}</i>` : ''}</button>`; }).join('')}</div>
      <p class="pp-i">${e ? `✅ <b>You’re in.</b> Results at ${frTime(ppDue(e))} <small>(demo: about 2 min)</small>` : n3 ? 'Your podium is set. Tap a photo to change it.' : `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo`}</p>
      ${e ? '' : `<button class="btn block pc-go" id="ppGo" ${n3 ? '' : 'disabled'}>🏅 Enter · ${cash ? `$${PP_CASH}` : `${PP_COIN} 🟡`}</button>${cash ? '' : `<button class="btn block pc-real" id="ppReal" ${n3 ? '' : 'disabled'}>💵 Play for real · $${PP_CASH}</button>`}`}
      <p class="pp-r">10 pts for each photo in the right place · 5 if it made the top 3 in a different place. Top 10% share the pool. ${y ? 'Judges' : 'Voters'} decide.</p>
      <div style="text-align:center"><button class="link pc-later" id="ppLater">${$('#panes').dataset.at === 'judge' ? (y ? 'Keep judging' : 'Keep voting') : 'Not now'}</button></div></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, n = picks.indexOf(i); if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); draw(); });
    const rec = cur => { S.pp = S.pp || {}; S.pp[g.sl] = { sl: g.sl, picks: picks.slice(), cur, at: Date.now(), players: g.players }; save(); toast('🏅 You’re in! Results soon.'); setTimeout(ppOpen, 300); };
    if ($('#ppGo')) $('#ppGo').onclick = () => { if (picks.length < 3) return; if (cash) { popClose(); payCash(PP_CASH, 'Podium Pick', () => rec('cash')); return; }
      if (S.gems < PP_COIN) { popClose(); runOut('gems', `You need ${PP_COIN - Math.floor(S.gems)} more coins`); return; } S.gems -= PP_COIN; paintGems(); rec('gems'); };
    if ($('#ppReal')) $('#ppReal').onclick = () => { if (picks.length < 3) return; popClose(); payCash(PP_CASH, 'Podium Pick', () => rec('cash')); };
    $('#ppLater').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); };
  draw(); }
function ppResult(e) { const g = ppGame(e.sl), r = cpRng(e.sl * 31 + 5), sc = ppScore(e.picks, g.ord), n = e.players || g.players; let better = 0;
  for (let i = 0; i < n - 1; i++) { const a = ppShuffle([0, 1, 2, 3, 4], r); if (r() < .45) { const w = a.indexOf(g.ord[0]); [a[0], a[w]] = [a[w], a[0]]; } if (ppScore(a.slice(0, 3), g.ord) > sc) better++; }
  const rank = better + 1, paid = Math.max(3, Math.ceil(n * .1)), win = rank <= paid, net = n * (e.cur === 'cash' ? PP_CASH : PP_COIN) * .8;
  const prize = win ? (e.cur === 'cash' ? +(net / paid).toFixed(2) : Math.round(net / paid)) : 0, amt = e.cur === 'cash' ? money(prize) : `${prize.toLocaleString()} 🟡`;
  Object.assign(e, { done: 1, score: sc, rank, prize }); if (prize) { if (e.cur === 'cash') { S.cash = +((S.cash || 0) + prize).toFixed(2); paintWallet(); } else { S.gems += prize; paintGems(); } } save();
  const top = g.ord.slice(0, 3), mk = (p, i) => top[i] === p ? '✅' : top.includes(p) ? '↕️' : '❌', y = isYoungW();
  popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pp-k">🏅 Podium Pick · ${esc(crownName(g.k))} · results</p><h2 class="pp-h">${prize ? `You won ${amt}!` : `${sc} points`}</h2>
    <p class="pp-m"><b>${sc} points</b> · ${ppOrd(rank)} of ${n}${prize ? '' : ` · top ${paid} paid`}</p>
    <div class="pp-cmp"><small>Crowd’s top 3</small><div>${top.map((p, i) => `<figure><img src="${g.ph[p].src}" alt=""><i>${PP_MED[i]}</i></figure>`).join('')}</div>
      <small>Your picks</small><div>${e.picks.map((p, i) => `<figure><img src="${g.ph[p].src}" alt=""><i>${mk(p, i)}</i></figure>`).join('')}</div></div>
    <p class="pp-r">✅ right place · ↕️ in the top 3, different place · ❌ not in the top 3</p>
    <button class="btn block pc-go" id="ppOk">${y ? 'Keep judging' : 'Keep voting'}</button></div>`);
  if (prize) setTimeout(() => e.cur === 'cash' ? cashExplosion && cashExplosion(prize, { label: 'Podium Pick' }) : gemExplosion(prize, { label: 'Podium Pick' }), 500);
  $('#ppOk').onclick = () => { popClose(); go('judge'); }; document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
setInterval(() => { if (!S || !S.pp || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on')) return; const now = Date.now();
  const e = Object.values(S.pp).find(x => !x.done && now >= ppDue(x)); if (e) ppResult(e); }, 3000);
const ppRowHTML = () => { if (!S || S.geoBlock) return ''; const g = ppGame(), e = (S.pp || {})[g.sl], cash = e ? e.cur === 'cash' : isCash();
  return `<button class="tsr2 pprow ${e ? 'in' : ''}" id="ppRow"><span class="tsr2-t"><span class="fr-tag pp-tag">${e ? 'YOU’RE IN ✓' : 'PODIUM PICK'}</span><b>${tLeft(g.end)}</b></span><span class="tsr2-p">${ppPool(g.players, cash ? 'cash' : 'gems')}</span><span class="tsr2-n"><small>Pick top 3</small></span><span class="tsr2-e">${e ? 'View' : cash ? `$${PP_CASH}` : `${PP_COIN} 🟡`}</span></button>`; };
document.addEventListener('click', e => { if (e.target.closest('#ppRow')) { e.preventDefault(); e.stopPropagation(); ppOpen(); } }, true);
function fcNotify() {""",1)
RA('<div class="tsl2" data-tfl="${TF}">${chRowHTML()}${frRows}${rows}</div>','<div class="tsl2" data-tfl="${TF}">${ppRowHTML()}${chRowHTML()}${frRows}${rows}</div>')
# Coming up: Podium Pick in its last 20 minutes, if not entered
RA("return it.sort((p, q) => p.need - q.need)[0] || null; }",
   "{ const g = ppGame(), m = Math.ceil((g.end - Date.now()) / 60000); if (S.potSeen && !(S.pp || {})[g.sl] && m <= 20) return { ic: '🏅', t: `<b>Podium Pick · ${esc(crownName(g.k))}</b> · pick the top 3`, k: 'p', need: 0, per: 1, mins: m }; }\n  return it.sort((p, q) => p.need - q.need)[0] || null; }")
RA("function upNow() { const x = upNext(); if (!x) return;","function upNow() { const x = upNext(); if (!x) return; if (x.k === 'p') { ppOpen(); return; }")
RA('<em>${x.need ? `in ${x.need} vote${x.need === 1 ? \'\' : \'s\'}` : \'Now\'}</em>','<em>${x.k === \'p\' ? `${x.mins} min left` : x.need ? `in ${x.need} vote${x.need === 1 ? \'\' : \'s\'}` : \'Now\'}</em>')
s=s.replace('</style>',""".pp{position:relative;text-align:center;padding:4px 2px 2px}.pp-k{margin:22px 30px 2px;font-size:.74rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase}.pp-h{margin:0 0 4px;font-size:1.5rem;line-height:1.15}
.pp-m{margin:0 0 10px;font-size:.88rem}.pp-g{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:0 0 8px}.pp-t{grid-column:span 2;position:relative;border:0;padding:0;border-radius:14px;overflow:hidden;cursor:pointer;background:none}.pp-t:nth-child(4){grid-column:2/span 2}.pp-t:nth-child(5){grid-column:4/span 2}
.pp-t img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}.pp-t.on img{filter:brightness(.82)}.pp-b{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-style:normal;font-size:2.2rem;line-height:1;filter:drop-shadow(0 2px 4px rgba(0,0,0,.4));animation:qsPlus .35s ease-out}
.pp-i{margin:0 0 10px;font-size:.92rem;min-height:1.3em}.pp-i small{opacity:.7}.pp-r{margin:8px 0 4px;font-size:.76rem;line-height:1.4;opacity:.85}.pp .pc-go,.pp .pc-real{text-transform:none!important}
.pp-cmp{text-align:left;margin:0 0 4px}.pp-cmp small{display:block;font-size:.72rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;margin:6px 0 4px;opacity:.75}.pp-cmp>div{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.pp-cmp figure{margin:0;position:relative}.pp-cmp img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:12px;display:block}.pp-cmp figure i{position:absolute;right:4px;top:4px;font-style:normal;font-size:1.3rem;filter:drop-shadow(0 1px 3px rgba(0,0,0,.4))}
html:not(.yg) .pp-k{color:#2F6B3F}html:not(.yg) .pp-h{color:#1F2F55;font-family:"Fraunces",serif}html:not(.yg) .pp-m,html:not(.yg) .pp-i,html:not(.yg) .pp-r{color:#2B2320}html:not(.yg) .pp-m b{color:#2F6B3F}html:not(.yg) .pp-t{box-shadow:0 0 0 2px #E6D9C4}html:not(.yg) .pp-t.on{box-shadow:0 0 0 3px #D9A441}
html.yg .pp-k{color:#2EE59D}html.yg .pp-h{color:#fff}html.yg .pp-m,html.yg .pp-i,html.yg .pp-r{color:#E9E2FF}html.yg .pp-m b{color:#2EE59D}html.yg .pp-t{box-shadow:0 0 0 2px #3A2766}html.yg .pp-t.on{box-shadow:0 0 0 3px #FFC93C}
.tsr2.pprow .pp-tag{background:#2D4E86!important;color:#fff!important}html.yg .tsr2.pprow .pp-tag{background:#C13CFF!important}.tsr2.pprow .tsr2-n small{font-size:.72rem;font-weight:800;line-height:1.1;text-align:center}
html:not(.yg) .tsr2.pprow{background:#EEF2FA!important;box-shadow:inset 0 0 0 1.5px #2D4E86!important}html.yg .tsr2.pprow{background:#24164A!important;box-shadow:inset 0 0 0 1.5px #C13CFF!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('podium ok')
s=open(d+'yofi-simple.html').read(); a="${e ? 'YOU’RE IN ✓' : 'PODIUM PICK'}</span>"; assert s.count(a)==1
s=s.replace(a,"${e ? 'IN ✓' : '🏅 PODIUM'}</span>")
s=s.replace('</style>','.tsr2.pprow .pp-tag{white-space:nowrap}.tsr2.pprow .tsr2-p{white-space:nowrap}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('pp tag ok')
s=open(d+'yofi-simple.html').read(); s=s.replace('</style>','.tsr2.pprow .tsr2-t{flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:2px!important}.tsr2.pprow .pp-tag{display:inline-block!important;font-size:.6rem!important;font-weight:900!important;line-height:1.3!important;padding:2px 7px!important;border-radius:6px!important;letter-spacing:.04em!important}.tsr2.pprow .tsr2-t b{font-size:1rem}\n</style>',1); open(d+'yofi-simple.html','w').write(s); print('pp row ok')

# ---------- Instant Podium Pick (1 v 1) alternating with Quick Sprint; scheduled Podium Pick every 30 minutes ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# scheduled every 30 min (set PP_MS = 3600e3 for hourly)
RA("const PP_COIN = 50, PP_CASH = 2, PP_DEMO = 120000,","const PP_MS = 3600e3, PP_COIN = 50, PP_CASH = 2, PP_DEMO = 120000,")
RA("const ppSlot = (t = Date.now()) => Math.floor(t / 3600e3);","const ppSlot = (t = Date.now()) => Math.floor(t / PP_MS);")
RA("return { sl, k, ph, ord, players, end: (sl + 1) * 3600e3 }; }","return { sl, k, ph, ord, players, end: (sl + 1) * PP_MS }; }")
RA("const ppDue = e => Math.min((e.sl + 1) * 3600e3, e.at + PP_DEMO);","const ppDue = e => Math.min((e.sl + 1) * PP_MS, e.at + PP_DEMO);")
RA("players = 140 + Math.floor(r() * 120) + Math.floor((Date.now() % 3600e3) / 60000) * 2;","players = 140 + Math.floor(r() * 120) + Math.floor((Date.now() % PP_MS) / 60000) * 2;")
RA("if (S.potSeen && !(S.pp || {})[g.sl] && m <= 20)","if (S.potSeen && !(S.pp || {})[g.sl] && m <= 20)")
# quick game runner switch
s=s.replace("qsRun();","(window.__qsGame === 'pp' ? ppqRun() : qsRun());")
RA('<h2 class="qs2-t">🎯 Quick Sprint</h2><p class="qs2-sub">1 vs 1 · 10 photo pairs</p>','<h2 class="qs2-t">${window.__qsGame === \'pp\' ? \'🏅 Podium Pick\' : \'🎯 Quick Sprint\'}</h2><p class="qs2-sub">${window.__qsGame === \'pp\' ? \'1 vs 1 · pick the top 3 of 5\' : \'1 vs 1 · 10 photo pairs\'}</p>')
s=s.replace("function fcNotify() {",r"""function ppqRun() { window.__qsGame = 'qs'; const pr = window.__qsPractice, st = window.__qsStake || 2, r = cpRng(window.__qsSet || 7), ks = CATS8.filter(k => k !== 'any'), k = ks[Math.floor(r() * ks.length)];
  const pool = SEED.filter(x => x.src && x.cat === BATTLE_POOL[k]), list = ppShuffle((pool.length >= 5 ? pool : SEED.filter(x => x.src)).slice(), r).slice(0, 5), ord = ppShuffle([0, 1, 2, 3, 4], r);
  const opp = QS_NAMES[Math.floor(r() * QS_NAMES.length)], oa = ppShuffle([0, 1, 2, 3, 4], r); if (r() < .55) { const w = oa.indexOf(ord[0]); [oa[0], oa[w]] = [oa[w], oa[0]]; }
  const os = ppScore(oa.slice(0, 3), ord), oms = 6000 + Math.floor(r() * 9000), t0 = Date.now(), y = isYoungW(); let picks = [];
  const prize = pr ? `${QS_COIN_PAY[0]} 🟡` : qsM(qsPay(st)[0]);
  const draw = () => { popOpen(`<div class="pp"><p class="pp-k">🏅 Podium Pick${pool.length >= 5 ? ` · ${esc(crownName(k))}` : ''} · vs @${esc(opp)}</p><h2 class="pp-h">Pick the crowd’s top 3</h2>
    <p class="pp-m">Winner gets <b>${prize}</b> · same 5 photos as @${esc(opp)}</p>
    <div class="pp-g">${list.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on' : ''}" data-pp="${i}"><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-b">${PP_MED[n]}</i>` : ''}</button>`; }).join('')}</div>
    <p class="pp-i">${picks.length < 3 ? `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo` : 'Your podium is set. Tap a photo to change it.'}</p>
    <button class="btn block pc-go" id="ppqGo" ${picks.length < 3 ? 'disabled' : ''}>🏅 Lock in my podium</button>
    <p class="pp-r">The crowd has already judged these photos. Higher score wins · tie goes to the faster player.</p></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, n = picks.indexOf(i); if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); draw(); });
    $('#ppqGo').onclick = () => { if (picks.length === 3) ppqDone(); }; };
  const ppqDone = () => { const ms = Date.now() - t0, sc = ppScore(picks, ord), won = sc > os || (sc === os && ms <= oms), pay = pr ? QS_COIN_PAY[0] : qsPay(st)[0];
    if (pr) { S.qsTried = 1; if (won) { S.gems = (S.gems || 0) + pay; setTimeout(paintGems, 200); } } else if (won) { S.cash = +((S.cash || 0) + pay).toFixed(2); setTimeout(paintWallet, 200); } save();
    const top = ord.slice(0, 3), mk = (p, i) => top[i] === p ? '✅' : top.includes(p) ? '↕️' : '❌', amt = pr ? `${pay} 🟡` : qsM(pay);
    popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏅 Podium Pick${pr ? ' · coins' : ''}</p>
      <h2 class="pp-h">${won ? `You won ${amt}!` : sc === os ? 'Lost on time!' : 'So close!'}</h2>
      <p class="pp-m"><b>You ${sc}</b> · @${esc(opp)} ${os} points${sc === os ? ` · ${(ms / 1000).toFixed(1)}s vs ${(oms / 1000).toFixed(1)}s` : ''}</p>
      <div class="pp-cmp"><small>Crowd’s top 3</small><div>${top.map((p, i) => `<figure><img src="${list[p].src}" alt=""><i>${PP_MED[i]}</i></figure>`).join('')}</div>
        <small>Your picks</small><div>${picks.map((p, i) => `<figure><img src="${list[p].src}" alt=""><i>${mk(p, i)}</i></figure>`).join('')}</div></div>
      <button class="btn block pc-go" id="ppqAgain">${pr ? `Play again · ${QS_COIN} 🟡` : `Play again · ${qsM(st)} entry`}</button>${pr ? `<button class="btn block pc-real" id="ppqReal">💵 Play for real · win ${qsM(qsPay(2)[0])}</button>` : ''}
      <div style="text-align:center"><button class="link pc-later" id="ppqBack">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
    if (won && !pr) setTimeout(() => cashExplosion && cashExplosion(pay, { label: 'Podium Pick' }), 400);
    $('#ppqAgain').onclick = () => { popClose(); window.__qsGame = 'pp'; pr ? sprPractice() : sprEnter(st); };
    if ($('#ppqReal')) $('#ppqReal').onclick = () => { popClose(); window.__qsGame = 'pp'; window.__qsReal = 1; sprEnter(); };
    $('#ppqBack').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); };
  draw(); }
function qgPop() { const pp = !!S.qgAlt; S.qgAlt = !S.qgAlt; save(); if (!pp) { window.__qsGame = 'qs'; qsPop(); return; }
  const c = isCash(); celebrate({ src: (SEED[3] || {}).src, score: '🏅', title: 'Podium Pick', text: `Pick the crowd’s <b>top 3 of 5 photos</b>, 1 v 1 against a real player. Highest score wins: ${c ? `up to <b>$32</b>` : `<b>${QS_COIN_PAY[0]} 🟡</b>`}.`, cta: c ? '🏅 Play · from $2' : `🏅 Play · ${QS_COIN} 🟡`, onCta: () => { window.__qsGame = 'pp'; sprEnter(); }, later: 'Keep voting' }); }
function fcNotify() {""",1)
RA("S.qsPopAt = Date.now(); save(); renderJudge(); judging = false; qsPop(); return; }","S.qsPopAt = Date.now(); save(); renderJudge(); judging = false; qgPop(); return; }")
# Coming up line: alternate label, and tapping opens the right game
RA("it.push({ ic: '🎯', t: `<b>Quick Sprint</b> · ${isCash() ? 'win up to $32' : `win ${QS_COIN_PAY[0]} 🟡`}`, k: 'q', need, per }); }",
   "it.push(S.qgAlt ? { ic: '🏅', t: `<b>Podium Pick</b> · pick the top 3 · ${isCash() ? 'win up to $32' : `win ${QS_COIN_PAY[0]} 🟡`}`, k: 'q', need, per } : { ic: '🎯', t: `<b>Quick Sprint</b> · ${isCash() ? 'win up to $32' : `win ${QS_COIN_PAY[0]} 🟡`}`, k: 'q', need, per }); }")
RA("if (x.k === 'q') { S.cpN = 0; S.qsPopAt = Date.now(); save(); sprEnter(); return; }","if (x.k === 'q') { S.cpN = 0; S.qsPopAt = Date.now(); window.__qsGame = S.qgAlt ? 'pp' : 'qs'; S.qgAlt = !S.qgAlt; save(); sprEnter(); return; }")
RA("onCta: () => sprEnter(), later: 'Keep voting' }); }","onCta: () => { window.__qsGame = 'qs'; sprEnter(); }, later: 'Keep voting' }); }")
open(d+'yofi-simple.html','w').write(s); print('pp quick ok')

# ---------- Hourly Race: race card, form, crowd backing, live race view, owner prizes (photographers enter free) ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# new race model: runners have strength, form; finish order follows strength + luck; owner's photo can run in a future race
a=s.index("function ppGame(sl = ppSlot()) {"); b=s.index("const ppScore = (p, ord) =>")
s=s[:a]+r"""const RACE_OWN = { cash: [10, 5, 2], gems: [300, 150, 50] }, RACE_FIN = [.31, .24, .19, .15, .11];
const ownTxt = c => c ? '$10 · $5 · $2' : '300 · 150 · 50 🟡';
const raceName = sl => { const t = new Date((sl + 1) * PP_MS); let h = t.getHours(); const m = t.getMinutes(), ap = h < 12 ? 'am' : 'pm'; h = h % 12 || 12; return `${h}${m ? ':' + String(m).padStart(2, '0') : ''}${ap}`; };
const ppHash = x => { let h = 7; for (const c of String(x)) h = (h * 31 + c.charCodeAt(0)) % 1e9; return h; };
const formHTML = f => f && f.length ? f.slice(-4).map(n => `<b class="${n <= 3 ? 'f' + n : ''}">${n}</b>`).join('') : '<i>Debut</i>';
function ppGame(sl = ppSlot()) { const ks = CATS8.filter(k => k !== 'any'), k = ks[sl % ks.length], r = cpRng(sl * 13 + 7);
  const pool = SEED.filter(x => x.src && x.cat === BATTLE_POOL[k]), list = ppShuffle((pool.length >= 5 ? pool : SEED.filter(x => x.src)).slice(), r);
  const ph = list.slice(0, 5).map((x, i) => { const q = cpRng(ppHash(x.id || x.title || i) + sl % 3), st = .3 + q() * .6;
    return { src: x.src, t: x.title || 'Untitled', h: (x.owner && x.owner.h) || QS_NAMES[(sl + i) % QS_NAMES.length], st, form: [0, 1, 2, 3].map(() => Math.min(5, Math.max(1, Math.round(1 + (1 - st) * 4.4 + (q() - .5) * 2.2)))) }; });
  const mine = ((S && S.races) || {})[sl], mp = mine && (S.photos || []).find(x => x.id === mine.pid);
  if (mp) ph[4] = { src: mp.src, t: mp.title || `My ${crownName(k)} shot`, h: (S.user && S.user.h) || 'you', st: Math.min(.95, Math.max(.3, ((mp.s && mp.s.total) || 80) / 100 * 1.6 - .64)), form: (S.raceHist || []).slice(-4), mine: 1 };
  const ord = ph.map((p, i) => [i, p.st + (r() - .5) * .45]).sort((p, q) => q[1] - p[1]).map(x => x[0]);
  const players = 140 + Math.floor(r() * 120) + Math.floor((Date.now() % PP_MS) / 60000) * 2;
  return { sl, k, ph, ord, players, end: (sl + 1) * PP_MS }; }
function ppBack(g, t = Date.now()) { const q = cpRng(g.sl * 101 + Math.floor(t / 60000) % 997), w = g.ph.map(p => Math.exp(3.2 * p.st + (q() - .5) * .9)), T = w.reduce((a, b) => a + b, 0);
  const v = w.map(x => Math.round(100 * x / T)); v[v.indexOf(Math.max(...v))] += 100 - v.reduce((a, b) => a + b, 0); return v; }
function ppLive(g, prog) { const q = cpRng(g.sl * 7 + Math.floor(Date.now() / 4000)), wt = Math.min(1, Math.pow(prog, .75)), tot = Math.round(g.players * 3.2 * prog);
  const ns = g.ph.map(p => p.st + q() * .7), T = ns.reduce((a, b) => a + b, 0);
  return g.ph.map((p, i) => ({ i, v: Math.round(tot * ((1 - wt) * ns[i] / T + wt * RACE_FIN[g.ord.indexOf(i)])) })).sort((a, b) => b.v - a.v || g.ord.indexOf(a.i) - g.ord.indexOf(b.i)); }
function ppBoard(g, e) { const now = Date.now(), cp = 1 - (g.end - now) / PP_MS, prog = Math.min(1, Math.max(.04, e ? Math.max(cp, (now - e.at) / PP_DEMO) : cp)), L = ppLive(g, prog), mx = Math.max(1, ...L.map(x => x.v));
  return `<div class="rb" id="rbLive"><p class="rb-h"><span class="rb-live">● LIVE</span>${L.reduce((a, x) => a + x.v, 0).toLocaleString()} votes so far</p>${L.map((x, n) => { const p = g.ph[x.i], pk = e ? e.picks.indexOf(x.i) : -1;
    return `<div class="rb-r ${p.mine ? 'me' : ''}"><b class="rb-n">${n + 1}</b><img src="${p.src}" alt=""><span class="rb-t"><b>${esc(p.t)}</b><small>@${esc(p.h)}${p.mine ? ' · your photo' : ''}${pk >= 0 ? ` · your ${PP_MED[pk]}` : ''}</small><i style="width:${Math.round(100 * x.v / mx)}%"></i></span><em>${x.v.toLocaleString()}</em></div>`; }).join('')}</div>`; }
setInterval(() => { const el = document.getElementById('rbLive'); if (!el || window.__rbSl == null || !S) return; const g = ppGame(window.__rbSl); el.outerHTML = ppBoard(g, (S.pp || {})[g.sl]); }, 2500);
"""+s[b:]
# pick screen: race name, form + backing under each runner; live board when entered or when your own photo runs
a=s.index("function ppOpen() {"); b=s.index("function ppResult(e) {")
s=s[:a]+r"""function ppOpen() { const g = ppGame(), e = (S.pp || {})[g.sl], own = g.ph.some(p => p.mine), cash = e ? e.cur === 'cash' : isCash(), y = isYoungW(), cn = esc(crownName(g.k)), bk = ppBack(g); let picks = e ? e.picks.slice() : []; window.__rbSl = g.sl;
  const head = `<button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 The ${raceName(g.sl)} race · ${cn}</p>`, keep = $('#panes').dataset.at === 'judge' ? (y ? 'Keep judging' : 'Keep voting') : 'Close';
  const bind = () => { if ($('#ppLater')) $('#ppLater').onclick = () => popClose(); if ($('#ppCard')) $('#ppCard').onclick = () => raceCard(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); };
  if (e || own) { popOpen(`<div class="pp">${head}<h2 class="pp-h">${e ? 'You’re in!' : 'Your photo is running!'}</h2><p class="pp-m"><b>${ppPool(g.players, cash ? 'cash' : 'gems')}</b> pool · ${g.players} players · ends ${frTime(g.end)}</p>
      ${ppBoard(g, e)}<p class="pp-i">${e ? `Results at ${frTime(ppDue(e))} <small>(demo: about 2 min)</small>` : `Top 3 photos win <b>${ownTxt(cash)}</b>. Owners can’t pick in their own race.`}</p>
      <button class="btn block pc-go" id="ppLater">${keep}</button><div style="text-align:center"><button class="link pc-later" id="ppCard">🏇 Race card</button></div></div>`); bind(); return; }
  const draw = () => { const n3 = picks.length === 3;
    popOpen(`<div class="pp">${head}<h2 class="pp-h">Pick the top 3</h2>
      <p class="pp-m"><b>${ppPool(g.players, cash ? 'cash' : 'gems')}</b> pool · ${g.players} players · closes ${frTime(g.end)}</p>
      <div class="pp-g">${g.ph.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on' : ''}" data-pp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-b">${PP_MED[n]}</i>` : ''}</span><span class="pp-cap"><span class="rf">${formHTML(p.form)}</span><b>${bk[i]}%</b></span></button>`; }).join('')}</div>
      <p class="pp-leg"><b>Form</b> = last 4 finishes · <b>%</b> = players backing it to win</p>
      <p class="pp-i">${n3 ? 'Your podium is set. Tap a photo to change it.' : `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo`}</p>
      <button class="btn block pc-go" id="ppGo" ${n3 ? '' : 'disabled'}>🏅 Enter · ${cash ? `$${PP_CASH}` : `${PP_COIN} 🟡`}</button>${cash ? '' : `<button class="btn block pc-real" id="ppReal" ${n3 ? '' : 'disabled'}>💵 Play for real · $${PP_CASH}</button>`}
      <p class="pp-r">10 pts for each photo in the right place · 5 if it made the top 3 in a different place. Top 10% share the pool. ${y ? 'Judges' : 'Voters'} decide.</p>
      <div style="text-align:center"><button class="link pc-later" id="ppCard">🏇 Race card</button> · <button class="link pc-later" id="ppLater">${keep}</button></div></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, n = picks.indexOf(i); if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); draw(); });
    const rec = cur => { S.pp = S.pp || {}; S.pp[g.sl] = { sl: g.sl, picks: picks.slice(), cur, at: Date.now(), players: g.players }; save(); toast('🏇 You’re in! Watch it live.'); setTimeout(ppOpen, 300); };
    $('#ppGo').onclick = () => { if (picks.length < 3) return; if (cash) { popClose(); payCash(PP_CASH, 'Hourly race', () => rec('cash')); return; }
      if (S.gems < PP_COIN) { popClose(); runOut('gems', `You need ${PP_COIN - Math.floor(S.gems)} more coins`); return; } S.gems -= PP_COIN; paintGems(); rec('gems'); };
    if ($('#ppReal')) $('#ppReal').onclick = () => { if (picks.length < 3) return; popClose(); payCash(PP_CASH, 'Hourly race', () => rec('cash')); };
    bind(); };
  draw(); }
function raceCard() { const cur = ppSlot(), cash = isCash(), y = isYoungW(), g = ppGame(cur), e = (S.pp || {})[cur], own = g.ph.some(p => p.mine), bk = ppBack(g);
  const mine = Object.entries(S.races || {}).filter(([sl, x]) => !x.done && +sl > cur).map(([sl, x]) => { const p = (S.photos || []).find(q => q.id === x.pid); return p ? `<p class="rc-mine">📷 <b>${esc(p.title || 'Your photo')}</b> runs in the <b>${raceName(+sl)}</b> race</p>` : ''; }).join('');
  const next = [cur + 1, cur + 2].map(sl => { const n = ppGame(sl); return `<div class="rc-nx"><p><b>${raceName(sl)}</b> · ${esc(crownName(n.k))}<small>opens ${frTime(sl * PP_MS)}</small></p><div>${n.ph.map(p => `<img src="${p.src}" class="${p.mine ? 'me' : ''}" alt="">`).join('')}</div></div>`; }).join('');
  popOpen(`<div class="pp rc"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 Race card</p><h2 class="pp-h">The ${raceName(cur)} race · ${esc(crownName(g.k))}</h2>
    <p class="pp-m"><b>${ppPool(g.players, (e ? e.cur === 'cash' : cash) ? 'cash' : 'gems')}</b> pool · ${g.players} players · <b class="rc-tl">${tLeft(g.end)}</b> left</p>
    <div class="rc-l"><p class="rc-cols"><span>Runner</span><span>Form</span><span>Backing</span></p>${g.ph.map((p, i) => `<div class="rc-r ${p.mine ? 'me' : ''}"><img src="${p.src}" alt=""><span class="rc-t"><b>${esc(p.t)}</b><small>@${esc(p.h)}${p.mine ? ' · you' : ''}</small></span><span class="rf">${formHTML(p.form)}</span><em><i style="width:${Math.min(100, bk[i] * 2)}%"></i>${bk[i]}%</em></div>`).join('')}</div>
    <button class="btn block pc-go" id="rcGo">${e ? '🔴 Watch live' : own ? '🔴 Watch your photo run' : `🏅 Pick the top 3 · ${cash ? '$' + PP_CASH : PP_COIN + ' 🟡'}`}</button>
    <p class="rc-sec">Next races</p>${next}
    <div class="rc-own"><b>📷 Race your photo, free</b><span>Top 3 photos in every race win <b>${ownTxt(cash)}</b><br>Photos need ${FR_MIN}+ · entry is free</span>${mine}<button class="btn block pc-real" id="rcEnter">Enter a photo</button></div>
    <div style="text-align:center"><button class="link pc-later" id="rcLater">${$('#panes').dataset.at === 'judge' ? (y ? 'Keep judging' : 'Keep voting') : 'Close'}</button></div></div>`);
  $('#rcGo').onclick = () => ppOpen(); $('#rcEnter').onclick = () => raceEnter(); $('#rcLater').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function raceEnter() { const cur = ppSlot(), cash = isCash(), y = isYoungW(), R = S.races || {}, busy = Object.values(R).filter(x => !x.done).map(x => x.pid), P = (S.photos || []).slice().sort((a, b) => b.s.total - a.s.total);
  if (!P.length) { popClose(); toast('Add a photo first, then race it.'); pickPhoto(true); return; }
  const ks = CATS8.filter(k => k !== 'any'), slotFor = p => { for (let sl = cur + 1; sl <= cur + ks.length; sl++) if (!R[sl] && fitsTheme(p, ks[sl % ks.length])) return sl; for (let sl = cur + 1; ; sl++) if (!R[sl]) return sl; };
  popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 Race your photo · free</p><h2 class="pp-h">Choose a photo</h2>
    <p class="pp-m">Top 3 win <b>${ownTxt(cash)}</b> · needs <b>${FR_MIN}+</b></p>
    <div class="re-g">${P.slice(0, 6).map(p => { const b = busy.includes(p.id), low = p.s.total < FR_MIN, sl = slotFor(p);
      return `<button class="re-t ${b || low ? 'off' : ''}" data-rep="${p.id}" ${b || low ? 'disabled' : ''}><img src="${p.src}" alt=""><b>${p.s.total}</b><small>${b ? 'Already racing' : low ? `Needs +${FR_MIN - p.s.total}` : `${raceName(sl)} race`}</small></button>`; }).join('')}</div>
    <p class="pp-r">Your photo runs in the next race for its category. ${y ? 'Judges' : 'Voters'} decide the finish. You can’t pick in a race your photo is in.</p>
    <div style="text-align:center"><button class="link pc-later" id="reBack">🏇 Back to race card</button></div></div>`);
  document.querySelectorAll('#coach [data-rep]').forEach(b => b.onclick = () => { const p = P.find(x => x.id === b.dataset.rep), sl = slotFor(p); S.races = S.races || {}; S.races[sl] = { pid: p.id, at: Date.now() }; save();
    popOpen(`<div class="pp"><p class="pp-k">🏇 Entered · free</p><div class="re-ok"><img src="${p.src}" alt=""></div><h2 class="pp-h">You’re racing in the ${raceName(sl)}!</h2>
      <p class="pp-m">${esc(crownName(ppGame(sl).k))} race · starts ${frTime(sl * PP_MS)} · results ${frTime((sl + 1) * PP_MS)}<br><small>(demo: result in about 3 min)</small></p>
      <p class="pp-i">Finish top 3 to win <b>${ownTxt(cash)}</b>. Share it to get more ${y ? 'judges' : 'voters'} watching.</p>
      <button class="btn block pc-go" id="reDone">${y ? 'Keep judging' : 'Keep voting'}</button></div>`); $('#reDone').onclick = () => popClose(); });
  $('#reBack').onclick = () => raceCard(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function raceOwnResult(sl) { const x = S.races[sl], g = ppGame(sl), i = g.ph.findIndex(p => p.mine), cash = isCash(), y = isYoungW();
  const pl = i < 0 ? 5 : g.ord.indexOf(i) + 1, pz = pl <= 3 ? RACE_OWN[cash ? 'cash' : 'gems'][pl - 1] : 0, amt = cash ? money(pz) : `${pz.toLocaleString()} 🟡`;
  const ph = i >= 0 ? g.ph[i] : { src: '', t: 'Your photo' }; S.raceHist = (S.raceHist || []).concat(pl).slice(-8); x.done = 1; x.place = pl; x.prize = pz;
  if (pz) { if (cash) { S.cash = +((S.cash || 0) + pz).toFixed(2); paintWallet(); } else { S.gems += pz; paintGems(); } } save();
  popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 The ${raceName(sl)} race · ${esc(crownName(g.k))} · result</p>
    <div class="re-ok">${ph.src ? `<img src="${ph.src}" alt="">` : ''}${pl <= 3 ? `<i>${PP_MED[pl - 1]}</i>` : ''}</div>
    <h2 class="pp-h">${pl <= 3 ? `Your photo finished ${ppOrd(pl)}!` : `Your photo finished ${ppOrd(pl)}`}</h2>
    <p class="pp-m">${pz ? `You won <b>${amt}</b>` : `Top 3 win prizes. Your form: ${S.raceHist.slice(-4).join('-')}`}</p>
    <div class="rc-fin">${g.ord.map((j, n) => `<span class="${g.ph[j].mine ? 'me' : ''}"><img src="${g.ph[j].src}" alt=""><b>${n < 3 ? PP_MED[n] : ppOrd(n + 1)}</b></span>`).join('')}</div>
    <button class="btn block pc-go" id="roAgain">🏇 Race another photo</button><div style="text-align:center"><button class="link pc-later" id="roBack">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  if (pz) setTimeout(() => cash ? cashExplosion && cashExplosion(pz, { label: 'Race prize' }) : gemExplosion(pz, { label: 'Race prize' }), 500);
  $('#roAgain').onclick = () => raceEnter(); $('#roBack').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
setInterval(() => { if (!S || !S.races || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on')) return; const now = Date.now();
  const k = Object.keys(S.races).find(sl => !S.races[sl].done && now >= Math.min((+sl + 1) * PP_MS, S.races[sl].at + PP_DEMO * 1.5)); if (k) raceOwnResult(+k); }, 3000);
"""+s[b:]
# results for players: say who won and that owners were paid
RA("<p class=\"pp-k\">🏅 Podium Pick · ${esc(crownName(g.k))} · results</p>",
   "<p class=\"pp-k\">🏇 The ${raceName(g.sl)} race · ${esc(crownName(g.k))} · results</p><p class=\"pp-win\">🏆 Won by <b>“${esc(g.ph[g.ord[0]].t)}”</b> · @${esc(g.ph[g.ord[0]].h)}<small>Photo owners won ${ownTxt(e.cur === 'cash')}</small></p>")
RA("cashExplosion(prize, { label: 'Podium Pick' }) : gemExplosion(prize, { label: 'Podium Pick' })","cashExplosion(prize, { label: 'Hourly race' }) : gemExplosion(prize, { label: 'Hourly race' })")
# Tournaments row -> race card
RA("${e ? 'IN ✓' : '🏅 PODIUM'}","${e ? 'IN ✓' : '🏇 RACE'}")
RA('<span class="tsr2-n"><small>Pick top 3</small></span>','<span class="tsr2-n"><small>${raceName(g.sl)} race</small></span>')
RA("if (e.target.closest('#ppRow')) { e.preventDefault(); e.stopPropagation(); ppOpen(); }","if (e.target.closest('#ppRow')) { e.preventDefault(); e.stopPropagation(); raceCard(); }")
# Coming up line
RA("return { ic: '🏅', t: `<b>Podium Pick · ${esc(crownName(g.k))}</b> · pick the top 3`","return { ic: '🏇', t: `<b>The ${raceName(g.sl)} race · ${esc(crownName(g.k))}</b> · pick the top 3`")
s=s.replace('</style>',""".pp-t{display:flex;flex-direction:column}.pp-im{position:relative;display:block}.pp-cap{display:flex;align-items:center;justify-content:space-between;gap:4px;padding:4px 5px 5px;font-size:.72rem}.pp-cap>b{font-weight:900}
.rf{display:inline-flex;gap:2px;align-items:center}.rf b{display:inline-grid;place-items:center;min-width:15px;height:15px;border-radius:4px;font-size:.66rem;font-weight:900;background:rgba(127,127,127,.18)}.rf b.f1{background:#F2C14E;color:#3B2A00}.rf b.f2{background:#C9CED6;color:#222}.rf b.f3{background:#D99A5B;color:#2A1600}.rf i{font-size:.66rem;font-weight:800;font-style:normal;opacity:.75}
.pp-leg{margin:0 0 6px;font-size:.72rem;opacity:.8}.pp-win{margin:2px 0 8px;font-size:.95rem}.pp-win small{display:block;font-size:.76rem;opacity:.8;margin-top:2px}
.rb{text-align:left;margin:0 0 8px;border-radius:14px;padding:8px}.rb-h{margin:0 0 6px;font-size:.78rem;font-weight:800;display:flex;align-items:center;gap:8px}.rb-live{color:#fff;background:#E5383B;border-radius:6px;padding:1px 6px;font-size:.66rem;letter-spacing:.08em;animation:unGlow 1.4s infinite}
.rb-r{display:grid;grid-template-columns:18px 40px 1fr auto;gap:8px;align-items:center;padding:4px 0}.rb-n{text-align:center;font-weight:900}.rb-r img{width:40px;height:40px;object-fit:cover;border-radius:9px}.rb-t{position:relative;min-width:0;padding-bottom:7px}.rb-t b{display:block;font-size:.85rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rb-t small{font-size:.7rem;opacity:.8}
.rb-t i{position:absolute;left:0;bottom:0;height:4px;border-radius:3px;background:#FBC20A;transition:width .8s}.rb-r em{font-style:normal;font-weight:900;font-size:.82rem}.rb-r.me .rb-t b{color:#2EA36B}
.rc-l{text-align:left;margin:0 0 10px}.rc-cols{display:grid;grid-template-columns:1fr 78px 58px;gap:6px;margin:0 0 2px;font-size:.62rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;opacity:.7}.rc-cols span:first-child{padding-left:50px}
.rc-r{display:grid;grid-template-columns:42px 1fr 78px 58px;gap:8px;align-items:center;padding:5px 0;border-top:1px solid rgba(127,127,127,.18)}.rc-r img{width:42px;height:42px;object-fit:cover;border-radius:9px}.rc-t{min-width:0}.rc-t b{display:block;font-size:.85rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rc-t small{font-size:.7rem;opacity:.8}
.rc-r em{position:relative;font-style:normal;font-weight:900;font-size:.82rem;text-align:right;padding-bottom:5px}.rc-r em i{position:absolute;right:0;bottom:0;height:3px;border-radius:2px;background:#FBC20A}.rc-r.me{background:rgba(46,163,107,.12);border-radius:10px}
.rc-sec{margin:12px 0 4px;text-align:left;font-size:.68rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;opacity:.75}.rc-nx{text-align:left;padding:6px 0;border-top:1px solid rgba(127,127,127,.18)}.rc-nx p{margin:0 0 4px;font-size:.85rem;display:flex;gap:6px;align-items:baseline}.rc-nx small{margin-left:auto;font-size:.72rem;opacity:.75}
.rc-nx div{display:grid;grid-template-columns:repeat(5,1fr);gap:5px}.rc-nx img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:8px}.rc-nx img.me{box-shadow:0 0 0 2px #2EA36B}
.rc-own{margin:12px 0 4px;padding:10px 12px;border-radius:14px;text-align:left}.rc-own>b{display:block;font-size:1rem}.rc-own>span{display:block;font-size:.82rem;margin:2px 0 8px}.rc-mine{margin:0 0 6px;font-size:.8rem}.rc-own .btn{margin:0!important}
.re-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 8px}.re-t{border:0;padding:0 0 6px;border-radius:14px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:1px}.re-t img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;margin-bottom:4px}.re-t b{font-size:1rem}.re-t small{font-size:.7rem;font-weight:800}.re-t.off{opacity:.55}
.re-ok{position:relative;width:120px;margin:4px auto 8px}.re-ok img{width:120px;height:120px;object-fit:cover;border-radius:18px;display:block}.re-ok i{position:absolute;right:-12px;top:-12px;font-style:normal;font-size:2.6rem;filter:drop-shadow(0 2px 4px rgba(0,0,0,.4))}
.rc-fin{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin:4px 0 12px}.rc-fin span{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.78rem}.rc-fin img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:9px}.rc-fin span.me img{box-shadow:0 0 0 3px #2EA36B}
html:not(.yg) .rb,html:not(.yg) .rc-own{background:#F3ECDF}html:not(.yg) .re-t{background:#F3ECDF;color:#2B2320}html:not(.yg) .rc-l,html:not(.yg) .rc-nx,html:not(.yg) .pp-leg,html:not(.yg) .pp-win,html:not(.yg) .rc-sec,html:not(.yg) .rc-own,html:not(.yg) .rb{color:#2B2320}html:not(.yg) .pp-cap{color:#2B2320}html:not(.yg) .pp-win b{color:#2F6B3F}
html.yg .rb,html.yg .rc-own{background:#2A1A52}html.yg .re-t{background:#2A1A52;color:#fff}html.yg .rc-l,html.yg .rc-nx,html.yg .pp-leg,html.yg .pp-win,html.yg .rc-sec,html.yg .rc-own,html.yg .rb,html.yg .pp-cap{color:#E9E2FF}html.yg .pp-win b{color:#2EE59D}html.yg .rb-r.me .rb-t b{color:#2EE59D}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('race ok')

# ---------- Heats: photos earn form in voter-decided heats, top 3 qualifies for an hourly race; My stable; status on Touch-ups; Coming up; notifications ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# race runner form comes from the photo's own record
RA("form: (S.raceHist || []).slice(-4), mine: 1 };","form: rcRec(mp.id).f.map(x => x.pl).slice(-4), mine: 1 };")
# replace direct race entry + owner result with the heats flow
a=s.index("function raceEnter() {"); b=s.index("setInterval(() => { if (!S || !S.races || $('#coach').classList.contains('on')")
s=s[:a]+r"""var HEAT_EVERY = 6, HEAT_WIN = 10;
function rcRec(id) { S.rc = S.rc || {}; return S.rc[id] = S.rc[id] || { st: null, f: [] }; }
function rcName(p) { return p.title || `${crownName(p.cat || 'any')} photo`; }
const rcStr = p => Math.min(.95, Math.max(.3, ((p.s && p.s.total) || 80) / 100 * 1.6 - .64));
const rcSlotFor = p => { const cur = ppSlot(), R = S.races || {}, ks = CATS8.filter(k => k !== 'any'); for (let sl = cur + 1; sl <= cur + ks.length; sl++) if (!R[sl] && fitsTheme(p, ks[sl % ks.length])) return sl; for (let sl = cur + 1; ; sl++) if (!R[sl]) return sl; };
function rcStatus(p) { const r = rcRec(p.id), last = r.last, hs = r.f.filter(x => x.k === 'h').slice(-3).map(x => ppOrd(x.pl)).join(' · '), y = isYoungW();
  if (r.st === 'q') { const x = (S.races || {})[r.sl]; return { cls: 'q', ic: '✅', t: `Qualified · runs in the <b>${raceName(r.sl)}</b> race`, s: x && r.sl === ppSlot() ? 'Racing now' : `Result ${x ? frTime(Math.min((r.sl + 1) * PP_MS, x.at + PP_DEMO * 1.5)) : ''} <small>(demo)</small>` }; }
  if (r.st === 'heats') return { cls: 'h', ic: '🏇', t: hs ? `Heats: ${hs}` : 'In the heats', s: `Next heat in <b>${Math.max(1, HEAT_EVERY - (S.hN || 0))}</b> ${y ? 'judge' : 'vote'}s · top 3 qualifies` };
  if (p.s.total < FR_MIN) return { cls: 'low', ic: '🔒', t: `Needs ${FR_MIN}+ to race`, s: `${y ? 'Enhance' : 'Touch up'} +${FR_MIN - p.s.total} to enter the heats` };
  if (last) return { cls: 'w', ic: last.pl <= 3 ? PP_MED[last.pl - 1] : '🏁', t: last.pz ? `Won <b>${last.cash ? money(last.pz) : last.pz + ' 🟡'}</b> in the ${raceName(last.sl)} race` : `${ppOrd(last.pl)} in the ${raceName(last.sl)} race`, s: 'Enter the heats again to race' };
  return { cls: 'n', ic: '📷', t: 'Not racing yet', s: `Enter the heats free · top 3 win ${isCash() ? 'cash' : 'coins'}` }; }
function stableOpen() { const P = (S.photos || []).slice().sort((a, b) => b.s.total - a.s.total), y = isYoungW(), cash = isCash();
  if (!P.length) { popClose(); toast('Add a photo first, then race it.'); pickPhoto(true); return; }
  popOpen(`<div class="pp st"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 My stable</p><h2 class="pp-h">Your photos</h2>
    <p class="pp-m">Heats are free. Top 3 in a heat qualifies for an hourly race. Race top 3 win <b>${ownTxt(cash)}</b>.</p>
    <div class="st-l">${P.map(p => { const r = rcRec(p.id), x = rcStatus(p), f = r.f.map(z => z.pl), can = !r.st && p.s.total >= FR_MIN;
      return `<div class="st-r ${x.cls}"><img src="${p.src}" alt=""><div class="st-t"><b>${esc(rcName(p))} <em>${p.s.total}</em></b><span>${x.ic} ${x.t}</span><small>${x.s}</small>${f.length ? `<span class="rf">${formHTML(f)}</span>` : ''}</div>
        ${can ? `<button class="btn st-go" data-heat="${p.id}">Enter heats<small>free</small></button>` : r.st === 'q' ? `<button class="btn st-go st-w" data-rcw="${r.sl}">${r.sl === ppSlot() ? '🔴 Watch' : 'Race card'}</button>` : ''}</div>`; }).join('')}</div>
    <p class="pp-r">${y ? 'Judges' : 'Voters'} decide every heat and race. Heat winners get ${HEAT_WIN} 🟡. You can’t pick in a race your own photo is in.</p>
    <div style="text-align:center"><button class="link pc-later" id="stCard">🏇 Race card</button> · <button class="link pc-later" id="stUp">＋ Add a photo</button></div></div>`);
  document.querySelectorAll('#coach [data-heat]').forEach(b => b.onclick = () => { const r = rcRec(b.dataset.heat); r.st = 'heats'; S.hN = Math.max(S.hN || 0, HEAT_EVERY - 2); save(); toast(`🏇 In the heats! First heat in ${HEAT_EVERY - S.hN} ${y ? 'judge' : 'vote'}s.`); stableOpen(); });
  document.querySelectorAll('#coach [data-rcw]').forEach(b => b.onclick = () => +b.dataset.rcw === ppSlot() ? ppOpen() : raceCard());
  $('#stCard').onclick = () => raceCard(); $('#stUp').onclick = () => { popClose(); pickPhoto(true); }; document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function raceEnter() { stableOpen(); }
function rcHeat() { const ids = (S.photos || []).filter(p => rcRec(p.id).st === 'heats').map(p => p.id); if (!ids.length) return;
  const id = ids.sort((a, b) => (rcRec(a).ha || 0) - (rcRec(b).ha || 0))[0], p = S.photos.find(x => x.id === id), r = rcRec(id), q = cpRng(Date.now() % 1e6);
  const me = rcStr(p) + (q() - .5) * .5, pl = 1 + [0, 1, 2, 3].filter(() => .3 + q() * .6 + (q() - .5) * .5 > me).length; r.ha = Date.now(); r.f.push({ k: 'h', pl }); r.f = r.f.slice(-12);
  if (pl === 1) { S.gems = (S.gems || 0) + HEAT_WIN; setTimeout(paintGems, 100); }
  if (pl <= 3) { const sl = rcSlotFor(p); S.races = S.races || {}; S.races[sl] = { pid: id, at: Date.now() }; r.st = 'q'; r.sl = sl; S.rcPop = { k: 'q', pid: id, pl, sl }; }
  else toast(`🏇 ${rcName(p)} finished ${ppOrd(pl)} in a heat. Next heat in ${HEAT_EVERY} votes.`);
  save(); }
function rcQualPop(x) { const p = (S.photos || []).find(z => z.id === x.pid); if (!p) return; const cash = isCash(), y = isYoungW(), g = ppGame(x.sl);
  popOpen(`<div class="pp"><p class="pp-k">🏇 Heat result</p><div class="re-ok"><img src="${p.src}" alt=""><i>${PP_MED[x.pl - 1]}</i></div><h2 class="pp-h">Qualified!</h2>
    <p class="pp-m"><b>${esc(rcName(p))}</b> finished ${ppOrd(x.pl)} in its heat${x.pl === 1 ? ` · +${HEAT_WIN} 🟡` : ''}</p>
    <p class="pp-i">It runs in the <b>${raceName(x.sl)} ${esc(crownName(g.k))} race</b>. Top 3 win <b>${ownTxt(cash)}</b>.<br><small>(demo: result in about 3 min)</small></p>
    <button class="btn block pc-go" id="qpOk">${y ? 'Keep judging' : 'Keep voting'}</button><div style="text-align:center"><button class="link pc-later" id="qpSt">🏇 My stable</button></div></div>`);
  $('#qpOk').onclick = () => popClose(); $('#qpSt').onclick = () => stableOpen(); }
function raceOwnResult(sl) { const x = S.races[sl], g = ppGame(sl), i = g.ph.findIndex(p => p.mine), cash = isCash(), y = isYoungW();
  const pl = i < 0 ? 5 : g.ord.indexOf(i) + 1, pz = pl <= 3 ? RACE_OWN[cash ? 'cash' : 'gems'][pl - 1] : 0, amt = cash ? money(pz) : `${pz.toLocaleString()} 🟡`;
  const ph = i >= 0 ? g.ph[i] : { src: '', t: 'Your photo' }, r = rcRec(x.pid); r.f.push({ k: 'r', pl }); r.f = r.f.slice(-12); r.st = null; r.sl = null; r.last = { sl, pl, pz, cash: cash ? 1 : 0 }; x.done = 1; x.place = pl; x.prize = pz;
  if (pz) { if (cash) { S.cash = +((S.cash || 0) + pz).toFixed(2); paintWallet(); } else { S.gems += pz; paintGems(); } } save();
  popOpen(`<div class="pp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏇 The ${raceName(sl)} race · ${esc(crownName(g.k))} · result</p>
    <div class="re-ok">${ph.src ? `<img src="${ph.src}" alt="">` : ''}${pl <= 3 ? `<i>${PP_MED[pl - 1]}</i>` : ''}</div>
    <h2 class="pp-h">${esc(ph.t)} finished ${ppOrd(pl)}${pl <= 3 ? '!' : ''}</h2>
    <p class="pp-m">${pz ? `You won <b>${amt}</b>` : 'Top 3 win prizes.'} · form <span class="rf">${formHTML(r.f.map(z => z.pl))}</span></p>
    <div class="rc-fin">${g.ord.map((j, n) => `<span class="${g.ph[j].mine ? 'me' : ''}"><img src="${g.ph[j].src}" alt=""><b>${n < 3 ? PP_MED[n] : ppOrd(n + 1)}</b></span>`).join('')}</div>
    <button class="btn block pc-go" id="roAgain">🏇 Back to the heats · free</button><div style="text-align:center"><button class="link pc-later" id="roBack">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  if (pz) setTimeout(() => cash ? cashExplosion && cashExplosion(pz, { label: 'Race prize' }) : gemExplosion(pz, { label: 'Race prize' }), 500);
  $('#roAgain').onclick = () => { r.st = 'heats'; save(); toast('🏇 Back in the heats!'); stableOpen(); }; $('#roBack').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
setInterval(() => { if (!S || !S.rcPop || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on')) return; const x = S.rcPop; S.rcPop = null; save(); rcQualPop(x); }, 1500);
setInterval(() => { if (!S || !S.races) return; const cur = ppSlot(); Object.entries(S.races).forEach(([sl, x]) => { if (+sl === cur && !x.done && !x.on) { x.on = 1; save(); toast('🔴 Your photo is racing now! Watch it live.'); } }); }, 5000);
"""+s[b:]
# heats run as people vote
RA("S.votes++; S.cpN = (S.cpN || 0) + 1;","S.votes++; S.cpN = (S.cpN || 0) + 1; if (S.rc && Object.values(S.rc).some(r => r.st === 'heats')) { S.hN = (S.hN || 0) + 1; if (S.hN >= HEAT_EVERY) { S.hN = 0; setTimeout(rcHeat, 0); } }")
# race card: owner section becomes the stable
a=s.index('<div class="rc-own"><b>📷 Race your photo, free</b>'); b=s.index('</div>', s.index('id="rcEnter"', a))+6
s=s[:a]+r"""<div class="rc-own"><b>📷 Race your photos, free</b><span>Top 3 in a heat qualifies. Race top 3 win <b>${ownTxt(cash)}</b><br>Photos need ${FR_MIN}+ · entry is free</span>${(() => { const P = (S.photos || []), h = P.filter(p => rcRec(p.id).st === 'heats').length, q = P.filter(p => rcRec(p.id).st === 'q').length; return h || q ? `<p class="rc-mine">${q ? `✅ <b>${q}</b> qualified` : ''}${q && h ? ' · ' : ''}${h ? `🏇 <b>${h}</b> in the heats` : ''}</p>` : ''; })()}${mine}<button class="btn block pc-real" id="rcEnter">🏇 My stable</button></div>"""+s[b:]
# Coming up: your race result soon, or your next heat (counts down in votes)
RA("{ const g = ppGame(), m = Math.ceil((g.end - Date.now()) / 60000); if (S.potSeen",
   "{ const R = Object.entries(S.races || {}).filter(([sl, x]) => !x.done).map(([sl, x]) => ({ sl: +sl, x, due: Math.min((+sl + 1) * PP_MS, x.at + PP_DEMO * 1.5) })).sort((a, b) => a.due - b.due)[0];\n    if (R && R.due - Date.now() < 3600e3) { const p = (S.photos || []).find(z => z.id === R.x.pid); if (p) return { ic: '🏇', t: `<b>${esc(rcName(p))}</b> · ${R.sl === ppSlot() ? 'racing now' : `the ${raceName(R.sl)} race`}`, k: 'r', need: 0, per: 1, em: R.sl === ppSlot() ? '🔴 Live' : `result in ${Math.max(1, Math.ceil((R.due - Date.now()) / 60000))} min` }; } }\n  if (S.rc && S.photos) { const hp = S.photos.find(p => rcRec(p.id).st === 'heats'); if (hp) it.push({ ic: '📷', t: `<b>${esc(rcName(hp))}</b> · next heat`, k: 'h', need: Math.max(1, HEAT_EVERY - (S.hN || 0)), per: HEAT_EVERY }); }\n  { const g = ppGame(), m = Math.ceil((g.end - Date.now()) / 60000); if (S.potSeen")
RA("if (x.k === 'p') { ppOpen(); return; }","if (x.k === 'p') { ppOpen(); return; } if (x.k === 'r' || x.k === 'h') { stableOpen(); return; }")
RA("<em>${x.k === 'p' ?","<em>${x.em ? x.em : x.k === 'p' ?")
# Quick Pick is a qualifying heat
RA("<p class=\"pp-k\">🏅 Podium Pick${pool.length >= 5 ? ` · ${esc(crownName(k))}` : ''} · vs @${esc(opp)}</p>","<p class=\"pp-k\">🏅 Podium Pick · qualifying heat${pool.length >= 5 ? ` · ${esc(crownName(k))}` : ''} · vs @${esc(opp)}</p>")
RA("<p class=\"pp-r\">The crowd has already judged these photos. Higher score wins · tie goes to the faster player.</p>","<p class=\"pp-r\">${isYoungW() ? 'Judges' : 'Voters'} already ranked this heat. Its top 3 qualify for an hourly race. Higher score wins · tie goes to the faster player.</p>")
# Touch-ups: racing status under the photo
RA("if (window.__sdWhy) h.insertAdjacentHTML('beforeend', `<p class=\"sd-why\">${window.__sdWhy}</p>`);",
   "if (window.__sdWhy) h.insertAdjacentHTML('beforeend', `<p class=\"sd-why\">${window.__sdWhy}</p>`); { const p = cur(), x = p && rcStatus(p); if (x) { h.insertAdjacentHTML('beforeend', `<button class=\"sd-rc ${x.cls}\" id=\"sdRc\"><span>${x.ic}</span><span><b>${x.t}</b><small>${x.s}</small></span><i>›</i></button>`); $('#sdRc').onclick = () => stableOpen(); } }")
s=s.replace('</style>',""".st-l{text-align:left;margin:0 0 8px}.st-r{display:grid;grid-template-columns:56px 1fr auto;gap:10px;align-items:center;padding:8px 0;border-top:1px solid rgba(127,127,127,.18)}.st-r>img{width:56px;height:56px;object-fit:cover;border-radius:12px}
.st-t{min-width:0;display:flex;flex-direction:column;gap:1px}.st-t>b{font-size:.92rem}.st-t>b em{font-style:normal;font-size:.72rem;font-weight:900;padding:1px 6px;border-radius:6px;background:rgba(127,127,127,.18);margin-left:4px}.st-t>span{font-size:.82rem}.st-t>small{font-size:.72rem;opacity:.8}.st-t .rf{margin-top:3px}
.st-go{margin:0!important;padding:8px 10px!important;font-size:.8rem!important;line-height:1.1!important;min-height:0!important;width:auto!important;text-transform:none!important;display:flex!important;flex-direction:column;align-items:center}.st-go small{font-size:.66rem;opacity:.85}.st-r.q{background:rgba(46,163,107,.1);border-radius:12px}
.sd-rc{display:flex;align-items:center;gap:10px;width:100%;margin:8px 0 0;padding:9px 12px;border:0;border-radius:14px;text-align:left;cursor:pointer;font:inherit}.sd-rc>span:first-child{font-size:1.3rem}.sd-rc>span:nth-child(2){flex:1;display:flex;flex-direction:column;font-size:.85rem;line-height:1.25}.sd-rc small{font-size:.74rem;opacity:.8}.sd-rc i{font-style:normal;font-size:1.3rem;opacity:.6}
html:not(.yg) .st-l,html:not(.yg) .st-t{color:#2B2320}html:not(.yg) .st-go{background:#2F6B3F!important;color:#fff!important}html:not(.yg) .st-go.st-w{background:#2D4E86!important}html:not(.yg) .sd-rc{background:#F3ECDF;color:#2B2320;box-shadow:inset 0 0 0 1.5px #E6D9C4}html:not(.yg) .sd-rc.q{background:#E5F2E8;box-shadow:inset 0 0 0 1.5px #2F6B3F}
html.yg .st-l,html.yg .st-t{color:#E9E2FF}html.yg .st-go{background:#2EE59D!important;color:#14092B!important}html.yg .st-go.st-w{background:#C13CFF!important;color:#fff!important}html.yg .sd-rc{background:#2A1A52;color:#fff;box-shadow:inset 0 0 0 1.5px #3A2766}html.yg .sd-rc.q{box-shadow:inset 0 0 0 1.5px #2EE59D}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('heats ok')

