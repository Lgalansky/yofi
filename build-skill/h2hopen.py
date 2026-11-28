# Skill preview: no score locks on higher stakes (user request). Every stake ($1 / $5 / $10 head-to-head,
# tournament tiers) is open to any photo; the "🔒 80+" / "🔒 90+" chips and lock pop no longer show.
# Usage: python3 build-skill/h2hopen.py in.html out.html  (run after sprintic.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
a = "tierOpen = f => bestScore() >= T_TIERS[f].min;"
assert s.count(a) == 1
s = s.replace(a, "tierOpen = f => !!T_TIERS[f];")
open(p, 'w').write(s); print('h2hopen ok')
