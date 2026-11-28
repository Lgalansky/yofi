# Skill preview: shields feel earned and you're asked to use them.
#  - The special tile never sits on top of a sheet or pop-up any more (it hides while one is open).
#  - Revealing a Shield: a big gold shield flies from the tile into the 🛡 pill in the header, the pill glows and
#    its number ticks up, so you see where it went.
#  - You're prompted to place it: right after you earn a shield (special tile, 3-day streak, judge rank-up) the
#    "New shield!" sheet opens once the reveal is done: "Put it on your best card. It blocks one steal while you're
#    away." with "🛡 Shield Milo" and "Later". If you still have one unplaced, it asks again once a day on Vote.
# Usage: python3 build-skill/shieldfx.py in.html out.html  (run after cmpquick.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- shield reveal → header pill → "New shield!" prompt ----
(() => {
  let last = S.shields || 0, want = 0;
  const busy = () => !!(document.querySelector('#vfTile') || document.getElementById('raid') || $('#sheet').classList.contains('on') || $('#coach').classList.contains('on') || $('#flow').classList.contains('on'));
  const target = () => riskable().filter(p => !p.shield).sort((a, b) => b.s.total - a.s.total)[0] || null;
  function fly() { const t = document.querySelector('#vfTile .vf-face.front') || document.querySelector('#vfTile'), pill = $('#vfSh'), sh = $('#shell'); if (!t || !pill || !sh) return;
    const a = t.getBoundingClientRect(), b = pill.getBoundingClientRect(), o = sh.getBoundingClientRect(), f = document.createElement('i'); f.className = 'shf-fly'; f.textContent = '🛡';
    f.style.left = (a.left + a.width / 2 - o.left) + 'px'; f.style.top = (a.top + a.height / 2 - o.top) + 'px'; sh.appendChild(f);
    requestAnimationFrame(() => { f.style.transform = `translate(${b.left + b.width / 2 - a.left - a.width / 2}px, ${b.top + b.height / 2 - a.top - a.height / 2}px) scale(.35)`; f.style.opacity = '.9'; });
    setTimeout(() => { f.remove(); pill.classList.remove('shf-glow'); void pill.offsetWidth; pill.classList.add('shf-glow'); }, 900); }
  function prompt(fresh) { const t = target(); if (!t || !(S.shields > 0)) return; S.shPromptDay = dayKey(); save();
    openSheet(`<div class="shs shp"><div class="shp-ic">🛡</div><h2 class="shs-h">${fresh ? 'New shield!' : 'Use your shield'}</h2><p class="shs-p">Put it on your best card. It blocks one steal while you’re away.</p>
      <div class="shp-card"><img src="${t.src}" alt=""><span><b>${esc(alName(t))}</b><small>Earns ${GAL.BASE * galMult(t.s.total)} coins a vote</small></span></div>
      <button class="btn block shs-go" id="shpGo">🛡 Shield ${esc(alName(t))}</button><div style="text-align:center"><button class="link" data-shclose>Later</button></div></div>`);
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
    $('#shpGo').onclick = () => { closeSheet(); window.__shPut && window.__shPut(t); }; }
  const _p = vfShPaint;
  vfShPaint = function () { const n = S.shields || 0, up = n > last; last = n; _p.apply(this, arguments);
    if (up) { want = 1; if (document.querySelector('#vfTile')) setTimeout(fly, 250); } };
  setInterval(() => { try { if (!S.user || busy() || $('#panes').dataset.at !== 'judge') return;
    if (want) { want = 0; setTimeout(() => { if (!busy()) prompt(true); }, 700); return; }
    if ((S.shields || 0) > 0 && S.shPromptDay !== dayKey() && target()) { S.shPromptDay = dayKey(); save(); setTimeout(() => { if (!busy()) prompt(false); }, 2500); } } catch (e) {} }, 1200);
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
body:has(#sheet.on) #vfTile,body:has(#coach.on) #vfTile,body:has(#flow.on) #vfTile{visibility:hidden!important}
.shf-fly{position:absolute;z-index:90;margin:-40px 0 0 -40px;width:80px;height:80px;display:grid;place-items:center;font-size:3.2rem;font-style:normal;pointer-events:none;border-radius:50%;background:radial-gradient(circle,#FFE9A3,rgba(255,201,60,.0) 70%);filter:drop-shadow(0 6px 10px rgba(0,0,0,.35));transition:transform .85s cubic-bezier(.5,-.3,.6,1),opacity .85s}
#vfSh.shf-glow{animation:shfGlow 1.2s ease-out}@keyframes shfGlow{0%{transform:scale(1)}25%{transform:scale(1.35);box-shadow:0 0 0 6px rgba(255,201,60,.55),0 0 22px rgba(255,201,60,.9)}100%{transform:scale(1);box-shadow:none}}
.shp{text-align:center!important}.shp-ic{margin:4px auto 2px;width:74px;height:74px;display:grid;place-items:center;font-size:2.6rem;border-radius:50%;background:radial-gradient(circle at 50% 35%,#2A3F6E,#14213D 70%);box-shadow:0 0 0 3px #D9AE4F,0 0 0 8px rgba(217,174,79,.22);animation:shpIn .6s cubic-bezier(.2,1.6,.4,1)}@keyframes shpIn{from{transform:scale(.3) rotate(-25deg)}}
.shp-card{display:flex;align-items:center;gap:12px;margin:0 0 14px;padding:10px;border-radius:16px;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #D9B467;text-align:left}.shp-card img{width:58px;height:58px;border-radius:12px;object-fit:cover}.shp-card b{display:block;font:900 1.15rem Fraunces,Georgia,serif;color:#14213D}.shp-card small{font-size:.82rem;color:#6B5B4B}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('shieldfx ok')
