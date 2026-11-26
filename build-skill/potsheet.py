# Skill preview: the daily jackpot challenge screen, rebuilt to be short, clear and fun.
#  - top: "🐾 Pet jackpot", the pot counting up, "Pays in 19h 37m"
#  - your stars: 3 star slots ("2 more ⭐ to share the pot" / "You're in · about $9.27")
#  - the match: blue ribbon holder vs your photo (score badge, readable)
#  - $1 / $2 / $5 stake chips (win +1/+2/+5 ⭐), one green button, one "How it works" link
#  - if your photo is under 70: one navy "Touch up Cleo to 70" button instead
# Also: rival photos never use one of your own photos.
# Stars: every star you win shares the 70% (no 3-star minimum); screens show your star count.
# usage: python3 build-skill/potsheet.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# rivals never show one of your photos
rep("const lgPhoto = (h, k) => { const pool = SEED.filter(x => x.cat === BATTLE_POOL[k]),",
    "const lgPhoto = (h, k) => { const mineS = new Set(S.photos.flatMap(p => [p.src, p.orig])), pool = SEED.filter(x => x.cat === BATTLE_POOL[k] && !mineS.has(x.src)),")

# every star shares the 70% (no 3-star wall since the pot is split by stars)
rep("let LG_FEE = 2, LG_SHARE = 3,", "let LG_FEE = 2, LG_SHARE = 1,")
rep("<p>With <b>3+ stars</b> you share the other <b>70%</b> by stars: more stars, bigger share.", "<p>Every star you win gets a share of the other <b>70%</b>: more stars, bigger share.")
rep("🏆 Most stars wins 30% · 3+ stars share 70% by stars", "🏆 Most stars wins 30% · every ⭐ shares 70%")
rep("With 3+ stars you share the other 70% by stars: more stars, bigger share.", "Every star you win shares the other 70%: more stars, bigger share.")
rep("70% shared by ${ST} among players with ${LG_SHARE}+.<br>", "70% is shared by every ${ST.slice(0, -1)} won today.<br>")
rep("⭐ ${LG_SHARE}+ stars share <b>70%</b> by stars", "⭐ every star shares <b>70%</b>")
rep("<span class=\"yd-s\">${Math.min(r.y, LG_SHARE)}/${LG_SHARE}</span>", "<span class=\"yd-s\">${r.y} ⭐</span>")
rep("<span class=\"y\">You <b>${Math.min(Math.max(0, y), LG_SHARE)}/${LG_SHARE}</b></span>", "<span class=\"y\">You <b>${Math.max(0, y)} ⭐</b></span>")
rep("<p><b>${Math.min(y, LG_SHARE)}/${LG_SHARE} ${ST}</b> · ${need ? `${need} more ⭐ to qualify`", "<p><b>${y} ${y === 1 ? ST.slice(0, -1) : ST}</b> · ${need ? 'win one to get a share'")
rep("<p><b>${Math.min(y, LG_SHARE)}/${LG_SHARE} stars</b> · ${need ? `${need} more win${need === 1 ? '' : 's'} to share the pool`", "<p><b>${y} star${y === 1 ? '' : 's'}</b> · ${need ? 'win one to get a share'")
rep("'Earn 3 stars to share the pot'", "'Every star wins a share of the pot'")
rep("Collect 3 stars in a category by midnight to share the pot.", "Every star you win by midnight gets a share of the pot.")
rep("Get ${LG_SHARE} ⭐ to qualify.", "Every ⭐ gets a share.")
rep("s: mine ? `You ${Math.min(y, LG_SHARE)}/${LG_SHARE} ⭐ · from $1 · daily`", "s: mine ? (y ? `You ${y} ⭐ · about ${money(lgShare(k))} · from $1` : 'Win ⭐ for a share · from $1')")
s = s.replace("an equal share wi", "a share by stars wi")

