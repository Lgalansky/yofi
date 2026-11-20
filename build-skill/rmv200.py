# Real Money build, step 203 (after rmv199.py): reviewers' quick wins — pinned main buttons and leftovers cleared.
#  1. The main green button stays pinned to the bottom of every full-screen navy screen (Final lobby "Enter the
#     final", start line "Start voting", results "Race again" / "New challenge", Qualified, So close, head-to-head
#     setup, name-and-frame, tune-up). The rest scrolls behind it. The strip under navy screens is gone.
#  2. Leftovers removed: the old "You've got N coins! … Use 25 on it now" popup; the "3 in a row" toast (rule is 2);
#     "$843 prize pool" on the entry sheet (now "1st wins up to $70").
#  3. Landing page matches the real game: new sub-line, a 4-step "How it works", one call to action. Removed the
#     Photo games / Grand National / "Pick a winner" / prize-pool cards / AI score strip / old testimonials and FAQ.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("3 in a row · your photo moves on", "2 in a row · your photo moves on")
RA("<em>${ppPool(g.players)} prize pool</em><u class=\"fp-sel\">", "<em>1st wins up to ${money(20 * QF_PAY[0])}</em><u class=\"fp-sel\">")
s = s.replace("function fcNotify() {", r"""function gemNudge() { return false; }
function landFix() { try { const L = document.getElementById('landing'); if (!L || L.dataset.fx) return; L.dataset.fx = 1;
  const sub = L.querySelector('.lp-sub'); if (sub) sub.textContent = 'Enter your photos. Vote them into a live race. Win real cash in the Final.';
  const S2 = L.querySelectorAll('.lp2-sec');
  if (S2[2]) S2[2].innerHTML = `<h2>How it works</h2><ol class="lf-steps"><li><b>1</b><span><strong>Enter a photo</strong>Free. Pets or Nature &amp; landscapes.</span></li><li><b>2</b><span><strong>Vote it forward</strong>Two right in a row moves it a step.</span></li><li><b>3</b><span><strong>Win the live qualifier</strong>A 2-horse race decided by the crowd.</span></li><li><b>4</b><span><strong>Race the Final for cash</strong>$2 to $20 entry. 1st wins 3.5×, up to $70.</span></li></ol><button class="lp-btn" onclick="rmEnterOwn()">📷 Enter your photo <span aria-hidden="true">→</span></button>`;
  if (S2[1]) S2[1].remove();
  L.querySelectorAll('.lp-ct,.lp-watch').forEach(e => e.remove());
  L.querySelectorAll('.cs').forEach(e => { if (/camera roll to cash|everyday joy|quick answers/i.test(e.textContent)) e.remove(); });
  const end = L.querySelector('.cs-end'); if (end) end.innerHTML = end.innerHTML.replace('Your first frame is free.', 'Entering a photo is free.'); } catch (e) {} }
landFix(); setTimeout(landFix, 400); setTimeout(landFix, 1500);
function fcNotify() {""", 1)
PIN = "html body #coach .qfx #qfpGo,html body #coach .qfx #qsJ,html body #coach .qfx #qrA,html body #coach .qfx #h2Ag,html body #coach .qfx #qlvGo,html body #coach .qfx #xqGo,html body #coach .qfx #h2Go,html body #coach .qfx #trY,html body #coach .qfx.qw>.nv-go[data-trn]"
s = s.replace('</style>', PIN + """{position:sticky!important;bottom:12px;z-index:6;box-shadow:0 0 0 7px rgba(14,24,48,.94),0 -14px 22px 8px rgba(14,24,48,.75),0 10px 24px rgba(0,0,0,.5)!important}
html body #coach:has(.qfx){background:#0E1830!important;padding:0!important}html body #coach:has(.qfx) .ppop{min-height:100dvh;height:100dvh!important;padding-bottom:calc(env(safe-area-inset-bottom) + 22px)!important}
.lf-steps{list-style:none;margin:10px 0 14px;padding:0;display:grid;gap:8px;text-align:left}.lf-steps li{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}
.lf-steps li>b{flex:none;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#14213D;color:#F3D98B;font:900 1rem Fraunces,Georgia,serif;box-shadow:0 0 0 2px #D9AE4F}
.lf-steps span{font:600 .86rem/1.35 Nunito,system-ui;color:#5B4A3F}.lf-steps strong{display:block;font:800 1rem Nunito,system-ui;color:#14213D}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v200 ok')
