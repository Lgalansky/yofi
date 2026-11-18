# Real Money build, step 95 (after rmv91.py):
#  - Games rotate after the new-player journey: every 10 votes the next game alternates qualifier → Quick Sprint →
#    qualifier… The "Coming up" strip names the next one ("Quick Sprint · 1 v 1 · win 160 in 4 votes"). The separate
#    Quick Sprint nudge (every 20/50 votes) is gone, so the two never stack. No coins for a Sprint → the qualifier runs.
#  - Streak boxes: no pop-up. Reaching 3 / 6 / 10 in a row gives the coins straight away with a burst
#    ("Bronze box · +20"); the streak bar still shows the next box.
#  - Your photo: no toast after every qualifier try and no "in the ring now" toast. You hear about it when it matters:
#    "Through to the Final!" and its Final result. Tries and status live in the Gallery.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# rotation
RA("S.gatePend = 0; window.__autoT = Date.now(); save(); gateOpen(false);",
   "S.gatePend = 0; window.__autoT = Date.now(); S.rotN = (S.rotN || 0) + 1; save(); if (S.rotN % 2 === 0 && (S.gems || 0) >= QS_COIN) sprintUp(); else gateOpen(false);")
RA("if (!comboHit && !S.geoBlock && S.potSeen && S.votes >= 15 && (S.cpN || 0) >= (S.qsTried ? 50 : 20)",
   "if (false && !comboHit && !S.geoBlock && S.potSeen && S.votes >= 15 && (S.cpN || 0) >= (S.qsTried ? 50 : 20)")
RA("if (S.potSeen && !newbie()) { const per = S.qsTried ? 50 : 20,", "if (false && S.potSeen && !newbie()) { const per = S.qsTried ? 50 : 20,")
RA("it.push({ ic: '⚖️', t: `<b>Upcoming qualifier · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of 5 · free`, k: 'g',",
   "it.push(sprNext() ? { ic: '🎯', t: `<b>Quick Sprint</b> · 1 v 1 · win ${QS_COIN_PAY[0]} coins`, k: 'g', need: Math.max(1, GATE_EVERY - (S.gtN || 0)), per: GATE_EVERY } : { ic: '⚖️', t: `<b>Upcoming qualifier · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of 5 · free`, k: 'g',")
s = s.replace("function fcNotify() {", r"""function sprNext() { return (S.tut || 9) >= 4 && ((S.rotN || 0) + 1) % 2 === 0 && (S.gems || 0) >= QS_COIN; }
function sprintUp() { celebrate({ src: (SEED[6] || {}).src, score: '🎯', title: 'Quick Sprint is up', text: `1 v 1 against a real player: pick the photo the crowd chose in <b>10 pairs</b>. <b>${QS_COIN} coins</b> in, win <b>${QS_COIN_PAY[0]} coins</b>.`,
  cta: `🎯 Play · ${QS_COIN} coins`, onCta: () => { closeFlow(); window.__qsGame = 'qs'; sprPractice(); }, later: 'Keep voting' }); }
function fcNotify() {""", 1)
# box pops off
RA("if ((S.tut || 9) < 4) { gemExplosion(B.n, { label: `🔥 ${B.k} right in a row` }); return; }",
   "{ gemExplosion(B.n, { label: `🔥 ${B.k} in a row · ${B.t} box` }); return; }")
# fewer photo notifications
RA("toast(`🎀 ${rcName(p)} finished ${ppOrd(pl)} · that was its last qualifier try. Its spot is free for a new photo.`);", "")
RA("else toast(`🎀 ${rcName(p)} finished ${ppOrd(pl)} in its qualifier · ${HEAT_RUNS - r.runs} ${HEAT_RUNS - r.runs === 1 ? 'try' : 'tries'} left.`);", "")
RA("toast('🔴 Your photo is in the ring now! Watch it live.');", "")
open(d + 'yofi-real.html', 'w').write(s); print('rm v92 ok')
# the old coin battle ("Pet coin challenge", photo vs rival by score) is switched off in PhotoPicks
s = open(d + 'yofi-real.html').read()
RA("if (!comboHit && S.votes >= 12 && fighters().length && tUnlocked() && S.since >= CFG.BATTLE_EVERY)", "if (false && !comboHit && S.votes >= 12 && fighters().length && tUnlocked() && S.since >= CFG.BATTLE_EVERY)")
RA("return it.sort((p, q) => p.need - q.need)[0] || null; }", "return it.filter(z => z.k !== 'b').sort((p, q) => p.need - q.need)[0] || null; }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v92 battle off ok')
