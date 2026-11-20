# Real Money build, step 169 (after rmv165.py): a loop for photos that don't qualify — tune up, train, race again.
#  - Out screens: "🏋️ Tune up & train · free" (main) or "📷 Enter another photo" (100 🟡 as normal). No more free new photo.
#  - Tune-up (free, full screen): before/after of a one-tap enhancement (brighter, richer colour, slightly closer crop).
#    Apply it or keep the original. Like shoeing the horse before the race: maintenance, no levels.
#  - Training: the photo plays head-to-heads for coins, driven by your votes (one per vote). Each win: +5 🟡 and +1 form.
#    Losses cost nothing. 5 wins = "Race fit!" → re-enter the qualifier free. Form (and the tune-up) make it a bit stronger.
#  - Training shows as a card in "Your photos in play" (🏋️ Training · 3 of 5 wins · form +3).
#  Simulated: the crowd's votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const pvList = () => (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin));",
   "const pvList = () => (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || (p.tr && !p.tr.done)));")
RA("if (!was && p.ql && p.ql.done === 'x') { S.freeRe = 1; save(); }", "")
RA("Your next entry is on us: try another shot. Bright, close-up photos tend to win.", "Train it to race again: a free tune-up, then 5 head-to-heads for coins.")
RA("One win short. Your next entry is on us: bright, close-up shots tend to win.", "One win short. Train it to race again: a free tune-up, then 5 head-to-heads for coins.")
RA('<button class="btn block db-go cashb" id="qoE">📷 Try another photo · free</button>',
   '<button class="btn block db-go cashb" data-trn="${p.id}">🏋️ Tune up & train · free</button><button class="btn block db-go quiet" id="qoE">📷 Enter another photo</button>')
RA('<button class="btn block db-go cashb" id="qlvE">📷 Try another photo · free</button>',
   '<button class="btn block db-go cashb" data-trn="${p.id}">🏋️ Tune up & train · free</button><button class="btn block db-go quiet" id="qlvE">📷 Enter another photo</button>')
