# Skill only: the Freeroll is replaced by a free cash challenge ($1, once an hour).
# 300 coins (earned by voting, never sold) = one real $1 photo challenge, free, once an hour.
# A quick 1 v 1: a win pays $1.60 real cash straight away (we fund it only when the player wins). No stars, no pot.
# Run by simplify.py unless YOFI_BUILD=real.
import re
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
s=s.replace("function fcNotify() {",r"""const FC_COINS = 300;
const fcReady = () => S.fcDay !== frHourKey();
const fcRowHTML = () => { if (!S || S.geoBlock) return ''; const r = fcReady(), ok = r && (S.gems || 0) >= FC_COINS;
  return `<button class="tsr2 fcrow ${ok ? 'can' : 'need'}" id="fcRow"><span class="tsr2-t"><span class="fr-tag fc-tag">FREE CASH CHALLENGE</span><b>${r ? 'Ready' : frMinsLeft() + 'm'}</b></span><span class="tsr2-p">$1</span><span class="tsr2-n"><small>${r ? '1 an hour' : 'Used'}</small></span><span class="tsr2-e">${ok ? `${FC_COINS} 🟡` : `🔒 ${FC_COINS} 🟡`}</span></button>`; };
const FC_PRIZE = 1.6, FC_N = 15;
function freeCh() { if ($('#sheet').classList.contains('on')) closeSheet(); const y = isYoungW(), keep = $('#panes').dataset.at === 'judge' ? (y ? 'Keep judging' : 'Keep voting') : 'Not now';
  if (!fcReady()) { popOpen(`<div class="pc pc2 fc2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pc-k"><span>🎟️ Free cash ${y ? 'battle' : 'challenge'}</span></p><h2 class="pc-h">Next one in ${frMinsLeft()} min</h2>
      <p class="fch-m">You’ve had this hour’s free cash ${y ? 'battle' : 'challenge'}. A new one opens every hour.</p>
      <button class="btn block pc-go" id="fcOk">${keep}</button><div style="text-align:center"><button class="link pc-later fc-test" id="fcReset">↺ Reset for testing</button></div></div>`);
    $('#fcOk').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#fcReset').onclick = () => { S.fcDay = null; if ((S.gems || 0) < FC_COINS) S.gems = FC_COINS; save(); paintGems(); toast('Free cash challenge reset (test)'); freeCh(); }; return; }
  const ks = CATS8.filter(k => lgMine(k)).sort((a, b) => (a === 'any') - (b === 'any'));
  if (!ks.length) { toast(`Get a photo to ${CFG.QUALIFY}+ first, then play free.`); pickPhoto(true); return; }
  const k = ks[0], me = lgMine(k), L = lgS(), P = L.pl.filter(p => p.sc && p.sc[k]), O = P[Math.floor(Math.random() * P.length)] || L.pl[0], opp = O.h, their = (O.sc && O.sc[k]) || 80, osrc = lgPhoto(opp, k);
  const can = (S.gems || 0) >= FC_COINS, cn = esc(crownName(k)), CH = y ? 'battle' : 'challenge';
  const vs = (a, b, done, won) => `<div class="pc-vs pc2-vs fc-vs"><figure class="${done && won ? 'won' : ''}"><img src="${me.src}" alt=""><figcaption>You</figcaption><small>Score ${me.s.total}</small>${a != null ? `<strong class="fc-n" id="fcA">${a}</strong>` : ''}</figure><span class="pc-x2">VS</span>
    <figure class="${done && !won ? 'won' : ''}"><img src="${osrc}" alt=""><figcaption>@${esc(opp)}</figcaption><small>Score ${their}</small>${b != null ? `<strong class="fc-n" id="fcB">${b}</strong>` : ''}</figure></div>`;
  popOpen(`<div class="pc pc2 fc2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pc-k">${gi(k)}<span>Free cash ${CH} · ${cn}</span></p><h2 class="pc-h">Win ${money(FC_PRIZE)} real cash</h2>
    <div class="pc2-pool"><b>${money(FC_PRIZE)}</b><span>winner gets, paid straight away<em>A real $1 ${CH}, free with ${FC_COINS} 🟡</em></span></div>
    ${vs()}
    <div class="pc2-stake"><div class="w"><b>Win</b><span>${money(FC_PRIZE)} cash in your wallet now</span></div><div class="l"><b>Lose</b><span>nothing lost · next free one in an hour</span></div></div>
    <button class="btn block pc-go" id="fcGo" ${can ? '' : 'disabled'}>🎟️ Play free · ${FC_COINS} 🟡</button>
    <p class="fch-r">${can ? `One an hour. Coins are earned by ${y ? 'judging' : 'voting'}, never sold.` : `You need <b>${(FC_COINS - Math.floor(S.gems || 0)).toLocaleString()} more 🟡</b>. ${y ? 'Judge' : 'Vote'} to earn them.`}</p>
    <div style="text-align:center"><button class="link pc-later" id="fcNo">${keep}</button></div></div>`);
  const bindX = () => document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
  $('#fcNo').onclick = () => popClose(); bindX();
  $('#fcGo').onclick = () => { if (S.user && S.user.guest) { popClose(); openSignup(() => freeCh(), { locked: false }); return; } if ((S.gems || 0) < FC_COINS || !fcReady()) return;
    S.gems -= FC_COINS; S.fcDay = frHourKey(); save(); paintGems();
    const pWin = Math.max(.25, Math.min(.75, .5 + (me.s.total - their) / 30)), won = Math.random() < pWin, mv = won ? 8 + Math.floor(Math.random() * 3) : 4 + Math.floor(Math.random() * 4);
    const seq = [...Array(FC_N)].map((_, i) => i < mv); for (let i = FC_N - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [seq[i], seq[j]] = [seq[j], seq[i]]; }
    if (won) { S.cash = +((S.cash || 0) + FC_PRIZE).toFixed(2); } S.fcLog = (S.fcLog || []).concat({ at: Date.now(), k, won: won ? 1 : 0 }).slice(-20); save();
    popOpen(`<div class="pc pc2 fc2"><p class="pc-k">${gi(k)}<span>Free cash ${CH} · ${cn}</span></p><h2 class="pc-h" id="fcH">Live voting…</h2>${vs(0, 0)}
      <div class="kg2-bar fc-bar"><i id="fcAb" style="width:50%"></i><i id="fcBb" style="width:50%"></i></div><p class="fch-r" id="fcV">0 of ${FC_N} votes</p></div>`);
    const result = () => { const d = Math.abs(mv - (FC_N - mv)), iHold = lgHold(k).h === 'you';
      popOpen(`<div class="pc pc2 fc2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pc-k">${gi(k)}<span>Free cash ${CH} · ${cn}</span></p>
        <h2 class="pc-h">${won ? `You won ${money(FC_PRIZE)}!` : `Lost by ${d} vote${d === 1 ? '' : 's'}`}</h2>
        ${vs(mv, FC_N - mv, true, won)}
        ${won ? `<div class="pc2-pool fc-won"><b>+${money(FC_PRIZE)}</b><span>real cash, in your wallet now<em>Yours to keep. Add cash any time to play for more</em></span></div>` : `<p class="fch-m">Next free ${CH} in <b>${frMinsLeft()} min</b>. Or play a real one now.</p>`}
        <button class="btn block pc-real" id="fcReal">💵 ${won ? `Play a $${LG_FEE} cash ${CH}` : `Play for real · $${LG_FEE}`}</button>
        <div style="text-align:center"><button class="link pc-later" id="fcNo">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
      if (won) setTimeout(() => { try { cashExplosion(FC_PRIZE, { label: 'Free cash ' + CH }); } catch (e) {} paintWallet(); }, 400);
      $('#fcReal').onclick = () => { popClose(); const o2 = iHold ? (lgRank(k).find(r => !r.me) || {}).h : lgHold(k).h; payCash(LG_FEE, 'A challenge', () => lgFight(k, o2, !iHold)); };
      $('#fcNo').onclick = () => popClose(); bindX(); };
    let v = 0, m = 0; const iv = setInterval(() => { if (!$('#fcV')) { clearInterval(iv); return; } if (seq[v]) m++; v++; const sh = m / v * 100;
      $('#fcAb').style.width = sh + '%'; $('#fcBb').style.width = (100 - sh) + '%'; $('#fcA').textContent = m; $('#fcB').textContent = v - m; $('#fcV').textContent = `${v} of ${FC_N} votes`;
      if (v < FC_N) return; clearInterval(iv); setTimeout(result, 600); }, 380);
  }; }
const fcShopHTML = () => { const r = fcReady(), ok = r && (S.gems || 0) >= FC_COINS, y = isYoungW(); return `<button class="ug-r ug-swap fc-shop" id="fcShop"><span class="ug-i">🎟️</span><span class="ug-t"><b>Free $1 cash ${y ? 'battle' : 'challenge'}</b><small>${r ? `No cash needed · 1 an hour` : `Used · next one in ${frMinsLeft()} min`}</small></span><em class="${ok ? '' : 'need'}">${FC_COINS} 🟡</em></button>`; };
document.addEventListener('click', e => { if (e.target.closest('#fcRow, #fcShop, #tshTix, #ugSwap, [data-frrow]')) { e.preventDefault(); e.stopPropagation(); freeCh(); } }, true);
function fcNotify() {""",1)
# coin players: no star/pot challenges (no coin pot screen anywhere). Their challenge pops alternate:
# instant coin challenge (25 in, win 50) and the free cash challenge when it's ready.
RA("function openBattle() {", "function openBattle() { if (!isCash() && !S.potSeen) { S.potSeen = 1; save(); }")
RA("S.btAlt = !S.btAlt; save();", "S.btAlt = !S.btAlt; if (!isCash()) { S.btAlt = false; } save();")
RA("if (!S.potSeen) { const pp = fighters()[0]", "if (!S.potSeen && isCash()) { const pp = fighters()[0]")
RA("else if (S.btAlt) { if (!S.nextBth", "else if (S.btAlt || !isCash()) { if (!S.nextBth")
# coin prices (Skill): coin challenge 100 in / win 200, Quick Sprint 250 in / win 400, free cash challenge 500
RA("const FC_COINS = 300;", "const FC_COINS = 500, CC_COIN = 100;")
RA("const QS_COIN = 100, QS_COIN_PAY = [160];", "const QS_COIN = 250, QS_COIN_PAY = [400];")
RA("openGemBattle(25)", "openGemBattle(CC_COIN)", 3)
RA("openGemBattle(25, null, { theme: bth })", "openGemBattle(CC_COIN, null, { theme: bth })")
RA("Stake <b>25 🟡</b>, win <b>50 🟡</b>", "Stake <b>${CC_COIN} 🟡</b>, win <b>${CC_COIN * 2} 🟡</b>")
RA("Free challenge · 25 🟡", "Free challenge · ${CC_COIN} 🟡")
RA("'Free challenge · ${CC_COIN} 🟡'", "`Free challenge · ${CC_COIN} 🟡`")
RA("for <b>50 🟡</b>", "for <b>${CC_COIN * 2} 🟡</b>")
RA("win 50 🟡`, k: 'b' }", "win ${CC_COIN * 2} 🟡`, k: 'b' }")
RA("Win <b>50 🟡</b> in 30 seconds.`, cost: 25, src: f.src, go: () => { closeSheet(); openGemBattle(CC_COIN); } });",
   "Win <b>${CC_COIN * 2} 🟡</b> in 30 seconds.`, cost: CC_COIN, src: f.src, go: () => { closeSheet(); openGemBattle(CC_COIN); } });\n  I.unshift({ ic: '🎯', t: 'Quick Sprint', d: `1 v 1: pick the crowd’s choice in 10 photo pairs. Win <b>${QS_COIN_PAY[0]} 🟡</b>.`, cost: QS_COIN, src: (fighters()[0] || S.photos[0] || {}).src || '', go: () => { closeSheet(); sprPractice(); } });")
