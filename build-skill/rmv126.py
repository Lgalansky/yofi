# Real Money build, step 129 (after rmv125.py): county-fair prize rosettes for your picks.
#  - Drawn rosette badge (gold 1st, silver 2nd, bronze 3rd, gold ★ for your Winner pick) in the photo's top-left
#    corner, so it never covers the subject.
#  - Picked tile: border in the rosette's colour and a strip along the bottom of the photo: "Your 1st pick".
#  - Once all 3 are picked, the other photos fade back.
#  - 🔥% chip stays top-right.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
ORD = "['1st', '2nd', '3rd']"
RA("""<div class="pp-g g6">${g.ph.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on' : ''}" data-pp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-b">${PP_MED[n]}</i>` : ''}</span><span class="pp-nm">""",
   """<div class="pp-g g6 ${picks.length === 3 ? 'full' : ''}">${g.ph.map((p, i) => { const n = picks.indexOf(i); return `<button class="pp-t ${n >= 0 ? 'on rk' + n : ''}" data-pp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${n >= 0 ? `<i class="pp-rz">${rosette(n)}</i><span class="pp-strip">Your ${""" + ORD + """[n]} pick</span>` : ''}</span><span class="pp-nm">""")
RA("""<button class="pp-t ${pick === i ? 'on' : ''}" data-wp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${pick === i ? '<i class="pp-b">🏆</i>' : ''}""",
   """<button class="pp-t ${pick === i ? 'on rk0' : ''}" data-wp="${i}"><span class="pp-im"><img src="${p.src}" alt="">${pick === i ? `<i class="pp-rz">${rosette('w')}</i><span class="pp-strip">🏆 Your winner</span>` : ''}""")
