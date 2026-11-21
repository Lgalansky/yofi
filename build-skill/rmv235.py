# Real Money build, step 238 (after rmv234.py): Survivor for coins + one coin icon everywhere (user request).
#  - Play tab gets a toggle: "🐎 My stable | (coin) Coin games". Coin games holds the Daily Cup and Survivor.
#  - Survivor (weekly, 7 days): enter with 50 coins. Each day pick ONE photo to win today's race (4 matchups shown).
#    Right pick = survive; wrong = out. A photo can only be picked once. Survive all 7 days and split $100 cash
#    (prize paid by PhotoPicks; entry is coins only, so no purchase). Demo: "settle today now" runs the day instantly;
#    the field of 1,000 players and results are simulated. Results otherwise settle at 8pm.
#  - Coins: every 🪙 / 🟡 shown in the app is drawn with the same yellow coin icon as the header balance.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""const CN_RE = /[\u{1FA99}\u{1F7E1}]/u, CN_SKIP = '#qsChip, #fbBar, #caSched, #lpLive, #crWrap, script, style, textarea, input, option, title, svg';
function cnSwap(root) { if (!root) return; const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => CN_RE.test(n.nodeValue) && n.parentNode && !n.parentNode.closest(CN_SKIP) ? 1 : 3 }); const L = []; let n; while ((n = w.nextNode())) L.push(n);
  L.forEach(t => { const f = document.createDocumentFragment(); t.nodeValue.split(/([\u{1FA99}\u{1F7E1}])/u).forEach(pt => { if (CN_RE.test(pt)) { const sp = document.createElement('span'); sp.className = 'cn-w'; sp.innerHTML = gemIcon('cn-ic'); f.appendChild(sp); } else if (pt) f.appendChild(document.createTextNode(pt)); }); t.parentNode.replaceChild(f, t); }); }
(() => { let q = 0; new MutationObserver(() => { if (q) return; q = 1; requestAnimationFrame(() => { q = 0; try { cnSwap(document.body); pkAll(); } catch (e) {} }); }).observe(document.body, { childList: true, subtree: true, characterData: true }); setTimeout(() => { try { cnSwap(document.body); } catch (e) {} }, 300); })();
(() => { const pt = pkTag; pkTag = function (b) { pt.apply(this, arguments); try { if (b && b.querySelector && b.querySelector('.cn-w, svg.cn-ic') && !b.closest('.pt-seg') && !/\$\d/.test(b.innerText || '') && (b.classList.contains('pk-free') || b.classList.contains('pk-cash'))) { b.classList.remove('pk-free', 'pk-cash', 'pk-dark'); b.classList.add('pk-coin'); } } catch (e) {} }; })();
const SV_COST = 50, SV_DAYS = 7, SV_PRIZE = 100, SV_FIELD = 1000, CN = () => gemIcon('cn-ic');
const svWeek = () => { const m = new Date(); m.setHours(0, 0, 0, 0); m.setDate(m.getDate() - ((m.getDay() + 6) % 7)); return m.toISOString().slice(0, 10); };
function svS() { const w = svWeek(); if (!S.sv || (S.sv.wk !== w && !(S.sv.in && !S.sv.done))) { S.sv = { wk: w, in: 0 }; } return S.sv; }
const svStr = x => 25 + ppHash(String(x.title || '') + String(x.src).slice(-60)) % 70;
function svMx() { const V = svS(); if (V.mx && V.mxd === V.day) return V.mx; const pool = ppShuffle(SEED.filter(x => x.src), cpRng((Date.now() % 1e6) + V.day * 97)).slice(0, 8);
  V.mx = [0, 1, 2, 3].map(i => [pool[i * 2], pool[i * 2 + 1]].map(x => ({ src: x.src, t: x.title || 'Photo', h: '@' + QS_NAMES[ppHash(x.src.slice(-30)) % QS_NAMES.length], st: svStr(x) }))); V.mxd = V.day; save(); return V.mx; }
