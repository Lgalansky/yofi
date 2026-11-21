# Real Money build, step 237 (after rmv233.py): free (neutral) buttons pick navy or cream from the colour directly
# behind them, so a free button on a light row inside a dark screen is navy, not cream-on-cream.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""function pkBgDark(el) { let e = el.parentElement; while (e && e !== document.documentElement) { const cs = getComputedStyle(e), bi = cs.backgroundImage, bc = cs.backgroundColor;
    if (bi && bi !== 'none') { const m = bi.match(/rgba?\(([^)]+)\)/); if (m) { const [r, g, b] = m[1].split(',').map(Number); return (0.299 * r + 0.587 * g + 0.114 * b) < 140; } }
    const m = bc.match(/rgba?\(([^)]+)\)/); if (m) { const v = m[1].split(',').map(Number); if (v.length < 4 || v[3] > 0.5) return (0.299 * v[0] + 0.587 * v[1] + 0.114 * v[2]) < 140; } e = e.parentElement; } return false; }
(() => { const pt = pkTag; pkTag = function (b) { pt.apply(this, arguments); try { if (b && b.classList.contains('pk-free')) b.classList.toggle('pk-dark', pkBgDark(b)); } catch (e) {} }; })();
function fcNotify() {""")
open(d + 'yofi-real.html', 'w').write(s); print('rm v234 ok')