# testing only: a cash player can switch back to coin play from the cash menu
RA('const body = `<h3 class="sp-h">${head[0]}</h3><p class="sp-s">${head[1]}</p><div class="sp-list">`',
   'const body = `<h3 class="sp-h">${head[0]}</h3><p class="sp-s">${head[1]}</p>${T === \'cash\' && S.cashMode ? \'<div style="text-align:center;margin:-4px 0 10px"><button class="link fc-test" id="toCoin">↺ Back to coin play (testing)</button></div>\' : \'\'}<div class="sp-list">`')
s=s.replace("function fcNotify() {","document.addEventListener('click', e => { if (e.target.closest('#toCoin')) { e.preventDefault(); e.stopPropagation(); S.cashMode = 0; save(); try { closeSheet(); } catch (x) {} try { paintWallet(); paintGems(); paintMode(); } catch (x) {} if ($('#panes').dataset.at === 'judge') renderJudge(); toast('Back to coin play (test)'); } }, true);\nfunction fcNotify() {",1)
# testing tools in the account menu too
RA('<button class="link" id="mR" style="margin-top:6px">Reset prototype</button></div>`);',
   '<p class="pf-test">Testing</p>${S.cashMode ? \'<button class="btn quiet block" id="toCoin">↺ Back to coin play</button>\' : \'\'}<button class="btn quiet block" id="fcRst">↺ Reset free cash challenge</button>\n    <button class="link" id="mR" style="margin-top:6px">Reset prototype</button></div>`);')
