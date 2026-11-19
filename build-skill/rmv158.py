# Real Money build, step 161 (after rmv157.py): the qualifier is 15 crowd votes (not 15 matches of 7), and quieter rounds.
#  - Each crowd vote is one head-to-head: your photo vs a rival. 8 votes won = finalist, 8 lost = out.
#  - Live box: "● LIVE · Vote 6 of 15", big won–lost tally, the latest vote ("✓ A voter picked Rex over “Too cool” · +5 🟡"),
#    and 15 pips with the 8-win line. Votes arrive with yours and every few seconds.
#  - Wording everywhere: "15 crowd votes · win 8" (no more "head-to-heads").
#  - Round ends: only the 3rd round (entry ticket earned) opens the popup. Rounds 1 and 2 show a short banner under the
#    round bar ("✓ Round 1 done · 3/6 · +10 🟡 · 2 more rounds to your next photo entry") and you keep voting.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("It plays <b>15 head-to-heads</b> judged by the crowd. Win 8", "The crowd gives it <b>15 votes</b>, each against another photo. Win 8")
RA("Its qualifier is 15 head-to-heads judg", "Its qualifier is 15 crowd votes judg")
RA("Win 8 of 15 head-to-heads and it reaches a cash Final duel.", "Win 8 of 15 crowd votes and it reaches a cash Final duel.")
RA("<h2 class=\"db-h\">15 head-to-heads. Win 8 to reach a Final.</h2>", "<h2 class=\"db-h\">15 crowd votes. Win 8 to reach a Final.</h2>")
RA("Win 8 of 15 head-to-heads to reach a Final.", "Win 8 of 15 crowd votes to reach a Final.")
RA("The crowd judges it in 15 head-to-heads.", "The crowd gives it 15 votes.")
# quiet rounds
RA("""  popOpen(`<div class="pp vrr"><p class="pp-k">⚖️ Round ${v.n} complete</p>""",
   """  if (!qual) { vrQuiet(v.n, ok, pay); return; }
  popOpen(`<div class="pp vrr"><p class="pp-k">⚖️ Round ${v.n} complete</p>""")
