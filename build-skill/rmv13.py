# Real Money build, step 16 (after rmv12.py): design pass from the user's mock-ups.
#  - Qualifier pick: "Predict the top 3", group chip, prize chips, bigger 3+2 photos, 1st/2nd/3rd slots, "Choose 3 photos · Free".
#  - Qualifier result: "No exact matches" style headline, crowd's top 3 vs your picks with labels under each photo.
#  - Finalists card: big prize pool box, players + countdown, "Explore the finalists".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("function gateOpen(real, tk) {", "function gateOpenOld(real, tk) {")
RA("function gateResult(G, picks, real, tk) {", "function gateResultOld(G, picks, real, tk) {")
s = s.replace("function fcNotify() {", r"""const GQ_ORD = ['1st', '2nd', '3rd'];
function gateOpen() { const G = gateGame(), y = isYoungW(), keep = y ? 'Keep judging' : 'Keep voting', fin = raceName(G.ns); let picks = [];
  const draw = () => { const n = picks.length;
    popOpen(`<div class="pp gq"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🎀 Qualifiers · ${fin} ${esc(showName(ppGame(G.ns).k))}</p>
      <h2 class="pp-h">Predict the top 3</h2><span class="gq-g">Group ${G.gi + 1} of 3</span>
      <p class="gq-m">Match the ${y ? 'judges’' : 'crowd’s'} ranking to win coins.</p>
      <div class="gq-pz"><span>3 correct · <b>${GATE_COINS[3]} 🟡</b></span><span>2 correct · <b>${GATE_COINS[2]} 🟡</b></span></div><p class="gq-n">Only exact positions count.</p>
      <div class="gq-ph">${G.ph.map((p, i) => { const k = picks.indexOf(i); return `<button class="gq-t ${k >= 0 ? 'on' : ''}" data-pp="${i}" aria-label="Photo ${i + 1}"><img src="${p.src}" alt="">${k >= 0 ? `<i>${PP_MED[k]}</i>` : ''}</button>`; }).join('')}</div>
      <p class="gq-hint">${n < 3 ? `Tap your <b>${GQ_ORD[n]} place</b> photo` : 'Your top 3 is set. Tap a photo to change it.'}</p>
      <div class="gq-sl">${[0, 1, 2].map(k => `<button class="${k === n ? 'cur' : ''} ${picks[k] != null ? 'set' : ''}" data-gsl="${k}">${picks[k] != null ? `<img src="${G.ph[picks[k]].src}" alt="">` : ''}<b>${GQ_ORD[k]}</b></button>`).join('')}</div>
      <button class="btn block pc-go ${n < 3 ? 'gq-off' : ''}" id="gtGo">${n < 3 ? `Choose ${3 - n} photo${3 - n === 1 ? '' : 's'} · Free` : '🎀 Lock in my top 3 · Free'}</button>
      <p class="gq-n">The ${y ? 'judges’' : 'crowd’s'} top 2 go through to the ${fin} Final.</p>
      <div style="text-align:center"><button class="link pc-later" id="gtNo">${keep}</button></div></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, k = picks.indexOf(i); if (k >= 0) picks.splice(k, 1); else if (picks.length < 3) picks.push(i); draw(); });
    document.querySelectorAll('#coach [data-gsl]').forEach(b => b.onclick = () => { const k = +b.dataset.gsl; if (picks[k] != null) { picks.splice(k, 1); draw(); } });
    $('#gtNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#gtGo').onclick = () => { if (picks.length < 3) { toast(`Pick your top 3 first · ${3 - picks.length} to go`); return; } gateResult(G, picks); }; };
  draw(); }
function gateResult(G, picks) { const y = isYoungW(), top = G.ord.slice(0, 3), right = picks.filter((p, i) => top[i] === p).length, pay = GATE_COINS[right], fin = raceName(G.ns);
  S.gateI = (S.gateI || 0) + 1; S.gateN = (S.gateN || 0) + 1; if (pay) { S.gems = (S.gems || 0) + pay; setTimeout(paintGems, 300); } save();
  const nm = j => `“${esc(G.ph[j].t || 'Untitled')}”`, tag = (p, i) => top[i] === p ? '<em class="ok">✓ Exact</em>' : top.includes(p) ? `<em class="mid">Placed ${GQ_ORD[top.indexOf(p)]}</em>` : '<em>Not in top 3</em>';
  popOpen(`<div class="pp gq"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🎀 Group ${G.gi + 1} of 3 · results</p>
    <h2 class="pp-h">${right === 3 ? 'Perfect! 3 exact matches' : right === 2 ? '2 exact matches!' : right === 1 ? '1 exact match' : 'No exact matches'}</h2>
    <p class="gq-m">${right} of 3 in the correct position${pay ? ` · <b>+${pay} 🟡</b>` : ''}</p>
    <div class="gq-cmp"><span></span>${GQ_ORD.map(o => `<b class="gq-o">${o}</b>`).join('')}
      <small>${y ? 'Judges’' : 'Crowd’s'}<br>top 3</small>${top.map((p, i) => `<figure><img src="${G.ph[p].src}" alt="">${i < 2 ? '<em class="ok">Qualified</em>' : '<em>&nbsp;</em>'}</figure>`).join('')}
      <small>Your<br>picks</small>${picks.map((p, i) => `<figure><img src="${G.ph[p].src}" alt="">${tag(p, i)}</figure>`).join('')}</div>
    <p class="gq-q">${nm(top[0])} and ${nm(top[1])} go through to the ${fin} Final.</p>
    ${gtUpsell()}
    <div style="text-align:center"><button class="link pc-later" id="gtNo">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  if (pay) setTimeout(() => gemExplosion(pay, { label: 'Qualifier win' }), 400);
  if ($('#gtFin')) $('#gtFin').onclick = () => { popClose(); setTimeout(ppOpen, 250); };
  $('#gtNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
function fcNotify() {""", 1)

