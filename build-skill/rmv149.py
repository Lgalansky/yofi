# Real Money build, step 152 (after rmv148.py): voting in rounds, with purpose.
#  - Rounds of 10: a navy round bar above the pair ("Round 3 · Call the crowd", score, 10 dots).
#  - Stakes: about 1 pair in 3 says what it decides ("🏆 Today's Pets contest · these two are fighting for 4th place");
#    live-Final pairs keep their own tag.
#  - Your photo moves: a green strip under the pair with your photo's views and score and the 60% Play Pool line.
#    Each finished round adds 10 views and nudges a below-pool photo's score up 0–2 points (simulated); crossing 60%
#    puts it in the Play Pool.
#  - End of round: "Sharp eye! 8/10", dots, "You beat 76% of voters", round coins (10/10: 100, 9: 60, 8: 40, 7: 25,
#    else 10), rounds-in-a-row ≥7, what your votes did, your photo's move, then Next round / Race with this eye /
#    Check on your photo. The very first round's race button is the free first Match Race.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const VR_PAY = { 10: 100, 9: 60, 8: 40, 7: 25 }, VR_BEAT = { 10: 98, 9: 93, 8: 76, 7: 58, 6: 40, 5: 24, 4: 12, 3: 5, 2: 2, 1: 1, 0: 1 };
const vrMine = () => (S.photos || []).filter(p => p.framed).sort((a, b) => (b.starter ? 0 : 1) - (a.starter ? 0 : 1))[0];
(() => { const cf = callFx, rj = renderJudge;
  callFx = function (pick, pct, agree) { const r = cf.apply(this, arguments);
    try { S.vr = S.vr || { n: 1, res: [], hot: 0 }; S.vr.res.push(agree ? 1 : 0); save(); vrPaint();
      if (S.vr.res.length >= 10) setTimeout(vrEnd, 1500); } catch (e) {}
    return r; };
  renderJudge = function () { const r = rj.apply(this, arguments); try { vrDecor(); } catch (e) {} return r; }; })();
function vrBarHTML() { const v = S.vr || { n: 1, res: [] }, ok = v.res.filter(Boolean).length;
  return `<div class="vr-top" id="vrTop"><div><b>Round ${v.n}</b><small>${S.fmPend || S.tut === 1 ? 'Finish it for your free Match Race' : 'Call the crowd · 10 pairs'}</small></div><span class="vr-score">${ok} ✓</span><div class="vr-dots">${Array.from({ length: 10 }, (_, i) => `<i class="${i < v.res.length ? (v.res[i] ? 'ok' : 'no') : i === v.res.length ? 'now' : ''}"></i>`).join('')}</div></div>`; }
function vrPaint() { const t = document.getElementById('vrTop'); if (t) t.outerHTML = vrBarHTML(); }
function vrDecor() { const J = document.getElementById('judge'); if (!J || J.querySelector('#vrTop')) return; const h = J.querySelector('.tot-h'), jc = document.getElementById('jcard'); if (!h || !jc) return;
  h.insertAdjacentHTML('beforebegin', vrBarHTML());
  if (!window.__finPair) { const imgs = [...jc.querySelectorAll('img')].map(i => i.src), x = SEED.find(z => z.src === imgs[0]), k = x && finCatOf(x), r = cpRng(ppHash(imgs.join('').slice(-40) + (S.votes || 0)));
    if (k && r() < .36) { const pl = 1 + Math.floor(r() * 9); jc.insertAdjacentHTML('beforebegin', `<div class="vr-stake">🏆 <b>Today’s ${esc(showName(k))} contest</b> · these two are fighting for <b>${ppOrd(pl)} place</b>. Your vote counts.</div>`); } }
  const p = vrMine(); if (p) { const pc = (p.vd && p.vd.pct) || 55, sd = (S.vr && S.vr.res.length) || 0;
    (document.getElementById('stk2') || jc).insertAdjacentHTML('afterend', `<div class="vr-mine"><img src="${p.src}" alt=""><span><b>${esc(rcName(p))}</b> · ${p.views || 20} views${sd ? ` · +${sd} this round` : ''}<div class="vr-bar"><i style="width:${pc}%"></i><u></u></div>${pc}% picked it · ${p.pool ? 'in the Play Pool ▶️' : `${60 - pc}% to the Play Pool`}</span></div>`); } }
