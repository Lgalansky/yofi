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
    return { p, t: `${nm} earns ${rate} coins a pick`, s: 'Picks pay out here', cta: 'Earn more', act: () => jarGoImprove(p) }; }
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
// ---- one clear earnings line on every photo screen: what a voter's pick pays this photo ----
stLine = function (v, from) {
  const t = galTier(v), pay = GAL.BASE * galMult(v), ci = gemIcon('gem st-ci');
  if (from != null) { const t0 = galTier(from), p0 = GAL.BASE * galMult(from);
    if (p0 !== pay) return `${t && t !== t0 ? `${TIER_IC[t]} ${t} · each` : 'Each'} voter pick ${p0} → <b>${pay}</b>${ci}`; }
  const nx = galNextMult(v), nb = !t ? 70 : null;
  return `${t ? `${TIER_IC[t]} ${t} · each` : 'Each'} voter pick earns <b>${pay}</b>${ci}${nb ? ` · 🥇 ${nb}+ earns ${GAL.BASE * galMult(nb)}` : ''}`;
};

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
assert s.count(a) == 1; s = s.replace(a, '<b>${GAL.BASE * x}</b>${gemIcon("gem st-ci")} a pick · <em>+${d} today</em>')
CSS += '.st-ci{width:1em;height:1em;vertical-align:-.15em;margin-left:2px}\n'
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('collect ok')
