# Real Money build, step 30 (after rmv26.py):
#  - Coins menu: Quick Sprint added (with Coin challenge); "Enter a photo to compete" row removed.
#  - A photo never goes straight into the Final: after improving, the first photo enters the qualifiers for its category's next Final.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# coins menu
RA("${showRowHTML()}${raceBetRowHTML()}", "${raceBetRowHTML()}")
RA("go: () => { closeSheet(); openGemBattle(100); } });",
   "go: () => { closeSheet(); openGemBattle(100); } });\n  if (!isCash()) I.push({ ic: '⚡', t: 'Quick Sprint', d: `1 v 1: pick the photo the crowd chose in 10 pairs. Win <b>${QS_COIN_PAY[0]} 🟡</b>.`, cost: QS_COIN, go: () => { closeSheet(); window.__qsGame = 'qs'; sprPractice(); } });")

# first photo: improve -> qualifiers (never straight to the Final)
RA("const sl = rcSlotFor(p); S.races = S.races || {}; S.races[sl] = { pid: p.id, at: Date.now() }; const r = rcRec(p.id); r.st = 'q'; r.sl = sl; save();",
   "const sl = rcSlotFor(p); const r = rcRec(p.id); r.st = 'heats'; r.runs = 0; S.hN = Math.max(S.hN || 0, HEAT_EVERY - 2); save();")
RA("title: 'Through to the Final!', text: `<b>${esc(p.title)}</b> improved to <b>${p.s.total}</b> and goes straight into the <b>${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>. Watch it live, and pick the top 3 in the Final that’s on now.`,\n        cta: '🎀 See the Finalists', onCta: () => { closeFlow(); raceCard(); },",
   "title: 'In the qualifiers!', text: `<b>${esc(p.title)}</b> improved to <b>${p.s.total}</b> and is in the qualifiers for the <b>${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>. ${y ? 'Judges' : 'Voters'} rank it in a group of 5: the top 2 go through to the Final.`,\n        cta: `⚖️ ${y ? 'Judge' : 'Vote'} to see its qualifier`, onCta: () => { closeFlow(); go('judge'); renderJudge(); },")
RA("Once it improves it goes <b>straight into the ${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>, no qualifiers.",
   "Once it improves it enters the <b>qualifiers for the ${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>: the top 2 in each qualifier go through.")
RA("title: 'Improve it, then straight to the Final'", "title: 'Improve it to enter the qualifiers'")
RA("t: 'Touch up to go straight to the Final', s: `Any improvement sends it to the <b>${raceName(rcSlotFor(p))} ${esc(showName(photoShow(p)))} Final</b>",
   "t: 'Touch up to enter the qualifiers', s: `Any improvement enters it for the <b>${raceName(rcSlotFor(p))} ${esc(showName(photoShow(p)))} Final</b>")
RA("We’ll give you 150 coins to improve your first photo, then it goes straight into a Final.", "We’ll give you 150 coins to improve your first photo, then it enters the qualifiers.")
RA("Your first photo goes <b>straight into that Final</b> once you improve it.", "Improve your photo and it enters that Final’s <b>qualifiers</b>: the top 2 in each go through.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v27 ok')
