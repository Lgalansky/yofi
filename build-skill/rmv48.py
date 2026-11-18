# Real Money build, step 51 (after rmv47.py): more hero moments + an exciting live Final.
#  - First real cash win ever: a bigger one-off celebration ("Your first real cash win!").
#  - Your own photo in a Final: reveal highlights it ("📷 Your photo finished 2nd!") and a hero screen shows your creator earnings.
#  - Near miss on a Final pick: "So close! One photo in its exact spot would have paid about $X".
#  - Live Final board: big countdown, "If it ended now: you'd win ~$X" status, ▲/▼ movement arrows, leader-change flash.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# --- first cash win + own photo reveal
RA("function raceOwnResult(sl) {", "function raceOwnResultShow(sl) {")
RA("    () => prize ? heroWin(`You won ${money(prize)}`, `${TR.mine.lab} · real cash`, () => ppResultShow(e)) : ppResultShow(e)); }",
   "    () => prize ? (S.firstCash ? heroWin(`You won ${money(prize)}`, `${TR.mine.lab} · real cash`, () => ppResultShow(e)) : (S.firstCash = 1, save(), heroWin(`${money(prize)}`, `<b>Your first real cash win!</b><br>${TR.mine.lab} · it’s in your wallet now`, () => ppResultShow(e), 1))) : ppResultShow(e)); }")
RA("function heroWin(big, sub, done) { const c = $('#coach');\n  popOpen(`<div class=\"pp rvw\"><p class=\"rvw-k\">🎉 Winner!</p>",
   "function heroWin(big, sub, done, first) { const c = $('#coach');\n  popOpen(`<div class=\"pp rvw ${first ? 'first' : ''}\"><p class=\"rvw-k\">${first ? '🏆 First win!' : '🎉 Winner!'}</p>")
RA("rvConfetti(document.querySelector('.rvw'), 70); let gone = false; const go = () => { if (gone) return; gone = true; done(); }; $('#rvwGo').onclick = go; setTimeout(go, 3600); }",
   "rvConfetti(document.querySelector('.rvw'), first ? 140 : 70); if (first) setTimeout(() => rvConfetti(document.querySelector('.rvw'), 90), 900); let gone = false; const go = () => { if (gone) return; gone = true; done(); }; $('#rvwGo').onclick = go; setTimeout(go, first ? 5200 : 3600); }")
s = s.replace("function fcNotify() {", r"""function raceOwnResult(sl) { const x = S.races[sl]; if (!x || x.__rv) return; x.__rv = 1; const g = ppGame(sl), i = g.ph.findIndex(p => p.mine), pl = i < 0 ? RACE_N : g.ord.indexOf(i) + 1, earn = pl <= RACE_N ? finShare(sl, pl) : 0, ph = i >= 0 ? g.ph[i] : null;
  revealSeq({ ph: g.ph, ord: g.ord, picks: [], mine: i, kicker: `${raceName(sl)} Final · ${esc(showName(g.k))}`, title: ph ? `📷 Your photo “${esc(ph.t)}” is in this Final` : '' },
    () => earn ? heroWin(`You earned ${money(earn)}`, `📷 “${esc(ph.t)}” finished ${ppOrd(pl)} · your creator share`, () => raceOwnResultShow(sl), !S.firstCash && (S.firstCash = 1, save(), 1)) : raceOwnResultShow(sl)); }
function fcNotify() {""", 1)
# reveal: own photo highlight
RA("const { ph, ord, picks, kicker, title } = o;", "const { ph, ord, picks, kicker, title, mine } = o;")
RA("$('#rvMe').innerHTML = hit ?", "$('#rvMe').innerHTML = mine != null && ord[k] === mine ? `<b class=\"ok\">📷 Your photo finished ${RV_ORD[k]}!</b>` : hit ?")
RA("if (hit) { el.classList.add('pop'); rvConfetti(el, 14); } }));",
   "if (hit || (mine != null && ord[k] === mine)) { el.classList.add('pop', 'hit'); rvConfetti(el, 14); } }));\n  if (mine != null && mine >= 0 && !ord.slice(0, 3).includes(mine)) at(1900 + 3 * 1300 + 100, () => { $('#rvMe').innerHTML = `📷 Your photo finished ${ppOrd(ord.indexOf(mine) + 1)} · finalists still share the pool`; });")
