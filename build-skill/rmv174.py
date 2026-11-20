# Real Money build, step 177 (after rmv173.py): easier streaks, one photo at a time, both balances always shown.
#  - Streak is 2 correct in a row (was 3) to move a photo 1 step. 2 dots; the 2nd pulses "1 more for a step!".
#  - Your votes move ONE photo at a time: the card you're looking at (swipe to choose). That card says
#    "⚖️ Your votes are moving this one"; the others say "Swipe here and vote to move this one".
#  - The cash and coin balances both always show at the top (coin players see $0.00 cash too).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const QS_STEPS = 3, QS_RUN = 3;", "const QS_STEPS = 3, QS_RUN = 2;")
RA("    (S.photos || []).forEach(p => { const q = p.ql;", "    [qsTarget()].filter(Boolean).forEach(p => { const q = p.ql;")
RA("""${[0, 1, 2].map(i => `<i class="${i < k ? 'on' : i === 2 && k === 2 ? 'next' : ''}"></i>`).join('')}</span>${k === 2 ?""",
   """${Array.from({ length: QS_RUN }, (_, i) => `<i class="${i < k ? 'on' : i === QS_RUN - 1 && k === QS_RUN - 1 ? 'next' : ''}"></i>`).join('')}</span>${k === QS_RUN - 1 ?""")
s = s.replace("function fcNotify() {", r"""const qsElig = () => pvList().filter(p => (p.ql && !p.ql.done && !p.ql.live && !p.tr) || (p.fin && !(p.fr && p.fr.go)));
function qsTarget() { const E = qsElig(); if (!E.length) return null; const t = E.find(p => p.id === window.__pvSel) || E[0]; if (t.fin && !t.fr) t.fr = { s: 0 }; return t; }
(() => { const pc = pvCard; pvCard = function (p) { let h = pc.apply(this, arguments); try { const E = qsElig(); if (E.length > 1 && E.includes(p)) { const t = qsTarget();
    h = h.replace('<div class="pv-c', `<div class="pv-c ${t && t.id === p.id ? 'act' : 'wait'}`); h = h.replace(/<\/div>\s*$/, `<p class="pv-who"><span class="a">⚖️ Your votes are moving this one</span><span class="w">👉 Swipe here and vote to move this one</span></p></div>`); } } catch (e) {} return h; }; })();
document.addEventListener('scroll', e => { const t = e.target; if (!t || t.id !== 'pvS') return; clearTimeout(window.__pvT); window.__pvT = setTimeout(() => { const C = [...t.querySelectorAll('.pv-c')]; if (!C.length) return;
  const mid = t.scrollLeft + t.clientWidth / 2, c = C.reduce((a, x) => Math.abs(x.offsetLeft + x.offsetWidth / 2 - mid) < Math.abs(a.offsetLeft + a.offsetWidth / 2 - mid) ? x : a);
  const E = qsElig(); if (!E.some(p => p.id === c.dataset.pid)) return; window.__pvSel = c.dataset.pid; C.forEach(x => { if (x.classList.contains('act') || x.classList.contains('wait')) { x.classList.toggle('act', x === c); x.classList.toggle('wait', x !== c); } }); }, 120); }, true);
function fcNotify() {""", 1)
s = s.replace('</style>', """html.coinp #wCash{display:flex!important}
.pv-who{margin:6px 0 0;font:800 .74rem Nunito,system-ui}.pv-who .w{display:none;color:#8A7B6C}.pv-who .a{color:#22502F}.pv-c.wait .pv-who .a{display:none}.pv-c.wait .pv-who .w{display:inline}
.pv-c.wait{opacity:.72}.pv-c.act{box-shadow:inset 0 0 0 2.5px #2F6B3F,0 4px 14px rgba(47,107,63,.18)}.pv-c.fin.act{box-shadow:inset 0 0 0 2.5px #D9AE4F,0 4px 14px rgba(217,174,79,.25)}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v174 ok')
# pass 2: streak dots and step count refresh after every vote (in-place card update covers .pv-k too)
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""(() => { const qp = qlPaint; qlPaint = function () { const r = qp.apply(this, arguments); try { document.querySelectorAll('#qlS .pv-c[data-pid]').forEach(c => { const p = (S.photos || []).find(x => x.id === c.dataset.pid); if (!p) return;
  const t = document.createElement('div'); t.innerHTML = pvCard(p); const n = t.firstElementChild; ['.pv-k', '.pv-tr'].forEach(k => { const a = c.querySelector(k), b = n && n.querySelector(k); if (a && b && a.innerHTML !== b.innerHTML) {
    if (k === '.pv-tr') { const hz = a.querySelector('.pv-hz'), nz = b.querySelector('.pv-hz'), u = a.querySelector('.pv-rail u'), nu = b.querySelector('.pv-rail u'); if (hz && nz) hz.style.left = nz.style.left; if (u && nu) u.style.width = nu.style.width; }
    else a.innerHTML = b.innerHTML; } }); }); } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v174 pass2 ok')
