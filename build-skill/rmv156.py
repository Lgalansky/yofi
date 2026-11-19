# Real Money build, step 159 (after rmv155.py): free coin predictions on other players' Final duels.
#  - Every ~8 votes (when your own duel isn't live) a slim card appears above the pair: "🔮 Call a live duel · free ·
#    +20 🟡 if you're right" with the two finalists. Tap one; the result lands ~20 s later in the card.
#  - Coins only, never cash: cash stays with the photo owners. You don't judge a duel you've called.
#  - Ignored cards go away after 10 votes. Simulated: the duel and its result. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
s = s.replace("function fcNotify() {", r"""const PR_COIN = 20, PR_MS = 20000;
function prNew() { const ks = [...new Set(SEED.filter(x => x.src).map(finCatOf).filter(Boolean))], k = ks[Math.floor(Math.random() * ks.length)], L = ppShuffle(SEED.filter(x => x.src && finCatOf(x) === k), Math.random);
  if (L.length < 2) return; S.pr = { k, a: { src: L[0].src, t: L[0].title || 'Photo' }, b: { src: L[1].src, t: L[1].title || 'Photo' }, n: 0, pick: null }; save(); }
function prHTML() { const P = S.pr; if (!P) return ''; const c = (o, i) => `<button class="dp-o ${P.pick === i ? 'on' : ''} ${P.res != null && P.res === i ? 'win' : ''}" data-prp="${i}" ${P.pick != null ? 'disabled' : ''}><img src="${o.src}" alt=""><small>${esc(o.t)}</small></button>`;
  let ft; if (P.res != null) { const ok = P.res === P.pick, w = P.res ? P.b : P.a; ft = ok ? `<b class="ok">✅ You called it! “${esc(w.t)}” won ${P.sc} · +${PR_COIN} 🟡</b>` : `<b class="no">✕ “${esc(w.t)}” won ${P.sc} · next call soon</b>`; }
  else if (P.pick != null) ft = `⏱ Result in <b id="prT">${Math.max(1, Math.ceil((PR_MS - (Date.now() - P.at)) / 1000))}s</b> · you don’t judge a duel you’ve called`;
  else ft = `Tap who wins · the crowd decides`;
  return `<div class="dpr" id="prC"><p class="dp-h">🔮 <b>Call a live duel</b> · ${esc(showName(P.k))} · free · <em>+${PR_COIN} 🟡</em> if you’re right</p>
    <div class="dp-vs">${c(P.a, 0)}<span>VS</span>${c(P.b, 1)}</div><p class="dp-f">${ft}</p><p class="dp-sim">Prototype: other players’ duels are simulated</p></div>`; }
function prPaint() { const e = document.getElementById('prC'); if (S.pr && e) e.outerHTML = prHTML(); else if (S.pr && !e) { const jc = document.getElementById('jcard'); if (jc) jc.insertAdjacentHTML('beforebegin', prHTML()); } else if (!S.pr && e) e.remove(); }
(() => { const rj = renderJudge; renderJudge = function () { const r = rj.apply(this, arguments); try { if (S.pr && !(S.pr.res != null && Date.now() - S.pr.done > 5000)) prPaint(); } catch (e) {} return r; }; })();
(() => { const cf = callFx; callFx = function () { const r = cf.apply(this, arguments); try {
  if (S.pr && S.pr.pick == null && ++S.pr.n >= 10) { S.pr = null; save(); prPaint(); }
  else if (!S.pr && !duLive() && (S.prN = (S.prN || 0) + 1) >= 8) { S.prN = 0; prNew(); } } catch (e) {} return r; }; })();
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-prp]'); if (!b || !S.pr || S.pr.pick != null) return; e.preventDefault();
  S.pr.pick = +b.dataset.prp; S.pr.at = Date.now(); save(); prPaint(); });
setInterval(() => { try { const P = S && S.pr; if (!P || P.pick == null) return; const t = document.getElementById('prT');
  if (P.res == null) { if (Date.now() - P.at < PR_MS) { if (t) t.textContent = Math.max(1, Math.ceil((PR_MS - (Date.now() - P.at)) / 1000)) + 's'; return; }
    P.res = Math.random() < .5 ? 0 : 1; const w = 8 + Math.floor(Math.random() * 3), l = 15 - w; P.sc = `${w}–${l}`; P.done = Date.now();
    if (P.res === P.pick) { S.gems = (S.gems || 0) + PR_COIN; try { paintGems(); } catch (e) {} } save(); prPaint();
    const c = document.getElementById('prC'); if (c && P.res === P.pick) { c.classList.add('hit'); try { rvConfetti(c, 24); } catch (e) {} }
  } else if (Date.now() - P.done > 6000) { S.pr = null; S.prN = 0; save(); const c = document.getElementById('prC'); if (c) { c.classList.add('bye'); setTimeout(() => c.remove(), 350); } } } catch (e) {} }, 1000);
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .dpr{margin:6px 2px 8px;padding:8px 10px 6px;border-radius:14px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #D9AE4F;text-align:left;animation:qmFl .35s ease-out both;transition:opacity .3s}
.dpr.bye{opacity:0}.dpr.hit{box-shadow:inset 0 0 0 2px #2F6B3F;background:#F1F6EC}
.dp-h{margin:0 0 6px;font:700 .76rem/1.3 Nunito,system-ui;color:#5B4A3F}.dp-h b{color:#14213D}.dp-h em{font-style:normal;font-weight:900;color:#9A6B12}
.dp-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center}.dp-vs>span{font:900 .8rem Fraunces,Georgia,serif;color:#fff;background:#14213D;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center}
html body .dp-o{display:flex;align-items:center;gap:7px;padding:4px;border:0;border-radius:11px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;cursor:pointer;min-width:0;font:inherit;color:#14213D}
.dp-o img{width:40px;height:40px;border-radius:8px;object-fit:cover;flex:none}.dp-o small{font:800 .72rem/1.2 Nunito,system-ui;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left}
.dp-o:disabled{cursor:default;opacity:.55}.dp-o.on{opacity:1;box-shadow:inset 0 0 0 2.5px #14213D}.dp-o.win{opacity:1;box-shadow:inset 0 0 0 2.5px #2F6B3F;background:#F1F6EC}
.dp-f{margin:6px 0 0;font:700 .74rem Nunito,system-ui;color:#3D4A5C;text-align:center}.dp-f b{color:#14213D}.dp-f b.ok{color:#2F6B3F}.dp-f b.no{color:#A6402F}
.dp-sim{margin:2px 0 0;font:600 .6rem Nunito,system-ui;color:#A89C8C;text-align:right}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v156 ok')
# pass 2: card sits under the round bar (full width), not inside the pair row
s = open(d + 'yofi-real.html').read()
RA("else if (S.pr && !e) { const jc = document.getElementById('jcard'); if (jc) jc.insertAdjacentHTML('beforebegin', prHTML()); }",
   "else if (S.pr && !e) { const top = document.getElementById('vrTop'); if (top) top.insertAdjacentHTML('afterend', prHTML()); }")
s = s.replace('</style>', """html body .dpr{display:block;width:auto;flex:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v156 pass2 ok')
# pass 3: one extra card at a time above the pair
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #judge:has(.dpr) .vr-stake{display:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v156 pass3 ok')
