# Real Money build, step 170 (after rmv166.py): one progress bar per thing — no accuracy counter on the Vote screen.
#  - Round bar: only coins toward the next photo entry (no "3 ✓" score, no 6 round dots).
#  - "👁️ Your eye: 47% agree with the crowd" line removed.
#  - Round-end banner: "+25 🟡 round bonus" (no "4/6 right").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function vrBarHTML() { const g = Math.floor(S.gems || 0), can = g >= ENTRY_COINS;
  return `<div class="vr-top vr-c" id="vrTop"><div class="vr-l"><b>${can ? '📷 Enough coins for a photo entry' : `🟡 ${ENTRY_COINS - g} more coins to enter a photo`}</b>
    <span class="vr-cb"><i style="width:${Math.min(100, g / ENTRY_COINS * 100)}%"></i></span></div>${can ? `<button class="vr-en" data-vre>Enter · ${ENTRY_COINS} 🟡</button>` : ''}</div>`; }
function vrQuiet(n, ok, pay) { try { paintGems(); gemExplosion(pay, { label: 'Round bonus' }); } catch (e) {}
  const put = () => { try { vrPaint(); } catch (e) {} const top = document.getElementById('vrTop'); if (!top) return; const o = document.getElementById('vrQ'); if (o) o.remove(); const g = Math.floor(S.gems || 0);
    top.insertAdjacentHTML('afterend', `<div class="vrqb" id="vrQ">✓ <b>+${pay} 🟡 round bonus</b><small>${g >= ENTRY_COINS ? '📷 You have enough coins to enter another photo' : `${ENTRY_COINS - g} more coins to your next photo entry`}</small></div>`);
    setTimeout(() => { const e = document.getElementById('vrQ'); if (e) { e.classList.add('bye'); setTimeout(() => e.remove(), 400); } }, 4200); };
  setTimeout(put, 50); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #judge .eye{display:none!important}
html body .vr-top.vr-c{display:flex;align-items:center;gap:12px;padding:10px 14px}html body .vr-top.vr-c .vr-l{flex:1}html body .vr-top.vr-c .vr-en{margin:0;flex:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v167 ok')
# pass 2: won/lost counts never wrap
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """.pv-n .w,.pv-n .l{white-space:nowrap;flex:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v167 pass2 ok')
