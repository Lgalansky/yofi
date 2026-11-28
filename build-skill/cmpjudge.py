# Skill preview: Compete › Judge games matches the Photo games tab (user request). The judge score card is gone
# (your score lives behind the 🔥 pill), the "1 v 1 now" Judge Duel card is gone, and the tab reads Tournaments
# (Crowd Championship) then one "⚡ Quick games" row: Judge Duel · Photo Duel (same small buttons as Photo games).
#  The "Every vote trains your eye · Keep voting" link is gone too.
# Usage: python3 build-skill/cmpjudge.py in.html out.html  (run after jduel.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- Compete › Judge games: tournaments, then the quick games row ----
(() => { const _ce = c2Eye;
  c2Eye = function () { const h = _ce.apply(this, arguments);
    try { const t = document.createElement('div'); t.innerHTML = h; const kill = el => el && el.parentNode && el.parentNode.removeChild(el);
      t.querySelectorAll('.c3-eye, .c3-qs').forEach(kill); [...t.querySelectorAll('h3.c2-h')].forEach(x => { if (/1 v 1/.test(x.textContent)) kill(x); }); [...t.querySelectorAll('button')].forEach(x => { if (/Every vote trains/.test(x.textContent)) kill(x); });
      const best = fighters()[0];
      t.insertAdjacentHTML('beforeend', `<h3 class="c2-h">⚡ Quick games</h3><div class="cq-row">
        <button class="cq" data-c2r="qs"><span>🎯</span><b>Judge Duel</b><small>from $2</small></button>
        <button class="cq" data-c2r="${best ? 'h2h' : 'need'}"><span>⚔️</span><b>Photo Duel</b><small>from $1</small></button></div>`);
      return t.innerHTML; } catch (e) { return h; } };
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
open(p, 'w').write(s); print('cmpjudge ok')