function svCard() { const V = svS(), g = Math.floor(S.gems || 0), dots = n => `<span class="sv-dots">${Array.from({ length: SV_DAYS }, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('')}</span>`; let body;
  if (!V.in) body = `<h3>$${SV_PRIZE} for the last ones standing</h3><p class="sv-s">Each day pick one photo to win its race. Wrong pick and you’re out. You can only pick a photo once.</p>
    ${g >= SV_COST ? `<button class="btn sv-b" data-sv="enter">Enter · ${CN()} ${SV_COST}</button>` : `<button class="btn sv-b off" disabled>${SV_COST - g} more coins to enter</button>`}<p class="sv-f">7 days · prize paid by PhotoPicks · enter with coins you earn</p>`;
  else if (V.done === 'out') body = `<h3>Knocked out on day ${V.day}</h3><p class="sv-s">${V.last ? `${esc(V.last.mine)} lost ${V.last.b}–${V.last.a}. ` : ''}${V.left.toLocaleString()} of ${SV_FIELD.toLocaleString()} are still standing.</p>${dots(V.day - 1)}<button class="btn sv-b" data-sv="new">Demo: start a new week</button><p class="sv-f">The next Survivor starts Monday</p>`;
  else if (V.done === 'won') body = `<h3>You survived all ${SV_DAYS} days!</h3><p class="sv-s">You and ${V.left - 1} others split $${SV_PRIZE}: <b>${money(V.prize)}</b> added to your cash.</p>${dots(SV_DAYS)}<button class="btn sv-b" data-sv="new">Demo: start a new week</button>`;
  else { const P = V.pk, M = P && svMx()[P.i], me = P && M[P.side], op = P && M[1 - P.side];
    body = `<h3>Day ${V.day} of ${SV_DAYS}</h3><p class="sv-s"><b>${V.left.toLocaleString()}</b> of ${SV_FIELD.toLocaleString()} still standing</p>${dots(V.day - 1)}
      ${P ? `<div class="sv-pk"><img src="${me.src}" alt=""><div><b>Your pick: ${esc(me.t)}</b><small>vs ${esc(op.t)} · results tonight 8pm</small></div></div><button class="link sv-demo" data-sv="settle">Demo: settle today now</button>`
        : `<button class="btn sv-b" data-sv="pick">🛡️ Make today’s pick</button>`}`; }
  return `<div class="sv" id="svC"><span class="sv-ic">🛡️</span><p class="sv-k">Survivor · this week</p>${body}</div>`; }
function svPick() { const V = svS(), M = svMx(), used = V.used || []; let sel = null;
  popOpen(`<div class="pp qfx nv svp"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Survivor · day ${V.day}</span></div><h2 class="nv-h2">Pick one photo to win today</h2><p class="qw-o">The crowd decides each race. Wrong pick and you’re out.</p>
    <div class="svm">${M.map((m, i) => `<div class="svm-r">${m.map((x, k) => { const u = used.includes(x.src); return `<button class="svm-p ${u ? 'used' : ''}" data-svp="${i}:${k}" ${u ? 'disabled' : ''}><img src="${x.src}" alt=""><span>${esc(x.t)}</span>${u ? '<em>used</em>' : ''}</button>`; }).join('<b class="svm-x">VS</b>')}</div>`).join('')}</div>
    <button class="btn block nv-go" id="svGo" disabled>Pick a photo</button><div style="text-align:center"><button class="link nv-later" id="svL">Later</button></div><p class="nv-sim">Demo · other players and crowd votes are simulated</p></div>`);
  document.querySelectorAll('[data-svp]').forEach(b => b.onclick = () => { document.querySelectorAll('[data-svp]').forEach(x => x.classList.toggle('on', x === b)); const [i, k] = b.dataset.svp.split(':').map(Number); sel = { i, side: k }; const g = $('#svGo'); g.disabled = false; g.textContent = `Lock in ${M[i][k].t}`; });
  $('#svL').onclick = () => popClose(); $('#svGo').onclick = () => { if (!sel) return; V.pk = sel; save(); popClose(); toast(`🛡️ Locked in: ${M[sel.i][sel.side].t}`); finalsTab(); }; }
