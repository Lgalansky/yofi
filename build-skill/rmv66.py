# Real Money build, step 69 (after rmv65.py): reveal end state from the user's mock-up.
#  Headline tells the story ("You picked the winner!" / "You're a winner!" / "Spot on!" / "Not this time") with a one-line sub,
#  navy "YOU WON $1.33" box with a gold amount (muted pill on a loss), pool line under it, gold-ruled section labels,
#  "✓ Exact match" chips under the crowd's photos you matched and on your picks.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<p class="rv-s" id="rvS">${title}</p>', '<p class="rv-s" id="rvS">${title}</p><div id="rvBox"></div>')
RA("res: { won: !!pay, txt: pay ? `+${pay}", "res: { won: !!pay, amt: `+${pay} coins`, txt: pay ? `+${pay}")
RA("res: { won: !!prize, txt: prize ? `You won ${money(prize)}", "res: { won: !!prize, amt: money(prize), txt: prize ? `You won ${money(prize)}")
RA("""    const O = ['1st', '2nd', '3rd'], tg = (p, i) => top[i] === p ? '<em class="ok">✓ Exact</em>'""",
   """    const O = ['1st', '2nd', '3rd'], won = o.res && o.res.won, w1 = picks[0] === top[0];
    $('#rvH').innerHTML = won ? (o.qual ? 'Spot on!' : w1 ? 'You picked the winner!' : 'You’re a winner!') : 'Not this time';
    const sub = o.qual ? `${ex} of 3 in the exact spot` : w1 && ex === 1 ? 'Your 1st pick finished 1st.' : `${ex} in the exact spot · ${inT} of your photos in the top 3`;
    $('#rvBox').innerHTML = `<p class="rv-sub2">${sub}</p>${won ? `<div class="rv-won"><span>You won</span><b>${o.res.amt}</b></div>` : `<span class="rv-res">${o.res ? o.res.txt : ''}</span>`}<p class="rv-pool">${title}</p>`;
    $('#rvS').style.display = 'none'; document.querySelector('.rv').classList.add(won ? 'rv-w' : 'rv-l'); if (won) rvConfetti($('#rvBox'), 40);
    const pod = $('#rvPod'); if (pod && !document.querySelector('.rv-exs')) pod.insertAdjacentHTML('afterend', `<div class="rv-pod rv-exs">${[0, 1, 2].map(k => `<span>${picks[k] === top[k] ? '<em>✓ Exact match</em>' : ''}</span>`).join('')}</div>`);
    const tg = (p, i) => top[i] === p ? '<em class="ok">✓ Exact match</em>'""")
RA("""$('#rvMe').innerHTML = `<b class="rv-sum">${o.qual ? `${ex} of 3 in the exact spot` : `${inT} of your photos in the top 3 · ${ex} in the exact spot`}</b>${o.res ? `<span class="rv-res ${o.res.won ? 'won' : ''}">${o.res.txt}</span>` : ''}
      <span class="rv-yp-h">Your picks</span>""", """$('#rvMe').innerHTML = `<span class="rv-yp-h rv-rule"><span>Your picks</span></span>""")
RA('<p class="rv-lab">', '<p class="rv-lab rv-rule">')
RA("${isYoungW() ? 'The judges’' : 'The crowd’s'} top 3</p>", "<span>${isYoungW() ? 'The judges’' : 'The crowd’s'} top 3</span></p>")
s = s.replace('</style>', """html body .ppop .rv .rv-h{font:800 2.3rem/1.02 Fraunces,Georgia,serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D}.rv-sub2{margin:4px 0 10px;font-size:1.05rem}
.rv-won{position:relative;background:linear-gradient(#1E3A6E,#14274E);border-radius:20px;box-shadow:0 0 0 2.5px #D9AE4F,0 8px 20px -10px rgba(20,33,61,.6);padding:10px 12px 12px;margin:0 4px 8px;overflow:hidden}
.rv-won span{display:flex;align-items:center;justify-content:center;gap:12px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;font-size:1.05rem}.rv-won span::before,.rv-won span::after{content:'';flex:0 0 46px;height:1.5px;background:#D9AE4F}
html body .ppop .rv-won span{color:#F3D98B!important;-webkit-text-fill-color:#F3D98B}html body .ppop .rv-won b{display:block;font:900 3.6rem/1 Fraunces,Georgia,serif;background:linear-gradient(#FFF3C4,#E9B949 60%,#C8901F);-webkit-background-clip:text;background-clip:text;color:transparent!important;-webkit-text-fill-color:transparent}
.rv-pool{margin:2px 0 10px;font-size:.92rem;opacity:.85}.rv-rule{display:flex!important;align-items:center;gap:12px;justify-content:center}.rv-rule::before,.rv-rule::after{content:'';flex:1;height:1.5px;background:#D9AE4F}
html body .ppop .rv-lab,html body .ppop .rv-yp-h{color:#14213D!important;-webkit-text-fill-color:#14213D;font-size:.86rem}
.rv-exs{margin-top:6px}.rv-exs span{text-align:center;min-height:0}.rv-exs em,.rv-yp em.ok{display:inline-block;font-style:normal;font-weight:800;font-size:.78rem;padding:3px 10px;border-radius:999px;background:#E3F0DE!important}
html body .ppop .rv-exs em,html body .ppop .rv-yp em.ok{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}html:not(.yg) body .ppop .rv .rv-slot.hit{box-shadow:0 0 0 3px #D9AE4F,0 0 18px rgba(217,174,79,.55)!important}
.rv.rv-w{background:radial-gradient(circle at 10% 8%,rgba(233,185,73,.18),transparent 30%),radial-gradient(circle at 90% 8%,rgba(233,185,73,.18),transparent 30%)}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v66 ok')
