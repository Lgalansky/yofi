# Real Money build, step 188 (after rmv184.py): the Stable in the owner's mock-up style.
#  - "Your stable" with gold rules, "Qualify once. Race for cash anytime."
#  - Photos Ready for Cash Races: hero card — big photo with name and "$8.50 won" (all cash it has won), rosette,
#    "Cash races unlocked", chip "Head-to-head 1–1 · Form +2", green "🏁 Enter a final" and outlined
#    "VS Head-to-head" (entry $2 shown above).
#  - Other photos: compact card — photo, name, status (In qualifying / Missed the cut / Resting), form chip,
#    "Win 3 before 3 losses" with Wins 0/3 and Losses 0/3 chips, "Training costs 50 coins", buttons
#    "⚖️ Vote to advance" (or "Re-enter qualifier") and "🏋️ Train".
#  - "+ Add a photo" at the bottom. Ready photos are listed first.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function stWon(p) { return +((S.earn || []).filter(e => e.pid === p.id).reduce((a, e) => a + (e.amt || 0), 0)).toFixed(2); }
function stHero(p) { const H = p.h2h || { w: 0, l: 0 }, won = stWon(p), rz = (p.rz && p.rz[0]) || (H.w > 0) ? rosette(0) : rosette('f');
  return `<div class="sx-hero"><div class="sx-ph"><img src="${p.src}" alt=""><i class="sx-rz">${rz}</i><div class="sx-cap"><b>${esc(rcName(p))}</b>${won ? `<em>${money(won)} won</em>` : '<em class="no">Ready to race</em>'}</div></div>
    <p class="sx-rule"><span>Cash races unlocked</span></p><p class="sx-chip">Head-to-head ${H.w}–${H.l} <i>•</i> Form +${p.form || 0}</p>
    <div class="sx-btns"><button class="btn sx-go" data-stf="${p.id}">🏁 Enter a final</button><div class="sx-h2"><small>Head-to-head entry $2</small><button class="btn sx-ol" data-sth="${p.id}" data-m="c"><i>VS</i> Head-to-head</button></div></div></div>`; }
function stTrain(p) { const q = p.ql, T = p.tq || { w: 0, l: 0 }, inQ = q && !q.done;
  const stt = inQ ? '🎀 In qualifying' : q && q.done === 'x' ? '📷 Missed the cut' : '😴 Resting';
  return `<div class="sx-card"><div class="sx-row"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><span class="sx-st">${stt}</span><span class="sx-f">💪 Form +${p.form || 0}</span></div></div>
    <p class="sx-rule g"><span>Win 3 before 3 losses</span></p><div class="sx-wl"><span class="w">🏆 Wins ${T.w}/${TQ_WIN}</span><span class="l">✕ Losses ${T.l}/${TQ_WIN}</span></div>
    <p class="sx-note">Training costs ${TQ_COST} coins</p>
    <div class="sx-btns two">${inQ ? '<button class="btn sx-nv" data-stv>⚖️ Vote to advance</button>' : `<button class="btn sx-nv" data-str="${p.id}" data-free="1">🎀 Re-enter qualifier</button>`}<button class="btn sx-nv" data-sth="${p.id}" data-m="t">🏋️ Train</button></div></div>`; }
