# Real Money build, step 17 (after rmv13.py): newbie flow shows the core loop.
# When a photo reaches 70+, "Ready to compete!" offers to enter it in the qualifiers (free) instead of a free first coin challenge.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""function rmReady(p) { const g = ppGame(), y = isYoungW();
  celebrate({ src: p.src, score: p.s.total, title: 'Ready to compete!', text: `Your photo hit <b>${p.s.total}</b>. Enter it in the <b>${esc(showName(photoShow(p)))}</b> qualifiers, free. ${y ? 'Judges' : 'Voters'} send the top 2 to the hourly <b>Final</b>, where every finalist’s creator shares <b>10% of the prize pool</b> (the ${raceName(g.sl)} Final’s is <b>${ppPool(g.players)}</b>).`,
    cta: '🎀 Enter the qualifiers · free', onCta: () => { closeFlow(); showEnter(p.id); setTimeout(() => { go('judge'); renderJudge(); toast(`🎀 ${rcName(p)} is in! ${y ? 'Judge' : 'Vote'} to see its first qualifier.`); }, 1400); }, later: 'Later' }); }
function fcNotify() {""", 1)
RA("  if (p && p.s.total >= CFG.QUALIFY && S.gbDone) { celebrate({ src: p.src, score: p.s.total, title: 'Ready to compete!'",
   "  if (p && p.s.total >= SHOW_MIN && photoShow(p) && !rcRec(p.id).st && inPlay() < SLOT_BASE) { rmReady(p); return; }\n  if (p && p.s.total >= CFG.QUALIFY && S.gbDone) { celebrate({ src: p.src, score: p.s.total, title: 'Ready to compete!'")
open(d + 'yofi-real.html', 'w').write(s); print('rm v14 ok')
