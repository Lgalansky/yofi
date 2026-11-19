# Real Money build, step 151 (after rmv147.py): voting fun pass.
#  1. Hot streak: the vote tiles glow warmer as you call it right in a row (3 / 5 / 10), with a banner at each step:
#     "🔥 On fire! 3 in a row" → "🔥🔥 Hot streak! 5 in a row" → "👑 Crowd whisperer! 10 in a row". A miss cools it.
#  2. 🔮 Crowd Call: about every 20 votes in a session, one pair is a Crowd Call (purple glow, banner). Call it with
#     the crowd for 3× coins; miss and nothing is lost.
#  3. Race caller: "😱 Pipped at the post!" when the lead is lost on the last pair, "🏆 First past the post!" when won.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (i >= N) t = '📸 Across the line…';", "if (i >= N) t = rk === 1 ? '🏆 First past the post!' : prev === 1 ? '😱 Pipped at the post!' : `📸 Across the line in ${ppOrd(rk)}`;")
s = s.replace("function fcNotify() {", r"""(() => { const cf = callFx, rj = renderJudge; let sv = 0;
  const tier = c => c >= 10 ? 3 : c >= 5 ? 2 : c >= 3 ? 1 : 0;
  const banner = (cls, html) => { const jc = document.getElementById('jcard'); if (!jc) return; const b = document.createElement('div'); b.className = 'hsb ' + cls; b.innerHTML = html; jc.appendChild(b); setTimeout(() => b.remove(), 1700); };
  callFx = function (pick, pct, agree, earn, combo, prev, mine) { const r = cf.apply(this, arguments); sv++;
    try { const jc = document.getElementById('jcard');
      if (window.__ccOn) { window.__ccOn = 0; if (agree) { const bonus = Math.max(4, (earn || 2) * 2); S.gems = (S.gems || 0) + bonus; save(); setTimeout(() => { try { paintGems(); gemExplosion(bonus, { label: '🔮 Crowd Call · 3×' }); } catch (e) {} }, 500); banner('cc', `🔮 <b>Crowd Call!</b> 3× coins`); }
        else banner('cc miss', '🔮 Not this time · no coins lost'); }
      else { const t = tier(combo); if (agree && t && t !== tier(combo - 1)) { banner('t' + t, ['', '🔥 <b>On fire!</b> 3 in a row', '🔥🔥 <b>Hot streak!</b> 5 in a row', '👑 <b>Crowd whisperer!</b> 10 in a row'][t]); try { navigator.vibrate && navigator.vibrate([10, 40, 10, 40, 20]); } catch (e) {} } }
      if (sv % 20 === 14) window.__ccNext = 1; } catch (e) {}
    return r; };
  renderJudge = function () { const r = rj.apply(this, arguments);
    try { const jc = document.getElementById('jcard'); if (jc) { const c = (S && S.combo) || 0; jc.classList.remove('hs1', 'hs2', 'hs3', 'ccp'); const t = tier(c); if (t) jc.classList.add('hs' + t);
      if (window.__ccNext && (S.tut || 9) >= 4) { window.__ccNext = 0; window.__ccOn = 1; jc.classList.add('ccp'); jc.insertAdjacentHTML('afterbegin', '<div class="cc-top">🔮 <b>Crowd Call</b> · call it right for <b>3× coins</b></div>'); } } } catch (e) {}
    return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """#jcard{position:relative;transition:box-shadow .4s,border-radius .4s;border-radius:22px}
#jcard.hs1{box-shadow:0 0 0 3px #F2B544,0 0 22px rgba(242,181,68,.55)}
#jcard.hs2{box-shadow:0 0 0 3px #E07B24,0 0 30px rgba(224,123,36,.65);animation:hsPulse 1.6s ease-in-out infinite}
#jcard.hs3{box-shadow:0 0 0 4px #D9AE4F,0 0 40px rgba(217,174,79,.9);animation:hsPulse 1.1s ease-in-out infinite}
@keyframes hsPulse{50%{filter:brightness(1.06)}}
#jcard.ccp{box-shadow:0 0 0 3px #7B4FC9,0 0 30px rgba(123,79,201,.55)!important}
.cc-top{position:absolute;left:50%;top:-14px;transform:translateX(-50%);z-index:6;padding:5px 12px;border-radius:999px;background:#5B3A9E;color:#fff;font:800 .8rem Nunito,system-ui,sans-serif;white-space:nowrap;box-shadow:0 4px 12px rgba(91,58,158,.4);animation:cdPop .5s ease-out both}
.hsb{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);z-index:40;padding:10px 18px;border-radius:999px;background:#14213D;color:#F3D98B;font:800 1.05rem Nunito,system-ui,sans-serif;white-space:nowrap;box-shadow:0 0 0 2px #D9AE4F,0 10px 26px rgba(0,0,0,.35);pointer-events:none;animation:hsb 1.7s ease-out both}
.hsb b{color:#fff}.hsb.t2{background:#B5541A}.hsb.t3{background:linear-gradient(135deg,#9A6B12,#D9AE4F);color:#14213D}.hsb.t3 b{color:#14213D}
.hsb.cc{background:#5B3A9E;color:#fff;box-shadow:0 0 0 2px #C9B3F2,0 10px 26px rgba(0,0,0,.35)}.hsb.cc.miss{background:#5B4A6E}
@keyframes hsb{0%{opacity:0;transform:translate(-50%,-50%) scale(.6)}15%{opacity:1;transform:translate(-50%,-50%) scale(1.08)}25%{transform:translate(-50%,-50%) scale(1)}80%{opacity:1}100%{opacity:0;transform:translate(-50%,-70%)}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v148 ok')
# pass 2: shorter Crowd Call label that fits; never on a live-Final pair (it waits for the next pair)
s = open(d + 'yofi-real.html').read()
RA("if (window.__ccNext && (S.tut || 9) >= 4) {", "if (window.__ccNext && (S.tut || 9) >= 4 && !window.__finPair) {")
RA("'<div class=\"cc-top\">🔮 <b>Crowd Call</b> · call it right for <b>3× coins</b></div>'", "'<div class=\"cc-top\">🔮 <b>Crowd Call</b> · 3× coins</div>'")
s = s.replace('</style>', """html body .cc-top{max-width:92%;overflow:hidden;text-overflow:ellipsis}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v148 pass2 ok')
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .cc-top{left:0!important;right:0;margin:0 auto;width:max-content;transform:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v148 pass3 ok')
