# Real Money build, step 239 (after rmv235.py): Survivor polish.
#  - Coin icon sized like text everywhere (fixes the oversized icon on "Enter · 50").
#  - Play tab heading: "Your stable" / "Coin games" to match the toggle.
#  - Coins sheet lists Survivor (cost 50, opens Coin games).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""(() => { const ft = finalsTab; finalsTab = function () { const r = ft.apply(this, arguments); try { const h = document.querySelector('#flow .sx .sx-h span') || document.querySelector('#flow .sx .sx-h'); if (h) h.textContent = window.__ptab === 'coins' ? 'Coin games' : 'Your stable'; } catch (e) {} return r; }; })();
(() => { const cs = coinSheet; coinSheet = function () { const r = cs.apply(this, arguments); try { const L = document.querySelector('#sheet .cs-l'); if (!L) return r; const V = svS(), g = Math.floor(S.gems || 0);
    const sub = V.in && !V.done ? `Day ${V.day} of ${SV_DAYS} · you’re still in` : g < SV_COST ? `<u>${SV_COST - g} more coins</u>` : `$${SV_PRIZE} for the last ones standing`;
    const btn = V.in && !V.done ? '<button class="btn cs-b" data-svgo>Play</button>' : `<button class="btn cs-b ${g >= SV_COST ? '' : 'off'}" data-svgo ${g >= SV_COST ? '' : 'disabled'}>${gemIcon('cn-ic')} ${SV_COST}</button>`;
    const first = L.querySelector('.cs-r'); (first || L).insertAdjacentHTML(first ? 'afterend' : 'beforeend', `<div class="cs-r"><span class="cs-ic">🛡️</span><div><b>Survivor</b><small>${sub}</small></div>${btn}</div>`); } catch (e) {} return r; }; })();
useGems = coinSheet;
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-svgo]'); if (!b) return; e.preventDefault(); try { closeSheet(); } catch (x) {} window.__ptab = 'coins'; setTimeout(finalsTab, 200); });
function fcNotify() {""")
s = s.replace('</style>', """html body svg.cn-ic{display:inline-block!important;width:1.05em!important;height:1.05em!important;vertical-align:-.16em;flex:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v236 ok')
