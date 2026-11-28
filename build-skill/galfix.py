# Skill preview: Gallery binder page with no photos in it. The empty sleeves on the first row had no height
# (nothing inside them sets one), so their "+ Add a home photo" labels sat on top of the page title.
# Empty sleeves now keep the same card height as a filled sleeve.
# Usage: python3 build-skill/galfix.py in.html out.html  (run after judgecard.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
CSS = """
html body #studio .a2-grid .a2-sl.empty{min-height:190px!important}html body #studio .a2-grid .a2-sl.empty .a2-box{min-height:190px!important;height:100%!important}
"""
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('galfix ok')
