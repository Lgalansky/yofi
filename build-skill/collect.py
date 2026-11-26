# Skill preview: the top Vote card makes it clear your photos earn coins.
# Each time a voter picks one of your photos, its coins go into a jar on the card
# ("3 voters picked Sterling"); the gold button shows the coins waiting ("+6 🟡"),
# pulses, and ticks up on each pick. Tap it and the coins fly into your balance.
# With nothing to collect, the earnings card explains the rate and links to Improve.
# usage: python3 build-skill/collect.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- coin jar on the top Vote card ----
let JAR_HOLD = 0, JAR_SHOWN = null;
const _gemExplosionJ = gemExplosion;
gemExplosion = function () { if (Date.now() - JAR_HOLD < 1500) return; return _gemExplosionJ.apply(this, arguments); };
function jarAdd(n, p) { if (!(n > 0)) return; S.vgJar = (S.vgJar || 0) + n; S.vgJarN = (S.vgJarN || 0) + 1;
  if (p) { if (S.vgJarP && S.vgJarP !== p.id) S.vgJarMix = 1; S.vgJarP = p.id; } S.gems -= n; save(); }
const _galPickJ = galPick;
galPick = function () { const g0 = S.gems, before = new Map(S.photos.map(x => [x.id, x.gl || 0])); JAR_HOLD = Date.now();
  _galPickJ.apply(this, arguments);
  const d = S.gems - g0; if (d > 0) { const p = S.photos.find(x => (x.gl || 0) > (before.get(x.id) || 0)); jarAdd(d, p); try { paintGems(); vgPaint(); } catch (e) {} } };
// coins earned while away go into the jar too
if (typeof VG_AWAY !== 'undefined' && VG_AWAY && !VG_AWAY.shown) { const a = VG_AWAY; VG_AWAY = null; S.vgJar = (S.vgJar || 0) + a.tot; S.vgJarAway = 1; S.gems -= a.tot; if (a.top) S.vgJarP = a.top.id; save(); }
const jarPhoto = () => S.photos.find(x => x.id === S.vgJarP) || S.photos.filter(x => x.s).sort((a, b) => (b.gl || 0) - (a.gl || 0))[0];
function jarCollect() { const n = S.vgJar || 0; if (!n) return; const from = document.querySelector('#vgGoal .vg-cta');
  S.gems += n; S.vgJar = 0; S.vgJarN = 0; S.vgJarMix = 0; S.vgJarAway = 0; S.vgTurn = 0; save(); JAR_HOLD = 0; JAR_SHOWN = null;
  try { _gemExplosionJ(n, { mid: 1, from }); } catch (e) { paintGems(); }
  setTimeout(() => { try { vgPaint(); } catch (e) {} }, 650); }
