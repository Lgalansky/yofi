# Real Money build, step 167 (after rmv163.py): full-screen start line when a photo enters its qualifier.
#  "Sterling is in!" — big framed photo, its horse on the start of the track, "15 crowd votes · win 8 to reach a Final",
#  "Each vote you make moves it forward", button "⚖️ Start voting". Mirrors the full-screen "Qualified!" finish.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function upDone(p) { qlStart(p); window.__nudgeAt = Date.now(); const nm = esc(rcName(p)), more = qlReal().filter(x => x !== p && x.ql && !x.ql.done).length;
  popOpen(`<div class="pp qfx qlv qls"><p class="pp-k">🎀 Qualifier · starting now</p><h2 class="db-h">${nm} is in!</h2>
    <div class="qlv-ph"><img src="${p.src}" alt=""></div>${qlLiveTrack(p)}
    <div class="qls-r"><div><b>15</b><small>crowd votes</small></div><div><b>8</b><small>wins to the Final</small></div><div><b>+5 🟡</b><small>per win</small></div></div>
    <p class="db-s">⚖️ <b>Each vote you make moves it forward.</b> Reach 🏁 and it races in a Final for cash.${more ? ` You now have ${more + 1} photos in play.` : ''}</p>
    <button class="btn block db-go" id="qsJ">⚖️ Start voting</button><p class="db-sim">Prototype: the crowd’s votes are simulated</p></div>`);
  setTimeout(() => { const hz = document.getElementById('qlHz'); if (hz) hz.classList.add('qls-go'); }, 400);
  $('#qsJ').onclick = () => { popClose(); go('judge'); renderJudge(); }; }
function fcNotify() {""", 1)
s = s.replace('</style>', """.qls-r{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:10px 0}.qls-r div{padding:8px 4px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}
.qls-r b{display:block;font:900 1.25rem Fraunces,Georgia,serif;color:#14213D}.qls-r small{font:700 .7rem Nunito,system-ui;color:#5B4A3F}
.qls-go{animation:qlsGo 1.2s ease-in-out 2}@keyframes qlsGo{0%,100%{transform:translateX(0)}50%{transform:translateX(6px) rotate(4deg)}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v164 ok')
