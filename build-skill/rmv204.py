# Real Money build, step 207 (after rmv203.py): a "Your cash" sheet with withdrawal.
#  - Tap the cash balance (not the +) → navy "Your cash" sheet: real cash (can be withdrawn), Bonus Cash (entries only,
#    can't be withdrawn), buttons "Withdraw $12.00" and "Add cash".
#  - Withdraw: minimum $10; choose Bank transfer or PayPal; confirm → "✓ $12.00 is on its way · 1–3 working days".
#    Needs an account (guests are asked to sign up). Past withdrawals are listed.
#  Demo only: no money moves; the balance is reduced to show the flow.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const WD_MIN = 10;
function cashSheet(step, how) { const c = +(S.cash || 0).toFixed(2), bn = +(S.bonus || 0).toFixed(2), ok = c >= WD_MIN, W = S.wd || []; let body;
  if (step === 'pick') body = `<h2 class="t2-h">Withdraw ${money(c)}</h2><p class="t2-s">Where should we send it?</p>
      <div class="cw-opt">${[['bank', '🏦', 'Bank transfer', '1–3 working days'], ['paypal', '🅿️', 'PayPal', 'Usually within 24 hours']].map(o => `<button class="${how === o[0] ? 'on' : ''}" data-cwh="${o[0]}"><span>${o[1]}</span><b>${o[2]}</b><small>${o[3]}</small></button>`).join('')}</div>
      <button class="btn t2-b green" id="cwGo" ${how ? '' : 'disabled'}>Confirm withdrawal</button><button class="t2-inv cw-back" data-cwb><span><b>Back</b></span></button><p class="t2-f">Demo only: no money moves.</p>`;
  else if (step === 'done') body = `<h2 class="t2-h">✓ ${money(how)} is on its way</h2><p class="t2-s">You’ll get an email when it lands.<br>Bank transfers take 1–3 working days.</p><button class="btn t2-b green" data-t2x>Done</button><p class="t2-f">Demo only: no money moved.</p>`;
  else body = `<h2 class="t2-h">Your cash</h2>
      <div class="cw-box"><span>Real cash</span><b>${money(c)}</b><small>Yours to race with or withdraw</small></div>
      ${bn > 0 ? `<div class="cw-box bn"><span>Bonus Cash</span><b>${money(bn)}</b><small>Spent first on entries · can’t be withdrawn · winnings are real cash</small></div>` : ''}
      <button class="btn t2-b green" id="cwW" ${ok ? '' : 'disabled'}>${ok ? `Withdraw ${money(c)}` : `Withdraw · minimum ${money(WD_MIN)}`}</button>${ok ? '' : `<p class="cw-n">${money(WD_MIN - c)} more to reach the minimum withdrawal.</p>`}
      <button class="btn t2-b blue" id="cwAdd">＋ Add cash</button>
      ${W.length ? `<div class="cw-hist"><p>Withdrawals</p>${W.slice(-3).reverse().map(w => `<div><span>${new Date(w.at).toLocaleDateString([], { day: 'numeric', month: 'short' })} · ${w.how === 'paypal' ? 'PayPal' : 'Bank'}</span><b>${money(w.amt)}</b></div>`).join('')}</div>` : ''}
      <p class="t2-f">PhotoPicks keeps a 15% fee from each race’s entries. Prizes are paid to your real cash.</p>`;
  openSheet(`<div class="trc t2 cw"><button class="t2-x" data-t2x aria-label="Close">✕</button>${body}</div>`);
  const B = $('#sheetBody'); B.querySelectorAll('[data-t2x]').forEach(b => b.onclick = () => closeSheet());
  B.querySelectorAll('[data-cwh]').forEach(b => b.onclick = () => cashSheet('pick', b.dataset.cwh)); B.querySelectorAll('[data-cwb]').forEach(b => b.onclick = () => cashSheet());
  if ($('#cwAdd')) $('#cwAdd').onclick = () => { closeSheet(); setTimeout(() => openStore('Add cash to play'), 200); };
  if ($('#cwW')) $('#cwW').onclick = () => { if (S.user && S.user.guest) { closeSheet(); setTimeout(() => openSignup(() => setTimeout(cashSheet, 250), { locked: false, real: 1 }), 200); return; } cashSheet('pick'); };
  if ($('#cwGo')) $('#cwGo').onclick = () => { const amt = +(S.cash || 0).toFixed(2); if (amt < WD_MIN || !how) return; S.wd = (S.wd || []).concat({ amt, how, at: Date.now() }).slice(-20); S.cash = 0; save(); try { paintWallet(); } catch (e) {} cashSheet('done', amt); }; }
document.addEventListener('click', e => { const w = e.target.closest && e.target.closest('#wCash'); if (!w || e.target.closest('.gplus')) return; if (!S || !S.user) return; e.preventDefault(); e.stopImmediatePropagation(); e.stopPropagation(); cashSheet(); }, true);
function fcNotify() {""", 1)
s = s.replace('</style>', """.cw-box{margin:0 0 10px;padding:12px 14px;border-radius:16px;box-shadow:inset 0 0 0 2px #D9AE4F;text-align:center}.cw-box span{display:block;font:900 .74rem Nunito,system-ui;letter-spacing:.1em;text-transform:uppercase;color:#F3D98B}
.cw-box b{display:block;font:900 2.4rem/1.1 Fraunces,Georgia,serif;color:#FBF3DC}.cw-box small{font:600 .82rem Nunito,system-ui;color:#C9D3E6}.cw-box.bn{box-shadow:inset 0 0 0 1.5px #8C9AB5}.cw-box.bn b{font-size:1.5rem;color:#F3D98B}
html body .cw .btn.t2-b{margin:0 0 10px!important}html body .cw .btn.t2-b:disabled{background:#3A4766!important;color:#B9C3DA!important}.cw-n{margin:-4px 0 10px;font:600 .82rem Nunito,system-ui;color:#C9D3E6}
.cw-opt{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 12px}.cw-opt button{padding:12px 6px;border:0;border-radius:14px;background:#FBF6EE;cursor:pointer;font:inherit;box-shadow:0 0 0 1.5px #EADCC6}.cw-opt span{display:block;font-size:1.5rem}
.cw-opt b{display:block;font:800 .95rem Nunito,system-ui;color:#14213D}.cw-opt small{font:600 .72rem Nunito,system-ui;color:#5B4A3F}.cw-opt button.on{box-shadow:0 0 0 3px #E9B949;background:#FFF8E6}
html body .cw .cw-back{justify-content:center;margin:0 0 6px}.cw-hist{margin:4px 0 0;padding:10px 14px;border-radius:14px;background:rgba(255,255,255,.05);text-align:left}.cw-hist p{margin:0 0 4px;font:900 .7rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8C9AB5}
.cw-hist div{display:flex;justify-content:space-between;padding:4px 0;font:700 .86rem Nunito,system-ui;color:#EEF1F8}.cw-hist b{color:#F3D98B}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v204 ok')
# pass 2: "Add cash" readable on navy (outlined)
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .cw .btn.t2-b.blue{background:transparent!important;box-shadow:inset 0 0 0 2px #8C9AB5!important;color:#FBF3DC!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v204 pass2 ok')
