# Skill preview: a lost game offers at most two actions (option B).
#  If the photo you played with scores under 75, the main button becomes gold "✨ Touch up <name>"
#  (opens Improve on that photo) and the rematch moves down to the link. Otherwise you get the
#  rematch button and the "Back" link. The old third "Touch up your photo first" link is gone.
#  Card steals are left out (the lost card is held by the rival, so you can't touch it up).
# usage: python3 build-skill/losetip.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- lost result: two actions; a weak photo gets "Touch up" first ----
const LT_MIN = 75;
function ltTidy() { const w = document.querySelector('#sheetBody .pj.gs.gr.lost'); if (!w || w.dataset.lt) return;
  const main = w.querySelector('.gr-acts .btn, #grGo'), link = w.querySelector('.pj-how'); if (!main || !link) return; w.dataset.lt = 1;
  w.querySelectorAll('.gr-tip').forEach(x => x.remove());
  if (/🃏/.test((w.querySelector('.pj-t') || {}).textContent || '')) return;
  const im = w.querySelector('.pj-me img'), ph = im && S.photos.find(x => x.src === im.getAttribute('src') || x.src === im.src);
  if (!ph || !ph.s || ph.s.total >= LT_MIN) return;
  const reTxt = main.textContent.trim(), reFn = main.onclick;
  const nb = document.createElement('button'); nb.className = 'btn block lt-gold'; nb.textContent = `✨ Touch up ${alName(ph)}`;
  nb.onclick = () => { closeSheet(); S.cur = ph.id; TU_GAL = false; WALL = false; AL_OPEN = null; save(); go('studio'); try { renderStudio(); } catch (e) {} };
  main.replaceWith(nb);
  const nl = link.cloneNode(false); nl.removeAttribute('data-shclose'); nl.removeAttribute('id'); nl.textContent = reTxt; nl.onclick = e => { if (reFn) reFn.call(main, e); };
  link.replaceWith(nl);
  const box = w.querySelector('.gr-box span'); if (box) box.textContent = `${alName(ph)} scores ${ph.s.total} · touch it up to win more votes`; }
new MutationObserver(() => { try { ltTidy(); } catch (e) {} }).observe($('#sheetBody'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
html body #sheetBody .lt-gold{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important;box-shadow:0 8px 18px -8px rgba(160,110,10,.7)!important;font-weight:900}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('losetip ok')
