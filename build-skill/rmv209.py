# Real Money build, step 212 (after rmv208.py): navy & gold "Add cash" sheet that keeps the entry in view.
#  - A cash entry with too little cash opens a navy sheet: what you tapped ("A $2 head-to-head"), what you have,
#    one offer sized to cover it (welcome: Add $5 + $10 Bonus Cash), what you'll have left after the entry,
#    and one button "Add $5 · enter now" that pays and goes straight into the entry.
#  - "Other amounts" and "Not now" stay. Replaces the older cream "You need $2 cash" pop for payCash entries.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)
RA("if (tot() < amt) { openStore(`${what} costs ${money(amt)} cash.`, () => { if (tot() >= amt) take(); }); return false; }",
   "if (tot() < amt) { addCashNv(amt, what, () => { if (tot() >= amt) take(); }); return false; }")
RA("function fcNotify() {", r"""function addCashNv(amt, what, onBuy) { const have = +((S.cash || 0) + (S.bonus || 0)).toFixed(2), w = !S.paidCash && !S.bonusGot, bn = w ? 10 : 0;
  const add = [5, 10, 20, 50, 100].find(a => have + a + bn >= amt) || 100, left = +(have + add + bn - amt).toFixed(2), m0 = v => money(v).replace(/\.00$/, '');
  const ttl = String(what).replace(/^(The|A|An) /, '').replace(/^./, c => c.toUpperCase());
  try { if ($('#sheet').classList.contains('on')) closeSheet(); } catch (e) {}
  popOpen(`<div class="pp qfx nv acn"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">${w ? 'Welcome offer' : 'Add cash'}</span></div>
    <h2 class="nv-h2">${esc(ttl)}</h2>
    <p class="qw-o">Entry <b class="gold">${m0(amt)}</b> · you have <b class="gold">${m0(have)}</b></p>
    <div class="acn-box"><div class="h2w-amt">${m0(add)}</div>${w ? '<span class="acn-bn">+ $10 Bonus Cash free</span>' : ''}
      <small>${w ? 'Bonus Cash is spent first on entries and can’t be withdrawn. Your winnings are real cash.' : 'Cash to play. Your winnings are real cash.'}</small>
      <p class="acn-left">After this entry you’ll have <b>${m0(left)}</b> left to play</p></div>
    <button class="btn block nv-go" id="acnGo">Add ${m0(add)} · enter now</button>
    <div style="text-align:center"><button class="link nv-later" id="acnAll">Other amounts</button> <button class="link nv-later" id="acnNo">Not now</button></div><p class="nv-sim">Demo · no real payment is taken</p></div>`);
  $('#acnGo').onclick = () => { popClose(); checkout(`$${add} cash`, add, () => applyOffer(add, 0, w ? 'Welcome offer · $10 Bonus Cash' : `$${add} pack`, () => { S.cashMode = 1; save(); if (w && !S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + 10).toFixed(2); save(); toast('🎁 $10 Bonus Cash added · used first on entries'); } if (onBuy) onBuy(); })); };
  $('#acnAll').onclick = () => { popClose(); openStore(null, onBuy, 'cash'); }; $('#acnNo').onclick = () => popClose(); }
function fcNotify() {""")
s = s.replace('</style>', """.acn-box{margin:10px 0 14px;padding:14px 12px;border-radius:16px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(10,16,32,.4);text-align:center}
.acn-box .h2w-amt{margin:0;line-height:1}.acn-bn{display:inline-block;margin:8px 0 2px;padding:5px 14px;border-radius:999px;background:linear-gradient(180deg,#F3D98B,#D9AE4F);font:900 .95rem Nunito,system-ui;color:#14213D}
.acn-box small{display:block;margin-top:8px;font:600 .8rem/1.4 Nunito,system-ui;color:#C9D3E6}.acn-left{margin:10px 0 0;padding-top:10px;border-top:1px dashed rgba(217,174,79,.5);font:700 .92rem Nunito,system-ui;color:#EEF1F8}.acn-left b{color:#F3D98B}
.acn .nv-later{margin:0 10px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v209 ok')
