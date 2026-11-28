# Skill preview: Compete stops repeating the Live games (user chose option B).
#  Compete › Photo games keeps Daily jackpots and Tournaments (Photo Knockout, Showdown), then one small
#  "⚡ Quick games" row: Photo Duel · Judge Duel · Friend (each opens its game; Photo Duel opens Improve when no photo
#  is at 70 yet). The big Photo Duel card, the Challenge a friend row, an incoming-challenge row, Card challenges
#  (stealing lives on Vote) and the Clubs link are gone. The Judge games tab is unchanged.
# Usage: python3 build-skill/cmpquick.py in.html out.html  (run after shields.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- Compete › Photo games: jackpots, tournaments, one quick-games row ----
(() => { const _cp = c2Photo;
  c2Photo = function () { const h = _cp.apply(this, arguments);
    try { const t = document.createElement('div'); t.innerHTML = h;
      const kill = el => el && el.parentNode && el.parentNode.removeChild(el);
      [...t.querySelectorAll('h3.c2-h')].forEach(x => { if (/Photo Duel|Head-to-head|Card challenges/.test(x.textContent)) kill(x); });
      t.querySelectorAll('.c4-card, .c4-row, .c4-panel, .c3-club').forEach(kill);
      const best = fighters()[0];
      t.insertAdjacentHTML('beforeend', `<h3 class="c2-h">⚡ Quick games</h3><div class="cq-row">
        <button class="cq" data-c2r="${best ? 'h2h' : 'need'}"><span>⚔️</span><b>Photo Duel</b><small>from $1</small></button>
        <button class="cq" data-c2r="qs"><span>🎯</span><b>Judge Duel</b><small>from $2</small></button>
        ${best ? `<button class="cq" data-c2r="friend"><span>🤝</span><b>Friend</b><small>from $1</small></button>` : ''}</div>`);
      return t.innerHTML; } catch (e) { return h; } };
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
.cq-row{display:flex;gap:8px;margin:0 14px 14px}.cq{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:2px;padding:10px 6px;border:0;border-radius:14px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;cursor:pointer;color:#14213D}
.cq span{font-size:1.3rem;line-height:1}.cq b{font:800 .88rem "Nunito Sans",sans-serif;white-space:nowrap}.cq small{font:700 .74rem "Nunito Sans",sans-serif;color:#2F7A3F}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('cmpquick ok')
