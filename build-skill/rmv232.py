# Real Money build, step 235 (after rmv231.py): "So close" with too few coins to train (user choice A):
#  main "Vote to earn · N more 🪙" + secondary "📷 Enter another photo" (was "Back to voting", a duplicate of the main button).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""(() => { const ql = qlLost; qlLost = function (p) { const r = ql.apply(this, arguments); try { if (!document.querySelector('#coach.on #qlvV')) return r; const L = document.getElementById('qlvL'); if (!L) return r;
    const n = L.cloneNode(false); n.id = 'qlvN'; n.textContent = '📷 Enter another photo'; n.onclick = () => { popClose(); setTimeout(finPick, 200); }; L.parentNode.replaceChild(n, L); } catch (e) {} return r; }; })();
function fcNotify() {""")
open(d + 'yofi-real.html', 'w').write(s); print('rm v232 ok')
