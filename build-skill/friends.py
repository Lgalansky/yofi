# Skill preview: friend challenges in coins and cash (they bring new players in).
#  - The friend challenge screen lets you pick the stake: 100 🟡 coins, $1 or $5 (was set by
#    coin/cash mode). Coin chip gold, cash chips green; the WhatsApp button says what it costs.
#  - The coin drop-down offers Challenge a friend · coins (Suggested) and Quick Sprint · coins.
#    Head-to-head · coins is gone: it used live votes on strangers' matches.
#  - Compete › Your photo › 1 v 1 has a "Challenge a friend" tile (cash) next to Head-to-head.
# usage: python3 build-skill/friends.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)

# coins or cash is the player's choice, not the app mode; coin stakes 100 / 250 / 500
rep("const FR_GEM = 100, frGem", "let FR_GEM = (typeof S !== 'undefined' && S && [100, 250, 500].includes(S.frGemAmt)) ? S.frGemAmt : 100; const frGem")
rep("document.querySelectorAll('#sheetBody [data-frs]').forEach(b => b.onclick = () => { S.frSt = b.dataset.frs === 'gem' ? 'gem' : +b.dataset.frs; save(); sel = po.sel; paint(); });",
    "document.querySelectorAll('#sheetBody [data-frs]').forEach(b => b.onclick = () => { S.frSt = b.dataset.frs === 'gem' ? 'gem' : +b.dataset.frs; if (b.dataset.amt) { FR_GEM = +b.dataset.amt; S.frGemAmt = FR_GEM; } save(); sel = po.sel; paint(); });")
rep("frGem = () => !isCash()", "frGem = () => S.frSt === 'gem' || (S.frSt == null && !isCash())")
rep('<div class="riv-st fr-st bf-st" role="group" aria-label="Entry">${isCash() ? FR_ST.map(x => `<button data-frs="${x}" aria-pressed="${x === st}">$${x}</button>`).join(\'\') : `<button data-frs="gem" aria-pressed="true">${FR_GEM} ${G}</button>`}</div>',
    '<div class="fr-tg" role="tablist"><button role="tab" data-frs="gem" aria-selected="${coin}">🟡 Coins</button><button role="tab" data-frs="${[1, 2, 5].includes(st) ? st : 1}" aria-selected="${!coin}">💵 Cash</button></div>'
    + '<div class="sk-row fr-sk" role="radiogroup" aria-label="Entry">${coin ? [100, 250, 500].map(a => `<button role="radio" class="fr-coin" data-frs="gem" data-amt="${a}" aria-checked="${a === FR_GEM}"><b>${a} 🟡</b><small>win ${a * 2} 🟡</small></button>`).join(\'\') : [1, 2, 5].map(x => `<button role="radio" data-frs="${x}" aria-checked="${x === st}"><b>$${x}</b><small>win ${money(.85 * x * 2)}</small></button>`).join(\'\')}</div>')
rep('<span class="fcs-wa">${WA_ICON}</span>Invite on WhatsApp</a>', '<span class="fcs-wa">${WA_ICON}</span>Invite on WhatsApp · ${coin ? FR_GEM + \' 🟡\' : \'$\' + st}</a>')
rep('<h2><span class="bf-ic">${VS_IC}</span>Challenge a friend</h2>', '<h2>🤝 Challenge a friend</h2>')
s = s.replace('<a class="btn block fcn-go bf-go" id="bfGo"', '<a class="btn block fcn-go bf-go ${coin ? \'fr-gold\' : \'fr-green\'}" id="bfGo"', 1)

