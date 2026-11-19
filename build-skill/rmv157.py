# Real Money build, step 160 (after rmv156.py): My Photos rebuilt as photo hero cards (the owner's mock-up, improved).
#  - Each photo in play gets a hero card: big framed photo with its rosette pinned on the frame, serif title,
#    category between gold rules, a status box (icon | headline | detail) and ONE main button for the next step:
#      duel live → "🔴 Watch the duel"; finalist → "🥊 Duel · $2" (winner takes $3.40); qualifying → wins bar + "Watch it live";
#      out → "Enter another photo". Under it, "Last duel" with the score, rival and cash won (or "rosette kept").
#  - Below: entry card (tickets / rounds to go), other photos as compact rows, earnings in plain words.
#  - Removed old-race leftovers: 10% creator pool, "tries left", upcoming 6-photo Finals, Form, stats strip.
#  - Round-end card: "Race someone with this eye · $1" (old Match Race) replaced by "🥊 Duel <photo> · $2" when you
#    have a finalist, otherwise nothing.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""<button class="btn block db-go ${first || !isCash() ? '' : 'cashb'}" id="vrRace">⚔️ ${first ? 'Your first Match Race · free' : isCash() ? 'Race someone with this eye · $1' : 'Race someone with this eye · 25 🟡'}</button>""",
   """${(fp => fp && !duLive() ? `<button class="btn block db-go cashb" id="vrDuel" data-qfr="${fp.id}">🥊 Duel ${esc(rcName(fp))} · $2</button>` : '')((S.photos || []).find(x => x.fin))}""")
