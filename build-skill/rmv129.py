# Real Money build, step 132 (after rmv128.py): slim streak strip + a real box opening.
#  - The streak bar (a tall card with ten pills and three gift emojis) becomes one slim line under the photos:
#    flame counter · progress track with three drawn chests (Bronze 3, Silver 6, Gold 10) · "1 more → Bronze box".
#    The next chest glows when you're one away; reached chests show as open.
#  - Hitting a box now plays a short chest opening over the photos (drop, shake, lid flies open, light, coins burst to
#    your balance) in about 1.5 s. No pop-up and nothing to tap. Values stay fixed: Bronze 20, Silver 40, Gold 80 coins.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# template: replace the whole streak card
i = s.index('<div class="stk"><p class="stk-nx">'); j = s.index(".join('')}</div></div></div>", i) + len(".join('')}</div></div></div>")
s = s[:i] + '<div class="stk2" id="stk2">${stkHTML(combo)}</div>' + s[j:]
# per-vote update
i = s.index("const nx = document.querySelector('#judge .stk-nx'); if (nx) {"); j = s.index("nx.classList.add('bump'); }", i) + len("nx.classList.add('bump'); }")
s = s[:i] + "const sk = document.getElementById('stk2'); if (sk) { sk.innerHTML = stkHTML(combo); sk.classList.remove('bump'); void sk.offsetWidth; sk.classList.add('bump'); }" + s[j:]
# box opening
RA("{ gemExplosion(B.n, { label: `🔥 ${B.k} in a row · ${B.t} box` }); return; }",
   "{ chestBurst(B); return; }")
