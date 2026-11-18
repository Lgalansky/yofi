# Real Money build, step 62 (after rmv58.py): FRAMING replaces touch-ups.
#  - A photo enters the qualifiers by being named and framed: 200 coins (a player's first frame is free). No 70+ score.
#    A framed photo can re-enter the qualifiers free whenever its run ends (like a racehorse running again).
#  - Gallery rebuilt: upcoming Finals by category first, "Add a photo to frame", then the framed wall: each photo in a frame
#    with a name plate and its record (races, Finals, best finish, prize money, form). Unframed photos wait under "Ready to frame".
#  - Touch-ups tab hidden; coins menu "Frame a photo" replaces "Touch up"; landing / Choose your Final / tutorial copy updated.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""const FRAME_COINS = 200;
const frameFree = () => !S.frameUsed;
function frameOpen(p, then) { if (!p) return; const k = photoShow(p), SH = SHOWS.find(x => x.k === k), free = frameFree(), y = isYoungW();
  if (!SH) { toast('Only Pets, Nature & landscapes and Garden & flowers photos can be framed for a Final.'); return; }
  const sl = rcSlotFor(p);
  popOpen(`<div class="pp fr3"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🖼️ Frame your photo</p>
    <div class="fr3-frame"><img src="${p.src}" alt=""></div><input class="fr3-name" id="frName" maxlength="28" value="${esc(p.title || '')}" placeholder="Name your photo">
    <p class="fr3-s">Framed photos enter the <b>${esc(SH.n)}</b> qualifiers. Next: the <b>${raceName(sl)} Final</b>. The top 2 in each qualifier go through, and every finalist’s creator shares 10% of the prize pool.</p>
    <button class="btn block fr3-go" id="frGo">🖼️ Frame &amp; enter · ${free ? 'free' : `${FRAME_COINS} coins`}</button>
    <p class="g2-foot">${free ? 'Your first frame is free.' : `You have ${Math.floor(S.gems || 0)} coins.`} Framed photos can race again free.</p>
    <div style="text-align:center"><button class="link g2-link" id="frNo">Not now</button></div></div>`);
  $('#frNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
  $('#frGo').onclick = () => { const nm = ($('#frName').value || '').trim(); if (!nm) { toast('Give your photo a name first'); $('#frName').focus(); return; }
    if (inPlay() >= SLOT_BASE && !passes()) { popClose(); toast(`All ${SLOT_BASE} spots are in play. ${y ? 'Judge' : 'Vote'} ${passNext()} more to earn an extra spot.`); return; }
    if (!free && (S.gems || 0) < FRAME_COINS) { popClose(); toast(`Framing costs ${FRAME_COINS} coins · ${y ? 'judge' : 'vote'} to earn ${FRAME_COINS - Math.floor(S.gems || 0)} more`); return; }
    if (free) S.frameUsed = 1; else { S.gems -= FRAME_COINS; paintGems(); }
    p.title = nm; p.framed = Date.now(); S.ffDone = 1; save(); popClose(); showEnter(p.id, 1); if (then) then(); }; }
function photoRec(p) { const r = rcRec(p.id), f = r.f || [], fin = f.filter(z => z.k === 'r'), best = fin.length ? Math.min(...fin.map(z => z.pl)) : 0;
  return { races: f.filter(z => z.k === 'h').length, finals: fin.length, best, won: earnOf(p.id), form: f.map(z => z.pl) }; }
function galFinalsHTML() { const cur = ppSlot(), L = SHOW_ROT.map(x => ({ k: x.k, sl: finFor(x.k) })).sort((a, b) => a.sl - b.sl);
  return `<p class="gl-h">Upcoming Finals</p><div class="gl-fin">${L.map(x => `<button data-glk="${x.k}"><span class="gl-ic">${SHOW_IC[x.k] || '🎀'}</span><b>${esc(showName(x.k))}</b><small>${raceName(x.sl)} Final</small><em>${ppPool(ppGame(x.sl).players)} pool</em></button>`).join('')}</div>`; }
function renderMyShow() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const y = isYoungW(), cur = ppSlot();
  const P = (S.photos || []).slice(), F = P.filter(p => p.framed).sort((a, b) => b.framed - a.framed), U = P.filter(p => !p.framed && photoShow(p));
  const tot = (S.earn || []).reduce((a, e) => a + e.amt, 0), finals = F.reduce((a, p) => a + photoRec(p).finals, 0), races = F.reduce((a, p) => a + photoRec(p).races, 0);
  const status = p => { const r = rcRec(p.id); if (r.st === 'q') return `<span class="gl-st live">🎀 Finalist · ${raceName(r.sl)} Final</span><button class="btn gl-act" data-glw="${r.sl}">${r.sl === cur ? '🔴 Watch' : 'Finalists'}</button>`;
    if (r.st === 'heats') return `<span class="gl-st">⚖️ In the qualifiers · ${Math.max(0, HEAT_RUNS - (r.runs || 0))} tries left</span>`;
    return `<span class="gl-st">Resting · ready to race again</span><button class="btn gl-act" data-glen="${p.id}">Enter again · free</button>`; };
  const frame = p => { const R = photoRec(p), SH = SHOWS.find(z => z.k === photoShow(p));
    return `<div class="gl-card"><div class="gl-frame"><img src="${p.src}" alt=""></div><div class="gl-plate"><b>${esc(p.title || rcName(p))}</b><small>${SH ? esc(SH.n) : ''} · framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small></div>
      <div class="gl-rec"><div><b>${money(R.won)}</b><small>prize money</small></div><div><b>${R.finals}</b><small>Final${R.finals === 1 ? '' : 's'}</small></div><div><b>${R.best ? ppOrd(R.best) : '–'}</b><small>best finish</small></div><div><b>${R.races}</b><small>qualifiers</small></div></div>
      ${R.form.length ? `<p class="gl-form">Form <span class="rf">${formHTML(R.form)}</span></p>` : ''}<div class="gl-row">${status(p)}</div></div>`; };
  g.innerHTML = `<div class="ms gl"><h1 class="ms-h">🖼️ Gallery</h1><p class="ms-sub">Your framed photos and their race record</p>
    ${galFinalsHTML()}
    <button class="btn block gl-add" id="glAdd">📷 Add a photo to frame · ${frameFree() ? 'first frame free' : `${FRAME_COINS} coins`}</button>
    <div class="gl-sum"><div><b>${money(tot)}</b><small>prize money</small></div><div><b>${F.length}</b><small>framed</small></div><div><b>${finals}</b><small>Finals</small></div><div><b>${races}</b><small>qualifiers</small></div></div>
    <p class="gl-h">Your framed photos</p>${F.length ? `<div class="gl-wall">${F.map(frame).join('')}</div>` : '<p class="ms-none">No framed photos yet. Add a photo, name it and frame it to enter the qualifiers.</p>'}
    ${U.length ? `<p class="gl-h">Ready to frame</p><div class="gl-un">${U.map(p => `<div><img src="${p.src}" alt=""><b>${esc(p.title || rcName(p))}</b><button class="btn gl-act" data-glfr="${p.id}">🖼️ Frame · ${frameFree() ? 'free' : FRAME_COINS}</button></div>`).join('')}</div>` : ''}
    <div class="ms-earn"><div class="ms-eh"><b>💰 Earnings</b><span>${money(tot)} total · ${money(earnWeek())} this week</span></div>${(S.earn || []).length ? (S.earn || []).slice(-3).reverse().map(earnRowHTML).join('') : '<p class="er-none">Prize money from your framed photos shows here.</p>'}<button class="link ms-all" id="msEarn">See all earnings ›</button></div>
    <p class="ms-r">Frame a photo for ${FRAME_COINS} coins (your first is free) to enter its category’s qualifiers. The top 2 in each qualifier go through to the hourly Final, where finalists’ creators share 10% of the prize pool: 1st 4% · 2nd 2.5% · 3rd 1.5% · 4th–6th share 2%. Framed photos can race again free.</p></div>`;
  g.querySelectorAll('[data-glk]').forEach(b => b.onclick = () => { window.__preCat = showHint(b.dataset.glk).cats[0]; pickPhoto(true); });
  g.querySelectorAll('[data-glen]').forEach(b => b.onclick = () => showEnter(b.dataset.glen));
  g.querySelectorAll('[data-glfr]').forEach(b => b.onclick = () => frameOpen((S.photos || []).find(x => x.id === b.dataset.glfr)));
  g.querySelectorAll('[data-glw]').forEach(b => b.onclick = () => +b.dataset.glw === cur ? ppOpen() : raceCard());
  $('#glAdd').onclick = () => finPick(); }
