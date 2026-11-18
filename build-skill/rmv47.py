# Real Money build, step 50 (after rmv46.py): suspense and hero moments.
#  - Before qualifier and Final results: "Counting the votes…" with live vote bars, then 3rd, 2nd, 1st revealed one by one
#    (medal drops, your pick for that place shown: "✓ Spot on!" or "You picked …"). Skip button.
#  - Wins get a hero screen first: confetti, big "+50 COINS" / "YOU WON $8.25", then the results.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("function gateResult(G, picks) {", "function gateResultShow(G, picks) {")
RA("function ppResult(e) {", "function ppResultShow(e) {")
s = s.replace("function fcNotify() {", r"""const RV_ORD = ['1st', '2nd', '3rd'], RV_MED = ['🥇', '🥈', '🥉'];
function rvConfetti(el, n) { for (let i = 0; i < (n || 40); i++) { const c = document.createElement('i'); c.className = 'rv-cf'; c.style.left = Math.random() * 100 + '%'; c.style.background = ['#F2B21E', '#2F6B3F', '#E0457B', '#2D4E86', '#F7C9A0'][i % 5]; c.style.animationDelay = (Math.random() * .6).toFixed(2) + 's'; c.style.transform = `rotate(${Math.random() * 360}deg)`; el.appendChild(c); } }
function revealSeq(o, done) { const { ph, ord, picks, kicker, title } = o; let stop = false, timers = [];
  const fin = () => { if (stop) return; stop = true; timers.forEach(clearTimeout); done(); }, at = (ms, f) => timers.push(setTimeout(() => { if (!stop) f(); }, ms));
  popOpen(`<div class="pp rv"><p class="pp-k">${kicker}</p><h2 class="rv-h" id="rvH">Counting the votes…</h2><p class="rv-s" id="rvS">${title}</p>
    <div class="rv-bars">${ph.map((p, i) => `<div class="rv-b"><img src="${p.src}" alt=""><span><i style="--w:${(30 + Math.random() * 60).toFixed(0)}%"></i></span>${picks.includes(i) ? `<em>${RV_MED[picks.indexOf(i)]}</em>` : ''}</div>`).join('')}</div>
    <div class="rv-pod" id="rvPod">${[2, 1, 0].map(k => `<div class="rv-slot" data-k="${k}"><span class="rv-q">?</span><b>${RV_MED[k]} ${RV_ORD[k]}</b></div>`).join('')}</div>
    <p class="rv-me" id="rvMe">&nbsp;</p><div style="text-align:center"><button class="link rv-skip" id="rvSkip">Skip ›</button></div></div>`);
  $('#rvSkip').onclick = fin;
  [2, 1, 0].forEach((k, n) => at(1900 + n * 1300, () => { const el = document.querySelector(`#rvPod [data-k="${k}"]`); if (!el) return; const p = ph[ord[k]], hit = picks[k] === ord[k];
    if (n === 0) { $('#rvH').textContent = 'And the results are…'; document.querySelector('.rv-bars').classList.add('done'); }
    el.innerHTML = `<img src="${p.src}" alt=""><b>${RV_MED[k]} ${RV_ORD[k]}</b>`; el.classList.add('on', hit ? 'hit' : 'miss');
    $('#rvMe').innerHTML = hit ? `<b class="ok">✓ Spot on!</b> Your ${RV_ORD[k]} pick` : picks[k] != null ? `You picked <b>“${esc(ph[picks[k]].t || 'another photo')}”</b> for ${RV_ORD[k]}` : '&nbsp;';
    if (hit) { el.classList.add('pop'); rvConfetti(el, 14); } }));
  at(1900 + 3 * 1300 + 700, fin); }
function heroWin(big, sub, done) { const c = $('#coach');
  popOpen(`<div class="pp rvw"><p class="rvw-k">🎉 Winner!</p><b class="rvw-amt">${big}</b><p class="rvw-s">${sub}</p><button class="btn block rvw-go" id="rvwGo">See results</button></div>`);
  rvConfetti(document.querySelector('.rvw'), 70); let gone = false; const go = () => { if (gone) return; gone = true; done(); }; $('#rvwGo').onclick = go; setTimeout(go, 3600); }
function gateResult(G, picks) { const top = G.ord.slice(0, 3), right = picks.filter((p, i) => top[i] === p).length, pay = GATE_COINS[right];
  revealSeq({ ph: G.ph, ord: G.ord, picks, kicker: `Group ${G.gi + 1} of 3 · qualifier`, title: `${isYoungW() ? 'Judges' : 'The crowd'} decide who goes through` },
    () => pay ? heroWin(`+${pay} coins`, `${right} of 3 in the exact spot`, () => gateResultShow(G, picks)) : gateResultShow(G, picks)); }
function ppResult(e) { if (e.__rv) return; e.__rv = 1; const g = ppGame(e.sl), TR = ppTiers(e, g), prize = TR.prize;
  revealSeq({ ph: g.ph, ord: g.ord, picks: e.picks, kicker: `${raceName(g.sl)} Final · ${esc(showName(g.k))}`, title: `${ppPool(g.players)} prize pool · ${g.players} players` },
    () => prize ? heroWin(`You won ${money(prize)}`, `${TR.mine.lab} · real cash`, () => ppResultShow(e)) : ppResultShow(e)); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.rv{text-align:center;min-height:430px;padding:0 4px}html .rv,html .rv .rv-s,html .rv .rv-me,html .rv .rv-slot b{color:#2B2320!important;-webkit-text-fill-color:#2B2320}html .rv .rv-me .ok{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}html .rvw .rvw-s{color:#2B2320!important}.rv .pp-k{color:#2F6B3F}.rv-h{font:800 1.9rem/1.1 Fraunces,Georgia,serif;margin:4px 0 2px}.rv-s{margin:0 0 12px;font-size:.92rem;opacity:.85}
.rv-bars{display:flex;flex-direction:column;gap:6px;margin:0 0 14px;transition:opacity .4s,max-height .5s;max-height:420px;overflow:hidden}.rv-bars.done{opacity:0;max-height:0;margin:0}
.rv-b{display:grid;grid-template-columns:44px 1fr 24px;gap:8px;align-items:center}.rv-b img{width:44px;height:44px;object-fit:cover;border-radius:9px}.rv-b span{height:12px;border-radius:6px;background:#EEE6D8;overflow:hidden}
.rv-b i{display:block;height:100%;width:var(--w);background:linear-gradient(90deg,#E2A21C,#F2C14E);border-radius:6px;animation:rvGrow 1.8s ease-in-out infinite alternate}@keyframes rvGrow{from{width:8%}to{width:var(--w)}}.rv-b em{font-style:normal}
.rv-pod{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;align-items:end}.rv-slot{position:relative;border-radius:14px;background:#F3EDE2;aspect-ratio:1/1.15;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;overflow:hidden;box-shadow:inset 0 0 0 1.5px #E2D3BC}
.rv-slot .rv-q{font:900 2.4rem Fraunces,Georgia,serif;color:#C9B89C}.rv-slot b{font:800 .95rem Fraunces,Georgia,serif}.rv-slot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.rv-slot.on b{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);background:rgba(255,255,255,.92);padding:2px 10px;border-radius:999px;white-space:nowrap}
.rv-slot.on{animation:rvDrop .55s cubic-bezier(.2,1.5,.4,1)}@keyframes rvDrop{from{transform:translateY(-30px) scale(.8);opacity:0}to{transform:none;opacity:1}}.rv-slot.hit{box-shadow:0 0 0 3px #2F6B3F,0 0 18px rgba(47,107,63,.5)}.rv-slot.miss{box-shadow:inset 0 0 0 1.5px #E2D3BC}
.rv-me{min-height:1.4em;margin:12px 0 4px;font-size:.98rem}.rv-me .ok{color:#2F6B3F}.rv-skip{font-weight:800;color:#2F6B3F!important}
.rv-cf{position:absolute;top:-10px;width:8px;height:12px;border-radius:2px;animation:rvFall 1.6s ease-in forwards;pointer-events:none;z-index:3}@keyframes rvFall{to{top:110%;opacity:.2}}
.rvw{position:relative;overflow:hidden;text-align:center;padding:38px 16px 22px!important;background:radial-gradient(circle at 50% 30%,#FFF3C4,#FBF3EA 70%)}.rvw-k{font:800 1.3rem Fraunces,Georgia,serif;margin:0;color:#7A1638}
.rvw-amt{display:block;font:900 3.4rem/1.05 Fraunces,Georgia,serif;color:#2F6B3F;margin:10px 0 6px;animation:rvPop .7s cubic-bezier(.2,1.6,.4,1)}@keyframes rvPop{from{transform:scale(.3);opacity:0}to{transform:none;opacity:1}}.rvw-s{margin:0 0 18px;font-size:1rem}
html .rvw .btn.rvw-go{background:#24563A!important;color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v47 ok')
