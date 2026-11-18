# Real Money build, step 116 (after rmv112.py): "Pick the winner" pool, alongside the Top 3.
#  - Final pick screen has two tabs: Top 3 | Winner.
#  - Winner: pick one photo to win. Each photo shows live odds (e.g. 5.1×) and its share of winner picks; odds move as
#    picks come in. Cash from $2 (green) or a free pick with coins (navy, 250, 2 per hour, shared with Top 3).
#    Separate pool: winners share 78% of it (10% creators, 12% PhotoPicks), paid in proportion to their pick, so the
#    final return is the odds when picks close.
#  - After picking: "Winner pick confirmed · Pine road at 5.1×", pool, countdown and the live race (your photo ringed).
#  - Result: the same reveal (1st, 2nd, 3rd), headline "You picked the winner!" / "Not this time", paid at the
#    closing odds; Continue goes back to voting.
#  Simulated: other players' winner picks follow the popularity figures shown on the pick screen.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('popOpen(`<div class="pp pk">${head}<h2 class="pk-h">Win a share of</h2>',
   'popOpen(`<div class="pp pk">${head}<div class="wt-tabs"><button class="on">Top 3</button><button id="wtWin">🏆 Winner</button></div><h2 class="pk-h">Win a share of</h2>')
RA("document.querySelectorAll('#coach [data-rst]').forEach(b => b.onclick = () => { stake = +b.dataset.rst; S.raceSt = stake; save(); draw(); });",
   "document.querySelectorAll('#coach [data-rst]').forEach(b => b.onclick = () => { stake = +b.dataset.rst; S.raceSt = stake; save(); draw(); }); if ($('#wtWin')) $('#wtWin').onclick = () => winOpen(cash);")
# race track: winner pick label + use winner pick when no top-3 pick
RA("const sl = +el.dataset.sl, g = ppGame(sl), e = (S.pp || {})[sl] || { picks: [], at: Date.now() - PP_DEMO / 2, sl, nop: 1 };",
   "const sl = +el.dataset.sl, g = ppGame(sl), W0 = (S.pw || {})[sl], e = (S.pp || {})[sl] || (W0 ? { picks: [W0.pick], at: W0.at, sl, win: 1 } : { picks: [], at: Date.now() - PP_DEMO / 2, sl, nop: 1 });")
RA("<span class=\"rtk-lab\">${p.mine ? '<u>📷 Your photo</u> ' : ''}${pk >= 0 ? `<u>Your ${RT_ORD[pk]} pick</u> ` : ''}",
   "<span class=\"rtk-lab\">${p.mine ? '<u>📷 Your photo</u> ' : ''}${pk >= 0 ? `<u>${e && e.win ? 'Your winner pick' : `Your ${RT_ORD[pk]} pick`}</u> ` : ''}")
# reveal wording for winner picks
RA("$('#rvH').innerHTML = won ? (o.qual ? 'Spot on!' : w1 ? 'You picked the winner!' : 'You’re a winner!') : 'Not this time';",
   "$('#rvH').innerHTML = won ? (o.qual ? 'Spot on!' : w1 ? 'You picked the winner!' : 'You’re a winner!') : 'Not this time';\n    if (o.win) { const f = ord.indexOf(picks[0]) + 1; $('#rvBox').innerHTML = `<p class=\"rv-sub2\">${won ? `“${esc(ph[picks[0]].t)}” won at ${o.win.odds}×` : `Your pick “${esc(ph[picks[0]].t)}” finished ${ppOrd(f)}`}</p>${won ? `<div class=\"rv-won\"><span>You won</span><b>${o.res.amt}</b></div>` : `<span class=\"rv-res\">${o.res.txt}</span>`}<p class=\"rv-pool\">${title}</p>`; $('#rvS').style.display = 'none'; document.querySelector('.rv').classList.add(won ? 'rv-w' : 'rv-l'); if (won) rvConfetti($('#rvBox'), 40); $('#rvMe').innerHTML = ''; return; }")
