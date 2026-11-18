# Real Money build, step 115 (after rmv111.py):
#  - Coins menu shows the coin games to every player, including after a deposit (cash players had them hidden):
#    Free Final pick (250), Quick Sprint (25 → 40), and a new Coin Pick row (free, win up to 50) that opens a round now.
#  - "You have unused coins" pop timing: when your balance crosses 250 (after that vote's reveal), and at the start of a
#    session after your 3rd vote if you already have 250+. Still part of the game rotation; never more than once every
#    15 votes; needs a free pick left this hour. The old 100-coin milestone nudge is off.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (isCash()) return ''; const L = fqLeft()", "const L = fqLeft()")
RA("if (!isCash() && !newbie()) I.push({ ic: '⚡', t: 'Quick Sprint'", "if (!newbie()) I.push({ ic: '🎯', t: 'Coin Pick', d: 'Pick the crowd’s top 3 of 5. Win up to <b>50 coins</b>.', cost: 0, src: (SEED.find(z => z.src) || {}).src || '', go: () => { closeSheet(); setTimeout(gateOpen, 250); } });\n  if (!newbie()) I.push({ ic: '⚡', t: 'Quick Sprint'")
RA("p: !isCash() && fqLeft() && (S.gems || 0) >= FREE_BET_COINS }", "p: fqLeft() && (S.gems || 0) >= FREE_BET_COINS }")
RA("if (!isCash() && (S.tut || 9) >= 3 && fqLeft() && (S.gems || 0) >= FREE_BET_COINS)", "if (false && (S.tut || 9) >= 3 && fqLeft() && (S.gems || 0) >= FREE_BET_COINS)")
RA("function freePickUp() {", "function freePickUp() { S.ucV = S.votes || 0; save();")
s = s.replace("function fcNotify() {", r"""(function () { let lastG = null, v0 = null;
  setInterval(() => { try { if (!S || (S.tut || 9) < 4) return; const g = S.gems || 0, v = S.votes || 0; if (v0 == null) v0 = v;
    if (lastG != null && lastG < FREE_BET_COINS && g >= FREE_BET_COINS) S.ucPend = 1;
    if (!window.__ucSess && g >= FREE_BET_COINS && v - v0 >= 3) { window.__ucSess = 1; S.ucPend = 1; }
    lastG = g;
    if (S.ucPend && g >= FREE_BET_COINS && fqLeft() > 0 && v - (S.ucV == null ? -99 : S.ucV) >= 15 && !busyUI() && $('#panes').dataset.at === 'judge' && !(typeof judging !== 'undefined' && judging)) { S.ucPend = 0; window.__autoT = Date.now(); freePickUp(); }
    else if (S.ucPend && (g < FREE_BET_COINS || !fqLeft())) S.ucPend = 0; } catch (e) {} }, 400); })();
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v112 ok')