function svSettle() { const V = svS(), P = V.pk; if (!P) return; const M = svMx()[P.i], me = M[P.side], op = M[1 - P.side], pMe = me.st / (me.st + op.st), won = Math.random() < pMe;
  const tot = 9, a = won ? Math.max(5, Math.round(tot * Math.max(pMe, .56))) : Math.min(4, Math.round(tot * Math.min(pMe, .44))), b = tot - a, before = V.left;
  V.used = (V.used || []).concat(me.src); V.last = { mine: me.t, opp: op.t, a, b }; V.pk = null; V.mx = null;
  V.left = Math.max(won ? 2 : 1, Math.round(V.left * (0.56 + Math.random() * 0.1)));
  if (!won) V.done = 'out'; else if (V.day >= SV_DAYS) { V.done = 'won'; V.prize = +(SV_PRIZE / V.left).toFixed(2); S.cash = +((S.cash || 0) + V.prize).toFixed(2); try { earnAdd({ kind: 'sv', amt: V.prize, t: 'Survivor' }); } catch (e) {} } else V.day++;
  save(); try { paintWallet(); } catch (e) {}
  popOpen(`<div class="pp qfx nv qw svr"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Survivor · day ${V.done === 'won' ? SV_DAYS : won ? V.day - 1 : V.day}</span></div>
    <h2 class="nv-big sm">${V.done === 'won' ? 'You survived the week!' : won ? 'You survived!' : 'Knocked out'}</h2>
    <div class="svr-vs"><div class="${won ? 'w' : ''}"><img src="${me.src}" alt=""><b>${esc(me.t)}</b><small>Your pick</small></div><i>VS</i><div class="${won ? '' : 'w'}"><img src="${op.src}" alt=""><b>${esc(op.t)}</b></div></div>
    <div class="svr-bar"><u style="width:${Math.round(a / tot * 100)}%"></u><span>${Math.round(a / tot * 100)}%</span><span>${Math.round(b / tot * 100)}%</span></div>
    <p class="qw-o">${V.done === 'won' ? `You and ${V.left - 1} others split $${SV_PRIZE}: <b class="gold">${money(V.prize)}</b> added to your cash.` : won ? `${before.toLocaleString()} → <b class="gold">${V.left.toLocaleString()}</b> still standing · day ${V.day} pick opens now` : `${V.left.toLocaleString()} of ${SV_FIELD.toLocaleString()} still standing. Try again next week.`}</p>
    <button class="btn block nv-go" id="svOk">${won && V.done !== 'won' ? `🛡️ Make day ${V.day}’s pick` : 'Back to coin games'}</button><p class="nv-sim">Demo · results and other players are simulated · prize paid by PhotoPicks</p></div>`);
  setTimeout(() => { try { if (V.done === 'won') { cashExplosion(V.prize, { label: 'Survivor' }); rvConfetti(document.querySelector('.svr'), 120); } else if (won) rvConfetti(document.querySelector('.svr'), 50); SFX(won ? 'win' : 'lose'); } catch (e) {} }, 300);
  $('#svOk').onclick = () => { popClose(); if (won && V.done !== 'won') setTimeout(svPick, 200); else { window.__ptab = 'coins'; finalsTab(); } }; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-sv], [data-pt]'); if (!b) return; e.preventDefault();
  if (b.dataset.pt) { window.__ptab = b.dataset.pt; finalsTab(); return; } const k = b.dataset.sv, V = svS();
  if (k === 'enter') { if ((S.gems || 0) < SV_COST || V.in) return; S.gems -= SV_COST; Object.assign(V, { in: 1, day: 1, left: SV_FIELD, used: [], pk: null, mx: null, done: null }); save(); try { paintGems(); } catch (x) {} toast(`🛡️ You’re in Survivor · −${SV_COST} 🪙`); setTimeout(svPick, 250); }
  else if (k === 'pick') svPick(); else if (k === 'settle') svSettle(); else if (k === 'new') { S.sv = { wk: svWeek(), in: 0 }; save(); finalsTab(); } });
(() => { const ft = finalsTab; finalsTab = function () { const r = ft.apply(this, arguments); try { const sx = document.querySelector('#flow .sx'); if (!sx) return r; const coins = window.__ptab === 'coins', sub = sx.querySelector('.sx-sub');
    if (sub && !sx.querySelector('.pt-seg')) sub.insertAdjacentHTML('afterend', `<div class="pt-seg"><button data-pt="stable" class="${coins ? '' : 'on'}">🐎 My stable</button><button data-pt="coins" class="${coins ? 'on' : ''}">${CN()} Coin games</button></div>`);
    sx.classList.toggle('coinv', coins);
    if (coins) { if (sub) sub.textContent = 'Earn coins by voting. Play them for cash prizes.'; const seg = sx.querySelector('.pt-seg'); seg.insertAdjacentHTML('afterend', `<div id="svW">${svCard()}</div>`); const cup = document.getElementById('cupC'); if (cup) document.getElementById('svW').appendChild(cup); } } catch (e) {} return r; }; })();
