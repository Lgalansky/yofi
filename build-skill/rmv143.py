# Real Money build, step 146 (after rmv142.py): fair matching (hidden) + quick contests.
#  - Matching: each daily contest is quietly split into groups of similar-strength photos (by crowd score:
#    under 60% / 60–70% / 70%+). Your entry count, prizes and position are for your group; your photo ranks against
#    photos like it. Player sees one line: "You're matched with photos like yours, so every photo has a fair chance."
#  - Free daily prizes are per group: $6 / $4 / $2 (guaranteed).
#  - ⚡ Quick contest: 10 photos, $1, top 3 paid $4 / $2.50 / $2 (85% of entries), result within the hour
#    (demo: ~5 min). One running at a time per photo; enter again after the result.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("CT_FREE = [10, 6, 4];", "CT_FREE = [6, 4, 2];")
RA("function ctPrize(tier, n, rank) { if (tier === 'f')", "function ctPrize(tier, n, rank) { if (tier === 'q') return [4, 2.5, 2][rank - 1] || 0; if (tier === 'f')")
RA("1st <b>$10</b> · 2nd <b>$6</b> · 3rd <b>$4</b> · guaranteed", "1st <b>$6</b> · 2nd <b>$4</b> · 3rd <b>$2</b> · guaranteed")
RA("q = Math.max(.002, Math.min(.98, 1 - (sc - 42) / 44));", "q = Math.max(.002, Math.min(.98, .5 - (sc - ctMid(pct)) / 26));")
RA("const nf = ctN(cat, 'f'), nc = ctN(cat, 'c'),", "const pp = P.find(x => x.id === pid), pc = (pp && pp.vd && pp.vd.pct) || 60, nf = ctGrp(ctN(cat, 'f'), pc), nc = ctGrp(ctN(cat, 'c'), pc), hasQ = () => ctEntries().some(e => !e.done && e.tier === 'q' && e.pid === pid),")
RA("Free · $20 prizes · ${money(ctPool(ctN(z.k, 'c')))} cash contest", "Free · $2 daily · ⚡ $1 quick", 2)
RA("<p class=\"db-s\">The crowd’s votes decide. Closes in <b>${ctLeft()}</b>.</p>", "<p class=\"db-s\">The crowd’s votes decide. Daily contests close in <b>${ctLeft()}</b>.</p><p class=\"ct-m\">🤝 You’re matched with photos like yours, so every photo has a fair chance.</p>")
RA("${P.length ? '' : '<button class=\"btn block db-go\" id=\"ctUp\">📷 Add a photo</button>'}",
   "<div class=\"ct-t cash\"><div><b>⚡ Quick contest · $1</b><small>10 photos · top 3 paid: <b>$4</b> · <b>$2.50</b> · <b>$2</b><br>Result within the hour</small></div>${P.length ? (hasQ() ? '<em>Running ✓</em>' : '<button class=\"btn db-go cashb\" id=\"ctQ\">Enter · $1</button>') : ''}</div>\n      ${P.length ? '' : '<button class=\"btn block db-go\" id=\"ctUp\">📷 Add a photo</button>'}")
RA("Demo: results about 10 min after entering", "Demo: daily results ~10 min, quick ~5 min after entering")
RA("const enter = tier => { const k = ctDay() + cat + tier + pid; S.ct = S.ct || {}; S.ct[k] = { k, cat, tier, pid, day: ctDay(), at: Date.now(), n: tier === 'f' ? nf : nc };",
   "const enter = tier => { const k = tier === 'q' ? 'q' + pid + Date.now() : ctDay() + cat + tier + pid; S.ct = S.ct || {}; S.ct[k] = { k, cat, tier, pid, day: ctDay(), at: Date.now(), n: tier === 'q' ? 10 : tier === 'f' ? nf : nc };")
RA("toast(tier === 'f' ? '🏆 Entered free · the crowd decides' : '🏆 Entered the $2 contest');", "toast(tier === 'f' ? '🏆 Entered free · the crowd decides' : tier === 'q' ? '⚡ In a quick contest · result within the hour' : '🏆 Entered the $2 contest');")
RA("if ($('#ctF')) $('#ctF').onclick = () => enter('f');", "if ($('#ctF')) $('#ctF').onclick = () => enter('f');\n    if ($('#ctQ')) $('#ctQ').onclick = () => needAge(() => { popClose(); payCash(1, 'A $1 quick contest entry', () => setTimeout(() => { enter('q'); }, 250)); });")
RA("${e.tier === 'f' ? 'Free' : '$2'}", "${e.tier === 'f' ? 'Free' : e.tier === 'q' ? '⚡ Quick $1' : '$2'}", 2)
RA("const e = ctEntries().find(x => !x.done && Date.now() - x.at > CT_DEMO);", "const e = ctEntries().find(x => !x.done && Date.now() - x.at > (x.tier === 'q' ? CT_DEMO / 2 : CT_DEMO));")
RA("Math.max(0, 1 - (Date.now() - e.at) / CT_DEMO)", "Math.max(0, 1 - (Date.now() - e.at) / (e.tier === 'q' ? CT_DEMO / 2 : CT_DEMO))")
s = s.replace("function fcNotify() {", """const ctMid = pct => pct < 60 ? 52 : pct < 70 ? 65 : 76;
const ctGrp = (n, pct) => Math.max(12, Math.round(n * (pct < 60 ? .4 : pct < 70 ? .35 : .25)));
function fcNotify() {""", 1)
s = s.replace('</style>', """.ct-m{margin:-4px 0 8px;font-size:.82rem;color:#2F6B3F;font-weight:700}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v143 ok')
# pass 2: better-mixed random draw for each entry's crowd result (similar entries were getting near-identical draws)
s = open(d + 'yofi-real.html').read()
RA("r = cpRng(ppHash(e.k + e.pid)), base = pct + (r() - .5) * 22;", "r = cpRng((ppHash(e.k + e.pid) * 2654435761 + 12345) % 2147483647); r(); r(); r(); const base = pct + (r() - .5) * 22;")
open(d + 'yofi-real.html', 'w').write(s); print('rm v143 pass2 ok')
# pass 3: within a group, a photo's edge over the group's middle counts half (no big advantage at the top of a band)
s = open(d + 'yofi-real.html').read()
RA("q = Math.max(.002, Math.min(.98, .5 - (sc - ctMid(pct)) / 26));", "q = Math.max(.002, Math.min(.98, .5 - (sc - ctMid(pct) - (pct - ctMid(pct)) * .5) / 26));")
open(d + 'yofi-real.html', 'w').write(s); print('rm v143 pass3 ok')
