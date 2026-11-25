# Vote screen layout (Skill preview). Runs after votegoal.py.
# Top: the goal bar. Middle: "Which is better?" with a small streak widget (dots to the next gift + the gift).
# Below the photos: cash games only - one card, chosen in this order:
#   1. a friend's challenge waiting for your answer ("@larry challenged you · $1 each · View matchup")
#   2. the champion of your best photo's category ("Can Milo beat @kim, the Pets champion? · $1 entry · $12.40 pot")
#   3. the next tournament ("Quick tournament · starts in 04:12 · $1 entry · $25 guaranteed")
#   Champion and tournament take turns between pairs; viewing is free, money is only taken on the entry button inside.
#   The "Head-to-head in N votes" line moves down under the card. The big Wins x1 / gift strip is hidden.
# Usage: python3 build-skill/votecash.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function vgGoal(' not in s: sys.exit('run votegoal.py first')
if 'function vcCard(' in s: sys.exit('vote cash already applied')

JS = r'''
/* ---------- vote: small streak + one cash card under the photos ---------- */
function vcStreak() {
  const c = S.combo || 0, ms = [3, 6, 10], nx = ms.find(m => c < m) || 10, pv = [0, ...ms].filter(m => m < nx).pop(), done = Math.min(c, 10) - pv, n = nx - pv;
  return `<button class="vcs${done >= n - 1 ? ' near' : ''}" id="vcStk" aria-label="Streak ${c}. ${c >= 10 ? 'Top reward reached' : `${nx - c} more crowd picks in a row for ×${nx} coins`}">${[...Array(n)].map((_, i) => `<i class="${i < done ? 'on' : ''}"></i>`).join('')}<span class="vcs-sep"></span><span class="vcs-g">🎁<small>×${nx}</small></span></button>`;
}
function vcCard() {
  const fr = S.fr && (S.fr.ch || []).find(c => c.st === 'yours');
  if (fr) return { img: fr.theirSrc, t: `@${fr.f} challenged you`, s: `${stakeTxt(fr.stake)} each · winner takes ${prizeTxt(fr.stake)}`, cta: 'View matchup', go: () => fcAccept(fr) };
  // every cash game takes a turn; games that need a 70+ photo are skipped until you have one
  const F = fighters(), best = F[0], T = tSlots()[0], nm = best ? (GAL.PATH.includes(best.cat) ? alName(best) : 'your photo') : '';
  // real-money games only (coin games live in the coin balance sheet); head-to-head nudges come round most often
  const h2h = best && (() => { const rv = battleRival(best.cat || 'any'); return { img: rv.src, t: `A rival challenged ${nm}`, s: `Head-to-head · $1 entry · win $${(2 * (1 - KING_FEE)).toFixed(2)}`, cta: 'View matchup', go: () => openCashBattle(1, null, best) }; });
  const G = [
    h2h,
    best && (() => { const cat = best.cat || 'any', K = kingOf(cat); return { img: K.src, t: `Beat the ${catLabel(cat)} champion`, s: `$1 entry · ${money(K.bounty)} pot`, cta: 'View matchup', go: () => openKing(cat) }; }),
    () => ({ art: '🏆', t: 'Quick tournament', when: T.at, s: `$1 entry · US$${T.gtd} prize`, cta: 'View tournament', go: () => openTourney() }),
    h2h,
    () => ({ art: '🎯', t: 'Quick Sprint', s: '1 v 1 · $2 entry · win $3.20', cta: 'View sprint', go: () => { window.__qsReal = 1; sprEnter(); } }),
    best && (() => ({ art: '⚡', t: '5-player Showdown', s: `$${SD_FEE} entry · winner takes ${money(sdPrize())}`, cta: 'View showdown', go: () => openShowdown() })),
    best && (() => ({ art: '🤝', t: 'Challenge a friend', s: `$1 each · winner takes ${money(fcPrize({ cur: 'cash', amt: 1 }))}`, cta: 'Pick a friend', go: () => fcNew() }))
  ].filter(Boolean);
  // changes every 3 votes
  S.vcTurn = Math.floor(((S.votes || 0) + (S.vcOff || 0)) / 3) % G.length;
  return G[S.vcTurn]();
}
function vcPaint() {
  const j = $('#judge'), card = j && j.querySelector('#jcard'); if (!card) return;
  const h = j.querySelector('.tot-h'); if (h && !h.querySelector('#vcStk')) { const t = h.querySelector('h2'); if (t) { const row = document.createElement('div'); row.className = 'vch'; t.replaceWith(row); row.appendChild(t); row.insertAdjacentHTML('beforeend', vcStreak()); } }
  const st = $('#vcStk'); if (st) st.onclick = () => { const c = S.combo || 0, nx = [3, 6, 10].find(m => c < m); toast(nx ? `Pick the crowd favourite ${nx - c} more time${nx - c === 1 ? '' : 's'} in a row and your votes pay ×${nx}` : 'Top streak: your votes pay ×10'); };
  j.querySelectorAll('.vc, .vc-nxu').forEach(e => e.remove());
  const c = vcCard(); if (!c) return;
  const el = document.createElement('button'); el.className = 'vc';
  el.innerHTML = `${c.art ? `<span class="vc-art" aria-hidden="true">${c.art}</span>` : `<img src="${c.img}" alt="">`}<span class="vc-tx"><b>${esc(c.t)}</b><small>${c.when ? `🕒 <span data-tat="${c.when}">${tLeft(c.when)}</span> · ` : ''}${esc(c.s)}</small></span><span class="vc-cta">${c.cta}</span>`;
  el.onclick = c.go; card.insertAdjacentElement('afterend', el);
  const nu = h && h.querySelector('.nxu'); if (nu) nu.remove();
  const n = false; if (n) el.insertAdjacentHTML('afterend', `<p class="vc-nxu">${n.k === 'tour' ? '🏆 Tournament' : '🟡 Coin challenge'} ${n.left === 1 ? 'after this vote' : `in <b>${n.left}</b> votes`}</p>`);
}

const _openBattleV = openBattle;
openBattle = function () {
  if (this && this.__cash) return _openBattleV.apply(this, arguments);
  S.potSeen = 1; S.btAlt = true; const f = fighters()[0]; if (f && CATS8.includes(f.cat)) S.nextBth = f.cat; save();
  return _openBattleV.apply(this, arguments);
};

// button colour = what it costs: any main button that spends real money ($) is green
const VC_CASH_RX = /\$\s?\d/;
function vcGreen(root) {
  (root || document).querySelectorAll('#sheet .btn, #sheet .kg-go, #sheet .kg2-go, #sheet .tsr2-e, #sheet .bt-cta, #flow .btn, #flow .bt-cta, #coach .bt-cta, #coach .btn').forEach(b => {
    if (b.closest('#enArea, .actions') && !/\$/.test(b.textContent || '')) return;
    if (b.closest('.vc') || b.classList.contains('link')) return;
    const t = b.textContent || '', cash = VC_CASH_RX.test(t) && !/🟡|coins?\b/i.test(t);
    b.classList.toggle('pay-cash', cash);
    const coin = !cash && !/earn|need|get more|buy/i.test(t) && (/🟡|\bcoins?\b/i.test(t) || !!b.querySelector('svg.gem, .gem, .coinic, use[href="#gemPath"]'));
    b.classList.toggle('pay-coin', coin);
  });
}
function vcPills() { document.querySelectorAll('.tsr2-e').forEach(e => { const t = e.textContent || '', c = /\$\s?\d/.test(t), g = !c && !!e.querySelector('svg, .gem'); e.classList.toggle('pill-cash', c); e.classList.toggle('pill-coin', g); }); }
new MutationObserver(() => { clearTimeout(vcGreen.t); vcGreen.t = setTimeout(() => { vcGreen(); vcPills(); }, 30); }).observe(document.body, { childList: true, subtree: true, characterData: true });

const _voteNoPop = vote;
vote = async function () { if ((S.since || 0) >= CFG.BATTLE_EVERY - 1) S.since = 0; return _voteNoPop.apply(this, arguments); };
const _renderJudgeC2 = renderJudge;
renderJudge = function () { const r = _renderJudgeC2.apply(this, arguments); try { vcPaint(); } catch (e) {} return r; };
setInterval(() => { document.querySelectorAll('.vc [data-tat]').forEach(e => { e.textContent = tLeft(+e.dataset.tat); }); }, 1000);
'''
# coin challenge result: main action is the cash version (opens the $1 head-to-head matchup, charged only on its entry button)
_a = """: `<button class="btn block kg2-go" id="gbAgain">Play again · Free</button>${!isCash() ? `<button class="btn block pc-real kg2-real" id="gbReal">💵 Play for real · $${LG_FEE}</button>` : ''}<div style="text-align:center"><button class="link kg2-back" data-shclose>Back</button></div>`}`;"""
assert s.count(_a) == 1, 'coin result buttons'
s = s.replace(_a, """: `<button class="btn block kg2-go vc-up" id="gbCash">💵 Play for cash · win $${(2 * (1 - KING_FEE)).toFixed(2)}</button><div style="text-align:center"><button class="link kg2-back" id="gbVote">Back to voting</button></div>`}`;""")
_b = "if (!opt.revenge && /coins|Free/.test($('#gbAgain').textContent)) $('#gbAgain').onclick = () => openGemBattle(stake || 25);"
assert s.count(_b) == 1, 'gbAgain handler'
s = s.replace(_b, "if (!opt.revenge && $('#gbAgain') && /coins|Free/.test($('#gbAgain').textContent)) $('#gbAgain').onclick = () => openGemBattle(stake || 25);\n      if ($('#gbCash')) $('#gbCash').onclick = () => { const ph = opt.photo || fighters()[0]; closeSheet(); openCashBattle(1, null, ph); };\n      if ($('#gbVote')) $('#gbVote').onclick = () => { closeSheet(); go('judge'); };")
# coin challenge pop: say plainly whether it's free or costs coins
_c = "cta: bme ? `Free challenge · ${CC_COIN} 🟡` :"
assert s.count(_c) == 1, 'coin cta'
s = s.replace(_c, "cta: bme ? (S.gbDone ? `Play · ${CC_COIN} 🟡 · win ${CC_COIN * 2}` : `Play free · win ${CC_COIN * 2} 🟡`) :")
_d = "Stake <b>${CC_COIN} 🟡</b>, win <b>${CC_COIN * 2} 🟡</b>. Result in 30 seconds.`"
assert s.count(_d) == 1, 'coin text'
s = s.replace(_d, "${S.gbDone ? `Stake <b>${CC_COIN} 🟡</b>, win <b>${CC_COIN * 2} 🟡</b>` : `<b>Free this time</b>, win <b>${CC_COIN * 2} 🟡</b>`}. Result in 30 seconds.`")
# coin challenge sheet: a paid challenge says what it costs
_e = "free ? 'Start now · Free' : `Free challenge · ${stake} 🟡`}</button>"
assert s.count(_e) == 1, 'coin sheet label'
s = s.replace(_e, "free ? 'Start now · Free' : `Play · ${stake} 🟡 · win ${stake * 2}`}</button>")
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]