s=s.replace("function fcNotify() {","document.addEventListener('click', e => { if (e.target.closest('#fcRst')) { e.preventDefault(); e.stopPropagation(); S.fcDay = null; if ((S.gems || 0) < FC_COINS) S.gems = FC_COINS; save(); try { closeSheet(); } catch (x) {} paintGems(); toast('Free cash challenge reset (test)'); } }, true);\nfunction fcNotify() {",1)
s=s.replace('</style>','#tshTix[hidden]{display:none!important}\n</style>',1)
s=s.replace('</style>','.pf-test{margin:14px 0 4px;font-size:.7rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase;opacity:.6;text-align:left}\n</style>',1)
# coin players: the add-a-photo screen talks about the coin challenge, not the blue ribbon or the cash pot
RA("to challenge for the ${esc(cn)} blue ribbon${L ? ` and today’s <b>${('$' + Math.round(L.jp[k]).toLocaleString())}</b> pot` : ''}.</p>",
   "to ${isCash() ? `challenge for the ${esc(cn)} blue ribbon${L ? ` and today’s <b>${('$' + Math.round(L.jp[k]).toLocaleString())}</b> pot` : ''}` : `play the ${esc(cn.toLowerCase())} coin ${isYoungW() ? 'battle' : 'challenge'} and win <b>${CC_COIN * 2} 🟡</b>`}.</p>")
