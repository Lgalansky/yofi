# Real Money build, step 198 (after rmv194.py): challenges while you're away — a reason to come back.
#  - Photos that are Ready for Cash Races get challenged by other players: "@coco.pup challenged Cliff top · $2 ·
#    winner takes $3.40". Up to 2 waiting at a time; each expires after 24 h.
#  - On return (20+ min away): "While you were away" full-screen card listing the challenges, Accept / Decline.
#  - During play: a new one can arrive every ~4 min (toast + a red count on the Play tab).
#  - Stable: "⚔️ Challenges" section at the top with Accept · $2 / Decline. Accept → pay the entry → the live
#    head-to-head against that rival's photo (3-2-1, 15 votes, result).
#  Simulated: the challengers. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const CH_MAX = 2, CH_TTL = 864e5;
const chList = () => { S.chal = (S.chal || []).filter(c => Date.now() - c.at < CH_TTL && (S.photos || []).some(p => p.id === c.pid && isCashOK(p))); return S.chal; };
function chMake() { const R = (S.photos || []).filter(p => isCashOK(p) && !p.starter); if (!R.length || chList().length >= CH_MAX) return null;
  const p = R[Math.floor(Math.random() * R.length)], k = photoShow(p) || finCatOf(p) || 'pets', pool = SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src && !S.chal.some(c => c.src === x.src)); if (!pool.length) return null;
  const o = pool[Math.floor(Math.random() * pool.length)], taken = S.chal.map(c => c.h), N = QS_NAMES.filter(h => !taken.includes('@' + h));
  const c = { id: 'c' + Date.now() + Math.floor(Math.random() * 99), pid: p.id, src: o.src, t: o.title || 'A rival', h: '@' + N[Math.floor(Math.random() * N.length)], fee: Math.random() < .25 ? 5 : 2, at: Date.now() - Math.floor(Math.random() * 3) * 3600e3 };
  S.chal.push(c); S.chAt = Date.now(); save(); return c; }
const chAgo = c => { const m = Math.max(1, Math.round((Date.now() - c.at) / 60000)); return m < 60 ? `${m} min ago` : `${Math.round(m / 60)} h ago`; };
function chRow(c) { const p = S.photos.find(x => x.id === c.pid);
  return `<div class="cg-r"><div class="cg-vs"><img src="${c.src}" alt=""><i>VS</i><img src="${p.src}" alt=""></div><div class="cg-i"><b>${esc(c.h)} challenged ${esc(rcName(p))}</b><small>“${esc(c.t)}” · $${c.fee} entry · winner takes <em>${money(c.fee * H2H_PAY)}</em> · ${chAgo(c)}</small></div>
    <div class="cg-b"><button class="btn cg-y" data-chy="${c.id}">Accept · $${c.fee}</button><button class="cg-n" data-chn="${c.id}">Decline</button></div></div>`; }
function chDot() { const b = document.getElementById('segCompete'); if (!b) return; let d = b.querySelector('.cg-dot'); const n = chList().length; if (!n) { if (d) d.remove(); return; } if (!d) { d = document.createElement('i'); d.className = 'cg-dot'; b.style.position = 'relative'; b.appendChild(d); } d.textContent = n; }
function chAway() { const L = chList(); if (!L.length) return;
  popOpen(`<div class="pp qfx nv chw"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">While you were away</span></div><h2 class="nv-h2">${L.length} challenge${L.length > 1 ? 's' : ''} waiting</h2>
    <p class="qw-o">Other players want to race your photos for cash.</p><div class="cg-l">${L.map(chRow).join('')}</div>
    <div style="text-align:center"><button class="link nv-later" id="chL">Later</button></div><p class="nv-sim">Demo · challengers are simulated</p></div>`);
  $('#chL').onclick = () => popClose(); }
document.addEventListener('click', e => { const y = e.target.closest && e.target.closest('[data-chy]'), n = e.target.closest && e.target.closest('[data-chn]'); if (!y && !n) return; e.preventDefault();
  const id = (y || n).dataset.chy || (y || n).dataset.chn, c = chList().find(x => x.id === id); if (!c) return; const p = S.photos.find(x => x.id === c.pid);
  if (n) { S.chal = S.chal.filter(x => x.id !== id); save(); chDot(); const row = n.closest('.cg-r'); if (row) row.remove(); if (!chList().length) { try { if (document.querySelector('.chw')) popClose(); } catch (x) {} } toast('Challenge declined'); return; }
  try { popClose(); } catch (x) {} try { closeFlow(); } catch (x) {}
  payCash(c.fee, `A $${c.fee} head-to-head`, () => { S.chal = S.chal.filter(x => x.id !== id); save(); chDot(); setTimeout(() => h2hLive(p, { src: c.src, title: c.t, h: c.h }, c.fee), 250); }); });
