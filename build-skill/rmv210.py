# Real Money build, step 213 (after rmv209.py): a clear path after a missed qualifier.
#  - The "So close" screen now states both ways back, with the cost:
#      1. Free rematch when the timer ends.
#      2. Train now · 50 coins a match: win 3 and the photo is Ready for Cash Races (no qualifier needed).
#  - "Train now" goes straight to the training head-to-head (was: tune-up sheet -> Stable -> Train -> match).
#    The free tune-up is still offered once per photo, then leads into the match.
#  - Not enough coins: the main button becomes "Vote to earn coins · N more to train" and returns to voting,
#    instead of walking the player through screens that end in a refusal.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)
RA("""<small>${nm} races again for a place in the Final. Or train now to skip the wait.</small>${tmBtn()}</div>""",
   """<small>${nm} races again for a place in the Final.</small>${tmBtn()}</div>
    <p class="mq-or">or skip the wait</p>""")
RA("""<button class="btn block nv-go" data-trn="${p.id}">🏋️ Train now · skip the wait</button>""",
   """${(S.gems || 0) >= TQ_COST ? `<button class="btn block nv-go" data-trn="${p.id}">🏋️ Train now · ${TQ_COST} coins</button>` : `<button class="btn block nv-go" id="qlvV">⚖️ Vote to earn coins · ${TQ_COST - Math.floor(S.gems || 0)} more to train</button>`}
    <p class="mq-n">Win ${TQ_WIN} training matches (${TQ_COST} coins each) and ${nm} is <b>Ready for Cash Races</b>. No qualifier needed. You have <b>${Math.floor(S.gems || 0)} coins</b>.</p>""")
RA("function fcNotify() {", r"""document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('#qlvV'); if (!b) return; e.preventDefault(); try { popClose(); } catch (x) {} try { go('judge'); renderJudge(); } catch (x) {} });
function trBegin(p, tuned) { p.tr = null; p.trw = p.trw || 0; save(); try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {} if (tuned) toast(`✨ ${rcName(p)} tuned up`); setTimeout(() => h2hOpen(p, 0), 200); }
(() => { const tt = trTune; trTune = function (p) { if (!p) return; if ((S.gems || 0) < TQ_COST) { toast(`🪙 Training is ${TQ_COST} coins a match · ${TQ_COST - Math.floor(S.gems || 0)} more to go · vote to earn them`); return; } if (p.tuned) return trBegin(p, false); return tt.apply(this, arguments); }; })();
function fcNotify() {""")
s = s.replace('</style>', """.mq-or{margin:2px 0 8px;text-align:center;font:800 .74rem Nunito,system-ui;letter-spacing:.1em;text-transform:uppercase;color:#8C9AB5}
.mq-n{margin:8px 4px 10px;text-align:center;font:600 .84rem/1.4 Nunito,system-ui;color:#C9D3E6}.mq-n b{color:#F3D98B}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v210 ok')