RA("${picks.includes(i) ? `<em>${RV_MED[picks.indexOf(i)]}</em>` : ''}", "${picks.includes(i) ? `<em>${RV_MED[picks.indexOf(i)]}</em>` : mine === i ? '<em>📷</em>' : ''}")

# --- near miss chip on the Final result
RA("const chip = ex ? `${ex} in the correct position` :",
   "const nearAmt = (() => { const t = TR.T.find(z => z.k === 1); return t && t.stake ? t.amt * st / (t.stake + st) : 0; })();\n  const chip = !prize && inT ? `So close! One photo in its exact spot would have paid about ${money(nearAmt)}` : ex ? `${ex} in the correct position` :")

# --- live board
s = s.replace("function fcNotify() {", r"""function rbStatus(g, e, L) { if (!e) return ''; const gl = Object.assign({}, g, { ord: L.map(x => x.i) }), T = ppTiers(e, gl), pos = e.picks.map(i => L.findIndex(x => x.i === i) + 1);
  const ex = e.picks.filter((p, k) => pos[k] === k + 1).length;
  return `<div class="rb-st ${T.prize ? 'win' : ''}"><b>${T.prize ? `If it ended now: you’d win ~${money(T.prize)}` : 'If it ended now: no cash yet'}</b><small>${ex ? `${ex} of your picks in the exact spot` : 'Needs 1 pick in its exact spot'} · results in <span class="rb-cd" data-due="${ppDue(e)}">${(() => { const r = Math.max(0, ppDue(e) - Date.now()); return `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}`; })()}</span></small></div>`; }
setInterval(() => { document.querySelectorAll('.rb-cd').forEach(el => { const r = Math.max(0, +el.dataset.due - Date.now()); el.textContent = `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}`; }); }, 1000);
function fcNotify() {""", 1)
RA("return `<div class=\"rb\" id=\"rbLive\"><p class=\"rb-h\"><span class=\"rb-live\">● LIVE</span>${L.reduce((a, x) => a + x.v, 0).toLocaleString()} votes so far</p>${L.map((x, n) => { const p = g.ph[x.i], pk = e ? e.picks.indexOf(x.i) : -1;",
   "const pv = (window.__rbPrev && window.__rbPrev.sl === g.sl) ? window.__rbPrev.r : null, lead = pv && pv[L[0].i] !== 1; window.__rbPrev = { sl: g.sl, r: Object.fromEntries(L.map((x, n) => [x.i, n + 1])) };\n  return `<div class=\"rb\" id=\"rbLive\">${rbStatus(g, e, L)}<p class=\"rb-h\"><span class=\"rb-live\">● LIVE</span>${L.reduce((a, x) => a + x.v, 0).toLocaleString()} votes so far${lead ? ' <span class=\"rb-lead\">🔥 New leader!</span>' : ''}</p>${L.map((x, n) => { const p = g.ph[x.i], pk = e ? e.picks.indexOf(x.i) : -1, mv = pv ? pv[x.i] - (n + 1) : 0;")
RA("<b class=\"rb-n\">${n + 1}</b>", "<b class=\"rb-n\">${n + 1}${mv > 0 ? '<s class=\"up\">▲</s>' : mv < 0 ? '<s class=\"dn\">▼</s>' : ''}</b>")

s = s.replace('</style>', """.rvw.first{background:radial-gradient(circle at 50% 30%,#FFE58A,#FBF3EA 75%)}.rvw.first .rvw-amt{font-size:4.2rem}.rvw.first .rvw-k{font-size:1.6rem}
.rb-st{border-radius:14px;padding:10px 12px;margin:0 0 8px;background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #E8C46A;text-align:center}.rb-st b{display:block;font:800 1.15rem Fraunces,Georgia,serif}.rb-st small{font-size:.82rem}.rb-st.win{background:#E6F0DF;box-shadow:inset 0 0 0 2px #2F6B3F;animation:rbPulse 1.6s ease-in-out infinite}.rb-st.win b{color:#2F6B3F}
@keyframes rbPulse{50%{box-shadow:inset 0 0 0 2px #2F6B3F,0 0 16px rgba(47,107,63,.45)}}.rb-cd{font-weight:900;font-variant-numeric:tabular-nums}
.rb-n s{display:block;text-decoration:none;font-size:.62rem;line-height:1}.rb-n s.up{color:#2EA36B}.rb-n s.dn{color:#C8102E}.rb-lead{margin-left:auto;color:#C8102E;font-weight:900;animation:unGlow 1s 3}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v48 ok')
