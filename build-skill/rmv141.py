# Real Money build, step 144 (after rmv140.py): Stage 4 — your photos earn from real play; Finals the crowd decides.
#  - Play Pool: at its verdict, a photo picked by 60%+ of voters enters the Play Pool and is used in real games.
#    The verdict says so ("It made the Play Pool") or how close it was.
#  - Royalties (simulated): Play Pool photos are played over time (about 6–20 plays an hour each); each play pays its
#    creator 0.7¢ (30% of a $2 game's fee split across its 20 photo appearances). Starter photos earn 1 🟡 a play.
#    Earnings land in the cash balance (coins for starters).
#  - My Photos: an earnings card at the top ("This week $0.42 · 28 plays · top earner Rex") with how it works;
#    each photo shows plays and earnings.
#  - "While you were away": on return, "Your photos were played 46 times · +$0.32".
#  - Finals the crowd decides: every 5th vote is a pair from the live Final, marked "🔴 Live Final · your vote counts".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<div class="gl-sum"><div><b>${money(tot)}</b><small>prize money</small></div>', '${earnHeadHTML()}<div class="gl-sum"><div><b>${money(tot)}</b><small>prize money</small></div>', 2)
RA("</b> · tap your pick</p>", "</b> · tap your pick${window.__finPair ? ' · <em class=\"fin-tag\">🔴 Live Final · your vote counts</em>' : ''}</p>")
# verdict: Play Pool result
RA("p.vd = { pct, beat, at: Date.now() }; p.views = Math.max(p.views || 20, 20); save(); window.__nudgeAt = Date.now();",
   "p.vd = { pct, beat, at: Date.now() }; p.views = Math.max(p.views || 20, 20); p.pool = pct >= 60 ? Date.now() : 0; p.plAt = Date.now(); save(); window.__nudgeAt = Date.now();")
RA("<p class=\"vd-beat\">Better than <b>${beat} in 10</b> ${esc(cat)} photos</p>",
   "<p class=\"vd-beat\">Better than <b>${beat} in 10</b> ${esc(cat)} photos</p>${p.pool ? `<p class=\"vd-pool ok\">🎉 It made the <b>Play Pool</b>: it now appears in real games and ${p.starter ? 'earns coins' : 'earns you cash'} every time it’s played.</p>` : `<p class=\"vd-pool\">Just short of the <b>Play Pool</b> (60%+). Photos in the pool earn every time they’re played. Try a stronger shot?</p>`}")
# per-photo line
RA("function vdLine(p) { return `<p class=\"vd-l\">👁️ <b>${p.views || 20}</b> views${p.vd ? ` · <b>${p.vd.pct}%</b> picked it` : ' · verdict coming'}${p.starter ? ' · <em>Starter photo · coins only</em>' : ''}</p>`; }",
   "function vdLine(p) { return `<p class=\"vd-l\">👁️ <b>${p.views || 20}</b> views${p.vd ? ` · <b>${p.vd.pct}%</b> picked it` : ' · verdict coming'}${p.starter ? ' · <em>Starter photo · coins only</em>' : ''}</p>${p.pool ? `<p class=\"vd-l vd-e\">▶️ In the Play Pool · <b>${p.plays || 0}</b> plays · earned <b>${p.starter ? `${p.earnC || 0} 🟡` : money(p.earn || 0)}</b></p>` : ''}`; }")
