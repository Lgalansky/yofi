# Real Money build, step 183 (after rmv179.py): encourage 2 photos at a time.
#  - Entry screen: gold tip "📷 Pick 2 photos · double your chances · if one misses, the other's still racing".
#    The camera roll already allows several.
#  - After entering just one photo: the start line offers "📷 Add a second photo" (once) above "Start voting".
#  - First time you have 2 photos in play: +25 🟡 "Two horses in the race!".
#  - Photos named automatically ("Photo 3") show "✏️ Name it" on their card; tap to name.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("Win it and it races in a 6-photo Final for cash. Entry is free.</p>",
   "Win it and it races in a 6-photo Final for cash. Entry is free.</p><p class=\"two-tip\">📷 <b>Pick 2 photos · double your chances</b><small>If one misses, the other’s still racing.</small></p>")
RA('<button class="btn block db-go" id="qsJ">⚖️ Start voting</button>',
   '${!S.ask2 && pvList().length < 2 ? `<div class="two-add"><b>📷 Add a second photo?</b><small>If one misses, the other’s still racing · +25 🟡</small><button class="btn block db-go cashb" id="qs2">📷 Add a second photo</button></div>` : ""}<button class="btn block db-go" id="qsJ">⚖️ Start voting</button>')
s = s.replace("function fcNotify() {", r"""(() => { const ud = upDone; upDone = function (p) { const r = ud.apply(this, arguments); try { const b = document.getElementById('qs2'); if (b) { S.ask2 = 1; save(); b.onclick = () => { popClose(); setTimeout(finPick, 200); }; } } catch (e) {} return r; }; })();
(() => { const qs = qlStart; qlStart = function (p) { const r = qs.apply(this, arguments); try { const n = (S.photos || []).filter(x => x.ql && !x.ql.done && !x.starter).length;
  if (n >= 2 && !S.two) { S.two = 1; S.gems = (S.gems || 0) + 25; save(); setTimeout(() => { try { paintGems(); gemExplosion(25, { label: 'Two horses in the race!' }); } catch (e) {} }, 1200); } } catch (e) {} return r; }; })();
(() => { const pc = pvCard; pvCard = function (p) { let h = pc.apply(this, arguments); if (/^Photo \d+$/.test(p.title || '')) h = h.replace(`<b>${esc(rcName(p))}</b>`, `<b>${esc(rcName(p))}</b><button class="nm-it" data-nm="${p.id}">✏️ Name it</button>`); return h; }; })();
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-nm]'); if (!b) return; e.preventDefault(); e.stopPropagation(); const p = (S.photos || []).find(x => x.id === b.dataset.nm); if (!p) return;
  const t = (prompt('Name your photo', '') || '').trim().slice(0, 28); if (t) { p.title = t; save(); const e2 = document.getElementById('qlS'); if (e2) e2.outerHTML = qlStripHTML(); toast(`✏️ Named “${t}”`); } });
function fcNotify() {""", 1)
s = s.replace('</style>', """.two-tip{margin:8px 0 4px;padding:9px 12px;border-radius:12px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #D9AE4F;font:700 .86rem Nunito,system-ui;color:#5B3D06;text-align:left}.two-tip b{color:#14213D}.two-tip small{display:block;font:600 .76rem Nunito,system-ui;color:#5B4A3F}
.two-add{margin:4px 0 10px;padding:10px 12px;border-radius:14px;background:#FFF8E6;box-shadow:inset 0 0 0 1.5px #D9AE4F;text-align:left}.two-add b{font:800 .95rem Nunito,system-ui;color:#14213D}.two-add small{display:block;margin:2px 0 8px;font:600 .8rem Nunito,system-ui;color:#5B4A3F}
html body .nm-it{margin-left:4px;padding:2px 8px;border:0;border-radius:999px;background:#FFF1C9;color:#9A6B12;font:800 .68rem Nunito,system-ui;cursor:pointer;white-space:nowrap}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v180 ok')
# pass 2: start line matches the streak rule
s = open(d + 'yofi-real.html').read()
RA('<div><b>10</b><small>of your votes to start</small></div><div><b>2</b><small>horse live race</small></div>', '<div><b>2</b><small>in a row = 1 step</small></div><div><b>3</b><small>steps to a live race</small></div>')
RA("⚖️ <b>Your votes start its qualifier.</b> At 10 votes you watch it race a rival live. Win and it’s in the Final.", "⚖️ <b>Vote 2 in a row with the crowd to move it a step.</b> After 3 steps you watch it race a rival live. Win and it’s in the Final.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v180 pass2 ok')
# pass 3: start-line track shows the 3 steps
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function qlLiveTrack(p) { const q = p.ql || {}, pos = Math.min(1, (q.got || 0) / QS_STEPS);
  return `<div class="pv-tr ql-tr"><div class="pv-rail">${Array.from({ length: QS_STEPS - 1 }, (_, i) => `<i style="left:${(i + 1) / QS_STEPS * 100}%"></i>`).join('')}<u style="width:${pos * 100}%"></u></div><img class="pv-hz" id="qlHz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"><span class="pv-fl">🏁</span></div>`; }
function fcNotify() {""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v180 pass3 ok')
