# Skill preview: the coin balance drop-down and the "you've got coins" moment.
# Drop-down ("Your coins · 180 🟡"): Touch-ups first, then "Practise for coins" with the coin versions
# of the two cash games that translate straight to cash, using the same names:
# Quick Sprint · coins and Head-to-head · coins. One is marked Suggested (Quick Sprint once your judge
# score is 70%+, else Head-to-head). A green line points to the cash versions.
# The moment: the app's usual celebration pop, "You've got 180 coins" with "Use my coins", shown only at
# high milestones only (250, 500, 1,000, 2,500 coins; the top card already nudges touch-ups),
# each once, at most once per visit, and only on Vote when nothing else is open.
# usage: python3 build-skill/coins.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- the coin drop-down ----
const coinTU = () => S.photos.filter(p => p.s && lowestOpen(p) && !photoLock(p) && p.s.total < 99).sort((a, b) => a.s.total - b.s.total)[0];
function coinSuggest() { const l = typeof jgLv === 'function' && jgLv(); return l && jgAcc() >= 70 ? 'qs' : 'h2h'; }
useGems = function () { const g = Math.floor(S.gems || 0), p = coinTU(), best = fighters()[0], sug = coinSuggest(), l = typeof jgLv === 'function' && jgLv();
  const price = (n, id) => `<button class="cn-go ${g < n ? 'need' : ''}" data-cn="${id}">${n} 🟡</button>`;
  const nb = p ? [70, 80, 90].find(b => p.s.total < b) : null, tier = nb ? galBand(nb) : '';
  const tu = p ? `<div class="cn-tu"><span class="cn-im" style="background-image:url('${p.src}')"><i>${p.s.total}</i></span><span class="cn-tx"><b>Touch up ${esc(alName(p))}${tier ? ` to ${tier}` : ''}</b><small>${nb ? `${p.s.total} → ${nb} · then earns you ${GAL.BASE * galMult(nb)} 🟡 per vote` : 'Raise its score and earnings'}</small></span>${price(fixCost(p), 'tu')}</div>`
    : `<p class="cn-none">Upload a photo and your coins can touch it up.</p>`;
  const row = (id, ic, nm, sub, cost) => `<div class="cn-gm ${sug === id ? 'sug' : ''}">${sug === id ? '<i class="cn-tag">Suggested</i>' : ''}<span class="cn-ic">${ic}</span><span class="cn-tx"><b>${nm}</b><small>${sub}</small></span>${price(cost, id)}</div>`;
  const qs = row('qs', '🎯', 'Quick Sprint · coins', `${l ? `Your ${jgAcc()}% eye vs a rival · ` : ''}win ${QS_COIN_PAY[0]} 🟡`, QS_COIN);
  const h2h = best ? row('h2h', '⚔️', 'Head-to-head · coins', `${esc(alName(best))} vs a rival · win ${CC_COIN * 2} 🟡`, CC_COIN) : '';
  openSheet(`<div class="cn"><h2>Your coins · ${g.toLocaleString()} 🟡</h2><p class="cn-sub">Earned by voting. Spend them here.</p>
    <h3 class="cn-h">✨ Touch-ups <small>grow what your photos earn</small></h3>${tu}
    <h3 class="cn-h">🎯 Practise for coins <small>same games, coins not cash</small></h3>${sug === 'qs' ? qs + h2h : h2h + qs}
    <button class="cn-cash" id="cnCash">💵 Won a few? Play the same games for cash: <b>Head-to-head $1 · Quick Sprint $2</b></button></div>`);
  const need = n => { closeSheet(); runOut('gems', `You need ${n - g} more coins`, null, n - g); };
  document.querySelectorAll('#sheetBody [data-cn]').forEach(b => b.onclick = () => { const id = b.dataset.cn;
    if (id === 'tu') { const c = fixCost(p); if (g < c) { need(c); return; } closeSheet(); galImprove(p.id); go('studio'); return; }
    if (id === 'qs') { if (g < QS_COIN) { need(QS_COIN); return; } sprPractice(); return; }
    if (id === 'h2h') { if (g < CC_COIN) { need(CC_COIN); return; } closeSheet(); openGemBattle(CC_COIN); } });
  $('#cnCash').onclick = () => { closeSheet(); goCash(); GV.tab = 'battle'; go('gallery'); renderGallery(); }; };
