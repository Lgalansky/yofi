# Real Money build, step 195 (after rmv191.py): My Photos becomes your trophy wall.
#  - Navy earnings banner: total cash your photos have won, this week, counts (Finals, head-to-head wins, rosettes).
#  - Each photo in a gold frame with its rosettes hanging on it, name + real category, a record row
#    (Qualifiers · Finals · Head-to-head · Cash won) and ONE status line in today's rules that taps to the right place:
#      "1 of 3 steps to its qualifier race" / "Qualifier race live" → Vote; "Qualified · 2 of 3 steps to the Final" → Vote;
#      "Your Final is waiting" → Final lobby; "💵 Ready for Cash Races" → Stable; "Training 1–0 · win 3…" → Stable.
#  - Best photos first (cash won, then progress). Recent winnings listed with clear labels.
#  - Removed: the stale "8 more wins / losses to spare" text, "Race" shortcut, the 100-coin entry box.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function twCat(p) { try { const k = photoShow(p) || finCatOf(p) || (SHOW_ROT.find(z => z.k === p.cat) || {}).k; return k ? showName(k) : ''; } catch (e) { return ''; } }
function twStatus(p) { const q = p.ql;
  if (q && !q.done) return q.live ? { t: '🔴 Qualifier race live', a: 'v', c: 'q' } : { t: `🎀 ${Math.min(QS_STEPS, q.got || 0)} of ${QS_STEPS} steps to its qualifier race`, a: 'v', c: 'q' };
  if (p.fin) { const fr = p.fr || { s: 0 }; return fr.go ? { t: '🏁 Your Final is waiting', a: 'f', c: 'f' } : { t: `🏆 Qualified · ${Math.min(QS_STEPS, fr.s || 0)} of ${QS_STEPS} steps to the Final`, a: 'v', c: 'f' }; }
  if (isCashOK(p)) return { t: '💵 Ready for Cash Races', a: 's', c: 'r' };
  const T = p.tq || { w: 0, l: 0 }; if (T.w || T.l) return { t: `🏋️ Training ${T.w}–${T.l} · win ${TQ_WIN} to be Ready for Cash Races`, a: 's', c: 't' };
  return { t: q && q.done === 'x' ? '📷 Missed the cut · train it in your stable' : '😴 Resting · re-enter from your stable', a: 's', c: 'x' }; }
function twRec(p) { const E = (S.earn || []).filter(e => e.pid === p.id), H = p.h2h || { w: 0, l: 0 };
  return { qual: (p.ql && p.ql.done === 'q' ? 1 : 0) + (p.rq || 0), fin: E.filter(e => e.kind === 'f').length + (p.raced && !E.some(e => e.kind === 'f') ? 1 : 0), h: H, cash: stWon(p) }; }
function twCard(p) { const st = twStatus(p), r = twRec(p), L = rzList(p).slice(0, 4);
  return `<div class="tw-c"><div class="tw-fr"><div class="tw-mat"><img src="${p.src}" alt=""></div>${L.length ? `<div class="tw-rz">${L.map((k, i) => `<i style="transform:rotate(${[-8, 6, -3, 9][i]}deg)">${rosette(k)}</i>`).join('')}</div>` : ''}${r.cash ? `<span class="tw-won">${money(r.cash)} won</span>` : ''}</div>
    <div class="tw-pl"><b>${esc(rcName(p))}</b>${twCat(p) ? `<small>${esc(twCat(p))}</small>` : ''}</div>
    <div class="tw-rec"><div><b>${r.qual}</b><small>Qualified</small></div><div><b>${r.fin}</b><small>Finals</small></div><div><b>${r.h.w}–${r.h.l}</b><small>Head-to-head</small></div><div><b>${money(r.cash)}</b><small>Cash won</small></div></div>
    <button class="tw-st ${st.c}" data-twa="${st.a}" data-pid="${p.id}"><span>${st.t}</span><em>›</em></button></div>`; }
