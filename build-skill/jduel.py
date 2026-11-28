# Skill preview: a Judge Duel special tile while voting (user request, user's art in assets/judgeduel.jpg).
#  About 1 in 25 right votes the face-down special tile holds the Judge Duel card (red / blue judges' paddles).
#  Three taps crack it open with a blue-and-red glow and sparks, then the Judge Duel game screen opens and the player
#  chooses whether to play. No photo needed, so it can show for players who only vote.
# Usage: python3 build-skill/jduel.py in.html out.html  (run after tilefit.py)
import sys, os, base64
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
IMG = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'judgeduel.jpg'), 'rb').read()).decode()
def R(a, b):
    global s
    assert s.count(a) == 1, (a[:60], s.count(a)); s = s.replace(a, b)
R("CHL_IMG = '", "JDL_IMG = '" + IMG + "', CHL_IMG = '")
R("roll < .16 && fighters().length ? 'chal' : null", "roll < .16 && fighters().length ? 'chal' : roll < .20 ? 'jduel' : null")
R("kind === 'chal' ? `<img class=\"vf-jk\" src=\"${CHL_IMG}\"", "kind === 'jduel' ? `<img class=\"vf-jk vf-jdl\" src=\"${JDL_IMG}\" alt=\"Judge Duel: your judging vs another judge\">` : kind === 'chal' ? `<img class=\"vf-jk\" src=\"${CHL_IMG}\"")
R("kind === 'chal' ? 'red' : 'silver'", "kind === 'chal' ? 'red' : kind === 'jduel' ? 'blue' : 'silver'")
R("else if (kind === 'chal') {", "else if (kind === 'jduel') { const r = vfRel(fr); vfPop(sh, r.x + r.w / 2, r.y + r.h / 2, ['#2F5BD8', '#E23B3B', '#F3D27A', '#fff'], 40); setTimeout(() => { el.remove(); VF_BUSY = 0; try { QS_SEL = 2; qsSheet(); } catch (e) {} }, 1600); }\n      else if (kind === 'chal') {")
i = s.rfind('</style>'); s = s[:i] + "html body #vfTile .vf-jk.vf-jdl{background:#0B1638!important}\n" + s[i:]
open(p, 'w').write(s); print('jduel ok')
