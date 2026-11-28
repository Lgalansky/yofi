# Skill preview: the judge card (tap the 🔥 pill) redone to the user's "Judge status" mock-up.
#  - "Judge status" title; a Current rank card: big gold-ringed navy medallion, the rank name, "28% accuracy",
#    "You picked the crowd favourite in 9 of your last 32 votes." (before 20 votes: "New judge · vote N more").
#  - Rank progression: the four ranks as a ladder of medallions (Good Eye 👁️, Sharp Eye 🦅 65%, Expert 🏅 75% +1 coin
#    a correct vote, Master 👑 85% +2), with "Current rank" / "Next rank · 65% accuracy" / "Top rank".
#  - Two tiles: League position (#8) and Judging streak (1 day, with what's left today).
#  - One navy "Keep voting" button. The old goals rows and 3-row league list are gone (the 8-of-10 bonus still pays).
# Usage: python3 build-skill/judgecard.py in.html out.html  (run after jartext.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- judge status (user's mock-up) ----
judgeCard = function () { const l = jgLv(), nx = jgNext(), a = jgAcc(), h = jgHist(), ok = h.reduce((x, y) => x + (y ? 1 : 0), 0), ds = dailyState(), L = jgLeague();
  const IC = { 'Good Eye': '👁️', 'Sharp Eye': '🦅', 'Expert': '🏅', 'Master': '👑' }, cur = l ? JG_LV.indexOf(l) : -1;
  const med = (n, big) => `<span class="js-med${big ? ' big' : ''}"><i>${IC[n] || '🎯'}</i></span>`;
  const top = l ? `<div class="js-cur"><p class="js-k">Current rank</p><div class="js-row">${med(l.n, 1)}<b class="js-n">${l.n}</b></div>
      <p class="js-acc">${a}% accuracy</p><p class="js-why">You picked the crowd favourite in ${ok} of your last ${h.length} votes.</p></div>`
    : `<div class="js-cur"><p class="js-k">Current rank</p><div class="js-row">${med('', 1)}<b class="js-n">New judge</b></div>
      <p class="js-acc">${jgN()} of ${JG_MIN} votes</p><p class="js-why">Vote ${JG_MIN - jgN()} more to get your rank.</p></div>`;
  const lad = JG_LV.map((r, i) => { const st = i === cur ? 'cur' : i === cur + 1 ? 'next' : i < cur ? 'done' : 'lock';
    const sub = st === 'cur' ? '' : i === JG_LV.length - 1 ? `Top rank · ${r.at}% accuracy` : st === 'next' ? (r.at ? `Next rank · ${r.at}% accuracy` : `First rank · after ${JG_MIN} votes`) : st === 'done' ? 'Reached' : `${r.at}% accuracy`;
    const perk = r.bonus ? ` · +${r.bonus} ${gemIcon('js-ci')} a correct vote` : '';
    return `<div class="js-l ${st}">${med(r.n)}<span><b>${r.n}${st === 'cur' ? '<em>Current rank</em>' : ''}</b>${sub || perk ? `<small>${sub}${perk}</small>` : ''}</span></div>`; }).join('');
  const done = ds.D.last === ds.t, n = done ? 3 : Math.min(3, ds.D.n || 0), stk = ds.streak || 0;
  openSheet(`<div class="js"><h2 class="js-h">Judge status</h2>${top}<h3 class="js-h3">Rank progression</h3><div class="js-lad">${lad}</div>
    <div class="js-tiles"><div class="js-t"><p class="js-k">League position</p><b>${l ? '#' + L.rank : '–'}</b><small>${l ? `of ${L.of} judges like you` : `After ${JG_MIN} votes`}</small></div>
      <div class="js-t"><p class="js-k">Judging streak</p><b>${stk} day${stk === 1 ? '' : 's'}</b><small>${done ? 'Today counted' : `Vote ${3 - n} more today`}</small></div></div>
    <button class="btn block js-go" data-shclose>Keep voting</button></div>`);
  document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet()); };
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
html body #sheetBody .js{text-align:left;color:#14213D}.js-h{margin:2px 0 14px!important;text-align:center;font:900 2rem/1.1 Fraunces,Georgia,serif!important;color:#14213D!important}
.js-k{margin:0;font:800 .72rem "Nunito Sans",Nunito,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#5F534A}
.js-cur{padding:14px 16px;border-radius:18px;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #D9B467,0 6px 16px -10px rgba(60,40,20,.4)}
.js-row{display:flex;align-items:center;gap:14px;margin:8px 0 6px}.js-n{font:900 2rem/1.05 Fraunces,Georgia,serif;color:#14213D}
.js-acc{margin:4px 0 2px;font:900 1.35rem Fraunces,Georgia,serif;color:#14213D}.js-why{margin:0;font-size:.92rem;color:#4E433C}
.js-med{flex:none;display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:radial-gradient(circle at 50% 35%,#2A3F6E,#14213D 70%);box-shadow:0 0 0 2.5px #D9AE4F,0 3px 8px rgba(0,0,0,.25)}
.js-med i{font-style:normal;font-size:1.35rem;line-height:1;filter:saturate(.9)}.js-med.big{width:76px;height:76px;box-shadow:0 0 0 3px #D9AE4F,0 0 0 7px rgba(217,174,79,.22),0 6px 14px rgba(0,0,0,.25)}.js-med.big i{font-size:2.3rem}
.js-h3{margin:18px 0 10px!important;font:900 1.35rem Fraunces,Georgia,serif!important;color:#14213D!important}
.js-lad{position:relative;display:flex;flex-direction:column;gap:12px;padding-left:4px}.js-lad::before{content:"";position:absolute;left:27px;top:20px;bottom:20px;width:2.5px;background:#D9AE4F;opacity:.7}
.js-l{position:relative;display:flex;align-items:center;gap:14px}.js-l>span{min-width:0}.js-l b{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font:900 1.15rem Fraunces,Georgia,serif;color:#14213D}
.js-l b em{font:800 .74rem "Nunito Sans",Nunito,sans-serif;font-style:normal;padding:3px 10px;border-radius:999px;background:#F6E1A6;color:#3A2600}
.js-l small{display:flex;align-items:center;gap:3px;font-size:.84rem;color:#5F534A}.js-l small .js-ci{width:14px;height:14px}
.js-l.lock{opacity:.55}.js-l.done .js-med{box-shadow:0 0 0 2.5px #2E6B42,0 3px 8px rgba(0,0,0,.25)}.js-l.cur .js-med{box-shadow:0 0 0 3px #E0A82E,0 0 0 7px rgba(224,168,46,.25)}
.js-tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:18px 0 14px}.js-t{padding:12px 10px;border-radius:16px;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #E2D5BE;text-align:center}
.js-t b{display:block;margin:4px 0 2px;font:900 1.9rem/1.05 Fraunces,Georgia,serif;color:#14213D}.js-t small{font-size:.78rem;color:#5F534A}
html body #sheetBody .js .js-go{background:#14213D!important;color:#fff!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('judgecard ok')