# coin nudge: names the game; suggests the free cash challenge first when it's ready and affordable
RA("const x = I.find(i => S.gems >= i.cost) || I[0];\n  celebrate({ src: x.src, score: '🟡', title: `You’ve got ${Math.floor(S.gems).toLocaleString()} coins!`, text: `${x.d}<br>Use <b>${x.cost} 🟡</b> on it now.`, cta: '🟡 Use my coins', onCta: useGems, later: 'Later' });",
   "const x = I.find(i => S.gems >= i.cost) || I[0];\n  celebrate({ src: x.src, score: '🟡', title: `You’ve got ${Math.floor(S.gems).toLocaleString()} coins!`, text: `<b>${x.t}</b> · ${x.d}<br>Use <b>${x.cost} 🟡</b> on it now.`, cta: '🟡 Use my coins', onCta: useGems, later: 'Later' });")
# Challenge a friend: cash players see only cash entries, coin players only coins
RA("frGem = () => S.frSt === 'gem'", "frGem = () => !isCash()")
RA('${FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${!coin && x === st}">$${x}</button>`).join(\'\')}<button data-frs="gem" aria-pressed="${coin}">${FR_GEM} ${G}</button>',
   '${isCash() ? FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${x === st}">$${x}</button>`).join(\'\') : `<button data-frs="gem" aria-pressed="true">${FR_GEM} ${G}</button>`}')
RA('${FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${!frGem() && x === frSt()}">$${x}</button>`).join(\'\')}<button data-frs="gem" aria-pressed="${frGem()}">${FR_GEM} ${gemIcon(\'\')}</button>',
   '${isCash() ? FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${x === frSt()}">$${x}</button>`).join(\'\') : `<button data-frs="gem" aria-pressed="true">${FR_GEM} ${gemIcon(\'\')}</button>`}')