function fcNotify() {""", 1)
# old renderMyShow out of the way (the new one is defined later and wins)
RA("function renderMyShow() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const y = isYoungW(), P = (S.photos || []).slice().sort",
   "function renderMyShowOld() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const y = isYoungW(), P = (S.photos || []).slice().sort")
# entering needs a frame (no 70+)
RA("function showEnter(id) {", "function showEnter(id, fr) {")
RA("  const ff = ffree(); if (p.s.total < SHOW_MIN && !ff) { S.cur = p.id; save(); go('studio'); renderStudio(); toast(`${y ? 'Enhance' : 'Touch up'} to ${SHOW_MIN}+ to enter the qualifiers`); return; }",
   "  if (!p.framed) { frameOpen(p); return; } if (['heats', 'q'].includes(rcRec(id).st)) { toast(`${rcName(p)} is already racing`); return; }")
# new-player first photo: frame it free
RA("title: 'Improve it to enter the qualifiers', text: `${S.user && S.user.guest ? `Create your free account and get <b>${FF_GIFT} coins</b> to improve <b>${esc(p.title)}</b>.` : `Use your coins to ${y ? 'enhance' : 'touch up'} <b>${esc(p.title)}</b>.`} Once it improves it enters the",
   "title: 'Frame it to enter the qualifiers', text: `Your first frame is free. Frame <b>${esc(p.title)}</b> and it enters the")
RA("cta: `✨ ${y ? 'Enhance' : 'Improve'} my photo`, onCta: () => { closeFlow(); S.cur = p.id; save(); go('studio'); renderStudio(); }, later: 'Later' }); return; } }",
   "cta: '🖼️ Frame it · free', onCta: () => { closeFlow(); frameOpen(p); }, later: 'Later' }); return; } }")
RA("if (S.ffPid && !S.ffDone) {", "if (false) {")
RA("if (p && p.id !== S.ffPid && p.s.total >= SHOW_MIN", "if (false && p && p.id !== S.ffPid && p.s.total >= SHOW_MIN")
RA("if (p.id === S.ffPid && !S.ffDone && photoShow(p)) return { cls: 'low', ic: '✨', t: 'Touch up to enter the qualifiers',",
   "if (!p.framed && photoShow(p)) return { cls: 'low', ic: '🖼️', t: 'Frame it to enter the qualifiers', s: `${frameFree() ? 'First frame free' : `${FRAME_COINS} coins`}` };\n  if (false) return { cls: 'low', ic: '✨', t: 'Touch up to enter the qualifiers',")
# coins menu: frame instead of touch up
RA("  if (up && up.s.total < CFG.QUALIFY) {", "  { const uf = S.photos.find(p => !p.framed && photoShow(p)); if (uf) I.push({ ic: '🖼️', t: 'Frame a photo', d: `Name and frame <b>${esc(uf.title || rcName(uf))}</b> to enter the qualifiers.`, cost: frameFree() ? 0 : FRAME_COINS, src: uf.src, go: () => { closeSheet(); frameOpen(uf); } }); }\n  if (false && up && up.s.total < CFG.QUALIFY) {")
# copy
RA("Improve quality &amp; qualify", "Name, frame &amp; qualify")
RA("Enhance with coins", "Frame it for 200 coins")
RA("Improve your photo and it enters that Final’s <b>qualifiers</b>: the top 2 in each go through.", "Your first frame is free: frame your photo and it enters that Final’s <b>qualifiers</b>.")
RA("Photos at 70+ enter its qualifiers free; the top 2 go through to the Final.", "Frame your photo for 200 coins and it enters that Final’s qualifiers; the top 2 go through.")
RA("We’ll give you 150 coins to improve your first photo.", "Your first frame is free.")
# hide Touch-ups tab
s = s.replace('</style>', """html body #segStudio{display:none!important}
html body .ms.gl{background:transparent!important;height:auto!important;min-height:0!important;box-shadow:none!important}html body .gl-fin button{background:#E3EAF5!important;border-radius:14px!important}
.gl-h{text-align:left;font:800 1.15rem Fraunces,Georgia,serif;color:#1E3A6E;margin:14px 0 6px}.gl-fin{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.gl-fin button{border:0;border-radius:14px;background:#E3EAF5;padding:10px 4px;font:inherit;color:#1E3A6E;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px}
.gl-fin .gl-ic{font-size:1.5rem}.gl-fin b{font-size:.84rem;line-height:1.15}.gl-fin small{font-size:.76rem}.gl-fin em{font-style:normal;font-weight:900;color:#2F6B3F;font-size:.86rem}
html body .gl .btn.gl-add{background:#1E3A6E!important;color:#fff!important;margin:12px 0 4px}
.gl-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0 2px}.gl-sum div{background:#F3EDE2;border-radius:12px;padding:8px 2px;text-align:center}.gl-sum b{display:block;font:800 1.05rem Fraunces,Georgia,serif;color:#1E3A6E}.gl-sum small{font-size:.7rem}
.gl-wall{display:flex;flex-direction:column;gap:16px}.gl-card{background:#FBF6EE;border-radius:18px;padding:14px;box-shadow:0 4px 14px -8px rgba(60,40,20,.4);text-align:center}
.gl-frame{padding:12px;background:linear-gradient(135deg,#E8C46A,#B8862E 45%,#F3D98B 55%,#A9771F);border-radius:6px;box-shadow:inset 0 0 0 3px #8A5E16,0 6px 14px -6px rgba(0,0,0,.45);margin:0 auto;max-width:250px}
.gl-frame img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;box-shadow:inset 0 0 0 1px rgba(0,0,0,.2),0 0 0 6px #F6EEDC}
.gl-plate{display:inline-block;margin:10px auto 8px;padding:6px 18px;border-radius:4px;background:linear-gradient(#E9CF86,#C9A24E);box-shadow:inset 0 0 0 1px #9A7224;color:#3B2A12}.gl-plate b{display:block;font:800 1.1rem Fraunces,Georgia,serif}.gl-plate small{font-size:.74rem}
.gl-rec{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:4px 0 6px}.gl-rec div{background:#fff;border-radius:10px;padding:6px 2px;box-shadow:inset 0 0 0 1px #EADCC6}.gl-rec b{display:block;font:800 1rem Fraunces,Georgia,serif;color:#1E3A6E}.gl-rec div:first-child b{color:#2F6B3F}.gl-rec small{font-size:.68rem}
.gl-form{margin:2px 0 6px;font-size:.84rem}.gl-row{display:flex;align-items:center;justify-content:space-between;gap:8px;text-align:left}.gl-st{font-size:.86rem;color:#1E3A6E;font-weight:700}.gl-st.live{color:#C8102E}
html body .gl .btn.gl-act{flex:none;width:auto!important;padding:8px 14px!important;font-size:.86rem!important;background:#1E3A6E!important;color:#fff!important;margin:0!important}
.gl-un{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.gl-un div{background:#FBF6EE;border-radius:14px;padding:8px;display:flex;flex-direction:column;gap:6px;align-items:stretch;text-align:center}.gl-un img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px}.gl-un b{font-size:.86rem}
.fr3{text-align:center}.fr3-frame{padding:12px;background:linear-gradient(135deg,#E8C46A,#B8862E 45%,#F3D98B 55%,#A9771F);border-radius:6px;box-shadow:inset 0 0 0 3px #8A5E16;margin:8px auto 10px;max-width:220px}.fr3-frame img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;box-shadow:0 0 0 6px #F6EEDC}
.fr3-name{width:100%;box-sizing:border-box;text-align:center;font:800 1.15rem Fraunces,Georgia,serif;padding:10px;border-radius:12px;border:1.5px solid #C9D6EA;background:#fff;color:#1E3A6E;margin:0 0 8px}.fr3-s{font-size:.9rem;margin:0 0 10px}
html body .fr3 .btn.fr3-go{background:#1E3A6E!important;color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v59 ok')
