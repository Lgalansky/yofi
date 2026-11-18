# Real Money build, step 126 (after rmv122.py): fix "the live pick page flashes back to voting".
#  Cause: a Final's result is marked "showing" when its reveal starts and only "done" at the end. If the reveal was cut
#  short (app closed mid-reveal, page reloaded), the "showing" mark was saved, so the result never ran again, while the
#  1-second result check (rmv119) kept closing whatever was open to make room for it: every pop flashed shut.
#  Fix: an interrupted result (marked showing, but nothing on screen) replays its reveal; the check only closes a
#  screen when it is really about to show a result; stale marks are cleared when the app loads.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function ppResult(e) { if (e.__rv) return; e.__rv = 1;", "function ppResult(e) { if (rvBusy(e)) return; e.__rv = Date.now();")
RA("function raceOwnResult(sl) { const x = S.races[sl]; if (!x || x.__rv) return; x.__rv = 1;", "function raceOwnResult(sl) { const x = S.races[sl]; if (!x || rvBusy(x)) return; x.__rv = Date.now();")
RA("function winResult(w) { if (w.__rv) return; w.__rv = 1;", "function winResult(w) { if (rvBusy(w)) return; w.__rv = Date.now();")
RA("const e = Object.values(S.pp).find(x => !x.done && now >= ppDue(x)); if (e) { popClose();",
   "const e = Object.values(S.pp).find(x => !x.done && now >= ppDue(x) && !rvBusy(x)); if (e) { popClose();")
RA("const k = Object.keys(S.races).find(sl => !S.races[sl].done && now >=", "const k = Object.keys(S.races).find(sl => !S.races[sl].done && !rvBusy(S.races[sl]) && now >=")
RA("const e = Object.values(S.pw).find(x => !x.done && Date.now() >= ppDue(x));", "const e = Object.values(S.pw).find(x => !x.done && Date.now() >= ppDue(x) && !rvBusy(x));")
RA("if (e && !e.done && !e.__rv) { el.removeAttribute", "if (e && !e.done && !rvBusy(e)) { el.removeAttribute")
s = s.replace("function fcNotify() {", r"""// a result counts as "in progress" only while something is on screen for it (or for 20 s after it starts)
function rvBusy(x) { return !!(x && x.__rv && (Date.now() - x.__rv < 20000 || document.querySelector('#coach.on, #heroWin.on, .hw.on'))); }
try { ['pp', 'pw', 'races'].forEach(k => Object.values(S[k] || {}).forEach(x => { if (x && !x.done) delete x.__rv; })); } catch (e) {}
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v123 ok')
