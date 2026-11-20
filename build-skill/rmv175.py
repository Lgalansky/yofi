# Real Money build, step 178 (after rmv174.py): when no photo is in play, the Vote screen promotes entering one.
#  An "empty lane" card where the photo cards go: dashed track with an empty 📷 at the start line, "Your photo could be
#  racing", "Free · your votes move it to a live race · win and it races for cash", button "📷 Enter a photo · free".
#  If you have cash-ready photos resting, a second line: "🐎 Or race one from your stable". At the 5-a-day limit it
#  points to the stable instead.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""(() => { const qs = qlStripHTML; qlStripHTML = function () { if (pvList().length) return qs.apply(this, arguments);
  const full = dEnt().n >= DAY_ENT, ready = (S.photos || []).some(p => isCashOK(p) && !p.fin);
  return `<div class="pv pv-empty" id="qlS"><div class="pv-c pe"><div class="pv-t"><b>${full ? 'Your stable is waiting' : 'Your photo could be racing'}</b></div>
    <div class="pv-tr"><div class="pv-rail pe-rail"></div><span class="pe-hz">📷</span><span class="pv-fl">🏁</span></div>
    <p class="pe-s">${full ? 'That’s 5 photos today. Train or race your photos in your stable.' : 'Free to enter · your votes move it to a live race · win and it races for cash'}</p>
    ${full ? '<button class="btn block pv-go" data-pe="s">🐎 Open your stable</button>' : `<button class="btn block pv-go" data-pe="u">📷 Enter a photo · free</button>${ready ? '<button class="link pe-l" data-pe="s">🐎 Or race one from your stable</button>' : ''}`}</div></div>`; }; })();
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-pe]'); if (!b) return; e.preventDefault(); if (b.dataset.pe === 'u') finPick(); else finalsTab(); });
function fcNotify() {""", 1)
s = s.replace('</style>', """.pv-c.pe{background:#FFFCF3;box-shadow:inset 0 0 0 2px #D9AE4F}.pe-rail{background:repeating-linear-gradient(90deg,#E5D3AE 0 10px,transparent 10px 18px)!important}
.pe-hz{position:absolute;left:0;top:3px;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;background:#fff;box-shadow:0 0 0 2px #D9AE4F;border:2px dashed #D9AE4F;box-sizing:border-box;animation:qlsGo 1.4s ease-in-out infinite}
.pe-s{margin:2px 0 0;font:700 .8rem/1.4 Nunito,system-ui;color:#5B4A3F}html body .pe-l{display:block;margin:8px auto 0;font:800 .84rem Nunito,system-ui;color:#2E4F8A;background:none;border:0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v175 ok')
