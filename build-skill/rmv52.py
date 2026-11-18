# Real Money build, step 55 (after rmv51.py): one navy-blue style for every pop (from the user's mock-up).
# Navy headings, kickers, buttons, selected borders and links; light-blue chips/boxes; gold stays for prize strips and medals;
# cash amounts stay green. Qualifier pick also matches the mock-up ("Your top 3 is ready", photo slots, "Judge photos").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("<p class=\"g2-hint\">${n < 3 ? `Choose your ${GQ_ORD[n]} place photo` : 'Your top 3 is set · tap a photo to change it'}</p>",
   "<p class=\"g2-hint ${n === 3 ? 'big' : ''}\">${n < 3 ? `Choose your ${GQ_ORD[n]} place photo` : '<b>Your top 3 is ready</b><small>Tap a photo to change your picks.</small>'}</p>")
RA("Match the ${cw} order. Win up to ${GATE_COINS[3]} coins.", "Match the ${cw} order.")
RA('<button class="link g2-link" id="gtNo">${keep}</button>', '<button class="link g2-link" id="gtNo">⚖️ Judge photos</button>', 2)

N, NB, NL = '#1E3A6E', '#E3EAF5', '#C9D6EA'
P = 'html:not(.yg) body'
css = f"""
{P} .ppop .pp-k,{P} #finPick .fp-k{{color:{N}!important}}
{P} .ppop .pp-h,{P} .ppop .g2-h,{P} .ppop .pk-h,{P} .ppop .pk-h3,{P} .ppop .fr2-h,{P} .ppop .rv-h,{P} .ppop .rvw-k,{P} #finPick h2,{P} .ppop .g2-thru b,{P} .ppop .fr2-g figure b{{color:{N}!important;-webkit-text-fill-color:{N}}}
{P} .ppop .g2-chip,{P} .ppop .g2-hint,{P} .ppop .fr2-chip,{P} .ppop .fr2-row,{P} .ppop .g2-row,{P} .ppop .fr2-rule,{P} .ppop .g2-thru,{P} .ppop .tut-up,{P} .ppop .rs-pool div,{P} .ppop .fr2-st div,{P} .ppop .pp-pays{{background:{NB}!important;color:{N}!important;box-shadow:none!important}}
{P} .ppop .tut-up{{box-shadow:inset 0 0 0 1.5px {NL}!important;color:#2B2320!important}}{P} .ppop .tut-up b{{color:{N}}}
{P} .ppop .g2-hint.big{{padding:10px 12px;border-radius:18px;max-width:none}}{P} .ppop .g2-hint.big b{{display:block;font:800 1.5rem/1.1 Fraunces,Georgia,serif;color:{N}}}{P} .ppop .g2-hint.big small{{display:block;font-weight:400;font-size:.9rem;color:#2B2320;margin-top:2px}}
{P} .ppop .btn.pc-go,{P} .ppop .btn.g2-go:not(.off),{P} .ppop .btn.g2-fin,{P} .ppop .btn.pk-go,{P} .ppop .btn.fr2-next,{P} .ppop .btn.rv-go,{P} .ppop .btn.rvw-go,{P} #finPick .btn,{P} .ppop .btn.pc-real{{background:{N}!important;background-image:none!important;color:#fff!important;-webkit-text-fill-color:#fff!important;box-shadow:0 6px 16px -8px rgba(30,58,110,.7)!important;border:0!important}}
{P} .ppop .btn.pk-go:disabled{{background:#B9B4AE!important}}
{P} .ppop .g2-link,{P} .ppop .fr2-j,{P} .ppop .rv-skip,{P} .ppop .pc-later,{P} .ppop .fr2-pay summary,{P} .ppop .lp-lnk{{color:{N}!important;-webkit-text-fill-color:{N}}}
{P} .ppop .g2-t.on,{P} .ppop .pp-t.on{{box-shadow:0 0 0 3px {N}!important}}{P} .ppop .g2-t{{box-shadow:inset 0 0 0 2px #E2D3BC}}
{P} .ppop .g2-cmp figure.ok,{P} .ppop .fr2-g figure.ok,{P} .ppop .rv-slot.hit,{P} .ppop .rb-r.pk,{P} .ppop .rs-tiers div.me,{P} .ppop .g2-prog.ready,{P} .ppop .g2-earn.won,{P} .ppop .rb-st.win{{background:{NB}!important;box-shadow:inset 0 0 0 2px {N}!important;color:{N}!important}}
{P} .ppop .rv-slot.hit{{box-shadow:0 0 0 3px {N},0 0 18px rgba(30,58,110,.45)!important;background:none!important}}
{P} .ppop .g2-cmp em.ok,{P} .ppop .g2-cmp em.fin,{P} .ppop .fr2-g em.ok,{P} .ppop .rb-t u,{P} .ppop .rv-me .ok,{P} .ppop .g2-prog.ready p+p{{color:{N}!important;-webkit-text-fill-color:{N}}}{P} .ppop .g2-cmp em.fin,{P} .ppop .fr2-g em.ok{{background:{NB}!important}}
{P} .ppop .fr2-pay th{{background:{N}!important}}{P} .ppop .fr2-pay tr.me td{{background:{NB}!important}}
{P} .ppop .g2-sl button{{height:auto!important;padding:0 0 4px!important;display:flex;flex-direction:column;align-items:stretch;background:#FBF6EE!important}}{P} .ppop .g2-sl img{{position:static!important;opacity:1!important;width:100%;height:58px;object-fit:cover;display:block;margin-bottom:4px}}
{P} .ppop .g2-sl button:not(.set){{height:58px!important;justify-content:center}}{P} .ppop .g2-sl button.cur{{border-color:{N}!important;background:{NB}!important}}{P} .ppop .g2-sl span{{font:800 1rem Fraunces,Georgia,serif;color:{N}}}
{P} .ppop .g2-chip{{font-weight:800}}
{P} .ppop .pk-lab,{P} .ppop .fr2-win b,{P} .ppop .fr2-sub{{color:{N}!important}}{P} .ppop .pk-lab::before,{P} .ppop .pk-lab::after{{background:{NL}!important}}
{P} #finPick .fp-c i{{color:{N}}}{P} #finPick .fp-t>b{{color:{N}}}
"""
s = s.replace('</style>', css + "</style>", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v52 ok')
