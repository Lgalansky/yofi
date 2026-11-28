# Skill preview: Quick Sprint uses its rival / you avatars everywhere (user request).
#  - Compete › Your eye: the Quick Sprint button shows the two avatars (rival left, you right, as on the game screen)
#    with their eye % pills, instead of two score rings.
#  - Vote › Live games: a Quick Sprint tile after the 1 v 1 tile: avatars VS, "Win $3.20", "Your eye vs a rival",
#    "About 30 seconds", green "Play · $2" (opens the Quick Sprint screen).
#  - Live games: the 1 v 1 tile is called "⚔️ Head-to-head" (same name as its game screen and Compete) and always shows
#    when you have a photo: under 70 it says "Get Milo to 70" with a gold "✨ Touch up" button (opens Improve);
#    a photo already in a game shows "Milo is in a game" with a navy "See game".
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
  " return `<span class=\"qsi-av rv\"><i class=\"qsi-cl\"><img src=\"${v[0]}\" alt=\"A rival\"></i><b>${l ? rvA + '%' : '?'}</b></span><i>VS</i><span class=\"qsi-av me\"><i class=\"qsi-cl\"><img src=\"${v[1]}\" alt=\"You\"></i><b>${l ? a + '%' : '?'}</b></span>`; })()}")
R("  if (best && !inc) T({ wa: best.src,",
  "  { const v = " + AVS + "; if (v && !out.some(t => t.sm === 'Quick Sprint')) T({ pair: v, chip: '🎯 Quick Sprint', big: `Win ${qsM(qsPay(2)[0])}`, sm: 'Your eye vs a rival', go: 'Play · $2', gs: 'About 30 seconds', fn: () => { QS_SEL = 2; qsSheet(); } }); }\n"
  "  if (best && !inc) T({ wa: best.src,")
R("chip: '⚔️ 1 v 1 challenge'", "chip: '⚔️ Head-to-head'")
R("<em class=\"${t.free ? 'nav' : ''}\">${t.go}</em>", "<em class=\"${t.free ? 'nav' : t.gold ? 'gld' : ''}\">${t.go}</em>")
R("  { const v = " + AVS + ";",
  "  if (!best) { const m = S.photos.filter(p => p.s && !p.heldBy).sort((a, b) => b.s.total - a.s.total)[0];\n"
  "    if (m) { const k = m.cat || 'any', low = m.s.total < 70;\n"
  "      T({ pair: [c2NotMine(battleRival(k).src, k), m.src], chip: '⚔️ Head-to-head', big: `Win ${win}`, sm: low ? `Get ${alName(m)} to 70` : `${alName(m)} is in a game`, gs: low ? 'Then play for $1' : 'Result soon',\n"
  "        go: low ? '✨ Touch up' : 'See game', gold: low ? 1 : 0, free: low ? 0 : 1,\n"
  "        fn: () => { if (low) { S.cur = m.id; TU_GAL = false; WALL = false; AL_OPEN = null; save(); go('studio'); try { renderStudio(); } catch (e) {} } else { GV.tab = 'battle'; go('gallery'); renderGallery(); } } }); } }\n"
  "  { const v = " + AVS + ";")
s = s.replace('</style>', """html body #judge .lgx em.gld{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important}
.qsi-av{position:relative;display:inline-block;width:64px;height:64px;flex:none}html body .c3-qs .qsi-av,html body .qsi-av{background:none!important;overflow:visible!important;border-radius:0!important;box-shadow:none!important;padding:0!important;width:64px!important;height:64px!important}html body .qsi-av i.qsi-cl{display:block;width:64px;height:64px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px #B8432F}.qsi-av.me i.qsi-cl{box-shadow:0 0 0 3px #2D4E86}html body .qsi-av img{width:64px!important;height:64px!important;object-fit:cover;transform:scale(1.16)}
.qsi-av b{position:absolute;left:50%;bottom:-8px;transform:translateX(-50%);padding:1px 8px;border-radius:999px;background:#9C3324;color:#fff;font:900 .78rem Fraunces,serif;white-space:nowrap;box-shadow:0 0 0 2px #fff}.qsi-av.me b{background:#24406F}
</style>""", 1)
open(p, 'w').write(s); print('qsicon ok')
