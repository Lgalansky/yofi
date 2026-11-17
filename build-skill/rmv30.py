# Real Money build, step 33 (after rmv29.py):
#  - After every Final result (not only in the tutorial), if you have no photo in play: "Enter your own photo · qualify for an
#    upcoming Final and win real cash", with the next Finals and a button to Choose your Final.
#  - Final picks cost $2 / $5 / $10 / $20 / $50 real cash. The free pick is a free $2 pick.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("${S.tut === 3 ? `<div class=\"tut-up\"><b>📷 Get your own photo in a Final</b><span>Every finalist’s creator gets paid. We’ll give you 150 coins to improve your first photo, then it enters the qualifiers.</span>${finSchedHTML(3)}<button class=\"btn block pc-go\" id=\"ppUp\">📷 Add a ${esc(showName(finNext(1)[0].k).toLowerCase())} photo</button></div>` : ''}",
   "${S.tut === 3 || !(S.photos || []).some(p => ['heats', 'q'].includes(rcRec(p.id).st)) ? `<div class=\"tut-up\"><b>📷 Enter your own photo</b><span>Qualify for an upcoming Final and win real cash. The top 2 in each qualifier go through, and every finalist’s creator gets paid.${ffreeFirst() ? ' We’ll give you 150 coins to improve your first photo.' : ''}</span>${finSchedHTML(3)}<button class=\"btn block pc-go\" id=\"ppUp\">📷 Enter a photo</button></div>` : ''}")

# stakes
RA("RACE_ST = [1, 2, 5, 10, 20]", "RACE_ST = [2, 5, 10, 20, 50]")
n = s.count("rec(1, true)"); assert n >= 1, n; s = s.replace("rec(1, true)", "rec(2, true)")
for a, b in [("S.pp[g.sl].stake = (S.pp[g.sl].stake || 1) + 1;", "S.pp[g.sl].stake = (S.pp[g.sl].stake || 2) + 2;"),
             ("🎟️ Add a free $1 · ${FREE_BET_COINS} 🟡", "🎟️ Add a free $2 · ${FREE_BET_COINS} 🟡"), ("'🎟️ Free $1 added to your pick'", "'🎟️ Free $2 added to your pick'"),
             ("`🎟️ Free $1 pick · ${FREE_BET_COINS} 🟡`", "`🎟️ Free pick · ${FREE_BET_COINS} 🟡`"), ("'🎟️ Free $1 pick in! Watch it live.'", "'🎟️ Free pick in! Watch it live.'"),
             ("'free $1 pick' : `${money(st)} pick`", "'free pick' : `${money(st)} pick`"), ("Your first $1 pick is on us.", "Your first pick is on us."),
             ("🎀 Pick the ${nm} Final · from $1", "🎀 Pick the ${nm} Final · from $2"), ("🎟️ Free $1 Final pick · ${FREE_BET_COINS} 🟡", "🎟️ Free Final pick · ${FREE_BET_COINS} 🟡"),
             ("💵 Final pick for real · from $1", "💵 Final pick for real · from $2"), ("'pick from $1' : 'free $1 pick'", "'pick from $2' : 'free pick'"), ("You’ve used both free $1 Final picks this hour.", "You’ve used both free Final picks this hour.")]:
    assert a in s, a; s = s.replace(a, b)
open(d + 'yofi-real.html', 'w').write(s); print('rm v30 ok')