function fcNotify() {""")
s = s.replace('</style>', """.cn-w{display:inline-block;vertical-align:-.14em;line-height:1}.cn-w svg.cn-ic{width:1.05em;height:1.05em;display:block}
.pt-seg{display:flex;gap:4px;margin:4px 0 14px;padding:4px;border-radius:999px;background:#EFE6D6}.pt-seg button{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;min-height:40px;border:0;border-radius:999px;background:none;font:900 .95rem Nunito,system-ui;color:#6B5B4B;cursor:pointer}.pt-seg button.on{background:#14213D;color:#F3D98B}.pt-seg .cn-ic{width:1.1em;height:1.1em}
.sx.coinv>*:not(.sx-h):not(.sx-sub):not(.pt-seg):not(#svW):not(.db-sim){display:none!important}.sx:not(.coinv) #cupC{display:none!important}#svW #cupC{display:block!important}
.sv{position:relative;overflow:hidden;margin:0 0 14px;padding:16px 16px 12px;border-radius:22px;text-align:left;color:#fff;background:radial-gradient(120% 90% at 85% 10%,#2A3E70 0%,#16244A 45%,#0E1830 100%);box-shadow:0 12px 26px -12px rgba(14,24,48,.55)}
.sv-ic{position:absolute;right:14px;top:14px;font-size:2.8rem;filter:drop-shadow(0 6px 12px rgba(160,190,255,.35))}.sv-k{margin:0 0 6px;display:inline-block;padding-bottom:3px;border-bottom:2px solid #D9AE4F;font:900 .78rem Fraunces,Georgia,serif;font-style:italic;letter-spacing:.1em;text-transform:uppercase;color:#FBF3DC}
.sv h3{margin:0 0 4px;max-width:80%;font:900 1.45rem/1.1 Fraunces,Georgia,serif;color:#fff}.sv-s{margin:0 0 10px;max-width:84%;font:600 .86rem/1.35 Nunito,system-ui;color:#DDE3F0}.sv-s b{color:#F3D98B}.sv-f{margin:8px 0 0;text-align:center;font:700 .74rem Nunito,system-ui;color:#B9C3DA}
html body #flow .sx .btn.sv-b{width:100%!important;min-height:48px!important;margin:0!important;border-radius:999px!important;font:900 1.02rem Nunito,system-ui!important}html body #flow .sx .btn.sv-b.off{background:#3A4766!important;color:#B9C3DA!important}
.sv-dots{display:flex;gap:6px;margin:0 0 12px}.sv-dots i{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.15)}.sv-dots i.on{background:linear-gradient(90deg,#8CC79A,#2F7A3F)}
.sv-pk{display:flex;align-items:center;gap:10px;padding:10px;border-radius:14px;background:rgba(255,255,255,.08)}.sv-pk img{width:48px;height:48px;border-radius:10px;object-fit:cover;box-shadow:0 0 0 2px #D9AE4F}.sv-pk b{display:block;font:900 .95rem Nunito,system-ui}.sv-pk small{font:600 .78rem Nunito,system-ui;color:#C9D3E6}
.sv-demo{display:block;margin:8px auto 0;color:#C9D3E6!important;font:700 .8rem Nunito,system-ui}
.svm{display:grid;gap:8px;margin:10px 0 12px}.svm-r{display:flex;align-items:center;gap:6px}.svm-x{flex:none;font:900 .78rem Fraunces,Georgia,serif;color:#F3D98B}
.svm-p{position:relative;flex:1;display:flex;align-items:center;gap:8px;padding:6px;border:0;border-radius:12px;background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.18);color:#fff;text-align:left;cursor:pointer}.svm-p img{width:44px;height:44px;border-radius:8px;object-fit:cover;flex:none}.svm-p span{font:800 .8rem/1.2 Nunito,system-ui}
.svm-p.on{background:rgba(217,174,79,.25);box-shadow:inset 0 0 0 2.5px #F3D98B}.svm-p.used{opacity:.35}.svm-p em{position:absolute;right:6px;top:4px;font:900 .6rem Nunito,system-ui;font-style:normal;color:#FFB4A8}
.svr-vs{display:flex;align-items:center;justify-content:center;gap:10px;margin:10px 0}.svr-vs div{text-align:center;opacity:.6}.svr-vs div.w{opacity:1}.svr-vs img{width:110px;height:110px;object-fit:cover;border-radius:14px;border:3px solid rgba(255,255,255,.25)}.svr-vs div.w img{border-color:#F3D98B}.svr-vs b{display:block;margin-top:4px;font:800 .85rem Nunito,system-ui}.svr-vs small{font:700 .72rem Nunito,system-ui;color:#F3D98B}.svr-vs i{font-style:normal;font:900 .9rem Fraunces,Georgia,serif;color:#F3D98B}
.svr-bar{position:relative;height:26px;margin:6px 0 10px;border-radius:13px;background:rgba(255,255,255,.15);overflow:hidden}.svr-bar u{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#F3D98B,#D9AE4F)}.svr-bar span{position:relative;z-index:1;display:inline-block;width:50%;line-height:26px;font:900 .8rem Nunito,system-ui;color:#14213D;padding:0 10px}.svr-bar span+span{text-align:right;color:#fff}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v235 ok')
