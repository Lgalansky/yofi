# Real Money build, step 163 (after rmv159.py): the 6-photo race Final is back (owner's call: "it was great").
#  - Finalist → "🏁 Race · $1": lobby fills with 6 finalists, the full-screen race with caller and photo finish,
#    1st $3.50 · 2nd $1.60 · rosettes for the top 3. The $2 duel is retired from the path.
#  - All wording back to the race: landing, entry screen, finalist moment, round-end button, panel, My Photos ("Last Final").
#  - The live pair banner in judging is now "🏁 LIVE FINAL · these two are racing · your vote moves them".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("Win 8 and it reaches a Final: a one-on-one duel for real cash.", "Win 8 and it races in a 6-photo Final for real cash.")
RA("Win 8 and it reaches a Final: a $2 duel, winner takes $3.40.", "Win 8 and it races in a 6-photo Final: 1st $3.50, 2nd $1.60.")
RA("win 8 and it reaches a Final: a $2 duel for cash.", "win 8 and it races in a Final for cash.")
RA("Win 8 of 15 crowd votes and it reaches a cash Final duel.", "Win 8 of 15 crowd votes and it races in a cash Final.")
RA("""${(fp => fp && !duLive() ? `<button class="btn block db-go cashb" id="vrDuel" data-qfr="${fp.id}">🥊 Duel ${esc(rcName(fp))} · $2</button>` : '')((S.photos || []).find(x => x.fin))}""",
   """${(fp => fp ? `<button class="btn block db-go cashb" id="vrDuel" data-qfr="${fp.id}">🏁 Race ${esc(rcName(fp))} in a Final · $1</button>` : '')((S.photos || []).find(x => x.fin))}""")
RA("""<div class="qf-box">🥊 <b>Final duel</b><br>Your photo vs another finalist · $2 each · winner takes <b>$3.40</b><br><small>Decided by the next 15 crowd votes. Watch it live while you judge.</small></div>""",
   """<div class="qf-box">🏁 <b>Race it in a Final</b><br>6 finalists · $1 each · 1st <b>$3.50</b> · 2nd <b>$1.60</b><br><small>The crowd’s votes decide the order. Watch the race live.</small></div>""")
RA("""<button class="btn block db-go cashb" id="qfGo">🥊 Duel · $2</button>""", """<button class="btn block db-go cashb" id="qfGo">🏁 Race ${nm} · $1</button>""")
RA("""if (p.fin || (q.done === 'q' && !R)) info = `🎀 <b>Finalist${R && R.st ? ` · 🔥 ${R.st} win${R.st > 1 ? 's' : ''} in a row` : '!'}</b> <button class="btn db-go cashb ql-btn" data-qfr="${p.id}">🥊 Duel · $2</button>`;""",
   """if (p.fin || (q.done === 'q' && !R && !p.raced)) info = `🎀 <b>Finalist!</b> <button class="btn db-go cashb ql-btn" data-qfr="${p.id}">🏁 Race · $1</button>`;""")
