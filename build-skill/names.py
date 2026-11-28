# Skill preview: games are named by what competes (user chose option A).
#  📷 your photo competes:   Head-to-head -> Photo Duel,   Sprint -> Photo Knockout
#  🎯 your judging competes: Quick Sprint -> Judge Duel
#  Plain-text swap over the whole app, so names used in code comparisons change on both sides together.
#  Lower-case "sprint" (ids such as tourSheet('sprint')) is untouched. "Crowd Sprint" was the Crowd Championship.
#  Compete tabs use the same words: "📷 Photo games | 🎯 Judge games" (was Your photo | Your eye).
# Usage: python3 build-skill/names.py in.html out.html  (run last, after qsicon.py)
import sys, re
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
for a, b in [('Quick Sprint', 'Judge Duel'), ('Crowd Sprint', 'Crowd Championship'), ('CROWD SPRINT', 'CROWD CHAMPIONSHIP'),
             ('Cash head-to-head', 'Cash Photo Duel'), ('Head-to-head', 'Photo Duel')]:
    assert a in s, a
    s = s.replace(a, b)
for a, b in [('aria-selected="${t === \'photo\'}">📷 Your photo</button>', 'aria-selected="${t === \'photo\'}">📷 Photo games</button>'),
             ('aria-selected="${t === \'eye\'}">🎯 Your eye$', 'aria-selected="${t === \'eye\'}">🎯 Judge games$'),
             ('<span class="c3-et"><small>Your eye</small>', '<span class="c3-et"><small>Your judge score</small>')]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
s, n = re.subn(r'\bSprint\b', 'Photo Knockout', s)
assert n > 0
open(p, 'w').write(s); print('names ok', n)
