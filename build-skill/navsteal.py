# Skill preview: a Steal button on the Vote screen, right under the two photos (not in the menu).
#  "🃏 Steal a card · Free try · first to 5 votes" with a navy "3 left" pill (free = navy).
#  If a rival holds one of your cards it becomes gold "Win Milo back · Emma has it · free try".
#  With no tries left it reads "Back tomorrow". The Live games row drops its own steal tiles so
#  the same offer isn't shown twice.
# usage: python3 build-skill/navsteal.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)

# the Live games row no longer carries the steal tiles (the button below the photos does)
rep("  if (held) T({ hot: 1, img: held.src, chip: '🃏 Stolen',", "  if (held && 0) T({ hot: 1, img: held.src, chip: '🃏 Stolen',")
rep("  if (rc && !held) T({ img: rc.src, chip: '🃏 Steal',", "  if (rc && !held && 0) T({ img: rc.src, chip: '🃏 Steal',")

JS = r'''
// ---- Steal button under the vote photos ----
function vsPaint() { const j = $('#judge'); if (!j) return; const lg = j.querySelector('.lgx-wrap'), foot = lg || j.querySelector('.jfoot') || j.querySelector('#jcard'); if (!foot) return;
  const held = S.photos.find(p => p.heldBy), rc = typeof rivalCards === 'function' ? rivalCards() : [], left = typeof stlLeft === 'function' ? stlLeft() : 0;
  if (!held && !rc.length) { const o = j.querySelector('.vst'); if (o) o.remove(); return; }
  const imgs = held ? [held.src] : [rc[0].src, (rc[1] || rc[0]).src];
  const sig = [held ? held.id : 'n', left, imgs.join()].join('|'); let b = j.querySelector('.vst');
  if (b && b.dataset.sig === sig && b.nextElementSibling === foot) return;
  if (!b) { b = document.createElement('button'); b.className = 'vst'; }
  b.classList.toggle('hot', !!held); b.dataset.sig = sig;
  b.innerHTML = `<span class="vst-fan">${imgs.map(x => `<img src="${x}" alt="">`).join('')}</span><span class="vst-tx"><b>${held ? `Win ${esc(alName(held))} back` : 'Steal a card'}</b><small>${held ? `${esc(rvName(held.heldBy))} has it · free try` : 'Free try · first to 5 votes'}</small></span><em>${left ? `${left} left ›` : 'Back tomorrow'}</em>`;
  b.onclick = () => stealSheet(held ? { back: held.id } : {}); foot.before(b); }
new MutationObserver(() => { try { const j = $('#judge'), b = j && j.querySelector('.vst'), lg = j && j.querySelector('.lgx-wrap'); if (!b || (lg && b.nextElementSibling !== lg)) vsPaint(); } catch (e) {} }).observe($('#judge'), { childList: true });
setInterval(() => { try { if ($('#panes').dataset.at === 'judge') vsPaint(); } catch (e) {} }, 2000); setTimeout(() => { try { vsPaint(); } catch (e) {} }, 500);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Steal button under the vote photos */
html body #judge .vst{display:flex;align-items:center;gap:12px;width:calc(100% - 32px);margin:12px 16px 0;padding:8px 12px 8px 8px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;text-align:left;font-family:inherit;cursor:pointer;box-sizing:border-box}
html body #judge .vst.hot{background:#FFF3D6;box-shadow:inset 0 0 0 2px #E0A82E}
.vst-fan{position:relative;width:54px;height:46px;flex:none}.vst-fan img{position:absolute;width:34px;height:44px;border-radius:7px;object-fit:cover;box-shadow:0 0 0 2px #E0A82E,0 3px 6px rgba(0,0,0,.25)}
.vst-fan img:first-child{left:0;top:2px;transform:rotate(-10deg)}.vst-fan img:nth-child(2){right:0;top:0;transform:rotate(8deg)}.vst-fan img:only-child{left:10px;transform:rotate(-4deg)}
.vst-tx{flex:1;min-width:0}.vst-tx b{display:block;font:900 1.02rem Fraunces,serif;color:#2D2521;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.vst-tx small{display:block;font:700 .78rem "Nunito Sans";color:#4E433C;white-space:nowrap}
html body #judge .vst em{flex:none;padding:7px 12px;border-radius:12px;background:#2D4E86;color:#fff;font:900 .82rem "Nunito Sans";font-style:normal}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('navsteal ok')
