# Skill preview: special-tile card art (Jokers, Steal, Photo Duel, Shield) always shows the whole card inside the
# vote photo's frame, on a dark background, instead of being cropped top and bottom ("JOKER 50" was cut off).
# Usage: python3 build-skill/tilefit.py in.html out.html  (run after shieldfx.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
CSS = """
html body #vfTile .vf-jk{object-fit:contain!important;object-position:50% 50%!important;background:radial-gradient(circle at 50% 40%,#2A2440,#0E0B1A 75%)!important}
"""
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('tilefit ok')