s = s.replace("function fcNotify() {", r"""function rosette(k) { const C = [['#A97A22', '#F8E6A8', '#E2B243'], ['#6F7886', '#F1F3F6', '#C3C9D2'], ['#86501F', '#F3CFA6', '#C9874B']][k === 'w' ? 0 : k];
  const pet = Array.from({ length: 16 }, (_, j) => { const a = j * Math.PI / 8; return `<circle cx="${(30 + 21 * Math.cos(a)).toFixed(1)}" cy="${(30 + 21 * Math.sin(a)).toFixed(1)}" r="7.5" fill="${C[2]}" stroke="${C[0]}" stroke-width=".8"/>`; }).join('');
  return `<svg viewBox="0 0 60 80" aria-hidden="true"><path d="M20 40 L10 78 L19 72 L26 79 L32 44Z" fill="${C[0]}"/><path d="M40 40 L50 78 L41 72 L34 79 L28 44Z" fill="${C[2]}" stroke="${C[0]}" stroke-width=".8"/>${pet}<circle cx="30" cy="30" r="21" fill="${C[2]}"/><circle cx="30" cy="30" r="16.5" fill="${C[1]}" stroke="${C[0]}" stroke-width="1.6"/><circle cx="30" cy="30" r="13.5" fill="none" stroke="${C[0]}" stroke-width=".6" stroke-dasharray="1.5 2"/><text x="30" y="${k === 'w' ? 36 : 37}" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-weight="900" font-size="${k === 'w' ? 18 : 20}" fill="#14213D">${k === 'w' ? '★' : k + 1}</text></svg>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .pp-g .pp-im{position:relative}
html body .pp-g .pp-rz{position:absolute;left:5px;top:3px;width:44px;height:59px;z-index:3;filter:drop-shadow(0 3px 4px rgba(20,33,61,.45));animation:qsPlus .35s ease-out}
html body .pp-g .pp-rz svg{width:100%;height:100%;display:block}
html body .pp-g .pp-strip{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:5px 8px;font:900 .8rem/1.2 Nunito,system-ui,sans-serif;color:#14213D;-webkit-text-fill-color:#14213D;text-align:left;letter-spacing:.01em}
html body .pp-g .rk0 .pp-strip{background:#F3D98B}html body .pp-g .rk1 .pp-strip{background:#E3E7EC}html body .pp-g .rk2 .pp-strip{background:#EFC59A}
html body .pp-g .pp-t.on.rk0{border-color:#C9962E!important;box-shadow:0 0 0 2.5px #C9962E,0 6px 16px rgba(201,150,46,.3)!important}
html body .pp-g .pp-t.on.rk1{border-color:#8E96A3!important;box-shadow:0 0 0 2.5px #8E96A3,0 6px 16px rgba(110,120,134,.25)!important}
html body .pp-g .pp-t.on.rk2{border-color:#B9773E!important;box-shadow:0 0 0 2.5px #B9773E,0 6px 16px rgba(185,119,62,.28)!important}
html body .pp-g.full .pp-t:not(.on){opacity:.45;filter:saturate(.6)}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v126 ok')
# Winner tab: odds chip top-right (same corner as the Top 3 🔥% chip) so the "Your winner" strip never covers it
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .pp-g .wp-od{top:6px!important;bottom:auto!important;z-index:3}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v126 pass2 ok')
# Chips off the photos: they covered too much of a small tile.
#  Top 3: popularity moves to the handle line ("@luna_loves · 🔥 16%"). Winner: odds move to the name line as a
#  compact pill next to the photo's name.
s = open(d + 'yofi-real.html').read()
RA('<small>@${esc(p.h)}</small></span><span class="pp-cap">', '<small class="pp-hd"><span>@${esc(p.h)}</span><em class="pp-pc" title="Share of players picking it to win">🔥 ${bk[i]}%</em></small></span><span class="pp-cap">')
RA('<b class="pop" title="Popularity: share of players picking it to win">🔥 ${bk[i]}%</b></span></button>', '</span></button>')
RA('<em class="wp-od">${od[i]}×</em></span><span class="pp-nm"><b>${esc(p.t)}</b>', '</span><span class="pp-nm"><span class="pp-tl"><b>${esc(p.t)}</b><em class="wp-od2">${od[i]}×</em></span>')
s = s.replace('</style>', """html body .pp-g .pp-hd{display:flex!important;align-items:center;gap:6px;min-width:0}html body .pp-g .pp-hd span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
html body .pp-g .pp-pc{flex:none;font-style:normal;font-weight:900;color:#14213D;-webkit-text-fill-color:#14213D;font-size:.8rem;white-space:nowrap}
html body .pp-g .pp-tl{display:flex;align-items:center;gap:6px;min-width:0}html body .pp-g .pp-tl b{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
html body .pp-g .wp-od2{flex:none;font-style:normal;font-weight:900;font-size:.8rem;padding:2px 8px;border-radius:999px;background:#14213D;color:#F3D98B;-webkit-text-fill-color:#F3D98B;box-shadow:0 0 0 1.5px #D9AE4F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v126 pass3 ok')
# ---- pass 4: shipped version ----
#  Fun: pinning a rosette drops it in with a bounce and a gold sparkle; the 3rd pick gets a bigger burst.
#  Money: after the 3rd pick (or the winner pick) the screen glides down to the pick button, which now shows what a
#  full win pays ("All 3 right pays about $10.60", from the live payout table) / the winner return.
#  Consistency: darker silver; the same rosettes on the live race lanes, the race card, the live ticket and the
#  "Your picks in this Final" panel.
s = open(d + 'yofi-real.html').read()
RA("['#6F7886', '#F1F3F6', '#C3C9D2']", "['#56606D', '#EEF1F4', '#A3ACB8']")
RA('<i class="pp-rz">${rosette(n)}</i>', '<i class="pp-rz ${n === window.__rzNew ? \'new\' : \'\'}">${rosette(n)}</i>')
RA('<i class="pp-rz">${rosette(\'w\')}</i>', '<i class="pp-rz ${window.__rzNew === \'w\' ? \'new\' : \'\'}">${rosette(\'w\')}</i>')
RA("if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); window.__keepScroll = 1; draw(); });",
   "let added = -1; if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) { picks.push(i); added = picks.length - 1; } window.__rzNew = added; window.__keepScroll = 1; draw(); window.__rzNew = -1; if (added >= 0) rzFx('pp', i, added === 2); });", 3)
RA("pick = +b.dataset.wp; window.__keepScroll = 1; draw(); });",
   "const was = pick; pick = +b.dataset.wp; window.__rzNew = was === pick ? -1 : 'w'; window.__keepScroll = 1; draw(); window.__rzNew = -1; if (was !== pick) rzFx('wp', pick, true); });")
RA("${n3 ? `Pick for ${money(stake)}` : 'Choose your top 3'}</button>",
   "${n3 ? `Pick for ${money(stake)}<small class=\"pk-win\">All 3 right pays about ${money(stake * ppTopX(g))}</small>` : 'Choose your top 3'}</button>")
RA("${pick == null ? 'Choose your winner' : `💵 Pick to win · ${money(stake)}`}</button>",
   "${pick == null ? 'Choose your winner' : `💵 Pick to win · ${money(stake)}<small class=\"pk-win\">Pays about ${money(stake * od[pick])} if it wins</small>`}</button>")
# rosettes elsewhere
RA("${pk >= 0 ? `<i>${PP_MED[pk]}</i>` : ''}<b class=\"rtk-pos\"", "${pk >= 0 ? `<i class=\"rz-mini\">${rosette(pk)}</i>` : ''}<b class=\"rtk-pos\"")
RA("<span class=\"rb-im\"><img src=\"${p.src}\" alt=\"\">${pk >= 0 ? `<i>${PP_MED[pk]}</i>` : ''}", "<span class=\"rb-im\"><img src=\"${p.src}\" alt=\"\">${pk >= 0 ? `<i class=\"rz-mini\">${rosette(pk)}</i>` : ''}")
RA("<em>${PP_MED[i]} ${['1st', '2nd', '3rd'][i]}</", "<em><span class=\"rz-in\">${rosette(i)}</span> ${['1st', '2nd', '3rd'][i]}</")
RA("`${PP_MED[k]} ${esc(g.ph[i].t)}", "`<span class=\"rz-in\">${rosette(k)}</span>${esc(g.ph[i].t)}")
s = s.replace("function fcNotify() {", r"""function ppTopX(g) { try { const n = g.players, T = ppField(g, g.sl, n + 1); ppUnits(T, n * RACE_AVG * .78); return (T.find(t => t.k === 3) || { x: 5.3 }).x; } catch (e) { return 5.3; } }
function rzFx(kind, i, big) { const t = document.querySelector(`#coach [data-${kind}="${i}"]`), im = t && t.querySelector('.pp-im'); if (!im) return;
  const n = big ? 16 : 9; for (let k = 0; k < n; k++) { const sp = document.createElement('i'), a = Math.random() * Math.PI * 2, r = (big ? 46 : 30) + Math.random() * 26;
    sp.className = 'rz-sp'; sp.style.setProperty('--dx', Math.cos(a) * r + 'px'); sp.style.setProperty('--dy', Math.sin(a) * r + 'px'); sp.style.animationDelay = (Math.random() * .12) + 's'; im.appendChild(sp); setTimeout(() => sp.remove(), 1100); }
  try { navigator.vibrate && navigator.vibrate(big ? [12, 40, 18] : 10); } catch (e) {}
  if (big) setTimeout(() => { const go = document.querySelector('#coach #ppGo:not([disabled]), #coach #ppFree:not([disabled]), #coach #wpGo:not([disabled]), #coach #wpFree:not([disabled])'); if (!go) return; go.scrollIntoView({ behavior: 'smooth', block: 'center' }); go.classList.remove('pk-pulse'); void go.offsetWidth; go.classList.add('pk-pulse'); }, 550); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .pp-g .pp-rz{animation:none}
html body .pp-g .pp-rz.new{animation:rzPin .5s cubic-bezier(.3,1.6,.5,1) both}
@keyframes rzPin{0%{transform:translateY(-26px) scale(1.9) rotate(-24deg);opacity:0}60%{transform:translateY(2px) scale(.92) rotate(6deg);opacity:1}100%{transform:none}}
.rz-sp{position:absolute;left:32px;top:30px;width:7px;height:7px;border-radius:50%;background:radial-gradient(circle,#FFF6D0,#E9B949 60%,transparent 70%);z-index:4;pointer-events:none;animation:rzSp .8s ease-out both}
@keyframes rzSp{0%{transform:translate(0,0) scale(.4);opacity:1}100%{transform:translate(var(--dx),var(--dy)) scale(1.1);opacity:0}}
html body .ppop .pk-win{display:block;font:800 .8rem/1.2 Nunito,system-ui,sans-serif;opacity:.92;margin-top:2px;color:#F3D98B;-webkit-text-fill-color:#F3D98B}
html body .ppop .pk-go.pk-pulse{animation:pkPulse 1s ease-out 2}
@keyframes pkPulse{0%{box-shadow:0 0 0 0 rgba(47,107,63,.55)}100%{box-shadow:0 0 0 16px rgba(47,107,63,0)}}
html body i.rz-mini{position:absolute!important;left:-6px!important;top:-8px!important;width:22px!important;height:30px!important;font-size:0!important;background:none!important;box-shadow:none!important;border:0!important;padding:0!important;z-index:3;filter:drop-shadow(0 1px 2px rgba(0,0,0,.4))}
html body i.rz-mini svg,.rz-in svg{width:100%;height:100%;display:block}
.rz-in{display:inline-block;width:15px;height:20px;vertical-align:-5px;margin-right:2px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v126 pass4 ok')
# payout line sits under the button label, not beside it
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .ppop .pk-go{flex-wrap:wrap!important;row-gap:0!important}html body .ppop .pk-go .pk-win{flex-basis:100%;text-align:center}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v126 pass5 ok')
