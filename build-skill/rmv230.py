# Real Money build, step 233 (after rmv229.py): four fixes from the user's screenshots.
#  1. Head-to-head result: only 2 options: "New challenge · $X" and "Back to stable" (Step up removed).
#  2. Qualifier start screen rebuilt from the user's mock-up (navy): photo, step track, 3-row "how it works" card,
#     "Start voting", and the "Add a second photo?" card. Copy corrected: winning the race = Qualified, then 3 steps to the Final.
#  3. Daily Cup tile simplified in the landing-page style: kicker, one big line, one short line, one button, one footnote.
#  4. Photo progress shows Done (green ticks) · Now (highlighted, with progress) · Still to do (numbered, grey) · the goal.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA('${H2H_FEES[H2H_FEES.indexOf(fee) + 1] ? `<button class="btn block nv-up" id="h2Up">', '${false ? `<button class="btn block nv-up" id="h2Up">')
RA("function fcNotify() {", r"""(() => { const ud = upDone; upDone = function (p) { const r = ud.apply(this, arguments); try { const box = document.querySelector('#coach.on .qls'); if (!box) return r; const J = document.getElementById('qsJ'), T2 = document.getElementById('qs2'), tr = box.querySelector('.pv-tr'), nm = esc(rcName(p));
    const fin = (() => { try { return showName(photoShow(p) || finCatOf(p) || p.cat) + ' Final'; } catch (e) { return 'the Final'; } })(), got = Math.min(QS_STEPS, (p.ql && p.ql.got) || 0);
    box.className = 'pp qfx nv qls2'; box.innerHTML = `<p class="nv-brand">PhotoPicks</p><p class="q2-k">🎀 Qualifier · starting now</p><h2 class="nv-h2">${nm} is in!</h2><div class="q2-ph"><img src="${p.src}" alt=""></div><div class="q2-tr"></div><p class="q2-st">${got} of ${QS_STEPS} steps to the live race</p>
      <div class="q2-c"><div class="q2-r"><span>👥</span><div><b>Pick the crowd favourite</b><small>Match the crowd twice in a row to move ${nm} one step.</small></div><em class="q2-d"><i></i><i></i></em></div>
        <div class="q2-r"><span>🏇</span><div><b>Take ${QS_STEPS} steps to race</b><small>After ${QS_STEPS} steps, ${nm} races another photo live.</small></div></div>
        <div class="q2-r"><span>🏆</span><div><b>Win to qualify</b><small>Beat the rival and ${nm} is qualified, then ${QS_STEPS} more steps to the ${esc(fin)}.</small></div></div></div><div class="q2-b"></div>`;
    if (tr) box.querySelector('.q2-tr').appendChild(tr); const bb = box.querySelector('.q2-b'); if (J) bb.appendChild(J);
    if (T2) { const c = document.createElement('div'); c.className = 'q2-two'; c.innerHTML = '<span>📷</span><div><b>Add a second photo?</b><small>If one misses, the other’s still racing · +25 🪙</small></div>'; c.onclick = () => T2.click(); T2.style.display = 'none'; c.appendChild(T2); bb.appendChild(c); } } catch (e) {} return r; }; })();
(() => { const cc = cupCard; cupCard = function () { try { const st = cupSt(), R = (S.photos || []).filter(p => isCashOK(p) && !p.starter), g = Math.floor(S.gems || 0); if (st !== 'open' || !R.length) return cc.apply(this, arguments);
    return `<div class="cup2" id="cupC"><span class="cup2-t">🏆</span><p class="cup2-k">Daily Cup · tonight 8pm</p><h3>$100 in prizes</h3><p class="cup2-s">Enter one photo. The crowd ranks it all day. 1st wins $30.</p>
      ${g >= CUP_COST ? `<button class="btn cup2-b" data-cup="enter">Enter · ${CUP_COST} 🪙</button>` : `<button class="btn cup2-b off" disabled>${CUP_COST - g} more 🪙 to enter</button>`}<p class="cup2-f">Top 25 win · closes in ${cupLeft(cupDl())}</p></div>`; } catch (e) { return cc.apply(this, arguments); } }; })();
stLadder = function (p) { const q = p.ql || {}, inQ = p.ql && !q.done, ok = isCashOK(p), miss = missed(p), T = p.tq || { w: 0, l: 0 }, R = p.raced; const done = [], todo = []; let now = null;
  const C = (() => { try { return chList().filter(c => c.pid === p.id); } catch (e) { return []; } })();
  done.push('📷 Entered');
  if (ok) { if (q.done === 'q' || p.qok || R || p.fin) done.push('🎀 Qualified'); else if (T.w >= TQ_WIN) done.push('🏋️ Trained'); done.push('💵 Cash-ready'); }
  if (R) done.push(`🏁 Final · ${ppOrd(R.rank)}${R.prize ? ` · ${money(R.prize)}` : ''}`);
  if (inQ) { const g = Math.min(QS_STEPS, q.got || 0); now = { ic: '🎀', t: q.live ? 'Qualifier race · live now' : `Qualifier · ${g} of ${QS_STEPS} steps`, sub: 'Vote 2 in a row with the crowd = 1 step', pct: g / QS_STEPS }; todo.push('🏁 Final'); }
  else if (miss) { done.push(`🎀 Qualifier lost ${q.w || 0}–${q.l || 0}`); now = { ic: '🏋️', t: `Training · ${T.w} of ${TQ_WIN} wins`, sub: `${TQ_COST} 🪙 a match · win ${TQ_WIN} before ${TQ_WIN} losses`, pct: T.w / TQ_WIN }; todo.push('💵 Cash-ready', '🏁 Final'); }
  else if (p.fin) { const s2 = Math.min(QS_STEPS, (p.fr && p.fr.s) || 0); now = (p.fr && p.fr.go) ? { ic: '🏁', t: 'Final ready · race it now', sub: '6 photos · crowd votes decide', pct: 1 } : { ic: '🏁', t: `Final · ${s2} of ${QS_STEPS} steps`, sub: 'Vote 2 in a row with the crowd = 1 step', pct: s2 / QS_STEPS }; }
  else if (!ok) { now = { ic: '🎀', t: 'Qualifier', sub: 'Vote to start its race', pct: 0 }; todo.push('🏁 Final'); }
  const isD = x => x.includes('lost') ? 'x' : '';
  return `<div class="pg"><p class="pg-k">✓ Done</p><div class="pg-done">${done.map(x => `<span class="${isD(x)}">${isD(x) ? '✕' : '✓'} ${x}</span>`).join('')}</div>
    ${now ? `<p class="pg-k now">▶ Now</p><div class="pg-now"><i>${now.ic}</i><div><b>${now.t}</b><small>${now.sub}</small><span class="pg-bar"><u style="width:${Math.round(now.pct * 100)}%"></u></span></div></div>` : `<p class="pg-k now">▶ Now</p><div class="pg-now idle"><i>🏁</i><div><b>Run complete</b><small>Race it again, or play a cash head-to-head</small></div></div>`}
    ${todo.length ? `<p class="pg-k">Still to do</p><div class="pg-todo">${todo.map((x, i) => `<span><em>${i + 1}</em>${x}</span>`).join('')}</div>` : ''}
    <div class="pg-goal ${ok ? 'on' : ''}"><i>⚔️</i><div><b>Cash challenges</b><small>${!ok ? 'Unlock by getting Cash-ready' : C.length ? `${C.length} player${C.length === 1 ? '' : 's'} want${C.length === 1 ? 's' : ''} to race ${esc(rcName(p))}` : 'Challengers arrive while you’re away'}</small></div>${ok && C.length ? '<button class="ld-b" data-ldc>See</button>' : ok ? '<em>OPEN</em>' : '<em>🔒</em>'}</div></div>`; };
(() => { const ft = finalsTab; finalsTab = function () { const r = ft.apply(this, arguments); try { const sub = document.querySelector('#flow .sx .sx-sub'); if (sub) sub.textContent = 'Your photos and what’s next'; } catch (e) {} return r; }; })();
function fcNotify() {""")
s = s.replace('</style>', """.qls2{text-align:center}.q2-k{margin:4px 0 0;font:900 .78rem Nunito,system-ui;letter-spacing:.12em;text-transform:uppercase;color:#F3D98B}
.q2-ph{width:62%;margin:8px auto 4px;padding:5px;border-radius:18px;background:linear-gradient(135deg,#F3D98B,#C9952D)}.q2-ph img{display:block;width:100%;aspect-ratio:4/3.4;object-fit:cover;border-radius:13px}
.q2-tr .pv-tr{margin:10px 6px 0}.q2-tr .pv-rail{background:rgba(255,255,255,.85)!important}.q2-st{margin:2px 0 10px;font:800 .95rem Nunito,system-ui;color:#F3D98B}
.q2-c{border-radius:18px;background:#FBF6EE;box-shadow:inset 0 0 0 2px #D9AE4F;text-align:left;padding:4px 12px}.q2-r{display:flex;align-items:center;gap:12px;padding:10px 0}.q2-r+.q2-r{border-top:1px solid #E7DCC8}
.q2-r>span{flex:none;width:40px;font-size:1.5rem;text-align:center;border-right:1px solid #E7DCC8;padding-right:8px}.q2-r>div{flex:1}.q2-r b{display:block;font:900 1rem Fraunces,Georgia,serif;color:#14213D}.q2-r small{font:600 .8rem/1.35 Nunito,system-ui;color:#5B4A3F}
.q2-d{display:flex;gap:4px;align-self:flex-start;margin-top:3px}.q2-d i{width:13px;height:13px;border-radius:50%;box-shadow:inset 0 0 0 1.5px #14213D}
.q2-b{margin-top:12px}.q2-b #qsJ{width:100%!important}.q2-two{display:flex;align-items:center;gap:12px;margin-top:10px;padding:10px 12px;border-radius:16px;background:#FBF6EE;box-shadow:inset 0 0 0 2px #D9AE4F;text-align:left;cursor:pointer}
.q2-two>span{font-size:1.5rem}.q2-two b{display:block;font:900 1rem Fraunces,Georgia,serif;color:#14213D}.q2-two small{font:600 .8rem Nunito,system-ui;color:#5B4A3F}
.cup2{position:relative;overflow:hidden;margin:0 0 14px;padding:16px 16px 12px;border-radius:22px;text-align:left;color:#fff;background:radial-gradient(120% 90% at 85% 10%,#2A3E70 0%,#16244A 45%,#0E1830 100%);box-shadow:0 12px 26px -12px rgba(14,24,48,.55)}
.cup2-t{position:absolute;right:12px;top:16px;font-size:3.6rem;filter:drop-shadow(0 6px 12px rgba(243,201,90,.5))}.cup2-k{margin:0 0 6px;display:inline-block;padding-bottom:3px;border-bottom:2px solid #D9AE4F;font:900 .78rem Fraunces,Georgia,serif;font-style:italic;letter-spacing:.1em;text-transform:uppercase;color:#FBF3DC}
.cup2 h3{margin:0 0 4px;font:900 1.7rem/1.05 Fraunces,Georgia,serif;color:#fff}.cup2-s{margin:0 0 12px;max-width:72%;font:600 .88rem/1.35 Nunito,system-ui;color:#DDE3F0}
html body #flow .sx .btn.cup2-b{width:100%!important;min-height:48px!important;margin:0!important;border-radius:999px!important;background:linear-gradient(180deg,#2F8A45,#1E6B34)!important;color:#fff!important;font:900 1.05rem Nunito,system-ui!important}html body #flow .sx .btn.cup2-b.off{background:#3A4766!important;color:#B9C3DA!important}
.cup2-f{margin:8px 0 0;text-align:center;font:700 .76rem Nunito,system-ui;color:#B9C3DA}
.pg{margin:10px 14px 12px;text-align:left}.pg-k{margin:10px 0 5px;font:900 .7rem Nunito,system-ui;letter-spacing:.12em;text-transform:uppercase;color:#2F7A3F}.pg-k.now{color:#9A6B12}.pg-k:not(.now):nth-of-type(n+3){color:#8A7A6A}
.pg-done{display:flex;flex-wrap:wrap;gap:6px}.pg-done span{padding:5px 10px;border-radius:999px;background:#E3F1E5;color:#1E5C2E;font:800 .8rem Nunito,system-ui}.pg-done span.x{background:#F4E4DF;color:#9C3B2B}
.pg-now{display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:#FFF6DA;box-shadow:inset 0 0 0 2px #D9AE4F,0 6px 14px -8px rgba(201,149,45,.6)}.pg-now>i{flex:none;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-size:1.3rem;font-style:normal;background:#fff;box-shadow:0 0 0 3px rgba(217,174,79,.35)}
.pg-now>div{flex:1}.pg-now b{display:block;font:900 1rem Nunito,system-ui;color:#14213D}.pg-now small{display:block;font:600 .78rem Nunito,system-ui;color:#6B5B4B}.pg-bar{display:block;height:8px;margin-top:7px;border-radius:4px;background:#EADFC6;overflow:hidden}.pg-bar u{display:block;height:100%;background:linear-gradient(90deg,#E8C766,#C9952D);text-decoration:none}
.pg-now.idle{background:#F4EBD6;box-shadow:inset 0 0 0 1.5px #E2D5C2}
.pg-todo{display:flex;flex-direction:column;gap:5px}.pg-todo span{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #E7DCC8;color:#8A7A6A;font:800 .86rem Nunito,system-ui}.pg-todo em{width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font-style:normal;font:900 .72rem Nunito,system-ui;background:#EFE6D6;color:#8A7A6A}
.pg-goal{display:flex;align-items:center;gap:10px;margin-top:10px;padding:10px 12px;border-radius:16px;background:#F4EBD6;opacity:.75}.pg-goal.on{opacity:1;background:#14213D;color:#fff}.pg-goal>i{font-style:normal;font-size:1.3rem}.pg-goal>div{flex:1}.pg-goal b{display:block;font:900 .95rem Nunito,system-ui}.pg-goal small{font:600 .76rem Nunito,system-ui;opacity:.8}.pg-goal em{font-style:normal;font:900 .72rem Nunito,system-ui;letter-spacing:.08em;color:#F3D98B}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v230 ok')
