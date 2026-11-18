# Real Money build, step 80 (after rmv76.py): the Tournaments tab becomes a Finals tab.
#  The old tab listed Freerolls, a $2 Crowd Championship, $1 knockouts and jackpots: a second, older product.
#  Finals tab: Live now (pool, ticking countdown, the 6 finalists, green "Pick the Final · from $2", navy free pick or
#  "View your pick"), Coming up (next 3 Finals by category with pools; tap to enter a photo), Your picks (live and settled),
#  Recent results (winner photo, pool, your result), and a short "How Finals work".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("<span>Tournaments</span></button>", "<span>Finals</span></button>")
RA("const T = { segCompete: 'Competitions'", "const T = { segCompete: 'Finals'")
RA("segGallery: 'Friends'", "segGallery: 'Gallery'")
s = s.replace("function fcNotify() {", r"""function finalsTab() { const cur = ppSlot(), g = ppGame(cur), e = (S.pp || {})[cur], cash = isCash(), y = isYoungW(), mm = r => `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}`;
  const pool = sl => ppPool(ppGame(sl).players), freeOk = !cash && fqLeft() && (S.gems || 0) >= FREE_BET_COINS;
  const mine = Object.values(S.pp || {}).sort((a, b) => b.sl - a.sl).slice(0, 4);
  const res = x => x.done ? (x.prize ? `<em class="fn-w">Won ${money(x.prize)}</em>` : '<em>No win</em>') : '<em class="fn-l">● Live</em>';
  openFlow(`<div class="fnx"><h1 class="fn-h">Finals</h1><p class="fn-s">A new Final every hour. Pick the top 3 for real cash.</p>
    <div class="fn-live"><div class="fn-top"><span class="fn-k">● Live now · ${raceName(cur)} Final</span><b class="fn-cat">${SHOW_IC[g.k] || '🎀'} ${esc(showName(g.k))}</b></div>
      <div class="lk-row"><div class="lk-pz"><small>Cash prize pool</small><b>${ppPool(g.players)}</b><span>${g.players} players</span></div><div class="lk-cd"><small>Closes in</small><b class="rb-cd" data-due="${g.end}">${mm(Math.max(0, g.end - Date.now()))}</b><span>${raceName(cur)} Final</span></div></div>
      <div class="fn-ph">${g.ph.map(p => `<img src="${p.src}" alt="">`).join('')}</div>
      ${e ? `<button class="btn block fn-nv" id="fnMine">🎟️ View your pick · ${e.free ? 'free' : money(e.stake || 2)}</button>` : `<button class="btn block fn-cash" id="fnCash">💵 Pick the Final · from $2</button>${freeOk ? `<button class="btn block fn-nv" id="fnFree">🎟️ Free pick · ${FREE_BET_COINS} coins</button>` : ''}`}
      <div style="text-align:center"><button class="link fn-lk" id="fnCard">See the finalists ›</button></div></div>
    <h2 class="fn-h2">Coming up</h2><div class="g4-fin fn-up">${[1, 2, 3].map(k => { const sl = cur + k, G = ppGame(sl); return `<button data-fnk="${G.k}"><img src="${(G.ph[0] || {}).src}" alt=""><span><b>${esc(showName(G.k))}</b><small>${raceName(sl)} Final</small></span><span class="g4-amt"><b>${pool(sl)}</b><small>Enter a photo ›</small></span></button>`; }).join('')}</div>
    ${mine.length ? `<h2 class="fn-h2">Your picks</h2><div class="fn-my">${mine.map(x => { const G = ppGame(x.sl); return `<div><span class="fn-th">${x.picks.slice(0, 3).map(p => `<img src="${(G.ph[p] || {}).src}" alt="">`).join('')}</span><span class="fn-t"><b>${raceName(x.sl)} ${esc(showName(G.k))}</b><small>${x.free ? 'Free pick' : money(x.stake || 2) + ' pick'}</small></span>${res(x)}</div>`; }).join('')}</div>` : ''}
    <h2 class="fn-h2">Recent results</h2><div class="fn-my">${[1, 2, 3].map(k => { const sl = cur - k, G = ppGame(sl), w = G.ph[G.ord[0]], x = (S.pp || {})[sl]; return `<div><img class="fn-w1" src="${w.src}" alt=""><span class="fn-t"><b>${raceName(sl)} ${esc(showName(G.k))}</b><small>🏆 “${esc(w.t)}” · ${ppPool(G.players)} pool</small></span>${x ? res(x) : '<em>—</em>'}</div>`; }).join('')}</div>
    <details class="g4-how2 fn-how"><summary>How Finals work</summary><p>Every hour, 6 photos that came through the qualifiers race in a Final. ${y ? 'Judges' : 'Voters'} decide the order. Pick the top 3: win with 1 photo in its exact spot, or 2 in the top 3. Pickers share 78% of the pool, the finalists’ creators share 10%.</p></details></div>`, false);
  $('#flow').classList.add('astab'); ['segJudge', 'segStudio', 'segGallery'].forEach(id => $('#' + id).setAttribute('aria-pressed', 'false')); $('#segCompete').setAttribute('aria-pressed', 'true'); setTimeout(() => { $('#ptitle').textContent = 'Finals'; }, 0);
  const B = $('#flowBody'), on = (id, f) => { const b = B.querySelector('#' + id); if (b) b.onclick = f; };
  on('fnMine', () => ppOpen()); on('fnCash', () => { window.__ppCash = 1; ppOpen(); }); on('fnFree', () => fqStart()); on('fnCard', () => raceCard());
  B.querySelectorAll('[data-fnk]').forEach(b => b.onclick = () => { window.__preCat = showHint(b.dataset.fnk).cats[0]; pickPhoto(true); }); }
function fcNotify() {""", 1)
s = s.replace('</script>\n</body>', "<script>try { $('#segCompete').onclick = () => finalsTab(); } catch (e) {}</script>\n</body>") if False else s
# rebind the tab after the original handler is attached
RA("$('#segCompete').onclick = () => { CX_WB = false; if (!S.user) { openSignup(() => openComps(null)); return; } if (CX.some(c => canEnter(c))) goEligible(); else openComps(null); };",
   "$('#segCompete').onclick = () => finalsTab();")
