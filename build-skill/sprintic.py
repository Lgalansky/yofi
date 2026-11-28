# Skill preview: Sprint uses the pyramid icon everywhere (user request: "4 levels, 1 v 1").
#  - Sprint game screen: pyramid next to the title (was a stopwatch), line "4 rounds of 1 v 1 · 16 photos",
#    and the field tile shows the pyramid (was a trophy).
#  - Compete › Tournaments row: pyramid (was a stopwatch).
# Usage: python3 build-skill/sprintic.py in.html out.html  (run after ctafix.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a)); s = s.replace(a, b)
R("gameSheet({ ic: kind === 'big' ? '🏆' : '⏱', nm, what: '16-photo knockout · 1 v 1 rounds to the final',",
  "gameSheet({ ic: kind === 'big' ? '🏆' : `<span class=\"gs-pyr\">${KO_PYR2}</span>`, nm, what: kind === 'big' ? '16-photo knockout · 1 v 1 rounds to the final' : '4 rounds of 1 v 1 · 16 photos',")
R("left: gsTile('🏆', '16 photos'), lcap: 'The field<small>Winner and finalist paid</small>'",
  "left: gsTile(kind === 'big' ? '🏆' : `<span class=\"gs-pyr2\">${KO_PYR2}</span>`, '16 photos'), lcap: 'The field<small>Winner and finalist paid</small>'")
R("tour('sprint', '⏱', 'Sprint',", "tour('sprint', `<span class=\"gs-pyr\">${KO_PYR2}</span>`, 'Sprint',")
s = s.replace('</style>', """.gs-pyr{display:inline-flex;vertical-align:-3px}.gs-pyr .ko-pyr{width:30px!important;height:26px!important;filter:none!important;margin:0!important}
.gs-pyr2{display:inline-flex}.gs-pyr2 .ko-pyr{width:64px!important;height:54px!important;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))!important;margin:0!important}
</style>""", 1)
open(p, 'w').write(s); print('sprintic ok')
