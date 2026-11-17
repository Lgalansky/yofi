# Real Money build, step 6 (after rmv2.py):
#  - you can see if you're a coin or real money player (account menu + My show), with a testing switch
#  - Friends pop: challenge a friend; coins for coin players, real money for cash players
#  - friend challenges are a straight 1 v 1: no weekly club pot, no blue ribbon; the winner takes the prize now
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# ---------- coin vs real is by player type, never mixed ----------
RA("frGem = () => S.frSt === 'gem'", "frGem = () => !isCash()")
RA('${FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${!coin && x === st}">$${x}</button>`).join(\'\')}<button data-frs="gem" aria-pressed="${coin}">${FR_GEM} ${G}</button>',
   '${isCash() ? FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${x === st}">$${x}</button>`).join(\'\') : `<button data-frs="gem" aria-pressed="true">${FR_GEM} ${G}</button>`}')
RA('${FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${!frGem() && x === frSt()}">$${x}</button>`).join(\'\')}<button data-frs="gem" aria-pressed="${frGem()}">${FR_GEM} ${gemIcon(\'\')}</button>',
   '${isCash() ? FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${x === frSt()}">$${x}</button>`).join(\'\') : `<button data-frs="gem" aria-pressed="true">${FR_GEM} ${gemIcon(\'\')}</button>`}')
# ---------- straight 1 v 1: winner takes the prize now ----------
RA(": `<small>Winner takes the ${esc(cn)} blue ribbon</small><b>${money(.85 * frSt() * 2)}</b><span>$${frSt()} each into the club pot · pays Sunday</span>`;",
   ": `<small>Winner takes</small><b>${money(.85 * frSt() * 2)}</b><span>$${frSt()} each · paid straight away</span>`;")
RA('<span class="tr">${coin ? \'🏆\' : CRW}</span>', '<span class="tr">🏆</span>')
RA("if (st) c.pot[k] = +((c.pot[k] || 0) + LG_CUT * st).toFixed(2);",
   "const fWin = st ? +(st * 2 * .85).toFixed(2) : 0; if (won && st) { S.cash = +((S.cash || 0) + fWin).toFixed(2); setTimeout(() => { paintWallet(); try { cashExplosion(fWin, { label: 'Friend challenge won' }); } catch (e) {} }, 9000); }")
RA("${esc(c.name)} · ${cn} blue ribbon${rev ? ' · 🔥 rematch bonus +25' : ''}",
   "${esc(c.name)} · ${coin ? `winner gets ${FR_GEM * 2} 🟡` : `winner takes ${money(.85 * st * 2)}`}${rev ? ' · 🔥 rematch bonus +25' : ''}")
RA("${msg ? `<p class=\"fb-crown ${won ? 'w' : 'l'}\">${msg}</p>` : ''}", "")
RA("<div class=\"kg2-next ${won ? 'win' : 'lose'}\"><small>${cn} club pot</small><b>${money(c.pot[k])}</b><span>${c.hold[k] === 'you' ? 'Yours if you hold the blue ribbon at Sunday midnight' : `@${esc(c.hold[k])} takes it if they still hold the blue ribbon on Sunday`}</span></div>",
   "<div class=\"kg2-next ${won ? 'gemw' : 'lose'}\"><small>${won ? 'You won' : 'You lost'}</small><b>${coin ? `🟡 ${won ? FR_GEM * 2 : FR_GEM}` : money(won ? fWin : st)}</b><span>${won ? (coin ? 'Added to your coins' : 'Added to your cash') : 'Rematch to win it back'}</span></div>${coin ? `<button class=\"btn block pc-real kg2-real\" id=\"cbReal\">💵 Play for real · $${LG_FEE}</button>` : ''}")
RA("$('#cbAgain').onclick = () => won ? crewCat(c, k) : revengePrep(c, k, h, me.id);",
   "$('#cbAgain').onclick = () => { closeSheet(); friendsPop(); }; if ($('#cbReal')) $('#cbReal').onclick = () => { closeSheet(); payCash(LG_FEE, 'A friend challenge', () => { setTimeout(friendsPop, 300); }); };")

