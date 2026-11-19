# Real Money build, step 143 (after rmv139.py): Stage 3 — your photos in the first session, and reasons to come back.
#  - Photo moment after the first game: "Now let's see how your eye does as a photographer" →
#    📷 Upload your best photo (main) · 🐶 "No photo to hand? Try with a starter photo" (link; coins only, labelled).
#  - Instant verdict a few seconds after a photo is entered: "Your photo's first 20 votes are in · 68% picked it ·
#    better than 7 in 10 pet photos" (simulated), then "every vote you cast = 1 more view for it".
#  - Votes power your photos: each vote you cast adds a view to each of your entered photos; shown on My Photos.
#  - Gallery tab → "My Photos"; each photo shows views, verdict, and "Starter photo · coins only" where relevant.
#  - Reasons to return: a 7-day reward calendar (Day 1 20 🟡 … Day 7 150 🟡, shown once a day after the first game),
#    "full result tomorrow" on the verdict, and a notifications opt-in after the first win (once).
#  - Pop-ups are spaced: at most one of these every 20 s, never over another screen.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("S.photos.unshift(p); S.cur = p.id;", "if (window.__starter) { p.starter = 1; window.__starter = 0; } S.photos.unshift(p); S.cur = p.id;")
RA("S.votes++; S.cpN = (S.cpN || 0) + 1;", "S.votes++; S.cpN = (S.cpN || 0) + 1; (S.photos || []).forEach(q => { if (q.framed) q.views = (q.views || 20) + 1; });")
i = s.index('<button id="segGallery"'); j = s.index('<span>Gallery</span>', i); s = s[:j] + '<span>My Photos</span>' + s[j + len('<span>Gallery</span>'):]
RA("$('#ptitle').textContent = 'Gallery';", "$('#ptitle').textContent = 'My Photos';", 4)
RA('<span class="g4-hi">🖼️</span> My gallery</h1>', '<span class="g4-hi">🖼️</span> My photos</h1>', 2)
RA("framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small>${rzLine(p)}", "framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small>${rzLine(p)}${vdLine(p)}")
# first game → photo moment
RA("S.eyeN = (S.eyeN || 0) + nPicks; S.eyeOk = (S.eyeOk || 0) + ok; S.gmN = (S.gmN || 0) + 1;",
   "S.eyeN = (S.eyeN || 0) + nPicks; S.eyeOk = (S.eyeOk || 0) + ok; S.gmN = (S.gmN || 0) + 1; if (!(S.photos || []).length && !S.phAsked) S.phPend = 1; if (prize && !S.notifAsked) S.notifPend = 1;")