function jarGoImprove(p) { if (!p) return; S.cur = p.id; save(); TU_GAL = false; WALL = false; go('studio'); renderStudio(); }
const _vgGoalJ = vgGoal;
vgGoal = function () {
  if (S.user && (S.vgJar || 0) > 0) { const p = jarPhoto(), nm = p ? alName(p) : 'your photo', n = S.vgJarN || 0;
    const t = S.vgJarAway ? `Voters picked ${S.vgJarMix ? 'your photos' : nm} while you were away` : n === 1 ? `A voter picked ${nm}` : `${n} voters picked ${S.vgJarMix ? 'your photos' : nm}`;
    return { p, jar: S.vgJar, t, s: 'Tap to collect', cta: `+${S.vgJar}`, act: jarCollect }; }
  const g = _vgGoalJ.apply(this, arguments);
  if (g && g.earn != null && g.p) { const p = g.p, rate = GAL.BASE * galMult(p.s.total), nm = alName(p);
    return { p, t: `${nm} earns you ${rate} coins per vote`, s: 'Votes pay out here', cta: 'Earn more', act: () => jarGoImprove(p) }; }
  return g;
};
const _vgPaintJ = vgPaint;
vgPaint = function () { _vgPaintJ.apply(this, arguments);
  const el = $('#vgGoal'); if (!el) return; const g = vgGoal(); const c = el.querySelector('.vg-cta');
  el.classList.toggle('jar', !!(g && g.jar)); if (!c) return;
  if (!(g && g.jar)) { c.classList.remove('jar-cta'); JAR_SHOWN = null; return; }
  el.classList.remove('earn'); el.onclick = jarCollect; el.setAttribute('aria-label', `${g.t}. Collect ${g.jar} coins`);
  c.classList.add('jar-cta'); const from = JAR_SHOWN == null ? g.jar : JAR_SHOWN, to = g.jar; JAR_SHOWN = to;
  c.innerHTML = `<span class="jar-n">+${from}</span>${gemIcon('gem jar-ic')}`;
  if (to !== from) { el.classList.remove('jar-pop'); void el.offsetWidth; el.classList.add('jar-pop');
    const n = c.querySelector('.jar-n'), t0 = performance.now();
    const tick = t => { if (!n.isConnected) return; const k = Math.min(1, (t - t0) / 800); n.textContent = '+' + Math.round(from + (to - from) * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick); }
};
// one rate per level, so the line is always true: Gold 4, Diamond 8, Platinum 12 (unranked 2)
GAL.MULT = [[90, 6], [80, 4], [70, 2], [0, 1]];
const _im2LevelsL = im2Levels;
im2Levels = function () { const r = _im2LevelsL.apply(this, arguments);
  try { const b = $('#sheetBody'); b.innerHTML = b.innerHTML.replace(/(\d+)–\1 coins/g, '$1 coins').replace(/(\d+) coins/g, '$1 per vote').replace('Each time a voter picks your photo, it earns coins.', 'Your photo earns coins every time a voter picks it.').replace('about 25 picks', 'about 25 votes'); if (b.querySelector('.btn')) b.querySelectorAll('[data-shclose], .btn').forEach(x => x.onclick = () => closeSheet()); } catch (e) {}
  return r; };

// a photo reaching a new level: celebrate with what it now earns
function lvUp(p, t) { const pay = GAL.BASE * galMult(p.s.total);
  celebrate({ src: p.src, score: p.s.total, title: `${alName(p)} is ${t}!`, text: `${TIER_IC[t] || ''} ${esc(alName(p))} now earns you <b>${pay} 🟡 per vote</b>.`,
    cta: '🗳 Back to voting', onCta: () => go('judge'), later: 'Keep improving' }); }

// gallery sleeves: level icon on the photo, today's earnings as a gold pill on the photo, rate underneath
const _renderGalleriesE = renderGalleries;
renderGalleries = function () { const r = _renderGalleriesE.apply(this, arguments);
  try { document.querySelectorAll('#studio .a2-sl[data-alc]').forEach(b => { const p = S.photos.find(x => x.id === b.dataset.alc); if (!p || !p.s) return;
    const t = galTier(p.s.total), sc = b.querySelector('.a2-sc'), ph = b.querySelector('.a2-ph'), l2 = b.querySelector('.a2-l2'), d = galToday(p), pay = GAL.BASE * galMult(p.s.total);
    if (sc && t && !sc.querySelector('.a2-ti')) sc.insertAdjacentHTML('afterbegin', `<i class="a2-ti">${TIER_IC[t]}</i>`);
    if (ph && !ph.querySelector('.a2-earn')) ph.insertAdjacentHTML('beforeend', d > 0 ? `<em class="a2-earn"><b>+${d}</b>${gemIcon('gem a2-eic')}<small>today</small></em>` : `<em class="a2-earn none"><small>Earns on votes</small></em>`);
    if (l2) l2.innerHTML = `Earns <b>${pay}</b>${gemIcon('gem st-ci')} per vote`; }); } catch (e) {}
  return r; };
// ---- one clear earnings line on every photo screen: what a voter's pick pays this photo ----
stLine = function (v, from) {
  const t = galTier(v), pay = GAL.BASE * galMult(v), ci = gemIcon('gem st-ci');
  if (from != null) { const t0 = galTier(from), p0 = GAL.BASE * galMult(from);
    }
  const nx = galNextMult(v), nb = !t ? 70 : null;
  return t ? `${TIER_IC[t]} ${t} photos earn you <b>${pay}</b>${ci} per vote` : `Earns you <b>${pay}</b>${ci} per vote · 🥇 Gold earns ${GAL.BASE * galMult(nb)}`;
};

// ---- score on its own full-width line, earnings line right under it (Improve and Before and after) ----
const _im2RenderL = im2Render;
im2Render = function () { const r = _im2RenderL.apply(this, arguments);
  try { const g = document.querySelector('#studio .im2 .im2-grid'), sr = document.querySelector('#studio .im2 .im2-sr'), lb = document.querySelector('#studio .im2 .im2-lb'), strip = document.querySelector('#studio .im2 .im2-strip');
    if (g && sr && !document.querySelector('#studio .im2-scb')) { const bar = document.createElement('div'); bar.className = 'im2-scb'; bar.innerHTML = '<small class="im2-scl">Score now</small>'; bar.appendChild(sr); if (lb) lb.remove(); g.before(bar); if (strip) bar.after(strip); } } catch (e) {}
  return r; };
const _renderVariantsL = renderVariants;
renderVariants = function () { const r = _renderVariantsL.apply(this, arguments);
  try { const fb = $('#flowBody'), sc = fb.querySelector('.ba-sc'), ls = [...fb.querySelectorAll('.st-line')]; if (sc && ls.length) { const keep = ls.pop(); ls.forEach(x => x.remove()); sc.after(keep); keep.classList.add('st-top'); } } catch (e) {}
  return r; };

setTimeout(() => { try { vgPaint(); } catch (e) {} }, 350);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* coin jar button on the top Vote card */
html body #vgGoal .vg-cta.jar-cta{display:inline-flex;align-items:center;gap:5px;padding:10px 14px!important;font:900 1.15rem Fraunces,serif!important;animation:jarPulse 1.6s ease-in-out infinite;position:relative;overflow:hidden}
#vgGoal .jar-ic{width:20px;height:20px}
#vgGoal .vg-cta.jar-cta::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.65) 50%,transparent 70%);transform:translateX(-120%);animation:jarShine 2.4s ease-in-out infinite}
@keyframes jarPulse{0%,100%{transform:scale(1);box-shadow:0 4px 10px -5px rgba(160,110,10,.6)}50%{transform:scale(1.07);box-shadow:0 0 0 5px rgba(224,168,46,.28),0 6px 14px -5px rgba(160,110,10,.7)}}
@keyframes jarShine{0%,55%{transform:translateX(-120%)}85%,100%{transform:translateX(120%)}}
#vgGoal.jar-pop{animation:jarBump .5s ease-out}
@keyframes jarBump{0%{transform:scale(1)}35%{transform:scale(1.03)}100%{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){html body #vgGoal .vg-cta.jar-cta,#vgGoal .vg-cta.jar-cta::after,#vgGoal.jar-pop{animation:none}}
'''
a = '<b>${x}×</b> per vote · <em>+${d} today</em>'
assert s.count(a) == 1; s = s.replace(a, '<b>${GAL.BASE * x}</b>${gemIcon("gem st-ci")} per vote · <em>+${d} today</em>')
CSS += '.st-ci{width:1em;height:1em;vertical-align:-.15em;margin-left:2px}\n'
CSS += """
/* Improve: score bar like Before and after, earnings line under it */
html body .im2 .im2-scb{display:flex;align-items:center;gap:10px;margin:0 14px 8px;padding:8px 14px;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(60,40,20,.45)}
.im2-scl{font:800 .74rem "Nunito Sans",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#4E433C}
html body .im2 .im2-scb .im2-sr{flex:1;display:flex;align-items:center;justify-content:space-between;margin:0}
html body .im2 .im2-scb #i2Score{font:900 2.4rem/1 Fraunces,serif!important;color:#2E6B42!important}
html body .im2 .im2-scb + .im2-strip{margin:0 14px 12px!important}
html body .im2 .im2-side{justify-content:center}
html body #flowBody .st-line.st-top{margin:-4px 0 12px!important}
html body .im2 .im2-scb ~ .im2-grid{margin-bottom:14px!important}
"""

# level-ups celebrate with the coin rate; the last "2×" wording becomes coins per vote
for a, b in [
  ("toast(t1 !== t0 && t1 ? `${alName(p)} is ${t1}! ${p.s.total} · ${x1}× coins per vote` : x1 > x0 ? `${alName(p)} ${v0} → ${p.s.total} · now ${x1}× coins per vote`",
   "(t1 !== t0 && t1 ? () => lvUp(p, t1) : toast)(t1 !== t0 && t1 ? '' : x1 > x0 ? `${alName(p)} ${v0} → ${p.s.total} · now earns you ${GAL.BASE * x1} 🟡 per vote`"),
  ("toast(t1 !== run.t0 && t1 ? `${alName(p)} is ${t1}! ${p.s.total} · ${x1}× coins per vote` : x1 > run.x0 ? `${alName(p)} ${run.v0} → ${p.s.total} · now ${x1}× coins per vote`",
   "(t1 !== run.t0 && t1 ? () => lvUp(p, t1) : toast)(t1 !== run.t0 && t1 ? '' : x1 > run.x0 ? `${alName(p)} ${run.v0} → ${p.s.total} · now earns you ${GAL.BASE * x1} 🟡 per vote`"),
  ("· ${x1}× coins every time a voter picks it`", "· earns you ${GAL.BASE * x1} 🟡 per vote`"),
  ("to earn ${nx.x}× per vote`, s: `Earning ${galMult(p.s.total)}× now ·", "to earn ${GAL.BASE * nx.x} per vote`, s: `Earns ${GAL.BASE * galMult(p.s.total)} per vote now ·"),
  ("t: nx ? `Improve ${name} to ${nx.at} to earn ${nx.x}× per vote`", "t: nx ? `Get ${name} to ${nx.at} to earn ${GAL.BASE * nx.x} per vote`"),
  ("They now earn at least <b>${galMult(band)}× coins</b> every time a voter picks them.", "They now earn you at least <b>${GAL.BASE * galMult(band)} 🟡 per vote</b>."),
  ('<div class="al-bot"><b>${x}× coins</b><span>${GAL.BASE * x} coins per vote received</span></div>',
   '<div class="al-bot"><b class="al-lv">${t ? `${({ Gold: "🥇", Diamond: "💎", Platinum: "🏆" })[t]} ${t}` : "Not ranked"}</b><span class="al-td"><em>+${galToday(p)}</em>${gemIcon("gem al-tic")}<small>today</small></span></div>'),
  ("<small>${galMult(p.s.total)}× · +${galToday(p)} today</small>", "<small>${GAL.BASE * galMult(p.s.total)} per vote · +${galToday(p)} today</small>"),
  ("for ${galMult(band)}× coins per vote`", "to earn ${GAL.BASE * galMult(band)} per vote`"),
  ("earns <b>${x}×</b> per vote${nm ? ` · <b>${nm.at}</b> pays ${nm.x}×` : ''}", "earns you <b>${GAL.BASE * x}</b> per vote${nm ? ` · <b>${nm.at}+</b> earns ${GAL.BASE * nm.x}` : ''}"),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
CSS += """
/* gallery: level icon + earnings on the photo */
html body .a2-sc{display:inline-flex!important;align-items:center;gap:3px}.a2-ti{font-style:normal;font-size:.9em;line-height:1}
html body .a2-ph{position:relative}
.a2-earn{position:absolute;left:6px;bottom:6px;display:inline-flex;align-items:center;gap:3px;padding:4px 9px 4px 8px;border-radius:999px;font-style:normal;background:linear-gradient(180deg,#FFF6DA,#F3D27A);box-shadow:0 3px 8px rgba(0,0,0,.35),inset 0 0 0 1.5px #E0A82E;color:#3A2600;animation:a2Earn .6s ease-out}
.a2-earn b{font:900 1.05rem/1 Fraunces,serif}.a2-earn small{font:800 .66rem "Nunito Sans",sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#6A4A10;margin-left:2px}
.a2-earn .a2-eic{width:16px;height:16px}
.a2-earn.none{background:rgba(255,253,249,.92);box-shadow:0 2px 6px rgba(0,0,0,.25);animation:none}.a2-earn.none small{margin:0;color:#4E433C}
@keyframes a2Earn{0%{transform:scale(.6);opacity:0}70%{transform:scale(1.08);opacity:1}100%{transform:scale(1)}}
html body .al-bot .al-lv{font-size:1.6rem!important}html body .al-card.big .al-sc em,html body .al-card.big .al-gem{display:none!important}.al-td small{white-space:nowrap}html body #studio .st-line{text-align:center!important}html body #studio .st-line .im2-sh{text-align:center;font-weight:700}.al-td{display:inline-flex;align-items:center;gap:5px;margin-left:auto}.al-td em{font:900 1.6rem/1 Fraunces,serif;font-style:normal;color:#8A5A0A!important}.al-td .al-tic{width:22px;height:22px}.al-td small{font:800 .8rem "Nunito Sans",sans-serif;color:#4E433C}
html body .a2-l2{font-size:.86rem!important;color:#4E433C}html body .a2-l2 b{font:900 1.05rem Fraunces,serif;color:#8A5A0A}
"""
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('collect ok')
