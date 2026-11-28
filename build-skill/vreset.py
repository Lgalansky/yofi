# Skill preview: one-time reset of each photo's vote record (user request).
#  On the next open, every photo's votes (gv), coins earned from votes (gl, and today's gt/gd),
#  lost games (losses) and "out of lives" flag (retired) go back to zero. Photo scores, names,
#  touch-ups, cards, the coin balance and the judge score are untouched. Runs once (S.vrReset).
# usage: python3 build-skill/vreset.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
JS = r'''
// ---- one-time reset of each photo's vote record ----
if (S && S.vrReset !== 1) { (S.photos || []).forEach(p => { ['gv', 'gl', 'gt', 'gd', 'losses', 'retired'].forEach(k => delete p[k]); }); S.vrReset = 1; save(); }
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
open(p, 'w', encoding='utf-8').write(s); print('vreset ok')
