# Real Money build, step 136 (after rmv132.py): every screen stays inside one category; Coin Pick decided by the crowd.
#  Library check: Pets has 6 real pet photos; Nature & landscapes 8 (Nature + Travel shots); Garden & flowers had no
#  garden photos at all and was padded with dogs, cats and the tiger. So:
#  - Garden & flowers is parked as "coming soon" (like Food) until real garden photos are added. Finals rotate
#    Pets / Nature & landscapes.
#  - Nature & landscapes no longer pulls in Wildlife (the tiger).
#  - Finals never fill from another category.
#  - Voting: both photos always come from the same category and the label matches; photos outside the live
#    categories (people, food, city, surf, tiger) are not shown.
#  - Coin Pick: 5 photos from the category, order decided by the crowd (no longer "the two Final photos always win");
#    no claim that the top 2 go to the Final (Coin Pick is a coin game; qualifiers are for players' own photos).
#  - Copy and entry checks list the live categories only; Garden photos can't be framed until it opens.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("{ k: 'nature', n: 'Nature & landscapes', seed: ['Nature', 'Travel', 'Wildlife'] }, { k: 'garden', n: 'Garden & flowers', seed: ['Nature', 'Travel'] }",
   "{ k: 'nature', n: 'Nature & landscapes', seed: ['Nature', 'Travel'] }, { k: 'garden', n: 'Garden & flowers', seed: ['Garden'], soon: 1 }")
# Finals: no filling from other categories
RA("list = ppShuffle(pool.slice(), r).concat(ppShuffle(SEED.filter(x => x.src && !pool.includes(x)), r));", "list = ppShuffle(pool.slice(), r);")
# photoShow: parked categories can't take entries
RA("function photoShow(p) { const c = p && p.cat, y = isYoungW(); if (!c) return null;", "function photoShow(p) { const r = photoShow0(p); return r && SHOWS.some(z => z.k === r && z.soon) ? null : r; }\nfunction photoShow0(p) { const c = p && p.cat, y = isYoungW(); if (!c) return null;")
# voting pair: same category, live categories only
i = s.index("function seedPair() {"); j = s.index("\n", i)
s = s[:i] + r"""function seedPair() { if (!S.order) return [null, null]; if (S.order.length !== SEED.length) { S.order = ppShuffle(SEED.map((_, k) => k), cpRng(Date.now() % 1e6)); save(); }
  const n = S.order.length, at = k => SEED[S.order[((S.jIdx + k) % n + n) % n]], ok = x => x && x.src && finCatOf(x); let i = 0, a = null;
  for (; i < n; i++) if (ok(at(i))) { a = at(i); break; } if (!a) return [null, null]; const c = finCatOf(a); let b = null;
  for (let k = 1; k < n; k++) { const x = at(i + k); if (x !== a && ok(x) && finCatOf(x) === c) { b = x; break; } }
  return [a, b || a]; }""" + s[j:]
# Coin Pick: crowd decides, same category
i = s.index("function gateGame() {"); j = s.index("\nfunction ", i + 10)
s = s[:i] + r"""function gateGame() { const ns = ppSlot() + 1, R = ppGame(ns), gi = (S.gateI || 0) % 3, rr = cpRng(ns * 17 + gi * 5 + (S.gateN || 0) * 101 + 3);
  const shSeed = (SHOWS.find(z => z.k === R.k) || { seed: [] }).seed, pool = ppShuffle(SEED.filter(x => x.src && shSeed.includes(x.cat)), rr).slice(0, 5);
  const ph = pool.map((x, i) => ({ src: x.src, t: x.title || 'Untitled', h: QS_NAMES[(ns + i + 3) % QS_NAMES.length], st: .3 + rr() * .6 }));
  const ord = ph.map((p, i) => [i, p.st + (rr() - .5) * .5]).sort((a, b) => b[1] - a[1]).map(x => x[0]);
  return { ns, gi, ph, ord }; }""" + s[j:]
RA("<p class=\"g2-foot\">Free to play · Top 2 reach the ${fin} Final</p>", "<p class=\"g2-foot\">Free to play · the crowd’s votes decide the order</p>")
RA("title: `Top 2 go through to the ${raceName(G.ns)} Final` }", "title: `${showName(ppGame(G.ns).k)} · decided by the crowd’s votes` }")
# copy: live categories only
RA("'Pick the Final it’s for: Pets, Nature & landscapes or Garden & flowers.'", "'Pick the Final it’s for: Pets or Nature & landscapes.'")
RA("toast('Only Pets, Nature & landscapes, Garden & flowers and Food photos can be shown.')", "toast('Only Pets and Nature & landscapes photos can be entered right now. Garden & flowers opens soon.')")
RA("Categories: Pets · Nature & landscapes · Garden & flowers · Food (soon).", "Categories: Pets · Nature & landscapes · Garden & flowers (soon) · Food (soon).")
RA("toast('Only Pets, Nature & landscapes and Garden & flowers photos can be framed for a Final.')", "toast('Only Pets and Nature & landscapes photos can be framed for a Final right now. Garden & flowers opens soon.')")
RA("toast('Only Pets, Nature & landscapes and Garden & flowers photos can race in a Final.')", "toast('Only Pets and Nature & landscapes photos can race in a Final right now. Garden & flowers opens soon.')")
s = s.replace("Finals for Pets, Nature &amp; landscapes, Garden &amp; flowers.", "Finals for Pets and Nature &amp; landscapes · Garden &amp; flowers coming soon.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v133 ok')
