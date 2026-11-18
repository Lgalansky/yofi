# Real Money build, step 101 (after rmv97.py): "Call the crowd" voting.
#  After each vote both photos fill up from the bottom to the crowd's share with a big percentage, and a banner lands on
#  the pair: "✓ You called it!" + "+5 coins · 🔥 2 in a row" (green, small vibration) or "✕ The crowd went the other way"
#  + "62% picked the other photo" / "3-in-a-row streak reset" (navy, gentle shake). The streak counter updates at once.
#  The old small chips and the dark "picked the other one" box are hidden; the reveal holds a little longer (1.4 s).
#  Also: the old "Invite a friend! … blue ribbons and weekly pots" pop is switched off (old product copy).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("$('#jRes').textContent = `${word} ${mine}% of members picked this one.${earn ? ` Plus ${earn} coins.` : ''}`;",
   "$('#jRes').textContent = `${word} ${mine}% of members picked this one.${earn ? ` Plus ${earn} coins.` : ''}`; callFx(pick, pct, agree, earn, S.combo, prevCombo, mine);")
RA("if (earn) setTimeout(() => gemExplosion(earn, { mid: true, from: mc }), tier > 1 ? 900 : 0);", "if (earn) setTimeout(() => paintGems(), 500);")
RA("await sleep(tier === 20 ? 2800 : tier > 1 ? 1800 : 1100);", "await sleep(tier === 20 ? 2800 : tier > 1 ? 1800 : 1400);")
RA("if (!comboHit && S.votes >= 10 && !S.frIntro && S.gbDone && S.lgPlayed && !popPaced() && S.user && fighters().length) {",
   "if (false && !comboHit && S.votes >= 10 && !S.frIntro && S.gbDone && S.lgPlayed && !popPaced() && S.user && fighters().length) {")
s = s.replace("function fcNotify() {", r"""function callFx(pick, pct, agree, earn, combo, prev, mine) { const cards = document.querySelectorAll('#judge .tot-c'), jc = document.getElementById('jcard'); if (!jc) return;
  cards.forEach((c, i) => { c.insertAdjacentHTML('beforeend', `<span class="cfx-fill ${pct[i] >= 50 ? 'w' : ''} ${i === pick ? 'cfx-mine' : ''}"><i style="--h:${pct[i]}%"></i><b>${pct[i]}%</b></span>`); });
  jc.insertAdjacentHTML('beforeend', `<div class="cfx-b ${agree ? 'ok' : 'no'}"><b>${agree ? '✓ You called it!' : '✕ The crowd went the other way'}</b><small>${agree ? `${earn ? `+${earn} coins · ` : ''}🔥 ${combo} in a row` : prev >= 2 ? `${prev}-in-a-row streak reset` : `${100 - mine}% picked the other photo`}</small></div>`);
  try { if (agree && navigator.vibrate) navigator.vibrate(18); } catch (e) {}
  const nx = document.querySelector('#judge .stk-nx'); if (nx) { const c = Math.min(combo, 10), n = [3, 6, 10].find(k => k > c), nm = { 3: 'Bronze', 6: 'Silver', 10: 'Gold' }; nx.innerHTML = n ? `🔥 <b>${c} in a row</b> · ${n - c} more for a <b class="t${n}">${nm[n]} box</b>` : '🔥 <b>10 in a row!</b> Gold box earned'; nx.classList.remove('bump'); void nx.offsetWidth; nx.classList.add('bump'); } }
function fcNotify() {""", 1)
s = s.replace('</style>', """html:not(.yg) #judge .tot-c .tot-v,html:not(.yg) #judge .tot-c .tot-miss,html:not(.yg) #judge .tot-c .tot-x,html:not(.yg) #judge .tot-c .tot-r{display:none!important}
html:not(.yg) #judge #jcard{position:relative}
.cfx-fill{position:absolute!important;inset:0!important;width:auto!important;height:auto!important;border-radius:inherit;overflow:hidden;pointer-events:none;z-index:3}.cfx-fill i{position:absolute;left:0;right:0;bottom:0;height:0;background:rgba(20,33,61,.55);animation:cfxUp .7s cubic-bezier(.2,.9,.3,1) forwards}
.cfx-fill.w i{background:linear-gradient(0deg,rgba(47,107,63,.85),rgba(47,107,63,.45))}@keyframes cfxUp{to{height:var(--h)}}
.cfx-fill b{position:absolute;left:0;right:0;top:16%;text-align:center;font:900 2.4rem/1 Fraunces,Georgia,serif;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.45);opacity:0;animation:cfxIn .3s .35s forwards}
@keyframes cfxIn{to{opacity:1}}
html body #judge .tot-c .cfx-fill b{position:absolute!important;left:0!important;right:0!important;top:16%!important;bottom:auto!important;width:auto!important;height:auto!important;min-width:0!important;padding:0!important;margin:0!important;background:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;display:block!important;text-align:center!important;font:900 2.4rem/1 Fraunces,Georgia,serif!important;color:#fff!important;-webkit-text-fill-color:#fff!important}
html body #judge .tot-c .cfx-fill i{display:block!important;width:auto!important;border-radius:0!important;box-shadow:none!important;top:auto!important;inset:auto 0 0 0!important}
.cfx-b{position:absolute;left:50%;top:50%;z-index:6;transform:translate(-50%,-50%) scale(.6);opacity:0;min-width:78%;padding:12px 18px;border-radius:18px;text-align:center;box-shadow:0 14px 30px -10px rgba(0,0,0,.55);animation:cfxPop .45s .25s cubic-bezier(.2,1.5,.4,1) forwards}
.cfx-b.ok{background:#2F6B3F;box-shadow:0 0 0 3px #F3D98B,0 14px 30px -10px rgba(0,0,0,.55)}.cfx-b.no{background:#14213D;animation:cfxPop .45s .25s cubic-bezier(.2,1.5,.4,1) forwards,cfxShake .4s .7s ease}
.cfx-b b{display:block;font:800 1.35rem/1.15 Fraunces,Georgia,serif;color:#fff}.cfx-b small{display:block;margin-top:3px;font-weight:800;font-size:.9rem;color:#F3D98B}
@keyframes cfxPop{to{transform:translate(-50%,-50%) scale(1);opacity:1}}@keyframes cfxShake{25%{margin-left:-6px}75%{margin-left:6px}}
#judge .stk-nx.bump{animation:rtkPop .5s ease}
@media (prefers-reduced-motion:reduce){.cfx-fill i,.cfx-b,.cfx-fill b{animation-duration:.01s!important;animation-delay:0s!important}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v98 ok')
