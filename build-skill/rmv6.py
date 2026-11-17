# Real Money build, step 9 (after rmv5.py): creator earnings ledger.
# Every payout to a photo's creator is recorded: qualifier 1st place (owner's share) and Best in Show places.
# My show shows total, this week, and the full list; each photo card shows what that photo has earned.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""function earnAdd(e) { S.earn = (S.earn || []).concat(Object.assign({ at: Date.now() }, e)).slice(-200); }
const earnOf = pid => (S.earn || []).filter(e => e.pid === pid).reduce((a, e) => a + e.amt, 0);
const earnWeek = () => { const t = Date.now() - 7 * 864e5; return (S.earn || []).filter(e => e.at >= t).reduce((a, e) => a + e.amt, 0); };
function earnRowHTML(e) { const p = (S.photos || []).find(x => x.id === e.pid), nm = p ? rcName(p) : (e.t || 'Your photo'), show = `${raceName(e.sl)} ${esc(showName(e.k))}`, dt = new Date(e.at), when = dt.toDateString() === new Date().toDateString() ? frTime(e.at) : dt.toLocaleDateString([], { day: 'numeric', month: 'short' });
  return `<div class="er-r">${p ? `<img src="${p.src}" alt="">` : '<span class="er-i">📷</span>'}<div><b>${e.kind === 'q' ? '🥇 Won its qualifier' : `${PP_MED[e.place - 1] || ''} ${ppOrd(e.place)} in Best in Show`}</b><small>${esc(nm)} · ${show} · ${when}</small></div><em>+${money(e.amt)}</em></div>`; }
function earningsOpen() { const L = (S.earn || []).slice().reverse(), tot = L.reduce((a, e) => a + e.amt, 0);
  popOpen(`<div class="pp er"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">💰 Your earnings</p><h2 class="pp-h">${money(tot)} won</h2>
    <p class="pp-m">${money(earnWeek())} this week · ${(n => `${n} qualifier win${n === 1 ? '' : 's'}`)(L.filter(e => e.kind === 'q').length)} · ${(n => `${n} Best in Show place${n === 1 ? '' : 's'}`)(L.filter(e => e.kind === 's').length)}</p>
    <div class="er-l">${L.length ? L.map(earnRowHTML).join('') : '<p class="er-none">No winnings yet. Enter a photo: the 1st place photo in a qualifier earns 10% of its real entries, and Best in Show 🥇🥈🥉 win $10 · $5 · $2.</p>'}</div>
    <div style="text-align:center"><button class="link pc-later" id="erNo">Close</button></div></div>`);
  $('#erNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
document.addEventListener('click', e => { if (e.target.closest('#msEarn')) { e.preventDefault(); e.stopPropagation(); earningsOpen(); } }, true);
function fcNotify() {""", 1)
# record payouts
RA("r.shareWon = +((r.shareWon || 0) + share).toFixed(2);", "r.shareWon = +((r.shareWon || 0) + share).toFixed(2); { const sl0 = rcSlotFor(p); earnAdd({ kind: 'q', pid: id, t: rcName(p), amt: share, sl: sl0, k: ppGame(sl0).k }); }")
RA("S.showWon = +((S.showWon || 0) + pz).toFixed(2);", "S.showWon = +((S.showWon || 0) + pz).toFixed(2); if (pz) earnAdd({ kind: 's', pid: x.pid, t: ph.t, amt: pz, place: pl, sl, k: g.k });")
# My show: earnings box + recent list; each photo shows what it has earned
RA("${r.last && r.last.pz ? `<span class=\"ms-w\">Won ${money(r.last.pz)}</span>` : ''}", "${earnOf(p.id) ? `<span class=\"ms-w\">Earned ${money(earnOf(p.id))}</span>` : ''}")
RA("<div class=\"ms-l\">", "<div class=\"ms-earn\"><div class=\"ms-eh\"><b>💰 Earnings</b><span>${money((S.earn || []).reduce((a, e) => a + e.amt, 0))} total · ${money(earnWeek())} this week</span></div>${(S.earn || []).length ? (S.earn || []).slice(-3).reverse().map(earnRowHTML).join('') : '<p class=\"er-none\">Your winnings will show here: qualifier wins and Best in Show places.</p>'}<button class=\"link ms-all\" id=\"msEarn\">See all earnings ›</button></div><div class=\"ms-l\">")
s = s.replace('</style>', """.er-l{text-align:left;margin:4px 0 8px}.er-r{display:grid;grid-template-columns:44px 1fr auto;gap:10px;align-items:center;padding:7px 0;border-top:1px solid rgba(127,127,127,.18)}.er-r img{width:44px;height:44px;object-fit:cover;border-radius:10px}.er-i{font-size:1.5rem;text-align:center}.er-r b{display:block;font-size:.88rem}.er-r small{font-size:.72rem;opacity:.8}.er-r em{font-style:normal;font-weight:900;color:#2EA36B}.er-none{font-size:.84rem;opacity:.85}
.ms-earn{border-radius:16px;padding:10px 12px 6px;margin:0 0 12px;text-align:left}.ms-eh{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:2px}.ms-eh b{font-size:1rem}.ms-eh span{font-size:.8rem;opacity:.85}.ms-all{display:block;margin:4px auto 2px;font-weight:800}
html:not(.yg) .ms-earn{background:#E8F3EA;color:#2B2320;box-shadow:inset 0 0 0 1.5px #2F6B3F}html.yg .ms-earn{background:#10301F;color:#fff;box-shadow:inset 0 0 0 1.5px #21C77A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v6 ok')