s = s.replace("function fcNotify() {", r"""const TR_WIN = 5;
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-trn]'); if (!b) return; e.preventDefault(); const p = (S.photos || []).find(x => x.id === b.dataset.trn); if (p) trTune(p); });
function trEnhance(src, done) { const im = new Image(); im.onload = () => { try { const k = .9, sw = im.naturalWidth * k, sh = im.naturalHeight * k, sc = Math.min(1, 1000 / Math.max(sw, sh)), cv = document.createElement('canvas');
    cv.width = Math.round(sw * sc); cv.height = Math.round(sh * sc); const c = cv.getContext('2d'); c.drawImage(im, (im.naturalWidth - sw) / 2, (im.naturalHeight - sh) / 2, sw, sh, 0, 0, cv.width, cv.height);
    const D = c.getImageData(0, 0, cv.width, cv.height), a = D.data, B = 1.07, C = 1.1, Sa = 1.22;
    for (let i = 0; i < a.length; i += 4) { let r = a[i] * B, g = a[i + 1] * B, b = a[i + 2] * B; r = (r - 128) * C + 128; g = (g - 128) * C + 128; b = (b - 128) * C + 128; const l = .3 * r + .59 * g + .11 * b;
      a[i] = Math.max(0, Math.min(255, l + (r - l) * Sa)); a[i + 1] = Math.max(0, Math.min(255, l + (g - l) * Sa)); a[i + 2] = Math.max(0, Math.min(255, l + (b - l) * Sa)); }
    c.putImageData(D, 0, 0); done(cv.toDataURL('image/jpeg', .88)); } catch (e) { done(null); } }; im.onerror = () => done(null); im.src = src; }
function trTune(p) { const nm = esc(rcName(p)); try { popClose(); } catch (e) {}
  popOpen(`<div class="pp qfx trt"><p class="pp-k">🏋️ Training · ${nm}</p><h2 class="db-h">Free tune-up</h2><p class="db-s">A quick service before it races again.</p>
    <div class="trt-ba"><figure><img src="${p.src}" alt=""><figcaption>Before</figcaption></figure><figure class="aft"><img id="trA" src="${p.src}" alt="" style="filter:brightness(1.07) contrast(1.1) saturate(1.22)"><figcaption>After ✨</figcaption></figure></div>
    <div class="trt-c"><span>☀️ Brighter</span><span>🎨 Richer colour</span><span>🔍 Closer crop</span></div>
    <button class="btn block db-go cashb" id="trY" ${p.tuned ? 'disabled' : ''}>${p.tuned ? '✨ Already tuned up' : '✨ Apply tune-up & train'}</button>
    <div style="text-align:center"><button class="link pc-later" id="trN">Keep it as it is & train</button></div></div>`);
  if (!p.tuned) trEnhance(p.src, u => { const a = document.getElementById('trA'); if (a && u) { a.src = u; a.style.filter = ''; a.dataset.u = u; } });
  $('#trY').onclick = () => { const a = document.getElementById('trA'), u = a && a.dataset.u; if (u) { p.src = u; } p.tuned = 1; qlStrength(p); p.vd.pct = Math.min(85, p.vd.pct + 6); trBegin(p, true); };
  $('#trN').onclick = () => trBegin(p, false); }
function trBegin(p, tuned) { p.tr = { w: 0, l: 0, at: Date.now() }; save(); const nm = esc(rcName(p));
  popOpen(`<div class="pp qfx qlv"><p class="pp-k">🏋️ Training${tuned ? ' · tuned up ✨' : ''}</p><h2 class="db-h">${nm} is in training</h2><div class="qlv-ph"><img src="${p.src}" alt=""></div>
    <div class="qls-r"><div><b>${TR_WIN}</b><small>wins to race again</small></div><div><b>+5 🟡</b><small>per win</small></div><div><b>💪</b><small>form grows</small></div></div>
    <p class="db-s">⚖️ <b>Each vote you make plays a training head-to-head.</b> Losses cost nothing. Win ${TR_WIN} and it re-enters the qualifier free.</p>
    <button class="btn block db-go" id="trGo">⚖️ Start training</button><p class="db-sim">Prototype: the crowd’s votes are simulated</p></div>`);
  $('#trGo').onclick = () => { popClose(); go('judge'); renderJudge(); }; }
function trStep(p) { const t = p.tr; if (!t || t.done) return; const pr = Math.max(.4, Math.min(.8, .52 + (qlStrength(p) - 62) / 80)), win = Math.random() < pr, o = qlOpp(p);
  if (win) { t.w++; p.form = Math.min(10, (p.form || 0) + 1); p.vd.pct = Math.min(85, p.vd.pct + 1); p.qc = (p.qc || 0) + 5; S.gems = (S.gems || 0) + 5; try { paintGems(); } catch (e) {} } else t.l++;
  t.last = { win, t: o.t, src: o.src }; if (t.w >= TR_WIN) { t.done = 1; setTimeout(function tf() { if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx')) { setTimeout(tf, 1200); return; } trFit(p); }, 1400); } save(); }
function trFit(p) { const nm = esc(rcName(p));
  popOpen(`<div class="pp qfx qlv"><p class="pp-k">🏋️ Training · ${p.tr.w} wins, ${p.tr.l} losses</p><h2 class="db-h qlv-win">${nm} is race fit!</h2><div class="qlv-ph"><img src="${p.src}" alt=""></div>
    <p class="re-rzl">💪 Form +${p.form || 0} · ${p.tr.w * 5} 🟡 earned in training</p><button class="btn block db-go cashb" id="trR">🎀 Re-enter the qualifier · free</button><div style="text-align:center"><button class="link pc-later" id="trL">Later</button></div></div>`);
  try { rvConfetti(document.querySelector('.qlv'), 40); } catch (e) {}
  $('#trR').onclick = () => { S.freeRe = 1; p.rq = (p.rq || 0) + 1; p.tr = null; p.ql = null; save(); popClose(); setTimeout(() => upDone(p), 200); };
  $('#trL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }
(() => { const cf = callFx; callFx = function () { const r = cf.apply(this, arguments); try { (S.photos || []).filter(p => p.tr && !p.tr.done).forEach(trStep); qlPaint(); } catch (e) {} return r; }; })();
function trCard(p) { const t = p.tr, pos = Math.min(1, t.w / TR_WIN), L = t.last, need = TR_WIN - t.w;
  return `<div class="pv-c trn" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">🏋️ Training${p.tuned ? ' ✨' : ''}</span><em>💪 Form +${p.form || 0}</em></div>
    <div class="pv-tr"><div class="pv-rail">${Array.from({ length: TR_WIN - 1 }, (_, i) => `<i style="left:${(i + 1) / TR_WIN * 100}%"></i>`).join('')}<u style="width:${pos * 100}%"></u></div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"><span class="pv-fl">🎀</span></div>
    <div class="pv-n"><span class="w">✓ ${t.w}</span><span class="l">✕ ${t.l}</span><span class="pv-need">${need > 0 ? `<b>${need} more win${need === 1 ? '' : 's'}</b> to race again · +5 🟡 each` : '<b>Race fit!</b>'}</span></div>
    <p class="pv-l ${L ? (L.win ? 'w' : 'l') : ''}">${L ? (L.win ? `✓ Beat “${esc(L.t)}” · +5 🟡 · form +1` : `✕ Lost to “${esc(L.t)}” · no harm in training`) : '⚖️ Each vote you make plays a training round'}</p></div>`; }
(() => { const pc = pvCard; pvCard = function (p) { return p.tr && !p.tr.done ? trCard(p) : pc.apply(this, arguments); }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.trt-ba{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}.trt-ba figure{margin:0}.trt-ba img{display:block;width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px;box-shadow:0 0 0 2px #EADCC6}
.trt-ba .aft img{box-shadow:0 0 0 3px #D9AE4F,0 4px 14px rgba(217,174,79,.35)}.trt-ba figcaption{margin-top:5px;font:800 .78rem Nunito,system-ui;color:#5B4A3F}.trt-ba .aft figcaption{color:#9A6B12}
.trt-c{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin:0 0 12px}.trt-c span{padding:4px 10px;border-radius:999px;background:#FFF1C9;font:800 .76rem Nunito,system-ui;color:#5B3D06}
.pv-c.trn{box-shadow:inset 0 0 0 2px #2E4F8A;background:#F6F8FC}.pv-c.trn .pv-rail u{background:linear-gradient(90deg,#8FA8D6,#2E4F8A)}.pv-c.trn .pv-hz{box-shadow:0 0 0 3px #fff,0 0 0 5px #2E4F8A,0 3px 8px rgba(0,0,0,.25)}
.pv-c.trn .pv-t em{background:#E3EAF5;color:#2E4F8A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v166 ok')
# pass 2: wording — training is "win 5", losses don't count
s = open(d + 'yofi-real.html').read()
s = s.replace("a free tune-up, then 5 head-to-heads for coins.", "a free tune-up, then win 5 head-to-heads for coins.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v166 pass2 ok')
