# Real Money build, step 79 (after rmv75.py): review fixes, part 1 (broken items, fewer interruptions).
#  - Invite pop: the coin stack overlapped "for every friend you invite"; now one coin beside "100 coins".
#  - Earnings rows never print "undefinedth"; account sheet never prints "undefined" under the handle.
#  - Pacing: unsolicited pops (daily rewards on open, unused-coins nudge, auto qualifier) keep 90 s apart,
#    and daily rewards wait until the new-player journey is done (first free-pick result).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<span class="iv-stack"><i class="qz3-coin"></i><i class="qz3-coin"></i><i class="qz3-coin"></i></span>', '<i class="qz3-coin iv-c"></i>')
RA("${e.kind === 'f' ? `🎀 Finalist · ${ppOrd(e.place)} · pool share` : e.kind === 'q' ? '🥇 Won its qualifier' : `${PP_MED[e.place - 1] || ''} ${ppOrd(e.place)} in the Final`}",
   "${!e.place ? (e.t ? esc(e.t) : 'Prize') : e.kind === 'f' ? `🎀 Finalist · ${ppOrd(e.place)} · pool share` : e.kind === 'q' ? '🥇 Won its qualifier' : `${PP_MED[e.place - 1] || ''} ${ppOrd(e.place)} in the Final`}")
RA("<p class=\"sub\">${S.user ? esc(S.user.em) : 'Not signed up yet.'}</p>", "<p class=\"sub\">${S.user ? (S.user.em ? esc(S.user.em) : S.user.guest ? 'Guest player' : 'PhotoPicks player') : 'Not signed up yet.'}</p>")
# pacing
RA("function streakHello() {", "function streakHello() { if ((S.tut || 9) < 9 || Date.now() - (window.__autoT || 0) < 90000) return;")
import re
m = re.search(r"if \(ds\.doneToday\) return;\s*streakPop\(\);\s*\}", s); assert m
s = s[:m.start()] + "if (ds.doneToday) return; window.__autoT = Date.now(); streakPop(); }" + s[m.end():]
RA("if (!force && popPaced()) return false;", "if (!force && (popPaced() || Date.now() - (window.__autoT || 0) < 90000)) return false;")
RA("S.gnMark = mark; S.gnVote = S.votes || 0; save(); paintGemGlow();", "S.gnMark = mark; S.gnVote = S.votes || 0; window.__autoT = Date.now(); save(); paintGemGlow();", 3)
RA("if (!S || !S.gatePend || busyUI()", "if (!S || !S.gatePend || busyUI() || Date.now() - (window.__autoT || 0) < 20000")
RA("S.gatePend = 0; save(); gateOpen(false);", "S.gatePend = 0; window.__autoT = Date.now(); save(); gateOpen(false);")
s = s.replace('</style>', """html body .iv2 .iv-c{width:.75em!important;height:.75em!important;font-size:1em;flex:none}html body .iv2 .iv-sub{font-size:1.35rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v76 ok')
