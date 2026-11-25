# No Wow factor (Skill preview): the overall score is the average of the four touch-up scores
# (Lighting, Composition = Soften background, Colour, Technical = Sharpen details). Wow factor is no longer shown or
# counted; existing photos are rescored once on load. Runs on the source before galleries.py (or on any later stage).
# Usage: python3 build-skill/nowow.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if '/* no wow factor */' in s: sys.exit('nowow already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("    { k: 'subject', name: 'Wow factor', short: 'Wow factor', verb: 'Improve Wow factor', tip: 'Makes your subject pop and draws the eye' },\n", "")
rep("s.total = Math.round((s.light + s.comp + s.colour + s.subject + s.tech) / 5);", "s.total = Math.round((s.light + s.comp + s.colour + s.tech) / 4);", 2)
# Improve: four parts, Suncast raises Composition
for a, b in [("const s = { ...s0 }, K = ['light', 'comp', 'colour', 'subject', 'tech'], target = Math.min(99, s0.total + gain);",
              "const s = { ...s0 }, K = ['light', 'comp', 'colour', 'tech'], target = Math.min(99, s0.total + gain);"),
             ("let need = target * 5 - K.reduce((a, k) => a + s[k], 0), guard = 0;", "let need = target * 4 - K.reduce((a, k) => a + s[k], 0), guard = 0;"),
             ("s.total = Math.min(99, Math.round(K.reduce((a, k) => a + s[k], 0) / 5)); return s;", "s.total = Math.min(99, Math.round(K.reduce((a, k) => a + s[k], 0) / 4)); return s;"),
             ("{ k: 'suncast', t: 'Suncast', v: 'Apply Suncast', g: 4, part: 'subject',", "{ k: 'suncast', t: 'Suncast', v: 'Apply Suncast', g: 4, part: 'comp',")]:
    if a in s: rep(a, b)
JS = r'''
/* no wow factor */
(() => { if (S.noWow) return; (S.photos || []).forEach(p => { if (p.s && p.s.light != null) { p.s.total = Math.round((p.s.light + p.s.comp + p.s.colour + p.s.tech) / 4); p.q = p.s.total >= CFG.QUALIFY; } }); S.noWow = 1; save(); })();
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('nowow ok')
