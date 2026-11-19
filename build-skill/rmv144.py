# Real Money build, step 147 (after rmv143.py): first-session pacing (newbie run-through #3).
#  1. First game is winnable: a player's first-ever game is matched with newer players (prototype: weaker simulated
#     opponents, accuracy ~25 points below your eye). Real build: match newcomers with newcomers.
#  2. One ask at a time: the "first real game is on us" offer waits until the player has seen their photo's verdict
#     (or skipped the photo moment). Then it arrives as its own moment: "Now race for real cash".
#  3. Starter photo in 3 screens, not 5: auto-framed (already named) → "Collecting its first votes…" → verdict.
#  4. Daily reward only when the app is opened (first 90 s of a session), never in the very first session.
#  5. Play tab shows games only; contests live on My Photos.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# 1
RA("const g = GM[mode], seed = Date.now() % 1e7, r = cpRng(seed), eye = dbEye(), O = gmOpps(g.n - 1, eye, r),",
   "const g = GM[mode], seed = Date.now() % 1e7, r = cpRng(seed), eye = dbEye(), O = gmOpps(g.n - 1, (S.gmN || 0) < 1 ? Math.max(.3, eye - .25) : eye, r),")
# 2
RA("function gmFreeRealHTML() { return !isCash() && !S.frGiven ?", "function gmFreeRealHTML() { return !isCash() && !S.frGiven && frReady() ?")
RA("document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());\n  $('#phUp').onclick",
   "document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => { S.phSkip = 1; save(); popClose(); });\n  $('#phUp').onclick")
RA("if (S.notifPend && !S.notifAsked) { notifAsk(); return; }",
   "if (S.notifPend && !S.notifAsked) { notifAsk(); return; }\n  if (frReady() && !S.frGiven && !S.frNudged && !isCash() && Date.now() - (window.__vdAt || 0) > 25000) { frNudge(); return; }")
RA("p.vd = { pct, beat, at: Date.now() };", "window.__vdAt = Date.now(); p.vd = { pct, beat, at: Date.now() };")
# 4
RA("if ((S.gmN || 0) >= 1 && (!S.cal || S.cal.last !== new Date().toDateString())) { calShow(); return; }",
   "if (window.__gmN0 >= 1 && Date.now() - window.__sessAt < 90000 && (!S.cal || S.cal.last !== new Date().toDateString())) { calShow(); return; }")
# 5
RA("${gmCardsHTML()}${ctCardHTML()}\n    <div class=\"fn-live\">", "${gmCardsHTML()}\n    <div class=\"fn-live\">")
s = s.replace("function fcNotify() {", r"""const frReady = () => !!(S && ((S.photos || []).some(p => p.vd) || S.phSkip));
window.__sessAt = Date.now(); try { window.__gmN0 = (S && S.gmN) || 0; } catch (e) { window.__gmN0 = 0; }
function frNudge() { S.frNudged = 1; save(); window.__nudgeAt = Date.now();
  popOpen(`<div class="pp"><p class="pp-k">💵 Ready for the real thing?</p><h2 class="db-h">Now race for real cash</h2><p class="db-s">Same game, same photo pairs. Your first <b>$1 Match Race</b> is on us. Win and <b>$1.70</b> real cash is yours.</p>
    <button class="btn block db-go cashb" id="fnGo">🎟️ Play my free real game</button><div style="text-align:center"><button class="link pc-later" id="fnLater">Later</button></div></div>`);
  $('#fnGo').onclick = () => { popClose(); setTimeout(freeRealStart, 200); }; $('#fnLater').onclick = () => popClose(); }
(() => { const ur = upReady; upReady = function (p) { if (p && p.starter) { p.nmAsk = 1; p.framed = Date.now(); S.ffDone = 1; save(); try { closeFlow(); } catch (e) {} try { const fp = document.getElementById('finPick'); if (fp) fp.className = ''; myShow(); } catch (e) {} setTimeout(() => upDone(p), 300); return; } return ur(p); }; })();
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v144 ok')
