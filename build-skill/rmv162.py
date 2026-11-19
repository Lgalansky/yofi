# Real Money build, step 165 (after rmv161.py): one simple loop — vote → coins → enter photos → your votes move them → race.
#  1. Entry = 100 🟡 (first photo free). No more "judge 3 rounds" tickets. Round bar shows coins toward the next entry;
#     a pop appears once when you reach 100 unused coins ("Enter another photo · 100 🟡").
#  2. "Your photos in play" is a swipeable row of cards on the Vote screen, one per photo (qualifying or finalist).
#  3. Each vote YOU make = one crowd vote for each of your photos: the photo (your horse) moves along its track to the
#     🏁 at 8 wins. No background progress, so voting visibly drives it.
#  4. Finalist → full-screen "Your rivals": the 5 other finalists, choose your entry $2 / $5 / $10 / $20
#     (1st 3.5× · 2nd 1.6×), then the full-screen race with a live vote counter and photo finish.
#  Simulated: crowd votes, rivals, race order. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("S.vrq = (S.vrq || 0) + 1; const qual = S.vrq >= 3; if (qual) { S.vrq = 0; S.entT = (S.entT || 0) + 1; } save();", "S.vrq = 0; const qual = false; save();")
RA("""<div class="mp-ent"><span class="mp-ic">🎟️</span><div><b>${first || tk ? `${first ? 'Your first entry is free' : `${tk} entry ticket${tk > 1 ? 's' : ''} ready`}` : `Judge ${left} more round${left === 1 ? '' : 's'} to enter another photo`}</b><small>More photos in play, more Finals to win.</small></div>""",
   """<div class="mp-ent"><span class="mp-ic">🟡</span><div><b>${first ? 'Your first entry is free' : (S.gems || 0) >= ENTRY_COINS ? 'You can enter another photo · 100 🟡' : `${ENTRY_COINS - Math.floor(S.gems || 0)} more coins to enter another photo`}</b><small>Every photo entry costs 100 coins. Voting earns them.</small></div>""")
RA("Win 8 and it races in a 6-photo Final: 1st $3.50, 2nd $1.60.${first ? ' Your first entry is free.' : ''}", "Win 8 and it races in a 6-photo Final for cash.${first ? ' Your first entry is free.' : ' Entry: 100 🟡.'}")
RA("Finals are 6-photo races: $1 to enter, the crowd’s votes decide the order, 1st wins $3.50 and 2nd $1.60.", "Each photo entry costs 100 🟡. Finals are 6-photo races: choose a $2, $5, $10 or $20 entry; 1st wins 3.5× and 2nd 1.6× the entry.")
RA("Race it against 5 other finalists · $1 · 1st <b>$3.50</b> · 2nd <b>$1.60</b>", "Race 5 other finalists · choose a <b>$2–$20</b> entry · 1st wins <b>3.5×</b>")
RA("""<div class="qf-box">🏁 <b>Race it in a Final</b><br>6 finalists · $1 each · 1st <b>$3.50</b> · 2nd <b>$1.60</b><br><small>The crowd’s votes decide the order. Watch the race live.</small></div>""",
   """<div class="qf-box">🏁 <b>Race it in a Final</b><br>See your 5 rivals, choose a <b>$2, $5, $10 or $20</b> entry. 1st wins <b>3.5×</b>, 2nd <b>1.6×</b>.</div>""")