s = s.replace("function fcNotify() {", r"""const freeScreen = () => !document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx') && !(typeof judging !== 'undefined' && judging);
const popGap = () => Date.now() - (window.__nudgeAt || 0) > 20000;
function vdLine(p) { return `<p class="vd-l">👁️ <b>${p.views || 20}</b> views${p.vd ? ` · <b>${p.vd.pct}%</b> picked it` : ' · verdict coming'}${p.starter ? ' · <em>Starter photo · coins only</em>' : ''}</p>`; }
function photoMoment() { S.phAsked = 1; save(); window.__nudgeAt = Date.now();
  popOpen(`<div class="pp phm"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">📷 Your photos</p><h2 class="db-h">Now let’s see how your eye does as a photographer</h2>
    <p class="db-s">Enter a photo and get its <b>verdict in minutes</b>: how many voters pick it. Every vote you cast gives your photo more views, and winners race in the Finals for prizes.</p>
    <button class="btn block db-go" id="phUp">📷 Upload your best photo</button><div style="text-align:center"><button class="link pc-later" id="phStart">🐶 No photo to hand? Try with a starter photo</button></div></div>`);
  document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
  $('#phUp').onclick = () => { popClose(); setTimeout(finPick, 200); };
  $('#phStart').onclick = () => { popClose(); const x = SEED.find(z => z.src && z.cat === 'Pets' && z.id === 'shades') || SEED.find(z => z.src && z.cat === 'Pets'); window.__starter = 1; window.__preCat = 'pets'; window.__sampleURL = x.src; window.__sample = 1; try { $('#file').dispatchEvent(new Event('change', { bubbles: true })); } catch (e) { window.__starter = 0; } }; }
function verdictShow(p) { const r = cpRng(ppHash('vd:' + p.id)), pct = Math.round(52 + r() * 28), beat = Math.max(2, Math.min(9, Math.round((pct - 45) / 4))), cat = ({ pets: 'pet', nature: 'nature', garden: 'garden' })[photoShow(p) || 'pets'] || 'pet';
  p.vd = { pct, beat, at: Date.now() }; p.views = Math.max(p.views || 20, 20); save(); window.__nudgeAt = Date.now();
  popOpen(`<div class="pp vdx"><p class="pp-k">📷 ${p.starter ? 'Your starter photo' : 'Your photo'}</p><h2 class="db-h">Its first 20 votes are in</h2>
    <div class="vd-ph"><img src="${p.src}" alt=""></div><div class="vd-big"><b>${pct}%</b><span>of voters picked it</span></div>
    <p class="vd-beat">Better than <b>${beat} in 10</b> ${esc(cat)} photos</p>
    <p class="db-s">It’s in the qualifiers now. <b>Every vote you cast = 1 more view</b> for it. Full result tomorrow.${p.starter ? '<br><small>Starter photos earn coins only. Upload your own to earn cash.</small>' : ''}</p>
    <button class="btn block db-go" id="vdVote">⚖️ Vote to move it up</button><div style="text-align:center"><button class="link pc-later" id="vdMore">📷 ${p.starter ? 'Upload one of yours' : 'Add another photo'}</button></div></div>`);
  setTimeout(() => { try { rvConfetti(document.querySelector('.vdx'), 30); } catch (e) {} }, 300);
  $('#vdVote').onclick = () => { popClose(); go('judge'); renderJudge(); }; $('#vdMore').onclick = () => { popClose(); setTimeout(finPick, 200); }; }
const CAL_R = [20, 30, 40, 50, 60, 80, 150];
function calShow() { const t = new Date().toDateString(), y = new Date(Date.now() - 864e5).toDateString(), C = S.cal || {}; const n = C.last === y ? Math.min(7, (C.n || 0) + 1) : 1; const day = C.last === y && C.n === 7 ? 1 : n;
  S.cal = { last: t, n: day }; S.gems = (S.gems || 0) + CAL_R[day - 1]; save(); window.__nudgeAt = Date.now();
  popOpen(`<div class="pp calx"><p class="pp-k">🗓️ Daily reward</p><h2 class="db-h">Day ${day} of 7</h2>
    <div class="cal-row">${CAL_R.map((v, i) => `<div class="${i + 1 < day ? 'got' : i + 1 === day ? 'now' : ''}"><small>Day ${i + 1}</small><b>${v}</b><i>🟡</i></div>`).join('')}</div>
    <p class="db-s">+${CAL_R[day - 1]} coins added. ${day < 7 ? `Come back tomorrow for <b>Day ${day + 1}: ${CAL_R[day]} 🟡</b>. Miss a day and it starts again.` : 'You completed the week!'}</p>
    <button class="btn block db-go" id="calOk">Collect</button></div>`);
  $('#calOk').onclick = () => { popClose(); setTimeout(() => { try { paintGems(); gemExplosion(CAL_R[day - 1], { label: `Day ${day} reward` }); } catch (e) {} }, 200); }; }
function notifAsk() { S.notifAsked = 1; S.notifPend = 0; save(); window.__nudgeAt = Date.now();
  popOpen(`<div class="pp"><p class="pp-k">🔔 Stay in the loop</p><h2 class="db-h">Want a nudge when your results are in?</h2><p class="db-s">We’ll tell you when your photo’s result is ready and when tomorrow’s reward is waiting. Nothing else.</p>
    <button class="btn block db-go" id="ntYes">🔔 Yes, nudge me</button><div style="text-align:center"><button class="link pc-later" id="ntNo">Not now</button></div></div>`);
  $('#ntYes').onclick = () => { popClose(); S.notify = 1; save(); try { if (window.Notification && Notification.requestPermission) Notification.requestPermission(); } catch (e) {} toast('🔔 We’ll nudge you when results are in'); }; $('#ntNo').onclick = () => popClose(); }
setInterval(() => { try { if (!S || !S.user || !$('#app').classList.contains('on') || !freeScreen() || !popGap()) return;
  const nv = (S.photos || []).find(p => p.framed && !p.vd && Date.now() - (p.framed || 0) > 6000); if (nv) { verdictShow(nv); return; }
  if (S.phPend && !(S.photos || []).length) { S.phPend = 0; photoMoment(); return; } S.phPend = 0;
  if (S.notifPend && !S.notifAsked) { notifAsk(); return; }
  if ((S.gmN || 0) >= 1 && (!S.cal || S.cal.last !== new Date().toDateString())) { calShow(); return; } } catch (e) {} }, 1500);
function fcNotify() {""", 1)
s = s.replace('</style>', """.vd-l{margin:4px 0 0;font-size:.76rem;color:#1E3A6E}.vd-l b{color:#14213D}.vd-l em{font-style:normal;color:#9A6B12;font-weight:800}
.vd-ph{width:62%;margin:6px auto 8px;border-radius:14px;overflow:hidden;box-shadow:0 0 0 4px #D9AE4F,0 8px 20px rgba(20,33,61,.25)}.vd-ph img{width:100%;display:block;aspect-ratio:3/4;object-fit:cover}
.vd-big{text-align:center}.vd-big b{display:block;font:900 3rem/1 Fraunces,Georgia,serif;color:#2F6B3F}.vd-big span{font-weight:800;color:#5B4A3F;font-size:.9rem}
.vd-beat{text-align:center;margin:6px 0;font-size:1rem;color:#14213D}
.cal-row{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:10px 0}.cal-row div{display:flex;flex-direction:column;align-items:center;padding:6px 0;border-radius:10px;background:#F3EEE5;opacity:.7}.cal-row small{font-size:.58rem;font-weight:800}.cal-row b{font-size:.85rem;color:#14213D}.cal-row i{font-style:normal;font-size:.7rem}
.cal-row div.got{background:#E3EAF5;opacity:.9}.cal-row div.now{background:#FFF1C9;opacity:1;box-shadow:inset 0 0 0 2px #D9AE4F;transform:scale(1.06)}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v140 ok')
# pass 2: starter photo arrives named (one tap to frame); frame screen wording matches the current rules
s = open(d + 'yofi-real.html').read()
RA("if (window.__starter) { p.starter = 1; window.__starter = 0; }", "if (window.__starter) { p.starter = 1; p.title = p.title || window.__starterT || 'Starter photo'; window.__starter = 0; }")
RA("window.__starter = 1; window.__preCat = 'pets';", "window.__starter = 1; window.__starterT = x.title; window.__preCat = 'pets';")
RA("The top 2 in each qualifier go through, and every finalist’s creator shares 10% of the prize pool.</p>", "The top 2 in each qualifier go through, and the finalists’ creators share the Final’s prize.${p.starter ? ' <b>Starter photos win coins only.</b>' : ''}</p>")
RA("<p class=\"g2-foot\">${free ? 'Your first frame is free.' : `You have ${Math.floor(S.gems || 0)} coins.`} Framed photos can race again free.</p>", "<p class=\"g2-foot\">Framing is free. Framed photos can race again free.</p>")
open(d + 'yofi-real.html', 'w').write(s); print('rm v140 pass2 ok')
# pass 3: after framing, "Collecting its first votes…" (3 s) leads straight into the verdict — replaces the
#  "is in the qualifiers!" screen that asked guests to sign up and repeated the old 10%-of-pool rule.
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function upDone(p) { window.__nudgeAt = Date.now();
  popOpen(`<div class="pp vdc"><p class="pp-k">📷 ${esc(rcName(p))}</p><h2 class="db-h">Collecting its first votes…</h2><div class="vd-ph"><img src="${p.src}" alt=""></div><div class="nfx-bar vdc-bar"><i></i></div><p class="db-s">Voters are seeing it now.</p></div>`);
  setTimeout(() => { if (document.querySelector('#coach .vdc')) { popClose(); setTimeout(() => verdictShow(p), 150); } }, 3200); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.vdc-bar i{width:0;animation:vdcFill 3s linear forwards}@keyframes vdcFill{to{width:100%}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v140 pass3 ok')
