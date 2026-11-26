# Skill preview: small consistency fixes.
# 1. A wrong vote: the "So close! / Missed it" overlay on your tile was dark text on a dark box.
#    It is now a light card with navy text, matching the rest of the Vote screen.
# 2. The score screen after an upload ("Touch up your photo"): every bar row has the same
#    padding so the highlighted row lines up with the rest; rows and the button use the same four
#    touch-up names as Improve (Fix lighting, Boost colour, Sharpen details, Soften background);
#    the button is gold because it spends coins.
# usage: python3 build-skill/polish.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- score screen: same four touch-up names as Improve ----
const TU_NM = { light: 'Fix lighting', colour: 'Boost colour', tech: 'Sharpen details', comp: 'Soften background' };
function rsTidy() { const fb = $('#flowBody'); if (!fb || !fb.querySelector('.rs-top')) return;
  fb.querySelectorAll('.rs-top .bar[data-fix], .rs-top .bar').forEach(b => { const k = b.dataset.fix || (b.getAttribute('aria-label') || ''); const key = b.dataset.fix; const sp = b.querySelector(':scope > span'); if (key && TU_NM[key] && sp && sp.firstChild && sp.firstChild.nodeType === 3 && sp.firstChild.textContent !== TU_NM[key]) sp.firstChild.textContent = TU_NM[key]; });
  const low = fb.querySelector('.rs-top .bar.low[data-fix]'), btn = $('#doFix'), t = btn && btn.querySelector('span'); if (low && t && TU_NM[low.dataset.fix] && t.textContent !== TU_NM[low.dataset.fix]) t.textContent = TU_NM[low.dataset.fix]; }
new MutationObserver(() => { try { rsTidy(); } catch (e) {} }).observe($('#flowBody'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* wrong vote: readable light card */
html:not(.yg) .tot-miss{background:rgba(255,253,249,.95)!important;box-shadow:inset 0 0 0 2px #2E508A,0 8px 18px -8px rgba(0,0,0,.45)!important}
html:not(.yg) .tot-miss b{color:#1F3157!important}html:not(.yg) .tot-miss small{color:#4E433C!important}
/* score screen bars: every row the same box, so the highlighted one lines up */
html body #flowBody .rs-top .bars .bar{padding:6px 8px!important;margin-left:-8px!important;margin-right:0!important;border-radius:12px;box-shadow:inset 0 0 0 1.5px transparent}
html body #flowBody .rs-top .bars .bar.low{box-shadow:inset 0 0 0 1.5px #2E508A!important}
/* spending coins = gold button */
html body #flowBody #doFix.pay-coin{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important;box-shadow:0 6px 14px -8px rgba(160,110,10,.7)!important}
html body #flowBody #doFix.pay-coin > span:first-child{color:#3A2600!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('polish ok')
