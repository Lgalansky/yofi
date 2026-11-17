# Skill only: the Freeroll is replaced by a free cash challenge ($1, once an hour).
# 300 coins (earned by voting, never sold) = one real $1 photo challenge, free, once an hour.
# We don't fund the pot: a free challenge adds nothing to the pot; a win counts like a paid one (+1 star).
# Run by simplify.py unless YOFI_BUILD=real.
import re
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
s=s.replace("function fcNotify() {",r"""const FC_COINS = 300;
const fcReady = () => S.fcDay !== frHourKey();
const fcRowHTML = () => { if (!S || S.geoBlock) return ''; const r = fcReady(), ok = r && (S.gems || 0) >= FC_COINS;
  return `<button class="tsr2 fcrow ${ok ? 'can' : 'need'}" id="fcRow"><span class="tsr2-t"><span class="fr-tag fc-tag">FREE CASH CHALLENGE</span><b>${r ? 'Ready' : frMinsLeft() + 'm'}</b></span><span class="tsr2-p">$1</span><span class="tsr2-n"><small>${r ? '1 an hour' : 'Used'}</small></span><span class="tsr2-e">${ok ? `${FC_COINS} 🟡` : `🔒 ${FC_COINS} 🟡`}</span></button>`; };
function freeCh() { if ($('#sheet').classList.contains('on')) closeSheet(); const y = isYoungW();
  if (!fcReady()) { toast(`You’ve had this hour’s free cash challenge. Next one in ${frMinsLeft()} min.`); return; }
  const L = lgS(), ks = CATS8.filter(k => lgMine(k)).sort((a, b) => (a === 'any') - (b === 'any') || (L.jp[b] || 0) - (L.jp[a] || 0));
  if (!ks.length) { toast(`Get a photo to ${CFG.QUALIFY}+ first, then play free.`); pickPhoto(true); return; }
  const k = ks[0], me = lgMine(k), H = lgHold(k), opp = H.h && H.h !== 'you' ? H.h : (lgRank(k).find(r => !r.me) || {}).h, can = (S.gems || 0) >= FC_COINS, cn = esc(crownName(k)), st = y ? 'stars' : 'stars';
  if (!opp) { toast('No rival is free right now. Try again in a minute.'); return; }
  popOpen(`<div class="pc pc2 fch"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pc-k">${gi(k)}<span>🎟️ Free cash challenge · ${cn}</span></p><h2 class="pc-h">A real $1 challenge, free</h2>
    <div class="fch-vs"><figure><img src="${me.src}" alt=""><small>You · ${me.s.total}</small></figure><b>VS</b><figure><img src="${lgPhoto(opp, k)}" alt=""><small>@${esc(opp)}</small></figure></div>
    <p class="fch-m">Win and you get <b>+1 ⭐</b> in today’s <b>$${Math.round(L.jp[k]).toLocaleString()}</b> ${cn} cash pot. <b>${LG_SHARE} ⭐</b> by midnight share the pot.</p>
    <button class="btn block pc-real" id="fcGo" ${can ? '' : 'disabled'}>🎟️ Play free · ${FC_COINS} 🟡</button>
    <p class="fch-r">${can ? `One an hour. Coins are earned by ${y ? 'judging' : 'voting'}, never sold.` : `You need <b>${(FC_COINS - Math.floor(S.gems || 0)).toLocaleString()} more 🟡</b>. ${y ? 'Judge' : 'Vote'} to earn them.`}</p>
    <div style="text-align:center"><button class="link pc-later" id="fcNo">${$('#panes').dataset.at === 'judge' ? (y ? 'Keep judging' : 'Keep voting') : 'Not now'}</button></div></div>`);
  $('#fcGo').onclick = () => { if (S.user && S.user.guest) { popClose(); openSignup(() => freeCh(), { locked: false }); return; } if ((S.gems || 0) < FC_COINS || !fcReady()) return;
    S.gems -= FC_COINS; S.fcDay = frHourKey(); save(); paintGems(); popClose(); window.__fcFree = 1; window.__fcAt = Date.now(); lgFight(k, opp, false, false, me.id); };
  $('#fcNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
setInterval(() => { if (window.__fcFree && Date.now() - (window.__fcAt || 0) > 4000 && !$('#sheet').classList.contains('on') && !$('#coach').classList.contains('on')) { window.__fcFree = 0; try { paintWallet(); paintGems(); } catch (e) {} } }, 1000);
document.addEventListener('click', e => { if (e.target.closest('#fcRow, #tshTix, #ugSwap, [data-frrow]')) { e.preventDefault(); e.stopPropagation(); freeCh(); } }, true);
function fcNotify() {""",1)
# during a free challenge the player plays for real
RA("const isCash = () => !!(S && S.cashMode),","const isCash = () => !!(S && (S.cashMode || window.__fcFree)),")
# a free challenge adds nothing to the pot; a win makes you a cash player
RA("if (cur === 'cash') L.jp[k] = +(L.jp[k] + LG_CUT * LG_FEE).toFixed(2);","if (cur === 'cash' && !window.__fcFree) L.jp[k] = +(L.jp[k] + LG_CUT * LG_FEE).toFixed(2);")
RA("if (won) { L.you[k] = (L.you[k] || 0) + g; P.cr[k] = Math.max(0, P.cr[k] - 1); }","if (won) { L.you[k] = (L.you[k] || 0) + g; P.cr[k] = Math.max(0, P.cr[k] - 1); if (window.__fcFree) goCash(); }")
RA("<b>${isKing ? 'Head-to-head' : wasHolder ? 'Blue ribbon defence' : rematch ? 'Rematch' : 'Challenge'}</b>","<b>${window.__fcFree ? '🎟️ Free cash challenge' : isKing ? 'Head-to-head' : wasHolder ? 'Blue ribbon defence' : rematch ? 'Rematch' : 'Challenge'}</b>")
# every Freeroll door now opens the free cash challenge
RA("function swapTicket() {","function swapTicket() { freeCh(); return;")
RA("function frEnter(f) {","function frEnter(f) { freeCh(); return;")
# Tournaments: free cash challenge row instead of Freeroll rows; no Freerolls filter
RA('<div class="tsl2" data-tfl="${TF}">${chRowHTML()}${frRows}${rows}</div>','<div class="tsl2" data-tfl="${TF}">${fcRowHTML()}${chRowHTML()}${rows}</div>')
RA("const TF = window.__tFil || 'all',","const TF = (window.__tFil === 'fr' ? 'all' : window.__tFil) || 'all',")
RA("['fr', '🎟️ Freerolls'], ","")
a=s.index('<button class="tsh-tix tsh-fr" id="tshTix">'); b=s.index('</button>',a)
s=s[:a]+'<button class="tsh-tix tsh-fr" id="tshTix">${fcReady() ? `🎟️ Free cash challenge · <b>${FC_COINS} 🟡</b>` : `🎟️ Next free cash challenge in ${frMinsLeft()} min`}'+s[b:]
a=s.index('<b>Enter a Freeroll</b><small>'); b=s.index('</button>`;',a)
s=s[:a]+'<b>Free cash challenge</b><small>${fcReady() ? `A real $1 challenge · 1 an hour` : `Next one in ${frMinsLeft()} min`}</small></span><em class="${(S.gems || 0) < FC_COINS || !fcReady() ? \'need\' : \'\'}">${FC_COINS} 🟡</em>'+s[b:]
# photo reaches 80: point at the free cash challenge
a=s.index("title: 'Freeroll ready!'"); b=s.index("later: 'Later' })",a)
s=s[:a]+"title: 'Ready to play for real!', text: `Your photo reached <b>${tot}</b>. Use <b>${FC_COINS} coins</b> for a <b>free $1 cash challenge</b>, once an hour.`, cta: '🎟️ Free cash challenge', onCta: () => { closeFlow(); freeCh(); }, "+s[b:]
# how it works + small texts
a=s.index("${T('t-fr'"); b=s.index("${T('t-ko'",a)
s=s[:a]+"${T('t-fr', '🎟️', 'Free cash challenge', 'Every hour · top row', '🎟️ Free', [`Use <b>${FC_COINS} coins</b>, once an hour. Coins are earned by ${isYoungW() ? 'judging' : 'voting'}.`, 'A <b>real $1 challenge</b>: your photo against a rival, decided live by member votes.', `Win <b>+1 ⭐</b> in that day’s cash pot. <b>${LG_SHARE} ⭐</b> by midnight share the pot.`, 'A win makes you a cash player.'])}\n    "+s[b:]
RA("Win coins to touch up photos and enter cash Freerolls.<br>","Win coins to touch up photos and play a free cash challenge.<br>")
# Coming up: tell coin players when a free cash challenge is ready
RA("return it.sort((p, q) => p.need - q.need)[0] || null; }",
   "if (!isCash() && fcReady() && (S.gems || 0) >= FC_COINS && fighters().length) it.push({ ic: '🎟️', t: '<b>Free cash challenge</b> · a real $1 challenge', k: 'f', need: 0, per: 1 });\n  return it.sort((p, q) => p.need - q.need)[0] || null; }")
