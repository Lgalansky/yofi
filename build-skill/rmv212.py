# Real Money build, step 215 (after rmv211.py): a proper celebration when training makes a photo cash-ready.
#  - The third training win now opens a full navy & gold "Ready for Cash Races!" screen (photo, rosette, confetti)
#    shortly after the match result: what is unlocked, what a Final can pay ($2 entry, 1st wins $7; entries up to $20),
#    and one button into the Final. Shown once per photo.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""function crReady(p) { if (!p || p.crSeen) return; p.crSeen = 1; save(); const nm = esc(rcName(p)), lo = QF_FEES[0], hi = QF_FEES[QF_FEES.length - 1], m0 = v => money(v).replace(/\.00$/, '');
  popOpen(`<div class="pp qfx nv qw crr"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Training complete</span></div><h2 class="nv-big sm">Ready for Cash Races!</h2><i class="nv-sw"></i>
    <div class="qw-ph"><img src="${p.src}" alt=""><i class="qw-rz">${rosette('f')}</i></div>
    <p class="qw-r">${nm} earned its place</p><p class="qw-o">${TQ_WIN} training wins · no qualifier needed</p>
    <div class="crr-box"><div><b>⚔️ Cash head-to-heads · open now</b><small>1 on 1 · ${m0(H2H_FEES[0])} entry, winner takes <em>${money(H2H_FEES[0] * H2H_PAY)}</em></small></div>
      <div><b>🏁 Finals · ${QS_STEPS} voting steps away</b><small>6 photos race · ${m0(lo)} entry, 1st wins <em>${m0(lo * QF_PAY[0])}</em> · up to ${m0(hi)} entry, 1st wins <em>${m0(hi * QF_PAY[0])}</em></small></div>
      <div><b>🏆 Daily Cup</b><small>${CUP_COST} coins · $100 in prizes every day</small></div></div>
    <button class="btn block nv-go" id="crrGo">⚔️ Race a ${m0(H2H_FEES[0])} head-to-head</button><button class="btn block nv-go2" id="crrF">⚖️ Vote ${QS_STEPS} steps to the Final</button><div style="text-align:center"><button class="link nv-later" id="crrL">Back to your stable</button></div><p class="nv-sim">Entry fees are real cash · prizes are paid from entries after the PhotoPicks fee</p></div>`);
  try { rvConfetti(document.querySelector('.crr'), 130); } catch (e) {}
  $('#crrGo').onclick = () => { popClose(); h2hOpen(p, H2H_FEES[0]); }; $('#crrF').onclick = () => { popClose(); qfStart(p); }; $('#crrL').onclick = () => { popClose(); finalsTab(); }; }
(() => { const hd = h3Done; h3Done = function (p, o, oh, fee) { const was = p && p.cashOK; const r = hd.apply(this, arguments); try { if (p && !(fee > 0) && p.cashOK && !was) setTimeout(() => { if (document.getElementById('h2Ag')) crReady(p); }, 2200); } catch (e) {} return r; }; })();
function fcNotify() {""")
t = "toast(`🏁 Vote 3 in a row to move ${rcName(p)} on · ${QS_STEPS - (p.fr.s || 0)} steps to the Final`)"
assert s.count(t) == 1, s.count(t)
s = s.replace(t, "toast(`🏁 ${QS_STEPS - (p.fr.s || 0)} voting steps to ${rcName(p)}’s Final · vote ${QS_RUN} in a row with the crowd = 1 step`)")
s = s.replace('</style>', """.crr-box{margin:10px 0 14px;border-radius:16px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(10,16,32,.4);text-align:left;overflow:hidden}
.crr-box div{padding:10px 14px}.crr-box div+div{border-top:1px dashed rgba(217,174,79,.4)}.crr-box b{display:block;font:800 1rem Nunito,system-ui;color:#FBF3DC}.crr-box small{display:block;margin-top:2px;font:600 .82rem/1.35 Nunito,system-ui;color:#C9D3E6}.crr-box em{font-style:normal;font-weight:800;color:#F3D98B}
html body .nv.qw.crr .qw-r{font-size:1.3rem!important;margin:6px 0 2px!important}html body .nv.qw.crr .nv-big{font-size:2rem!important}.crr-box div{padding:8px 14px!important}
html body .nv.qw.crr .qw-rz{transform:scale(.55)!important;transform-origin:top right!important}
html body .nv.qw.crr .qw-ph{width:40%!important;margin-left:auto!important;margin-right:auto!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v212 ok')
