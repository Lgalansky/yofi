# Real Money build, step 31 (after rmv27.py): newbie judging flow has no qualifiers.
# "Coming up" shows "Free Final pick · in 15 votes"; after 15 votes the free Final pick opens. Qualifiers start after the free pick is used.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

TUT_V = 15
RA("if (S.gtN >= (S.tut === 1 ? 5 : GATE_EVERY)) { S.gtN = 0; S.gatePend = 1; if (S.tut === 1) S.tut = 2; }",
   "if (S.tut === 1 || S.tut === 2) { if (S.tut === 1 && S.gtN >= %d) { S.gtN = 0; S.tut = 2; S.fpPend = 1; } } else if (S.gtN >= GATE_EVERY) { S.gtN = 0; S.gatePend = 1; }" % TUT_V)
RA("function upNext() { if (!S || !S.user || S.geoBlock) return null;",
   "function upNext() { if (!S || !S.user || S.geoBlock) return null;\n  if (S.tut === 1 || S.tut === 2) { const nd = S.tut === 2 ? 0 : Math.max(1, %d - (S.gtN || 0)); return { ic: '🎟️', t: `<b>Free Final pick</b> · pick the top 3 of 6 · real cash prizes`, k: 'fp', need: nd, per: %d, em: nd ? `in ${nd} vote${nd === 1 ? '' : 's'}` : 'Now' }; }" % (TUT_V, TUT_V))
RA("if (x.k === 'g') { S.gtN = 0; save(); gateOpen(false); return; }",
   "if (x.k === 'fp') { if (S.tut === 2) ppOpen(); else toast(`${isYoungW() ? 'Judge' : 'Vote'} ${x.need} more to unlock your free Final pick`); return; } if (x.k === 'g') { S.gtN = 0; save(); gateOpen(false); return; }")
s = s.replace("function fcNotify() {", r"""setInterval(() => { try { if (!S || !S.fpPend || S.tut !== 2 || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || $('#panes').dataset.at !== 'judge') return; S.fpPend = 0; save();
  celebrate({ src: (ppGame().ph[0] || {}).src || '', score: '🎟️', title: 'Your free Final pick is ready', text: `You’ve judged ${%d} photos. Pick the top 3 of 6 in the <b>${raceName(ppGame().sl)} ${esc(showName(ppGame().k))} Final</b>, free. Top scores share the <b>${ppPool(ppGame().players)}</b> prize pool in real cash.`, cta: '🎟️ Make my free pick', onCta: () => { closeFlow(); ppOpen(); }, later: 'Later' }); } catch (e) {} }, 1200);
function fcNotify() {""" % TUT_V, 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v28 ok')
