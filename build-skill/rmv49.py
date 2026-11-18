# Real Money build, step 52 (after rmv48.py): the new-player flow ends when they see their first free pick's RESULT.
#  - Until then (pick still running): no qualifiers, no Quick Sprint / coin challenge, no 250-coin free pick row,
#    no "unused coins" nudges. The coins menu shows "Your free pick is live · Watch".
#  - After the first result: the coins menu shows everything, and a one-time note points the player to their coins.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("const newbie = () => S && (S.tut || 9) < 3;", "const newbie = () => S && (S.tut || 9) < 4;")
RA("if (S.tut === 1 || S.tut === 2) { if (S.tut === 1 && S.gtN >= 15)", "if ((S.tut || 9) < 4) { if (S.tut === 1 && S.gtN >= 15)")
RA("  if (S.tut === 1 || S.tut === 2) { const nd", "  if (S.tut === 3) return null;\n  if (S.tut === 1 || S.tut === 2) { const nd")
RA("function raceBetRowHTML() { if (S.tut === 2)",
   "function raceBetRowHTML() { if (S.tut === 3) return `<button class=\"ug-r ug-swap ug-tk\" id=\"rbLiveRow\"><span class=\"ug-i\">🔴</span><span class=\"ug-t\"><b>Your free pick is live</b><small>Results soon · more ways to use your coins unlock after your first result</small></span><em>Watch ›</em></button>`; if (S.tut === 2)")
RA("function gemNudge(force) {", "function gemNudge(force) { if (S && (S.tut || 9) < 4) return false;")
RA("if (S.tut === 3) { S.tut = 4; save(); }", "if (S.tut === 3) { S.tut = 4; S.unlk = 1; save(); }")
s = s.replace("function fcNotify() {", r"""document.addEventListener('click', e => { if (e.target.closest('#rbLiveRow')) { e.preventDefault(); e.stopPropagation(); try { closeSheet(); } catch (x) {} ppOpen(); } }, true);
setInterval(() => { try { if (!S || !S.unlk || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on')) return; S.unlk = 0; save();
  toast('🟡 Unlocked: free Final picks, Quick Sprint and coin challenges · tap your coins'); const p = document.querySelector('#gemPill, .gempill, #wCoins'); if (p) { p.classList.add('unl'); setTimeout(() => p.classList.remove('unl'), 6000); } } catch (e) {} }, 1500);
function fcNotify() {""", 1)
s = s.replace('</style>', """.unl{animation:unlGlow 1s ease-in-out 6}@keyframes unlGlow{50%{box-shadow:0 0 0 3px #E2A21C,0 0 18px rgba(226,162,28,.7)}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v49 ok')
