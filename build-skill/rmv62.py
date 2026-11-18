# Real Money build, step 65 (after rmv61.py): Gallery from the user's mock-up.
#  "My gallery" hero (three tilted photos, "Turn your photos into cash prizes", Enter your first photo, first-frame pill),
#  Upcoming Finals rows (thumb, category, time, creators' share = 10% "from $X total pool"), "How your photo wins" 3 steps,
#  "One frame. Enter again free." callout, "How creator prizes are shared" fold, Your photos (framed wall / ready to frame / empty card),
#  green Photo earnings box, closing navy button.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
def I(p, w=26): return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
CAM = I('<path d="M20 12v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2.5L9 5h5"/><circle cx="11.5" cy="13" r="3.2"/><path d="M19 3v5M16.5 5.5h5"/>')
CAM2 = I('<path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.4"/>')
SCALE = I('<path d="M12 4v16M7 20h10M5 7h14M5 7l-2.5 6a2.5 2.5 0 0 0 5 0L5 7zm14 0l-2.5 6a2.5 2.5 0 0 0 5 0L19 7z"/>')
COINS = I('<ellipse cx="12" cy="6" rx="6" ry="2.4"/><path d="M6 6v4c0 1.3 2.7 2.4 6 2.4s6-1.1 6-2.4V6M6 10v4c0 1.3 2.7 2.4 6 2.4s6-1.1 6-2.4v-4M6 14v4c0 1.3 2.7 2.4 6 2.4s6-1.1 6-2.4v-4"/>')
LOOP = I('<path d="M20 11a8 8 0 0 0-14-5l-2 2M4 4v4h4M4 13a8 8 0 0 0 14 5l2-2M20 20v-4h-4"/>', 36)
ADD = I('<rect x="3" y="4" width="15" height="13" rx="2"/><circle cx="13" cy="8.5" r="1.4"/><path d="M4 15l4-4 4 4"/><circle cx="18" cy="18" r="4" fill="#C9962E" stroke="#C9962E"/><path d="M18 16v4M16 18h4" stroke="#fff"/>', 40)
CASH = '<i class="g4-cash"></i>'
RA("function renderMyShow() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const y = isYoungW(), cur = ppSlot();",
   "function renderMyShow59() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const y = isYoungW(), cur = ppSlot();")
