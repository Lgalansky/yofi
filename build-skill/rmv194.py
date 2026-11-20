# Real Money build, step 197 (after rmv193.py): one-tap rematch on every cash result.
#  - Final result: green "🏁 Race again · $2" and gold "⬆️ Step up · $5 · 1st wins $17.50" above the other buttons.
#    A rematch goes straight to a new Final (new rivals, 3-2-1, race); no voting steps for a rematch.
#    With 300+ coins, "🪙 Race again free · 300 coins" shows too.
#  - Head-to-head result: "⬆️ Step up · $5 · winner takes $8.50" under "New challenge · $2".
#  Simulated: rivals and crowd votes.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<button class="btn block nv-go" id="h2Ag">New challenge · $${fee}</button>',
   '<button class="btn block nv-go" id="h2Ag">New challenge · $${fee}</button>${fee < 5 ? `<button class="btn block nv-up" id="h2Up">⬆️ Step up · $5 · winner takes ${money(5 * H2H_PAY)}</button>` : ""}')
RA("$('#h2Ag').onclick = () => { if (fresh) { popClose(); qfStart(p); } else h2hOpen(p, fee); };", "$('#h2Ag').onclick = () => { if (fresh) { popClose(); qfStart(p); } else h2hOpen(p, fee); }; if ($('#h2Up')) $('#h2Up').onclick = () => h2hOpen(p, 5);")
s = s.replace("function fcNotify() {", r"""(() => { const qr = qfResult; qfResult = function (p, L, ord) { const r = qr.apply(this, arguments); try { const fee = window.__qfFee || 2, up = QF_FEES[QF_FEES.indexOf(fee) + 1], e = document.getElementById('qrE'); if (!e) return r;
    const again = f => { p.fin = 1; p.fr = { s: QS_STEPS, go: 1 }; p.fl = null; save(); window.__qfFee = f; popClose(); payCash(f, `A $${f} Final entry`, () => setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(qfRivals(p))), 250)); };
    e.insertAdjacentHTML('beforebegin', `<button class="btn block db-go cashb" id="qrA">🏁 Race again · $${fee}</button>${up ? `<button class="btn block db-go rm-up" id="qrU">⬆️ Step up · $${up} · 1st wins ${money(up * QF_PAY[0])}</button>` : ''}${(S.gems || 0) >= FIN_COINS ? `<button class="btn block db-go rm-coin" id="qrC">🪙 Race again free · ${FIN_COINS} coins</button>` : ''}`);
    e.classList.add('quiet'); $('#qrA').onclick = () => again(fee); if ($('#qrU')) $('#qrU').onclick = () => again(up);
    if ($('#qrC')) $('#qrC').onclick = () => { S.gems -= FIN_COINS; p.fin = 1; p.fr = { s: QS_STEPS, go: 1 }; p.fl = null; save(); try { paintGems(); } catch (x) {} window.__qfFee = 2; popClose(); setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(qfRivals(p))), 250); }; } catch (x) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .btn.rm-up{background:linear-gradient(180deg,#F3D98B,#D9AE4F)!important;color:#14213D!important;margin-top:8px!important}html body .btn.rm-coin{background:#14213D!important;color:#F3D98B!important;margin-top:8px!important}
html body .h3 .btn.nv-up{min-height:48px!important;margin:10px 0 0!important;border-radius:999px!important;background:linear-gradient(180deg,#F3D98B,#D9AE4F)!important;color:#14213D!important;font:800 1.05rem Nunito,system-ui!important;box-shadow:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v194 ok')
