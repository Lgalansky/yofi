# Real Money build, step 130 (after rmv126.py): picks get ticket tags; rosettes are earned in the result.
#  A prize rosette means "this photo won", so a gold "1" rosette on a pick running 6th said the opposite of the truth.
#  - Picking: your picks carry a navy ticket tag ("MY PICK / 1st", "MY PICK / Winner") with a gold, silver or bronze
#    edge, plus the coloured border and "Your 1st pick" strip. Pin bounce and sparkle kept.
#  - Live race / race card: no badge on the photo; the lane label and coloured ring already say "Your 1st pick".
#  - Live ticket and "Your picks in this Final": a small "Pick 1st" tag; one pick per line ("now 6th").
#  - Result reveal: a pick that lands in its exact spot earns its rosette, pinned onto the podium photo with a burst;
#    exact matches in "Your picks" show the rosette too. A miss earns nothing.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# picking grid: ticket tag instead of rosette
RA('<i class="pp-rz ${n === window.__rzNew ? \'new\' : \'\'}">${rosette(n)}</i>', '<i class="pp-rz ptw ${n === window.__rzNew ? \'new\' : \'\'}">${pickTag(n)}</i>')
RA('<i class="pp-rz ${window.__rzNew === \'w\' ? \'new\' : \'\'}">${rosette(\'w\')}</i>', '<i class="pp-rz ptw ${window.__rzNew === \'w\' ? \'new\' : \'\'}">${pickTag(\'w\')}</i>')
# race lanes and race card: no badge on the avatar
RA("${pk >= 0 ? `<i class=\"rz-mini\">${rosette(pk)}</i>` : ''}</span><span class=\"rb-t\">", "</span><span class=\"rb-t\">")
RA("${pk >= 0 ? `<i class=\"rz-mini\">${rosette(pk)}</i>` : ''}<b class=\"rtk-pos\">", "<b class=\"rtk-pos\">")
# live ticket + picks panel: small Pick tags, one per line
RA("<em><span class=\"rz-in\">${rosette(i)}</span> ${['1st', '2nd', '3rd'][i]}</em>", "<em>${pickTag(i, 1)}</em>")
RA("`<span class=\"rz-in\">${rosette(k)}</span>${esc(g.ph[i].t)} <em>${RT_ORD[rank[i] - 1]}</em>`).join(' · ')",
   "`<span class=\"myp-l\">${pickTag(k, 1)} ${esc(g.ph[i].t)} <em>· now ${RT_ORD[rank[i] - 1]}</em></span>`).join('')")
# reveal: exact spot earns the rosette
RA("el.innerHTML = `<img src=\"${p.src}\" alt=\"\">${yi >= 0 ?", "el.innerHTML = `<img src=\"${p.src}\" alt=\"\">${hit ? `<i class=\"rv-rz\">${rosette(o.win ? 'w' : k)}</i>` : ''}${yi >= 0 ?")
RA("<span class=\"${top[i] === p ? 'ex' : ''}\"><img src=\"${ph[p].src}\" alt=\"\">", "<span class=\"${top[i] === p ? 'ex' : ''}\"><img src=\"${ph[p].src}\" alt=\"\">${top[i] === p ? `<i class=\"rv-rz sm\">${rosette(i)}</i>` : ''}")
s = s.replace("function fcNotify() {", r"""function pickTag(k, mini) { const r = k === 'w' ? 'Winner' : ['1st', '2nd', '3rd'][k], c = k === 'w' || k === 0 ? 'g' : k === 1 ? 's' : 'b';
  return mini ? `<span class="ptin ${c}">Pick ${r}</span>` : `<span class="ptk ${c}"><small>My pick</small><b>${r}</b></span>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .pp-g .pp-rz.ptw{width:auto;height:auto;left:6px;top:6px;filter:drop-shadow(0 3px 5px rgba(20,33,61,.4))}
.ptk{display:inline-flex;flex-direction:column;align-items:center;min-width:54px;padding:4px 9px 5px;border-radius:7px;background:#14213D;color:#F3D98B;-webkit-text-fill-color:#F3D98B;font-style:normal;line-height:1;position:relative;border-left:5px solid #E2B243;
  -webkit-mask:radial-gradient(circle 5px at 100% 50%,transparent 98%,#000) ;mask:radial-gradient(circle 5px at 100% 50%,transparent 98%,#000)}
.ptk small{font:900 .56rem/1 Nunito,system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;opacity:.85;margin-bottom:2px}
.ptk b{font:900 1.05rem/1 Fraunces,Georgia,serif}
.ptk.s{border-left-color:#A3ACB8}.ptk.b{border-left-color:#C9874B}
.ptin{display:inline-block;padding:1px 7px;border-radius:5px;background:#14213D;color:#F3D98B;-webkit-text-fill-color:#F3D98B;font:900 .68rem/1.5 Nunito,system-ui,sans-serif;letter-spacing:.03em;border-left:4px solid #E2B243;vertical-align:1px;font-style:normal;white-space:nowrap}
.ptin.s{border-left-color:#A3ACB8}.ptin.b{border-left-color:#C9874B}
.myp-l{display:block;margin-top:3px}
.rv-slot{position:relative}
.rv-rz{position:absolute;left:-8px;top:-10px;width:40px;height:53px;z-index:4;font-style:normal;filter:drop-shadow(0 3px 5px rgba(20,33,61,.45));animation:rzPin .6s cubic-bezier(.3,1.6,.5,1) .15s both}
.rv-rz svg{width:100%;height:100%;display:block}
.rv-rz.sm{width:24px;height:32px;left:-6px;top:-8px}
.rv-yp > span{position:relative}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v127 ok')
# polish: earned rosette on the podium sits on the right edge (clear of the "Your 1st pick" label); picks panel lines stay on one line
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .rv-pod .rv-rz{left:auto;right:-8px;top:34%;width:44px;height:58px}
html body .myp-l{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}html body .myp-l em{font-style:normal;font-weight:800;color:#1E3A6E}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v127 pass2 ok')