JS = r'''
// ---- coin drop-down: friends + Quick Sprint (no strangers' coin matches using live votes) ----
const _useGemsF = useGems;
useGems = function () { _useGemsF.apply(this, arguments);
  try { const sb = $('#sheetBody'), g = Math.floor(S.gems || 0), rows = sb.querySelectorAll('.cn-gm'); if (!rows.length) return;
    rows.forEach(r => { if (r.querySelector('[data-cn="h2h"]')) r.remove(); else { r.classList.remove('sug'); const t = r.querySelector('.cn-tag'); if (t) t.remove(); } });
    const best = fighters()[0] || S.photos.slice().sort((a, b) => b.s.total - a.s.total)[0];
    const fr = document.createElement('div'); fr.className = 'cn-gm sug';
    fr.innerHTML = `<i class="cn-tag">Suggested</i><span class="cn-ic">🤝</span><span class="cn-tx"><b>Challenge a friend · coins</b><small>${best ? esc(alName(best)) + ' vs a friend’s photo · ' : ''}win ${FR_GEM * 2} 🟡 · they join free</small></span><button class="cn-go ${g < FR_GEM ? 'need' : ''}" data-cn="fr">${FR_GEM} 🟡</button>`;
    const h = [...sb.querySelectorAll('.cn-h')].pop(); h.after(fr);
    fr.querySelector('[data-cn="fr"]').onclick = () => { if (g < FR_GEM) { closeSheet(); runOut('gems', `You need ${FR_GEM - g} more coins`, null, FR_GEM - g); return; } S.frSt = 'gem'; save(); closeSheet(); frDare(); };
    const cash = $('#cnCash'); if (cash) cash.innerHTML = '💵 Play them for cash: <b>Challenge a friend $1 · Quick Sprint $2</b>'; } catch (e) {} };
// ---- Compete: a Challenge a friend tile next to Head-to-head ----
const _c2PhotoF = c2Photo;
c2Photo = function () { let h = _c2PhotoF.apply(this, arguments); const best = fighters()[0];
  if (best && h.includes('data-c2r="h2h"')) h = h.replace(/<button class="c3-t c3-h2h" data-c2r="h2h">[\s\S]*?<\/button>/, m => m + `<button class="c3-t c3-h2h c3-frc" data-c2r="friend"><span class="c3-pair"><span class="c3-wa">${WA_ICON}<b>A friend</b></span><i>VS</i><img src="${best.src}" alt=""></span><span class="c3-lb"><b>Challenge a friend</b><em>$1 → ${money(1.7)}</em></span></button>`);
  return h; };
const _c2RenderF = c2Render;
c2Render = function () { _c2RenderF.apply(this, arguments); const b = document.querySelector('#gallery [data-c2r="friend"]'); if (b) b.onclick = () => { if (S.frSt === 'gem' || S.frSt == null) S.frSt = 1; save(); frDare(); }; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* friend challenge stake: coins gold, cash green */
.fr-tg{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:3px;border-radius:12px;background:#EFE6D6;margin:2px 0 8px}.fr-tg button{border:0;cursor:pointer;padding:7px;border-radius:9px;background:none;font:800 .88rem "Nunito Sans";color:#5F534A}.fr-tg button[aria-selected="true"]{background:#FFFDF9;color:#1F3157;box-shadow:0 1px 4px rgba(0,0,0,.15)}
.sk-row.fr-sk{margin:4px 0 10px}.sk-row.fr-sk button.fr-coin{box-shadow:inset 0 0 0 1.5px #E0B860;color:#8A5A0A}
.sk-row.fr-sk button.fr-coin[aria-checked="true"]{background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;box-shadow:0 5px 12px -6px rgba(160,110,10,.7)}.sk-row.fr-sk button.fr-coin[aria-checked="true"] small{color:#5A3E00}
html body #sheetBody .bf-go{white-space:nowrap;font-size:1.05rem!important}
html body #sheetBody .bf-go.fr-gold{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important}
html body #sheetBody .bf-go.fr-green{background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important}
.c3-frc{grid-column:1/-1}.c3-wa{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;height:120px;background:linear-gradient(160deg,#E9F7EE,#CFEBD9);color:#1E6B3E}.c3-wa svg{width:34px;height:34px}.c3-wa b{font:900 .9rem Fraunces,serif}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('friends ok')