RA("function upNow() { const x = upNext(); if (!x) return;","function upNow() { const x = upNext(); if (!x) return; if (x.k === 'f') { freeCh(); return; }")
s=s.replace('</style>',""".fch-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin:4px 0 10px}.fch-vs figure{margin:0;display:flex;flex-direction:column;gap:3px;align-items:center}.fch-vs img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:14px}.fch-vs small{font-size:.76rem;font-weight:800}.fch-vs>b{font-weight:900}
.fch-m{margin:0 0 10px;font-size:.92rem;line-height:1.4}.fch-r{margin:8px 0 2px;font-size:.78rem;opacity:.85}.fc-tag{background:#2F6B3F!important;color:#fff!important}html.yg .fc-tag{background:#21C77A!important;color:#0B1A12!important}
html:not(.yg) .tsr2.fcrow{background:#E8F3EA!important;box-shadow:inset 0 0 0 1.5px #2F6B3F!important}html.yg .tsr2.fcrow{background:#10301F!important;box-shadow:inset 0 0 0 1.5px #21C77A!important}
.tsr2.fcrow .tsr2-t{flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:2px!important}.tsr2.fcrow .fc-tag{display:inline-block!important;font-size:.56rem!important;font-weight:900!important;line-height:1.3!important;padding:2px 6px!important;border-radius:6px!important}.tsr2.fcrow .tsr2-n small{font-size:.72rem;font-weight:800}
html:not(.yg) .fch-m,html:not(.yg) .fch-r,html:not(.yg) .fch-vs{color:#2B2320}html.yg .fch-m,html.yg .fch-r,html.yg .fch-vs{color:#E9E2FF}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('free cash challenge ok')
