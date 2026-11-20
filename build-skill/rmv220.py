# Real Money build, step 223 (after rmv219.py): fun pass.
#  - Vote verdict you can see: the line under "Which is better?" flips to "✓ You called it! +N 🪙" (green) or
#    "✗ The crowd went the other way" for a moment; coins float up from your pick.
#  - Sound + haptics (Web Audio, no files): good vote, miss, streak dot, step, 3-2-1 countdown, crowd votes in races,
#    win fanfare, loss. 🔊/🔇 toggle in the header (remembered).
#  - Races feel alive: each crowd vote for your photo pops a 👏/🔥/💛 from its lane.
#  - Landing page you can play: "Tap the photo you think the crowd picked" -> medals and crowd % reveal with a verdict,
#    then the CTA; a rotating "just won" ticker under it (demo).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
# landing: playable podium + ticker
RA("""p.innerHTML = [['pets', '1st', 'g'], ['nature', '2nd', 's'], ['garden', '3rd', 'b']].map(([k, t, c]) => `<div><img src="${lpImg(k)}" alt=""><span class="lp-ros ${c}">${t}</span></div>`).join(''); }""",
   """lpGame(p); }""")
RA("""<p class="lp-cap lp2-cap">Which photo would the crowd pick?</p>""",
   """<p class="lp-cap lp2-cap" id="lpCap">Tap the photo you think the crowd picked 👆</p><div class="lp-tick" id="lpTick"><span>🏁 @pawprincess just won $7.00 in the Pets Final</span></div>""")
