# Real Money build, step 44 (after rmv40.py): qualifier pick + result screens from the user's mock-up.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()

i = s.index('function gateOpen() {'); j = s.index('function rmReady(p)', i)
TICKET = '<svg viewBox="0 0 48 32" width="34" height="23" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" aria-hidden="true"><path d="M5 9 L37 3 L40 11 a4.5 4.5 0 0 0 2 8.6 L44 27 L12 31 L9 23 a4.5 4.5 0 0 0-2-8.6z"/><path d="M22 8 l1.6 6 M24.6 17.5 l1.6 6" stroke-dasharray="2.5 3"/></svg>'
NEW = r"""const GQ_MED = ['🥇', '🥈', '🥉'];
function gateOpen() { const G = gateGame(), y = isYoungW(), keep = y ? 'Keep judging' : 'Keep voting', fin = raceName(G.ns), cw = y ? 'judges’' : 'crowd’s'; let picks = [];
  const draw = () => { const n = picks.length;
    popOpen(`<div class="pp gq2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">${esc(showName(ppGame(G.ns).k))}</p><span class="g2-chip">Qualifier · Group ${G.gi + 1} of 3</span>
      <h2 class="g2-h">Pick the top 3</h2><p class="g2-s">Match the ${cw} order. Win up to ${GATE_COINS[3]} coins.</p>
      <div class="g2-pz"><span>3 exact · <b>${GATE_COINS[3]} coins</b></span><span>2 exact · <b>${GATE_COINS[2]} coins</b></span></div><p class="g2-n">Only the correct positions count.</p>
      <div class="g2-ph">${G.ph.map((p, i) => { const k = picks.indexOf(i); return `<button class="g2-t ${k >= 0 ? 'on' : ''}" data-pp="${i}" aria-label="Photo ${i + 1}"><img src="${p.src}" alt="">${k >= 0 ? `<i>${GQ_MED[k]}</i>` : ''}</button>`; }).join('')}</div>
      <p class="g2-hint">${n < 3 ? `Choose your ${GQ_ORD[n]} place photo` : 'Your top 3 is set · tap a photo to change it'}</p>
      <div class="g2-sl">${[0, 1, 2].map(k => `<button class="${k === n ? 'cur' : ''} ${picks[k] != null ? 'set' : ''}" data-gsl="${k}">${picks[k] != null ? `<img src="${G.ph[picks[k]].src}" alt="">` : ''}<span>${GQ_MED[k]} ${GQ_ORD[k]}</span></button>`).join('')}</div>
      <button class="btn block g2-go ${n < 3 ? 'off' : ''}" id="gtGo">${n < 3 ? 'Select 3 photos to continue' : 'Lock in my top 3'}</button>
      <p class="g2-foot">Free to play · Top 2 reach the ${fin} Final</p>
      <div style="text-align:center"><button class="link g2-link" id="gtNo">${keep}</button></div></div>`);
    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, k = picks.indexOf(i); if (k >= 0) picks.splice(k, 1); else if (picks.length < 3) picks.push(i); draw(); });
    document.querySelectorAll('#coach [data-gsl]').forEach(b => b.onclick = () => { const k = +b.dataset.gsl; if (picks[k] != null) { picks.splice(k, 1); draw(); } });
    $('#gtNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    $('#gtGo').onclick = () => { if (picks.length < 3) { toast(`Pick your top 3 first · ${3 - picks.length} to go`); return; } gateResult(G, picks); }; };
  draw(); }
function g2Next() { if (S.tut === 2) return 'Your first Final pick is free'; if (isCash()) return 'From $2 · real cash prize pool';
  return fqLeft() && (S.gems || 0) >= FREE_BET_COINS ? `Free pick · ${FREE_BET_COINS} coins` : `Free pick at ${FREE_BET_COINS} coins · ${Math.max(0, FREE_BET_COINS - Math.floor(S.gems || 0))} to go`; }
function gateResult(G, picks) { const y = isYoungW(), top = G.ord.slice(0, 3), ex = picks.map((p, i) => top[i] === p), right = ex.filter(Boolean).length, pay = GATE_COINS[right], fin = raceName(G.ns), cw = y ? 'Judges’' : 'Crowd’s';
  S.gateI = (S.gateI || 0) + 1; S.gateN = (S.gateN || 0) + 1; if (pay) { S.gems = (S.gems || 0) + pay; setTimeout(paintGems, 300); } save();
  const hit = ex.map((v, i) => v ? `${GQ_ORD[i]}-place` : null).filter(Boolean),
    sub = right === 3 ? 'All three spot on!' : right === 2 ? `Your ${hit[0].replace('-place', '')} and ${hit[1]} picks were spot on.` : right === 1 ? `Your ${hit[0]} pick was spot on.` : 'None of your picks were in the right place.';
  const tag = (p, i) => top[i] === p ? '<em class="ok">✓ Exact match</em>' : top.includes(p) ? `<em class="mid">Finished ${GQ_ORD[top.indexOf(p)]}</em>` : '<em>Outside top 3</em>';
  popOpen(`<div class="pp gq2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">Group ${G.gi + 1} of 3 · results</p>
    <h2 class="g2-h">${right} of 3 matched</h2><p class="g2-s">${sub}</p>
    <span class="g2-earn ${pay ? 'won' : ''}">${pay ? `+${pay} coins earned` : `0 coins earned · 2 matches needed`}</span>
    <div class="g2-cmp"><span></span>${GQ_ORD.map((o, i) => `<b class="g2-o">${GQ_MED[i]} ${o}</b>`).join('')}
      <small class="g2-row">${cw} top 3</small>${top.map((p, i) => `<figure><img src="${G.ph[p].src}" alt="">${i < 2 ? '<em class="fin">Finalist</em>' : '<em class="no">&nbsp;</em>'}</figure>`).join('')}
      <small class="g2-row">Your picks</small>${picks.map((p, i) => `<figure class="${top[i] === p ? 'ok' : ''}"><img src="${G.ph[p].src}" alt="">${tag(p, i)}</figure>`).join('')}</div>
    <div class="g2-thru"><span>${top.slice(0, 2).map(p => `<img src="${G.ph[p].src}" alt="">`).join('')}</span><div><b>Through to the ${fin} Final</b><small>The ${cw.toLowerCase()} top 2 qualify.</small></div></div>
    <button class="btn block g2-fin" id="gtFin">""" + TICKET + r""" Pick the Final winner</button><p class="g2-foot">${g2Next()}</p>
    <div style="text-align:center"><button class="link g2-link" id="gtNo">${y ? 'Keep judging' : 'Keep voting'}</button></div></div>`);
  if (pay) setTimeout(() => gemExplosion(pay, { label: 'Qualifier win' }), 400);
  $('#gtFin').onclick = () => { popClose(); setTimeout(ppOpen, 250); };
  $('#gtNo').onclick = () => popClose(); document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
"""
s = s[:i] + NEW + s[j:]
s = s.replace('</style>', """.gq2{text-align:center}.gq2 .pp-k{color:#2F6B3F}.g2-chip{display:inline-block;background:#E6F0DF;color:#2F6B3F;font-weight:700;font-size:.86rem;padding:4px 14px;border-radius:999px;margin:2px 0 4px}
.g2-h{font:800 2.2rem/1.05 Fraunces,Georgia,serif;margin:4px 0 4px}.g2-s{margin:0 0 10px;font-size:.98rem}
.g2-pz{display:flex;border-radius:999px;background:#FFF3D6;box-shadow:inset 0 0 0 1.5px #E8C46A;overflow:hidden;margin:0 0 4px}.g2-pz span{flex:1;padding:8px 4px;font-size:.92rem}.g2-pz span+span{border-left:1.5px solid #E8C46A}
.g2-n{font-size:.78rem;opacity:.8;margin:2px 0 10px}.g2-ph{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:0 0 10px}.g2-t{flex:0 0 calc(33.33% - 6px);aspect-ratio:1/1.05;padding:0;border:0;background:none;border-radius:14px;overflow:hidden;position:relative;cursor:pointer}
.g2-t img{width:100%;height:100%;object-fit:cover;display:block}.g2-t.on{box-shadow:0 0 0 3px #E2A21C}.g2-t i{position:absolute;right:5px;top:5px;font-style:normal;font-size:1.6rem;filter:drop-shadow(0 1px 3px rgba(0,0,0,.4))}
.g2-hint{background:#E6F0DF;color:#2F6B3F;font-weight:800;border-radius:999px;padding:8px 12px;margin:0 auto 8px;max-width:340px}
.g2-sl{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 10px}html .gq2 .g2-sl button{position:relative;height:52px;border-radius:12px;border:1.5px solid #E2D3BC!important;background:#FBF6EE!important;font:inherit;font-weight:800;color:#2B2320;overflow:hidden;cursor:pointer;padding:0}
html .gq2 .g2-sl button.cur{background:#FFF3D6!important;border:2px solid #E2A21C!important}.g2-sl img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5}.g2-sl span{position:relative}
html .gq2 .btn.g2-go{background:#2F6B3F!important;color:#fff!important;font-weight:800}html .gq2 .btn.g2-go.off{background:#B9B4AE!important;color:#fff!important}
.g2-foot{font-size:.86rem;margin:6px 0 2px}.g2-link{font-weight:800;color:#2F6B3F!important}
.g2-earn{display:inline-block;background:#FFF3D6;box-shadow:inset 0 0 0 1.5px #E8C46A;border-radius:999px;padding:6px 14px;font-size:.9rem;margin:0 0 10px}.g2-earn.won{background:#E6F0DF;box-shadow:inset 0 0 0 1.5px #2F6B3F;color:#2F6B3F;font-weight:800}
.g2-cmp{display:grid;grid-template-columns:repeat(3,1fr);gap:6px 8px;text-align:center;margin:0 0 10px}.g2-cmp>span{display:none}.g2-o{font:800 1rem Fraunces,Georgia,serif}
.g2-row{grid-column:1/-1;justify-self:start;background:#EEE6D8;border-radius:999px;padding:2px 10px;font-size:.7rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase}
.g2-cmp figure{margin:0;border-radius:14px;padding:2px}.g2-cmp figure.ok{box-shadow:inset 0 0 0 2px #2F6B3F;background:#E6F0DF}.g2-cmp img{width:100%;aspect-ratio:1/.85;object-fit:cover;border-radius:12px;display:block}
.g2-cmp em{display:inline-block;font-style:normal;font-size:.74rem;margin-top:4px;padding:2px 8px;border-radius:999px;background:#EEE6D8}.g2-cmp em.no{background:none}.g2-cmp em.fin{background:#E6F0DF;color:#2F6B3F;font-weight:700}.g2-cmp em.mid{background:#FFF0C7;font-weight:700}.g2-cmp em.ok{color:#2F6B3F;font-weight:800;background:none}
.g2-thru{display:flex;align-items:center;gap:10px;background:#E6F0DF;border-radius:14px;padding:8px;margin:0 0 10px;text-align:left}.g2-thru span{display:flex;gap:6px;flex:none;padding-right:10px;border-right:1px solid rgba(47,107,63,.3)}.g2-thru img{width:58px;height:46px;object-fit:cover;border-radius:8px}
.g2-thru b{display:block;font:800 1.02rem Fraunces,Georgia,serif;color:#2F6B3F}.g2-thru small{font-size:.8rem}
html .gq2 .btn.g2-fin{background:#24563A!important;color:#fff!important;font:800 1.2rem Fraunces,Georgia,serif;display:flex;align-items:center;justify-content:center;gap:10px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v41 ok')
