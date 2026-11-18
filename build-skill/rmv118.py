# Real Money build, step 121 (after rmv117.py): Finals named by category, run when ready; one free pick per Final.
#  - No clock time in a Final's name: "The 7pm Pets Final" → "The Pets Final". Times only as countdowns
#    ("Closes in 23 min"); upcoming Finals show "Starts when 6 finalists are in · 4 of 6 in".
#  - Coin players: one free pick per Final (Top 3 or Winner), instead of two an hour.
#  Simulated: Finals still run on the prototype's hourly timer behind the scenes; the "finalists in" count is
#  derived from it.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
i = s.index('const raceName = sl =>'); j = s.index('\n', i)
s = s[:i] + "const raceName = sl => { const z = SHOW_ROT[((sl % SHOW_ROT.length) + SHOW_ROT.length) % SHOW_ROT.length]; return z ? z.n : 'Final'; };" + s[j:]
# remove a category name repeated straight after the Final's (now category) name
before = len(s)
s = re.sub(r"\$\{raceName\(([^{}]*?)\)\} \$\{esc\(showName\([^{}]*?\)\)\}", r"${raceName(\1)}", s)
s = re.sub(r"\$\{raceName\(([^{}]*?)\)\} \$\{SH \? esc\(SH\.n\) : ''\}", r"${raceName(\1)}", s)
s = re.sub(r"\$\{raceName\(([^{}]*?)\)\} Final · \$\{esc\(showName\([^{}]*?\)\)\}", r"${raceName(\1)} Final", s)
s = re.sub(r"\$\{raceName\(([^{}]*?)\)\} Final · \$\{cn\}", r"${raceName(\1)} Final", s)
print('dedupe chars removed', before - len(s))
# clock times → countdowns / readiness
RA("· ends ${frTime(g.end)}</p>", "· closes in ${Math.max(1, Math.ceil((g.end - Date.now()) / 60000))} min</p>")
RA("${g.players} players · Closes ${frTime(g.end)}</p>", "${g.players} players · Closes in ${Math.max(1, Math.ceil((g.end - Date.now()) / 60000))} min</p>")
RA("<small>opens ${frTime(sl * PP_MS)}</small>", "<small>${finReady(sl)}</small>")
# one free pick per Final
RA("const fqLeft = () => FQ_MAX - (S.fqH === frHourKey() ? (S.fqN || 0) : 0);",
   "const fqLeft = () => { const sl = ppSlot(); return [(S.pp || {})[sl], (S.pw || {})[sl]].some(x => x && x.free) ? 0 : 1; };")
s = s.replace("`<p class=\"pp-r\">Both free picks used this hour · next in ${frMinsLeft()} min</p>`", "`<p class=\"pp-r\">You’ve used your free pick for this Final · next Final soon</p>`")
s = s.replace("`<p class=\"pp-r\">${fqLeft()} of ${FQ_MAX} free picks left this hour</p>`", "`<p class=\"pp-r\">1 free pick per Final</p>`")
s = s.replace("${L ? `${L} of ${FQ_MAX} left this hour` : `next in ${frMinsLeft()} min`}", "${L ? '1 free pick per Final' : 'used for this Final'}")
s = s.replace("toast(`You’ve used both free Final picks this hour. Next ones", "toast(`You’ve used your free pick for this Final. Next Final")
s = s.replace("<small>Both free picks used this hour · next in ", "<small>Free pick used for this Final · next Final in ")
s = s.replace("'Both free picks used this hour'", "'Free pick used for this Final'")
s = s.replace("function fcNotify() {", r"""function finReady(sl) { const cur = ppSlot(), k = sl - cur; if (k <= 0) return 'Racing now'; const p = (Date.now() - cur * PP_MS) / PP_MS, n = Math.max(0, Math.min(6, Math.floor((k === 1 ? 2 + 4 * p : k === 2 ? 4 * p : 2 * p))));
  return n >= 6 ? 'All 6 finalists in · starting soon' : `Starts when 6 finalists are in · ${n} of 6 in`; }
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v118 ok')
# second pass: no doubled category names, no "every hour" / "hourly" promises
s = open(d + 'yofi-real.html').read()
RA("<b>${raceName(sl)}</b> · ${esc(showName(n.k))}", "<b>${raceName(sl)} Final</b>")
s = s.replace("<small>${raceName(x.sl)} Final</small>", "<small>${finReady(x.sl)}</small>")
RA("<b>${esc(showName(G.k))}</b><small>${raceName(sl)} Final</small>", "<b>${esc(showName(G.k))} Final</b><small>${finReady(sl)}</small>")
RA("Next Final <b>${lpWhen(x.sl)}</b>", "Next Final · <b>${finReady(x.sl)}</b>")
s = s.replace("A new Final every hour. Pick the top 3 for real cash.", "A new Final whenever 6 finalists are in. Pick for real cash.")
s = s.replace("A new Final every hour.", "A new Final whenever 6 finalists are in.")
s = s.replace("Pick the winners every hour", "Pick the winners")
s = s.replace("Finals every hour: Pets", "Finals for Pets")
s = s.replace("the hourly Final", "the Final").replace("hourly Final", "Final")
open(d + 'yofi-real.html', 'w').write(s); print('rm v118 pass2 ok')