RA("function fcNotify() {", r"""const SFX = (() => { let ac = null; const ctx = () => { if (S.mute) return null; try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); if (ac.state === 'suspended') ac.resume(); return ac; } catch (e) { return null; } };
  const tone = (f, t0, dur, type, vol, f2) => { const a = ctx(); if (!a) return; const o = a.createOscillator(), g = a.createGain(), t = a.currentTime + t0; o.type = type || 'sine'; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + dur);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol || .18, t + .012); g.gain.exponentialRampToValueAtTime(0.0001, t + dur); o.connect(g); g.connect(a.destination); o.start(t); o.stop(t + dur + .02); };
  const buzz = p => { try { if (!S.mute && navigator.vibrate) navigator.vibrate(p); } catch (e) {} };
  const P = { ok: () => { tone(880, 0, .12, 'triangle', .16); tone(1320, .07, .16, 'triangle', .14); buzz(15); }, no: () => { tone(220, 0, .18, 'sine', .14, 160); },
    dot: () => tone(1180, 0, .09, 'triangle', .12), step: () => { [660, 880, 1100, 1320].forEach((f, i) => tone(f, i * .07, .16, 'triangle', .15)); buzz([20, 40, 30]); },
    tick: () => tone(740, 0, .08, 'square', .07), go: () => { tone(988, 0, .25, 'square', .09); tone(1480, .02, .3, 'triangle', .1); buzz(40); },
    me: () => tone(1046, 0, .07, 'triangle', .09), them: () => tone(392, 0, .07, 'sine', .07),
    win: () => { [523, 659, 784, 1046, 1318].forEach((f, i) => tone(f, i * .1, .28, 'triangle', .16)); tone(1568, .55, .5, 'triangle', .12); buzz([30, 50, 30, 50, 60]); },
    lose: () => { [392, 330, 262].forEach((f, i) => tone(f, i * .16, .26, 'sine', .12)); }, coin: () => { tone(1568, 0, .06, 'square', .06); tone(2093, .05, .1, 'square', .06); } };
  return n => { try { P[n] && P[n](); } catch (e) {} }; })();
function sndBtn() { const f = document.querySelector('#judge .tot-h'); if (!f || f.querySelector('#sndT')) return; f.insertAdjacentHTML('beforeend', `<button id="sndT" class="snd-t" aria-label="Sound">${S.mute ? '🔇' : '🔊'}</button>`);
  document.getElementById('sndT').onclick = e => { e.stopPropagation(); S.mute = !S.mute; save(); e.currentTarget.textContent = S.mute ? '🔇' : '🔊'; if (!S.mute) SFX('ok'); }; }
setInterval(sndBtn, 800); setTimeout(sndBtn, 300); (() => { const rj = renderJudge; renderJudge = function () { const r = rj.apply(this, arguments); try { sndBtn(); } catch (e) {} return r; }; })();
(() => { const cf = callFx; callFx = function (pick, pct, agree, earn) { const g0 = S.gems || 0, k0 = S.stk || 0; const r = cf.apply(this, arguments); try { const gain = Math.round((S.gems || 0) - g0) || earn || 0, sub = document.querySelector('#judge .tot-h p');
      if (sub) { if (!sub.dataset.o) sub.dataset.o = sub.innerHTML; sub.innerHTML = agree ? `<b class="vv ok">✓ You called it!${gain > 0 ? ` +${gain} 🪙` : ''}</b>` : `<b class="vv no">✗ The crowd went the other way</b>`; sub.classList.remove('vvp'); void sub.offsetWidth; sub.classList.add('vvp'); }
      const card = document.querySelectorAll('#judge .tot-c')[pick]; if (agree && card && gain > 0) { card.insertAdjacentHTML('beforeend', `<span class="vv-fl">+${gain} 🪙</span>`); setTimeout(() => SFX('coin'), 180); }
      SFX(agree ? 'ok' : 'no'); } catch (e) {} return r; }; })();
(() => { const ps = pvStep; pvStep = function (p) { const h = ps.apply(this, arguments); try { const M = window.__pvM && window.__pvM[p.id]; if (M && M.fx && !M.snd && Date.now() - M.at < 1400) { M.snd = 1; if (M.fx === 'up') setTimeout(() => SFX('step'), 250); else if (M.fx === 'hit') setTimeout(() => SFX('dot'), 160); } } catch (e) {} return h; }; })();
(() => { const qc = qrCount; qrCount = function () { const r = qc.apply(this, arguments); try { if (document.getElementById('qrCd')) { [0, 900, 1800].forEach(t => setTimeout(() => { if (document.getElementById('qrCd')) SFX('tick'); }, t)); setTimeout(() => SFX('go'), 2700); } } catch (e) {} return r; }; })();
new MutationObserver(ms => { ms.forEach(m => { const t = m.target; if (m.attributeName !== 'class' || !t.classList || !t.classList.contains('hit') || !t.closest || !t.closest('#coach')) return; if (t.id === 'qrCA') { SFX('me');
      const em = ['👏', '🔥', '💛', '⭐', '🙌'][Math.floor(Math.random() * 5)], rail = t.querySelector('.hr-rail') || t; const hz = t.querySelector('img'); rail.insertAdjacentHTML('beforeend', `<span class="hr-pop" style="left:${hz ? hz.offsetLeft + hz.offsetWidth - 8 : 60}px;top:${hz ? hz.offsetTop - 14 : -6}px">${em}</span>`); const x = rail.querySelectorAll('.hr-pop'); if (x.length > 4) x[0].parentNode.removeChild(x[0]); } else if (t.id === 'qrCB') SFX('them'); }); })
  .observe(document.body, { attributes: true, subtree: true, attributeFilter: ['class'] });
[['qlWon', 'win'], ['qlLost', 'lose'], ['crReady', 'win'], ['cupResult', null], ['h3Done', null], ['qfResult', null]].forEach(([fn, snd]) => { try { const o = window[fn] || eval(fn); const w = function () { const r = o.apply(this, arguments); try {
      let k = snd; if (fn === 'h3Done') k = arguments[4] ? 'win' : 'lose'; if (fn === 'qfResult') { const P = arguments[0]; k = P && P.raced && P.raced.prize > 0 ? 'win' : 'lose'; } if (fn === 'cupResult') { const C = S.cup; k = C && C.res && C.res.pl <= cupWin(C.res.n) ? 'win' : 'lose'; }
      setTimeout(() => SFX(k), 250); } catch (e) {} return r; }; eval(`${fn} = w`); } catch (e) {} });
function lpGame(el) { const T = [['pets', 48], ['nature', 33], ['garden', 19]], order = [0, 1, 2].sort(() => Math.random() - .5), med = ['1st', '2nd', '3rd'], cls = ['g', 's', 'b'];
  el.innerHTML = order.map(i => `<div class="lpg" data-lpg="${i}"><img src="${lpImg(T[i][0])}" alt=""><span class="lp-ros ${cls[i]} hid">${med[i]}</span><em class="lpg-pc">${T[i][1]}%</em></div>`).join('');
  el.querySelectorAll('[data-lpg]').forEach(b => b.onclick = () => { if (el.dataset.done) return; el.dataset.done = 1; const i = +b.dataset.lpg; el.classList.add('rev'); b.classList.add('me');
    el.querySelectorAll('.lp-ros').forEach((r, n) => setTimeout(() => r.classList.remove('hid'), 150 + n * 120)); SFX(i === 0 ? 'win' : 'ok');
    const cap = document.getElementById('lpCap'); if (cap) cap.innerHTML = i === 0 ? '✓ <b>Spot on!</b> You think like the crowd. That’s how you move photos forward.' : `So close: the crowd put that one <b>${med[i]}</b>. Your eye gets sharper with every vote.`;
    try { const btn = document.querySelector('#landing .lp-btn'); if (btn) btn.classList.add('lp-pulse'); } catch (e) {} }); }
(() => { const W = [['@pawprincess', '$7.00', 'Pets Final'], ['@catlover22', '$17.50', 'Pets Final'], ['@linda.blooms', '$3.40', 'head-to-head'], ['@nana_bakes', '$30.00', 'Daily Cup'], ['@tom_frames', '$8.50', 'head-to-head'], ['@ella.travels', '$7.00', 'Nature Final']]; let i = 0;
  setInterval(() => { const t = document.getElementById('lpTick'); if (!t) return; i = (i + 1) % W.length; const w = W[i]; t.innerHTML = `<span class="in">🏁 ${w[0]} just won <b>${w[1]}</b> in the ${w[2]}</span>`; }, 3200); })();
function fcNotify() {""")
s = s.replace('</style>', """#judge .tot-h{position:relative}.snd-t{position:absolute;right:0;top:4px;z-index:2;width:32px;height:32px;padding:0;font-size:.85rem!important;border:0;border-radius:50%;background:#F4EBD6;box-shadow:inset 0 0 0 1.5px #E2D5C2;font-size:1rem;cursor:pointer}
#judge .tot-h p.vvp{animation:vvIn .35s cubic-bezier(.3,1.5,.5,1)}@keyframes vvIn{0%{transform:scale(.7);opacity:0}100%{transform:scale(1);opacity:1}}
#judge .tot-h p .vv{display:inline-block;padding:4px 14px;border-radius:999px;font:900 1rem Nunito,system-ui}#judge .tot-h p .vv.ok{background:#2F7A3F;color:#fff}#judge .tot-h p .vv.no{background:#F4E4DF;color:#9C3B2B}
.vv-fl{position:absolute;left:50%;top:40%;z-index:8;transform:translateX(-50%);padding:6px 14px;border-radius:999px;background:linear-gradient(180deg,#F3D98B,#D9AE4F);color:#14213D;font:900 1.3rem Nunito,system-ui;white-space:nowrap;box-shadow:0 6px 16px rgba(0,0,0,.3);animation:vvFl 1.3s forwards;pointer-events:none}
@keyframes vvFl{0%{opacity:0;transform:translate(-50%,20px) scale(.6)}20%{opacity:1;transform:translate(-50%,0) scale(1.1)}70%{opacity:1;transform:translate(-50%,-30px) scale(1)}100%{opacity:0;transform:translate(-50%,-60px)}}
.hr-pop{position:absolute;left:var(--x,60%);top:-6px;z-index:5;font-size:1.3rem;pointer-events:none;animation:hrPop 1s forwards}.hr-ln{position:relative}
@keyframes hrPop{0%{opacity:0;transform:translateY(10px) scale(.5)}25%{opacity:1;transform:translateY(-6px) scale(1.2)}100%{opacity:0;transform:translateY(-34px) scale(.9)}}
.lp-pod .lpg{position:relative;cursor:pointer;transition:transform .2s}.lp-pod .lpg:active{transform:scale(.96)}.lp-pod .lp-ros.hid{opacity:0;transform:scale(.3)}.lp-pod .lp-ros{transition:opacity .3s,transform .4s cubic-bezier(.3,1.6,.5,1)}
.lp-pod .lpg-pc{position:absolute;right:8px;top:8px;padding:2px 8px;border-radius:999px;background:rgba(20,33,61,.8);color:#F3D98B;font:900 .85rem Nunito,system-ui;font-style:normal;opacity:0;transition:opacity .4s .3s}.lp-pod.rev .lpg-pc{opacity:1}
.lp-pod:not(.rev) .lpg{animation:lpBob 2.4s ease-in-out infinite}.lp-pod:not(.rev) .lpg:nth-child(2){animation-delay:.3s}.lp-pod:not(.rev) .lpg:nth-child(3){animation-delay:.6s}@keyframes lpBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.lp-pod .lpg.me img{box-shadow:0 0 0 4px #2F7A3F}
#lpCap b{color:#2F7A3F}.lp-tick{margin:6px auto 0;max-width:92%;padding:6px 12px;border-radius:999px;background:#14213D;color:#EEF1F8;font:700 .82rem Nunito,system-ui;text-align:center;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.lp-tick b{color:#F3D98B}.lp-tick .in{display:inline-block;animation:tkIn .5s}@keyframes tkIn{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}
.lp-btn.lp-pulse{animation:lpPulse 1.4s ease-in-out 3}@keyframes lpPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05);box-shadow:0 0 0 8px rgba(47,122,63,.2)}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v220 ok')
