# Real Money build, step 168 (after rmv164.py): don't lose new players on their first photos.
#  - The "100 coins · enter another photo" pop is gone. The right moment to offer a new photo is when one doesn't qualify.
#  - A photo that goes out earns a FREE retry: "📷 Try another photo · free" on the out screen (no 100 🟡 needed).
#  - A player's first two entries get a strong crowd (about 98% qualify in simulation), so the first experience is a win.
#    After that about 7 in 10 photos qualify (stronger photos more often).
#  Simulated: the crowd's votes.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("!freeScreen() || S.c100 ||", "!freeScreen() || true || S.c100 ||")
RA("const pr = Math.max(.25, Math.min(.8, .5 + (qlStrength(p) - 62) / 60))", "const pr = p.bo ? .74 : Math.max(.45, Math.min(.8, .55 + (qlStrength(p) - 62) / 80))", 2)
RA("if (!first && (S.gems || 0) < ENTRY_COINS)", "if (!first && !S.freeRe && (S.gems || 0) < ENTRY_COINS)")
RA('<button class="btn block db-go" id="qoE">📷 Enter another photo</button>', '<button class="btn block db-go cashb" id="qoE">📷 Try another photo · free</button>')
RA('<button class="btn block db-go" id="qlvE">📷 Enter another photo</button>', '<button class="btn block db-go cashb" id="qlvE">📷 Try another photo · free</button>')
RA("Try another shot: bright, close-up photos tend to win.", "Your next entry is on us: try another shot. Bright, close-up photos tend to win.")
RA("One win short. Bright, close-up shots tend to win.", "One win short. Your next entry is on us: bright, close-up shots tend to win.")
s = s.replace("function fcNotify() {", r"""function qlStart(p) { qlStrength(p); const paid = !p.starter && qlReal().filter(x => x !== p).length >= 1;
  if (paid && S.freeRe) { S.freeRe = 0; try { toast('📷 Free retry used'); } catch (e) {} }
  else if (paid) { S.gems = Math.max(0, (S.gems || 0) - ENTRY_COINS); try { paintGems(); toast(`📷 Photo entered · −${ENTRY_COINS} 🟡`); } catch (e) {} }
  S.nEnt = (S.nEnt || 0) + 1; p.bo = !p.starter && S.nEnt <= 2 ? 1 : 0; S.entT = 0; p.ql = { w: 0, l: 0, at: Date.now() }; p.pool = 0; save(); }
(() => { const qs = qlStep; qlStep = function (p) { const was = p.ql && p.ql.done; const r = qs.apply(this, arguments); try { if (!was && p.ql && p.ql.done === 'x') { S.freeRe = 1; save(); } } catch (e) {} return r; }; })();
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v165 ok')
