# Real Money build, step 173 (after rmv169.py): more photos in, coins buy the route to cash.
#  - Photo entries are FREE (up to 5 a day). Pick several photos at once from the camera roll: the first goes through
#    the normal flow, the rest join your stable and start their qualifiers too.
#  - Training costs 20 🟡 a match (no coin payout). Win 3 before 3 losses = 💵 Cash-ready for good: that photo can enter
#    Finals ($2–$20) and cash head-to-heads any time, and never goes back to coins. 3 losses = training over, try again.
#  - Photos that qualify through voting are cash-ready for good too.
#  Simulated: rivals and crowd votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""<button class="btn block db-go" id="qrE">📷 Enter another photo · ${ENTRY_COINS} 🟡</button>""", """<button class="btn block db-go" id="qrE">📷 Enter another photo · free</button>""")
RA("""📷 Enter a new photo${qlReal().length ? ` · ${ENTRY_COINS} 🟡` : ' · free'}</button>""", """📷 Add photos · free</button>""")
RA("Entry: 100 🟡.", "Entry is free.")
RA("Each photo entry costs 100 🟡. Finals are 6-photo races", "Photo entries are free (up to 5 a day). Finals are 6-photo races")
RA("Send it to your stable: a free tune-up, then win 5 training head-to-heads to race again.", "Send it to your stable: a free tune-up, then train it to make it cash-ready.", 2)
s = s.replace("function fcNotify() {", r"""const DAY_ENT = 5, TQ_COST = 20, TQ_WIN = 3;
const dEnt = () => { const t = todayKey(); if (!S.dEnt || S.dEnt.d !== t) S.dEnt = { d: t, n: 0 }; return S.dEnt; };
function qlStart(p) { qlStrength(p); S.freeRe = 0; S.entT = 0; S.nEnt = (S.nEnt || 0) + 1; p.bo = !p.starter && S.nEnt <= 2 ? 1 : 0; if (!p.starter) dEnt().n++;
  p.ql = { w: 0, l: 0, at: Date.now() }; p.pool = 0; save(); }
(() => { const fp = finPick; finPick = function () { if (dEnt().n >= DAY_ENT) { try { popClose(); } catch (e) {}
    popOpen(`<div class="pp"><p class="pp-k">📷 Photo entries</p><h2 class="db-h">That’s ${DAY_ENT} photos today</h2><p class="db-s">New entries open again tomorrow. Meanwhile, vote to move your photos along, or train them in your stable.</p>
      <button class="btn block db-go" id="dlV">⚖️ Vote</button><div style="text-align:center"><button class="link pc-later" id="dlS">🐎 Your stable</button></div></div>`);
    $('#dlV').onclick = () => { popClose(); go('judge'); renderJudge(); }; $('#dlS').onclick = () => { popClose(); finalsTab(); }; return; }
  S.freeRe = 1; return fp.apply(this, arguments); }; window.finPick = finPick; })();
// several photos at once: extra files join the stable and start their qualifiers
try { $('#file').multiple = true; } catch (e) {}
$('#file').addEventListener('change', e => { const F = [...(e.target.files || [])].slice(1).filter(f => /^image\//.test(f.type)); if (!F.length) return; const cat = window.__preCat || null;
  const room = Math.max(0, DAY_ENT - dEnt().n - 1), L = F.slice(0, room); if (!L.length) { toast(`📷 ${DAY_ENT} photos a day: the extra ones can go in tomorrow`); return; }
  setTimeout(async () => { let n = 0; for (const f of L) { try { const url = URL.createObjectURL(f), img = await loadImg(url), id = toID(img, 960); URL.revokeObjectURL(url); const src = toURL(id), sc = capUpload(Engine.score(Engine.analyze(id)));
        const p = { id: uid(), src, orig: src, s: sc, start: sc.total, enh: 0, q: sc.total >= CFG.QUALIFY, at: Date.now(), cat, framed: Date.now(), title: `Photo ${S.photos.length + 1}` };
        S.photos.push(p); qlStart(p); n++; } catch (x) {} }
    if (n) { save(); toast(`📷 ${n} more photo${n > 1 ? 's' : ''} added to your stable and entered`); try { qlPaint(); } catch (x) {} } }, 2500); });
// training = the coin route to cash
const isCashOK = p => !!(p.cashOK || stProven(p));
function stStatus(p) { const q = p.ql, T = p.tq || { w: 0, l: 0 };
  if (isCashOK(p)) return { k: 'fin', t: p.fin ? '🏆 Finalist · 💵 Cash-ready' : '💵 Cash-ready', btn: `<button class="btn st-b cash" data-stf="${p.id}">🏁 Enter a Final</button>` };
  if (q && !q.done) return { k: 'q', t: `🎀 Qualifying · ${q.w}–${q.l}${T.w || T.l ? ` · training ${T.w}–${T.l}` : ''}`, btn: '<button class="btn st-b" data-stv>⚖️ Vote to move it</button>' };
  return { k: 'x', t: T.w || T.l ? `🏋️ Training ${T.w}–${T.l} · ${TQ_WIN - T.w} more win${TQ_WIN - T.w === 1 ? '' : 's'} to cash-ready` : 'Resting · train it to go cash-ready', btn: `<button class="btn st-b" data-str="${p.id}" data-free="1">🎀 Re-enter the qualifier · free</button>` }; }
function stCard(p) { const st = stStatus(p), H = p.h2h || { w: 0, l: 0, cash: 0 }, ok = isCashOK(p), T = p.tq || { w: 0, l: 0 };
  return `<div class="st-c ${st.k}"><div class="st-top"><img src="${p.src}" alt=""><div class="st-i"><b>${esc(rcName(p))}</b><span class="st-s">${st.t}</span>
      <span class="st-m"><em>💪 Form +${p.form || 0}</em>${H.w || H.l ? `<em>H2H ${H.w}–${H.l}</em>` : ''}${H.cash ? `<em class="cash">${money(H.cash)} won</em>` : ''}</span></div></div>
    ${ok ? '' : `<div class="st-tq">${[0, 1, 2].map(i => `<i class="${i < T.w ? 'w' : ''}">${i < T.w ? '✓' : ''}</i>`).join('')}<span>Win ${TQ_WIN} before ${TQ_WIN} losses to go 💵 cash-ready</span>${[0, 1, 2].map(i => `<i class="x ${i < T.l ? 'l' : ''}">${i < T.l ? '✕' : ''}</i>`).join('')}</div>`}
    <div class="st-a">${ok ? `<button class="btn st-b cash" data-sth="${p.id}" data-m="c">💵 Head-to-head · $2</button>` : `<button class="btn st-b tr" data-sth="${p.id}" data-m="t">🏋️ Train · ${TQ_COST} 🟡</button>`}${st.btn}</div></div>`; }
(() => { const ho = h2hOpen; h2hOpen = function (p, fee, rv) { const r = ho.apply(this, arguments); try { if (!(fee > 0)) { const P = document.querySelector('.h2x .qfp-p'), T = p.tq || { w: 0, l: 0 };
      if (P) P.innerHTML = `Training · <b>${TQ_COST} 🟡</b> a match<small>You’re ${T.w}–${T.l}. Win ${TQ_WIN} before ${TQ_WIN} losses and ${esc(rcName(p))} is cash-ready for good: Finals and cash head-to-heads.</small>`;
      const g = $('#h2Go'); g.textContent = `🏋️ Train · ${TQ_COST} 🟡`; g.onclick = () => { if ((S.gems || 0) < TQ_COST) { toast(`🟡 Training costs ${TQ_COST} coins · vote to earn them`); return; } S.gems -= TQ_COST; save(); try { paintGems(); } catch (e) {} h2hLive(p, R2(p), 0); }; } } catch (e) {} return r; };
  function R2(p) { const im = document.querySelectorAll('.h2x .h2-vs img')[1], sm = document.querySelectorAll('.h2x .h2-vs small')[1], t = (document.querySelector('.h2x .db-h').textContent.split(' vs ')[1] || 'A rival'); return { src: im ? im.getAttribute('src') : p.src, title: t, h: sm ? sm.textContent : '@rival' }; } })();
(() => { const hl = h2hLive; h2hLive = function (p, R, fee) { const r = hl.apply(this, arguments); if (fee > 0) return r;
  const iv = setInterval(() => { const box = document.getElementById('h2R'); if (!document.getElementById('h2n')) { clearInterval(iv); return; } if (!box || !box.innerHTML) return; clearInterval(iv);
    const won = !!document.querySelector('#h2A.win'), T = p.tq = p.tq || { w: 0, l: 0 }; S.gems = Math.max(0, (S.gems || 0) - (won ? TRN_COINS : 0)); if (won) T.w++; else T.l++;
    let msg; if (T.w >= TQ_WIN) { p.cashOK = 1; msg = `<div class="rv-won"><span>${esc(rcName(p))} is</span><b>💵 Cash-ready</b></div><p class="db-s">For good: it can enter Finals ($2–$20) and cash head-to-heads any time.</p>`; }
    else if (T.l >= TQ_WIN) { msg = `<p class="db-s">Training over at ${T.w}–${T.l}. Start a fresh run, or try another photo.</p>`; p.tq = { w: 0, l: 0 }; }
    else msg = `<p class="re-rzl">${won ? '✓ Win' : '✕ Loss'} · training ${T.w}–${T.l} · ${TQ_WIN - T.w} more win${TQ_WIN - T.w === 1 ? '' : 's'} to cash-ready</p>`;
    save(); try { paintGems(); } catch (e) {}
    box.innerHTML = `${msg}${p.cashOK ? `<button class="btn block db-go cashb" id="h2F">🏁 Enter a Final</button>` : `<button class="btn block db-go" id="h2Ag">🏋️ Train again · ${TQ_COST} 🟡</button>`}<div style="text-align:center"><button class="link pc-later" id="h2Bk">Back to stable</button></div>`;
    if (p.cashOK && T.w >= TQ_WIN) { try { rvConfetti(document.querySelector('.h2x'), 70); } catch (e) {} }
    if ($('#h2F')) $('#h2F').onclick = () => { popClose(); qfStart(p); }; if ($('#h2Ag')) $('#h2Ag').onclick = () => h2hOpen(p, 0); $('#h2Bk').onclick = () => { popClose(); finalsTab(); }; }, 150); return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.st-tq{display:flex;align-items:center;gap:5px;margin-top:9px}.st-tq span{flex:1;text-align:center;font:700 .7rem/1.25 Nunito,system-ui;color:#5B4A3F}
.st-tq i{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;font:900 .7rem Nunito,system-ui;background:#EEE6D8;color:#fff}.st-tq i.w{background:#2F6B3F}.st-tq i.l{background:#C0533F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v170 ok')
# pass 2: stable intro matches the new rules
s = open(d + 'yofi-real.html').read()
RA("Your photos are your horses. Train them for coins, race them head-to-head for cash. ${isYoungW() ? 'Judging' : 'Voting'} gets them to the Final.",
   "Your photos are your horses. ${isYoungW() ? 'Judging' : 'Voting'} moves them through the qualifier; training (coins) is the other way in. Once a photo is 💵 cash-ready, it races for real money for good.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v170 pass2 ok')
