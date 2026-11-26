# Skill preview: a calm first-upload journey in the right order.
#   1. pick a photo (or a sample)  2. "Name your photo" with the photo shown  3. the scan
#   4. land straight on Improve, the score counting up from 0, with any welcome gift
# The old "Touch up your photo" result screen no longer flashes for new uploads, and the
# name is never asked after the score.
# usage: python3 build-skill/upflow.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)

# 2. name before the scan
rep("  openFlow(`<div class=\"scan\"><img src=\"${src}\" alt=\"Your photo\"></div><p class=\"scanmsg\" id=\"scanMsg\">Checking lighting…</p>`, false);",
    "  const upName = window.upAskName ? await window.upAskName(src) : null;\n  openFlow(`<div class=\"scan\"><img src=\"${src}\" alt=\"Your photo\"></div><p class=\"scanmsg\" id=\"scanMsg\">Checking lighting…</p>`, false);")
rep("const p = { id: uid(), src, orig: src, s, start: s.total, enh: 0, q: s.total >= CFG.QUALIFY, at: Date.now() };",
    "const p = { id: uid(), src, orig: src, s, start: s.total, enh: 0, q: s.total >= CFG.QUALIFY, at: Date.now(), nm: upName || undefined, nmAsk: 1 };")

JS = r'''
// ---- first-upload journey: name → scan → Improve ----
function upAskName(src) { return new Promise(done => {
  const sug = (AL_NAMES[window.__preCat] || AL_NAMES.pets || ['Photo'])[S.photos.length % 6] || 'Photo';
  openSheet(`<div class="nm-ask"><h2>Name your photo</h2><p class="sub">It shows on its card and when voters pick it.</p><img class="nm-ph" src="${src}" alt=""><input id="upNm" maxlength="16" value="${esc(sug)}" aria-label="Photo name"><button class="btn block" id="upNmGo">Score my photo</button></div>`);
  const fin = () => { const v = ($('#upNm').value || '').trim(); closeSheet(); setTimeout(() => done(v || sug), 250); };
  $('#upNmGo').onclick = fin; $('#upNm').onkeydown = e => { if (e.key === 'Enter') fin(); };
  setTimeout(() => { try { $('#upNm').select(); } catch (e) {} }, 300); }); }
window.upAskName = upAskName;
// the collection map waits: the score reveal is the moment; the map shows next time Gallery opens
const _showMapU = showMap;
showMap = function (o) { if (!o && window.__upLand && Date.now() - window.__upLand < 8000) { S.mapSeen = 0; save(); return; } return _showMapU.apply(this, arguments); };
// 4. new uploads land on Improve, the score counting up; no old result screen
const _showResultU = showResult;
showResult = function (p, o = {}) {
  if (!o.fresh || o.prevTotal != null || !p) return _showResultU.apply(this, arguments);
  window.__upLand = Date.now();
  try { closeFlow(); } catch (e) {} S.cur = p.id; TU_GAL = false; WALL = false; AL_OPEN = null; save(); go('studio'); try { renderStudio(); } catch (e) {}
  setTimeout(() => { const sc = $('#i2Score'); if (sc) { const b = p.s.total, t0 = performance.now(); sc.classList.add('up-rev'); const tick = n => { const k = Math.min(1, (n - t0) / 1100); sc.textContent = Math.round(b * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); }; sc.textContent = '0'; requestAnimationFrame(tick); } }, 120);
  if (o.win) setTimeout(() => { try { gemExplosion(o.win, { label: o.first ? 'Welcome gift' : 'Daily upload bonus', from: $('#i2Score') }); } catch (e) {} }, 1400);
  try { galCheck(); } catch (e) {}
};
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
#i2Score.up-rev{animation:upRev 1.2s ease-out}
@keyframes upRev{0%{transform:scale(.6);opacity:.3}60%{transform:scale(1.15);opacity:1}100%{transform:none}}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('upflow ok')
