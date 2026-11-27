# Skill preview: the live knockout screen (Sprint) in the app's newer look.
#  - header "⏱ Sprint" with a "Knockout of 16 · live" line
#  - your status as a calm box ("You're out at Level 1" / "You're through to Level 2")
#  - the live match: framed photos with names underneath (not over the photos), a VS badge,
#    the vote bar with each side's count by its name, and "18 votes to go" as a chip
#  - your last match and the pyramid stay; "Keep judging" becomes "Keep voting"
# usage: python3 build-skill/tourlive.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- live knockout screen tidy ----
function tkTidy() { const b = $('#tkBody'); if (!b || !b.querySelector('.tk-h')) return;
  const h = b.querySelector('.tk-h'); if (h && !h.dataset.t) { h.dataset.t = 1; h.innerHTML = `${KO_PYR2}Sprint<small>Knockout of 16 · live</small>`; }
  const run = b.querySelector('.tk-run'); if (run && !run.dataset.t) { run.dataset.t = 1; const t = run.querySelector('b'), m = (t && t.textContent.match(/reached (Level \d|Best in Show)/)) || null;
    if (m) run.innerHTML = `<small>You’re out</small><b>${m[1]}</b><span>Your $1 went into the prize · we’ll tell you who wins</span>`; }
  const vs = b.querySelector('.tk-vs'); if (vs && !vs.dataset.t) { vs.dataset.t = 1; vs.querySelectorAll('.kg-ph').forEach(ph => { const tg = ph.querySelector('.kg-tag'); if (tg) { const c = document.createElement('span'); c.className = 'tk-nm'; c.textContent = tg.textContent; tg.remove(); ph.appendChild(c); } }); }
  const cnt = b.querySelector('.tk-cnt'); if (cnt && vs && !cnt.dataset.t) { cnt.dataset.t = 1; const n = [...vs.querySelectorAll('.tk-nm')].map(x => x.textContent); const sp = cnt.querySelectorAll('span'); if (sp[0]) sp[0].insertAdjacentHTML('afterend', `<small>${n[0] || ''}</small>`); if (sp[1]) sp[1].insertAdjacentHTML('beforebegin', `<small>${n[1] || ''}</small>`); }
  const rin = b.querySelector('.tk-rin'); if (rin && !rin.dataset.t) { rin.dataset.t = 1; const bar = b.querySelector('.kg-bar'); const c = b.querySelector('.tk-cnt'); if (c) c.after(rin); else if (bar) bar.after(rin); }
  const rc = b.querySelector('.tk-rc p'); if (rc && /-\d/.test(rc.textContent)) rc.textContent = rc.textContent.replace(/-(\d+)/, '$1');
  b.querySelectorAll('.btn[data-shclose]').forEach(x => { if (/Keep judging/.test(x.textContent)) x.textContent = 'Keep voting'; }); }
const KO_PYR2 = '<svg class="ko-pyr" viewBox="0 0 40 34" aria-hidden="true"><rect x="15" y="1" width="10" height="6" rx="2" fill="#F3D27A"/><rect x="10" y="9" width="20" height="6" rx="2" fill="#E0A82E"/><rect x="5" y="17" width="30" height="6" rx="2" fill="#C9D6EE"/><rect x="0" y="25" width="40" height="6" rx="2" fill="#9FB6DD"/></svg>';
new MutationObserver(() => { try { tkTidy(); } catch (e) {} }).observe($('#sheetBody'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* live knockout screen */
html body #tkBody .tk-h{display:flex;flex-direction:column;align-items:center;gap:2px;margin:0 0 12px;font:900 1.7rem Fraunces,serif;color:#1F3157}
#tkBody .tk-h .ko-pyr{width:42px;height:36px;margin-bottom:2px}#tkBody .tk-h small{font:800 .8rem "Nunito Sans";color:#4E433C}
html body #tkBody .tk-run{display:block;text-align:center;padding:10px 12px;margin:0 0 12px;border-radius:16px;background:#FBF5EA!important;box-shadow:inset 0 0 0 2px #E2D5BE!important;border:0!important;animation:none!important;background-image:none!important}
html body #tkBody .tk-run::before,html body #tkBody .tk-run::after{display:none!important}
#tkBody .tk-run small{display:block;font:800 .7rem "Nunito Sans";letter-spacing:.07em;text-transform:uppercase;color:#8A7E72}#tkBody .tk-run b{display:block;font:900 1.6rem/1.1 Fraunces,serif;color:#4E433C}#tkBody .tk-run span{display:inline-block;margin-top:4px;font:700 .78rem "Nunito Sans";color:#4E433C}
html body #tkBody .tk-pill{margin:0 auto 6px}
html body #tkBody .tk-judge{margin:0 0 8px;text-align:center;font:800 .85rem "Nunito Sans";color:#8A5A0A}
html body #tkBody .tk-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;margin-bottom:8px}
html body #tkBody .tk-vs .kg-ph{display:flex;flex-direction:column;padding:0;border:0;background:none;box-shadow:none;cursor:pointer}
html body #tkBody .tk-vs .kg-ph img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:16px;box-shadow:0 0 0 3px #2D4E86}
html body #tkBody .tk-vs .kg-ph:last-child img{box-shadow:0 0 0 3px #E0A82E}
#tkBody .tk-nm{display:block;margin-top:6px;font:800 .82rem "Nunito Sans";color:#2D2521;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body #tkBody .tk-vs .kg-x{width:40px;height:40px;border-radius:50%;background:#2D4E86;color:#fff;font:900 .9rem/40px Fraunces,serif;text-align:center;box-shadow:0 0 0 4px #F7F0E4}
html body #tkBody .kg-bar{height:14px;border-radius:99px;margin:4px 0 4px}
html body #tkBody .tk-cnt{display:flex;align-items:baseline;gap:6px;margin:0 2px 6px}#tkBody .tk-cnt span{font:900 1.3rem Fraunces,serif}#tkBody .tk-cnt small{font:700 .74rem "Nunito Sans";color:#4E433C}#tkBody .tk-cnt b{flex:1}
html body #tkBody .tk-rin{display:flex;align-items:center;justify-content:center;gap:6px;width:max-content;margin:0 auto 14px;padding:4px 12px;border-radius:99px;background:#FFF3D6;border:0!important;box-shadow:none!important;min-height:0}
#tkBody .tk-rin span{font:800 .78rem "Nunito Sans";color:#4E433C;letter-spacing:0;text-transform:none;opacity:1}#tkBody .tk-rin b{font:900 1rem "Nunito Sans";color:#1F3157}#tkBody .tk-rin{flex-direction:row-reverse}html body #tkBody #tkSv{font:900 1rem/1.2 "Nunito Sans"!important;color:#1F3157!important}html body #tkBody .tk-rin{padding:4px 12px!important;height:auto!important}
html body #tkBody .tk-rc{border-radius:16px}
html body #tkBody .btn[data-shclose]{background:#2D4E86!important;color:#fff!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('tourlive ok')
