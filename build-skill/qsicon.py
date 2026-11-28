# Skill preview: Quick Sprint uses its rival / you avatars everywhere (user request).
#  - Compete › Your eye: the Quick Sprint button shows the two avatars (rival left, you right, as on the game screen)
#    with their eye % pills, instead of two score rings.
#  - Vote › Live games: a Quick Sprint tile after the 1 v 1 tile: avatars VS, "Win $3.20", "Your eye vs a rival",
#    "About 30 seconds", green "Play · $2" (opens the Quick Sprint screen).
# Usage: python3 build-skill/qsicon.py in.html out.html  (run after h2hopen.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
def R(a, b):
    global s
    assert s.count(a) == 1, (a[:60], s.count(a)); s = s.replace(a, b)
AVS = "(() => { try { return [AV_RIVAL, (S.user && S.user.pic) || AV_YOU]; } catch (e) { return null; } })()"
R("${ring(l ? a : 50, l ? a + '%' : '?', 'me')}<i>VS</i>${ring(l ? rvA : 50, l ? rvA + '%' : '?', 'them')}",
  "${(() => { const v = " + AVS + "; if (!v) return ring(l ? rvA : 50, l ? rvA + '%' : '?', 'them') + '<i>VS</i>' + ring(l ? a : 50, l ? a + '%' : '?', 'me');"
  " return `<span class=\"qsi-av rv\"><img src=\"${v[0]}\" alt=\"A rival\"><b>${l ? rvA + '%' : '?'}</b></span><i>VS</i><span class=\"qsi-av me\"><img src=\"${v[1]}\" alt=\"You\"><b>${l ? a + '%' : '?'}</b></span>`; })()}")
R("  if (best && !inc) T({ wa: best.src,",
  "  { const v = " + AVS + "; if (v && !out.some(t => t.sm === 'Quick Sprint')) T({ pair: v, chip: '🎯 Quick Sprint', big: `Win ${qsM(qsPay(2)[0])}`, sm: 'Your eye vs a rival', go: 'Play · $2', gs: 'About 30 seconds', fn: () => { QS_SEL = 2; qsSheet(); } }); }\n"
  "  if (best && !inc) T({ wa: best.src,")
s = s.replace('</style>', """.qsi-av{position:relative;display:inline-block;width:64px;height:64px;flex:none}.qsi-av img{width:64px;height:64px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #B8432F}.qsi-av.me img{box-shadow:0 0 0 3px #2D4E86}
.qsi-av b{position:absolute;left:50%;bottom:-8px;transform:translateX(-50%);padding:1px 8px;border-radius:999px;background:#9C3324;color:#fff;font:900 .78rem Fraunces,serif;white-space:nowrap;box-shadow:0 0 0 2px #fff}.qsi-av.me b{background:#24406F}
</style>""", 1)
open(p, 'w').write(s); print('qsicon ok')
