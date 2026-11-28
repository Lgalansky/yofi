# Skill preview: Sprint uses the pyramid icon everywhere (user request: "4 levels, 1 v 1").
#  - Sprint game screen: pyramid next to the title (was a stopwatch), line "4 rounds of 1 v 1 · 16 photos",
#    and the field tile shows the pyramid (was a trophy).
#  - Compete › Tournaments row: pyramid (was a stopwatch).
#  - Showdown uses a race icon (5 pins racing to a chequered finish line; user's mock-up) on its Compete row,
#    game screen and result, and reads "5 entries · top vote wins" (row) / "5 entries · top vote-getter wins" (game screen).
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
SD_SVG = ('<svg class="sd-race" viewBox="0 0 48 36" aria-hidden="true">'
  + ''.join(f'<path d="M2 {y-1.3}L{x-3} {y-0.8}L{x-3} {y+0.8}L2 {y+1.3}Z" fill="{c}"/><circle cx="{x}" cy="{y}" r="3.4" fill="{c}"/>' for y, x, c in [(4, 25, '#E0A82E'), (10, 17, '#FBF3DC'), (16, 22, '#E0A82E'), (22, 34, '#FBF3DC'), (28, 19, '#E0A82E'), (34, 24, '#FBF3DC')])
  + ''.join(f'<rect x="{40 + (i % 2) * 3}" y="{i * 3}" width="3" height="3" fill="#fff"/><rect x="{43 - (i % 2) * 3}" y="{i * 3}" width="3" height="3" fill="#111"/>' for i in range(12))
  + '</svg>')
s = s.replace("const KO_PYR2 =", "const SD_RACE = '" + SD_SVG + "';\nconst KO_PYR2 =", 1) if s.count("const KO_PYR2 =") == 1 else s
R("tour('sd', '⚡', 'Showdown', '5 photos · one vote',", "tour('sd', `<span class=\"gs-sd\">${SD_RACE}</span>`, 'Showdown', '5 entries · top vote wins',")
R("gameSheet({ ic: '⚡', nm: 'Showdown', what: '5 photos, one room · voters pick',", "gameSheet({ ic: `<span class=\"gs-pyr\">${SD_RACE}</span>`, nm: 'Showdown', what: '5 entries · top vote-getter wins',")
R("gsResultSheet({ ic: '⚡', nm: 'Showdown',", "gsResultSheet({ ic: `<span class=\"gs-pyr\">${SD_RACE}</span>`, nm: 'Showdown',")
s = s.replace('</style>', """.gs-pyr{display:inline-flex;vertical-align:-3px}.gs-pyr .ko-pyr{width:30px!important;height:26px!important;filter:none!important;margin:0!important}
.gs-pyr .sd-race{width:34px;height:26px}.gs-pyr .sd-race [fill="#FBF3DC"]{fill:#2D4E86}.gs-pyr .sd-race [fill="#fff"]{stroke:#111;stroke-width:.3}.gs-sd{display:inline-flex}.gs-sd .sd-race{width:40px;height:30px}
.gs-pyr2{display:inline-flex}.gs-pyr2 .ko-pyr{width:64px!important;height:54px!important;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))!important;margin:0!important}
</style>""", 1)
open(p, 'w').write(s); print('sprintic ok')
