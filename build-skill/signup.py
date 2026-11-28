# Skill preview: user decisions from the audit.
#  1. No sign-up coin bonus. The first touch-up is already the welcome gift, so the 150 coins given at sign-up bought
#     nothing at that moment. Sign-up from a touch-up now reads "Save Milo's touch-up" / "Create your free account so
#     your photo and coins stay yours." No bonus box, no coins, no "+150" burst. The "Welcome bonus when you sign up"
#     banner on the empty Studio is gone too.
#  2. Profile sheet keeps two buttons (Hall of Fame, Spend coins); "Competitions" is gone (the Compete tab does that).
# Usage: python3 build-skill/signup.py in.html out.html  (run after audit1.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
R("${opts.bonus ? 'Claim your welcome bonus' :", "${opts.bonus ? (p ? `Save ${esc(typeof alName === 'function' ? alName(p) : (p.nm || p.title || 'your photo'))}’s touch-up` : 'Save your touch-up') :")
R("${opts.bonus || !S.giftEn ? `<div class=\"wbx\"><span>🎁 Welcome bonus</span><b>${gemIcon('')}${(CFG.FIRST_WIN + CFG.SIGNUP).toLocaleString()} coins</b><small>Free when you create your account</small></div>` : ''}", "")
R("'Create your free account to touch up your photo and get it ready to compete. '", "'Create your free account so your photo and coins stay yours. '")
R("const wb = !S.giftEn ? CFG.FIRST_WIN + CFG.SIGNUP : CFG.SIGNUP;", "const wb = 0;")
R("gemExplosion(wb, { label: `Welcome bonus · @${h}` })", "(wb && gemExplosion(wb, { label: `Welcome bonus · @${h}` }))", 2)
R("<div class=\"wl-gift\"><span>🎁 Welcome bonus when you sign up</span><b>${gemIcon('')}${CFG.FIRST_WIN + CFG.SIGNUP}</b><small>Coins to touch up your photo</small></div>", "")
R('<button class="btn quiet block" id="mC">Competitions</button>', '')
R("$('#mC').onclick = () => openComps(null);", "if ($('#mC')) $('#mC').onclick = () => openComps(null);")
open(p, 'w').write(s); print('signup ok')