RA("${A.filter(p => p.dr).length} duelled", "${A.filter(p => p.raced).length} raced")
RA("Finals are one-on-one duels: you both pay $2, the crowd votes, the winner takes $3.40.", "Finals are 6-photo races: $1 to enter, the crowd’s votes decide the order, 1st wins $3.50 and 2nd $1.60.")
s = s.replace("function fcNotify() {", r"""function qfStart(p) { needAge(() => { try { popClose(); } catch (e) {} payCash(1, 'A $1 Final entry', () => setTimeout(() => qfLobby(p), 250)); }); }
function vdLine(p) { const q = p.ql; let st = '';
  if (p.fin) st = `🎀 <b>Finalist</b> · ready to race <button class="btn db-go cashb ql-btn" data-qfr="${p.id}">🏁 Race · $1</button>`;
  else if (p.raced) st = `🏁 Raced a Final · ${ppOrd(p.raced.rank)}${p.raced.prize ? ` · won <b>${money(p.raced.prize)}</b>` : ''}`;
  else if (q && q.done === 'x') st = `Qualifier ${q.w}–${q.l} · out this time`;
  else if (q) st = `🎀 Qualifier <b>${q.w}–${q.l}</b> · ${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'} to a Final`;
  return `<p class="vd-l">${st || 'Not entered yet'}${p.starter ? ' · <em>Starter photo</em>' : ''}</p>`; }
function mpState(p) { const q = p.ql; if (p.fin) return 1; if (q && !q.done) return 2; if (q && q.done === 'x' && Date.now() - (q.at || 0) < 864e5) return 3; return 4; }
function mpRz(p) { const r = p.raced; if (r && r.rank <= 3) return rosette(r.rank - 1); if (p.fin || (p.ql && p.ql.done === 'q') || r) return rosette('f'); return ''; }
function mpHero(p) { const q = p.ql || { w: 0, l: 0 }, F = p.raced, SH = SHOWS.find(z => z.k === photoShow(p)), st = mpState(p); let ic, h, sm, btn, extra = '';
  if (st === 1) { ic = '🏆'; h = 'Your photo made the Final'; sm = `Race it against 5 other finalists · $1 · 1st <b>$3.50</b> · 2nd <b>$1.60</b>`; btn = `<button class="btn block mp-go cash" data-qfr="${p.id}">🏁 Race · $1</button>`; }
  else if (st === 2) { ic = '🎀'; h = `In its qualifier · ${q.w}–${q.l}`; sm = `<b>${QF_WIN - q.w} more win${QF_WIN - q.w === 1 ? '' : 's'}</b> to the Final · ${QF_N - QF_WIN + 1 - q.l} loss${QF_N - QF_WIN + 1 - q.l === 1 ? '' : 'es'} to spare`; extra = `<div class="qv-bar mp-bar"><i style="width:${Math.min(100, q.w / QF_WIN * 100)}%"></i><u>🏁</u></div>`; btn = `<button class="btn block mp-go" data-mpv>⚖️ Watch it live while you vote</button>`; }
  else if (st === 3) { ic = '📷'; h = `Out at ${q.w}–${q.l}`; sm = `${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'} short. Bright, close-up shots tend to win.`; btn = `<button class="btn block mp-go" data-mpe>📷 Enter another photo</button>`; }
  else { ic = F ? '🏁' : '🖼️'; h = F ? `Raced its Final · ${ppOrd(F.rank)}` : 'Not in play'; sm = F ? (F.prize ? `${money(F.prize)} won with this photo` : 'Its rosettes stay on the frame') : 'Enter a photo to start a qualifier'; btn = `<button class="btn block mp-go" data-mpe>📷 Enter another photo</button>`; }
  const z = mpRz(p);
  return `<div class="mp-card"><div class="mp-pic"><div class="mp-frame"><img src="${p.src}" alt=""></div>${z ? `<i class="mp-rz">${z}</i>` : ''}</div>
    <h2 class="mp-t">${esc(rcName(p))}</h2><p class="mp-c"><span>${SH ? esc(SH.n) : 'Photo'}</span></p>
    <div class="mp-st"><span class="mp-ic">${ic}</span><div><b>${h}</b><small>${sm}</small>${extra}</div></div>${btn}
    ${F && st !== 4 ? '' : F ? `<div class="mp-last"><span class="mp-lk">Last Final</span><div class="mp-lr"><span class="mp-pl">${['🥇', '🥈', '🥉'][F.rank - 1] || ppOrd(F.rank)}</span><span><b>${ppOrd(F.rank)} place</b><small>6-photo ${SH ? esc(SH.n) : ''} Final</small></span><em class="${F.prize ? 'w' : ''}">${F.prize ? `${money(F.prize)} won` : 'rosette kept'}</em></div></div>` : ''}</div>`; }
function mpRow(p) { const st = mpState(p), q = p.ql || { w: 0, l: 0 }, F = p.raced;
  const t = st === 1 ? '🏆 Finalist · ready to race' : st === 2 ? `🎀 Qualifier ${q.w}–${q.l}` : st === 3 ? `Out at ${q.w}–${q.l}` : F ? `🏁 Final · ${ppOrd(F.rank)}${F.prize ? ` · ${money(F.prize)} won` : ''}` : 'Not in play';
  return `<div class="mp-row"><img src="${p.src}" alt=""><span><b>${esc(rcName(p))}</b><small>${t}</small></span>${st === 1 ? `<button class="btn mp-sm cash" data-qfr="${p.id}">Race · $1</button>` : st === 2 ? '<button class="btn mp-sm" data-mpv>Watch</button>' : ''}</div>`; }
function ldBanner() { const top = document.getElementById('vrTop'), o = document.getElementById('ldB'); if (o) o.remove(); if (!window.__finPair || !top) return; window.__ld = null;
  const g = ppGame(ppSlot());
  top.insertAdjacentHTML('afterend', `<div class="ldb" id="ldB"><p class="ldb-h"><span class="qm-live">● LIVE</span><b>🏁 ${esc(raceName(g.sl))} Final</b><em>1st takes $3.50</em></p>
    <p class="ldb-f" id="ldF">These two are racing in it right now · <b>your vote moves them</b> · <i>simulated</i></p></div>`); }
(() => { const cf = callFx; callFx = function () { const r = cf.apply(this, arguments); try { const f = document.getElementById('ldF'); if (window.__finPair && f) { f.innerHTML = '✓ <b>Your vote counted</b> · it just moved the race'; document.getElementById('ldB').classList.add('done'); } } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.mp-pl{width:40px;text-align:center;font:900 1.6rem/1 Fraunces,Georgia,serif;color:#14213D}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v160 ok')