s = s.replace("function fcNotify() {", r"""function vrQuiet(n, ok, pay) { const left = 3 - (S.vrq || 0); try { paintGems(); gemExplosion(pay, { label: `Round ${n} · ${ok}/${VR_N}` }); } catch (e) {}
  const put = () => { const top = document.getElementById('vrTop'); if (!top) return; const o = document.getElementById('vrQ'); if (o) o.remove();
    top.insertAdjacentHTML('afterend', `<div class="vrqb" id="vrQ">✓ <b>Round ${n} done</b> · ${ok}/${VR_N} right · +${pay} 🟡<small>${left === 1 ? '<b>1 more round</b>' : `<b>${left} more rounds</b>`} to your next photo entry</small></div>`);
    setTimeout(() => { const e = document.getElementById('vrQ'); if (e) { e.classList.add('bye'); setTimeout(() => e.remove(), 400); } }, 4200); };
  setTimeout(put, 50); }
function qlStep(p, n) { const q = p.ql; if (!q || q.done) return; n = n || 1;
  for (let i = 0; i < n && !q.done; i++) { const pr = Math.max(.25, Math.min(.8, .5 + (qlStrength(p) - 62) / 60)), win = Math.random() < pr, o = qlOpp(p);
    if (win) { q.w++; p.qc = (p.qc || 0) + 5; S.gems = (S.gems || 0) + 5; try { paintGems(); } catch (e) {} } else q.l++;
    q.v = (q.v || []).concat(win ? 1 : 0); q.last = { win, t: o.t, src: o.src }; q.fl = Date.now();
    if (q.w >= QF_WIN) q.done = 'q'; else if (q.l > QF_N - QF_WIN) q.done = 'x';
    if (q.done) setTimeout(function tr() { if (q.shown) return; if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx')) { setTimeout(tr, 1200); return; } qlDone(p); }, 1400); }
  save(); }
function qlLiveHTML(p) { const q = p.ql, L = q.last, nw = L && Date.now() - (q.fl || 0) < 1500, need = QF_WIN - q.w, spare = QF_N - QF_WIN + 1 - q.l, V = q.v || [];
  const pips = Array.from({ length: QF_N }, (_, i) => `<i class="${i < V.length ? (V[i] ? 'w' : 'l') : ''}"></i>`).join('');
  return `<div class="qm qv2" id="qm-${p.id}"><div class="qm-h"><span class="qm-live">● LIVE</span><b>Vote ${Math.min(QF_N, q.w + q.l + 1)} of ${QF_N}</b><i class="qm-s">simulated</i><em>🟡 +${p.qc || 0}</em></div>
    <div class="qv2-m"><img src="${p.src}" alt=""><div class="qv2-t"><span class="w"><b>${q.w}</b>won</span><span class="d">–</span><span class="l"><b>${q.l}</b>lost</span></div>
      <div class="qv2-n"><b>${need > 0 ? `${need} more win${need === 1 ? '' : 's'}` : 'Finalist!'}</b><small>${need > 0 ? `to the Final · ${spare} loss${spare === 1 ? '' : 'es'} to spare` : 'into the Final'}</small></div></div>
    <div class="qv2-p">${pips}<u style="left:calc(${QF_WIN / QF_N * 100}% - 1px)"></u></div>
    <p class="qv2-l ${L ? (L.win ? 'w' : 'l') : ''} ${nw ? 'nw' : ''}">${L ? `${L.src ? `<img src="${L.src}" alt="">` : ''}${L.win ? `✓ A voter picked <b>${esc(rcName(p))}</b> over “${esc(L.t)}” · +5 🟡` : `✕ A voter picked “${esc(L.t)}” over ${esc(rcName(p))}`}` : '⏳ Votes are coming in…'}</p></div>`; }
function qlPaint() { const e = document.getElementById('qlS'); if (e) e.outerHTML = qlStripHTML(); }
function fcNotify() {""", 1)
# background votes: one every ~4 s while you're on the Vote screen (the old 2.5 s ticker also skips during the 2.6 s after a vote)
s = s.replace('</style>', """.qv2-m{display:flex;align-items:center;gap:10px}.qv2-m>img{width:50px;height:50px;border-radius:10px;object-fit:cover;box-shadow:0 0 0 3px #2F6B3F;flex:none}
.qv2-t{display:flex;align-items:baseline;gap:6px}.qv2-t span{display:flex;flex-direction:column;align-items:center;font:800 .6rem Nunito,system-ui;text-transform:uppercase;letter-spacing:.06em;color:#8A7B6C}
.qv2-t b{font:900 1.6rem/1 Fraunces,Georgia,serif}.qv2-t .w b{color:#2F6B3F}.qv2-t .l b{color:#A6402F}.qv2-t .d{font:900 1.2rem Fraunces;color:#B9AE9C}
.qv2-n{margin-left:auto;text-align:right}.qv2-n b{display:block;font:800 .95rem Fraunces,Georgia,serif;color:#14213D}.qv2-n small{font:700 .7rem Nunito,system-ui;color:#5B4A3F}
.qv2-p{position:relative;display:flex;gap:3px;margin:8px 0 6px}.qv2-p i{flex:1;height:9px;border-radius:3px;background:#E6EFE2}.qv2-p i.w{background:#2F6B3F}.qv2-p i.l{background:#C0533F}
.qv2-p u{position:absolute;top:-4px;bottom:-4px;width:2px;background:#D9AE4F;border-radius:1px}
.qv2-l{display:flex;align-items:center;gap:7px;margin:0;padding:5px 8px;border-radius:10px;background:#F3EEE5;font:700 .76rem/1.3 Nunito,system-ui;color:#5B4A3F}.qv2-l img{width:24px;height:24px;border-radius:6px;object-fit:cover;flex:none}
.qv2-l.w{background:#F1F6EC;color:#22502F}.qv2-l.l{background:#F9ECE8;color:#A6402F}.qv2-l b{color:#14213D}.qv2-l.nw{animation:qmFl .4s ease-out both}
.vrqb{margin:6px 2px 8px;padding:8px 12px;border-radius:12px;background:#F1F6EC;box-shadow:inset 0 0 0 1.5px #2F6B3F;font:700 .84rem Nunito,system-ui;color:#22502F;text-align:center;animation:qmFl .35s ease-out both;transition:opacity .4s}
.vrqb b{color:#14213D}.vrqb small{display:block;font-size:.76rem;color:#3D4A5C}.vrqb.bye{opacity:0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v158 ok')
# pass 2: last-vote line text kept in one block so it wraps cleanly
s = open(d + 'yofi-real.html').read()
RA("""${L.win ? `✓ A voter picked <b>${esc(rcName(p))}</b> over “${esc(L.t)}” · +5 🟡` : `✕ A voter picked “${esc(L.t)}” over ${esc(rcName(p))}`}` : '⏳ Votes are coming in…'}</p></div>`; }""",
   """<span>${L.win ? `✓ A voter picked <b>${esc(rcName(p))}</b> over “${esc(L.t)}” · +5 🟡` : `✕ A voter picked “${esc(L.t)}” over ${esc(rcName(p))}`}</span>` : '⏳ Votes are coming in…'}</p></div>`; }""")
open(d + 'yofi-real.html', 'w').write(s); print('rm v158 pass2 ok')