function finalsTab() { const H = stHorses(), R = H.filter(isCashOK), O = H.filter(p => !isCashOK(p));
  openFlow(`<div class="fnx sx"><h1 class="sx-h"><span>Your stable</span></h1><p class="sx-sub">Qualify once. Race for cash anytime.</p>
    ${R.map(stHero).join('')}${O.map(stTrain).join('')}${H.length ? '' : '<div class="sx-card sx-empty"><p>Your stable is empty. Add a photo and vote it into a qualifier, or train it with coins.</p></div>'}
    <button class="sx-add" data-stn><b>＋</b> Add a photo</button><p class="db-sim">Demo · rivals and crowd votes are simulated</p></div>`, false);
  $('#flow').classList.add('astab'); ['segJudge', 'segStudio', 'segGallery'].forEach(id => $('#' + id).setAttribute('aria-pressed', 'false')); $('#segCompete').setAttribute('aria-pressed', 'true'); setTimeout(() => { $('#ptitle').textContent = 'Stable'; }, 0); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.sx{padding-bottom:18px}.sx-h{display:flex;align-items:center;gap:12px;margin:6px 0 2px}.sx-h::before,.sx-h::after{content:'';flex:1;height:2px;background:#D9AE4F}.sx-h span{font:900 2.5rem/1.05 Fraunces,Georgia,serif;color:#14213D}
.sx-sub{margin:0 0 14px;text-align:center;font:600 1.05rem Nunito,system-ui;color:#3D4A5C}
.sx-hero,.sx-card{margin:0 0 14px;padding:0 0 14px;border-radius:20px;background:#FBF6EE;box-shadow:inset 0 0 0 2.5px #D9AE4F,0 6px 18px rgba(20,33,61,.1);overflow:hidden}
.sx-ph{position:relative}.sx-ph img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:18px 18px 16px 16px}
.sx-rz{position:absolute;top:8px;right:10px;width:96px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.4))}.sx-rz svg{width:100%;height:auto;display:block}
.sx-cap{position:absolute;left:0;right:0;bottom:0;padding:44px 16px 12px;background:linear-gradient(transparent,rgba(6,12,28,.85));border-radius:0 0 16px 16px}.sx-cap b{display:block;font:900 2.2rem/1 Fraunces,Georgia,serif;color:#fff}.sx-cap em{font-style:normal;font:900 1.5rem Fraunces,Georgia,serif;color:#F3D98B}.sx-cap em.no{font-size:1.05rem;color:#E8EDF7}
.sx-rule{display:flex;align-items:center;gap:10px;margin:12px 16px 8px}.sx-rule::before,.sx-rule::after{content:'';flex:1;height:1.5px;background:#D9AE4F}.sx-rule span{font:900 1.3rem Fraunces,Georgia,serif;color:#14213D;white-space:nowrap}.sx-rule.g span{font-size:1.1rem;color:#3D2B1F}
.sx-chip{display:table;margin:0 auto 10px;padding:5px 18px;border-radius:999px;background:#EFE6D6;font:800 .92rem Nunito,system-ui;color:#3D2B1F}.sx-chip i{font-style:normal;margin:0 8px;color:#8A7B6C}
.sx-btns{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:end;padding:0 14px}.sx-h2{display:flex;flex-direction:column;align-items:center;gap:3px}.sx-h2 small{font:700 .78rem Nunito,system-ui;color:#3D2B1F}
html body .sx-go{width:100%!important;min-height:50px!important;margin:0!important;border-radius:16px!important;background:linear-gradient(180deg,#2F7A3F,#1E5C2E)!important;color:#fff!important;font:800 1.05rem Nunito,system-ui!important;box-shadow:0 4px 10px rgba(30,92,46,.3)!important}
html body .sx-ol{width:100%!important;min-height:46px!important;margin:0!important;border-radius:999px!important;background:#fff!important;color:#1E5C2E!important;box-shadow:inset 0 0 0 2px #1E5C2E!important;font:800 1.02rem Nunito,system-ui!important;display:flex!important;align-items:center;justify-content:center;gap:8px}
html body .sx-ol i{font-style:normal;width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:#1E5C2E;color:#fff;font:900 .7rem Nunito,system-ui}
.sx-card{padding-top:14px;box-shadow:inset 0 0 0 2px #2F6B3F,0 4px 12px rgba(20,33,61,.08)}.sx-row{display:flex;gap:14px;align-items:center;padding:0 14px}.sx-row img{width:112px;height:104px;border-radius:14px;object-fit:cover;box-shadow:0 0 0 3px #D9AE4F;flex:none}
.sx-row div{display:flex;flex-direction:column;align-items:flex-start;gap:5px;min-width:0}.sx-row b{font:900 1.8rem/1.05 Fraunces,Georgia,serif;color:#14213D;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sx-st{font:800 1rem Nunito,system-ui;color:#3D4A5C}.sx-f{padding:3px 12px;border-radius:999px;background:#EFE6D6;font:800 .88rem Nunito,system-ui;color:#3D2B1F}
.sx-wl{display:flex;justify-content:center;gap:10px;margin:0 14px}.sx-wl span{flex:1;max-width:46%;padding:7px 8px;border-radius:999px;text-align:center;font:800 .98rem Nunito,system-ui}.sx-wl .w{background:#E3EFDF;color:#1E5C2E}.sx-wl .l{background:#F6E1DD;color:#A6402F}
.sx-note{margin:8px 16px 4px;text-align:right;font:700 .8rem Nunito,system-ui;color:#3D2B1F}.sx-btns.two{grid-template-columns:1fr 1fr}
html body .sx-nv{width:100%!important;min-height:44px!important;margin:0!important;border-radius:14px!important;background:linear-gradient(180deg,#22325A,#14213D)!important;color:#fff!important;font:800 .98rem Nunito,system-ui!important;box-shadow:0 3px 8px rgba(20,33,61,.25)!important}
.sx-add{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;min-height:58px;margin:4px 0 6px;border:0;border-radius:18px;background:#FBF3E2;box-shadow:inset 0 0 0 2px #D9AE4F;cursor:pointer;font:800 1.15rem Nunito,system-ui;color:#14213D}.sx-add b{font-size:1.6rem;line-height:1}
.sx-empty p{margin:0;padding:0 16px;text-align:center;font:700 .95rem Nunito,system-ui;color:#3D4A5C}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v185 ok')
# pass 2: stronger button styles inside the flow (no wrapping, right colours)
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #flow .sx .btn{white-space:nowrap;padding:0 10px!important;line-height:1.1!important}
html body #flow .sx .btn.sx-go{background:linear-gradient(180deg,#2F7A3F,#1E5C2E)!important;color:#fff!important;font-size:1rem!important}
html body #flow .sx .btn.sx-ol{background:#fff!important;color:#1E5C2E!important;box-shadow:inset 0 0 0 2px #1E5C2E!important;font-size:.98rem!important}
html body #flow .sx .btn.sx-nv{background:linear-gradient(180deg,#22325A,#14213D)!important;color:#fff!important;font-size:.92rem!important}
html body #flow .sx .sx-add{font:600 1.15rem Nunito,system-ui;color:#14213D}html body #flow .sx .sx-add b{font-weight:900}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v185 pass2 ok')
# pass 3: VS badge text visible
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #flow .sx .btn.sx-ol i{color:#fff!important;-webkit-text-fill-color:#fff!important;background:#1E5C2E!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v185 pass3 ok')
