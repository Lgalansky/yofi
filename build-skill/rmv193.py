# Real Money build, step 196 (after rmv192.py): coins have a real job — 300 coins = a free $2 Final entry.
#  - Final lobby: under "Enter the final · $2", a gold button "🪙 Enter free with 300 coins" (when you have them),
#    or a progress line "🪙 120 more coins for a free $2 entry". It always buys the $2 entry (1st wins $7.00 cash).
#  - Coins sheet: a second gold box "🎟️ 300 coins = a free $2 Final entry" with your progress.
#  Coins stay earned, never sold; they lead to a real-money chance.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const FIN_COINS = 300;
(() => { const qp = qfPick; qfPick = function (p, fee) { const r = qp.apply(this, arguments); try { const go = document.getElementById('qfpGo'); if (!go) return r; const g = Math.floor(S.gems || 0);
    if (g >= FIN_COINS) { go.insertAdjacentHTML('afterend', `<button class="btn block nv-coin" id="qfpCoin">🪙 Enter free with ${FIN_COINS} coins<small>a $2 entry · 1st wins ${money(2 * QF_PAY[0])} cash</small></button>`);
      document.getElementById('qfpCoin').onclick = () => { if ((S.gems || 0) < FIN_COINS) return; S.gems -= FIN_COINS; save(); try { paintGems(); } catch (e) {} window.__qfFee = 2; popClose(); toast(`🪙 −${FIN_COINS} coins · free $2 entry`); const R = qfRivals(p); setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(R)), 250); }; }
    else go.insertAdjacentHTML('afterend', `<p class="nv-coinp">🪙 <b>${FIN_COINS - g} more coins</b> for a free $2 entry<span><i style="width:${Math.min(100, g / FIN_COINS * 100)}%"></i></span></p>`); } catch (e) {} return r; }; })();
(() => { const ug = useGems; useGems = function () { const r = ug.apply(this, arguments); try { const per = document.querySelector('.t2 .t2-per'), g = Math.floor(S.gems || 0); if (per) per.insertAdjacentHTML('afterend',
    `<div class="t2-tk"><b>🎟️ ${FIN_COINS} coins = a free $2 Final entry</b><small>${g >= FIN_COINS ? 'You have enough: use it when you enter a Final.' : `${FIN_COINS - g} more coins to go. Use it in the Final lobby.`}</small><span><i style="width:${Math.min(100, g / FIN_COINS * 100)}%"></i></span></div>`); } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .nv .btn.nv-coin{display:block;width:100%;min-height:52px!important;margin:10px 0 0!important;border-radius:999px!important;background:linear-gradient(180deg,#F3D98B,#D9AE4F)!important;color:#14213D!important;font:900 1.05rem Nunito,system-ui!important;box-shadow:0 4px 12px rgba(0,0,0,.3)!important;line-height:1.15!important;padding:6px 10px!important}
html body .nv .btn.nv-coin small{display:block;font:700 .74rem Nunito,system-ui;color:#3D2B1F}
.nv-coinp{margin:10px 0 0;font:700 .86rem Nunito,system-ui;color:#C9D3E6}.nv-coinp b{color:#F3D98B}.nv-coinp span,.t2-tk span{display:block;height:7px;margin:5px auto 0;max-width:240px;border-radius:4px;background:rgba(255,255,255,.14);overflow:hidden}.nv-coinp i,.t2-tk i{display:block;height:100%;background:linear-gradient(90deg,#F3D98B,#E9B949)}
.t2-tk{margin:0 0 12px;padding:10px 14px;border-radius:14px;background:rgba(233,185,73,.12);box-shadow:inset 0 0 0 1.5px #D9AE4F;text-align:center}.t2-tk b{display:block;font:800 1rem Nunito,system-ui;color:#F3D98B}.t2-tk small{font:600 .82rem Nunito,system-ui;color:#EEF1F8}.t2-tk span{max-width:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v193 ok')
