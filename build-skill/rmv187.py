# Real Money build, step 190 (after rmv186.py): finalist cards never get stuck.
#  Qualifying now leads straight to the Final, so a finalist's card on the Vote screen shows "🏆 Into the Final!"
#  with a big green "🏁 Meet your finalists & race" button (opens the Final lobby) instead of streak steps.
#  Old saves: finalists are treated as ready (no leftover "Step 3 of 3"). Votes never try to move a finalist.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
old = "const qsElig = () => pvList().filter(p => (p.ql && !p.ql.done && !p.ql.live && !p.tr) || (p.fin && !(p.fr && p.fr.go)));"
assert s.count(old) == 1; s = s.replace(old, "const qsElig = () => pvList().filter(p => p.ql && !p.ql.done && !p.ql.live && !p.tr);")
s = s.replace("function fcNotify() {", r"""try { (S.photos || []).forEach(p => { if (p.fin) p.fr = { s: QS_STEPS, go: 1 }; }); save(); } catch (e) {}
(() => { const pc = pvCard; pvCard = function (p) { if (!p.fin) return pc.apply(this, arguments); p.fr = { s: QS_STEPS, go: 1 };
  return `<div class="pv-c fin" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">🏆 Finalist</span><em>🟡 +${p.qc || 0}</em></div>
    <div class="pv-fn"><img src="${p.src}" alt=""><div><b>Into the Final!</b><small>Pick your entry ($2–$20) · 1st wins up to ${money(20 * QF_PAY[0])}</small></div></div>
    <button class="btn block pv-go" data-qfr="${p.id}">🏁 Meet your finalists & race</button></div>`; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.pv-fn{display:flex;align-items:center;gap:10px;margin:8px 0 2px}.pv-fn img{width:54px;height:54px;border-radius:10px;object-fit:cover;box-shadow:0 0 0 3px #D9AE4F;flex:none}
.pv-fn b{display:block;font:900 1.1rem Fraunces,Georgia,serif;color:#14213D}.pv-fn small{font:700 .78rem Nunito,system-ui;color:#5B4A3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v187 ok')