JS = r'''
// ---- the jackpot challenge screen ----
const LG_IC = { pets: '🐾', travel: '✈️', night: '🍃', selfie: '👨‍👩‍👧', fitness: '🌷', food: '🧁', style: '🏠', any: '⭐' };
function lgRulesSheet() { openSheet(`<div class="pj-rules"><h2>How jackpots work</h2>${LG_RULES()}<button class="btn block" data-shclose style="margin-top:14px">Got it</button></div>`); }
lgCat = function (k) {
  const L = lgS(), H = lgHold(k), iHold = H.h === 'you', R0 = lgRank(k), y = L.you[k] || 0, mine = lgMine(k), cn = crownName(k);
  const near = iHold ? R0.filter(r => !r.me).sort((a, b) => Math.abs(a.n - y) - Math.abs(b.n - y))[0] : { h: H.h };
  const low = !mine && S.photos.filter(p => fitsTheme(p, k) && p.s).sort((a, b) => b.s.total - a.s.total)[0];
  const rematch = !iHold && (H.hist || [])[0] === 'you', cash = isCash(), free = cash && (S.cashTix || 0) > 0 && LG_FEE === 1;
  const pot = L.jp[k] || 0, share = y ? lgShare(k) : 0, stars = `<i class="${y ? 'on' : ''}">★</i><b>${y}</b>`;
  const me = mine || low, theirs = lgPhoto(near.h, k);
  const starLine = y ? `Your share now: about <b>${money(share)}</b>` : 'Win a ⭐ to get a share of the pot';
  const btn = S.minor ? `<p class="pj-min">Cash jackpots are 18+</p>`
    : mine ? `<button class="btn block pj-go" id="lgQuick">${VS_IC}${iHold ? 'Defend your ribbon' : rematch ? 'Rematch' : 'Challenge'} · ${cash ? (free ? 'Free 🎟️' : '$' + LG_FEE) : LG_COIN + ' 🟡'}</button>
       <p class="pj-win">Win: <b>+${cash ? LG_FEE : 1} ⭐</b>${iHold ? ' and keep the ribbon' : ' and take the ribbon'}</p>`
    : low ? `<button class="btn block pj-up" id="lgQuick">✨ Touch up ${esc(alName(low))} to ${CFG.QUALIFY}</button><p class="pj-win">Your photo scores <b>${low.s.total}</b> · challenges open at ${CFG.QUALIFY}</p>`
    : `<button class="btn block pj-up" id="lgQuick">📷 Add a ${esc(cn.toLowerCase())} photo</button><p class="pj-win">Then get it to ${CFG.QUALIFY} to play</p>`;
  const chips = mine && cash && !S.minor ? `<div class="sk-row" role="radiogroup" aria-label="Entry">${LG_STAKES.map(v => `<button role="radio" aria-checked="${v === LG_FEE}" data-sk="${v}" class="${v === 1 && (S.cashTix || 0) > 0 ? 'sk-fr' : ''}">${v === 1 && (S.cashTix || 0) > 0 ? '<i class="sk-free">FREE</i>' : ''}<b>$${v}</b><small>Win +${v} ⭐</small></button>`).join('')}</div>` : '';
  openSheet(`<div class="pj">
    <div class="pj-top"><span class="pj-t">${LG_IC[k] || '⭐'} ${esc(cn)} jackpot</span><button class="pj-x" data-shclose aria-label="Close">✕</button></div>
    <div class="pj-pot"><b id="pjPot">$${Math.round(pot).toLocaleString()}</b><span>⏱ Pays in ${dayLeft()}</span></div>
    <div class="pj-st"><span class="pj-stars">${stars}</span><span>${starLine}</span></div>
    <div class="pj-vs"><figure class="pj-them"><span class="pj-ph"><img src="${theirs}" alt="">${iHold ? '' : `<i class="pj-rib">${CRW}</i>`}</span><figcaption>@${esc(near.h)}<small>${iHold ? 'Nearest rival' : 'Ribbon holder'}</small></figcaption></figure>
      <span class="pj-x2">VS</span>
      <figure class="pj-me ${mine ? '' : 'low'}">${me ? `<span class="pj-ph"><img src="${me.src}" alt="">${iHold ? `<i class="pj-rib">${CRW}</i>` : ''}<i class="pj-sc">${me.s.total}</i></span>` : `<span class="pj-ph pj-add">+</span>`}<figcaption>You<small>${mine ? (iHold ? '🎀 You hold it' : 'Ready to play') : low ? `Needs ${CFG.QUALIFY}` : 'No photo yet'}</small></figcaption></figure></div>
    ${chips}${btn}
    <button class="link pj-how" id="pjHow">How it works</button></div>`);
  // the pot counts up a little
  const pe = $('#pjPot'); if (pe) { const t0 = performance.now(), from = Math.max(0, pot - 18); const tick = t => { if (!pe.isConnected) return; const q = Math.min(1, (t - t0) / 900); pe.textContent = '$' + Math.round(from + (pot - from) * (1 - Math.pow(1 - q, 3))).toLocaleString(); if (q < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }
  document.querySelectorAll('#sheetBody [data-sk]').forEach(b => b.onclick = () => { LG_FEE = +b.dataset.sk; S.lgStake = LG_FEE; save(); lgCat(k); });
  $('#pjHow').onclick = lgRulesSheet;
  const q = $('#lgQuick'); if (q) q.onclick = () => {
    if (mine) { if (rematch) { revengePrep(null, k, H.h); return; } lgPay(() => lgFight(k, near.h, !iHold)); return; }
    closeSheet(); if (low) { S.cur = low.id; save(); TU_GAL = false; WALL = false; go('studio'); renderStudio(); return; } addCatPhoto(k); };
};
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* jackpot challenge screen */
.pj{padding:2px 2px 4px}
.pj-top{display:flex;align-items:center;justify-content:space-between}.pj-t{font:900 1.5rem Fraunces,serif;color:#1F3157}
.pj-x{border:0;background:#EFE6D6;width:34px;height:34px;border-radius:50%;font:900 .95rem "Nunito Sans";color:#2D2521;cursor:pointer}
.pj-pot{position:relative;margin:10px 0 10px;padding:12px 14px 10px;border-radius:18px;text-align:center;background:linear-gradient(180deg,#E9F7EE,#CFEBD9);box-shadow:inset 0 0 0 2px #7FBE91;overflow:hidden}
.pj-pot::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 35%,rgba(255,255,255,.6) 50%,transparent 65%);transform:translateX(-120%);animation:jarShine 3.2s ease-in-out infinite}
.pj-pot b{display:block;font:900 2.6rem/1 Fraunces,serif;color:#1E6B3E}.pj-pot span{display:inline-block;margin-top:6px;font:800 .8rem "Nunito Sans";color:#2E6B42;background:rgba(255,255,255,.7);padding:2px 10px;border-radius:99px}
.pj-st{display:flex;align-items:center;gap:10px;justify-content:center;margin:0 0 12px;font:700 .92rem "Nunito Sans";color:#2D2521}.pj-st b{color:#1E6B3E}
.pj-stars{display:inline-flex;align-items:center;gap:3px;padding:3px 10px 3px 7px;border-radius:99px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E0B860}.pj-stars b{font:900 1.15rem Fraunces,serif;color:#8A5A0A}.pj-stars i{font-style:normal;font-size:1.5rem;line-height:1;color:#E2D5BE}.pj-stars i.on{color:#E0A82E;text-shadow:0 0 8px rgba(224,168,46,.6);animation:pjStar .5s ease-out both}
@keyframes pjStar{0%{transform:scale(.3)}70%{transform:scale(1.25)}100%{transform:none}}
.pj-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;margin-bottom:12px}
.pj-vs figure{margin:0;text-align:center}.pj-ph{position:relative;display:block;aspect-ratio:3/4;border-radius:16px;overflow:hidden;background:#EFE6D6}.pj-ph img{width:100%;height:100%;object-fit:cover;display:block}
.pj-them .pj-ph{box-shadow:0 0 0 3px #E0A82E}.pj-me .pj-ph{box-shadow:0 0 0 3px #2D4E86}.pj-me.low .pj-ph img{filter:grayscale(.6) brightness(.9)}
.pj-rib{position:absolute;left:4px;top:4px;width:36px;height:44px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.4))}html body .pj-rib svg{width:36px!important;height:44px!important}
.pj-sc{position:absolute;right:6px;top:6px;font:900 1rem Fraunces,serif;font-style:normal;background:#FFFDF9;color:#2D2521;padding:3px 9px;border-radius:99px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.pj-me.low .pj-sc{background:#FBEFD2;color:#8A3B00}
.pj-add{display:flex;align-items:center;justify-content:center;font:900 2.4rem "Nunito Sans";color:#8A7E72;box-shadow:inset 0 0 0 2px #CDB98F}
.pj-vs figcaption{margin-top:6px;font:800 .92rem "Nunito Sans";color:#2D2521}.pj-vs figcaption small{display:block;font:700 .74rem "Nunito Sans";color:#4E433C}
.pj-x2{width:44px;height:44px;border-radius:50%;background:#2D4E86;color:#fff;display:flex;align-items:center;justify-content:center;font:900 1rem Fraunces,serif;box-shadow:0 0 0 4px #F7F0E4,0 4px 10px rgba(45,78,134,.5)}
html body #sheetBody .pj-go{background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important;box-shadow:0 8px 18px -8px rgba(33,120,74,.7)!important;display:flex;align-items:center;justify-content:center;gap:8px}
.pj-win{margin:6px 0 2px;text-align:center;font:700 .86rem "Nunito Sans";color:#4E433C}.pj-win b{color:#8A5A0A}
.pj-min{text-align:center;font-weight:800}
.pj-how{display:block;margin:8px auto 0;font:800 .9rem "Nunito Sans"}
.pj-rules h2{margin:0 0 8px;font:900 1.4rem Fraunces,serif;color:#1F3157;text-align:center}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('potsheet ok')
