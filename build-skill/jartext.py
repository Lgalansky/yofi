# Skill preview: the coin jar card on Vote says plainly whose photo earned what (user chose option A).
#  Was "A voter picked Milo · Jar full in 2h 32m · +4". Now:
#   "Milo earned you 4 coins" / fill bar / "Full in 2h 32m" (the "Players voted for it" line was cut),
#   and the gold button reads "Collect" (the amount is already in the title).
#  Several photos: "Your photos earned you 12 coins". Full jar: "... · Full · collect to keep earning".
#  The upgrade card matches: "Milo can reach Diamond" / "71 → 80 · earns 8 coins a vote", 
#  gold button "Improve" with the cost ("120 🪙") under it (was "Milo’s upgrade is ready · 71 → 80 for Diamond · 120 c…").
# Usage: python3 build-skill/jartext.py in.html out.html  (run after names.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- coin jar card: plain words ----
(() => {
  const _g = vgGoal;
  vgGoal = function () { const g = _g.apply(this, arguments);
    if (g && g.jar) { const n = S.vgJar || 0, mix = S.vgJarMix || !g.p, nm = mix ? 'Your photos' : alName(g.p), full = jarFull();
      g.t = `${nm} earned you ${n} coin${n === 1 ? '' : 's'}`;
      g.s = mix ? 'Players voted for them' : 'Players voted for it';
      g.when = full ? 'Full · collect to keep earning' : `Full in ${jarLeft()}`; }
    else if (g && g.ready && g.p) { const p = g.p, nm = alName(p), nb = [70, 80, 90].find(b => p.s.total < b), tier = nb ? galBand(nb) : '', cost = fixCost(p);
      g.t = tier ? `${nm} can reach ${tier}` : `${nm} can score higher`;
      g.s = nb ? `${p.s.total} → ${nb} · ${GAL.BASE * galMult(nb)} coins a vote` : `Now ${p.s.total} · touch it up`;
      g.cost = cost; }
    return g; };
  const _p = vgPaint;
  vgPaint = function () { _p.apply(this, arguments);
    try { const el = $('#vgGoal'); if (!el) return; const g = vgGoal(), jar = !!(g && g.jar);
      el.querySelectorAll('.jt-yp,.jt-when').forEach(x => x.parentNode.removeChild(x));
      if (g && g.ready && g.p) { const sm = el.querySelector('.vg-tx > small'); if (sm) sm.textContent = g.s;
        el.classList.add('jt-rel');
        const c = el.querySelector('.vg-cta'); if (c && !c.querySelector('.jt-cost')) { c.classList.add('jt-two'); c.innerHTML = `<small class="jt-cl">Improve</small><span class="jt-cost">${g.cost} ${gemIcon('jt-ci')}</span>`; }
        el.setAttribute('aria-label', `${g.t}. ${g.s}. Improve for ${g.cost} coins`); return; }
      if (!jar) return;
      const sm = el.querySelector('.vg-tx > small'); if (sm) sm.parentNode.removeChild(sm);
      const tx = el.querySelector('.vg-tx'); if (tx) tx.insertAdjacentHTML('beforeend', `<small class="jt-when">${esc(g.when)}</small>`);
        el.classList.add('jt-rel');
      const c = el.querySelector('.vg-cta'); if (c && !c.querySelector('.jt-cl')) { c.classList.add('jt-one'); c.innerHTML = '<small class="jt-cl">Collect</small>'; }
      el.setAttribute('aria-label', `${g.t}. ${g.s}. Collect ${g.jar} coins`); } catch (e) {} };
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
s = s.replace('</style>', """html body #vgGoal.jt-rel{position:relative}.jt-yp{position:absolute;z-index:2;padding:1px 7px;border-radius:999px;background:#fff;color:#2D2521;font:800 .66rem "Nunito Sans",Nunito,sans-serif;font-style:normal;box-shadow:0 1px 3px rgba(0,0,0,.25);white-space:nowrap;pointer-events:none}
html body #vgGoal .jt-when{display:block;margin-top:4px;font-size:.78rem;color:#6B5B4B;opacity:1}html body #vgGoal .vg-cta .jt-cl{display:block;font:900 .95rem Fraunces,serif;line-height:1;margin-bottom:2px}
html body #vgGoal .jt-cost{display:inline-flex;align-items:center;gap:4px;font:900 1.05rem Fraunces,serif}html body #vgGoal .jt-cost .jt-ci{display:inline-block!important;width:18px!important;height:18px!important;opacity:1!important;visibility:visible!important}html body #vgGoal .vg-cta.jt-two{text-align:center}
html body #vgGoal .vg-cta:has(.jt-cl){flex-direction:row!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;align-content:center!important;gap:0 4px!important;line-height:1.1;padding:8px 12px!important;min-width:84px}html body #vgGoal .vg-cta .jt-cl{flex:0 0 100%;text-align:center}html body #vgGoal .vg-cta.jt-one .jt-cl{margin:0;font-size:1.1rem}
html body #vgGoal.jt-rel{height:auto!important;min-height:0!important;max-height:none!important;align-items:center!important;padding-top:12px!important;padding-bottom:12px!important;overflow:visible!important}html body #vgGoal.jt-rel .vg-tx{flex:1 1 auto!important;min-width:0!important}html body #vgGoal.jt-rel .vg-tx b{white-space:normal!important;line-height:1.15;display:block!important;-webkit-line-clamp:unset!important;overflow:visible!important;max-height:none!important;font-size:1.08rem!important;text-overflow:clip!important}html body #vgGoal.jt-rel .vg-cta{flex:0 0 auto!important;width:auto!important;max-width:92px!important}html body #vgGoal.jt-rel .vg-tx small{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style>""", 1)
open(p, 'w').write(s); print('jartext ok')