# every Freeroll door now opens the free cash challenge
RA("function swapTicket() {","function swapTicket() { freeCh(); return;")
RA("function frEnter(f) {","function frEnter(f) { freeCh(); return;")
# Tournaments: free cash challenge row instead of Freeroll rows; no Freerolls filter
RA('<div class="tsl2" data-tfl="${TF}">${chRowHTML()}${frRows}${rows}</div>','<div class="tsl2" data-tfl="${TF}">${chRowHTML()}${rows}</div>')
RA("const TF = window.__tFil || 'all',","const TF = (window.__tFil === 'fr' ? 'all' : window.__tFil) || 'all',")
RA("['fr', '🎟️ Freerolls'], ","")
a=s.index('<button class="tsh-tix tsh-fr" id="tshTix">'); b=s.index('</button>',a)
s=s[:a]+'<button class="tsh-tix tsh-fr" id="tshTix" hidden>'+s[b:]
a=s.index('<b>Enter a Freeroll</b><small>'); b=s.index('</button>`;',a)
s=s[:a]+'<b>Free $1 cash challenge</b><small>${fcReady() ? `${(S.gems || 0) >= FC_COINS ? \'No cash needed · 1 an hour\' : `${(FC_COINS - Math.floor(S.gems || 0)).toLocaleString()} more 🟡 needed · ${isYoungW() ? \'judge\' : \'vote\'} to earn them`}` : `Next one in ${frMinsLeft()} min`}</small></span><em class="${(S.gems || 0) < FC_COINS || !fcReady() ? \'need\' : \'\'}">${FC_COINS} 🟡</em>'+s[b:]
# photo reaches 80: point at the free cash challenge
a=s.index("title: 'Freeroll ready!'"); b=s.index("later: 'Later' })",a)
s=s[:a]+"title: 'Ready to play for real!', text: `Your photo reached <b>${tot}</b>. Tap your <b>coin balance</b> to use <b>${FC_COINS} coins</b> on a <b>free $1 cash challenge</b>, once an hour. Win <b>$1.60 real cash</b>.`, cta: '🟡 Open my coins', onCta: () => { closeFlow(); useGems(); }, "+s[b:]
# how it works + small texts
a=s.index("${T('t-fr'"); b=s.index("${T('t-ko'",a)
s=s[:a]+"${T('t-fr', '🎟️', 'Free cash challenge', 'From your coin balance', '🎟️ Free', [`Use <b>${FC_COINS} coins</b>, once an hour. Coins are earned by ${isYoungW() ? 'judging' : 'voting'}.`, 'A <b>real $1 challenge</b>: your photo against a rival, decided live by member votes.', 'Win and <b>$1.60 real cash</b> goes straight into your wallet.', 'You stay a coin player until you add cash.'])}\n    "+s[b:]
RA("Win coins to touch up photos and enter cash Freerolls.<br>","Win coins to touch up photos and play a free cash challenge.<br>")
# Coming up: tell coin players when a free cash challenge is ready
RA("return it.sort((p, q) => p.need - q.need)[0] || null; }",
   "return it.sort((p, q) => p.need - q.need)[0] || null; }")
RA("function upNow() { const x = upNext(); if (!x) return;","function upNow() { const x = upNext(); if (!x) return; if (x.k === 'f') { freeCh(); return; }")
s=s.replace('</style>',""".fch-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin:4px 0 10px}.fch-vs figure{margin:0;display:flex;flex-direction:column;gap:3px;align-items:center}.fch-vs img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:14px}.fch-vs small{font-size:.76rem;font-weight:800}.fch-vs>b{font-weight:900}
.fch-m{margin:0 0 10px;font-size:.92rem;line-height:1.4}.fch-r{margin:8px 0 2px;font-size:.78rem;opacity:.85}.fc-tag{background:#2F6B3F!important;color:#fff!important}html.yg .fc-tag{background:#21C77A!important;color:#0B1A12!important}
html:not(.yg) .tsr2.fcrow{background:#E8F3EA!important;box-shadow:inset 0 0 0 1.5px #2F6B3F!important}html.yg .tsr2.fcrow{background:#10301F!important;box-shadow:inset 0 0 0 1.5px #21C77A!important}
.tsr2.fcrow .tsr2-t{flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:2px!important}.tsr2.fcrow .fc-tag{display:inline-block!important;font-size:.56rem!important;font-weight:900!important;line-height:1.3!important;padding:2px 6px!important;border-radius:6px!important}.tsr2.fcrow .tsr2-n small{font-size:.72rem;font-weight:800}
html:not(.yg) .fch-m,html:not(.yg) .fch-r,html:not(.yg) .fch-vs{color:#2B2320}html.yg .fch-m,html.yg .fch-r,html.yg .fch-vs{color:#E9E2FF}
</style>""",1)
s=s.replace('</style>','.fc2 .fc-vs figure{position:relative}.fc2 .fc-n{display:block;font-size:1.6rem;font-weight:900;line-height:1.1;margin-top:2px}.fc2 .fc-vs figure.won img{box-shadow:0 0 0 4px #F2C14E}.fc-bar{margin:6px 0 4px}.fc-won b{color:#2EA36B!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('free cash challenge ok')
