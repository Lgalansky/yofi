# Real Money build, step 8 (after rmv4.py):
#  - cash players get the free qualifier too, with "Play for real · $1" as the upsell
#  - owner's share: 10% of a qualifier's real $1 entries goes to the owner of the photo that finishes 1st
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# free qualifier for everyone
RA("S.gatePend = 0; save(); gateOpen(isCash()); }, 1200);", "S.gatePend = 0; save(); gateOpen(false); }, 1200);")
RA("if (x.k === 'g') { S.gtN = 0; save(); gateOpen(isCash()); return; }", "if (x.k === 'g') { S.gtN = 0; save(); gateOpen(false); return; }")
RA("pick 3 of 5 · ${isCash() ? `$${GATE_FEE} · win $${GATE_CASH[3]}` : 'free'}`", "pick 3 of 5 · free`")
# owner's share
s = s.replace("function fcNotify() {", "var OWNER_SHARE = .1;\nconst gateEntries = (ns, gi) => 30 + ((ns * 7 + gi * 13) % 50);\nfunction fcNotify() {", 1)
RA("<p class=\"gt-q\">✅ The top 2 go through to the <b>${raceName(G.ns)} Best in Show</b></p>",
   "<p class=\"gt-q\">✅ The top 2 go through to the <b>${raceName(G.ns)} Best in Show</b></p><p class=\"gt-own\">🏆 @${esc(G.ph[top[0]].h || 'owner')} owns the 1st place photo and earned <b>${money(gateEntries(G.ns, G.gi) * GATE_FEE * OWNER_SHARE)}</b> · 10% of ${gateEntries(G.ns, G.gi)} real entries</p>")
RA("if (pl === 1) { S.gems = (S.gems || 0) + HEAT_WIN; setTimeout(paintGems, 100); }",
   "let share = 0; if (pl === 1) { S.gems = (S.gems || 0) + HEAT_WIN; share = +((30 + Math.floor(q() * 50)) * GATE_FEE * OWNER_SHARE).toFixed(2); S.cash = +((S.cash || 0) + share).toFixed(2); S.showWon = +((S.showWon || 0) + share).toFixed(2); r.shareWon = +((r.shareWon || 0) + share).toFixed(2); setTimeout(() => { paintGems(); paintWallet(); }, 100); }")
RA("S.rcPop = { k: 'q', pid: id, pl, sl };", "S.rcPop = { k: 'q', pid: id, pl, sl, share };")
RA("in its qualifier${x.pl === 1 ? ` · +${HEAT_WIN} 🟡` : ''}", "in its qualifier${x.pl === 1 ? ` · +${HEAT_WIN} 🟡${x.share ? ` · <b>+${money(x.share)}</b> owner’s share` : ''}` : ''}")
RA("Best in Show 🥇🥈🥉 win <b>$10 · $5 · $2</b> real cash.</p>", "Best in Show 🥇🥈🥉 win <b>$10 · $5 · $2</b> real cash. Win a qualifier and you get <b>10% of its real entries</b>.</p>")
s = s.replace('</style>', '.gt-own{margin:-2px 0 10px;font-size:.8rem;opacity:.9}\n</style>', 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v5 ok')
