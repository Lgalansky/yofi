# Real Money build, step 222 (after rmv218.py): Vote card shows progress and streak clearly.
#  - Under the route: one labelled row. Left "Steps ■■□ 1/3", right "🔥 Streak ●○".
#  - Feedback on each vote: a good vote pops a streak dot; a step flashes "+1 step!" and pulses the steps;
#    a wrong vote that breaks a streak shakes the streak dots.
#  - Title row shows the next stop on the right ("Next: 🎀 Race" / "Next: 🏁 Final").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""function pvStep(p, s, fin) { s = Math.min(QS_STEPS, s || 0); const idx = fin ? QS_STEPS + s : s, N = QS_STEPS * 2, pos = idx / N, k = S.stk || 0, live = !fin && p.ql && p.ql.live;
  const M = window.__pvM = window.__pvM || {}, now = Date.now(), pr = M[p.id]; let fx = '';
  if (!pr || pr.s !== idx || pr.k !== k) { const up = pr && idx > pr.s, hit = pr && !up && k > pr.k, miss = pr && !up && k < pr.k; M[p.id] = { s: idx, k, fx: up ? 'up' : hit ? 'hit' : miss ? 'miss' : '', at: now }; }
  if (M[p.id] && now - M[p.id].at < 1400) fx = M[p.id].fx;
  const node = i => { const x = i / N * 100, cp = i === QS_STEPS || i === N, done = i <= idx;
    return cp ? `<span class="jc ${done ? 'd' : ''}" style="left:${x}%">${i === N ? '🏁' : '🎀'}</span>` : i ? `<i class="jn ${done ? 'd' : ''} ${i > QS_STEPS ? 'g' : ''}" style="left:${x}%"></i>` : ''; };
  const steps = live ? '<span class="jr-live">🔴 Race live</span>' : `${Array.from({ length: QS_STEPS }, (_, i) => `<i class="${i < s ? 'on' : ''} ${fin ? 'g' : ''} ${fx === 'up' && i === s - 1 ? 'new' : ''}"></i>`).join('')}`;
  const streak = Array.from({ length: QS_RUN }, (_, i) => `<i class="${i < k ? 'on' : ''} ${fx === 'hit' && i === k - 1 ? 'new' : ''}"></i>`).join('');
  return `<div class="pv-tr jr ${fin ? 'fin' : ''}"><div class="pv-rail"><u style="width:${pos * 100}%"></u>${Array.from({ length: N + 1 }, (_, i) => node(i)).join('')}</div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"></div>
    <div class="pv-k jk2 ${fx}"><div class="jk-s"><small>Steps · <b>${s}/${QS_STEPS}</b></small>${steps}</div>${fx === 'up' ? '<b class="jk-pop">+1 step!</b>' : ''}<div class="jk-k"><small>🔥 Streak · <b>${k}/${QS_RUN}</b></small><span>${streak}</span></div></div>`; }
(() => { const pc = pvCard; pvCard = function (p) { let h = pc.apply(this, arguments); try { if (h.includes('pv-tr jr') && !h.includes('jr-nx')) { const fin = h.includes('pv-tr jr fin'), live = p.ql && p.ql.live && !fin;
      h = h.replace(/(<div class="pv-t"><b>[\s\S]*?<\/b>)/, `$1<span class="jr-nx">${live ? '🔴 Live' : fin ? 'Next: 🏁 Final' : 'Next: 🎀 Race'}</span>`); } } catch (e) {} return h; }; })();
function fcNotify() {""")
s = s.replace('</style>', """html body #qlS .pv-t .jr-nx{margin-left:auto;padding:3px 10px;border-radius:999px;background:#F4EBD6;font:800 .76rem Nunito,system-ui;color:#5B4A3F;white-space:nowrap}html body #qlS .pv-c.fin .pv-t .jr-nx{background:#FBF3DC;color:#9A6B12}
html body #qlS .pv-k.jk2{position:relative;display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:4px;padding:8px 10px;border-radius:12px;background:#F6F1E6}
.jk2 small b{color:#14213D;font-weight:900}.jk2 small{display:block!important;margin-bottom:3px;font:800 .62rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8A7A6A}
.jk2 .jk-s,.jk2 .jk-k{display:flex;flex-direction:column}.jk2 .jk-k{align-items:flex-end}
.jk2 .jk-s{flex-direction:row;flex-wrap:wrap;align-items:center;gap:5px}.jk2 .jk-s small{flex-basis:100%}
.jk2 .jk-s i{width:22px;height:10px;border-radius:3px;background:#E2D9C6}.jk2 .jk-s i.on{background:#2F7A3F}.jk2 .jk-s i.on.g{background:#C9952D}.jk2 .jk-s em{margin-left:4px;font:900 .9rem Nunito,system-ui;font-style:normal;color:#14213D}
.jk2 .jk-k span{display:flex;gap:6px}.jk2 .jk-k i{width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:inset 0 0 0 2px #E0B85A}.jk2 .jk-k i.on{background:radial-gradient(circle at 35% 35%,#FFD66B,#E58A12);box-shadow:0 0 0 2px #fff,0 0 8px rgba(229,138,18,.6)}
.jk2 .jr-live{font:800 .85rem Nunito,system-ui;color:#B3261E}
.jk2 i.new{animation:jkPop .6s cubic-bezier(.3,1.6,.5,1)}@keyframes jkPop{0%{transform:scale(.3)}60%{transform:scale(1.5)}100%{transform:scale(1)}}
.jk2.up{animation:jkGlow 1.2s}@keyframes jkGlow{0%{box-shadow:0 0 0 0 rgba(47,122,63,.6)}40%{box-shadow:0 0 0 6px rgba(47,122,63,.25)}100%{box-shadow:0 0 0 0 rgba(47,122,63,0)}}
.jk2.miss .jk-k span{animation:jkShake .45s}@keyframes jkShake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.jk2 .jk-pop{position:absolute;left:50%;top:-14px;transform:translateX(-50%);padding:3px 10px;border-radius:999px;background:#2F7A3F;color:#fff;font:900 .8rem Nunito,system-ui;white-space:nowrap;animation:jkUp 1.4s forwards}@keyframes jkUp{0%{opacity:0;transform:translate(-50%,8px)}20%{opacity:1;transform:translate(-50%,0)}80%{opacity:1}100%{opacity:0;transform:translate(-50%,-8px)}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v219 ok')
