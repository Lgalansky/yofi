# Real Money build, step 155 (after rmv151.py): the photo loop — judge → enter → qualify → race for cash.
#  - New players start by entering a photo (landing "Enter your photo"); no Match Race offers in the newbie path.
#  - Qualifier: each entered photo plays 15 head-to-heads judged by the crowd; 8 wins = finalist, 8 losses = out.
#    It advances one matchup each time you vote (and slowly in the background), shown live in a strip under the pair.
#  - Finalist: 🎀 rosette + 50 🟡, then "Race it in a Final · $1". Cash only (no coin Finals).
#  - Final: 6 finalists ($1 each, 15% fee): 1st $3.50, 2nd $1.60, top 3 rosettes. Live race animation + photo finish.
#  - Entries: the first is free; after that judge 3 rounds (6 pairs each) per entry. Starter photos don't count.
#  - Removed from the path: Play Pool, royalties, earnings card, daily contests cards, free-real-game nudge.
#  Simulated: matchup results (by photo strength), other finalists, race outcome. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("S.tut = 9; S.fmPend = 1;", "S.tut = 9;")
RA('<button class="lp-btn" onclick="rmStartVote()">Start playing <span aria-hidden="true">→</span></button>', '<button class="lp-btn" onclick="rmEnterOwn()">📷 Enter your photo <span aria-hidden="true">→</span></button>')
RA('<h2>Start here: vote on photos.</h2><p>Every vote earns coins and sharpens your eye. After 10 votes, your first Match Race is on us.</p>',
   '<h2>Start here: enter your best photo.</h2><p>The crowd judges it in 15 head-to-heads. Win 8 and it races in a Final for real cash. Your first entry is free.</p>')
RA("The top 2 in each qualifier go through, and the finalists’ creators share the Final’s prize.", "Its qualifier is 15 head-to-heads judged by the crowd: win 8 and it races in a Final for cash.")
RA("Enter your photo in today’s contest, free. The crowd decides, prizes in real cash.", "Enter another photo. Win 8 of 15 head-to-heads and it races in a Final.")
RA("setTimeout(() => P.length ? ctOpen(photoShow(P[0]), P[0].id) : finPick(), 200);", "setTimeout(finPick, 200);")
RA("⚖️ Your votes helped decide today’s <b>contests</b> and the next <b>Final</b>", "⚖️ Your votes decided <b>${VR_N} qualifier matchups</b> for other players’ photos")
RA("if (p.vd.pct >= 60) { p.pool = Date.now(); p.plAt = Date.now(); }", "")
RA("🏆 <b>Today’s ${esc(showName(k))} contest</b> · these two are fighting for <b>${ppOrd(pl)} place</b>. Your vote counts.",
   "🎀 <b>${esc(showName(k))} qualifier</b> · one of these needs <b>${1 + pl % 3} more win${pl % 3 ? 's' : ''}</b> to reach a Final. Your vote counts.")
