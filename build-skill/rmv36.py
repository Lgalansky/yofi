# Real Money build, step 39 (after rmv35.py): "You have unused coins" pops open the coins menu, where the ticket waits.
#  - Newbie at 15 votes: pop "You have unused coins · a free ticket" -> Open my coins -> top row "Free ticket earned" -> Final picker.
#  - Coming up during that step: "Free ticket earned · open your coins".
#  - Coin players with 250+ coins: the same "unused coins" pop opens the coins menu (free Final pick row).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("celebrate({ src: (ppGame().ph[0] || {}).src || '', score: '🎟️', title: 'Your free Final pick is ready', text: `You’ve judged ${15} photos. Pick the top 3 of 6 in the <b>${raceName(ppGame().sl)} ${esc(showName(ppGame().k))} Final</b>, free. Top scores share the <b>${ppPool(ppGame().players)}</b> prize pool in real cash.`, cta: '🎟️ Make my free pick', onCta: () => { closeFlow(); ppOpen(); }, later: 'Later' });",
   "celebrate({ src: (ppGame().ph[0] || {}).src || '', score: '🟡', title: 'You have unused coins', text: `You’ve judged ${15} photos and earned a <b>free ticket</b>: a free pick in the <b>${raceName(ppGame().sl)} ${esc(showName(ppGame().k))} Final</b>, with real cash prizes. Open your coins to use it.`, cta: '🟡 Open my coins', onCta: () => { closeFlow(); useGems(); }, later: 'Later' });")
RA("function raceBetRowHTML() { if (isCash()) return '';",
   "function raceBetRowHTML() { if (S.tut === 2) return `<button class=\"ug-r ug-swap ug-tk\" id=\"rbBet\"><span class=\"ug-i\">🎟️</span><span class=\"ug-t\"><b>Free ticket earned</b><small>Your first pick in the ${raceName(ppGame().sl)} Final · free · real cash prizes</small></span><em>Use ›</em></button>`; if (isCash()) return '';")
RA("function fqStart() { try { closeSheet(); } catch (x) {}", "function fqStart() { try { closeSheet(); } catch (x) {} if (S.tut === 2) { ppOpen(); return; }")
RA("em: nd ? `in ${nd} vote${nd === 1 ? '' : 's'}` : 'Now' };",
   "em: nd ? `in ${nd} vote${nd === 1 ? '' : 's'}` : 'Open coins', t2: 1 }; ")
RA("if (x.k === 'fp') { if (S.tut === 2) ppOpen(); else", "if (x.k === 'fp') { if (S.tut === 2) useGems(); else")
# Coming up title once earned
RA("return { ic: '🎟️', t: `<b>Free Final pick</b> · pick the top 3 of 6 · real cash prizes`, k: 'fp'",
   "return { ic: '🎟️', t: S.tut === 2 ? `<b>Free ticket earned</b> · open your coins to use it` : `<b>Free Final pick</b> · pick the top 3 of 6 · real cash prizes`, k: 'fp'")
# 250+ coins nudge -> coins menu
RA("title: `You’ve got ${Math.floor(S.gems).toLocaleString()} coins!`, text: `Use <b>${FREE_BET_COINS} 🟡</b> for a free pick in the <b>${raceName(g.sl)} ${esc(showName(g.k))} Final</b>. Top scores share the <b>${ppPool(g.players)}</b> prize pool in real cash.`, cta: '🎟️ Make a free Final pick', onCta: () => { closeFlow(); ppOpen(); }, later: 'Later' });",
   "title: 'You have unused coins', text: `You’ve got <b>${Math.floor(S.gems).toLocaleString()} 🟡</b>: enough for a free pick in the <b>${raceName(g.sl)} ${esc(showName(g.k))} Final</b>, with real cash prizes. Open your coins to use them.`, cta: '🟡 Open my coins', onCta: () => { closeFlow(); useGems(); }, later: 'Later' });")
s = s.replace('</style>', """html:not(.yg) .ug-r.ug-tk{background:#E6F0DF!important;box-shadow:inset 0 0 0 2px #2F6B3F!important}html.yg .ug-r.ug-tk{background:#10301F!important;box-shadow:inset 0 0 0 2px #21C77A!important}.ug-tk em{font-weight:900}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v36 ok')