CSS = r'''
/* vote: streak widget + cash card */
#judge.has-goal .wcard{display:none!important}
#judge .jfoot .stk{display:none!important}
.vch{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 4px}.vch h2{margin:0!important;text-align:left}
.vcs{flex:none;display:flex;align-items:center;gap:5px;border:0;background:none;padding:6px 2px;cursor:pointer}
.vcs i{width:10px;height:10px;border-radius:50%;background:#DCCFB6}.vcs i.on{background:#9E2F2A}
.vcs-sep{width:1.5px;height:20px;background:#CDBFA8;margin:0 4px}
.vcs-g{position:relative;font-size:1.25rem;line-height:1}.vcs-g small{position:absolute;right:-12px;bottom:-6px;font:800 .62rem "Nunito Sans",sans-serif;color:#9E2F2A}
.vcs.near .vcs-g{animation:vcwob .9s ease-in-out infinite}@keyframes vcwob{50%{transform:rotate(-12deg) scale(1.15)}}
html.yg .vcs i{background:rgba(255,255,255,.2)}html.yg .vcs i.on{background:#FF2D8E}html.yg .vcs-g small{color:#FF7AB8}
.vc{display:flex;align-items:center;gap:12px;width:100%;margin:12px 0 4px;box-sizing:border-box;padding:9px;border:0;border-radius:18px;text-align:left;cursor:pointer;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(60,40,20,.5);font-family:"Nunito Sans",sans-serif;color:#2D2521!important}
.vc img,.vc-art{flex:none;width:72px;height:72px;border-radius:12px;object-fit:cover}
.vc-art{display:grid;place-items:center;background:#2D4E86;font-size:2.2rem}
.vc-tx{flex:1;min-width:0}.vc-tx b{display:block;font:800 1.05rem/1.18 Fraunces,serif;color:#2D2521!important}
.vc-tx small{display:block;margin-top:3px;font-size:.86rem;color:#4E433C!important}
.vc-when{display:inline-block;margin-top:4px;padding:2px 9px;border-radius:999px;background:#F1E9DA;font-size:.78rem;font-weight:700;color:#2D2521!important}
.vc-cta{flex:none;width:92px;padding:8px 6px;border-radius:12px;background:#2D4E86;color:#fff!important;font:800 .8rem/1.15 "Nunito Sans",sans-serif;text-align:center;box-sizing:border-box}
#judge .jfoot:has(.en-hide){display:none}
/* goal bar and cash card: same height */
#vgGoal.vg,#judge .vc{height:92px;min-height:92px;max-height:92px;padding:0 12px 0 10px;overflow:hidden}
#vgGoal.vg img,#vgGoal .vg-ic,#judge .vc img,#judge .vc-art{width:68px;height:68px}
#vgGoal.vg img{border-radius:50%}#judge .vc img,#judge .vc-art{border-radius:12px}
#vgGoal .vg-tx b,#judge .vc-tx b{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
#vgGoal .vg-tx small,#judge .vc-tx small{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#judge .vc-tx b{font-size:.95rem}
#judge .vc-tx small{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;line-height:1.25}
#vgGoal .vg-ci{margin-right:5px;vertical-align:-3px}
html.yg .vc{background:#FBF6EC!important}
html body #sheet .pay-coin,html body #coach .pay-coin,.pay-coin{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;background-color:#E0A82E!important;color:#3A2600!important;box-shadow:0 8px 18px -8px rgba(160,110,10,.7)!important}.pay-coin *{color:#3A2600!important}
.tsr2-e.pill-cash{background:#21784A!important;color:#fff!important;border-radius:999px;padding:4px 10px!important;font-weight:800}.tsr2-e.pill-coin{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important;border-radius:999px;padding:4px 10px!important;font-weight:800}
html body #sheet .pay-cash,html body #flow .pay-cash,html body #coach .pay-cash,html:not(.yg) body #sheet .btn.pay-cash,html.yg body #sheet .btn.pay-cash,html:not(.yg) body #sheet .kg .kg-go.pay-cash,html.yg body #sheet .kg .kg-go.pay-cash,.pay-cash{background-color:#21784A!important;background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important;box-shadow:0 8px 18px -8px rgba(33,120,74,.7)!important;border-color:transparent!important}.pay-cash *{color:#fff!important}
#gbCash.vc-up{background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important;box-shadow:0 8px 18px -8px rgba(33,120,74,.7)!important}
.vc-nxu{margin:6px 0 0;text-align:center;font-size:.86rem;opacity:.85}
.vc-who{display:block;margin-top:2px;font-style:normal;font-size:.76rem;font-weight:700;color:#8A5A0A!important}
#vgGoal.vg{width:100%;margin:6px 0 4px;box-sizing:border-box}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('vote cash ok')
