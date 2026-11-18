# Real Money build, step 96 (after rmv92.py): uploading a photo never shows the old improve flow.
#  - The old AI scan ("Checking lighting… Reading composition…") becomes a short "Preparing your photo…".
#  - After the scan the photo goes straight to the Gallery and the "Frame your photo" step (name + frame); the old score
#    result / touch-up screen is never shown. Photos without a category ask for it first, then frame.
#  - Coin nudges ("You have unused coins") never open while an upload, pick or any other screen is open.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<p class="scanmsg" id="scanMsg">Checking lighting…</p>', '<p class="scanmsg" id="scanMsg">Preparing your photo…</p>')
RA("const msgs = ['Checking lighting…', 'Reading composition…', 'Measuring colour…', 'Finding your subject…', 'Testing sharpness…'];",
   "const msgs = ['Preparing your photo…'];")
RA("const s = capUpload(Engine.score(Engine.analyze(id)));\n  await sleep(2000); clearInterval(iv);",
   "const s = capUpload(Engine.score(Engine.analyze(id)));\n  await sleep(700); clearInterval(iv);")
RA("if (gc && gc.cats) { p.cat = gc.cats.find(k => PICKCATS.includes(k)) || gc.cats[0]; save(); showResult(p, { win, first, fresh: true }); return; }",
   "if (gc && gc.cats) { p.cat = gc.cats.find(k => PICKCATS.includes(k)) || gc.cats[0]; save(); upReady(p); return; }")
RA("if (p.cat) { save(); showResult(p, { win, first, fresh: true }); return; }", "if (p.cat) { save(); upReady(p); return; }")
RA("askCategory(p, () => showResult(p, { win, first, fresh: true }),", "askCategory(p, () => upReady(p),")
RA("if (!S.user || S.gems < 100 || (S.votes || 0) < 12 || $('#coach').classList.contains('on')",
   "if (!S.user || S.gems < 100 || (S.votes || 0) < 12 || busyUI() || $('#coach').classList.contains('on')")
s = s.replace("function fcNotify() {", r"""function upReady(p) { p.nmAsk = 1; save(); try { closeFlow(); } catch (e) {} const fp = document.getElementById('finPick'); if (fp) fp.className = '';
  myShow(); if (photoShow(p)) setTimeout(() => frameOpen(p), 300); else toast('Only Pets, Nature & landscapes and Garden & flowers photos can race in a Final.'); }
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v93 ok')
# sign-up sheet: no photo scores; say what the account is for
s = open(d + 'yofi-real.html').read()
RA("${opts.bonus ? 'Create your free account to touch up your photo and get it ready to compete. ' : ''}${opts.win ? `Nice! Keep your coins and your ${p ? p.s.total : ''} photo. ` : ''}${opts.win || opts.bonus ? '' : p ? `Your photo is at ${p.s.total}${p.s.total < CFG.QUALIFY ? ` and ${CFG.QUALIFY - p.s.total} points from qualifying` : ' and qualified'}. ` : ''}Create your account so nothing gets lost.",
   "${opts.pick ? 'Your picks and any winnings are saved to your account. ' : opts.photo ? 'Keep your framed photo and its prize record safe. ' : opts.win ? 'Keep your coins and your win. ' : ''}Create your account so nothing gets lost.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v93 signup ok')