function vrEnd() { if (!S.vr || S.vr.res.length < 10) return; if (!freeScreen()) { setTimeout(vrEnd, 1200); return; }
  const v = S.vr, ok = v.res.filter(Boolean).length, pay = VR_PAY[ok] || 10, beat = VR_BEAT[ok]; v.hot = ok >= 7 ? (v.hot || 0) + 1 : 0;
  S.gems = (S.gems || 0) + pay; const p = vrMine(); let mv = '';
  if (p) { const was = (p.vd && p.vd.pct) || 55; p.views = (p.views || 20) + 10; if (p.vd && !p.pool && !p.starter) { p.vd.pct = Math.min(80, was + Math.floor(cpRng(ppHash(p.id + v.n))() * 3)); if (p.vd.pct >= 60) { p.pool = Date.now(); p.plAt = Date.now(); } }
    const now = (p.vd && p.vd.pct) || was; mv = `📷 <b>${esc(rcName(p))}</b> was shown to 10 more voters${now !== was ? ` · ${was}% → <b>${now}%</b>` : ''}${p.pool && now >= 60 && was < 60 ? '<br>🎉 <b>It made the Play Pool!</b> It now earns every time it’s played.' : ''}`; }
  const first = !!S.fmPend; S.fmPend = 0; const res = v.res.slice(); S.vr = { n: v.n + 1, res: [], hot: v.hot }; save(); window.__nudgeAt = Date.now();
  const head = ok >= 9 ? 'Crowd whisperer!' : ok >= 7 ? 'Sharp eye!' : ok >= 5 ? 'Solid round' : 'Tough round';
  popOpen(`<div class="pp vrr"><p class="pp-k">⚖️ Round ${v.n} complete</p><h2 class="db-h">${head}</h2>
    <div class="vrr-big">${ok}<small>/10</small></div><div class="vrr-dots">${res.map(x => `<i class="${x ? 'ok' : 'no'}">${x ? '✓' : '✕'}</i>`).join('')}</div>
    <p class="vrr-beat">You beat <b>${beat}%</b> of voters this round</p>
    <div class="vrr-rw"><div><b>+${pay} 🟡</b><small>round reward</small></div><div><b>🔥 ${v.hot}</b><small>rounds in a row ≥ 7</small></div></div>
    <div class="vrr-did">⚖️ Your votes helped decide today’s <b>contests</b> and the next <b>Final</b>${mv ? '<br>' + mv : ''}</div>
    <button class="btn block db-go" id="vrNext">⚖️ Next round</button>
    <button class="btn block db-go ${first || !isCash() ? '' : 'cashb'}" id="vrRace">⚔️ ${first ? 'Your first Match Race · free' : isCash() ? 'Race someone with this eye · $1' : 'Race someone with this eye · 25 🟡'}</button>
    ${p ? `<div style="text-align:center"><button class="link pc-later" id="vrPh">📷 Check on ${esc(rcName(p))}</button></div>` : ''}</div>`);
  setTimeout(() => { try { paintGems(); gemExplosion(pay, { label: `Round ${v.n} · ${ok}/10` }); if (ok >= 8) rvConfetti(document.querySelector('.vrr'), 40); } catch (e) {} }, 300);
  $('#vrNext').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} };
  $('#vrRace').onclick = () => { popClose(); if (first) { S.gems = (S.gems || 0) + 25; save(); paintGems(); } setTimeout(() => { gmOpen('match', isCash() ? 1 : 0); if (first) setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 80); }, 200); };
  if ($('#vrPh')) $('#vrPh').onclick = () => { popClose(); go('gallery'); try { renderMyShow(); } catch (e) {} }; }
