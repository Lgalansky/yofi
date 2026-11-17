# Real Money build, step 2 (after `YOFI_BUILD=real python3 simplify.py`):
# turns the Skill app + racing into Yofi - Real Money.
#  - own saved data (yofi.real.v1), title and "Real money" badge
#  - mystery tournaments: a spin sets the winner's prize (x10 to x1,000 the entry)
#  - big spins (x100+) are shared prizes, paid down to the last 8
import os
d = os.path.dirname(os.path.abspath(__file__)) + '/'
d = os.environ.get('YOFI_DIR', d)
s = open(d + 'yofi-simple.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:80], s.count(a), n); s = s.replace(a, b)

# own save, title, badge
s = s.replace('yofi.proto.v1', 'yofi.real.v1')
RA('<title>Yofi - Skill (Preview)</title>', '<title>Yofi - Real Money</title>')
RA('<span class="a18-pill" title="Adults only · 18+">18+</span>', '<span class="a18-pill rm-pill" title="Real money · 18+ · Licensed">18+ · Real money</span>')

# mystery slots are not guaranteed-prize slots
RA("const tCfg = () => (S.tour && !S.tour.seen && S.tour.slot) ? S.tour.slot : (!(S.tour && !S.tour.seen) && window.__tSlot) || null;",
   "const tCfg = () => { const c = (S.tour && !S.tour.seen && S.tour.slot) ? S.tour.slot : (!(S.tour && !S.tour.seen) && window.__tSlot) || null; return c && !c.myst ? c : null; };")
# shared prizes on big spins
RA("const tPay = (k, n = T_N) => {",
   "const SHARE = { win: .70, final: .15, semi: .05, quarter: .0125 }; // big spins pay down to the last 8\nconst bigSpin = T => T && T.mult >= 100;\nconst tShare = (T, k) => +(T.fee * T.mult * SHARE[k]).toFixed(2);\nconst tPay = (k, n = T_N) => {")
RA("if (k === 'win' && tMult()) return +(S.tour.fee * S.tour.mult).toFixed(2);",
   "if (tMult() && bigSpin(S.tour) && SHARE[k]) return tShare(S.tour, k); if (k === 'win' && tMult()) return +(S.tour.fee * S.tour.mult).toFixed(2);")
RA("$('#mypT').innerHTML = `Win it and you take <b>${money(T.fee * T.mult)}</b>`;",
   "$('#mypT').innerHTML = big ? `<b>${money(T.fee * T.mult)}</b> prize pool, shared down to the last 8. Winner takes <b>${money(T.fee * T.mult * .7)}</b>` : `Win it and you take <b>${money(T.fee * T.mult)}</b>`;")
RA("    <p>Earlier round wins earn coins</p></div>`;\n}\nfunction tStats",
   "    ${m && bigSpin(S.tour) ? `<div class=\"tk-pr f\"><span class=\"tk-sx\">3–4</span><b>Semi-finalists</b><em>${money(tShare(S.tour, 'semi'))} each</em></div><div class=\"tk-pr f\"><span class=\"tk-sx\">5–8</span><b>Last 8</b><em>${money(tShare(S.tour, 'quarter'))} each</em></div><p>Big spin: the prize is shared down to the last 8</p>` : `<p>${m ? 'Earlier round wins earn coins' : 'Spins of ×100+ pay the last 8 too'}</p>`}</div>`;\n}\nfunction tStats")
# mystery rows in the schedule
RA("if (hr && out.length < 8) out.push({ at, gtd: 5000, gem: true }); }",
   "if (hr && out.length < 8) out.push({ at, gtd: 5000, gem: true }); if (!hr && out.length < 8) out.push({ at, gtd: 0, gem: false, myst: true }); }")
RA("<button class=\"tsr2 ${t.now ? 'now' : ''} ${t.gem ? 'gemt' : ''}\" data-tsl=\"${i}\">",
   "<button class=\"tsr2 ${t.now ? 'now' : ''} ${t.gem ? 'gemt' : ''} ${t.myst ? 'myst' : ''}\" data-tsl=\"${i}\">")
RA("<span class=\"tsr2-p\">${t.gem ? `${gemIcon('')}${t.gtd.toLocaleString()}` : `US$${t.gtd}`}</span>",
   "<span class=\"tsr2-p\">${t.gem ? `${gemIcon('')}${t.gtd.toLocaleString()}` : t.myst ? '🎰 $1,000' : `US$${t.gtd}`}</span>")
RA("window.__tSlot = { gtd: t.gtd, gem: t.gem }", "window.__tSlot = { gtd: t.gtd, gem: t.gem, myst: !!t.myst }")
RA("window.__tSlot = { gtd: t.gtd, gem: false }", "window.__tSlot = { gtd: t.gtd, gem: false, myst: !!t.myst }")
RA("<p class=\"tk-sub\">${window.__tSlot.gem ? `${window.__tSlot.gtd.toLocaleString()} 🟡` : `US$${window.__tSlot.gtd}`} guaranteed ·",
   "<p class=\"tk-sub\">${window.__tSlot.myst ? '🎰 Mystery prize · up to $1,000 ·' : `${window.__tSlot.gem ? `${window.__tSlot.gtd.toLocaleString()} 🟡` : `US$${window.__tSlot.gtd}`} guaranteed ·`}")
RA("t.mult = t.slot ? 0 : mystRoll(); save(); closeSheet(); if (t.slot) openTourney();",
   "t.mult = t.slot && !t.slot.myst ? 0 : mystRoll(); save(); closeSheet(); if (t.slot && !t.slot.myst) openTourney();")
s = s.replace('</style>', """.tsr2.myst .tsr2-p{font-weight:900}html.yg .tsr2.myst .tsr2-p{color:#FFC93C}html.yg .tsr2.myst{box-shadow:inset 0 0 0 1.5px #8A6A2A}html:not(.yg) .tsr2.myst .tsr2-p{color:#8B3CA8}html:not(.yg) .tsr2.myst{box-shadow:inset 0 0 0 1.5px #C9A6D6}
.tk-sx{display:inline-grid;place-items:center;min-width:30px;height:22px;border-radius:7px;font-size:.72rem;font-weight:900;background:rgba(127,127,127,.18)}
.a18-pill.rm-pill{white-space:nowrap;background:#2F6B3F!important;color:#fff!important;border-color:#2F6B3F!important}html.yg .a18-pill.rm-pill{background:#21C77A!important;color:#0B1A12!important;border-color:#21C77A!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('real money ok')