s = s.replace("function fcNotify() {", r"""function renderMyShow() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'Gallery'; const cur = ppSlot(), ff = frameFree();
  const P = (S.photos || []).slice(), F = P.filter(p => p.framed).sort((a, b) => b.framed - a.framed), U = P.filter(p => !p.framed && photoShow(p)), first = !F.length;
  const tot = (S.earn || []).reduce((a, e) => a + e.amt, 0);
  const L = SHOW_ROT.map(x => { const sl = finFor(x.k), G = ppGame(sl), pool = G.players * RACE_AVG; return { k: x.k, sl, src: (G.ph[0] || {}).src, pool }; }).sort((a, b) => a.sl - b.sl);
  const cta = first ? 'Enter your first photo' : 'Enter a photo';
  const status = p => { const r = rcRec(p.id); if (r.st === 'q') return `<span class="gl-st live">🎀 Finalist · ${raceName(r.sl)} Final</span><button class="btn gl-act" data-glw="${r.sl}">${r.sl === cur ? '🔴 Watch' : 'Finalists'}</button>`;
    if (r.st === 'heats') return `<span class="gl-st">⚖️ In the qualifiers · ${Math.max(0, HEAT_RUNS - (r.runs || 0))} tries left</span>`;
    return `<span class="gl-st">Resting · ready to race again</span><button class="btn gl-act" data-glen="${p.id}">Enter again · free</button>`; };
  const frame = p => { const R = photoRec(p), SH = SHOWS.find(z => z.k === photoShow(p));
    return `<div class="gl-card"><div class="gl-frame"><img src="${p.src}" alt=""></div><div class="gl-plate"><b>${esc(p.title || rcName(p))}</b><small>${SH ? esc(SH.n) : ''} · framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small></div>
      <div class="gl-rec"><div><b>${money(R.won)}</b><small>prize money</small></div><div><b>${R.finals}</b><small>Final${R.finals === 1 ? '' : 's'}</small></div><div><b>${R.best ? ppOrd(R.best) : '–'}</b><small>best finish</small></div><div><b>${R.races}</b><small>qualifiers</small></div></div>
      ${R.form.length ? `<p class="gl-form">Form <span class="rf">${formHTML(R.form)}</span></p>` : ''}<div class="gl-row">${status(p)}</div></div>`; };
  g.innerHTML = `<div class="ms gl g4"><h1 class="g4-h"><span class="g4-hi">🖼️</span> My gallery</h1><p class="g4-sub">Your photos. Your prize record.</p>
    <div class="g4-hero"><div class="g4-fan">${L.slice(0, 3).map(x => `<img src="${x.src}" alt="">`).join('')}</div><h2>Turn your photos into cash prizes</h2><p>Reach a Final and get paid.<br>Every finalist’s creator wins cash.</p>
      <button class="btn block g4-go" data-g4go>""" + CAM + r""" ${cta}</button><span class="g4-pill">${ff ? 'First frame FREE · Then 200 coins per photo' : `${FRAME_COINS} coins per photo`}</span><p class="g4-it">Frame once. Enter again free.</p></div>
    <h2 class="g4-s">Upcoming Finals</h2><p class="g4-ss">Cash shared by photo creators.</p>
    <div class="g4-fin">${L.map(x => `<button data-glk="${x.k}"><img src="${x.src}" alt=""><span><b>${esc(showName(x.k))}</b><small>${raceName(x.sl)} Final</small></span><span class="g4-amt"><b>${money(x.pool * .1)}</b><small>from $${Math.round(x.pool)} total pool</small></span></button>`).join('')}</div>
    <h2 class="g4-s">How your photo wins</h2><div class="g4-how">
      <div><i>1</i><span class="g4-ic">""" + CAM2 + r"""</span><p><b>Add your photo</b>Choose a category and frame it.</p></div>
      <div><i>2</i><span class="g4-ic">""" + SCALE + r"""</span><p><b>Reach the Final</b>Finish in the top 2 of a qualifier.</p></div>
      <div><i>3</i><span class="g4-ic">""" + COINS + r"""</span><p><b>Win real cash</b>All 6 finalists’ creators share 10% of the total prize pool.</p></div></div>
    <div class="g4-one">""" + LOOP + r"""<p><b>One frame. Enter again free.</b>${ff ? 'Your first frame is free. Additional photos cost' : 'Each new photo costs'} ${FRAME_COINS} coins to frame. Framed photos can enter again free.</p></div>
    <details class="g4-how2"><summary>How creator prizes are shared</summary><p>Every Final’s 6 finalists’ creators share 10% of the prize pool: <b>1st 4%</b> · <b>2nd 2.5%</b> · <b>3rd 1.5%</b> · <b>4th–6th share 2%</b>. Your photo doesn’t have to finish first to get paid.</p></details>
    <h2 class="g4-s">Your photos</h2>
    ${F.length ? `<div class="gl-wall">${F.map(frame).join('')}</div>` : ''}
    ${U.length ? `<p class="gl-h">Ready to frame</p><div class="gl-un">${U.map(p => `<div><img src="${p.src}" alt=""><b>${esc(p.title || rcName(p))}</b><button class="btn gl-act" data-glfr="${p.id}">🖼️ Frame · ${ff ? 'free' : FRAME_COINS}</button></div>`).join('')}</div>` : ''}
    ${!F.length && !U.length ? `<button class="g4-empty" data-g4go>""" + ADD + r"""<p><b>Your first photo starts here</b>Add a photo to begin your gallery.</p></button>` : ''}
    <div class="g4-earn"><p class="g4-eh">""" + CASH + r""" Photo earnings</p><div class="g4-er"><div><b>${money(tot)}</b><small>Total earned</small></div><span>${money(earnWeek())} this week</span></div>
      ${(S.earn || []).length ? (S.earn || []).slice(-3).reverse().map(earnRowHTML).join('') + '<button class="link ms-all" id="msEarn">See all earnings ›</button>' : '<p class="g4-et">Track your photo prizes here.</p>'}</div>
    <button class="btn block g4-go" data-g4go>""" + CAM + r""" ${cta}</button>${ff ? '<p class="g4-it">Your first frame is free.</p>' : ''}</div>`;
  g.querySelectorAll('[data-glk]').forEach(b => b.onclick = () => { window.__preCat = showHint(b.dataset.glk).cats[0]; pickPhoto(true); });
  g.querySelectorAll('[data-glen]').forEach(b => b.onclick = () => showEnter(b.dataset.glen));
  g.querySelectorAll('[data-glfr]').forEach(b => b.onclick = () => frameOpen((S.photos || []).find(x => x.id === b.dataset.glfr)));
  g.querySelectorAll('[data-glw]').forEach(b => b.onclick = () => +b.dataset.glw === cur ? ppOpen() : raceCard());
  g.querySelectorAll('[data-g4go]').forEach(b => b.onclick = () => finPick()); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .g4{padding:4px 2px 20px}html body .g4 .g4-h{display:flex;align-items:center;gap:10px;font:800 2rem/1.1 Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:6px 0 2px;text-align:left}.g4-hi{font-size:2.1rem}
.g4-sub{margin:0 0 14px;text-align:left;font-size:1rem}
.g4-hero{background:#FBF4E6;border-radius:20px;box-shadow:inset 0 0 0 1.5px #E2C27A;padding:18px 14px 14px;text-align:center}
.g4-fan{display:flex;justify-content:center;margin:4px 0 14px}.g4-fan img{width:31%;aspect-ratio:1;object-fit:cover;border:5px solid #fff;border-radius:3px;box-shadow:0 6px 14px -6px rgba(0,0,0,.4)}
.g4-fan img:nth-child(1){transform:rotate(-8deg) translateY(10px);margin-right:-12px}.g4-fan img:nth-child(2){position:relative;z-index:1;transform:translateY(-4px)}.g4-fan img:nth-child(3){transform:rotate(8deg) translateY(10px);margin-left:-12px}
html body .g4 .g4-hero h2{font:800 1.85rem/1.05 Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:0 0 8px}.g4-hero>p{margin:0 0 14px;font-size:1rem}
html body .g4 .btn.g4-go{display:flex;align-items:center;justify-content:center;gap:10px;background:#1E3A6E!important;color:#fff!important;font-size:1.08rem!important}
.g4-pill{display:inline-block;margin:10px 0 4px;background:#F6E2AE;color:#14213D;font-weight:800;font-size:.84rem;border-radius:999px;padding:5px 16px}.g4-it{margin:4px 0 0;font-style:italic;font-size:.9rem;text-align:center}
html body .g4 .g4-s{font:800 1.5rem/1.1 Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:20px 0 4px;text-align:left}.g4-ss{margin:0 0 8px;text-align:left}
.g4-fin{display:flex;flex-direction:column;gap:8px}html body .g4-fin button{display:flex;align-items:center;gap:12px;background:#FBF6EE!important;border:0;border-radius:14px!important;box-shadow:inset 0 0 0 1.5px #EADCC6;padding:7px 12px 7px 7px;font:inherit;color:#14213D;cursor:pointer;text-align:left}
.g4-fin img{width:62px;height:52px;object-fit:cover;border-radius:9px;flex:none}.g4-fin span{display:flex;flex-direction:column;min-width:0}.g4-fin span b{font-size:1rem}.g4-fin span small{font-size:.86rem}
.g4-fin .g4-amt{margin-left:auto;text-align:right;align-items:flex-end}html body .g4-fin .g4-amt b{font:900 1.35rem/1 Fraunces,Georgia,serif;color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}.g4-fin .g4-amt small{font-size:.76rem;white-space:nowrap}
.g4-how>div{display:flex;align-items:center;gap:12px;padding:10px 0;text-align:left}.g4-how>div+div{border-top:1px solid #E2D3BC}.g4-how i{flex:none;width:28px;height:28px;border-radius:50%;background:#C9962E;color:#fff;font-style:normal;font-weight:900;display:grid;place-items:center}
.g4-ic{flex:none;width:50px;height:46px;border-radius:12px;box-shadow:inset 0 0 0 1.5px #C9B48E;display:grid;place-items:center;color:#14213D}.g4-how p{margin:0;font-size:.9rem}.g4-how b{display:block;font:800 1.2rem Fraunces,Georgia,serif;color:#14213D}
.g4-one{display:flex;gap:12px;align-items:center;background:#FFF6DF;border-radius:16px;box-shadow:inset 0 0 0 1.5px #E2B54E;padding:12px;margin:10px 0;text-align:left;color:#B8862E}.g4-one svg{flex:none}.g4-one p{margin:0;font-size:.86rem;color:#2B2320}.g4-one b{display:block;font:800 1.15rem Fraunces,Georgia,serif;color:#14213D}
.g4-how2{border-radius:14px;box-shadow:inset 0 0 0 1.5px #D9C29A;padding:10px 14px;text-align:left}.g4-how2 summary{font:800 1.05rem Fraunces,Georgia,serif;color:#14213D;cursor:pointer}.g4-how2 p{margin:8px 0 2px;font-size:.9rem}
html body .g4 .g4-empty{display:flex;align-items:center;gap:14px;width:100%;background:#FBF6EE;border:0;border-radius:16px;box-shadow:inset 0 0 0 1.5px #EADCC6;padding:16px;font:inherit;color:#14213D;text-align:left;cursor:pointer}.g4-empty svg{flex:none}.g4-empty p{margin:0;padding-left:14px;border-left:1.5px solid #E2D3BC;font-size:.92rem}.g4-empty b{display:block;font:800 1.15rem Fraunces,Georgia,serif}
.g4-earn{background:#F1F6EC;border-radius:16px;box-shadow:inset 0 0 0 1.5px #3E7A4E;padding:12px 16px;margin:14px 0;text-align:left}.g4-eh{display:flex;align-items:center;gap:10px;margin:0;font:800 1.15rem Fraunces,Georgia,serif;color:#14213D}
.g4-cash{display:inline-block;width:26px;height:16px;border-radius:3px;background:#3E9A55;box-shadow:inset 0 0 0 3px #57B86D}.g4-er{display:flex;align-items:center;margin:4px 0 8px}.g4-er>div{flex:1;border-right:1.5px solid #CFE0C8}.g4-er span{flex:1;text-align:center}
html body .g4 .g4-er b{display:block;font:900 2rem/1.1 Fraunces,Georgia,serif;color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}.g4-et{margin:0;padding-top:8px;border-top:1px solid #CFE0C8}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v62 ok')