s = s.replace("function fcNotify() {", r"""const QF_N = 15, QF_WIN = 8, QF_PAY = [3.5, 1.6];
try { if (S) { S.frNudged = 1; S.phAsked = 1; } } catch (e) {}
function royAccrue() { return null; }
function ctCardHTML() { return ''; }
const qlReal = () => (S.photos || []).filter(p => p.framed && !p.starter);
function qlStrength(p) { if (!p.vd) { const r = cpRng(ppHash('vd:' + p.id)); p.vd = { pct: p.starter ? 72 : Math.round(52 + r() * 28), beat: 5, at: Date.now() }; } return p.vd.pct; }
function qlStart(p) { qlStrength(p); if (!p.starter && qlReal().filter(x => x !== p).length >= 1) S.entT = Math.max(0, (S.entT || 0) - 1); p.ql = { w: 0, l: 0, at: Date.now() }; p.pool = 0; save(); }
function qlStep(p) { const q = p.ql; if (!q || q.done) return; const r = cpRng(ppHash(p.id + ':' + (q.w + q.l) + ':' + (S.votes || 0) + ':' + Date.now() % 997)), pr = Math.max(.2, Math.min(.82, .5 + (qlStrength(p) - 62) / 60));
  const win = r() < pr, pool = SEED.filter(x => x.src && finCatOf(x) === photoShow(p) && x.src !== p.src), opp = pool[Math.floor(r() * pool.length)] || { title: 'a rival' };
  if (win) q.w++; else q.l++; q.last = { win, t: opp.title }; if (q.w >= QF_WIN) q.done = 'q'; else if (q.l > QF_N - QF_WIN) q.done = 'x'; save(); }
const qlActive = () => (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown));
function qlStripHTML() { const A = qlActive(); if (!A.length) return '<div id="qlS"></div>';
  return `<div class="ql-s" id="qlS">${A.slice(0, 2).map(p => { const q = p.ql, dots = Array.from({ length: QF_N }, (_, i) => `<i class="${i < q.w ? 'w' : i < q.w + q.l ? 'l' : ''}"></i>`).join('');
    return `<div class="ql-r"><img src="${p.src}" alt=""><span><b>${esc(rcName(p))}</b> · qualifier <b>${q.w}–${q.l}</b> · ${q.done === 'q' ? '🎀 finalist!' : q.done === 'x' ? 'out' : `${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'} to a Final`}<span class="ql-d">${dots}</span>${q.last ? `<small class="${q.last.win ? 'w' : 'l'}">${q.last.win ? '✓ beat' : '✕ lost to'} “${esc(q.last.t)}”</small>` : '<small>Judging starts now · judge while you wait</small>'}</span></div>`; }).join('')}</div>`; }
function qlPaint() { const e = document.getElementById('qlS'); if (e) e.outerHTML = qlStripHTML(); }
(() => { const cf = callFx, rj = renderJudge;
  callFx = function () { const r = cf.apply(this, arguments); try { (S.photos || []).filter(p => p.ql && !p.ql.done).forEach(qlStep); qlPaint(); } catch (e) {} return r; };
  renderJudge = function () { const r = rj.apply(this, arguments); try { const jc = document.getElementById('jcard'); if (jc && !document.getElementById('qlS')) jc.insertAdjacentHTML('afterend', qlStripHTML()); } catch (e) {} return r; }; })();
setInterval(() => { try { if (!S || !$('#app').classList.contains('on') || document.querySelector('.qfx')) return; (S.photos || []).filter(p => p.ql && !p.ql.done).forEach(qlStep); qlPaint(); } catch (e) {} }, 20000);
setInterval(() => { try { if (!S || !$('#app').classList.contains('on') || !freeScreen() || !popGap()) return; const p = (S.photos || []).find(x => x.ql && x.ql.done && !x.ql.shown); if (p) qlDone(p); } catch (e) {} }, 1500);
function upDone(p) { qlStart(p); window.__nudgeAt = Date.now();
  popOpen(`<div class="pp"><p class="pp-k">🎀 ${esc(rcName(p))} is in its qualifier</p><h2 class="db-h">15 head-to-heads. Win 8 to reach a Final.</h2>
    <div class="vd-ph"><img src="${p.src}" alt=""></div><p class="db-s">The crowd is judging it now. Watch it play out while you judge other photos${qlReal().length > 1 ? '' : ', and earn your next entry'}.</p>
    <button class="btn block db-go" id="qsJ">⚖️ Judge while you wait</button></div>`);
  $('#qsJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; }
function qlDone(p) { const q = p.ql; q.shown = 1; window.__nudgeAt = Date.now(); const nm = esc(rcName(p));
  if (q.done === 'q') { rzAdd(p, 3); S.gems = (S.gems || 0) + 50; p.fin = 1; save();
    popOpen(`<div class="pp"><p class="pp-k">🎀 Qualifier · ${q.w} wins, ${q.l} losses</p><h2 class="db-h">${nm} is a finalist!</h2><div class="re-ok"><img src="${p.src}" alt=""><i class="re-rz">${rosette('f')}</i></div>
      <p class="re-rzl">🎀 Finalist rosette · +50 🟡</p><div class="qf-box">🏁 <b>Race it in a Final</b><br>6 finalists · $1 each · 1st <b>$3.50</b> · 2nd <b>$1.60</b></div>
      <button class="btn block db-go cashb" id="qfGo">🏁 Race ${nm} · $1</button><div style="text-align:center"><button class="link pc-later" id="qfL">Later</button></div></div>`);
    setTimeout(() => { try { paintGems(); gemExplosion(50, { label: 'Finalist!' }); rvConfetti(document.querySelector('#coach .pp'), 40); } catch (e) {} }, 300);
    $('#qfGo').onclick = () => qfStart(p); $('#qfL').onclick = () => popClose(); }
  else { save(); popOpen(`<div class="pp"><p class="pp-k">🎀 Qualifier · ${q.w} wins, ${q.l} losses</p><h2 class="db-h">${nm} is out this time</h2><div class="vd-ph"><img src="${p.src}" alt=""></div>
      <p class="db-s">${QF_WIN - q.w <= 2 ? `So close: just <b>${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'}</b> short.` : 'The crowd preferred others today.'} Try another shot: bright, close-up photos tend to win.</p>
      <button class="btn block db-go" id="qoE">📷 Enter another photo</button><div style="text-align:center"><button class="link pc-later" id="qoJ">⚖️ Keep judging</button></div></div>`);
    $('#qoE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qoJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; } }
(() => { const fp = finPick; finPick = function () { if (qlReal().length >= 1 && !((S.entT || 0) > 0)) { const left = 3 - (S.vrq || 0); try { popClose(); } catch (e) {}
      popOpen(`<div class="pp"><p class="pp-k">🎟️ Photo entry</p><h2 class="db-h">Judge to enter another photo</h2><p class="db-s">Judge <b>${left} more round${left === 1 ? '' : 's'}</b> (6 pairs each) to earn your next entry. Your judging gives other players’ photos their matchups.</p>
        <div class="vr-tk vr-tk2">${[0, 1, 2].map(i => `<i class="${i < (S.vrq || 0) ? 'got' : ''}"></i>`).join('')}</div><button class="btn block db-go" id="ntJ">⚖️ Judge now</button></div>`);
      $('#ntJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; return; }
    return fp.apply(this, arguments); }; window.finPick = finPick; })();
function qfStart(p) { needAge(() => { try { popClose(); } catch (e) {} payCash(1, 'A $1 Final entry', () => setTimeout(() => qfLobby(p), 250)); }); }
function qfLobby(p) { const k = photoShow(p), r = cpRng(Date.now() % 1e6), pool = ppShuffle(SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src), r).slice(0, 5);
  const L = [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(pool.map((x, i) => ({ src: x.src, t: x.title || 'Photo', h: '@' + QS_NAMES[(i * 3 + Math.floor(r() * 9)) % QS_NAMES.length], st: 55 + ppHash(x.id || x.title) % 25 })));
  popOpen(`<div class="pp qfx"><p class="pp-k">🏁 ${esc(showName(k))} Final · $1</p><h2 class="db-h" id="qfH">Finalists arriving…</h2><div class="qf-lob">${L.map((x, i) => `<div id="qfL${i}" class="${i ? '' : 'in'}"><img src="${i ? '' : x.src}" alt=""><small>${i ? '…' : 'You'}</small></div>`).join('')}</div>
    <p class="db-s">Prize pool <b>$5.10</b> · 1st <b>$3.50</b> · 2nd <b>$1.60</b></p><p class="db-sim">Prototype: other finalists are simulated</p></div>`);
  L.forEach((x, i) => i && setTimeout(() => { const e = document.getElementById('qfL' + i); if (!e) return; e.className = 'in'; e.innerHTML = `<img src="${x.src}" alt=""><small>${esc(x.h)}</small>`; }, 450 * i));
  setTimeout(() => { const h = document.getElementById('qfH'); if (h) h.textContent = '6 finalists · they’re off!'; setTimeout(() => qfRace(p, L), 900); }, 450 * L.length); }
function qfRace(p, L) { const r = cpRng(Date.now() % 1e6), ord = L.map((x, i) => [i, x.st + (r() - .5) * 34]).sort((a, b) => b[1] - a[1]).map(x => x[0]), rank = i => ord.indexOf(i);
  popOpen(`<div class="pp qfx"><p class="pp-k">🏁 ${esc(showName(photoShow(p)))} Final · live</p><h2 class="db-h">The crowd is voting…</h2>
    <div class="qf-trk">${L.map((x, i) => `<div class="qf-ln ${x.me ? 'me' : ''}"><span class="qf-nm">${x.me ? 'You' : esc(x.h)}</span><span class="qf-rail"><img id="qfH${i}" src="${x.src}" alt="" style="left:0%"></span></div>`).join('')}<i class="qf-fin"></i></div>
    <p class="db-com" id="qfC">🏁 And they’re off!</p></div>`);
  const T = 26; let t = 0; const iv = setInterval(() => { t++; const k = t / T;
    const pos = L.map((x, i) => Math.min(100, (100 - rank(i) * 7) * (1 - Math.pow(1 - k, 1.6)) + Math.sin(t * .9 + i * 1.7) * 5 * (1 - k)));
    L.forEach((x, i) => { const e = document.getElementById('qfH' + i); if (e) e.style.left = `calc(${pos[i] * .86}% )`; });
    const lead = pos.indexOf(Math.max(...pos)), me = 0, myR = [...pos].sort((a, b) => b - a).indexOf(pos[me]) + 1, c = document.getElementById('qfC');
    if (c) c.textContent = t >= T ? '📸 Across the line…' : lead === me ? '🔥 You’re in front!' : t > T - 6 ? `🏁 Final stretch · you’re ${ppOrd(myR)}` : `${L[lead].me ? 'You' : L[lead].h} leads · you’re ${ppOrd(myR)}`;
    if (t >= T) { clearInterval(iv); photoFinish(() => qfResult(p, L, ord)); } }, 500); }
function qfResult(p, L, ord) { const myRank = ord.indexOf(0) + 1, prize = QF_PAY[myRank - 1] || 0; p.fin = 0; p.raced = { rank: myRank, prize, at: Date.now() };
  if (myRank <= 3) rzAdd(p, myRank - 1); if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); try { earnAdd({ kind: 'f', pid: p.id, t: p.title, amt: prize, place: myRank }); } catch (e) {} } save();
  popOpen(`<div class="pp qfx ${prize ? 'won' : ''}"><p class="pp-k">🏁 Final result</p><h2 class="db-h">${myRank === 1 ? `${esc(rcName(p))} won the Final!` : `${esc(rcName(p))} finished ${ppOrd(myRank)}`}</h2>
    ${prize ? `<div class="rv-won"><span>Cash won</span><b>${money(prize)}</b></div>` : `<p class="db-s">Only 1st and 2nd are paid. ${myRank === 3 ? 'So close, and a bronze rosette for the frame!' : 'Its finalist rosette stays on the frame.'}</p>`}
    <div class="qf-res">${ord.map((i, k) => `<div class="${L[i].me ? 'me' : ''}"><em>${['🥇', '🥈', '🥉'][k] || ppOrd(k + 1)}</em><img src="${L[i].src}" alt=""><b>${L[i].me ? esc(rcName(p)) : esc(L[i].t)}</b><i>${k < 2 ? money(QF_PAY[k]) : ''}</i></div>`).join('')}</div>
    <button class="btn block db-go" id="qrE">📷 Enter another photo</button><div style="text-align:center"><button class="link pc-later" id="qrJ">⚖️ Judge to earn your next entry</button></div><p class="db-sim">Prototype: other finalists and votes are simulated</p></div>`);
  if (prize) setTimeout(() => { try { paintWallet(); cashExplosion(prize, { label: 'Final' }); rvConfetti(document.querySelector('.qfx'), 60); } catch (e) {} }, 300);
  $('#qrE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qrJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-qfr]'); if (b) { e.preventDefault(); const p = (S.photos || []).find(x => x.id === b.dataset.qfr); if (p) qfStart(p); } });
function vdLine(p) { const q = p.ql; let st = '';
  if (p.raced) st = `🏁 Raced a Final · ${ppOrd(p.raced.rank)}${p.raced.prize ? ` · won <b>${money(p.raced.prize)}</b>` : ''}`;
  else if (p.fin) st = `🎀 <b>Finalist</b> · ready to race <button class="btn db-go cashb ql-btn" data-qfr="${p.id}">🏁 Race · $1</button>`;
  else if (q && q.done === 'x') st = `Qualifier ${q.w}–${q.l} · out this time`;
  else if (q) st = `🎀 Qualifier <b>${q.w}–${q.l}</b> · ${QF_WIN - q.w} win${QF_WIN - q.w === 1 ? '' : 's'} to a Final`;
  return `<p class="vd-l">${st || 'Not entered yet'}${p.starter ? ' · <em>Starter photo</em>' : ''}</p>`; }
function earnHeadHTML() { if (!(S.photos || []).length) return ''; const left = 3 - (S.vrq || 0), t = S.entT || 0, A = qlReal();
  return `<div class="ern"><p class="ern-k">🎀 Your photos in play</p><p class="ern-top">${A.filter(p => p.ql && !p.ql.done).length} qualifying · ${A.filter(p => p.fin).length} ready to race · ${A.filter(p => p.raced).length} raced</p>
    <p class="ern-top">${t ? `🎟️ <b>${t} entry ticket${t > 1 ? 's' : ''}</b> ready` : `🎟️ Judge <b>${left} more round${left === 1 ? '' : 's'}</b> for your next entry`}</p><button class="btn block db-go" onclick="finPick()">📷 Enter a photo</button></div>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .vr-mine{display:none!important}
.ql-s{margin:8px 2px 0}.ql-r{display:flex;align-items:center;gap:10px;padding:8px 10px;margin:0 0 6px;border-radius:12px;background:#F1F6EC;box-shadow:inset 0 0 0 1.5px #2F6B3F;text-align:left}
.ql-r img{width:40px;height:50px;border-radius:7px;object-fit:cover;flex:none}.ql-r>span{flex:1;font:700 .8rem/1.35 Nunito,system-ui;color:#22502F}.ql-r b{color:#14213D}
.ql-d{display:flex;gap:2px;margin:4px 0 2px}.ql-d i{flex:1;height:7px;border-radius:2px;background:#DCE8D6}.ql-d i.w{background:#2F6B3F}.ql-d i.l{background:#C0533F}
.ql-r small{display:block;font-size:.74rem}.ql-r small.w{color:#2F6B3F}.ql-r small.l{color:#A6402F}
.qf-box{margin:8px 0;padding:10px 12px;border-radius:14px;background:#F1F6EC;box-shadow:inset 0 0 0 2px #2F6B3F;color:#22502F;font-size:.88rem;line-height:1.5}.qf-box b{color:#14213D}
.qf-lob{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}.qf-lob div{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px;border-radius:12px;background:#F3EEE5;opacity:.45}.qf-lob div.in{opacity:1;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;animation:qsPlus .35s ease-out}
.qf-lob img{width:56px;height:56px;border-radius:50%;object-fit:cover;background:#E3EAF5}.qf-lob small{font-size:.7rem;font-weight:800;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.qf-trk{position:relative;background:#14213D;border-radius:14px;padding:8px 10px;margin:8px 0;box-shadow:inset 0 0 0 1.5px #D9AE4F}
.qf-ln{display:grid;grid-template-columns:70px 1fr;align-items:center;gap:6px;height:44px}.qf-nm{font-size:.7rem;font-weight:800;color:#C9D3E6;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left}.qf-ln.me .qf-nm{color:#F3D98B}
.qf-rail{position:relative;height:40px;border-bottom:1px dashed rgba(255,255,255,.18)}.qf-rail img{position:absolute;top:2px;width:36px;height:36px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #fff;transition:left .5s linear}
.qf-ln.me .qf-rail img{box-shadow:0 0 0 3px #F3D98B,0 0 12px #F3D98B}.qf-fin{position:absolute;top:8px;bottom:8px;right:14px;width:6px;background:repeating-linear-gradient(0deg,#fff 0 6px,#14213D 6px 12px)}
.qf-res{display:grid;gap:5px;margin:8px 0}.qf-res div{display:grid;grid-template-columns:30px 34px 1fr auto;gap:8px;align-items:center;padding:6px 10px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.qf-res div.me{box-shadow:inset 0 0 0 2px #D9AE4F;background:#FFF8E6}
.qf-res em{font-style:normal;font-weight:900}.qf-res img{width:34px;height:34px;border-radius:50%;object-fit:cover}.qf-res b{font-size:.84rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.qf-res i{font-style:normal;font-weight:900;color:#2F6B3F}
html body .ql-btn{display:inline-block;width:auto;padding:4px 10px;margin:4px 0 0;font-size:.78rem}
.vr-tk2{justify-content:center;margin:8px 0 12px}.vr-tk2 i{background:#EADCC6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v152 ok')
# pass 2: finalist/out moment shows as soon as the screen is free (not held back by the round pop spacing);
#  Enter-photo screen wording matches the new rules.
s = open(d + 'yofi-real.html').read()
RA("if (!S || !$('#app').classList.contains('on') || !freeScreen() || !popGap()) return; const p = (S.photos || []).find(x => x.ql && x.ql.done && !x.ql.shown); if (p) qlDone(p);",
   "if (!S || !$('#app').classList.contains('on') || !freeScreen()) return; const p = (S.photos || []).find(x => x.ql && x.ql.done && !x.ql.shown); if (p) qlDone(p);")
RA("${first ? 'Your first frame is free: frame your photo and it enters that Final’s <b>qualifiers</b>.' : 'Frame your photo for 200 coins and it enters that Final’s qualifiers; the top 2 go through.'}",
   "It plays <b>15 head-to-heads</b> judged by the crowd. Win 8 and it races in a Final for cash.${first ? ' Your first entry is free.' : ''}")
s = s.replace("function vrEnd() { if (!S.vr || S.vr.res.length < VR_N) return; if (!freeScreen()) { setTimeout(vrEnd, 1200); return; }",
              "function vrEnd() { if (!S.vr || S.vr.res.length < VR_N) return; if (!freeScreen() || (S.photos || []).some(x => x.ql && x.ql.done && !x.ql.shown)) { setTimeout(vrEnd, 1200); return; }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v152 pass2 ok')
# pass 3: round bar never mentions the old free Match Race
s = open(d + 'yofi-real.html').read()
RA("nb = S.fmPend || S.tut === 1;", "nb = false;")
open(d + 'yofi-real.html', 'w').write(s); print('rm v152 pass3 ok')
