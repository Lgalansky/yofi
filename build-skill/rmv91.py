# Real Money build, step 94 (after rmv90.py): the Gallery changes once you have a framed photo.
#  Before: the intro pitch ("Turn your photos into cash prizes"), how-it-works and callouts came first; your photos last.
#  Now (1+ framed photo) the Gallery is your creator page:
#   - "My gallery" + record strip (prize money · framed · Finals · qualifiers)
#   - each framed photo shown as on the framing reveal (thick gold frame, brass plaque) with a live status card:
#       in the qualifiers → tries left, "next qualifier in N votes", its Final, "Vote to move it along"
#       finalist → which Final, Watch / Finalists
#       resting → its record and "Enter again · free"
#   - Ready to frame (unframed photos), photo earnings
#   - compact "Add another photo · 200 coins" card, upcoming Finals, how creator prizes are shared (fold)
#  Players with no framed photo still see the intro page.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function renderMyShow() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const cur = ppSlot(), ff = frameFree();",
   "function renderMyShowIntro() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const cur = ppSlot(), ff = frameFree();")
s = s.replace("function fcNotify() {", r"""function renderMyShow() { const g = $('#gallery'); if (!g) return; const P = (S.photos || []), F = P.filter(p => p.framed).sort((a, b) => b.framed - a.framed);
  if (!F.length) return renderMyShowIntro(); $('#ptitle').textContent = 'Gallery';
  const y = isYoungW(), cur = ppSlot(), U = P.filter(p => !p.framed && photoShow(p)), ff = frameFree(), vw = y ? 'Judge' : 'Vote';
  const tot = (S.earn || []).reduce((a, e) => a + e.amt, 0), R = F.map(photoRec), fin = R.reduce((a, r) => a + r.finals, 0), qual = R.reduce((a, r) => a + r.races, 0);
  const card = p => { const r = rcRec(p.id), rec = photoRec(p), SH = SHOWS.find(z => z.k === photoShow(p)), nsl = r.sl || rcSlotFor(p);
    const st = r.st === 'q' ? `<div class="gx-st live"><b>🎀 Finalist · ${raceName(r.sl)} ${esc(showName(ppGame(r.sl).k))} Final</b><small>${r.sl === cur ? 'Racing now · pickers are backing it' : `Races at ${raceName(r.sl)} · finalists’ creators share 10% of the pool`}</small><button class="btn block gx-go" data-glw="${r.sl}">${r.sl === cur ? '🔴 Watch it race' : '🎀 See the finalists'}</button></div>`
      : r.st === 'heats' ? `<div class="gx-st"><b>⚖️ In the qualifiers · ${Math.max(0, HEAT_RUNS - (r.runs || 0))} of ${HEAT_RUNS} tries left</b><small>Next qualifier in <b>${Math.max(1, HEAT_EVERY - (S.hN || 0))} ${vw.toLowerCase()}s</b> · top 2 go through to the <b>${raceName(nsl)} Final</b></small><div class="gx-bar"><i style="width:${Math.min(100, 100 * (S.hN || 0) / HEAT_EVERY)}%"></i></div><button class="btn block gx-go" data-gvote>⚖️ ${vw} to move it along</button></div>`
      : `<div class="gx-st rest"><b>Resting · ready to race again</b><small>Its next Final: <b>${raceName(nsl)} ${SH ? esc(SH.n) : ''}</b></small><button class="btn block gx-go" data-glen="${p.id}">🎀 Enter again · free</button></div>`;
    return `<div class="gx-card"><div class="gx-top"><div class="gx-pic"><div class="gx-frame"><div class="gx-mat"><img src="${p.src}" alt=""></div></div><div class="gx-plq"><b>${esc(p.title || rcName(p))}</b><small>${SH ? esc(SH.n) : ''} · framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small></div></div>
      <div class="gx-side"><div class="gx-rec"><div><b>${money(rec.won)}</b><small>won</small></div><div><b>${rec.finals}</b><small>Final${rec.finals === 1 ? '' : 's'}</small></div><div><b>${rec.best ? ppOrd(rec.best) : '–'}</b><small>best</small></div><div><b>${rec.races}</b><small>qualifiers</small></div></div>${rec.form.length ? `<p class="gl-form">Form <span class="rf">${formHTML(rec.form)}</span></p>` : ''}</div></div>${st}</div>`; };
  const L = SHOW_ROT.map(x => { const sl = finFor(x.k), G = ppGame(sl); return { k: x.k, sl, src: (G.ph[0] || {}).src, pool: G.players * RACE_AVG }; }).sort((a, b) => a.sl - b.sl);
  g.innerHTML = `<div class="ms gl g4 gx"><h1 class="g4-h"><span class="g4-hi">🖼️</span> My gallery</h1><p class="g4-sub">Your framed photos and their prize record.</p>
    <div class="gl-sum"><div><b>${money(tot)}</b><small>prize money</small></div><div><b>${F.length}</b><small>framed</small></div><div><b>${fin}</b><small>Finals</small></div><div><b>${qual}</b><small>qualifiers</small></div></div>
    <h2 class="g4-s">Your photos</h2><div class="gx-wall">${F.map(card).join('')}</div>
    ${U.length ? `<h2 class="g4-s">Ready to frame</h2><div class="gl-un">${U.map(p => `<div><img src="${p.src}" alt=""><b>${esc(p.title || rcName(p))}</b><button class="btn gl-act" data-glfr="${p.id}">🖼️ Frame · ${ff ? 'free' : FRAME_COINS}</button></div>`).join('')}</div>` : ''}
    <div class="g4-earn"><p class="g4-eh"><i class="g4-cash"></i> Photo earnings</p><div class="g4-er"><div><b>${money(tot)}</b><small>Total earned</small></div><span>${money(earnWeek())} this week</span></div>
      ${(S.earn || []).length ? (S.earn || []).slice(-3).reverse().map(earnRowHTML).join('') + '<button class="link ms-all" id="msEarn">See all earnings ›</button>' : '<p class="g4-et">Prize money from your photos shows here.</p>'}</div>
    <button class="gx-add" data-g4go><span>📷</span><span><b>Add another photo</b><small>${ff ? 'Your next frame is free' : `Frame it for ${FRAME_COINS} coins`} · more photos, more Finals</small></span><em>›</em></button>
    <h2 class="g4-s">Upcoming Finals</h2><div class="g4-fin">${L.map(x => `<button data-glk="${x.k}"><img src="${x.src}" alt=""><span><b>${esc(showName(x.k))}</b><small>${raceName(x.sl)} Final</small></span><span class="g4-amt"><b>${money(x.pool * .1)}</b><small>creators share</small></span></button>`).join('')}</div>
    <details class="g4-how2"><summary>How creator prizes are shared</summary><p>Every Final’s 6 finalists’ creators share 10% of the prize pool: <b>1st 4%</b> · <b>2nd 2.5%</b> · <b>3rd 1.5%</b> · <b>4th–6th share 2%</b>. Framed photos can race again free.</p></details></div>`;
  g.querySelectorAll('[data-glk]').forEach(b => b.onclick = () => { window.__preCat = showHint(b.dataset.glk).cats[0]; pickPhoto(true); });
  g.querySelectorAll('[data-glen]').forEach(b => b.onclick = () => showEnter(b.dataset.glen));
  g.querySelectorAll('[data-glfr]').forEach(b => b.onclick = () => frameOpen(P.find(x => x.id === b.dataset.glfr)));
  g.querySelectorAll('[data-glw]').forEach(b => b.onclick = () => +b.dataset.glw === cur ? ppOpen() : raceCard());
  g.querySelectorAll('[data-gvote]').forEach(b => b.onclick = () => { go('judge'); renderJudge(); });
  g.querySelectorAll('[data-g4go]').forEach(b => b.onclick = () => finPick()); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.gx-wall{display:flex;flex-direction:column;gap:16px}.gx-card{background:#FBF6EE;border-radius:20px;box-shadow:inset 0 0 0 1.5px #EADCC6;padding:16px 14px 14px;text-align:center}
.gx-top{display:grid;grid-template-columns:46% 1fr;gap:12px;align-items:center}.gx-pic{width:100%;margin:0}.gx-side{text-align:left}.gx-frame{padding:9px;border-radius:5px;background:linear-gradient(135deg,#F6E3A1 0%,#C9962E 22%,#8A5E16 38%,#E9C46A 52%,#A9771F 70%,#F3D98B 86%,#9B6B1A 100%);box-shadow:inset 0 0 0 3px #6E4A10,inset 0 0 0 6px #E8C46A,inset 0 0 0 8px #7A5212,0 14px 28px -12px rgba(20,33,61,.55)}
.gx-mat{padding:5px;background:#F6EEDC;box-shadow:inset 0 2px 6px rgba(0,0,0,.3)}.gx-mat img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover}
.gx-plq{position:relative;display:block;width:86%;margin:-10px auto 0;padding:5px 6px;text-align:center;border-radius:5px;background:linear-gradient(#F0D88F,#C9A24E 55%,#B08A36);box-shadow:inset 0 0 0 1.5px #8A6420,inset 0 1px 0 rgba(255,255,255,.6),0 6px 12px -6px rgba(0,0,0,.5)}.gx-plq b{display:block;font:800 .95rem/1.15 Fraunces,Georgia,serif;color:#3B2A12}.gx-plq small{font-size:.64rem;color:#5A4220}
.gx-rec{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:0 0 4px}.gx-rec div{background:#fff;border-radius:10px;padding:6px 2px;box-shadow:inset 0 0 0 1px #EADCC6}.gx-rec b{display:block;font:800 1rem Fraunces,Georgia,serif;color:#14213D}.gx-rec div:first-child b{color:#2F6B3F}.gx-rec small{font-size:.68rem}
.gx-st{margin-top:8px;padding:12px;border-radius:14px;background:#E3EAF5;text-align:left}.gx-st.live{background:#FDECEC;box-shadow:inset 0 0 0 1.5px #E7A3A3}.gx-st.rest{background:#F3EDE2}.gx-st b{display:block;color:#14213D;font-size:.98rem}.gx-st small{display:block;margin:2px 0 8px;font-size:.84rem;color:#2B2320}.gx-st small b{display:inline;font-size:inherit}
.gx-bar{height:8px;border-radius:5px;background:#fff;overflow:hidden;margin:0 0 10px}.gx-bar i{display:block;height:100%;background:#D9AE4F;border-radius:5px}
html body .gx .btn.gx-go{background:#1E3A6E!important;color:#fff!important;padding:11px!important;font-size:1rem!important}
html body .gx .gx-add{display:flex;align-items:center;gap:12px;width:100%;margin:14px 0 0;padding:12px 14px;border:0;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #D9AE4F;font:inherit;text-align:left;cursor:pointer;color:#14213D}.gx-add>span:first-child{font-size:1.6rem}.gx-add b{display:block;font:800 1.1rem Fraunces,Georgia,serif}.gx-add small{font-size:.82rem}.gx-add em{margin-left:auto;font-style:normal;font-size:1.6rem;color:#1E3A6E}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v91 ok')
