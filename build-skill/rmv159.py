# Real Money build, step 162 (after rmv158.py): live duels move into judging; the panel clears finished photos.
#  - The small "🔮 Call a live duel" card is gone (it duplicated voting: every vote already rewards calling the crowd).
#  - Instead, every 5th pair IS another player's live $2 duel: a gold banner above the pair names both players,
#    the prize and the live score ("🥊 LIVE $2 DUEL · winner takes $3.40 · 5–4 · 6 votes to go · your vote decides it").
#    After you vote: "✓ Your vote counted · 6–4". Same coins as any vote.
#  - "Your photos in play" only shows photos still in play (qualifying, finalist, duel live) plus a result not yet seen.
#    A photo that lost its duel or went out leaves the panel; its record lives in My Photos.
#  Simulated: the duel players and the other votes.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("P = (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || (p.raced && now - p.raced.at < 3 * 3600e3) || (p.ql.done === 'x' && now - (p.ql.at || 0) < 3600e3))).slice(0, 3);",
   "P = (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || (p.du && !p.du.shown))).slice(0, 3);")
RA("' · <em class=\"fin-tag\">🔴 Live Final · your vote counts</em>'", "' · <em class=\"fin-tag\">🥊 Live duel · your vote counts</em>'")
s = s.replace("function fcNotify() {", r"""function prNew() { return; }
try { if (S && S.pr) { S.pr = null; } } catch (e) {}
function ldBanner() { const jc = document.getElementById('jcard'), top = document.getElementById('vrTop'), o = document.getElementById('ldB'); if (o) o.remove(); if (!window.__finPair || !jc || !top) return;
  const r = cpRng((S.votes || 0) * 7 + 3), h = () => '@' + QS_NAMES[Math.floor(r() * QS_NAMES.length)], a = 3 + Math.floor(r() * 5), b = 3 + Math.floor(r() * 5), left = 15 - a - b;
  window.__ld = { a, b, ha: h(), hb: h() };
  top.insertAdjacentHTML('afterend', `<div class="ldb" id="ldB"><p class="ldb-h"><span class="qm-live">● LIVE</span><b>🥊 $2 duel</b><em>winner takes ${money(DU_PRIZE)}</em></p>
    <div class="ldb-s"><span>${window.__ld.ha}</span><b id="ldS">${a} – ${b}</b><span>${window.__ld.hb}</span></div>
    <p class="ldb-f" id="ldF">⏱ ${left} votes to go · <b>your vote decides it</b> · <i>simulated</i></p></div>`); }
(() => { const rj = renderJudge; renderJudge = function () { const r = rj.apply(this, arguments); try { ldBanner(); } catch (e) {} return r; }; })();
(() => { const cf = callFx; callFx = function (pick) { const r = cf.apply(this, arguments); try { const L = window.__ld, s1 = document.getElementById('ldS'), f = document.getElementById('ldF');
  if (L && window.__finPair && s1) { if (pick === 0) L.a++; else L.b++; s1.textContent = `${L.a} – ${L.b}`; s1.classList.add('bp'); f.innerHTML = `✓ <b>Your vote counted</b> · ${L.a === L.b ? 'all square' : `${L.a > L.b ? L.ha : L.hb} leads`} · ${15 - L.a - L.b} to go`; document.getElementById('ldB').classList.add('done'); } } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #judge .dpr{display:none!important}
.ldb{margin:6px 2px 8px;padding:8px 12px;border-radius:14px;background:#14213D;box-shadow:0 0 0 2px #D9AE4F;text-align:center;animation:qmFl .35s ease-out both}
.ldb-h{display:flex;align-items:center;gap:8px;margin:0 0 4px}.ldb-h b{font:900 .8rem Nunito,system-ui;letter-spacing:.05em;text-transform:uppercase;color:#F3D98B}.ldb-h em{margin-left:auto;font-style:normal;font:800 .72rem Nunito,system-ui;color:#fff;background:#2F6B3F;border-radius:999px;padding:2px 8px}
.ldb-s{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px}.ldb-s span{font:800 .74rem Nunito,system-ui;color:#C9D3E6;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.ldb-s span:first-child{text-align:right}.ldb-s span:last-child{text-align:left}
.ldb-s b{font:900 1.5rem/1 Fraunces,Georgia,serif;color:#fff}.ldb-s b.bp{animation:qmBp .45s ease-out}
.ldb-f{margin:4px 0 0;font:700 .74rem Nunito,system-ui;color:#C9D3E6}.ldb-f b{color:#F3D98B}.ldb-f i{font-style:normal;color:#8C9AB5;font-size:.66rem}.ldb.done .ldb-f{color:#9FE3AE}
html body #judge:has(.ldb) .vr-stake{display:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v159 ok')
# pass 2: the banner says it all; no second "Live duel" tag under the title
s = open(d + 'yofi-real.html').read()
RA("' · <em class=\"fin-tag\">🥊 Live duel · your vote counts</em>'", "''")
open(d + 'yofi-real.html', 'w').write(s); print('rm v159 pass2 ok')