(() => { const ft = finalsTab; finalsTab = function () { const r = ft.apply(this, arguments); try { const L = chList(), sub = document.querySelector('#flow .sx .sx-sub'); if (L.length && sub) sub.insertAdjacentHTML('afterend', `<div class="cg-box"><p class="cg-k">⚔️ Challenges <span>${L.length}</span></p>${L.map(chRow).join('')}<p class="cg-sim">Demo · challengers are simulated</p></div>`); chDot(); } catch (e) {} return r; }; })();
setTimeout(() => { try { if (!S || !S.user) return; const away = S.seenAt ? Date.now() - S.seenAt : 0; chList();
    if (away > 20 * 60000) { chMake(); if (Math.random() < .6) chMake(); }
    chDot(); if (away > 20 * 60000 && S.chal.length) { const t = setInterval(() => { if (!$('#app').classList.contains('on') || document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on')) return; clearInterval(t); chAway(); }, 1200); }
    S.seenAt = Date.now(); save(); } catch (e) {} }, 1500);
setInterval(() => { try { if (!S || !S.user || document.hidden) return; S.seenAt = Date.now();
    if ($('#app').classList.contains('on') && Date.now() - (S.chAt || 0) > 4 * 60000 && !window.__qlLive) { const c = chMake(); if (c) { c.at = Date.now(); const p = S.photos.find(x => x.id === c.pid); toast(`⚔️ ${c.h} challenged ${rcName(p)} · $${c.fee} · see Play`); chDot(); } }
    save(); } catch (e) {} }, 30000);
function fcNotify() {""", 1)
s = s.replace('</style>', """.cg-dot{position:absolute;top:4px;right:18%;min-width:20px;height:20px;padding:0 5px;border-radius:10px;background:#C0392B;color:#fff;font:900 .72rem/20px Nunito,system-ui;font-style:normal;text-align:center;box-shadow:0 0 0 2px #fff}
.cg-box{margin:0 0 14px;padding:12px;border-radius:18px;background:linear-gradient(180deg,#22325A,#14213D);box-shadow:0 0 0 2px #D9AE4F}.cg-k{margin:0 0 8px;font:900 1.05rem Fraunces,Georgia,serif;color:#F3D98B}.cg-k span{display:inline-block;min-width:22px;padding:0 6px;border-radius:11px;background:#C0392B;color:#fff;font:900 .78rem/22px Nunito,system-ui;text-align:center;vertical-align:2px}
.cg-sim{margin:6px 0 0;font:600 .7rem Nunito,system-ui;color:#8C9AB5;text-align:center}.cg-l{display:grid;gap:10px;margin:12px 0 4px}
.cg-r{padding:10px;border-radius:14px;background:#FBF6EE;text-align:left}.cg-box .cg-r+.cg-r{margin-top:8px}
.cg-vs{display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:8px}.cg-vs img{width:84px;height:64px;border-radius:10px;object-fit:cover;box-shadow:0 0 0 2px #EADCC6}.cg-vs img:last-child{box-shadow:0 0 0 3px #D9AE4F}.cg-vs i{font:900 .8rem Fraunces,Georgia,serif;font-style:normal;color:#fff;background:#14213D;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center}
.cg-i b{display:block;font:800 .98rem Nunito,system-ui;color:#14213D}.cg-i small{display:block;margin:2px 0 8px;font:600 .8rem/1.35 Nunito,system-ui;color:#5B4A3F}.cg-i em{font-style:normal;font-weight:900;color:#2F6B3F}
.cg-b{display:flex;align-items:center;gap:10px}html body .cg-r .btn.cg-y{flex:1;width:auto!important;min-height:44px!important;margin:0!important;border-radius:999px!important;background:linear-gradient(180deg,#2F8A3F,#1F6A2E)!important;color:#fff!important;font:800 1rem Nunito,system-ui!important;box-shadow:none!important}
.cg-n{border:0;background:none;padding:8px 10px;font:700 .9rem Nunito,system-ui;color:#5B4A3F;text-decoration:underline;cursor:pointer}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v195 ok')
# pass 2: readable Decline
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .cg-r .cg-n{color:#5B4A3F!important;-webkit-text-fill-color:#5B4A3F!important;opacity:1}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v195 pass2 ok')
