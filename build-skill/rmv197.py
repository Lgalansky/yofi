# Real Money build, step 200 (after rmv196.py): creative-director consistency pass (colour and component rules).
#  One system:
#   - Home screens (Vote, Stable, My Photos, photo entry) are cream. Every full-screen moment (start line, countdowns,
#     races, results, lobby, head-to-head setup, tune-up, challenges) is the SAME navy with gold.
#   - One navy gradient everywhere (was three). One centred gold "PhotoPicks" wordmark on every navy screen.
#   - Buttons: green = go / cash action (one green, one font, no gold ring); navy = neutral action on cream;
#     gold = step up / coins; outlined = secondary on navy. The two stray blues are gone.
#  CSS only; no behaviour changes.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
NAVY = "radial-gradient(120% 60% at 50% 0%,#1F2F58 0%,#14213D 55%,#0E1830 100%)"
GREEN = "linear-gradient(180deg,#2F8A3F,#1F6A2E)"
NBTN = "linear-gradient(180deg,#22325A,#14213D)"
GOLD = "linear-gradient(180deg,#F3D98B,#D9AE4F)"
S = "html body .pp.qfx:not(.nv):not(.h3)"
css = f"""
/* ---- consistency pass ---- */
html body #coach:has(.qfx) .ppop,html body #coach:has(.nv) .ppop,html body #coach:has(.h3) .ppop{{background:{NAVY}!important;color:#EEF1F8!important;border:0!important;box-shadow:none!important}}
html body .qrx>.qr-cd.cd2,html body .h3>.qr-cd,html body #coach:has(.nv) .qr-cd{{background:{NAVY}!important}}
html body #sheet:has(.t2){{background:linear-gradient(180deg,#1F2F58,#14213D 60%,#0E1830)!important}}
{S}{{color:#EEF1F8;text-align:center}}{S}::before{{content:'PhotoPicks';display:block;margin:0 0 8px;font:800 1.15rem Fraunces,Georgia,serif;color:#F3D98B;text-align:center}}
{S} .pp-k{{color:#F3D98B!important;-webkit-text-fill-color:#F3D98B!important}}{S} h2.db-h{{color:#FBF3DC!important;-webkit-text-fill-color:#FBF3DC!important}}
{S} .db-s,{S} .db-com,{S} .qf-vc,{S} .re-rzl,{S} .qlv-c,{S} .h2-vs small,{S} .trt-ba figcaption{{color:#EEF1F8!important}}
{S} .db-s b,{S} .qf-vc b,{S} .qlv-c b,{S} .db-com b{{color:#F3D98B!important}}{S} .db-sim{{color:#8C9AB5!important}}{S} .link{{color:#FBF3DC!important}}
{S} .h2-vs>div>b{{color:#FBF3DC}}{S} .trt-ba .aft figcaption{{color:#F3D98B!important}}
{S} .qfp-f button.on{{background:{GREEN}!important;box-shadow:0 0 0 2.5px #E9B949!important}}{S} .qfp-f button.on b,{S} .qfp-f button.on small{{color:#fff!important}}
{S} .btn.db-go{{background:{GREEN}!important;color:#fff!important}}
{S} .btn.db-go.quiet{{background:transparent!important;box-shadow:inset 0 0 0 2px #8C9AB5!important;color:#FBF3DC!important}}
{S} .btn.db-go.rm-up{{background:{GOLD}!important;color:#14213D!important}}{S} .btn.db-go.rm-coin{{background:transparent!important;box-shadow:inset 0 0 0 2px #D9AE4F!important;color:#F3D98B!important}}
{S} .rv-won{{box-shadow:0 0 0 2px #D9AE4F}}
/* one wordmark on navy */
html body .h3-top,html body .cd2-top{{position:relative;display:block;text-align:center;margin:0 0 10px}}
html body .h3-br,html body .cd2-top span{{font-size:0!important}}html body .h3-br::after,html body .cd2-top span::after{{content:'PhotoPicks';font:800 1.15rem Fraunces,Georgia,serif;color:#F3D98B}}
html body .h3-x{{position:absolute;right:0;top:-4px}}
/* one green, one navy, one gold for buttons */
html body .nv .btn.nv-go,html body .h3 .btn.nv-go,html body #flow .sx .btn.sx-go,html body .t2 .btn.t2-b.green,html body .pv .btn.pv-go,html body .cg-r .btn.cg-y,html body .btn.db-go.cashb,html body .tw .btn.cash,html body .mp-go.cash{{background:{GREEN}!important;color:#fff!important;font-family:Nunito,system-ui,sans-serif!important;font-weight:800!important;box-shadow:0 4px 12px rgba(0,0,0,.25)!important}}
html body .nv .btn.nv-go,html body .h3 .btn.nv-go{{font-size:1.2rem!important;min-height:54px!important}}
html body .t2 .btn.t2-b.blue,html body #flow .sx .btn.sx-nv{{background:{NBTN}!important;color:#fff!important}}
html body #coach .pp:not(.qfx) .btn.db-go:not(.cashb):not(.quiet):not(.rm-up):not(.rm-coin){{background:{NBTN}!important;color:#fff!important}}
html body .nv .btn.nv-coin,html body .h3 .btn.nv-up,html body .btn.db-go.rm-up{{background:{GOLD}!important;color:#14213D!important}}
html body .nv .btn.nv-go2{{background:transparent!important;box-shadow:inset 0 0 0 2px #8C9AB5!important;color:#FBF3DC!important;font:800 1rem Nunito,system-ui!important}}
/* gold and frames */
html body .nv-pill,html body .qf2-win,html body .rm-box,html body .nv-goal,html body .t2-bal{{box-shadow:inset 0 0 0 2px #D9AE4F!important}}
html body .h3-sub,html body .cd2-p,html body .h3-net{{color:#F3D98B}}
</style>"""
s = s.replace('</style>', css, 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v197 ok')
# pass 2: readable result rows, light entry tiles, light links on navy
s = open(d + 'yofi-real.html').read()
S = "html body .pp.qfx:not(.nv):not(.h3)"
s = s.replace('</style>', f"""{S} .qf-res b,{S} .qf-res em{{color:#14213D!important;-webkit-text-fill-color:#14213D!important}}{S} .qf-res i{{color:#1F6A2E!important}}
{S} .qfp-f button{{background:#FBF6EE!important;box-shadow:0 0 0 1.5px #EADCC6!important}}{S} .qfp-f button b{{color:#14213D!important}}{S} .qfp-f button small{{color:#1F6A2E!important}}
{S} .qfp-f button.on{{background:{GREEN}!important;box-shadow:0 0 0 2.5px #E9B949!important}}{S} .qfp-f button.on b,{S} .qfp-f button.on small{{color:#fff!important}}
{S} .link,{S} .link.pc-later,{S} button.link{{color:#FBF3DC!important;-webkit-text-fill-color:#FBF3DC!important}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v197 pass2 ok')