function renderMyShow() { const g = $('#gallery'); if (!g) return; const P = (S.photos || []).filter(p => p.framed && !(p.starter && !p.ql));
  if (!P.length) return renderMyShowIntro(); $('#ptitle').textContent = 'My Photos';
  const rank = p => { const st = twStatus(p).c; return ({ f: 0, q: 1, r: 2, t: 3, x: 4 })[st]; };
  const L = P.slice().sort((a, b) => stWon(b) - stWon(a) || rank(a) - rank(b));
  const E = S.earn || [], tot = E.reduce((a, e) => a + (e.amt || 0), 0), wk = earnWeek(), nRz = P.reduce((a, p) => a + rzList(p).length, 0);
  const lab = e => e.kind === 'h2' ? '💵 Head-to-head win' : e.kind === 'f' ? `🏁 Final · ${ppOrd(e.place || 1)}` : e.kind === 'du' ? '🥊 Duel win' : '🏆 Prize';
  g.innerHTML = `<div class="ms tw"><h1 class="tw-h">My Photos</h1><p class="tw-sub">Your trophy wall</p>
    <div class="tw-bank"><span>Your photos have won</span><b>${money(tot)}</b><small>${money(wk)} this week · ${E.filter(e => e.kind === 'f').length} Final prize${E.filter(e => e.kind === 'f').length === 1 ? '' : 's'} · ${E.filter(e => e.kind === 'h2').length} head-to-head win${E.filter(e => e.kind === 'h2').length === 1 ? '' : 's'} · ${nRz} rosette${nRz === 1 ? '' : 's'}</small></div>
    ${L.map(twCard).join('')}
    ${E.length ? `<div class="tw-earn"><p class="tw-k">Recent winnings</p>${E.slice(-5).reverse().map(e => { const ph = P.find(x => x.id === e.pid); return `<div class="tw-er">${ph ? `<img src="${ph.src}" alt="">` : '<span>🏆</span>'}<div><b>${lab(e)}</b><small>${esc((ph && rcName(ph)) || e.t || '')}</small></div><em>+${money(e.amt)}</em></div>`; }).join('')}</div>` : ''}
    <button class="sx-add" data-twn><b>＋</b> Add a photo · free</button></div>`;
  g.querySelectorAll('[data-twa]').forEach(b => b.onclick = () => { const p = S.photos.find(x => x.id === b.dataset.pid), a = b.dataset.twa;
    if (a === 'v') { go('judge'); renderJudge(); } else if (a === 'f') qfStart(p); else finalsTab(); });
  g.querySelectorAll('[data-twn]').forEach(b => b.onclick = () => finPick()); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.tw{padding:4px 2px 24px;text-align:left}.tw-h{margin:4px 4px 0;font:900 2.1rem/1.05 Fraunces,Georgia,serif;color:#14213D}.tw-sub{margin:0 4px 12px;font:italic 600 1.1rem Fraunces,Georgia,serif;color:#9A6B12}
.tw-bank{margin:0 0 16px;padding:14px 16px;border-radius:18px;background:linear-gradient(180deg,#22325A,#14213D);box-shadow:0 0 0 2px #D9AE4F,0 6px 18px rgba(20,33,61,.2);text-align:center;color:#C9D3E6}
.tw-bank span{display:block;font:800 .8rem Nunito,system-ui;letter-spacing:.1em;text-transform:uppercase;color:#F3D98B}.tw-bank b{display:block;font:900 2.6rem/1.1 Fraunces,Georgia,serif;color:#F3D98B}.tw-bank small{font:700 .8rem Nunito,system-ui}
.tw-c{margin:0 0 18px;padding:12px 12px 12px;border-radius:20px;background:#FFFCF6;box-shadow:inset 0 0 0 1.5px #E5C987,0 6px 18px rgba(20,33,61,.08)}
.tw-fr{position:relative;padding:7px;border-radius:12px;background:linear-gradient(135deg,#F3D98B,#C9963A 45%,#F6E3A6 70%,#B8862E);box-shadow:0 4px 12px rgba(120,80,20,.3)}.tw-mat{padding:6px;background:#FBF6EE;border-radius:6px}.tw-mat img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:3px}
.tw-rz{position:absolute;top:-14px;right:-6px;display:flex;gap:0}.tw-rz i{display:block;width:62px;margin-left:-20px;filter:drop-shadow(0 3px 5px rgba(0,0,0,.35))}.tw-rz i svg{width:100%;height:auto;display:block}
.tw-won{position:absolute;left:16px;bottom:16px;padding:4px 12px;border-radius:999px;background:#14213D;box-shadow:0 0 0 2px #D9AE4F;font:900 1rem Fraunces,Georgia,serif;color:#F3D98B}
.tw-pl{margin:10px auto 8px;padding:6px 14px;max-width:80%;border-radius:8px;background:linear-gradient(180deg,#F6E7C1,#E5C987);box-shadow:0 2px 4px rgba(0,0,0,.15);text-align:center}.tw-pl b{display:block;font:900 1.2rem Fraunces,Georgia,serif;color:#14213D}.tw-pl small{font:700 .78rem Nunito,system-ui;color:#5B3D06}
.tw-rec{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin:0 0 10px;text-align:center}.tw-rec div{padding:6px 2px;border-radius:10px;background:#F3EEE5}.tw-rec b{display:block;font:900 1.05rem Fraunces,Georgia,serif;color:#14213D}.tw-rec small{font:700 .64rem Nunito,system-ui;color:#5B4A3F}.tw-rec div:last-child b{color:#2F6B3F}
.tw-st{display:flex;align-items:center;justify-content:space-between;gap:8px;width:100%;padding:11px 14px;border:0;border-radius:12px;cursor:pointer;font:800 .9rem Nunito,system-ui;text-align:left;background:#EEF2F8;color:#14213D}.tw-st em{font-style:normal;font-size:1.3rem}
.tw-st.f{background:#FFF1C9;color:#5B3D06}.tw-st.q{background:#E3EFDF;color:#1E5C2E}.tw-st.r{background:#E3EFDF;color:#1E5C2E}.tw-st.t{background:#E6ECF8;color:#2E4F8A}.tw-st.x{background:#F3EEE5;color:#5B4A3F}
.tw-earn{margin:4px 0 14px;padding:12px 14px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.tw-k{margin:0 0 6px;font:900 .74rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8A7B6C}
.tw-er{display:flex;align-items:center;gap:10px;padding:7px 0;border-top:1px solid #F0E6D6}.tw-er:first-of-type{border-top:0}.tw-er img{width:40px;height:40px;border-radius:8px;object-fit:cover}.tw-er div{flex:1;min-width:0}.tw-er b{display:block;font:800 .88rem Nunito,system-ui;color:#14213D}.tw-er small{font:600 .76rem Nunito,system-ui;color:#5B4A3F}.tw-er em{font-style:normal;font:900 1rem Fraunces,Georgia,serif;color:#2F6B3F}
html body #gallery .tw .sx-add{font:700 1.1rem Nunito,system-ui}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v192 ok')