s = s.replace("function fcNotify() {", r"""const ROY = 0.007;
function royAccrue(silent) { const now = Date.now(); let plays = 0, cash = 0, coins = 0;
  (S.photos || []).forEach(p => { if (!p.pool) return; const last = p.plAt || p.pool, hrs = Math.min(48, (now - last) / 3600e3); const r = cpRng(ppHash('pl:' + p.id + Math.floor(now / 60000))), rate = 6 + ((p.vd && p.vd.pct) || 60) / 100 * 14;
    const n = Math.floor(hrs * rate + r()); if (n < 1) return; p.plAt = now; p.plays = (p.plays || 0) + n; plays += n;
    if (p.starter) { p.earnC = (p.earnC || 0) + n; coins += n; } else { const e = +(n * ROY).toFixed(2); p.earn = +((p.earn || 0) + e).toFixed(2); cash += e; }
    p.wk = p.wk || {}; const wk = Math.floor(now / 6048e5); p.wk[wk] = +((p.wk[wk] || 0) + (p.starter ? 0 : n * ROY)).toFixed(3); });
  if (!plays) return null; if (cash) { S.cash = +((S.cash || 0) + cash).toFixed(2); } if (coins) S.gems = (S.gems || 0) + coins; save(); try { paintWallet(); paintGems(); } catch (e) {}
  return { plays, cash: +cash.toFixed(2), coins }; }
function earnHeadHTML() { const P = (S.photos || []).filter(p => p.pool); if (!(S.photos || []).length) return '';
  const wk = Math.floor(Date.now() / 6048e5), week = P.reduce((a, p) => a + ((p.wk || {})[wk] || 0), 0), plays = P.reduce((a, p) => a + (p.plays || 0), 0), top = P.slice().sort((a, b) => (b.earn || 0) - (a.earn || 0))[0], coins = P.reduce((a, p) => a + (p.earnC || 0), 0);
  return `<div class="ern"><p class="ern-k">💵 Your photos’ earnings</p><div class="ern-row"><div><b>${money(+week.toFixed(2))}</b><small>this week</small></div><div><b>${plays}</b><small>plays</small></div><div><b>${P.length}</b><small>in the Play Pool</small></div></div>
    ${top && (top.earn || 0) > 0 ? `<p class="ern-top">⭐ Top earner: <b>${esc(rcName(top))}</b> · ${money(top.earn)}</p>` : coins ? `<p class="ern-top">Starter photo earned <b>${coins} 🟡</b> so far</p>` : `<p class="ern-top">${P.length ? 'Plays start within the hour.' : 'Photos picked by 60%+ of voters join the Play Pool and start earning.'}</p>`}
    <details class="ern-how"><summary>How earnings work</summary><p>Photos in the Play Pool appear in real Photo games. Each time yours is played, you earn a share of that game’s fee (30% of fees go to creators). Owners never see their own photos in games. Simulated in this prototype.</p></details></div>`; }
setInterval(() => { try { if (!S || !S.user) return; const r = royAccrue(true); if (!r) return; const away = Date.now() - (S.lastAway || Date.now()) > 5 * 60e3;
  if (away && $('#app').classList.contains('on') && freeScreen()) { window.__nudgeAt = Date.now();
    popOpen(`<div class="pp"><p class="pp-k">📷 While you were away</p><h2 class="db-h">Your photos were played ${r.plays} times</h2><div class="rv-won"><span>Earned</span><b>${r.cash ? money(r.cash) : `${r.coins} 🟡`}</b></div><p class="db-s">Every time your photo appears in a real game, you earn. More photos in the Play Pool = more plays.</p>
      <button class="btn block db-go" id="waSee">📷 See my photos</button><div style="text-align:center"><button class="link pc-later" id="waAdd">Add another photo</button></div></div>`);
    $('#waSee').onclick = () => { popClose(); go('gallery'); try { renderMyShow(); } catch (e) {} }; $('#waAdd').onclick = () => { popClose(); setTimeout(finPick, 200); }; }
  else if (r.cash >= 0.01) toast(`📷 Your photos earned ${money(r.cash)} · ${r.plays} plays`); S.lastAway = Date.now(); save(); } catch (e) {} }, 20000);
document.addEventListener('visibilitychange', () => { try { if (document.visibilityState === 'hidden' && S) { S.lastAway = Date.now(); save(); } } catch (e) {} });
(() => { const sp = seedPair; seedPair = function () { window.__finPair = false; try { if (S && (S.votes || 0) % 5 === 4) { const g = ppGame(ppSlot()), L = g.ph.map(x => SEED.find(z => z.src === x.src)).filter(Boolean);
      if (L.length >= 2) { const r = cpRng((S.votes || 0) * 13 + ppSlot()), i = Math.floor(r() * L.length); let j = Math.floor(r() * L.length); if (j === i) j = (i + 1) % L.length; window.__finPair = true; return [L[i], L[j]]; } } } catch (e) {} return sp(); }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.fin-tag{font-style:normal;font-weight:900;color:#B03A2E}
.vd-pool{margin:6px 0;padding:8px 10px;border-radius:12px;background:#F3EEE5;font-size:.86rem;text-align:center}.vd-pool.ok{background:#F1F6EC;box-shadow:inset 0 0 0 2px #2F6B3F;color:#22502F}
.vd-e{color:#2F6B3F}
.ern{margin:6px 0 14px;padding:12px 14px;border-radius:16px;background:linear-gradient(135deg,#F1F6EC,#FBF7F0);box-shadow:inset 0 0 0 2px #2F6B3F}
.ern-k{margin:0 0 6px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;font-size:.74rem;color:#22502F}
.ern-row{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;text-align:center}.ern-row b{display:block;font:900 1.35rem Fraunces,Georgia,serif;color:#2F6B3F}.ern-row small{font-size:.72rem;color:#3D5A44}
.ern-top{margin:8px 0 0;font-size:.86rem;color:#14213D;text-align:center}.ern-how{margin-top:6px;font-size:.8rem}.ern-how summary{cursor:pointer;font-weight:800;color:#1E3A6E}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v141 ok')
