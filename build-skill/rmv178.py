# Real Money build, step 181 (after rmv177.py): coins sheet = "Train for Cash Races"; training costs 50 🟡 a match.
#  - Tapping your coins opens: "Train for Cash Races · You have 345 🟡 · enough for 6 training matches",
#    the rule (win 3 before 3 losses = cash-ready for good), then one row per photo: 3 training dots + "Train · 50 🟡",
#    or "💵 Cash-ready" + "Race a Final". No photos yet → "Enter a photo (free), then train it".
#  - Invite a friend as a slim line; "how you earn coins" footer. Old "Photo games" and "Add cash" rows removed.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const DAY_ENT = 5, TQ_COST = 20, TQ_WIN = 3;", "const DAY_ENT = 5, TQ_COST = 50, TQ_WIN = 3;")
s = s.replace("function fcNotify() {", r"""function useGems() { const g = Math.floor(S.gems || 0), n = Math.floor(g / TQ_COST), P = stHorses();
  const row = p => { const ok = isCashOK(p), T = p.tq || { w: 0, l: 0 };
    return `<div class="trc-r"><img src="${p.src}" alt=""><div class="trc-i"><b>${esc(rcName(p))}</b>${ok ? '<small class="ok">💵 Cash-ready ✓</small>' : `<span class="trc-d">${[0, 1, 2].map(i => `<i class="${i < T.w ? 'w' : ''}"></i>`).join('')}<small>${T.w ? `${T.w} of ${TQ_WIN} wins` : 'Not started'}${T.l ? ` · ${T.l} loss${T.l > 1 ? 'es' : ''}` : ''}</small></span>`}</div>
      ${ok ? `<button class="btn trc-b cash" data-tcf="${p.id}">🏁 Race a Final</button>` : `<button class="btn trc-b" data-tct="${p.id}" ${g < TQ_COST ? 'disabled' : ''}>Train · ${TQ_COST} 🟡</button>`}</div>`; };
  openSheet(`<div class="trc"><h2>🏋️ Train for Cash Races</h2><p class="sub">You have <b>${g.toLocaleString()} 🟡</b>${n ? ` · enough for <b>${n} training match${n > 1 ? 'es' : ''}</b>` : ` · ${TQ_COST - g} more for a training match`}</p>
    <div class="trc-rule">Each training match is <b>${TQ_COST} 🟡</b>. Win <b>3</b> before 3 losses and your photo is <b>💵 cash-ready for good</b>: Finals ($2–$20) and cash head-to-heads.</div>
    ${P.length ? `<div class="trc-l">${P.map(row).join('')}</div>` : `<div class="trc-e"><p>📷 Enter a photo (free), then train it here with your coins.</p><button class="btn block db-go" data-tcn>📷 Enter a photo · free</button></div>`}
    <button class="trc-inv" data-tci><span>👥 Invite a friend</span><em>+100 🟡 each when they judge 15 photos ›</em></button>
    <p class="trc-how">Earn coins by voting: round bonuses, +50 🟡 when a photo qualifies. Coins can’t be bought.</p></div>`);
  const B = $('#sheetBody');
  B.querySelectorAll('[data-tct]').forEach(b => b.onclick = () => { const p = S.photos.find(x => x.id === b.dataset.tct); closeSheet(); setTimeout(() => h2hOpen(p, 0), 200); });
  B.querySelectorAll('[data-tcf]').forEach(b => b.onclick = () => { const p = S.photos.find(x => x.id === b.dataset.tcf); closeSheet(); setTimeout(() => qfStart(p), 200); });
  B.querySelectorAll('[data-tcn]').forEach(b => b.onclick = () => { closeSheet(); setTimeout(finPick, 200); });
  B.querySelectorAll('[data-tci]').forEach(b => b.onclick = () => { closeSheet(); setTimeout(openFriends, 200); }); }
function coinTour() { useGems(); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.trc h2{margin-bottom:2px}.trc-rule{margin:8px 0 12px;padding:10px 12px;border-radius:14px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #D9AE4F;font:700 .86rem/1.45 Nunito,system-ui;color:#5B3D06}.trc-rule b{color:#14213D}
.trc-l{display:grid;gap:8px}.trc-r{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.trc-r img{width:52px;height:52px;border-radius:10px;object-fit:cover;flex:none}
.trc-i{flex:1;min-width:0}.trc-i b{display:block;font:800 1rem Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.trc-i small{font:700 .74rem Nunito,system-ui;color:#5B4A3F}.trc-i small.ok{color:#2F6B3F;font-weight:900}
.trc-d{display:flex;align-items:center;gap:5px;margin-top:3px}.trc-d i{width:12px;height:12px;border-radius:50%;background:#EEE6D8}.trc-d i.w{background:#2F6B3F}.trc-d small{margin-left:4px}
html body .trc-b{width:auto!important;min-height:0!important;margin:0!important;padding:9px 14px!important;border-radius:999px!important;font:800 .82rem Nunito,system-ui!important;background:#2E4F8A!important;color:#fff!important;box-shadow:none!important;white-space:nowrap}
html body .trc-b.cash{background:#2F6B3F!important}html body .trc-b:disabled{background:#EEE6D8!important;color:#8A7B6C!important}
.trc-e{padding:12px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:center}.trc-e p{margin:0 0 8px;font:700 .9rem Nunito,system-ui;color:#3D4A5C}
.trc-inv{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;margin:12px 0 0;padding:10px 12px;border:0;border-radius:12px;background:#F3EEE5;cursor:pointer;font:inherit;text-align:left}.trc-inv span{font:800 .88rem Nunito,system-ui;color:#14213D}.trc-inv em{font-style:normal;font:700 .76rem Nunito,system-ui;color:#5B4A3F}
.trc-how{margin:10px 2px 0;font:600 .76rem/1.4 Nunito,system-ui;color:#8A7B6C;text-align:center}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v178 ok')
# pass 2: invite line on one row; compact progress text
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .trc-inv span{white-space:nowrap}html body .trc-inv{background:#F3EEE5!important}html body .trc-d small{white-space:nowrap}
</style>""", 1)
s = s.replace("${T.w ? `${T.w} of ${TQ_WIN} wins` : 'Not started'}${T.l ? ` · ${T.l} loss${T.l > 1 ? 'es' : ''}` : ''}", "${T.w || T.l ? `${T.w}–${T.l} · ${TQ_WIN - T.w} to go` : 'Not started'}", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v178 pass2 ok')
