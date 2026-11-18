# Real Money build, step 85 (after rmv81.py): new-player improvements 5–9.
#  5. Upload success moment: "<name> is in the qualifiers!" pop (photo, which Final, creators share 10%);
#     guests get "Save your photo" (account) first, then "Judge photos" takes them to the Vote tab to watch it race.
#  6. Lucky boxes and chests (random coin prizes on vote streaks) replaced by fixed streak rewards shown as a coin burst:
#     3 in a row +20, 6 in a row +40, 10 in a row +80. No pop, no chance.
#  7. New players: one goal while voting: "Free Final pick in N votes", now 10 votes (was 15); the WINS streak bar and
#     "agree with the crowd" line are hidden until the first free-pick result.
#  8. Sign-up says what it is for: "Create your account to place your pick" on the pick path; coins sheet no longer
#     mentions Studio.
#  9. First-pick guarantee: if a new player's first free pick loses, the result offers one more free pick
#     ("Not this time. Your next free pick is on us"), once.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# 5
RA("save(); toast(`🎀 ${rcName(p)} is in the qualifiers! First qualifier in ${HEAT_EVERY - S.hN} ${y ? 'judge' : 'vote'}s.`); myShow();",
   "save(); myShow(); setTimeout(() => upDone(p), 350);")
# 6
RA("function miniDrop(kind) {", "function miniDropOld(kind) {")
RA("function luckyDrop() {", "function luckyDropOld() {")
# 7
RA("if (S.tut === 1 && S.gtN >= 15)", "if (S.tut === 1 && S.gtN >= FP_VOTES)")
RA("Math.max(1, 15 - (S.gtN || 0))", "Math.max(1, FP_VOTES - (S.gtN || 0))")
RA("per: 15", "per: FP_VOTES")
RA("You judged 15 photos", "You judged ${FP_VOTES} photos")
# 8
RA("Upload a photo in Studio and your coins can start working for you.", "Keep voting to earn coins for free Final picks.")
RA("opts.win ? 'Save your win' : 'Save your photo and coins'", "opts.win ? 'Save your win' : opts.pick ? 'Create your account to place your pick' : opts.photo ? 'Save your photo' : 'Save your photo and coins'")
RA("openSignup(() => payCash(amt, what, then), { locked: false })", "openSignup(() => payCash(amt, what, then), { locked: false, pick: /pick/i.test(what) })")
RA("openSignup(() => setTimeout(ppOpen, 200), { locked: false })", "openSignup(() => setTimeout(ppOpen, 200), { locked: false, pick: 1 })")
# 9
RA("function ppOpen() { const pc = window.__ppCash; window.__ppCash = 0; const g = ppGame(),", "function ppOpen() { const pc = window.__ppCash; window.__ppCash = 0; const fsl = window.__ppSl; window.__ppSl = 0; const g = ppGame(fsl || undefined),")
RA("if (S.tut === 3) { S.tut = 4; S.unlk = 1; save(); }",
   """if (S.tut === 3 && e.free && !prize && !S.fg) { S.fg = 1; S.tut = 2; save(); const cb = document.querySelector('#coach .fr2-cash'); if (cb) { cb.insertAdjacentHTML('afterend', `<div class="fg2"><b>🎟️ Not this time. Your next free pick is on us.</b><small>New players get a second free pick in the ${raceName(fgSl())} ${esc(showName(ppGame(fgSl()).k))} Final.</small><button class="btn block" id="fgGo">🎟️ Make my free pick</button></div>`); $('#fgGo').onclick = () => { popClose(); window.__ppSl = fgSl(); setTimeout(ppOpen, 250); }; } }
  else if (S.tut === 3) { S.tut = 4; S.unlk = 1; save(); }""")
s = s.replace("function fcNotify() {", r"""var FP_VOTES = 10;
const fgSl = () => (S.pp || {})[ppSlot()] ? ppSlot() + 1 : ppSlot();
function miniDrop(kind) { const n = ({ 3: 20, 5: 40, 10: 80 })[kind] || 20, k = ({ 3: 3, 5: 6, 10: 10 })[kind] || 3; S.gems = (S.gems || 0) + n; save(); gemExplosion(n, { label: `🔥 ${k} right in a row` }); }
function luckyDrop() { miniDrop(5); }
function upDone(p) { const y = isYoungW(), r = rcRec(p.id), sl = rcSlotFor(p), guest = S.user && S.user.guest;
  celebrate({ src: p.src, score: '🎀', title: `${esc(rcName(p))} is in the qualifiers!`, text: `It’s racing for a place in the <b>${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>. ${y ? 'Judges' : 'Voters'} decide: the top 2 in each qualifier go through, and every finalist’s creator shares <b>10% of the prize pool</b>.`,
    cta: guest ? '💾 Save your photo' : `⚖️ ${y ? 'Judge' : 'Vote'} to watch it race`, onCta: () => { closeFlow(); const g = () => { go('judge'); renderJudge(); }; if (guest) openSignup(() => setTimeout(g, 200), { locked: false, photo: 1 }); else g(); }, later: 'Later' }); }
setInterval(() => { try { document.documentElement.classList.toggle('nbx', !!S && (S.tut || 9) < 4); } catch (e) {} }, 500);
function fcNotify() {""", 1)
s = s.replace('</style>', """html.nbx #judge .jfoot,html.nbx #judge p.eye{display:none!important}
.fg2{margin:10px 0 4px;padding:14px;border-radius:16px;background:#FFF6DF;box-shadow:inset 0 0 0 2px #D9AE4F;text-align:center}.fg2 b{display:block;font:800 1.15rem Fraunces,Georgia,serif;color:#14213D}.fg2 small{display:block;margin:4px 0 10px}
html body .ppop .fg2 .btn{background:#1E3A6E!important;color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v82 ok')
