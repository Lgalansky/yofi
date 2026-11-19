# Real Money build, step 154 (after rmv150.py): calmer voting, shorter rounds, clear entry indicator.
#  - Streak meter, streak chests and "On fire" banners removed (tile glow and Crowd Call stay).
#  - Rounds are 6 pairs (was 10): a photo entry costs 18 votes, not 30, so the photo library lasts longer.
#    Scores scale to the same rewards (6/6 = 100 🟡, 5/6 = 40 …).
#  - Round bar: "🎟️ 2 rounds to your next photo entry" with 3 pips (filled / current / to go) and "🎟️ 1 ready" when
#    a ticket is waiting.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<div class="stk2" id="stk2">${stkHTML(combo)}</div>', '')
RA("function miniDrop(kind) { const B = BOX_T[kind] || BOX_T[3];", "function miniDrop(kind) { return; const B = BOX_T[kind] || BOX_T[3];")
RA("if (agree && t && t !== tier(combo - 1))", "if (false && agree && t && t !== tier(combo - 1))")
RA("if (S.vr.res.length >= 10) setTimeout(vrEnd, 1500);", "if (S.vr.res.length >= VR_N) setTimeout(vrEnd, 1500);")
RA("if (!S.vr || S.vr.res.length < 10) return;", "if (!S.vr || S.vr.res.length < VR_N) return;")
RA("const v = S.vr, ok = v.res.slice(0, 10).filter(Boolean).length, pay = VR_PAY[ok] || 10, beat = VR_BEAT[ok];",
   "const v = S.vr, ok = v.res.slice(0, VR_N).filter(Boolean).length, k = Math.round(ok * 10 / VR_N), pay = VR_PAY[k] || 10, beat = VR_BEAT[k];")
RA("v.hot = ok >= 7 ?", "v.hot = k >= 7 ?")
RA("rounds in a row ≥ 7", "great rounds in a row")
RA("const res = v.res.slice(0, 10); S.vr = { n: v.n + 1, res: v.res.slice(10), hot: v.hot };", "const res = v.res.slice(0, VR_N); S.vr = { n: v.n + 1, res: v.res.slice(VR_N), hot: v.hot };")
RA("ok >= 9 ? 'Crowd whisperer!' : ok >= 7 ? 'Sharp eye!' : ok >= 5 ? 'Solid round' : 'Tough round';", "k >= 9 ? 'Crowd whisperer!' : k >= 7 ? 'Sharp eye!' : k >= 5 ? 'Solid round' : 'Tough round';")
RA("<small>/10</small>", "<small>/${VR_N}</small>")
RA("Round ${v.n} · ${ok}/10", "Round ${v.n} · ${ok}/${VR_N}")
RA("if (ok >= 8) rvConfetti", "if (k >= 8) rvConfetti")
s = s.replace("function fcNotify() {", r"""const VR_N = 6;
function vrBarHTML() { const v = S.vr || { n: 1, res: [] }, ok = v.res.filter(Boolean).length, q = S.vrq || 0, left = 3 - q, nb = S.fmPend || S.tut === 1;
  return `<div class="vr-top" id="vrTop"><div class="vr-l"><b>${nb ? '⚔️ Free Match Race at the end of this round' : `🎟️ ${left === 1 ? 'Last round' : left + ' rounds'} to your next photo entry`}</b>
    <span class="vr-tk">${nb ? '' : [0, 1, 2].map(i => `<i class="${i < q ? 'got' : i === q ? 'now' : ''}"></i>`).join('')}${(S.entT || 0) ? `<em>🎟️ ${S.entT} ready to use</em>` : ''}</span></div>
    <span class="vr-score">${ok} ✓</span><div class="vr-dots">${Array.from({ length: VR_N }, (_, i) => `<i class="${i < v.res.length ? (v.res[i] ? 'ok' : 'no') : i === v.res.length ? 'now' : ''}"></i>`).join('')}</div></div>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """.vr-l{flex:1;min-width:0}.vr-l b{display:block;font:800 .92rem/1.25 Nunito,system-ui,sans-serif!important;color:#F3D98B!important;-webkit-text-fill-color:#F3D98B}
.vr-tk{display:flex;align-items:center;gap:5px;margin-top:5px}.vr-tk i{width:22px;height:8px;border-radius:4px;background:rgba(255,255,255,.2)}.vr-tk i.got{background:#E9B949}.vr-tk i.now{background:rgba(233,185,73,.45);box-shadow:0 0 0 1.5px #E9B949}
.vr-tk em{font-style:normal;font:800 .72rem Nunito,system-ui;color:#9FE3AE;margin-left:6px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v151 ok')
s = open(d + 'yofi-real.html').read()
RA("S.vr = { n: v.n + 1, res: v.res.slice(VR_N), hot: v.hot }; save(); window.__nudgeAt = Date.now();", "S.vr = { n: v.n + 1, res: v.res.slice(VR_N), hot: v.hot }; save(); window.__nudgeAt = Date.now(); setTimeout(() => { try { vrPaint(); } catch (e) {} }, 0);")
open(d + 'yofi-real.html', 'w').write(s); print('rm v151 pass2 ok')
