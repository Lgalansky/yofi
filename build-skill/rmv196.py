# Real Money build, step 199 (after rmv195.py): a loop for photos that lose their qualifier, plus tuning.
#  - Lose a qualifier → "So close": near-miss reward (+15 🟡 if within 3 votes, else +5), then ONE clear rule:
#    "⏱ Free rematch in 2:00" (2 hours in the real game; 2 minutes in this demo) or "🏋️ Train now · skip the wait".
#    Second button: "📷 Enter another photo while you wait".
#  - The waiting photo keeps a card on the Vote screen with the countdown; when it's ready: "🏁 Race the rematch"
#    (straight into a new live qualifier race). A toast tells you when it's ready.
#  - Free re-entry at any time is gone (Stable shows the rematch timer / "Race the rematch" instead).
#  - Free Final entry costs 250 coins (was 300) so a first-time qualifier can afford it.
#  - Challenges only start after your first cash race; away challenges show a believable age ("3 h ago").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const pvList = () => (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || (p.tr && !p.tr.done)));",
   "const pvList = () => (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || (p.tr && !p.tr.done) || rmqWait(p)));")
RA("const FIN_COINS = 300", "const FIN_COINS = 250")
RA("if (!R.length || chList().length >= CH_MAX) return null;", "if (!R.length || chList().length >= CH_MAX || !(S.photos || []).some(x => x.raced || x.h2h)) return null;")
RA("at: Date.now() - Math.floor(Math.random() * 3) * 3600e3", "at: Date.now() - (1 + Math.floor(Math.random() * 5)) * 3600e3 - Math.floor(Math.random() * 3000e3)")
RA("Training costs ${TQ_COST} coins", "Train now to skip the wait · ${TQ_COST} coins a match", 2)
RA("Missed the cut · train it in your stable", "Lost its qualifier · free rematch on a timer")
s = s.replace("function fcNotify() {", r"""const RMQ_MS = 2 * 60000;
function rmqWait(p) { return !!(p && p.ql && p.ql.done === 'x' && p.rmAt && !(p.cashOK || p.fin || p.raced)); }
const rmqReady = p => rmqWait(p) && Date.now() >= p.rmAt;
const rmqFmt = t => { const s2 = Math.max(0, Math.ceil((t - Date.now()) / 1000)); return `${Math.floor(s2 / 60)}:${String(s2 % 60).padStart(2, '0')}`; };
try { (S.photos || []).forEach(p => { if (p.ql && p.ql.done === 'x' && !p.rmAt) p.rmAt = 1; }); } catch (e) {}
function rmqGo(p) { if (!rmqReady(p)) return; try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {} p.rmAt = 0; p.rmTold = 0; p.rq = (p.rq || 0) + 1; p.ql = { w: 0, l: 0, got: QS_STEPS, gv: 2, live: 1, at: Date.now() }; save(); go('judge'); renderJudge(); setTimeout(() => qlRace(p), 300); }
function qlLost(p, o, A, B) { const q = p.ql, nm = esc(rcName(p)), gap = B - A, near = gap <= 3, bonus = near ? 15 : 5; q.done = 'x'; q.shown = 1; q.w = A; q.l = B; q.at = Date.now(); p.rmAt = Date.now() + RMQ_MS; p.rmTold = 0; S.gems = (S.gems || 0) + bonus; save();
  popOpen(`<div class="pp qfx nv qw"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big sm">So close</h2><i class="nv-sw"></i>
    <div class="qw-ph out"><img src="${p.src}" alt=""></div><p class="qw-r">${esc(o.t)} wins ${B}–${A}</p>
    <p class="qw-o">${near ? `Just <b class="gold">${gap} vote${gap === 1 ? '' : 's'}</b> short` : 'Not this time'} · <b class="gold">+${bonus} coins</b> for racing</p>
    <div class="rm-box">⏱ Free rematch in <b class="rm-t" data-until="${p.rmAt}">${rmqFmt(p.rmAt)}</b><small>${nm} races again for a place in the Final. Or train now to skip the wait.</small></div>
    <button class="btn block nv-go" data-trn="${p.id}">🏋️ Train now · skip the wait</button><button class="btn block nv-go2" id="qlvE">📷 Enter another photo while you wait</button>
    <div style="text-align:center"><button class="link nv-later" id="qlvL">Back to voting</button></div><p class="nv-sim">Demo: the wait is 2 minutes here (2 hours in the real game)</p></div>`);
  try { paintGems(); } catch (e) {}
  $('#qlvE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }
(() => { const pc = pvCard; pvCard = function (p) { if (!rmqWait(p)) return pc.apply(this, arguments); const rd = rmqReady(p);
  return `<div class="pv-c rm ${rd ? 'rdy' : ''}" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">${rd ? '🏁 Rematch ready' : '⏱ Rematch'}</span></div>
    <div class="pv-fn"><img src="${p.src}" alt=""><div>${rd ? '<b>Its rematch is ready!</b><small>A new live race for a place in the Final</small>' : `<b>Free rematch in <span class="rm-t" data-until="${p.rmAt}">${rmqFmt(p.rmAt)}</span></b><small>Lost ${p.ql.w}–${p.ql.l} · or <a data-trn="${p.id}">train now to skip the wait</a></small>`}</div></div>
    ${rd ? `<button class="btn block pv-go" data-rmg="${p.id}">🏁 Race the rematch</button>` : ''}</div>`; }; })();
function stTrain(p) { const q = p.ql, T = p.tq || { w: 0, l: 0 }, inQ = q && !q.done, w = rmqWait(p), rd = rmqReady(p);
  const stt = inQ ? '🎀 In qualifying' : rd ? '🏁 Rematch ready' : w ? `⏱ Rematch in <span class="rm-t" data-until="${p.rmAt}">${rmqFmt(p.rmAt)}</span>` : '😴 Resting';
  return `<div class="sx-card"><div class="sx-row"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><span class="sx-st">${stt}</span><span class="sx-f">💪 Form +${p.form || 0}</span></div></div>
    <p class="sx-rule g"><span>Win 3 before 3 losses</span></p><div class="sx-wl"><span class="w">🏆 Wins ${T.w}/${TQ_WIN}</span><span class="l">✕ Losses ${T.l}/${TQ_WIN}</span></div>
    <p class="sx-note">Train now to skip the wait · ${TQ_COST} coins a match</p>
    <div class="sx-btns two">${inQ ? '<button class="btn sx-nv" data-stv>⚖️ Vote to advance</button>' : rd || !w ? `<button class="btn sx-go" data-rmg="${p.id}">🏁 Race the rematch</button>` : '<button class="btn sx-nv" disabled style="opacity:.55">⏱ Rematch soon</button>'}<button class="btn sx-nv" data-sth="${p.id}" data-m="t">🏋️ Train</button></div></div>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-rmg]'); if (!b) return; e.preventDefault(); const p = (S.photos || []).find(x => x.id === b.dataset.rmg); if (!p) return; if (!p.rmAt) p.rmAt = 1; rmqGo(p); });
setInterval(() => { try { document.querySelectorAll('.rm-t[data-until]').forEach(e => { e.textContent = rmqFmt(+e.dataset.until); });
  (S.photos || []).forEach(p => { if (rmqReady(p) && !p.rmTold) { p.rmTold = 1; save(); const e = document.getElementById('qlS'); if (e) e.outerHTML = qlStripHTML(); if (p.rmAt > 1 && $('#app').classList.contains('on')) toast(`🏁 ${rcName(p)}’s rematch is ready`); if (document.querySelector('#flow .sx')) finalsTab(); } }); } catch (e) {} }, 1000);
function fcNotify() {""", 1)
s = s.replace('</style>', """.qw-o b.gold{color:#F3D98B}.rm-box{margin:4px 0 12px;padding:10px 12px;border-radius:14px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(10,16,32,.4);font:800 1.1rem Nunito,system-ui;color:#FBF3DC}.rm-box b{font:900 1.4rem Fraunces,Georgia,serif;color:#F3D98B}.rm-box small{display:block;margin-top:2px;font:600 .82rem/1.35 Nunito,system-ui;color:#C9D3E6}
.pv-c.rm{box-shadow:inset 0 0 0 2px #8C9AB5;background:#F6F8FC}.pv-c.rm.rdy{box-shadow:inset 0 0 0 2.5px #2F6B3F,0 4px 14px rgba(47,107,63,.2);background:#F1F6EC}.pv-c.rm .pv-fn img{box-shadow:0 0 0 3px #8C9AB5}.pv-c.rm.rdy .pv-fn img{box-shadow:0 0 0 3px #2F6B3F}
.pv-c.rm a{color:#2E4F8A;text-decoration:underline;cursor:pointer;font-weight:800}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v196 ok')