s = s.replace('</style>', """.fnx{padding:6px 2px 24px}html body .fnx .fn-h{font:800 2rem/1.1 Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:4px 0 2px}.fn-s{margin:0 0 12px}
.fn-live{background:#FBF6EE;border-radius:20px;box-shadow:inset 0 0 0 1.5px #E2C27A;padding:12px}.fn-top{text-align:center;margin:0 0 8px}.fn-k{display:block;font-weight:900;letter-spacing:.1em;text-transform:uppercase;font-size:.76rem;color:#C8102E}
html body .fnx .fn-cat{display:block;font:800 1.45rem Fraunces,Georgia,serif;color:#14213D}.fn-ph{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin:0 0 10px}.fn-ph img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px}
html body .fnx .btn.fn-cash{background:#2F6B3F!important;color:#fff!important;margin-bottom:8px}html body .fnx .btn.fn-nv{background:#1E3A6E!important;color:#fff!important;margin-bottom:8px}.fn-lk{font-weight:800}
html body .fnx .fn-h2{font:800 1.35rem Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:18px 0 8px;text-align:left}
.fn-my{display:flex;flex-direction:column;gap:8px}.fn-my>div{display:flex;align-items:center;gap:10px;background:#FBF6EE;border-radius:14px;box-shadow:inset 0 0 0 1.5px #EADCC6;padding:8px 12px 8px 8px}
.fn-th{display:flex;flex:none}.fn-th img{width:30px;height:30px;object-fit:cover;border-radius:7px;margin-right:-6px;box-shadow:0 0 0 2px #FBF6EE}.fn-w1{width:52px;height:44px;object-fit:cover;border-radius:9px;flex:none}
.fn-t{display:flex;flex-direction:column;min-width:0;flex:1;margin-left:6px;text-align:left}.fn-t b{font-size:.95rem;color:#14213D}.fn-t small{font-size:.8rem}
.fn-my em{margin-left:auto;font-style:normal;font-weight:800;font-size:.84rem;white-space:nowrap}html body .fnx .fn-my em.fn-w{color:#2F6B3F!important}html body .fnx .fn-my em.fn-l{color:#C8102E!important}.fn-how{margin-top:16px}
html body .fnx .lk-pz small,html body .fnx .lk-pz b{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}html body .fnx .lk-cd small,html body .fnx .lk-cd span{color:#DCE5F4!important;-webkit-text-fill-color:#DCE5F4}html body .fnx .lk-cd b{display:block;font:900 2.2rem/1.05 Fraunces,Georgia,serif;color:#F3D98B!important;-webkit-text-fill-color:#F3D98B;font-variant-numeric:tabular-nums}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v77 ok')
