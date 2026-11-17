# Real Money build, step 45 (after rmv41.py): follow your Final pick while you judge.
#  - "Coming up" becomes "Your pick is live · <Final> · your 1st pick is running Nth · results in M min"; tap opens the live board.
#  - While judging, a short toast when one of your picks moves place ("📈 Beach buddy moved up to 2nd").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""function myLive() { const g = ppGame(), e = (S.pp || {})[g.sl]; if (!e || e.done) return null; const now = Date.now(), cp = 1 - (g.end - now) / PP_MS, prog = Math.min(1, Math.max(.04, Math.max(cp, (now - e.at) / PP_DEMO))), L = ppLive(g, prog);
  const pos = e.picks.map(i => L.findIndex(x => x.i === i) + 1); return { g, e, pos, mins: Math.max(1, Math.ceil((ppDue(e) - now) / 60000)) }; }
setInterval(() => { try { if (!S || $('#panes').dataset.at !== 'judge' || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on')) return; const m = myLive(); if (!m) { window.__lvPos = null; return; }
  const k = m.g.sl + ':' + m.pos.join(','), was = window.__lvPos; window.__lvPos = { k, pos: m.pos.slice(), sl: m.g.sl };
  if (!was || was.sl !== m.g.sl || was.k === k) return; const i = m.pos.findIndex((p, j) => p < was.pos[j]); if (i < 0) return;
  toast(`📈 ${m.g.ph[m.e.picks[i]].t} moved up to ${ppOrd(m.pos[i])} · your ${['1st', '2nd', '3rd'][i]} pick`); } catch (e) {} }, 15000);
function fcNotify() {""", 1)
RA("function upNext() { if (!S || !S.user || S.geoBlock) return null;",
   "function upNext() { if (!S || !S.user || S.geoBlock) return null;\n  { const m = myLive(); if (m) return { ic: '🔴', t: `<b>Your pick is live · ${raceName(m.g.sl)} ${esc(showName(m.g.k))} Final</b> · your 1st pick is running ${ppOrd(m.pos[0])}`, k: 'live', need: 0, per: 1, em: `results in ${m.mins} min` }; }")
RA("function upNow() { const x = upNext(); if (!x) return;", "function upNow() { const x = upNext(); if (!x) return; if (x.k === 'live') { ppOpen(); return; }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v42 ok')