s = s.replace("function fcNotify() {", r"""const STK_T = [[3, 'Bronze', 0], [6, 'Silver', 1], [10, 'Gold', 2]], CH_C = [['#B87333', '#7A4A1E', '#E2A877'], ['#9AA4B2', '#5F6773', '#E6E9EE'], ['#D9AE4F', '#9A6B12', '#F6DF97']];
function chestSVG(t, open) { const C = CH_C[t];
  return `<svg viewBox="0 0 100 84" aria-hidden="true"><rect x="10" y="38" width="80" height="40" rx="7" fill="${C[0]}" stroke="${C[1]}" stroke-width="3"/><rect x="10" y="52" width="80" height="7" fill="${C[1]}"/><rect x="24" y="38" width="7" height="40" fill="${C[1]}" opacity=".5"/><rect x="69" y="38" width="7" height="40" fill="${C[1]}" opacity=".5"/>
    <g class="ch-lid" ${open ? 'transform="rotate(-28 10 40) translate(-4 -6)"' : ''}><path d="M10 40 Q10 12 50 12 Q90 12 90 40 Z" fill="${C[2]}" stroke="${C[1]}" stroke-width="3"/><path d="M24 40 Q24 18 31 15" stroke="${C[1]}" stroke-width="5" fill="none" opacity=".5"/><path d="M76 40 Q76 18 69 15" stroke="${C[1]}" stroke-width="5" fill="none" opacity=".5"/></g>
    <rect x="43" y="44" width="14" height="16" rx="3" fill="#F3D98B" stroke="${C[1]}" stroke-width="2"/><circle cx="50" cy="51" r="2.4" fill="${C[1]}"/></svg>`; }
function stkHTML(combo) { const c = Math.min(combo || 0, 10), nx = STK_T.find(x => x[0] > c);
  const lab = c >= 10 ? '<b>Gold box!</b> Keep it going' : !c ? 'Call it with the crowd to start a streak' : `<b>${nx[0] - c} more</b> → ${nx[1]} box`;
  return `<span class="stk2-f ${c ? 'on' : ''}">🔥<b>${c}</b></span><span class="stk2-tr"><span class="stk2-bar"><i style="width:${c * 10}%"></i></span>${STK_T.map(([k, n, t]) => `<u class="stk2-bx ${c >= k ? 'got' : ''} ${nx && nx[0] === k && k - c === 1 ? 'near' : ''}" style="left:${k * 10}%" title="${n} box">${chestSVG(t, c >= k)}</u>`).join('')}</span><span class="stk2-l">${lab}</span>`; }
function chestBurst(B) { const t = B.t === 'Gold' ? 2 : B.t === 'Silver' ? 1 : 0, host = document.getElementById('jcard') || document.body, o = document.createElement('div');
  o.className = 'chx t' + t + (host === document.body ? ' fx' : ''); o.innerHTML = `<span class="chx-rays"></span><span class="chx-box">${chestSVG(t, false)}</span><b class="chx-lab">${B.t} box · +${B.n} coins</b>`; host.appendChild(o);
  try { navigator.vibrate && navigator.vibrate([10, 60, 10, 60, 30]); } catch (e) {}
  setTimeout(() => o.classList.add('open'), 800);
  setTimeout(() => { try { gemExplosion(B.n, { label: `🔥 ${B.k} in a row · ${B.t} box` }); } catch (e) {} }, 950);
  setTimeout(() => o.classList.add('out'), 2000); setTimeout(() => o.remove(), 2400); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .jfoot.jf2{background:none!important;box-shadow:none!important;border:0!important;padding:0!important;margin:6px 0 0!important;min-height:0!important}
html body .stk2{display:flex;align-items:center;gap:10px;margin:10px 2px 4px;padding:8px 12px;border-radius:14px;background:#FBF7F0;box-shadow:inset 0 0 0 1.5px #EADCC6}
.stk2.bump{animation:stkBump .4s ease-out}@keyframes stkBump{40%{transform:scale(1.03)}}
.stk2-f{flex:none;display:inline-flex;align-items:center;gap:2px;font-size:1.05rem;opacity:.5;filter:grayscale(.8)}.stk2-f.on{opacity:1;filter:none}
.stk2-f b{font:900 1.1rem Nunito,system-ui,sans-serif;color:#14213D;-webkit-text-fill-color:#14213D}
.stk2-tr{position:relative;flex:1;height:30px;min-width:90px}
.stk2-bar{position:absolute;left:0;right:0;top:13px;height:6px;border-radius:3px;background:#EADCC6;overflow:hidden}.stk2-bar i{display:block;height:100%;background:linear-gradient(90deg,#F2B544,#E07B24);border-radius:3px;transition:width .4s}
.stk2-bx{position:absolute;top:0;width:30px;height:26px;transform:translateX(-85%);text-decoration:none;filter:grayscale(.5) opacity(.75)}
.stk2-bx svg{width:100%;height:100%;display:block}
.stk2-bx.got{filter:none}.stk2-bx.near{filter:none;animation:bxNear 1s ease-in-out infinite}
@keyframes bxNear{0%,100%{transform:translateX(-85%) rotate(0)}25%{transform:translateX(-85%) rotate(-9deg) scale(1.12)}75%{transform:translateX(-85%) rotate(9deg) scale(1.12)}}
.stk2-l{flex:none;max-width:42%;font:700 .78rem/1.2 Nunito,system-ui,sans-serif;color:#5B4A3F;text-align:right}.stk2-l b{color:#14213D;font-weight:900}
.chx{position:absolute;inset:0;z-index:30;display:grid;place-items:center;pointer-events:none;background:rgba(20,33,61,.28);border-radius:inherit;animation:chxIn .25s ease-out both}
.chx.fx{position:fixed}
.chx.out{animation:chxOut .4s ease-in both}@keyframes chxIn{from{opacity:0}}@keyframes chxOut{to{opacity:0}}
.chx-box{grid-area:1/1;width:150px;height:126px;animation:chDrop .45s cubic-bezier(.3,1.5,.5,1) both,chShake .4s ease-in-out .42s 1;filter:drop-shadow(0 10px 16px rgba(0,0,0,.4))}
.chx-box svg{width:100%;height:100%;display:block;overflow:visible}
.chx .ch-lid{transform-box:fill-box;transform-origin:0% 100%;transition:transform .35s cubic-bezier(.3,1.6,.5,1)}
.chx.open .ch-lid{transform:rotate(-38deg) translate(-6px,-14px)}
.chx.open .chx-box{animation:chPop .4s ease-out both}
@keyframes chDrop{from{transform:translateY(-120px) scale(.6);opacity:0}}
@keyframes chShake{20%{transform:rotate(-7deg)}40%{transform:rotate(7deg)}60%{transform:rotate(-5deg)}80%{transform:rotate(4deg)}}
@keyframes chPop{40%{transform:scale(1.12)}}
.chx-rays{grid-area:1/1;width:300px;height:300px;border-radius:50%;opacity:0;background:repeating-conic-gradient(from 0deg,rgba(255,236,170,.75) 0 10deg,rgba(255,236,170,0) 10deg 24deg);-webkit-mask:radial-gradient(circle,#000 20%,transparent 68%);mask:radial-gradient(circle,#000 20%,transparent 68%)}
.chx.open .chx-rays{animation:rays 1.2s ease-out both}@keyframes rays{0%{opacity:0;transform:scale(.4) rotate(0)}30%{opacity:1}100%{opacity:0;transform:scale(1.2) rotate(40deg)}}
.chx-lab{grid-area:1/1;align-self:end;margin-bottom:18%;padding:6px 14px;border-radius:999px;background:#14213D;color:#F3D98B;-webkit-text-fill-color:#F3D98B;font:900 1rem Nunito,system-ui,sans-serif;box-shadow:0 0 0 2px #D9AE4F;opacity:0;transform:translateY(10px)}
.chx.open .chx-lab{transition:all .3s .1s;opacity:1;transform:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v129 ok')
# tidy: the coin burst already labels the box, so no second label; shorter empty-streak text
s = open(d + 'yofi-real.html').read()
RA("'Call it with the crowd to start a streak'", "'Call it right to start a streak'")
s = s.replace('</style>', """html body .chx-lab{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v129 pass2 ok')