s = s.replace("function fcNotify() {", r"""function winOdds(g, t) { const v = ppBack(g, t); return v.map(x => Math.max(1.2, Math.round(780 / Math.max(3, x)) / 10)); }
function winOpen(cash) { const g = ppGame(), w = (S.pw || {})[g.sl]; if (w) { winLive(w); return; } const y = isYoungW(); let pick = null, stake = RACE_ST.includes(S.raceSt) ? S.raceSt : 2;
  const draw = () => { const od = winOdds(g), bk = ppBack(g), freeOk = fqLeft() && (S.gems || 0) >= FREE_BET_COINS;
    popOpen(`<div class="pp pk wp"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🎀 The ${raceName(g.sl)} Final · ${esc(showName(g.k))}</p>
      <div class="wt-tabs"><button id="wtTop">Top 3</button><button class="on">🏆 Winner</button></div>
      <h2 class="pk-h">Pick the winner</h2><p class="pk-sub">Which photo will the crowd vote 1st? Long shots pay more.</p>
      <div class="pp-g g6 wp-g">${g.ph.map((p, i) => `<button class="pp-t ${pick === i ? 'on' : ''}" data-wp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${pick === i ? '<i class="pp-b">🏆</i>' : ''}<em class="wp-od">${od[i]}×</em></span><span class="pp-nm"><b>${esc(p.t)}</b><small>${bk[i]}% of winner picks</small></span></button>`).join('')}</div>
      <p class="pp-i">${pick == null ? 'Tap the photo you think will win' : `<b>${esc(g.ph[pick].t)}</b> at <b>${od[pick]}×</b>: a ${money(stake)} pick returns about <b>${money(stake * od[pick])}</b>`}</p>
      ${cash ? `<div class="rc-st" role="group" aria-label="Entry">${RACE_ST.map(v => `<button data-wst="${v}" aria-pressed="${v === stake}">$${v}</button>`).join('')}</div><button class="btn block pc-go pk-go cashb" id="wpGo" ${pick == null ? 'disabled' : ''}>${pick == null ? 'Choose your winner' : `Pick to win · ${money(stake)}`}</button>`
        : `<button class="btn block pc-go pk-go" id="wpFree" ${pick != null && freeOk ? '' : 'disabled'}>${pick == null ? 'Choose your winner' : `🎟️ Free winner pick · ${FREE_BET_COINS} 🟡`}</button>${!freeOk ? `<p class="pp-r">${!fqLeft() ? `Both free picks used this hour` : `${FREE_BET_COINS - Math.floor(S.gems || 0)} more 🟡 for a free pick`}</p>` : `<p class="pp-r">A free pick counts as a $2 pick.</p>`}`}
      <p class="pp-r">Winner pickers share 78% of the winner pool, in proportion to their pick. Odds move as picks come in and are fixed when picks close. ${y ? 'Judges' : 'Voters'} decide the result.</p>
      <div style="text-align:center"><button class="link pc-later" id="wpLater">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
    document.querySelectorAll('#coach [data-wp]').forEach(b => b.onclick = () => { pick = +b.dataset.wp; draw(); });
    document.querySelectorAll('#coach [data-wst]').forEach(b => b.onclick = () => { stake = +b.dataset.wst; S.raceSt = stake; save(); draw(); });
    const rec = (st, free) => { S.pw = S.pw || {}; S.pw[g.sl] = { sl: g.sl, pick, stake: st, free: free ? 1 : 0, at: Date.now(), players: g.players, odds: winOdds(g)[pick] }; save(); setTimeout(() => winLive(S.pw[g.sl]), 150); };
    if ($('#wpGo')) $('#wpGo').onclick = () => { if (pick == null) return; popClose(); payCash(stake, 'A winner pick', () => rec(stake)); };
    if ($('#wpFree')) $('#wpFree').onclick = () => { if (pick == null) return; if (S.user && S.user.guest) { popClose(); openSignup(() => setTimeout(() => winOpen(cash), 200), { locked: false, pick: 1 }); return; } if (!fqLeft() || (S.gems || 0) < FREE_BET_COINS) return; fqClaim(); rec(2, true); };
    $('#wtTop').onclick = () => { popClose(); window.__ppCash = cash ? 1 : 0; setTimeout(ppOpen, 120); }; $('#wpLater').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); };
  draw(); }
function winLive(w) { const g = ppGame(w.sl), od = winOdds(g)[w.pick], mm = r => `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}`;
  popOpen(`<div class="pp wlv"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🎀 The ${raceName(g.sl)} Final · ${esc(showName(g.k))}</p>
    <div class="lk-tk"><span class="lk-k">🏆 Winner pick confirmed</span><b class="lk-h">${esc(g.ph[w.pick].t)} to win</b><span class="lk-ph"><i><img src="${g.ph[w.pick].src}" alt=""><em>${w.free ? 'Free pick' : money(w.stake)} · now ${od}×</em></i></span></div>
    <div class="lk-row"><div class="lk-pz"><small>Cash prize pool</small><b>${ppPool(w.players || g.players)}</b><span>${w.players || g.players} players</span></div><div class="lk-cd"><small>Results in</small><b class="rb-cd" data-due="${ppDue(w)}">${mm(Math.max(0, ppDue(w) - Date.now()))}</b><span>${raceName(g.sl)} Final</span></div></div>
    ${raceTrackHTML(g, { picks: [w.pick], win: 1 })}<p class="pp-i"><small>Demo: results arrive about 2 minutes after you pick.</small></p>
    <button class="btn block pc-go" id="wlOk">${isYoungW() ? 'Keep judging' : 'Keep voting'}</button></div>`);
  $('#wlOk').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function winResult(w) { if (w.__rv) return; w.__rv = 1; const g = ppGame(w.sl), od = winOdds(g, (w.sl + 1) * PP_MS - 1)[w.pick], won = g.ord[0] === w.pick, st = w.stake || 2, prize = won ? +(st * od).toFixed(2) : 0;
  w.done = 1; w.prize = prize; w.odds = od; if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); paintWallet(); } save();
  revealSeq({ ph: g.ph, ord: g.ord, picks: [w.pick], win: { odds: od }, res: { won, amt: money(prize), txt: won ? `You won ${money(prize)}` : 'No cash this time' }, kicker: `${raceName(g.sl)} Final · Winner pick`, title: `${ppPool(w.players || g.players)} prize pool · ${w.players || g.players} players` },
    () => { popClose(); if (prize) setTimeout(() => cashExplosion && cashExplosion(prize, { label: 'Winner pick' }), 300); }); }
setInterval(() => { try { if (!S || !S.pw) return; const e = Object.values(S.pw).find(x => !x.done && Date.now() >= ppDue(x)); if (!e) return; if (busyUI() && !document.querySelector('#coach.on .wlv')) return; popClose(); window.__uiT = 0; setTimeout(() => winResult(e), 300); } catch (x) {} }, 1500);
function fcNotify() {""", 1)
s = s.replace('</style>', """.wt-tabs{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;margin:6px 0 10px;border-radius:999px;background:#E3EAF5}
html body .ppop .wt-tabs button{border:0;border-radius:999px;padding:9px 6px;font:800 .98rem Nunito,system-ui,sans-serif;background:transparent;color:#1E3A6E!important;-webkit-text-fill-color:#1E3A6E;cursor:pointer}
html body .ppop .wt-tabs button.on{background:#1E3A6E!important;color:#fff!important;-webkit-text-fill-color:#fff;box-shadow:0 4px 10px -6px rgba(20,33,61,.7)}
.wp-od{position:absolute;right:6px;bottom:6px;font-style:normal;font-weight:900;font-size:.9rem;padding:3px 9px;border-radius:999px;background:#14213D;color:#F3D98B;box-shadow:0 0 0 1.5px #D9AE4F}html body .ppop .wp-od{-webkit-text-fill-color:#F3D98B}
.wp-g .pp-im{position:relative}html body .ppop .wp .pp-t.on{box-shadow:0 0 0 3px #D9AE4F,0 0 16px rgba(217,174,79,.6)!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v113 ok')
s = open(d + 'yofi-real.html').read()
RA("<i class=\"rv-you ${yi === k ? 'ok' : ''}\">Your ${['1st', '2nd', '3rd'][yi]} pick</i>", "<i class=\"rv-you ${yi === k ? 'ok' : ''}\">${o.win ? 'Your winner pick' : `Your ${['1st', '2nd', '3rd'][yi]} pick`}</i>")
open(d + 'yofi-real.html', 'w').write(s); print('rm v113 label ok')
