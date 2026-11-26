# Skill preview: challenge stars follow the real money staked.
# Pick $1, $2 or $5 for a daily photo challenge; a win earns 1 star per $1 (a $5 win = 5 stars).
# Your stars for each category show on the front of its challenge photo.
# usage: python3 build-skill/stakes.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# the entry is whatever stake the player picked (kept between visits)
rep("const LG_FEE = 2,", "let LG_FEE = 2,")
# a cash win earns 1 star per $1 staked; coin practice stays at 1 star; rematch still doubles
rep("const g = won ? (rematch ? 2 : 1) : 0;", "const g = won ? (cur === 'cash' ? Math.max(1, Math.round(LG_FEE)) : 1) * (rematch ? 2 : 1) : 0;")
rep("'Rematch · win +2 stars'", "`Rematch · win +${2 * (cur === 'cash' ? LG_FEE : 1)} ⭐`")
rep("'Win +1 star'}", "`Win +${cur === 'cash' ? LG_FEE : 1} ⭐`}")
# challenge sheet: stake picker above the green button, button and line underneath follow it
rep("Today’s photo challenges`} · $2</button>", "Challenge now`} · $${LG_FEE}</button>")
# result screen always shows the stars just won
rep('<p class="pr3-s">${sub2}</p>', '<p class="pr3-s">${sub2}${won && (took || kept) ? ` <b class="pr3-g">+${g} ⭐</b>` : ""}</p>')
rep("<b>+1 star</b> · $1.60 goes into today’s pot", "<b>+${LG_FEE} ⭐</b> · ${money(LG_CUT * LG_FEE)} goes into today’s pot")
rep("<span>+1 ⭐${iHold", "<span>+${isCash() ? LG_FEE : 1} ⭐${iHold")
# rules
rep("Every challenge costs <b>$2</b>. <b>$1.60</b> goes into", "Pick <b>$1, $2 or $5</b> per challenge. <b>80%</b> goes into")
rep("Win <b>+1 star</b>. Lose and you keep your stars.", "Win <b>1 ⭐ per $1</b> you put in (a $5 win = 5 ⭐). Lose and you keep your stars.")
# your stars on the front of each challenge photo
rep('alt="" loading="lazy"></button>', 'alt="" loading="lazy">${y ? `<em class="bcc-ys">⭐ ${y}<small>your stars</small></em>` : \'\'}</button>')

# the 70% is shared by stars, not equally: 3+ stars to qualify, then each star is one share
# (demo: the other qualifiers hold about 6 stars each)
rep("return y < LG_SHARE ? 0 : +(L.jp[k] * (1 - LG_KING) / lgQn(k) +", "return y < LG_SHARE ? 0 : +(L.jp[k] * (1 - LG_KING) * y / (lgQn(k) * 6 + y) +")
rep("Everyone with <b>3+ stars</b> share the other <b>70%</b> equally.", "With <b>3+ stars</b> you share the other <b>70%</b> by stars: more stars, bigger share.")
s = s.replace("🏆 Most stars wins 30% · 3+ stars share 70%</span>", "🏆 Most stars wins 30% · 3+ stars share 70% by stars</span>")
rep("Everyone with 3+ stars shares the other 70% equally.", "With 3+ stars you share the other 70% by stars: more stars, bigger share.")
rep("<span>70% shared equally by players with ${LG_SHARE}+ ${ST}.<br>", "<span>70% shared by ${ST} among players with ${LG_SHARE}+.<br>")
rep("${need} win${need === 1 ? '' : 's'} to qualify", "${need} more ⭐ to qualify")
rep("Win ${LG_SHARE} to qualify.", "Get ${LG_SHARE} ⭐ to qualify.")
rep("⭐ ${LG_SHARE}+ stars share <b>70%</b> equally", "⭐ ${LG_SHARE}+ stars share <b>70%</b> by stars")

JS = r'''
// stakes: $1 / $2 / $5, one star per $1 on a win
const LG_STAKES = [1, 2, 5];
LG_FEE = LG_STAKES.includes(S.lgStake) ? S.lgStake : 2;
const _lgCatSK = lgCat;
lgCat = function (k) { const r = _lgCatSK.apply(this, arguments);
  try { const go = document.querySelector('#sheetBody #lgQuick'); if (go && isCash() && lgMine(k) && !document.querySelector('#sheetBody .sk-row')) {
    go.insertAdjacentHTML('beforebegin', `<div class="sk-row" role="radiogroup" aria-label="Entry">${LG_STAKES.map(v => `<button role="radio" aria-checked="${v === LG_FEE}" data-sk="${v}"><b>$${v}</b><small>Win +${v} ⭐</small></button>`).join('')}</div>`);
    document.querySelectorAll('#sheetBody [data-sk]').forEach(b => b.onclick = () => { LG_FEE = +b.dataset.sk; S.lgStake = LG_FEE; save(); const sc = document.querySelector('#sheetBody').scrollTop; lgCat(k); document.querySelector('#sheetBody').scrollTop = sc; }); } } catch (e) {}
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* stake picker + your stars on challenge photos */
.sk-row{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:4px 0 10px}
.sk-row button{border:0;cursor:pointer;padding:9px 4px 8px;border-radius:14px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #BFDCC8;color:#21784A;display:flex;flex-direction:column;align-items:center;gap:2px}
.sk-row b{font:900 1.35rem/1 Fraunces,serif}.sk-row small{font:700 .78rem "Nunito Sans",sans-serif;color:#4E433C}
.sk-row button[aria-checked="true"]{background:linear-gradient(180deg,#2E9A5C,#21784A);box-shadow:0 5px 12px -6px rgba(33,120,74,.7);color:#fff}.sk-row button[aria-checked="true"] small{color:#E6F5EC}
.bcc-ph{position:relative}
.bcc-ys{position:absolute;left:8px;bottom:8px;display:inline-flex;align-items:baseline;gap:5px;padding:5px 10px;border-radius:999px;background:linear-gradient(180deg,#FFF6DA,#F7DF97);box-shadow:0 3px 8px rgba(0,0,0,.35),inset 0 0 0 1.5px #E0B860;font:900 1.05rem Fraunces,serif;font-style:normal;color:#3A2600}
.bcc-ys small{font:800 .68rem "Nunito Sans",sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#6A4A10}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('stakes ok')
