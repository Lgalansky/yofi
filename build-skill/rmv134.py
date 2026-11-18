# Real Money build, step 137 (after rmv133.py): Quick Sprint pairs are skill, not coin flips.
#  Before: each pair's "crowd pick" was a 50/50 coin flip and pairs mixed categories (a dog vs a beach).
#  Now: both photos come from the same live category; each photo has a hidden crowd appeal, and the crowd share
#  follows the difference in appeal plus a little round-to-round noise. The stronger photo usually wins (about 7 in
#  10 for a clear gap), close pairs stay close, so judgement matters but memorising photos can't guarantee a win.
#  Nothing in the Finals (finalists, Up next card) feeds into Sprint results.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
i = s.index("function cpPairs(n, seed, close) {"); j = s.index("\nconst sprId", i)
s = s[:i] + r"""function cpAppeal(x) { const q = cpRng(ppHash('ap:' + (x.id || x.title || ''))); return .3 + q() * .6; }
function cpPairs(n, seed, close) { const r = cpRng(seed), P = SEED.filter(x => x.src && finCatOf(x)), out = [];
  for (let i = 0; i < n; i++) { const a = P[Math.floor(r() * P.length)], same = P.filter(x => x !== a && finCatOf(x) === finCatOf(a)), b = same[Math.floor(r() * same.length)] || P.find(x => x !== a);
    let share = 50 + (cpAppeal(a) - cpAppeal(b)) * 38 + (r() - .5) * 40; if (Math.abs(share - 50) < 2) share = share < 50 ? 48 : 52;
    share = Math.round(Math.max(close ? 30 : 22, Math.min(close ? 70 : 78, share))); out.push({ a, b, pa: share }); } return out; }""" + s[j:]
open(d + 'yofi-real.html', 'w').write(s); print('rm v134 ok')