function fcNotify() {""", 1)
# first-race pop is replaced by the round result
s = s.replace("setInterval(() => { try { if (!S || !S.fmPend ||", "setInterval(() => { try { if (true || !S || !S.fmPend ||", 1)
s = s.replace('</style>', """.vr-top{display:flex;align-items:center;gap:10px;margin:8px 2px 6px;padding:10px 12px;border-radius:14px;background:#14213D;color:#fff;box-shadow:inset 0 0 0 1.5px #D9AE4F}
.vr-top b{font:800 1rem Fraunces,Georgia,serif;color:#F3D98B;-webkit-text-fill-color:#F3D98B}.vr-top small{display:block;font-size:.72rem;opacity:.85;color:#fff}
.vr-dots{display:flex;gap:4px;margin-left:auto}.vr-dots i{width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.18)}.vr-dots i.ok{background:#5FD37A}.vr-dots i.no{background:#E06A5A}.vr-dots i.now{box-shadow:0 0 0 2px #F3D98B}
.vr-score{font:900 1.15rem Nunito,system-ui;color:#fff;white-space:nowrap}
html.coinp #qsChip,html #judge #qsChip{display:none!important}
.vr-stake{margin:0 0 8px;padding:8px 12px;border-radius:12px;background:#FFF1C9;box-shadow:inset 0 0 0 1.5px #D9AE4F;font:700 .84rem/1.35 Nunito,system-ui;color:#5B3D06;text-align:left}.vr-stake b{color:#14213D}
.vr-mine{display:flex;align-items:center;gap:10px;margin:8px 2px 0;padding:8px 10px;border-radius:12px;background:#F1F6EC;box-shadow:inset 0 0 0 1.5px #2F6B3F}
.vr-mine img{width:38px;height:46px;border-radius:7px;object-fit:cover}.vr-mine span{flex:1;font:700 .8rem/1.35 Nunito,system-ui;color:#22502F;text-align:left}.vr-mine b{color:#14213D}
.vr-bar{height:7px;border-radius:4px;background:#DCE8D6;margin:4px 0 2px;position:relative}.vr-bar i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#E9B949,#2F6B3F)}.vr-bar u{position:absolute;left:60%;top:-3px;bottom:-3px;width:2px;background:#14213D}
.vrr-big{font:900 3.4rem/1 Fraunces,Georgia,serif;color:#2F6B3F;margin:6px 0 0}.vrr-big small{font-size:1.3rem;color:#5B4A3F}
.vrr-dots{display:flex;justify-content:center;gap:5px;margin:10px 0}.vrr-dots i{width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-weight:900;font-size:.72rem;color:#fff}.vrr-dots .ok{background:#2F6B3F}.vrr-dots .no{background:#C0533F}
.vrr-beat{font-size:1rem;color:#14213D;margin:4px 0 10px}
.vrr-rw{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 10px}.vrr-rw div{background:#fff;border-radius:14px;padding:10px;box-shadow:inset 0 0 0 1.5px #EADCC6}.vrr-rw b{display:block;font:900 1.25rem Nunito,system-ui;color:#14213D}.vrr-rw small{font-size:.74rem;color:#5B4A3F}
.vrr-did{text-align:left;background:#fff;border-radius:14px;padding:10px 12px;margin:0 0 10px;box-shadow:inset 0 0 0 1.5px #EADCC6;font-size:.84rem;line-height:1.5;color:#14213D}
html body .ppop .vrr .btn.db-go{margin-top:6px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v149 ok')
# pass 2: a round is exactly 10 (extra votes made during the end-of-round pause carry into the next round);
#  race clock reads 0.0s during the 3·2·1 countdown (was showing a huge number).
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const first = !!S.fmPend; S.fmPend = 0; const res = v.res.slice(); S.vr = { n: v.n + 1, res: [], hot: v.hot };",
   "const first = !!S.fmPend; S.fmPend = 0; const res = v.res.slice(0, 10); S.vr = { n: v.n + 1, res: v.res.slice(10), hot: v.hot };")
RA("const v = S.vr, ok = v.res.filter(Boolean).length,", "const v = S.vr, ok = v.res.slice(0, 10).filter(Boolean).length,")
RA("let i = 0, tq = 0, lock = false;", "let i = 0, tq = Date.now(), lock = false;", 3)
open(d + 'yofi-real.html', 'w').write(s); print('rm v149 pass2 ok')
