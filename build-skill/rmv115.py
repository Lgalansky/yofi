# Real Money build, step 118 (after rmv114.py): coins can't be used on the Final pick screens.
#  The only way coins reach a Final is the free Final ticket in the coins menu (250 coins, up to 2 an hour).
#  - Opened normally (Finals tab, landing, Finalists, results), the Top 3 and Winner tabs show cash picks only:
#    stake row + green button. No "Free pick · 250" buttons.
#  - Opened from the coins menu's Free Final pick row (or a new player's free ticket), the screen is in ticket mode:
#    "Use your free ticket" on Top 3, and on Winner too (with the cash option still underneath). The ticket mode ends
#    when the pick is placed.
#  - Finals tab: the navy "Free pick · 250 coins" button is removed.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function fqStart() { try { closeSheet(); } catch (x) {}", "function fqStart() { window.__tk = Date.now(); try { closeSheet(); } catch (x) {}")
RA("cash = isCash() || !!pc", "cash = !(S.tut === 2 || (window.__tk && Date.now() - window.__tk < 600000))")
RA("const rec = (st, free) => { S.pp = S.pp || {};", "const rec = (st, free) => { if (free) window.__tk = 0; S.pp = S.pp || {};")
RA("const rec = (st, free) => { S.pw = S.pw || {};", "const rec = (st, free) => { if (free) window.__tk = 0; S.pw = S.pw || {};")
i = s.index('${freeOk ? `<button class="btn block fn-nv" id="fnFree">'); j = s.index("` : ''}", i) + len("` : ''}"); s = s[:i] + s[j:]
s = s.replace("<button class=\"btn block pc-go pk-go\" id=\"wpFree\" ${pick != null ? '' : 'disabled'}>${pick == null ? 'Choose your winner' : `🎟️ Free winner pick · ${FREE_BET_COINS} 🟡`}</button>",
              "<button class=\"btn block pc-go pk-go\" id=\"wpFree\" ${pick != null ? '' : 'disabled'}>${pick == null ? 'Choose your winner' : '🎟️ Use your free ticket'}</button>")
s = s.replace("${!freeOk && !cash ? `<p class=\"pp-r\">${!fqLeft() ? 'Both free picks used this hour' : `${FREE_BET_COINS - Math.floor(S.gems || 0)} more 🟡 for a free winner pick · ${isYoungW() ? 'judge' : 'vote'} to earn them`}</p>` : ''}", "")
open(d + 'yofi-real.html', 'w').write(s); print('rm v115 ok')