# ---------- Friends pop ----------
s = s.replace("function fcNotify() {", r"""function friendsPop() { if ($('#sheet').classList.contains('on')) closeSheet(); const cash = isCash(), y = isYoungW(), C = crewsS(), c = C[0], F = c ? (c.members || []).filter(h => h !== 'you') : [], me = fighters().slice().sort((a, b) => b.s.total - a.s.total)[0];
  const stake = cash ? `$${frSt()} each · winner takes ${money(.85 * frSt() * 2)}` : `${FR_GEM} 🟡 each · winner takes ${FR_GEM * 2} 🟡`;
  popOpen(`<div class="pp fr-p"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">👥 Friends</p><h2 class="pp-h">Challenge a friend</h2>
    <p class="pp-m">Your photo vs theirs · members vote · <b>${stake}</b></p>
    ${cash ? `<div class="rc-st" role="group" aria-label="Entry">${FR_ST.map(v => `<button data-fst="${v}" aria-pressed="${v === frSt()}">$${v}</button>`).join('')}</div>` : ''}
    <div class="fr-l">${F.length ? F.map(h => `<div class="fr-r">${fav(h, 40)}<b>@${esc(h)}</b><button class="btn fr-go" data-frh="${esc(h)}">${cash ? `Challenge · $${frSt()}` : `Challenge · ${FR_GEM} 🟡`}</button></div>`).join('') : `<p class="fr-none">No friends on Yofi yet. Invite one and challenge them as soon as they join.</p>`}</div>
    <button class="btn block ${F.length ? 'pc-later-b' : 'pc-go'}" id="frInv">📲 Invite a friend on WhatsApp</button>
    ${cash ? '' : `<button class="btn block pc-real" id="frReal">💵 Challenge for real money · from $1</button>`}
    <div style="text-align:center"><button class="link pc-later" id="frNo">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  document.querySelectorAll('#coach [data-fst]').forEach(b => b.onclick = () => { S.frSt = +b.dataset.fst; save(); friendsPop(); });
  document.querySelectorAll('#coach [data-frh]').forEach(b => b.onclick = () => { if (!me) { popClose(); toast(`Get a photo to ${CFG.QUALIFY}+ first.`); return; } const h = b.dataset.frh, k = CATS8.includes(me.cat) ? me.cat : 'any'; popClose(); frPay(() => crewFight(c, k, h, me.id)); });
  $('#frInv').onclick = () => { popClose(); frDare(); }; if ($('#frReal')) $('#frReal').onclick = () => { popClose(); payCash(5, 'Cash to challenge friends', () => setTimeout(friendsPop, 300)); };
  $('#frNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
const playerType = () => isCash() ? '💵 Real money player' : '🟡 Coin player';
document.addEventListener('click', e => { const t = e.target.closest('#pfToCoin, #pfToReal, #pfFriends, #msFriends'); if (!t) return; e.preventDefault(); e.stopPropagation();
  if (t.id === 'pfFriends' || t.id === 'msFriends') { try { closeSheet(); } catch (x) {} friendsPop(); return; }
  S.cashMode = t.id === 'pfToReal' ? Date.now() : 0; save(); try { closeSheet(); } catch (x) {} try { paintWallet(); paintGems(); } catch (x) {} if ($('#panes').dataset.at === 'gallery') renderMyShow(); else if ($('#panes').dataset.at === 'judge') renderJudge(); toast(isCash() ? 'You’re now a real money player (test)' : 'You’re now a coin player (test)'); }, true);
function fcNotify() {""", 1)
# account menu: player type, Friends, and a testing switch
RA('<button class="link" id="mR" style="margin-top:6px">Reset prototype</button></div>`);',
   '<button class="btn quiet block" id="pfFriends">👥 Friends</button><p class="pf-type">You’re a <b>${playerType()}</b></p><p class="pf-test">Testing</p>${isCash() ? \'<button class="btn quiet block" id="pfToCoin">↺ Switch to coin player</button>\' : \'<button class="btn quiet block" id="pfToReal">↺ Switch to real money player</button>\'}\n    <button class="link" id="mR" style="margin-top:6px">Reset prototype</button></div>`);')
# My show: player type and Friends
RA("<p class=\"ms-sub\">Your photos in group judging and the hourly Best in Show</p>",
   "<p class=\"ms-sub\">Your photos in group judging and the hourly Best in Show · <b>${playerType()}</b></p>")
RA("<button class=\"btn block ms-add\" id=\"msAdd\">", "<button class=\"btn block ms-fr\" id=\"msFriends\">👥 Challenge a friend · ${isCash() ? `from $${FR_ST[0]}` : `${FR_GEM} 🟡`}</button><button class=\"btn block ms-add\" id=\"msAdd\">")
s = s.replace('</style>', """.fr-l{text-align:left;margin:4px 0 10px}.fr-r{display:grid;grid-template-columns:40px 1fr auto;gap:10px;align-items:center;padding:6px 0;border-top:1px solid rgba(127,127,127,.18)}.fr-r>b{font-size:.92rem}.fr-go{margin:0!important;padding:8px 12px!important;font-size:.82rem!important;width:auto!important;min-height:0!important;text-transform:none!important}.fr-none{font-size:.88rem;opacity:.85}
.pf-type{margin:12px 0 0;font-size:.9rem;text-align:left}.pf-test{margin:14px 0 4px;font-size:.7rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase;opacity:.6;text-align:left}.ms-fr{margin:0 0 8px!important}
html:not(.yg) .fr-go{background:#2F6B3F!important;color:#fff!important}html.yg .fr-go{background:#2EE59D!important;color:#14092B!important}html:not(.yg) .ms-fr{background:#F3ECDF!important;color:#2B2320!important;box-shadow:inset 0 0 0 1.5px #E6D9C4!important}html.yg .ms-fr{background:#2A1A52!important;color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v3 ok')