// ---- the moment: the usual celebration pop at key coin milestones ----
let COIN_POPPED = false;
function coinMoment() { if (COIN_POPPED || !S.user || $('#panes').dataset.at !== 'judge') return;
  if ($('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on')) return;
  const g = Math.floor(S.gems || 0), p = coinTU(), steps = [QS_COIN, 500, 1000, 2500]; // high levels only: the top card already nudges touch-ups
  const hit = steps.filter(v => g >= v).pop(); if (!hit || (S.coinPop || 0) >= hit) return;
  COIN_POPPED = true; S.coinPop = hit; save();
  const what = 'practise Quick Sprint for coins';
  celebrate({ src: (p || fighters()[0] || S.photos[0] || {}).src || '', score: '🟡', title: `You’ve got ${g.toLocaleString()} coins`, text: `Earned from your votes and your photos. ${what.charAt(0).toUpperCase() + what.slice(1)}, or see everything they can do.`,
    cta: 'Use my coins', onCta: () => useGems(), later: 'Keep voting' }); }
setInterval(() => { try { coinMoment(); } catch (e) {} }, 2500);
// same name as the cash game
new MutationObserver(() => { try { document.querySelectorAll('#sheetBody .kg2-top b, #sheetBody .kg2-h').forEach(b => { if (/^Coin challenge$/.test(b.textContent.trim())) b.textContent = 'Head-to-head · coins'; }); } catch (e) {} }).observe($('#sheetBody'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* coin drop-down */
.cn h2{margin:0;font:900 1.5rem Fraunces,serif;color:#1F3157}.cn-sub{margin:2px 0 6px;font:700 .88rem "Nunito Sans";color:#4E433C}
.cn-h{display:flex;justify-content:space-between;align-items:baseline;margin:14px 2px 8px;font:900 1.05rem Fraunces,serif;color:#7A1F27}.cn-h small{font:700 .74rem "Nunito Sans";color:#4E433C}
.cn-tu,.cn-gm{position:relative;display:flex;gap:10px;align-items:center;padding:10px;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;margin-bottom:8px}
.cn-tu{box-shadow:inset 0 0 0 1.5px #E0B860}
.cn-im{position:relative;flex:none;width:56px;height:74px;border-radius:10px;background-size:cover;background-position:center}.cn-im i{position:absolute;right:3px;top:3px;font:900 .72rem Fraunces,serif;font-style:normal;background:#FFFDF9;padding:1px 5px;border-radius:99px}
.cn-ic{flex:none;width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;background:linear-gradient(160deg,#2B4372,#14213D)}
.cn-tx{flex:1;min-width:0}.cn-tx b{display:block;font:800 .95rem "Nunito Sans";color:#2D2521}.cn-tx small{display:block;font:600 .78rem "Nunito Sans";color:#4E433C}
.cn-go{flex:none;border:0;cursor:pointer;padding:8px 11px;border-radius:12px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .88rem "Nunito Sans";white-space:nowrap}.cn-go.need{opacity:.55}
html body #sheetBody .cn-go{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important;box-shadow:0 4px 10px -6px rgba(160,110,10,.8)!important;border:0!important;padding:8px 11px!important;border-radius:12px!important;font:900 .88rem "Nunito Sans"!important;width:auto!important;min-height:0!important}
.cn-gm.sug{margin-top:14px;box-shadow:inset 0 0 0 2px #E0A82E,0 6px 14px -10px rgba(160,110,10,.7)}.cn-tag{position:absolute;left:12px;top:-9px;font:900 .62rem "Nunito Sans";font-style:normal;letter-spacing:.05em;text-transform:uppercase;background:#E0A82E;color:#3A2600;padding:2px 7px;border-radius:99px}
.cn-cash{display:block;width:100%;margin-top:12px;padding:10px 12px;border:0;border-radius:14px;background:#E9F7EE;box-shadow:inset 0 0 0 1.5px #7FBE91;font:700 .82rem "Nunito Sans";color:#1E5233;text-align:left;cursor:pointer}.cn-cash b{color:#1E6B3E}
.cn-none{font:700 .85rem "Nunito Sans";color:#4E433C}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('coins ok')