# Finalists card
RA("""<p class="pp-k">🎀 Finalists</p><h2 class="pp-h">The ${raceName(cur)} Final · ${esc(showName(g.k))}</h2>
    <p class="pp-m"><b>${ppPool(g.players)}</b> pool · ${g.players} players · <b class="rc-tl">${tLeft(g.end)}</b> left</p>""",
   """<p class="pp-k">🎀 The ${raceName(cur)} Final</p><h2 class="pp-h">${esc(showName(g.k))}</h2>
    <div class="rc-pool"><b>${ppPool(g.players)}</b><span>Prize pool</span></div><p class="rc-meta">${g.players} players · <b class="rc-tl">${tLeft(g.end)}</b> left</p><p class="rc-ex">Explore the finalists</p>""")
RA('<p class="rc-sec">Next shows</p>', '<p class="rc-sec">Next Finals</p>')
RA("Photos need ${FR_MIN}+ · entry is free", "Photos need ${SHOW_MIN}+ · entry is free")
RA("in the gates` : ''}", "in the qualifiers` : ''}")

s = s.replace('</style>', """.gq .pp-h{margin-bottom:4px}.gq-g{display:inline-block;font-size:.72rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;padding:3px 12px;border-radius:999px;margin:0 0 6px}
.gq-m{margin:2px 0 8px;font-size:.92rem}.gq-pz{display:flex;justify-content:center;border-radius:999px;margin:0 auto 4px;max-width:330px;overflow:hidden}.gq-pz span{flex:1;padding:7px 6px;font-size:.84rem}.gq-pz span+span{border-left:1px solid rgba(127,127,127,.35)}
.gq-n{font-size:.76rem;opacity:.8;margin:2px 0 8px}.gq-ph{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:6px 0 4px}.gq-t{flex:0 0 calc(33.33% - 6px);padding:0;border:0;background:none;border-radius:14px;position:relative;cursor:pointer;aspect-ratio:1/1;overflow:hidden}
.gq-t img{width:100%;height:100%;object-fit:cover;display:block;border-radius:14px}.gq-t.on{box-shadow:0 0 0 3px #E2A21C}.gq-t i{position:absolute;right:4px;top:4px;font-style:normal;font-size:1.5rem;filter:drop-shadow(0 1px 3px rgba(0,0,0,.45))}
.gq-hint{margin:6px auto 6px;padding:7px 10px;border-radius:999px;font-weight:800;font-size:.92rem;max-width:340px}.gq-sl{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 10px}
.gq-sl button{position:relative;height:54px;border-radius:12px;border:1.5px solid rgba(127,127,127,.35);background:none;color:inherit;font:inherit;font-weight:800;overflow:hidden;padding:0;cursor:pointer}.gq-sl button.cur{border:2px solid #E2A21C}.gq-sl img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}.gq-sl b{position:relative}
.gq-off{opacity:.55;filter:grayscale(.6)}.gq-cmp{display:grid;grid-template-columns:54px repeat(3,1fr);gap:6px 8px;align-items:center;margin:6px 0 8px;text-align:center}.gq-cmp small{font-size:.66rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase;text-align:left;opacity:.8;line-height:1.25}
.gq-o{justify-self:center;font-size:.8rem;padding:2px 12px;border-radius:999px}.gq-cmp figure{margin:0}.gq-cmp img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:12px;display:block}.gq-cmp em{display:block;font-style:normal;font-size:.72rem;margin-top:4px;opacity:.85}.gq-cmp em.ok,.gq-cmp em.mid{font-weight:800;opacity:1}
.gq-q{font-weight:800;margin:4px 0 10px;padding-top:10px;border-top:1px solid rgba(127,127,127,.25)}
.rc-pool{border-radius:18px;padding:12px 10px 10px;margin:6px auto 4px;max-width:300px}.rc-pool b{display:block;font-size:2.6rem;line-height:1;font-weight:900}.rc-pool span{font-weight:800}.rc-meta{margin:6px 0 8px}.rc-ex{font-weight:900;font-size:1.05rem;margin:10px 0 6px;padding-top:10px;border-top:1px solid rgba(127,127,127,.25)}
html:not(.yg) .gq-g,html:not(.yg) .gq-hint{background:#E6F0DF;color:#2F6B3F}html:not(.yg) .gq-pz{background:#FFF3D6;box-shadow:inset 0 0 0 1.5px #E8C46A;color:#2B2320}html:not(.yg) .gq-o{background:#FFF0C7;color:#2B2320}html:not(.yg) .gq-cmp em.ok{color:#2F6B3F}html:not(.yg) .gq-cmp em.mid{color:#C27A0E}html:not(.yg) .rc-pool{background:#E6F0DF;color:#2F6B3F}
html.yg .gq-g,html.yg .gq-hint{background:#10301F;color:#7BE3B0}html.yg .gq-pz{background:#2A2208;box-shadow:inset 0 0 0 1.5px #F5C342;color:#fff}html.yg .gq-o{background:#2A2208;color:#F5C342}html.yg .gq-cmp em.ok{color:#21C77A}html.yg .gq-cmp em.mid{color:#F5C342}html.yg .rc-pool{background:#10301F;color:#21C77A}
</style>""", 1)
RA("🎟️ Free $1 pick in the ${nm} Final · ${FREE_BET_COINS} 🟡</button>", "🎟️ Free $1 Final pick · ${FREE_BET_COINS} 🟡</button>")
RA("💵 Pick the ${nm} Final for real · from $1</button>", "💵 Final pick for real · from $1</button>")
s = s.replace('.gq-sl button{position:relative;height:54px;border-radius:12px;border:1.5px solid rgba(127,127,127,.35)', '.gq-sl button{position:relative;height:54px;border-radius:12px;border:1.5px solid rgba(127,127,127,.5)', 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v13 ok')