RA("""<button class="btn block db-go cashb" id="qfGo">🏁 Race ${nm} · $1</button>""", """<button class="btn block db-go cashb" id="qfGo">🏁 See your rivals</button>""")
s = s.replace("Race · $1</button>", "Race</button>").replace(" in a Final · $1</button>", " in a Final</button>")
s = s.replace("function fcNotify() {", r"""const ENTRY_COINS = 100, QF_FEES = [2, 5, 10, 20];
function qlStart(p) { qlStrength(p); if (!p.starter && qlReal().filter(x => x !== p).length >= 1) { S.gems = Math.max(0, (S.gems || 0) - ENTRY_COINS); S.c100 = 0; try { paintGems(); toast(`📷 Photo entered · −${ENTRY_COINS} 🟡`); } catch (e) {} }
  S.entT = 0; p.ql = { w: 0, l: 0, at: Date.now() }; p.pool = 0; save(); }
(() => { const fp = finPick; finPick = function () { const first = !qlReal().length;
  if (!first && (S.gems || 0) < ENTRY_COINS) { const g = Math.floor(S.gems || 0); try { popClose(); } catch (e) {}
    popOpen(`<div class="pp"><p class="pp-k">📷 Photo entry · ${ENTRY_COINS} 🟡</p><h2 class="db-h">Earn ${ENTRY_COINS - g} more coins</h2><p class="db-s">You have <b>${g} 🟡</b>. Every vote earns coins, and each round pays a bonus.</p>
      <div class="vr-cb vr-cb2"><i style="width:${Math.min(100, g)}%"></i></div><button class="btn block db-go" id="ceJ">⚖️ Vote to earn coins</button></div>`);
    $('#ceJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; return; }
  S.entT = 1; return fp.apply(this, arguments); }; window.finPick = finPick; })();
setInterval(() => { try { if (!S || !$('#app').classList.contains('on') || !freeScreen() || S.c100 || (S.gems || 0) < ENTRY_COINS || !qlReal().length || Date.now() - (window.__uiT || 0) < 2500) return;
  S.c100 = 1; save(); popOpen(`<div class="pp"><p class="pp-k">🟡 ${Math.floor(S.gems)} coins</p><h2 class="db-h">Enter another photo</h2><p class="db-s">You’ve earned enough for a new entry. More photos in play means more Finals to race.</p>
    <button class="btn block db-go cashb" id="c1E">📷 Enter a photo · ${ENTRY_COINS} 🟡</button><div style="text-align:center"><button class="link pc-later" id="c1L">Later</button></div></div>`);
  $('#c1E').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#c1L').onclick = () => popClose(); } catch (e) {} }, 1500);
function vrBarHTML() { const v = S.vr || { n: 1, res: [] }, ok = v.res.filter(Boolean).length, g = Math.floor(S.gems || 0), can = g >= ENTRY_COINS;
  return `<div class="vr-top" id="vrTop"><div class="vr-l"><b>${can ? '📷 Enough coins for a photo entry' : `🟡 ${ENTRY_COINS - g} more coins to enter a photo`}</b>
    <span class="vr-cb"><i style="width:${Math.min(100, g / ENTRY_COINS * 100)}%"></i></span>${can ? `<button class="vr-en" data-vre>Enter · ${ENTRY_COINS} 🟡</button>` : ''}</div>
    <span class="vr-score">${ok} ✓</span><div class="vr-dots">${Array.from({ length: VR_N }, (_, i) => `<i class="${i < v.res.length ? (v.res[i] ? 'ok' : 'no') : i === v.res.length ? 'now' : ''}"></i>`).join('')}</div></div>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-vre]'); if (b) { e.preventDefault(); finPick(); } });
function vrQuiet(n, ok, pay) { try { paintGems(); gemExplosion(pay, { label: `Round ${n} · ${ok}/${VR_N}` }); } catch (e) {}
  const put = () => { try { vrPaint(); } catch (e) {} const top = document.getElementById('vrTop'); if (!top) return; const o = document.getElementById('vrQ'); if (o) o.remove(); const g = Math.floor(S.gems || 0);
    top.insertAdjacentHTML('afterend', `<div class="vrqb" id="vrQ">✓ <b>Round ${n} done</b> · ${ok}/${VR_N} right · +${pay} 🟡<small>${g >= ENTRY_COINS ? '📷 You have enough coins to enter another photo' : `${ENTRY_COINS - g} more coins to your next photo entry`}</small></div>`);
    setTimeout(() => { const e = document.getElementById('vrQ'); if (e) { e.classList.add('bye'); setTimeout(() => e.remove(), 400); } }, 4200); };
  setTimeout(put, 50); }
// your vote drives your photos: one crowd vote per photo per vote you make; nothing moves in the background
(() => { const cf = callFx; callFx = function () { window.__myVote = 1; try { return cf.apply(this, arguments); } finally { window.__myVote = 0; } }; })();
function qlStep(p) { const q = p.ql; if (!q || q.done || !window.__myVote) return;
  const pr = Math.max(.25, Math.min(.8, .5 + (qlStrength(p) - 62) / 60)), win = Math.random() < pr, o = qlOpp(p);
  if (win) { q.w++; p.qc = (p.qc || 0) + 5; S.gems = (S.gems || 0) + 5; try { paintGems(); } catch (e) {} } else q.l++;
  q.v = (q.v || []).concat(win ? 1 : 0); q.last = { win, t: o.t, src: o.src }; q.fl = Date.now();
  if (q.w >= QF_WIN) q.done = 'q'; else if (q.l > QF_N - QF_WIN) q.done = 'x';
  if (q.done) setTimeout(function tr() { if (q.shown) return; if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx')) { setTimeout(tr, 1200); return; } qlDone(p); }, 1400);
  save(); }
const pvList = () => (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin));
function pvCard(p) { const q = p.ql, fin = p.fin || q.done === 'q', out = q.done === 'x', pos = fin ? 1 : Math.min(1, q.w / QF_WIN), L = q.last, need = QF_WIN - q.w, spare = QF_N - QF_WIN + 1 - q.l;
  return `<div class="pv-c ${fin ? 'fin' : ''} ${out ? 'out' : ''}" data-pid="${p.id}">
    <div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">${fin ? '🏆 Finalist' : out ? 'Out' : `<i>●</i> Qualifier · ${q.w + q.l} of ${QF_N} votes`}</span><em>🟡 +${p.qc || 0}</em></div>
    <div class="pv-tr"><div class="pv-rail">${Array.from({ length: QF_WIN - 1 }, (_, i) => `<i style="left:${(i + 1) / QF_WIN * 100}%"></i>`).join('')}<u style="width:${pos * 100}%"></u></div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"><span class="pv-fl">🏁</span></div>
    <div class="pv-n"><span class="w">✓ ${q.w}</span><span class="l">✕ ${q.l}</span><span class="pv-need">${fin ? '<b>Into the Final!</b>' : out ? `${need} win${need === 1 ? '' : 's'} short` : `<b>${need} more win${need === 1 ? '' : 's'}</b> to the Final · ${spare} loss${spare === 1 ? '' : 'es'} to spare`}</span></div>
    ${fin ? `<button class="btn block pv-go" data-qfr="${p.id}">🏁 See your rivals & race</button>` : `<p class="pv-l ${L ? (L.win ? 'w' : 'l') : ''}">${L ? (L.win ? `✓ Beat “${esc(L.t)}” · +5 🟡` : `✕ Lost to “${esc(L.t)}”`) : '⚖️ Each vote you make moves it forward'}</p>`}</div>`; }
function qlStripHTML() { const P = pvList(); if (!P.length) return '<div id="qlS"></div>';
  return `<div class="pv" id="qlS" data-sig="${P.map(p => p.id + (p.fin || p.ql.done ? 'd' : '')).join(',')}"><div class="pv-h"><b>📷 Your photos in play</b>${P.length > 1 ? `<span>${P.length} photos · swipe ›</span>` : ''}</div>
    <div class="pv-s ${P.length > 1 ? 'multi' : ''}" id="pvS">${P.map(pvCard).join('')}</div>${P.length > 1 ? `<div class="pv-d">${P.map((_, i) => `<i class="${i ? '' : 'on'}"></i>`).join('')}</div>` : ''}</div>`; }
function qlPaint() { const e = document.getElementById('qlS'); if (!e) return; const P = pvList(), sig = P.map(p => p.id + (p.fin || p.ql.done ? 'd' : '')).join(',');
  if (P.length && e.dataset.sig === sig) { P.forEach(p => { const c = e.querySelector(`.pv-c[data-pid="${p.id}"]`); if (!c) return; const t = document.createElement('div'); t.innerHTML = pvCard(p); const n = t.firstElementChild;
      ['.pv-t', '.pv-n', '.pv-l'].forEach(k => { const a = c.querySelector(k), b = n.querySelector(k); if (a && b && a.innerHTML !== b.innerHTML) { a.innerHTML = b.innerHTML; a.className = b.className + ' pop'; } });
      const hz = c.querySelector('.pv-hz'), nz = n.querySelector('.pv-hz'); if (hz && nz) hz.style.left = nz.style.left; const u = c.querySelector('.pv-rail u'), nu = n.querySelector('.pv-rail u'); if (u && nu) u.style.width = nu.style.width; }); return; }
  const sc = document.getElementById('pvS'), sl = sc ? sc.scrollLeft : 0; e.outerHTML = qlStripHTML(); const ns = document.getElementById('pvS'); if (ns) ns.scrollLeft = sl; }
document.addEventListener('scroll', e => { const t = e.target; if (!t || t.id !== 'pvS') return; const i = Math.round(t.scrollLeft / Math.max(1, t.firstElementChild ? t.firstElementChild.offsetWidth + 8 : 1)); document.querySelectorAll('#qlS .pv-d i').forEach((d, k) => d.classList.toggle('on', k === i)); }, true);
// Final: rivals + entry choice, full screen
function qfRivals(p) { if (p.fl && p.fl.length === 5) return p.fl; const k = photoShow(p), pool = ppShuffle(SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src), Math.random).slice(0, 5), N = ppShuffle(QS_NAMES.slice(), Math.random);
  p.fl = pool.map((x, i) => ({ src: x.src, t: x.title || 'Photo', h: '@' + N[i], st: 55 + ppHash(x.id || x.title || String(i)) % 25, w: 8, l: Math.floor(Math.random() * 7) })); save(); return p.fl; }
function qfStart(p) { needAge(() => { try { popClose(); } catch (e) {} setTimeout(() => qfPick(p, window.__qfFee || 2), 120); }); }
function qfPick(p, fee) { const R = qfRivals(p), k = photoShow(p), me = p.ql || { w: 8, l: 0 };
  popOpen(`<div class="pp qfx qfp"><p class="pp-k">🏁 ${esc(showName(k))} Final · 6 photos</p><h2 class="db-h">Your rivals</h2>
    <div class="qfp-l"><div class="me"><img src="${p.src}" alt=""><span><b>${esc(rcName(p))}</b><small>You · qualified ${me.w}–${me.l}</small></span></div>${R.map(x => `<div><img src="${x.src}" alt=""><span><b>${esc(x.t)}</b><small>${esc(x.h)} · qualified ${x.w}–${x.l}</small></span></div>`).join('')}</div>
    <p class="qfp-k">Choose your entry</p><div class="qfp-f">${QF_FEES.map(f => `<button data-qff="${f}" class="${f === fee ? 'on' : ''}"><b>$${f}</b><small>1st ${money(f * QF_PAY[0])}</small></button>`).join('')}</div>
    <div class="qfp-p">1st wins <b>${money(fee * QF_PAY[0])}</b> · 2nd <b>${money(fee * QF_PAY[1])}</b><small>All 6 finalists pay $${fee}. The crowd’s votes decide the order.</small></div>
    <button class="btn block db-go cashb" id="qfpGo">🏁 Race · $${fee}</button><div style="text-align:center"><button class="link pc-later" id="qfpL">Later</button></div>
    <p class="db-sim">You have ${money(S.cash || 0)} · Prototype: rivals and votes are simulated</p></div>`);
  document.querySelectorAll('[data-qff]').forEach(b => b.onclick = () => { window.__keepScroll = 1; qfPick(p, +b.dataset.qff); });
  $('#qfpL').onclick = () => popClose();
  $('#qfpGo').onclick = () => { window.__qfFee = fee; popClose(); payCash(fee, `A $${fee} Final entry`, () => setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(R)), 250)); }; }
function qfRace(p, L) { const fee = window.__qfFee || 2, r = cpRng(Date.now() % 1e6), ord = L.map((x, i) => [i, x.st + (r() - .5) * 34]).sort((a, b) => b[1] - a[1]).map(x => x[0]), rank = i => ord.indexOf(i);
  popOpen(`<div class="pp qfx qfr"><p class="pp-k">🏁 ${esc(showName(photoShow(p)))} Final · $${fee} · live</p><h2 class="db-h">The crowd is voting…</h2>
    <p class="qf-vc">🗳️ <b id="qfV">0</b> votes in · 1st wins <b>${money(fee * QF_PAY[0])}</b></p>
    <div class="qf-trk">${L.map((x, i) => `<div class="qf-ln ${x.me ? 'me' : ''}"><span class="qf-nm">${x.me ? 'You' : esc(x.h)}</span><span class="qf-rail"><img id="qfH${i}" src="${x.src}" alt="" style="left:0%"></span></div>`).join('')}<i class="qf-fin"></i></div>
    <p class="db-com" id="qfC">🏁 And they’re off!</p><p class="db-sim">Prototype: votes and rivals are simulated</p></div>`);
  const T = 30; let t = 0, v = 0; const iv = setInterval(() => { t++; const k = t / T; v += 18 + Math.floor(Math.random() * 40); const vc = document.getElementById('qfV'); if (vc) vc.textContent = v.toLocaleString();
    const pos = L.map((x, i) => Math.min(100, (100 - rank(i) * 7) * (1 - Math.pow(1 - k, 1.6)) + Math.sin(t * .9 + i * 1.7) * 5 * (1 - k)));
    L.forEach((x, i) => { const e = document.getElementById('qfH' + i); if (e) e.style.left = `calc(${pos[i] * .86}% )`; });
    const lead = pos.indexOf(Math.max(...pos)), myR = [...pos].sort((a, b) => b - a).indexOf(pos[0]) + 1, c = document.getElementById('qfC');
    if (c) c.textContent = t >= T ? '📸 Across the line…' : lead === 0 ? '🔥 You’re in front!' : t > T - 6 ? `🏁 Final stretch · you’re ${ppOrd(myR)}` : `${L[lead].h} leads · you’re ${ppOrd(myR)}`;
    if (t >= T) { clearInterval(iv); photoFinish(() => qfResult(p, L, ord)); } }, 500); }
function qfResult(p, L, ord) { const fee = window.__qfFee || 2, PAY = QF_PAY.map(x => +(x * fee).toFixed(2)), myRank = ord.indexOf(0) + 1, prize = PAY[myRank - 1] || 0; p.fin = 0; p.fl = null; p.raced = { rank: myRank, prize, fee, at: Date.now() };
  if (myRank <= 3) rzAdd(p, myRank - 1); if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); try { earnAdd({ kind: 'f', pid: p.id, t: p.title, amt: prize, place: myRank }); } catch (e) {} } save();
  popOpen(`<div class="pp qfx ${prize ? 'won' : ''}"><p class="pp-k">🏁 Final result · $${fee} entry</p><h2 class="db-h">${myRank === 1 ? `${esc(rcName(p))} won the Final!` : `${esc(rcName(p))} finished ${ppOrd(myRank)}`}</h2>
    ${prize ? `<div class="rv-won"><span>Cash won</span><b>${money(prize)}</b></div>` : `<p class="db-s">Only 1st and 2nd are paid. ${myRank === 3 ? 'So close, and a bronze rosette for the frame!' : 'Its finalist rosette stays on the frame.'}</p>`}
    <div class="qf-res">${ord.map((i, k) => `<div class="${L[i].me ? 'me' : ''}"><em>${['🥇', '🥈', '🥉'][k] || ppOrd(k + 1)}</em><img src="${L[i].src}" alt=""><b>${L[i].me ? esc(rcName(p)) : esc(L[i].t)}</b><i>${k < 2 ? money(PAY[k]) : ''}</i></div>`).join('')}</div>
    <button class="btn block db-go" id="qrE">📷 Enter another photo · ${ENTRY_COINS} 🟡</button><div style="text-align:center"><button class="link pc-later" id="qrJ">⚖️ Back to voting</button></div><p class="db-sim">Prototype: other finalists and votes are simulated</p></div>`);
  if (prize) setTimeout(() => { try { paintWallet(); cashExplosion(prize, { label: 'Final' }); rvConfetti(document.querySelector('.qfx'), 60); } catch (e) {} }, 300);
  $('#qrE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qrJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; }
function fcNotify() {""", 1)
s = s.replace('</style>', """.vr-cb{display:block;height:8px;margin-top:6px;border-radius:4px;background:rgba(255,255,255,.18);overflow:hidden}.vr-cb i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#F3D98B,#E9B949);transition:width .5s}
.vr-cb2{background:#EEE6D8;margin:4px 0 14px;height:12px;border-radius:6px}
html body .vr-en{margin-top:7px;padding:4px 12px;border:0;border-radius:999px;background:#2F6B3F;color:#fff;font:800 .78rem Nunito,system-ui;cursor:pointer}
html body .pv{margin:8px 2px 8px;text-align:left}.pv-h{display:flex;align-items:baseline;justify-content:space-between;margin:0 4px 6px}.pv-h b{font:900 .74rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#22502F}.pv-h span{font:800 .72rem Nunito,system-ui;color:#8A7B6C}
.pv-s{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch}.pv-s::-webkit-scrollbar{display:none}
.pv-c{flex:0 0 100%;scroll-snap-align:center;box-sizing:border-box;padding:10px 12px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 2px #2F6B3F}.pv-s.multi .pv-c{flex-basis:90%}
.pv-c.fin{box-shadow:inset 0 0 0 2px #D9AE4F;background:#FFFCF3}.pv-c.out{box-shadow:inset 0 0 0 1.5px #EADCC6;opacity:.8}
.pv-t{display:flex;align-items:center;gap:8px}.pv-t b{font:800 1rem Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.pv-st{font:800 .68rem Nunito,system-ui;color:#5B4A3F;white-space:nowrap}.pv-st i{font-style:normal;color:#C0533F;animation:qmPulse 1.4s ease-in-out infinite}
.pv-t em{margin-left:auto;font-style:normal;font:900 .74rem Nunito,system-ui;color:#9A6B12;background:#FFF1C9;border-radius:999px;padding:2px 8px;white-space:nowrap}
.pv-tr{position:relative;height:46px;margin:6px 0 2px}.pv-rail{position:absolute;left:0;right:22px;top:50%;height:10px;margin-top:-5px;border-radius:5px;background:#E6EFE2}
.pv-rail i{position:absolute;top:-3px;bottom:-3px;width:2px;background:#fff}.pv-rail u{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:linear-gradient(90deg,#7FC48E,#2F6B3F);transition:width .6s ease-out}
.pv-hz{position:absolute;top:3px;width:40px;height:40px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #fff,0 0 0 5px #2F6B3F,0 3px 8px rgba(0,0,0,.25);transition:left .6s cubic-bezier(.3,1.4,.5,1);z-index:1}
.pv-c.fin .pv-hz{box-shadow:0 0 0 3px #fff,0 0 0 5px #D9AE4F,0 0 14px #F3D98B}.pv-fl{position:absolute;right:0;top:50%;transform:translateY(-50%);font-size:1.2rem}
.pv-n{display:flex;gap:10px;align-items:baseline;font:800 .74rem Nunito,system-ui}.pv-n .w{color:#2F6B3F}.pv-n .l{color:#B0473A}.pv-need{margin-left:auto;color:#3D4A5C;font-weight:700}.pv-need b{color:#14213D}
.pv-l{margin:5px 0 0;padding:5px 8px;border-radius:9px;background:#F3EEE5;font:700 .76rem Nunito,system-ui;color:#5B4A3F}.pv-l.w{background:#F1F6EC;color:#22502F}.pv-l.l{background:#F9ECE8;color:#A6402F}
.pv-l.pop,.pv-n.pop{animation:qmFl .35s ease-out}
html body .pv-go{margin:8px 0 0!important;min-height:44px;border-radius:999px!important;background:linear-gradient(180deg,#3A8050,#2F6B3F)!important;color:#fff!important;font:800 .95rem Nunito,system-ui!important}
.pv-d{display:flex;justify-content:center;gap:5px;margin-top:6px}.pv-d i{width:6px;height:6px;border-radius:50%;background:#D8CDBB}.pv-d i.on{background:#2F6B3F;width:16px;border-radius:3px}
html body #coach:has(.qfx) .ppop{position:fixed;inset:0;width:auto;max-width:none;max-height:none;height:100%;margin:0;border-radius:0;overflow-y:auto;box-sizing:border-box;padding:calc(env(safe-area-inset-top) + 18px) 16px 28px;display:flex;flex-direction:column;justify-content:center}
html body #coach:has(.qfx) .ppop>.pp{max-width:520px;margin:0 auto;width:100%}
.qfp-l{display:grid;gap:6px;margin:8px 0 12px}.qfp-l>div{display:flex;align-items:center;gap:10px;padding:6px 10px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.qfp-l>div.me{box-shadow:inset 0 0 0 2px #D9AE4F;background:#FFF8E6}
.qfp-l img{width:42px;height:42px;border-radius:50%;object-fit:cover}.qfp-l b{display:block;font:800 .92rem Fraunces,Georgia,serif;color:#14213D}.qfp-l small{font:700 .74rem Nunito,system-ui;color:#5B4A3F}
.qfp-k{margin:0 0 6px;font:900 .72rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8A7B6C}
.qfp-f{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.qfp-f button{display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 4px;border:0;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;cursor:pointer;font:inherit}
.qfp-f b{font:900 1.2rem Fraunces,Georgia,serif;color:#14213D}.qfp-f small{font:800 .64rem Nunito,system-ui;color:#2F6B3F}.qfp-f button.on{background:#14213D;box-shadow:0 0 0 2px #D9AE4F}.qfp-f button.on b{color:#F3D98B}.qfp-f button.on small{color:#9FE3AE}
.qfp-p{margin:10px 0;padding:10px;border-radius:12px;background:#F1F6EC;box-shadow:inset 0 0 0 1.5px #2F6B3F;font:800 .95rem Nunito,system-ui;color:#22502F}.qfp-p b{color:#14213D}.qfp-p small{display:block;margin-top:2px;font:600 .76rem Nunito,system-ui;color:#3D4A5C}
.qf-vc{margin:0 0 6px;font:700 .86rem Nunito,system-ui;color:#3D4A5C}.qf-vc b{color:#14213D}
html body .qfr .qf-ln{height:56px}html body .qfr .qf-rail{height:52px}html body .qfr .qf-rail img{width:46px;height:46px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v162 ok')
# pass 2: full-screen pages scroll from the top; rivals always from the photo's own category; green race button;
#  the yellow "one of these needs N more wins" note is gone (simpler Vote screen)
s = open(d + 'yofi-real.html').read()
RA("function qfRivals(p) { if (p.fl && p.fl.length === 5) return p.fl; const k = photoShow(p), pool = ppShuffle(SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src), Math.random).slice(0, 5),",
   "function qfRivals(p) { if (p.fl && p.fl.length === 5) return p.fl; const k = photoShow(p) || 'pets', pool = ppShuffle(SEED.filter(x => x.src && finCatOf(x) && finCatOf(x) === k && x.src !== p.src), Math.random).slice(0, 5),")
s = s.replace('</style>', """html body #coach:has(.qfx) .ppop{display:flex;flex-direction:column;justify-content:flex-start}html body #coach:has(.qfx) .ppop>.pp{margin:auto}
html body .pv .btn.pv-go{background:linear-gradient(180deg,#3A8050,#2F6B3F)!important;box-shadow:0 4px 12px rgba(47,107,63,.3)!important}
html body .vr-stake{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v162 pass2 ok')
