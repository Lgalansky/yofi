# Skill preview: retention beats borrowed from village games, without coin sinks.
# 1. The coin jar fills over time from votes on your photos and holds 8 hours of earnings.
#    The Vote card counts down ("Full in 3h 20m"); once full it says so and stops filling until collected.
# 2. Completing a collection (all 3 photos reach a new level) is a big moment that pays a
#    free $1 cash challenge entry (a ticket), used straight from the pop.
# usage: python3 build-skill/jarfull.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# the old one-off "while you were away" credit is replaced by the jar filling over time
rep("function vgAwayCheck(now = Date.now()) {\n  if (!S.user) return;", "function vgAwayCheck(now = Date.now()) {\n  return;")

# the app always opens on Vote (it used to open signed-in players on Compete)
rep("paintGems(false); if (S.user) openBattleTab(); }", "paintGems(false); if (S.user) { GV.tab = 'battle'; go('judge'); } }")
rep("renderStudio(); paintGems(false); openBattleTab(); }", "renderStudio(); paintGems(false); GV.tab = 'battle'; go('judge'); }")

JS = r'''
// ---- 1. a jar that fills over time and holds 8 hours ----
const JAR_HRS = 8;
const jarHung = () => GAL.PATH.filter(galOpen).flatMap(c => galRoom(c).ph).filter(p => p.s);
const jarRate = () => jarHung().reduce((a, p) => a + GAL.BASE * galMult(p.s.total) * Math.max(.5, 1 + (p.s.total - 55) / 15), 0); // coins an hour
const jarCap = () => Math.max(20, Math.round(jarRate() * JAR_HRS));
const jarFull = () => (S.vgJar || 0) >= jarCap();
const jarLeft = () => { const r = jarRate(); if (!r) return ''; const h = Math.max(0, (jarCap() - (S.vgJar || 0)) / r), hh = Math.floor(h), mm = Math.round((h - hh) * 60); return hh ? `${hh}h ${mm}m` : `${Math.max(1, mm)}m`; };
function jarTick(now = Date.now()) {
  if (!S.user) return; const last = S.jarAt || now; S.jarAt = now; const r = jarRate(); if (!r) { save(); return; }
  const room = jarCap() - (S.vgJar || 0); if (room <= 0) { S.jarF = 0; save(); return; }
  const f = (S.jarF || 0) + r * Math.max(0, now - last) / 36e5, add = Math.min(room, Math.floor(f)); S.jarF = add < Math.floor(f) ? 0 : f - add;
  if (add > 0) { S.vgJar = (S.vgJar || 0) + add; S.jarTime = (S.jarTime || 0) + add; if (now - last > 10 * 60000) { S.vgTurn = 0; S.jarAway = 1; } }
  save();
}
// picks while you vote still drop in, up to the cap
const _jarAddF = jarAdd;
jarAdd = function (n, p) { const room = jarCap() - (S.vgJar || 0); if (room <= 0) { S.gems -= n; save(); return; } const k = Math.min(n, room); _jarAddF(k, p); if (n > k) { S.gems -= n - k; save(); } };
// coins from time get credited to the photos that earned them (gallery "+N today")
const _jarCollectF = jarCollect;
jarCollect = function () { const t = Math.min(S.jarTime || 0, S.vgJar || 0); if (t > 0) { const H = jarHung(), w = H.map(p => GAL.BASE * galMult(p.s.total) * Math.max(.5, 1 + (p.s.total - 55) / 15)), W = w.reduce((a, b) => a + b, 0) || 1, d = todayKey(); let left = t;
    H.forEach((p, i) => { const m = i === H.length - 1 ? left : Math.round(t * w[i] / W); left -= m; if (p.gd !== d) { p.gd = d; p.gt = 0; } p.gt += m; p.gl = (p.gl || 0) + m; p.gv = (p.gv || 0) + Math.round(m / (GAL.BASE * galMult(p.s.total))); }); }
  S.jarTime = 0; S.jarAway = 0; S.jarAt = Date.now(); S.jarF = 0; return _jarCollectF.apply(this, arguments); };
jarTick(); setInterval(() => { const j0 = S.vgJar || 0; jarTick(); if ((S.vgJar || 0) !== j0 && $('#panes').dataset.at === 'judge') try { vgPaint(); } catch (e) {} }, 30000);
// the card: full, or counting down to full
const _vgGoalF = vgGoal;
vgGoal = function () { let g = _vgGoalF.apply(this, arguments);
  // the jar takes its turn in the rotation (and always shows when full)
  if (g && g.jar && !jarFull() && (S.vgTurn || 0) % 3 !== 0) { const j = S.vgJar; S.vgJar = 0; try { g = _vgGoalF.apply(this, arguments) || g; } finally { S.vgJar = j; } }
  if (g && g.jar) { const full = jarFull();
    if (full) { g.t = 'Your coin jar is full!'; g.s = 'Collect to keep earning'; g.full = 1; }
    else { if (!S.vgJarN || S.jarAway) g.t = S.jarAway ? 'Picked while you were away' : 'Voters picked your photos'; g.s = `Jar full in ${jarLeft()}`; } }
  return g; };
const _vgPaintF = vgPaint;
vgPaint = function () { _vgPaintF.apply(this, arguments); const el = $('#vgGoal'); if (!el) return; const g = vgGoal();
  el.classList.toggle('jar-full', !!(g && g.full));
  const tx = el.querySelector('.vg-tx'); if (tx) { let m = tx.querySelector('.jar-m'); if (g && g.jar) { if (!m) { tx.insertAdjacentHTML('beforeend', '<span class="jar-m"><i></i></span>'); m = tx.querySelector('.jar-m'); } m.firstChild.style.width = Math.min(100, Math.round((S.vgJar || 0) / jarCap() * 100)) + '%'; } else if (m) m.remove(); } };


// the jar on the Vote tab: coins waiting, or FULL
function jarTab() { const b = $('#segJudge'); if (!b) return; let t = b.querySelector('.jar-tb'); const n = S.user ? (S.vgJar || 0) : 0;
  if (!n) { if (t) t.remove(); return; }
  if (!t) { b.style.position = 'relative'; b.insertAdjacentHTML('beforeend', '<i class="jar-tb" aria-hidden="true"></i>'); t = b.querySelector('.jar-tb'); }
  const full = jarFull(); t.classList.toggle('full', full); t.textContent = full ? 'FULL' : `+${n}`;
  b.setAttribute('aria-label', full ? 'Vote. Your coin jar is full' : `Vote. ${n} coins in your jar`); }
setInterval(() => { try { jarTab(); } catch (e) {} }, 1000);
// ---- 2. completing a collection: a big moment that pays a free $1 cash challenge ----
const _galCeleF = galCele;
galCele = function (ev) { const key = ev.c + '_' + ev.tier; S.galTix = S.galTix || {}; const fresh = !S.galTix[key];
  if (fresh) { S.galTix[key] = Date.now(); S.cashTix = (S.cashTix || 0) + 1; save(); }
  _galCeleF.apply(this, arguments);
  if (!fresh) return;
  try { const box = document.querySelector('#coach .gl-pop'), gb = $('#glpGo'), no = $('#glpNo'), opened = ev.opened;
    box.classList.add('gl-big'); box.querySelector('p').insertAdjacentHTML('afterend', `<div class="gl-tix" aria-label="Reward: a free one dollar cash challenge"><span class="gl-tx-ic">🎟️</span><span><small>Collection reward</small><b>Free $1 cash challenge</b><em>Win stars for today’s cash prize</em></span></div>`);
    gb.textContent = '🎟️ Play my free challenge'; gb.classList.add('pay-cash', 'tix-go');
    no.textContent = opened ? `Open ${galNm(opened)}` : 'Later';
    const close = () => { const co = $('#coach'); co.classList.remove('on', 'cr'); co.innerHTML = ''; };
    gb.onclick = () => { close(); tixPlay(ev.c); };
    no.onclick = () => { close(); if (opened) { S.galCat = opened; TU_GAL = true; save(); go2studio(); } };
  } catch (e) {} };
const go2studio = () => { go('studio'); try { renderStudio(); } catch (e) {} };
function tixPlay(c) { const k = CATS8.includes(c) && lgMine(c) ? c : CATS8.find(x => lgMine(x)) || null;
  goCash(); LG_FEE = 1; S.lgStake = 1; save(); openBattleTab();
  setTimeout(() => { if (k) lgCat(k); else toast('Get a photo to 70+ to play your free entry'); }, 350); }
// the $1 chip shows when an entry is free
const _lgCatF = lgCat;
lgCat = function (k) { const r = _lgCatF.apply(this, arguments);
  try { if ((S.cashTix || 0) > 0) { const c = document.querySelector('#sheetBody [data-sk="1"]'); if (c && !c.querySelector('.sk-free')) { c.classList.add('sk-fr'); c.insertAdjacentHTML('afterbegin', '<i class="sk-free">FREE</i>'); }
    if (LG_FEE === 1) { const b = $('#lgQuick'); if (b) { b.innerHTML = b.innerHTML.replace(/· \$1$/, '· Free 🎟️'); b.classList.add('pay-cash', 'sk-gobtn'); } } } } catch (e) {}
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* jar fill meter + full state */
#vgGoal .jar-m{display:block;height:6px;margin-top:6px;border-radius:9px;background:#EBD9AE;overflow:hidden}#vgGoal .jar-m i{display:block;height:100%;background:linear-gradient(90deg,#E0A82E,#F3D27A);border-radius:9px;transition:width .8s ease}
#vgGoal .vg-tx small{margin-top:2px!important}
html body #vgGoal.jar-full{animation:jarFullG 1.4s ease-in-out infinite}
@keyframes jarFullG{0%,100%{box-shadow:inset 0 0 0 2px #E0A82E,0 0 0 0 rgba(224,168,46,.5)}50%{box-shadow:inset 0 0 0 2px #E0A82E,0 0 0 7px rgba(224,168,46,.18)}}
html body #vgGoal.jar-full .vg-tx b{color:#8A3B00!important}
/* jar badge on the Vote tab */
.jar-tb{position:absolute;top:-4px;left:50%;margin-left:12px;display:inline-flex;align-items:center;gap:2px;padding:2px 7px 2px 6px;border-radius:99px;font:900 .72rem/1.2 "Nunito Sans",sans-serif;font-style:normal;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;box-shadow:0 2px 5px rgba(0,0,0,.25);pointer-events:none;white-space:nowrap}
html body #segJudge .jar-tb svg{width:11px!important;height:11px!important;margin:0!important}
.jar-tb.full{background:linear-gradient(180deg,#FFB547,#E07A1E);color:#fff;letter-spacing:.06em;animation:jarTb 1.2s ease-in-out infinite}
@keyframes jarTb{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}
@media (prefers-reduced-motion:reduce){.jar-tb.full{animation:none}}
/* collection reward ticket */
.gl-tix{display:flex;align-items:center;gap:12px;margin:12px auto 4px;max-width:300px;padding:12px 14px;border-radius:16px;text-align:left;background:linear-gradient(180deg,#E9F7EE,#CFEBD9);box-shadow:inset 0 0 0 2px #7FBE91,0 8px 18px -10px rgba(33,120,74,.6);animation:tixIn .7s .5s cubic-bezier(.2,1.4,.4,1) both;position:relative}
.gl-tix::before,.gl-tix::after{content:"";position:absolute;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:#FFF8EA}.gl-tix::before{left:-7px}.gl-tix::after{right:-7px}
.gl-tx-ic{font-size:2.2rem;line-height:1}.gl-tix small{display:block;font:800 .7rem "Nunito Sans",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#2E6B42}.gl-tix b{display:block;font:900 1.2rem/1.15 Fraunces,serif;color:#1E5233}.gl-tix em{display:block;font:700 .82rem "Nunito Sans",sans-serif;font-style:normal;color:#2E6B42}
@keyframes tixIn{0%{transform:scale(.4) rotate(-8deg);opacity:0}100%{transform:none;opacity:1}}
.sk-row button.sk-fr{position:relative}html body #coach #glpGo.tix-go{background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important;box-shadow:0 8px 18px -8px rgba(33,120,74,.7)!important}html body #sheetBody .sk-gobtn{background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important}.sk-free{position:absolute;top:-8px;right:-4px;font:900 .62rem "Nunito Sans",sans-serif;font-style:normal;letter-spacing:.05em;padding:2px 6px;border-radius:99px;background:#E0A82E;color:#3A2600}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('jarfull ok')