RA("$('#vrRace').onclick = () => {", "if ($('#vrRace')) $('#vrRace').onclick = () => {")
RA("try { earnAdd({ kind: 'f', pid: p.id, t: p.title, amt: DU_PRIZE, place: 1 }); } catch (e) {}", "try { earnAdd({ kind: 'du', pid: p.id, t: p.title, amt: DU_PRIZE, o: u.o.t, sc: `${u.a}–${u.b}` }); } catch (e) {}")
s = s.replace("function fcNotify() {", r"""function mpState(p) { const q = p.ql;
  if (p.du && !p.du.done) return 0; if (p.fin) return 1; if (q && !q.done) return 2; if (q && q.done === 'x' && Date.now() - (q.at || 0) < 864e5) return 3; return 4; }
function mpRz(p) { const R = p.dr; if (R && R.w) return rosette(0); if (p.fin || (p.ql && p.ql.done === 'q') || R) return rosette('f'); return ''; }
function mpHero(p) { const q = p.ql || { w: 0, l: 0 }, R = p.dr, SH = SHOWS.find(z => z.k === photoShow(p)), st = mpState(p), u = p.du; let ic, h, sm, btn, extra = '';
  if (st === 0) { const t = u.a + u.b; ic = '🥊'; h = `Duel live · ${u.a}–${u.b}`; sm = `${u.a > u.b ? 'You lead' : u.a < u.b ? 'You trail' : 'All square'} · ${DU_V - t} vote${DU_V - t === 1 ? '' : 's'} to go · winner takes ${money(DU_PRIZE)}`; btn = `<button class="btn block mp-go" data-mpv>🔴 Watch the duel</button>`; }
  else if (st === 1) { ic = '🏆'; h = R && R.st ? `${R.st} duel${R.st > 1 ? 's' : ''} won in a row 🔥` : 'Your photo made the Final'; sm = `One-on-one duel · you both pay $2 · winner takes <b>${money(DU_PRIZE)}</b>`; btn = `<button class="btn block mp-go cash" data-qfr="${p.id}">🥊 Duel · $2</button>`; }
  else if (st === 2) { ic = '🎀'; h = `In its qualifier · ${q.w}–${q.l}`; sm = `<b>${QF_WIN - q.w} more win${QF_WIN - q.w === 1 ? '' : 's'}</b> to the Final · ${QF_N - QF_WIN + 1 - q.l} loss${QF_N - QF_WIN + 1 - q.l === 1 ? '' : 'es'} to spare`; extra = `<div class="qv-bar mp-bar"><i style="width:${Math.min(100, q.w / QF_WIN * 100)}%"></i><u>🏁</u></div>`; btn = `<button class="btn block mp-go" data-mpv>⚖️ Watch it live while you vote</button>`; }
  else if (st === 3) { ic = '📷'; h = `Out at ${q.w}–${q.l}`; sm = `${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'} short. Bright, close-up shots tend to win.`; btn = `<button class="btn block mp-go" data-mpe>📷 Enter another photo</button>`; }
  else { ic = R ? '🥊' : '🖼️'; h = R ? `Duel record ${R.w}–${R.l}` : 'Not in play'; sm = R ? (R.cash ? `${money(R.cash)} won with this photo` : 'Its rosettes stay on the frame') : 'Enter a photo to start a qualifier'; btn = `<button class="btn block mp-go" data-mpe>📷 Enter a photo</button>`; }
  const L = R && R.last, z = mpRz(p);
  return `<div class="mp-card"><div class="mp-pic"><div class="mp-frame"><img src="${p.src}" alt=""></div>${z ? `<i class="mp-rz">${z}</i>` : ''}${st === 0 ? '<span class="mp-live">● LIVE</span>' : ''}</div>
    <h2 class="mp-t">${esc(rcName(p))}</h2><p class="mp-c"><span>${SH ? esc(SH.n) : 'Photo'}</span></p>
    <div class="mp-st"><span class="mp-ic">${ic}</span><div><b>${h}</b><small>${sm}</small>${extra}</div></div>${btn}
    ${L ? `<div class="mp-last"><span class="mp-lk">Last duel</span><div class="mp-lr"><img src="${L.src}" alt=""><span><b>${L.win ? 'Won' : 'Lost'} ${L.a}–${L.b}</b><small>vs “${esc(L.t)}”</small></span><em class="${L.win ? 'w' : ''}">${L.win ? `${money(DU_PRIZE)} won` : 'rosette kept'}</em></div></div>` : ''}</div>`; }
function mpRow(p) { const st = mpState(p), q = p.ql || { w: 0, l: 0 }, R = p.dr;
  const t = st === 0 ? '🥊 Duel live' : st === 1 ? '🏆 Finalist · ready to duel' : st === 2 ? `🎀 Qualifier ${q.w}–${q.l}` : st === 3 ? `Out at ${q.w}–${q.l}` : R ? `🥊 Duels ${R.w}–${R.l}${R.cash ? ` · ${money(R.cash)} won` : ''}` : 'Not in play';
  return `<div class="mp-row"><img src="${p.src}" alt=""><span><b>${esc(rcName(p))}</b><small>${t}</small></span>${st === 1 ? `<button class="btn mp-sm cash" data-qfr="${p.id}">Duel · $2</button>` : st <= 2 ? '<button class="btn mp-sm" data-mpv>Watch</button>' : ''}</div>`; }
function renderMyShow() { const g = $('#gallery'); if (!g) return; const P = (S.photos || []), F = P.filter(p => p.framed && !(p.starter && !p.ql)).sort((a, b) => mpState(a) - mpState(b) || (b.ql ? b.ql.at || 0 : 0) - (a.ql ? a.ql.at || 0 : 0) || b.framed - a.framed);
  if (!F.length) return renderMyShowIntro(); $('#ptitle').textContent = 'My Photos';
  const hero = F.filter(p => mpState(p) <= 2).slice(0, 2), H = hero.length ? hero : [F[0]], rest = F.filter(p => !H.includes(p)), U = P.filter(p => !p.framed && photoShow(p));
  const tot = (S.earn || []).reduce((a, e) => a + e.amt, 0), left = 3 - (S.vrq || 0), tk = S.entT || 0, first = !qlReal().length;
  g.innerHTML = `<div class="ms mp"><h1 class="mp-h">My Photos</h1>${H.map(mpHero).join('')}
    <div class="mp-ent"><span class="mp-ic">🎟️</span><div><b>${first || tk ? `${first ? 'Your first entry is free' : `${tk} entry ticket${tk > 1 ? 's' : ''} ready`}` : `Judge ${left} more round${left === 1 ? '' : 's'} to enter another photo`}</b><small>More photos in play, more Finals to win.</small></div>
      <button class="btn mp-sm" data-mpe>${first || tk ? '📷 Enter' : '⚖️ Judge'}</button></div>
    ${rest.length ? `<h3 class="mp-s">More of your photos</h3><div class="mp-list">${rest.map(mpRow).join('')}</div>` : ''}
    ${U.length ? `<h3 class="mp-s">Ready to enter</h3><div class="mp-list">${U.map(p => `<div class="mp-row"><img src="${p.src}" alt=""><span><b>${esc(rcName(p))}</b><small>Not entered yet</small></span><button class="btn mp-sm" data-mpe>Enter</button></div>`).join('')}</div>` : ''}
    <div class="mp-earn"><div><span class="mp-lk">Photo earnings</span><b>${money(tot)}</b><small>${money(earnWeek())} this week</small></div>
      ${(S.earn || []).slice(-3).reverse().map(e => `<p><span>${e.kind === 'du' ? `🥊 Duel won · ${esc(e.t || 'Your photo')}${e.sc ? ` · ${e.sc}` : ''}` : `🏁 ${esc(e.t || 'Prize')}${e.place ? ` · ${ppOrd(e.place)}` : ''}`}</span><b>+${money(e.amt)}</b></p>`).join('') || '<p class="mp-none">Cash your photos win shows here.</p>'}</div>
    <p class="mp-how">Win 8 of 15 head-to-heads to reach a Final. Finals are one-on-one duels: you both pay $2, the crowd votes, the winner takes $3.40.</p></div>`;
  g.querySelectorAll('[data-mpv]').forEach(b => b.onclick = () => { go('judge'); renderJudge(); });
  g.querySelectorAll('[data-mpe]').forEach(b => b.onclick = () => finPick()); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .mp{padding:4px 2px 24px;text-align:left}.mp-h{margin:4px 4px 12px;font:800 2rem/1.1 Fraunces,Georgia,serif;color:#14213D}
.mp-card{margin:0 0 14px;padding:12px 12px 14px;border-radius:20px;background:#FFFCF6;box-shadow:inset 0 0 0 1.5px #E5C987,0 6px 20px rgba(20,33,61,.08)}
.mp-pic{position:relative}.mp-frame{padding:5px;border-radius:12px;background:linear-gradient(135deg,#F3D98B,#C9963A 45%,#F6E3A6 70%,#B8862E);box-shadow:0 3px 10px rgba(120,80,20,.25)}
.mp-frame img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px}
.mp-rz{position:absolute;top:-10px;right:-6px;width:92px;filter:drop-shadow(0 4px 6px rgba(0,0,0,.3));transform:rotate(8deg)}.mp-rz svg{width:100%;height:auto;display:block}
.mp-live{position:absolute;top:14px;left:14px;font:900 .72rem Nunito,system-ui;letter-spacing:.06em;color:#fff;background:#C0533F;border-radius:999px;padding:3px 9px;animation:qmPulse 1.4s ease-in-out infinite}
.mp-t{margin:12px 0 2px;text-align:center;font:800 1.7rem/1.15 Fraunces,Georgia,serif;color:#14213D}
.mp-c{display:flex;align-items:center;gap:10px;margin:0 0 12px;font:600 .95rem Nunito,system-ui;color:#5B4A3F}.mp-c::before,.mp-c::after{content:'';flex:1;height:1.5px;background:linear-gradient(90deg,transparent,#D9AE4F)}.mp-c::after{background:linear-gradient(90deg,#D9AE4F,transparent)}
.mp-st,.mp-ent{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}
.mp-ic{font-size:1.9rem;line-height:1;padding-right:12px;border-right:1.5px solid #E5C987}.mp-st>div,.mp-ent>div{flex:1;min-width:0}
.mp-st b,.mp-ent b{display:block;font:800 1.08rem/1.25 Fraunces,Georgia,serif;color:#14213D}.mp-st small,.mp-ent small{display:block;margin-top:2px;font:600 .82rem/1.35 Nunito,system-ui;color:#3D4A5C}.mp-st small b{display:inline;font:inherit;font-weight:900;color:#2F6B3F}
.mp-bar{margin-top:7px;height:10px}
html body .mp-go{margin:12px 0 0!important;min-height:52px;border-radius:999px!important;background:linear-gradient(180deg,#22325A,#14213D)!important;color:#fff!important;font:800 1.08rem Nunito,system-ui!important;box-shadow:0 4px 12px rgba(20,33,61,.25)!important}
html body .mp-go.cash,html body .mp-sm.cash{background:linear-gradient(180deg,#3A8050,#2F6B3F)!important}
.mp-last{margin-top:12px;padding:10px 12px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.mp-lk{display:block;font:900 .7rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8A7B6C}
.mp-lr{display:flex;align-items:center;gap:10px;margin-top:6px}.mp-lr img{width:40px;height:40px;border-radius:9px;object-fit:cover}.mp-lr span{flex:1;min-width:0}.mp-lr b{display:block;font:800 1rem Fraunces,Georgia,serif;color:#14213D}.mp-lr small{display:block;font:600 .78rem Nunito,system-ui;color:#5B4A3F;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mp-lr em{font-style:normal;font:900 1.05rem Fraunces,Georgia,serif;color:#8A7B6C;white-space:nowrap}.mp-lr em.w{color:#2F6B3F;font-size:1.25rem}
.mp-ent{margin:0 0 14px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #D9AE4F}
html body .mp-sm{width:auto!important;min-height:0!important;margin:0!important;padding:8px 14px!important;border-radius:999px!important;font:800 .84rem Nunito,system-ui!important;background:#14213D!important;color:#fff!important;box-shadow:none!important;white-space:nowrap}
.mp-s{margin:6px 4px 8px;font:800 1.1rem Fraunces,Georgia,serif;color:#14213D}.mp-list{display:grid;gap:8px;margin-bottom:14px}
.mp-row{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.mp-row img{width:48px;height:48px;border-radius:10px;object-fit:cover}
.mp-row span{flex:1;min-width:0}.mp-row b{display:block;font:800 .95rem Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.mp-row small{display:block;font:600 .78rem Nunito,system-ui;color:#5B4A3F}
.mp-earn{padding:12px 14px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.mp-earn>div{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}.mp-earn>div .mp-lk{width:100%}
.mp-earn>div b{font:800 1.8rem Fraunces,Georgia,serif;color:#2F6B3F}.mp-earn>div small{font:700 .8rem Nunito,system-ui;color:#5B4A3F}
.mp-earn p{display:flex;justify-content:space-between;gap:8px;margin:8px 0 0;padding-top:8px;border-top:1px solid #F0E6D6;font:700 .82rem Nunito,system-ui;color:#3D4A5C}.mp-earn p b{color:#2F6B3F}.mp-earn p.mp-none{border:0;color:#8A7B6C}
.mp-how{margin:12px 6px 0;font:600 .78rem/1.45 Nunito,system-ui;color:#8A7B6C;text-align:center}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v157 ok')
# pass 2: clearer streak headline; smaller entry-card title
s = open(d + 'yofi-real.html').read()
RA("h = R && R.st ? `${R.st} duel${R.st > 1 ? 's' : ''} won in a row 🔥` : 'Your photo made the Final';",
   "h = R && R.st >= 2 ? `${R.st} duels won in a row 🔥` : R && R.st ? 'Duel won! Go again?' : 'Your photo made the Final';")
s = s.replace('</style>', """html body .mp-ent b{font:800 .95rem/1.3 Nunito,system-ui}html body .mp-ent .mp-ic{font-size:1.6rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v157 pass2 ok')
