# Real Money build, step 88 (after rmv84.py): streak boxes come back as a fixed-value reveal (option B).
#  3 right in a row → Bronze box (20 coins), 6 → Silver (40), 10 → Gold (80). The prize is shown before opening:
#  nothing is random. Tap "Open box" → the box shakes, bursts open, coins fly to the balance.
#  New players (before their first free-pick result) just get the coin burst, no pop.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function miniDrop(kind) { const n = ({ 3: 20, 5: 40, 10: 80 })[kind] || 20, k = ({ 3: 3, 5: 6, 10: 10 })[kind] || 3; S.gems = (S.gems || 0) + n; save(); gemExplosion(n, { label: `🔥 ${k} right in a row` }); }",
   r"""const BOX_T = { 3: { k: 3, n: 20, t: 'Bronze', c: '#B87333' }, 5: { k: 6, n: 40, t: 'Silver', c: '#9AA4B2' }, 10: { k: 10, n: 80, t: 'Gold', c: '#D9AE4F' } };
function miniDrop(kind) { const B = BOX_T[kind] || BOX_T[3]; S.gems = (S.gems || 0) + B.n; save();
  if ((S.tut || 9) < 4) { gemExplosion(B.n, { label: `🔥 ${B.k} right in a row` }); return; }
  popOpen(`<div class="pp bx2"><p class="pp-k">🔥 ${B.k} right in a row</p><h2 class="bx2-h">${B.t} box</h2>
    <div class="bx2-box" style="--bc:${B.c}"><span class="bx2-lid">🎁</span></div>
    <p class="bx2-p">Inside: <b><i class="qz3-coin"></i> ${B.n} coins</b></p>
    <div class="bx2-tiers">${[3, 5, 10].map(q => `<span class="${q === kind ? 'on' : ''}" style="--bc:${BOX_T[q].c}"><b>${BOX_T[q].k} in a row</b>${BOX_T[q].t} · ${BOX_T[q].n}</span>`).join('')}</div>
    <button class="btn block bx2-go" id="bxGo">Open box</button></div>`);
  $('#bxGo').onclick = () => { const bx = document.querySelector('#coach .bx2-box'); bx.classList.add('open'); $('#bxGo').disabled = true;
    setTimeout(() => { popClose(); gemExplosion(B.n, { label: `${B.t} box · ${B.k} in a row` }); }, 900); }; }""")
s = s.replace('</style>', """.bx2{text-align:center}html body .ppop .bx2-h{font:800 2rem Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:2px 0 6px}
.bx2-box{width:132px;height:132px;margin:6px auto 10px;border-radius:28px;display:grid;place-items:center;background:radial-gradient(circle at 50% 35%,#fff,#FBF3E2);box-shadow:inset 0 0 0 4px var(--bc),0 12px 26px -14px rgba(20,33,61,.6);animation:bxWob 1.6s ease-in-out infinite}
.bx2-lid{font-size:4.4rem;line-height:1}.bx2-box.open{animation:bxShake .5s ease-in-out,bxPop .35s .5s ease-in forwards}
@keyframes bxWob{0%,100%{transform:rotate(0)}50%{transform:rotate(-4deg) scale(1.03)}}@keyframes bxShake{0%,100%{transform:rotate(0)}20%{transform:rotate(-12deg)}40%{transform:rotate(12deg)}60%{transform:rotate(-8deg)}80%{transform:rotate(8deg)}}@keyframes bxPop{to{transform:scale(1.5);opacity:0}}
.bx2-p{font-size:1.05rem;margin:0 0 10px}.bx2-p b{display:inline-flex;align-items:center;gap:6px;color:#14213D}.bx2-p .qz3-coin{width:1.1em;height:1.1em}
.bx2-tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:0 0 12px}.bx2-tiers span{border-radius:12px;padding:6px 2px;font-size:.76rem;box-shadow:inset 0 0 0 1.5px #E2D3BC;opacity:.65}.bx2-tiers span.on{opacity:1;box-shadow:inset 0 0 0 2.5px var(--bc);background:#FFF8EA}.bx2-tiers b{display:block;font-size:.8rem;color:#14213D}
html body .ppop .bx2 .btn.bx2-go{background:#1E3A6E!important;color:#fff!important}
@media (prefers-reduced-motion:reduce){.bx2-box{animation:none}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v85 ok')
