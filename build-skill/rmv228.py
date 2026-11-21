# Real Money build, step 231 (after rmv227.py): the user's picks from the options board.
#  A. Welcome offer popup when you reach the Final: "Deposit $10 · get $5 free" + "💵 Play for Real".
#     Not now -> use the free first entry. The welcome offer everywhere is now deposit $10, get $5 Bonus Cash.
#  1a. Daily rewards live inside Welcome back (no separate daily popup). Big 🔥 day streak at the top;
#      each row keeps its own button; no big green button. Tapping the header 🔥 opens it.
#  2b. Training opens a navy screen: Sterling vs rival, your 3-win progress, one "🏋️ Train · 50 🪙" button, then the race.
#  3a. No tune-up step. Training is a coins-only match (no crowd votes, no prizes) and says so.
#  4b. Daily Cup is a one-line teaser at the top of the Stable until a photo qualifies.
#  5a. Stable card: progress steps + buttons only (no "Cash races unlocked", "Ready to race", head-to-head chip, run line).
#      "Race it again" no longer says "free".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA('🎀 Race it again · free</button><button class="btn block nv-go2" id="rnH">', '🎀 Race it again</button><button class="btn block nv-go2" id="rnH">')
RA("function fcNotify() {", r"""const WO_DEP = 10, WO_BON = 5;
function woGive(onBuy) { return () => { S.cashMode = 1; save(); if (!S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + WO_BON).toFixed(2); save(); toast(`🎁 $${WO_BON} free added · used first on entries`); } try { paintWallet(); } catch (e) {} if (onBuy) onBuy(); }; }
function addCashNv(amt, what, onBuy) { amt = +amt || 0; const have = +((S.cash || 0) + (S.bonus || 0)).toFixed(2), w = !S.paidCash && !S.bonusGot, bn = w ? WO_BON : 0;
  const add = amt ? ([5, 10, 20, 50, 100].filter(a => !w || a >= WO_DEP).find(a => have + a + bn >= amt) || 100) : (w ? WO_DEP : 10), left = +(have + add + bn - amt).toFixed(2), m0 = v => money(v).replace(/\.00$/, '');
  const ttl = amt ? String(what).replace(/^(The|A|An) /, '').replace(/^./, c => c.toUpperCase()) : 'Add cash';
  try { if ($('#sheet').classList.contains('on')) closeSheet(); } catch (e) {}
  popOpen(`<div class="pp qfx nv acn"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">${w ? 'Welcome offer' : 'Add cash'}</span></div><h2 class="nv-h2">${esc(ttl)}</h2>
    <p class="qw-o">${amt ? `Entry <b class="gold">${m0(amt)}</b> · you have <b class="gold">${m0(have)}</b>` : `You have <b class="gold">${m0(have)}</b> to play`}</p>
    <div class="acn-box"><div class="h2w-amt">${m0(add)}</div>${w ? `<span class="acn-bn">+ $${WO_BON} free</span>` : ''}<small>${w ? 'The free $5 is spent first on entries and can’t be withdrawn. Your winnings are real cash.' : 'Cash to play. Your winnings are real cash.'}</small>
      <p class="acn-left">${amt ? `After this entry you’ll have <b>${m0(left)}</b> left to play` : `You’ll have <b>${m0(left)}</b> to play`}</p></div>
    <button class="btn block nv-go" id="acnGo">Deposit ${m0(add)}${amt ? ' · enter now' : ''}</button>
    <div style="text-align:center"><button class="link nv-later" id="acnAll">Other amounts</button> <button class="link nv-later" id="acnNo">Not now</button></div><p class="nv-sim">Demo · no real payment is taken</p></div>`);
  $('#acnGo').onclick = () => { popClose(); checkout(`$${add} cash`, add, () => applyOffer(add, 0, w ? `Welcome offer · $${WO_BON} free` : `$${add} deposit`, woGive(onBuy))); };
  $('#acnAll').onclick = () => { popClose(); openStore(null, onBuy, 'cash'); }; $('#acnNo').onclick = () => popClose(); }
(() => { const qp = qfPick; qfPick = function (p, fee) { if (!p || S.paidCash || S.bonusGot || p.woSeen || window.__woSkip) { window.__woSkip = 0; return qp.apply(this, arguments); } p.woSeen = 1; save(); const nm = esc(rcName(p));
  popOpen(`<div class="pp qfx nv qw wo"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Welcome offer</span></div><h2 class="nv-big sm">${nm} is in the Final!</h2><i class="nv-sw"></i>
    <div class="qw-ph"><img src="${p.src}" alt=""><i class="qw-rz">${rosette('f')}</i></div>
    <div class="wo-box"><small>Deposit</small><b>$${WO_DEP}</b><em>get $${WO_BON} free</em><p>$${WO_DEP + WO_BON} to play · enter this Final at $10 and 1st wins ${money(10 * QF_PAY[0]).replace(".00", "")}</p></div>
    <button class="btn block nv-go" id="woGo">💵 Play for Real</button><div style="text-align:center"><button class="link nv-later" id="woNo">${S.coinFin ? 'Not now' : 'Not now · use my free entry'}</button></div><p class="nv-sim">Demo · no real payment is taken · the free $5 is spent first and can’t be withdrawn</p></div>`);
  $('#woGo').onclick = () => { popClose(); checkout(`$${WO_DEP} cash`, WO_DEP, () => applyOffer(WO_DEP, 0, `Welcome offer · $${WO_BON} free`, woGive(() => { S.coinFin = 1; save(); window.__woSkip = 1; setTimeout(() => qfPick(p, 10), 300); }))); };
  $('#woNo').onclick = () => { popClose(); window.__woSkip = 1; setTimeout(() => qfPick(p, fee), 200); }; }; })();
streakHello = function () { if ((S.tut || 9) < 9 || window.__wbShown) return; const ds = dailyState(); if (ds.D.hello === ds.sk || ds.doneToday) return; ds.D.hello = ds.sk; save(); wbShow(1); };
function wbShow(force) { const R = wbRows(), C = chList(), ds = (() => { try { return dailyState(); } catch (e) { return null; } })(); if (!force && !R.length && !C.length) return false; window.__wbShown = 1;
  const st = ds ? ds.streak || 0 : 0, done = ds && ds.doneToday, n = ds ? Math.min(3, ds.D.sn || 0) : 0;
  const dr = ds && !done ? `<div class="wbk-r day"><span class="wbk-ic">🎁</span><div><b>Today’s reward</b><small>Vote on 3 photos · +15 coins${n ? ` · ${n} of 3 done` : ''}</small></div><button class="btn wbk-b nv2" data-wbv>⚖️ Vote</button></div>` : '';
  popOpen(`<div class="pp qfx nv chw wbk"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big sm">Welcome back</h2>
    <div class="wbs ${st ? '' : 'cold'}"><span class="wbs-f">🔥</span><div><b>${st}</b><small>day streak</small></div><div class="wbs-d">${Array.from({ length: 7 }, (_, i) => `<i class="${i < Math.min(st, 7) ? 'on' : ''}"></i>`).join('')}</div>
      <p>${done ? '✓ Streak safe today · come back tomorrow' : st ? 'Vote on 3 photos today to keep it alive' : 'Vote on 3 photos today to light your first 🔥'}</p></div>
    <div class="wbk-l">${dr}${R.join('')}</div>${C.length ? `<p class="nv-rule"><span>⚔️ ${C.length} challenge${C.length > 1 ? 's' : ''}</span></p><div class="cg-l">${C.map(chRow).join('')}</div>` : ''}
    <div style="text-align:center"><button class="link nv-later" id="chL">Later</button></div>${C.length ? '<p class="nv-sim">Demo · challengers are simulated</p>' : ''}</div>`);
  $('#chL').onclick = () => popClose(); return true; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('#sFlame'); if (!b) return; e.preventDefault(); e.stopPropagation(); try { popClose(); } catch (x) {} wbShow(1); }, true);
trTune = function (p) { if (!p) return; try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {} setTimeout(() => h2hOpen(p, 0), 150); };
(() => { const ho = h2hOpen; h2hOpen = function (p, fee, rv) { if (fee > 0 || !p) return ho.apply(this, arguments); const k = photoShow(p) || finCatOf(p) || 'pets', pool = SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src), o = rv || pool[Math.floor(Math.random() * pool.length)] || { src: p.src, title: 'A rival' };
  const R = rv || { src: o.src, title: o.title || 'A rival', h: '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)] }, T = p.tq || { w: 0, l: 0 }, g = Math.floor(S.gems || 0), nm = esc(rcName(p));
  popOpen(`<div class="pp qfx nv trn3"><button class="h3-x h2r-x" data-h3x aria-label="Close">✕</button><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Training match</span></div>
    <h2 class="nv-h2">${nm} vs ${esc(R.title)}</h2><div class="trn3-vs"><div class="me"><img src="${p.src}" alt=""><small>You</small></div><b>VS</b><div><img src="${R.src}" alt=""><small>${esc(R.h)}</small></div></div>
    <div class="trk-box"><p class="k">🏋️ Training · ${T.w} of ${TQ_WIN} wins</p>${trBars(p)}<p>Win ${TQ_WIN} before ${TQ_WIN} losses and ${nm} is <b>Ready for Cash Races</b>. You’re ${T.w}–${T.l}.</p></div>
    ${g >= TQ_COST ? `<button class="btn block nv-go" id="h2Go">🏋️ Train · ${TQ_COST} 🪙</button>` : `<button class="btn block nv-go" id="h2Go">⚖️ Vote to earn · ${TQ_COST - g} more 🪙</button>`}
    <p class="nv-sim">Training costs coins · no cash prizes · you have ${g} 🪙</p></div>`);
  document.querySelectorAll('[data-h3x]').forEach(b => b.onclick = () => { popClose(); finalsTab(); });
  $('#h2Go').onclick = () => { if ((S.gems || 0) < TQ_COST) { popClose(); try { closeFlow(); } catch (e) {} go('judge'); renderJudge(); return; } S.gems -= TQ_COST; save(); try { paintGems(); } catch (e) {} h2hLive(p, R, 0); }; }; })();
(() => { const hl = h2hLive; h2hLive = function (p, R, fee) { const r = hl.apply(this, arguments); try { if (!(fee > 0)) { const box = document.querySelector('#coach.on .h2r'); if (box) { const T = p.tq || { w: 0, l: 0 };
      const pill = box.querySelector('.nv-pill'); if (pill) pill.textContent = 'Training match'; const sub = box.querySelector('.nv-s'); if (sub) sub.textContent = `Training win ${Math.min(TQ_WIN, T.w + 1)} of ${TQ_WIN} · coins only`;
      const v = box.querySelector('#qrV'); if (v) v.textContent = '🏋️ Training match'; const sim = box.querySelector('.nv-sim'); if (sim) sim.textContent = 'Training · coins only · no cash prizes'; const g = box.querySelector('#h3N'); if (g) g.innerHTML = `First to <b>${H3_WIN}</b> wins`; } } } catch (e) {} return r; }; })();
(() => { const cc = cupCard; cupCard = function () { try { const R = (S.photos || []).filter(p => isCashOK(p) && !p.starter); if (!R.length && cupSt() === 'open') return `<div class="cup-t" id="cupC">🏆 <b>Daily Cup</b> · $100 tonight · qualify a photo to enter</div>`; } catch (e) {} return cc.apply(this, arguments); }; })();
function finBtn(p, plain) { const e = x => plain ? '' : x; if (p && p.runEnd) return `${e('🎀 ')}Race it again`;
  if (inQual(p)) { const n = QS_STEPS - Math.min(QS_STEPS, p.ql.got || 0); return p.ql.live ? `${e('🔴 ')}Qualifier race live` : `${e('⚖️ ')}Vote ${n} step${n === 1 ? '' : 's'} to its qualifier`; }
  const n = QS_STEPS - Math.min(QS_STEPS, (p && p.fr && p.fr.s) || 0); return n <= 0 ? `${e('🏁 ')}Enter a Final` : `${e('⚖️ ')}Vote ${n} step${n === 1 ? '' : 's'} to the Final`; }
(() => { const sh = stHero; stHero = function (p) { let h = sh.apply(this, arguments); try { h = h.replace(/<p class="sx-rule"><span>Cash races unlocked<\/span><\/p>/, '').replace(/<p class="sx-run[^"]*">[\s\S]*?<\/p>/, '').replace(/<p class="sx-chip">[^<]*<\/p>/, '').replace('<em class="no">Ready to race</em>', ''); } catch (e) {} return h; }; })();
function fcNotify() {""")
s = s.replace('</style>', """.wo-box{margin:12px 0 14px;padding:14px;border-radius:18px;text-align:center;background:linear-gradient(180deg,#FBF3DC,#F3D98B);color:#14213D}.wo-box small{display:block;font:900 .74rem Nunito,system-ui;letter-spacing:.12em;text-transform:uppercase;color:#9A6B12}
.wo-box b{display:block;font:900 3rem/1 Fraunces,Georgia,serif}.wo-box em{display:inline-block;margin-top:4px;padding:4px 14px;border-radius:999px;background:#1E6B34;color:#fff;font:900 1rem Nunito,system-ui;font-style:normal}.wo-box p{margin:8px 0 0;font:700 .86rem Nunito,system-ui;color:#5B4A3F}
html body .nv.wo .qw-ph{width:44%!important;margin-left:auto!important;margin-right:auto!important}
.wbs{position:relative;margin:10px 0 12px;padding:12px 14px;border-radius:18px;display:grid;grid-template-columns:auto auto 1fr;align-items:center;gap:10px;background:linear-gradient(135deg,#3B1F0E,#7A3A10 55%,#C0601A);box-shadow:inset 0 0 0 2px #F3A13B,0 8px 20px -8px rgba(240,120,30,.6);text-align:left}
.wbs.cold{background:linear-gradient(135deg,#1B2B52,#22325A);box-shadow:inset 0 0 0 2px rgba(255,255,255,.2)}.wbs-f{font-size:2.6rem;filter:drop-shadow(0 0 10px rgba(255,150,40,.8));animation:wbsF 1.6s ease-in-out infinite}.wbs.cold .wbs-f{filter:grayscale(.6);animation:none}
@keyframes wbsF{0%,100%{transform:scale(1) rotate(-3deg)}50%{transform:scale(1.12) rotate(3deg)}}.wbs b{display:block;font:900 2.4rem/1 Fraunces,Georgia,serif;color:#FFE7A8}.wbs small{font:900 .72rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#FFD08A}
.wbs-d{display:flex;gap:5px;justify-content:flex-end}.wbs-d i{width:14px;height:14px;border-radius:50%;background:rgba(255,255,255,.18)}.wbs-d i.on{background:radial-gradient(circle at 35% 35%,#FFE07A,#F08A1E);box-shadow:0 0 6px rgba(255,160,40,.8)}
.wbs p{grid-column:1/-1;margin:0;font:700 .84rem Nunito,system-ui;color:#FFE7C2}
.trn3-vs{display:flex;align-items:center;justify-content:center;gap:10px;margin:10px 0}.trn3-vs div{text-align:center}.trn3-vs img{width:120px;height:120px;object-fit:cover;border-radius:16px;border:3px solid rgba(255,255,255,.25)}.trn3-vs .me img{border-color:#D9AE4F}
.trn3-vs small{display:block;margin-top:4px;font:800 .8rem Nunito,system-ui;color:#C9D3E6}.trn3-vs b{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#14213D;box-shadow:inset 0 0 0 2px #D9AE4F;font:900 .9rem Fraunces,Georgia,serif;color:#F3D98B}.trn3{position:relative}
.cup-t{margin:0 0 12px;padding:9px 14px;border-radius:999px;background:#14213D;color:#EEF1F8;font:700 .86rem Nunito,system-ui;text-align:center;box-shadow:inset 0 0 0 1.5px #D9AE4F}.cup-t b{color:#F3D98B}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v228 ok')
