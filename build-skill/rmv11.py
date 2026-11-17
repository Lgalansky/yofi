# Real Money build, step 14 (after rmv10.py): coins menu has no "Touch up a photo" row,
# and the coin challenge costs 100 coins (win 200).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("  if (up) { const L = up.s.total < CFG.QUALIFY ? null : nextLvl(up.s.total), gap", "  if (0 && up) { const L = up.s.total < CFG.QUALIFY ? null : nextLvl(up.s.total), gap")
RA("Put your <b>${f.s.total}</b> photo up against a rival. Win <b>50 🟡</b> in 30 seconds.`, cost: 25, src: f.src, go: () => { closeSheet(); openGemBattle(25); }",
   "Put your <b>${f.s.total}</b> photo up against a rival. Win <b>200 🟡</b> in 30 seconds.`, cost: 100, src: f.src, go: () => { closeSheet(); openGemBattle(100); }")
RA("coin ${isYoungW() ? 'battle' : 'challenge'}</b> · win 50 🟡`", "coin ${isYoungW() ? 'battle' : 'challenge'}</b> · win 200 🟡`")
RA("photo. Stake <b>25 🟡</b>, win <b>50 🟡</b>. Result in 30 seconds.`", "photo. Stake <b>100 🟡</b>, win <b>200 🟡</b>. Result in 30 seconds.`")
RA("challenge for <b>50 🟡</b>. You don’t have a", "challenge for <b>200 🟡</b>. You don’t have a")
RA("cta: bme ? 'Free challenge · 25 🟡' : `📷 Add a ${tn.toLowerCase()} photo`, onCta: () => bme ? openGemBattle(25, null,",
   "cta: bme ? 'Play · 100 🟡' : `📷 Add a ${tn.toLowerCase()} photo`, onCta: () => bme ? openGemBattle(100, null,")
RA("coin challenges. Stake <b>25 🟡</b>, win <b>50 🟡</b>.", "coin challenges. Stake <b>100 🟡</b>, win <b>200 🟡</b>.")
RA("stake = free ? 0 : (stake || 25);", "stake = free ? 0 : (stake || 100);")
open(d + 'yofi-real.html', 'w').write(s); print('rm v11 ok')
