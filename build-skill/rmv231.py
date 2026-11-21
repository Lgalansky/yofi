# Real Money build, step 234 (after rmv230.py): option 1 (user choice): two actions per card/screen.
#  - Stable photo card: one main button (its next step; "Race it again" once a run ends) + "⚔️ Head-to-head · $2–$20".
#    The small "Head-to-head · $2–$20" label above the button is folded into the button.
#  - Qualifier start: "Start voting" + "📷 Add a second photo (+25 🪙)" as a text link (was a card).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""(() => { const sh = stHero; stHero = function (p) { let h = sh.apply(this, arguments); try { h = h.replace(/<small>Head-to-head · \$2–\$20<\/small>/, '').replace('<i>VS</i> Head-to-head</button>', '⚔️ Head-to-head · $2–$20</button>'); } catch (e) {} return h; }; })();
(() => { const ud = upDone; upDone = function (p) { const r = ud.apply(this, arguments); try { const c = document.querySelector('#coach.on .q2-two'); if (c) { const T2 = c.querySelector('#qs2'); const l = document.createElement('button'); l.className = 'link nv-later q2-l'; l.textContent = '📷 Add a second photo · +25 🪙'; l.onclick = () => T2 && T2.click(); c.parentNode.insertBefore(l, c); c.style.display = 'none'; } } catch (e) {} return r; }; })();
function fcNotify() {""")
s = s.replace('</style>', """.q2-l{display:block;margin:12px auto 0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v231 ok')
s = open(d + 'yofi-real.html').read()
a = "<small>Race it again, or play a cash head-to-head</small>"
assert s.count(a) == 1, s.count(a)
s = s.replace(a, "<small>Its Final is done · rosette on the frame</small>")
s = s.replace('</style>', """html body .qls2 .q2-b #qsJ{background:linear-gradient(180deg,#2F8A45,#1E6B34)!important;color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('tidy ok')
