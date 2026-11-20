# Real Money build, step 219 (after rmv215.py): one Final per run (user choice).
#  - A photo's Final ends its run. It goes on the trophy wall with its result and leaves the Vote screen.
#  - "🎀 Race it again" (free) sends it back to the start of the route: 3 steps -> qualifier race -> 3 steps -> Final.
#  - Cash head-to-heads stay open for it any time.
#  - Final result: "<name>'s run is complete" + Race it again / head-to-head now / enter another photo.
#  - Stable, coins sheet and My Photos show the run state; a photo racing again shows its qualifying steps.
#  - Saves from the last build (raced photo sent back to steps) are moved to "run complete" once.
#  - A proven photo that misses its qualifier on a re-run simply ends that run (race it again any time).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("function fcNotify() {", r"""const inQual = p => !!(p && p.ql && !p.ql.done);
function finBack(p) { if (p && isCashOK(p) && !p.runEnd && !inQual(p) && !(p.fin && p.fr)) { p.fin = 1; p.fr = { s: 0 }; p.fl = null; } }
function finBtn(p, plain) { const e = x => plain ? '' : x; if (p && p.runEnd) return `${e('🎀 ')}Race it again · free`;
  if (inQual(p)) { const n = QS_STEPS - Math.min(QS_STEPS, p.ql.got || 0); return p.ql.live ? `${e('🔴 ')}Qualifier race live` : `${e('⚖️ ')}Vote ${n} step${n === 1 ? '' : 's'} to its qualifier`; }
  const n = QS_STEPS - Math.min(QS_STEPS, (p && p.fr && p.fr.s) || 0); return n <= 0 ? `${e('🏁 ')}Enter a Final` : `${e('⚖️ ')}Vote ${n} step${n === 1 ? '' : 's'} to the Final`; }
function runAgain(p) { if (!p) return; p.runEnd = 0; p.fin = 0; p.fr = null; p.fl = null; p.ql = null; p.rmAt = 0; p.rq = (p.rq || 0) + 1; try { qlStart(p); } catch (e) { p.ql = { w: 0, l: 0, at: Date.now() }; } save();
  try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {} try { go('judge'); renderJudge(); } catch (e) {} setTimeout(() => upDone(p), 250); }
try { (S.photos || []).forEach(p => { if (isCashOK(p) && p.raced && p.fin && !(p.fr && p.fr.go) && !inQual(p) && !p.runEnd) { p.runEnd = 1; p.fin = 0; p.fr = null; } }); save(); } catch (e) {}
(() => { const qs = qfStart; qfStart = function (p) { if (p && p.runEnd) return runAgain(p); if (inQual(p)) { try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {} go('judge'); renderJudge(); toast(`⚖️ Vote ${QS_RUN} in a row with the crowd = 1 step · ${finBtn(p, 1).replace('Vote ', '')}`); return; } return qs.apply(this, arguments); }; })();
(() => { const qr = qfResult; qfResult = function (p) { const r = qr.apply(this, arguments); try { p.runEnd = 1; p.fin = 0; p.fr = null; p.fl = null; save(); try { qlPaint(); } catch (x) {}
    const v = document.getElementById('qrV'), nm = esc(rcName(p));
    if (v) { v.textContent = '🎀 Race it again · free'; v.onclick = () => runAgain(p); const hh = document.getElementById('qrH'); if (hh) hh.textContent = hh.textContent.replace('Race a ', '');
      v.insertAdjacentHTML('beforebegin', `<p class="rn-end">🏆 <b>${nm}’s run is complete</b><small>It’s on your trophy wall. Race it again from the qualifier (free), or enter a new photo.</small></p>`); } } catch (x) {} return r; }; })();
(() => { const ql = qlLost; qlLost = function (p) { const r = ql.apply(this, arguments); try { if (isCashOK(p)) { p.runEnd = 1; p.fin = 0; p.fr = null; p.rmAt = 0; save(); const nm = esc(rcName(p)), gone = x => x && x.parentNode && x.parentNode.removeChild(x);
      const box = document.querySelector('#coach.on .rm-box'); if (box) box.innerHTML = `🏁 This run is over<small>${nm} is still ready for cash races. Race it again from the qualifier (free), or play a head-to-head now.</small>`;
      document.querySelectorAll('#coach.on .mq-or, #coach.on .mq-n').forEach(gone);
      const t = document.querySelector('#coach.on [data-trn], #coach.on #qlvV'); if (t) { t.outerHTML = `<button class="btn block nv-go" id="rnA">🎀 Race it again · free</button><button class="btn block nv-go2" id="rnH">⚔️ Race a $${H2H_FEES[0]} head-to-head now</button>`;
        $('#rnA').onclick = () => runAgain(p); $('#rnH').onclick = () => { popClose(); h2hOpen(p, H2H_FEES[0]); }; }
      gone(document.querySelector('#coach.on #qlvE')); const sim = document.querySelector('#coach.on .nv-sim'); if (sim && /wait is 2 minutes/.test(sim.textContent)) gone(sim); } } catch (e) {} return r; }; })();
(() => { const sh = stHero; stHero = function (p) { let h = sh.apply(this, arguments); try { const st = p.runEnd ? `🏁 Run complete${p.raced ? ` · ${ppOrd(p.raced.rank)} in its Final` : ''}` : inQual(p) ? `🎀 Racing again · ${Math.min(QS_STEPS, p.ql.got || 0)} of ${QS_STEPS} steps to its qualifier` : p.fr && p.fr.go ? '🏁 Final ready' : p.fin ? `🏆 Qualified · ${Math.min(QS_STEPS, (p.fr && p.fr.s) || 0)} of ${QS_STEPS} steps to the Final` : '';
    if (st) h = h.replace('<p class="sx-chip">', `<p class="sx-run ${p.runEnd ? 'end' : ''}">${st}</p><p class="sx-chip">`); } catch (e) {} return h; }; })();
(() => { const tw = twStatus; twStatus = function (p) { if (p && p.runEnd) return { t: `🏁 Run complete${p.raced ? ` · ${ppOrd(p.raced.rank)}` : ''} · race it again`, a: 's', c: 'r' }; return tw.apply(this, arguments); }; })();
function fcNotify() {""")
s = s.replace('</style>', """.rn-end{margin:10px 0 12px;padding:10px 12px;border-radius:14px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(10,16,32,.35);text-align:center;font:600 .9rem Nunito,system-ui;color:#FBF3DC}.rn-end b{color:#F3D98B}.rn-end small{display:block;margin-top:3px;font:600 .8rem/1.35 Nunito,system-ui;color:#C9D3E6}
.sx-run{margin:4px 14px 6px;text-align:center;font:800 .92rem Nunito,system-ui;color:#2F7A3F}.sx-run.end{color:#9A6B12}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v216 ok')
