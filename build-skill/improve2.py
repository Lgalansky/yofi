# Improve, in the gallery card style (Skill preview, option A). Runs after album2.py.
# Replaces the old touch-up screen on the Improve tab:
# - The photo's card (tier foil, name, tier badge, score) with "Hold to compare" and a burgundy band that previews
#   the effect on earnings: "3× → 4× coins per vote · Sharpen details · 78 → 80 · Diamond".
# - Four touch-ups: Fix lighting (+3), Boost colour (+2), Sharpen details (+2), Soften background (+4); each can be
#   used 3 times and gains 1 less each time. Each tile shows the score it gets you and its price (Skill's touch-up price).
# - Premium filters (Suncast, Velvet, Nocturne) unlock at 80 and cost 1.5x.
# - A line when the touch-up completes a collection or opens the next one; Apply button with the price recessed;
#   short of coins -> "Need 40 more coins · Vote to earn".
# Scores stay consistent with the rest of Skill: the matching part score goes up (Lighting, Colour, Technical,
# Composition) so the overall score (the average of the five) rises by the gain. The look is baked into the photo.
# Usage: python3 build-skill/improve2.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function al2Card(' not in s: sys.exit('run album2.py first')
if 'function im2Render(' in s: sys.exit('improve2 already applied')

JS = r'''
/* ---------- Improve, card style ---------- */
const IM2 = {
  EDITS: [{ k: 'light', t: 'Fix lighting', v: 'Apply lighting fix', g: 3, part: 'light', f: 'brightness(1.07) contrast(1.03)' },
    { k: 'colour', t: 'Boost colour', v: 'Apply colour boost', g: 2, part: 'colour', f: 'saturate(1.2)' },
    { k: 'sharp', t: 'Sharpen details', v: 'Apply sharpening', g: 2, part: 'tech', f: 'contrast(1.09)' },
    { k: 'bg', t: 'Soften background', v: 'Apply soft background', g: 4, part: 'comp', f: 'none', vig: .45 }],
  PREM: [{ k: 'suncast', t: 'Suncast', v: 'Apply Suncast', g: 4, part: 'subject', f: 'sepia(.16) saturate(1.15)', warm: .5 },
    { k: 'velvet', t: 'Velvet', v: 'Apply Velvet', g: 3, part: 'colour', f: 'contrast(1.06) saturate(1.1) brightness(.98)' },
    { k: 'nocturne', t: 'Nocturne', v: 'Apply Nocturne', g: 3, part: 'tech', f: 'contrast(1.1) saturate(.92)', vig: .35 }],
  LEVELS: 3, PLEVELS: 2, PREM_AT: 80
};
let IM2SEL = null, IM2PID = null;
const im2All = () => IM2.EDITS.concat(IM2.PREM);
function im2Opts(p) {
  const lv = p.ed || {}, base = fixCost(p), out = IM2.EDITS.map(e => { const l = lv[e.k] || 0; return { ...e, l, max: l >= IM2.LEVELS, gain: Math.max(1, e.g - l), price: base }; });
  if (p.s.total >= IM2.PREM_AT) IM2.PREM.forEach(e => { const l = lv[e.k] || 0; out.push({ ...e, prem: 1, l, max: l >= IM2.PLEVELS, gain: Math.max(1, e.g - 2 * l), price: Math.round(base * 1.5) }); });
  return out;
}
// raise the part scores so the overall (average of five) goes up by gain; returns the new score object
function im2Raise(s0, part, gain) {
  const s = { ...s0 }, K = ['light', 'comp', 'colour', 'subject', 'tech'], target = Math.min(99, s0.total + gain);
  let need = target * 5 - K.reduce((a, k) => a + s[k], 0), guard = 0;
  const add = (k, n) => { const room = 99 - s[k], d = Math.max(0, Math.min(room, n)); s[k] += d; need -= d; };
  add(part, need);
  while (need > 0 && guard++ < 20) { const k = K.filter(x => s[x] < 99).sort((a, b) => s[a] - s[b])[0]; if (!k) break; add(k, Math.min(need, 5)); }
  s.total = Math.min(99, Math.round(K.reduce((a, k) => a + s[k], 0) / 5)); return s;
}
function im2Proj(p, o) { return im2Raise(p.s, o.part, o.gain).total; }
const im2Tier = v => galTier(v);
function im2Look(sel) { const o = sel && im2All().find(e => e.k === sel); return o ? { f: o.f, vig: o.vig || 0, warm: o.warm || 0 } : { f: 'none', vig: 0, warm: 0 }; }
// bake the look into the photo so every screen shows the touched-up version
function im2Bake(p, o, done) {
  const im = new Image(); im.onload = () => { try {
    const c = document.createElement('canvas'), w = Math.min(1080, im.naturalWidth), h = Math.round(w * im.naturalHeight / im.naturalWidth); c.width = w; c.height = h;
    const x = c.getContext('2d'); if ('filter' in x) x.filter = o.f; x.drawImage(im, 0, 0, w, h); if ('filter' in x) x.filter = 'none';
    if (o.vig) { const g = x.createRadialGradient(w / 2, h / 2, Math.min(w, h) * .32, w / 2, h / 2, Math.max(w, h) * .72); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(30,22,16,${o.vig})`); x.fillStyle = g; x.fillRect(0, 0, w, h); }
    if (o.warm) { x.globalCompositeOperation = 'soft-light'; const g = x.createLinearGradient(0, 0, w, h); g.addColorStop(0, `rgba(255,190,90,${o.warm})`); g.addColorStop(1, 'rgba(90,40,120,.15)'); x.fillStyle = g; x.fillRect(0, 0, w, h); x.globalCompositeOperation = 'source-over'; }
    p.src = c.toDataURL('image/jpeg', .9); } catch (e) {} done(); };
  im.onerror = () => done(); im.src = p.src;
}
function im2Render() {
  const st = $('#studio'); st.classList.remove('tallp');
  const p = cur(); if (!p || !p.s) { TU_GAL = true; renderStudio(); return; }
  if (IM2PID !== p.id) { IM2PID = p.id; IM2SEL = null; }
  const v = p.s.total, t = im2Tier(v), x = galMult(v), opts = im2Opts(p), sel = IM2SEL && opts.find(o => o.k === IM2SEL && !o.max);
  const to = sel ? im2Proj(p, sel) : v, t1 = im2Tier(to), x1 = galMult(to), lk = photoLock(p), inGal = GAL.PATH.includes(p.cat);
  const nb = [70, 80, 90].find(b => v < b), nmx = galNextMult(v);
  const strip = sel ? `<b>${t1 || 'Untiered'} card:</b> ${x1}× · ${GAL.BASE * x1} coins per vote win${x1 > x ? `<small>Up from ${x}×</small>` : ''}` : `<b>${t || 'Untiered'} card:</b> ${x}× · ${GAL.BASE * x} coins per vote win${nmx ? `<small>Reach ${nmx.at} for ${nmx.x}× · tap a touch-up to preview it free</small>` : ''}`;
  const look = im2Look(sel && sel.k);
  const tile = o => `<button class="im2-row${sel && sel.k === o.k ? ' on' : ''}${o.prem ? ' prem' : ''}" data-i2="${o.k}" ${o.max || lk ? 'disabled' : ''}><span>${o.prem ? '✨ ' : ''}${o.t}</span><b>${o.max ? '✓' : sel && sel.k === o.k ? `→ ${im2Proj(p, o)}` : o.prem ? '+' + o.gain : p.s[o.part]}</b></button>`;
  let proj = '';
  if (sel && inGal) { const r = galRoom(p.cat); if (r.full && r.ph.includes(p)) { const mins = r.ph.map(q => q.id === p.id ? to : q.s.total), tr = galTier(Math.min(...mins));
    if (galRank(tr) > galRank(r.tier)) { const i = GAL.PATH.indexOf(p.cat), nx = GAL.PATH[i + 1]; proj = `<b>Completes ${tr} ${esc(galNm(p.cat))}</b> · all three at ${tr === 'Gold' ? 70 : tr === 'Diamond' ? 80 : 90}+${tr === 'Gold' && nx && !galOpen(nx) ? ` · unlocks ${esc(galNm(nx))}` : ''}`; } } }
  if (sel && !proj && t1 !== t && t1) proj = `<b>${esc(alName(p))} becomes ${t1}</b> · ${x1}× coins every time a voter picks it`;
  if (sel && !proj && to >= IM2.PREM_AT && v < IM2.PREM_AT) proj = '<b>Unlocks premium filters</b> · Suncast, Velvet and Nocturne';
  const short = sel && S.gems < sel.price ? sel.price - Math.floor(S.gems) : 0;
  const maxed = opts.every(o => o.max);
  const btn = lk ? `<button class="im2-apply" disabled>In a competition · touch up after it ends</button>`
    : maxed ? `<button class="im2-apply" disabled>${esc(alName(p))} is at its best</button>`
    : !sel ? `<button class="im2-apply" disabled>Choose a touch-up<span>${fixCost(p)} <i class="im2-coin"></i></span></button>`
    : short ? `<button class="im2-apply" id="i2Vote">Need ${short} more coins · Vote to earn</button>`
    : `<button class="im2-apply" id="i2Go">${esc(sel.v)}<span>${sel.price} <i class="im2-coin"></i></span></button>`;
  st.innerHTML = `<div class="gl im2">${galSeg('imp')}
    <h2 class="im2-t">Improve ${esc(alName(p))}</h2>
    <div class="im2-grid"><div class="im2-ph t-${(t || 'plain').toLowerCase()}"><img id="i2Img" src="${p.src}" alt="" style="filter:${look.f}"><i class="im2-vig" style="opacity:${look.vig}"></i><i class="im2-warm" style="opacity:${look.warm}"></i><button class="im2-hold" id="i2Hold">Hold to compare</button></div>
      <div class="im2-side"><small class="im2-lb">Overall score</small><div class="im2-sr"><b id="i2Score">${v}</b>${nb ? `<span class="im2-goal">Goal <b>${nb}</b></span>` : '<span class="im2-goal">Platinum</span>'}</div>
        <div class="im2-rows">${opts.filter(o => !o.prem).map(tile).join('')}${opts.filter(o => o.prem).map(tile).join('')}</div></div></div>
    <p class="im2-strip">${strip}${proj ? `<small>${proj}</small>` : ''}</p>
    ${v < IM2.PREM_AT ? `<p class="im2-lock">🔒 Premium filters (Suncast, Velvet, Nocturne) unlock at ${IM2.PREM_AT}</p>` : ''}${btn}</div>`;
  galWire(st);
  if ($('#i2Back')) $('#i2Back').onclick = () => { if (inGal) S.galCat = p.cat; AL_OPEN = null; TU_GAL = true; save(); renderStudio(); st.scrollTop = 0; };
  st.querySelectorAll('[data-i2]').forEach(b => b.onclick = () => { IM2SEL = IM2SEL === b.dataset.i2 ? null : b.dataset.i2; im2Render(); });
  const h = $('#i2Hold'); if (h && sel) { const img = $('#i2Img'), vg = st.querySelector('.im2-vig'), wm = st.querySelector('.im2-warm');
    const show = raw => { img.style.filter = raw ? 'none' : look.f; vg.style.opacity = raw ? 0 : look.vig; wm.style.opacity = raw ? 0 : look.warm; h.textContent = raw ? 'Before' : 'Hold to compare'; };
    h.addEventListener('pointerdown', e => { e.preventDefault(); show(true); }); ['pointerup', 'pointerleave', 'pointercancel'].forEach(k => h.addEventListener(k, () => show(false))); }
  if ($('#i2Vote')) $('#i2Vote').onclick = () => go('judge');
  if ($('#i2Go')) $('#i2Go').onclick = () => sel.prem ? im2Apply(p, sel) : im2Run(p, sel);
}
function im2Apply(p, o) {
  if (!o || o.max || S.gems < o.price || photoLock(p)) return;
  const v0 = p.s.total, t0 = galTier(v0), x0 = galMult(v0);
  S.gems -= o.price; paintGems(); p.ed = p.ed || {}; p.ed[o.k] = (p.ed[o.k] || 0) + 1;
  p.s = im2Raise(p.s, o.part, o.gain); p.enh = (p.enh || 0) + 1; p.tu1 = 1; p.q = p.s.total >= CFG.QUALIFY; IM2SEL = null; save();
  const btn = $('#i2Go'); if (btn) { btn.disabled = true; btn.firstChild.textContent = 'Touching up…'; }
  im2Bake(p, o, () => { save(); im2Render();
    const sc = $('#i2Score'), card = document.querySelector('.im2-card'); if (card) { card.classList.remove('up'); void card.offsetWidth; card.classList.add('up'); }
    if (sc) { const a = v0, b = p.s.total, t1 = performance.now(); const tick = n => { const k = Math.min(1, (n - t1) / 700); sc.textContent = Math.round(a + (b - a) * k); if (k < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }
    const t1 = galTier(p.s.total), x1 = galMult(p.s.total);
    toast(t1 !== t0 && t1 ? `${alName(p)} is ${t1}! ${p.s.total} · ${x1}× coins per vote` : x1 > x0 ? `${alName(p)} ${v0} → ${p.s.total} · now ${x1}× coins per vote` : `${alName(p)} ${v0} → ${p.s.total}`);
    galCheck(); try { paintEnhBadge(); } catch (e) {} });
}

/* the four touch-ups go through Skill's Before and after screen (pick the new version, see the score jump),
   then come back to Improve; premium filters still apply straight away */
let IM2_RUN = null;
function im2Run(p, o) {
  if (!o || o.max || S.gems < o.price || photoLock(p)) return;
  IM2_RUN = { pid: p.id, k: o.k, v0: p.s.total, t0: galTier(p.s.total), x0: galMult(p.s.total) }; IM2SEL = null;
  startEnhance(p, o.part);
  setTimeout(() => { if (IM2_RUN && !$('#flow').classList.contains('on')) IM2_RUN = null; }, 800);
}
function im2After(p, run, changed) {
  im2Render(); if (!changed) return;
  const sc = $('#i2Score'); if (sc) { const a = run.v0, b = p.s.total, t1 = performance.now(); const tick = n => { const k = Math.min(1, (n - t1) / 700); sc.textContent = Math.round(a + (b - a) * k); if (k < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }
  const t1 = galTier(p.s.total), x1 = galMult(p.s.total);
  toast(t1 !== run.t0 && t1 ? `${alName(p)} is ${t1}! ${p.s.total} · ${x1}× coins per vote` : x1 > run.x0 ? `${alName(p)} ${run.v0} → ${p.s.total} · now ${x1}× coins per vote` : `${alName(p)} ${run.v0} → ${p.s.total}`);
  galCheck(); try { paintEnhBadge(); } catch (e) {}
}
const _showResultI2 = showResult;
showResult = function (p, o = {}) {
  if (IM2_RUN && p && IM2_RUN.pid === p.id) { const run = IM2_RUN; IM2_RUN = null; const changed = o.delta != null;
    if (changed) { p.ed = p.ed || {}; p.ed[run.k] = (p.ed[run.k] || 0) + 1; p.q = p.s.total >= CFG.QUALIFY; save(); }
    try { closeFlow(); } catch (e) {} S.cur = p.id; TU_GAL = false; WALL = false; save(); go('studio'); im2After(p, run, changed); return; }
  return _showResultI2.apply(this, arguments);
};
const _renderStudioI2 = renderStudio;
renderStudio = function () {
  if (!TU_GAL && S.user && S.photos.length) { WALL = false; im2Render(); galCheck(); return; }
  return _renderStudioI2.apply(this, arguments);
};
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]

CSS = r'''
/* Improve, card style */
.im2-back{display:block;border:0;background:none;margin:0 16px 8px;padding:4px 0;font:600 1.05rem Fraunces,serif;color:inherit;cursor:pointer}
.im2-card{margin:0 14px;border-radius:18px;padding:5px;background:linear-gradient(160deg,#EFE6D6,#CDBFA2);box-shadow:0 12px 20px -12px rgba(0,0,0,.6)}
.im2-card.t-gold{background:linear-gradient(135deg,#FFF3B0,#E7B940 22%,#B8862A 42%,#FBE39A 60%,#C99A2E 80%,#FFF1B5)}
.im2-card.t-diamond{background:linear-gradient(120deg,#BFE3FF,#E7C9FF 20%,#FFD6E8 38%,#FFF3C4 55%,#C8FFE6 72%,#BFD9FF 88%,#E7C9FF);background-size:220% 220%;animation:alholo 6s linear infinite}
.im2-card.t-platinum{background:linear-gradient(135deg,#FFFFFF,#D9DEE6 30%,#A7B0BD 50%,#F4F6F9 68%,#C5CCD6 85%,#FFFFFF);background-size:200% 200%;animation:alholo 8s linear infinite}
.im2-card.up{animation:i2up .8s cubic-bezier(.2,1.5,.4,1)}@keyframes i2up{35%{transform:scale(1.03);box-shadow:0 0 0 6px rgba(255,201,60,.5),0 12px 20px -12px rgba(0,0,0,.6)}}
.im2-in{border-radius:14px;overflow:hidden;background:#FBF6EC}
.im2-hd{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 12px}.im2-hd>b{font:900 1.6rem/1 Fraunces,serif;color:#2D2521;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.im2-sc{display:flex;align-items:center;gap:8px}.im2-sc b{font:900 1.9rem/1 Fraunces,serif;color:#2D2521}
.im2-ph{position:relative;height:clamp(180px,32vh,250px)}.im2-ph img{display:block;width:100%;height:100%;object-fit:cover;transition:filter .3s}
.im2-vig,.im2-warm{position:absolute;inset:0;pointer-events:none;transition:opacity .3s}.im2-vig{background:radial-gradient(ellipse at center,rgba(0,0,0,0) 45%,rgba(30,22,16,.85) 100%)}
.im2-warm{background:linear-gradient(160deg,rgba(255,190,90,.45),rgba(255,120,60,.05) 60%,rgba(90,40,120,.2));mix-blend-mode:soft-light}
.im2-hold{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);border:0;border-radius:999px;background:rgba(255,255,255,.92)!important;padding:6px 14px;font:700 .85rem "Nunito Sans",sans-serif;color:#2D2521!important;opacity:1!important;box-shadow:0 3px 8px rgba(0,0,0,.3);user-select:none;-webkit-user-select:none;touch-action:none;cursor:pointer}
.im2-band{padding:7px 10px 8px;background:linear-gradient(180deg,#8E2530,#6E1D22);text-align:center}.im2-band b{display:block;font:800 1rem "Nunito Sans",sans-serif;color:#FFE9A8}.im2-band b s{opacity:.6;text-decoration:none}
.im2-band small{display:block;font-size:.8rem;color:#fff;opacity:.92}
.im2-eds{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 14px 8px}
.im2-ed{border:0;border-radius:13px;padding:9px 11px;text-align:left;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;cursor:pointer;font-family:"Nunito Sans",sans-serif;color:#2D2521}
.im2-ed b{display:flex;justify-content:space-between;gap:6px;font-size:.88rem;white-space:nowrap;font-weight:800;color:#2D2521}.im2-ed b i{font-style:normal;color:#2E6B42;font-weight:900}
.im2-ed small{display:block;margin-top:2px;font-size:.78rem;color:#6F6258}
.im2-ed.on{background:#EEF2FA;box-shadow:inset 0 0 0 2px #2D4E86}.im2-ed[disabled]{opacity:.55;cursor:default}
.im2-prem .im2-ed{background:linear-gradient(180deg,#FFF8E6,#FBEFD2);box-shadow:inset 0 0 0 1.5px #D9B467}.im2-prem .im2-ed.on{box-shadow:inset 0 0 0 2px #2D4E86}
.im2-ph2{margin:6px 16px 0;font:800 .8rem "Nunito Sans",sans-serif;letter-spacing:.08em;text-transform:uppercase;opacity:.75}
.im2-lock{display:flex;align-items:center;gap:8px;margin:0 14px 8px;padding:8px 12px;border-radius:13px;background:#F1E9DA;font-size:.85rem;color:#5F534A}
.im2-proj{margin:0 14px 10px;padding:9px 12px;border-radius:13px;background:#FBEFD2;font-size:.9rem;color:#2D2521}
.im2-apply{display:flex;align-items:center;justify-content:space-between;gap:10px;width:calc(100% - 28px);margin:4px 14px 0;min-height:58px;border:0;border-radius:999px;padding:6px 6px 6px 22px;background:#2D4E86;color:#fff;font:800 1.15rem Fraunces,serif;cursor:pointer;box-shadow:0 6px 16px rgba(45,78,134,.25);text-align:left}
.im2-apply span{flex:none;display:flex;align-items:center;gap:7px;background:rgba(0,0,0,.28);box-shadow:inset 0 2px 4px rgba(0,0,0,.35);border-radius:999px;padding:9px 16px}
.im2-apply[disabled]{opacity:.55;cursor:default}#i2Vote{justify-content:center;padding:6px 18px;font-size:1.02rem}
.im2-coin{display:inline-block;width:18px;height:18px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF3A8,#E0A82E 60%,#A8761A)}
html.yg .im2-proj,html.yg .im2-lock{color:#2D2521}html.yg .im2-ed{background:#FFFDF9!important}html.yg .im2-prem .im2-ed{background:linear-gradient(180deg,#FFF8E6,#FBEFD2)!important}html.yg .im2-ed.on{background:#EEF2FA!important}.im2-ed b,.im2-ed small{opacity:1}html.yg .im2-ed b{color:#2D2521!important}html.yg .im2-ed small{color:#6F6258!important}
/* Improve: photo left, score and touch-ups right */
.im2-t{text-align:center;margin:0 16px 12px;font:900 clamp(1.8rem,8.4vw,2.3rem)/1.05 Fraunces,serif}
.im2-grid{display:grid;grid-template-columns:47% 1fr;gap:12px;align-items:start;margin:0 14px}
.im2 .im2-ph{position:relative;height:auto;aspect-ratio:3/4.2;border-radius:20px;overflow:hidden;box-shadow:0 10px 20px -12px rgba(0,0,0,.6)}
.im2 .im2-ph.t-gold{box-shadow:0 0 0 3px #E0A82E,0 10px 20px -12px rgba(0,0,0,.6)}.im2 .im2-ph.t-diamond{box-shadow:0 0 0 3px #8FB6EE,0 0 14px rgba(160,200,255,.7)}.im2 .im2-ph.t-platinum{box-shadow:0 0 0 3px #B9C1CC,0 10px 20px -12px rgba(0,0,0,.6)}
.im2-lb{display:block;font:800 .74rem "Nunito Sans",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#4E433C}
.im2-sr{display:flex;align-items:center;gap:10px;margin:2px 0 8px}.im2-sr>b{font:900 3.2rem/1 Fraunces,serif;color:#2E6B42}
.im2-goal{padding:5px 12px;border-radius:999px;background:#FBEFD2;box-shadow:inset 0 0 0 1.5px #E0B860;font:800 .78rem "Nunito Sans",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#8A5A0A;white-space:nowrap}.im2-goal b{font:900 1.3rem Fraunces,serif;letter-spacing:0;color:#8A5A0A}
.im2-rows{display:flex;flex-direction:column;gap:7px}
.im2-row{display:flex;align-items:center;justify-content:space-between;gap:6px;border:0;border-radius:12px;padding:8px 10px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;font:700 .86rem "Nunito Sans",sans-serif;color:#2D2521!important;cursor:pointer;text-align:left}
.im2-row span{min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.im2-row b{flex:none;font:900 1rem Fraunces,serif;color:#2D2521}
.im2-row.on{background:#EEF2FA!important;box-shadow:inset 0 0 0 2px #2D4E86;color:#24406F!important}.im2-row.on b{color:#2E6B42}
.im2-row.prem{background:linear-gradient(180deg,#FFF8E6,#FBEFD2)!important;box-shadow:inset 0 0 0 1.5px #D9B467}.im2-row.prem.on{box-shadow:inset 0 0 0 2px #2D4E86}
.im2-row[disabled]{opacity:.55;cursor:default}
.im2-strip{margin:14px 14px 8px;padding:10px 14px;border-radius:14px;background:#FBEFD2;text-align:center;font-size:1rem;color:#2D2521}.im2-strip b{color:#6A3500}.im2-strip s{opacity:.55}
.im2-strip small{display:block;margin-top:3px;font-size:.82rem;color:#4E433C}.im2-strip small b{color:#2D2521}
.im2 .im2-lock{margin:0 14px 8px;font-size:.8rem;justify-content:center;background:none;padding:0}
html.yg .im2-strip{color:#2D2521}html.yg .im2-row{background:#FFFDF9!important}html.yg .im2-lb{color:#D8CCF0}
.im2-t{display:block;position:static;margin:4px 16px 14px!important;padding:0}
.im2-side{min-width:0}.im2 .im2-row{font-size:.8rem;padding:8px 8px;gap:4px}.im2 .im2-row b{font-size:.95rem}.im2-rows .im2-row{width:100%;box-sizing:border-box}
.im2 .im2-hold{white-space:nowrap;font-size:.78rem!important;padding:5px 11px!important}
.im2 .im2-apply{background:#2D4E86!important;color:#fff!important;opacity:1}.im2 .im2-apply[disabled]{opacity:.55}
html.yg .im2 .im2-lock{color:#D8CCF0}
/* tidy layout: no back link, tighter spacing so Apply sits on screen */
.im2 .gl-seg{margin-bottom:10px}
.im2-t{margin:2px 16px 10px!important;font-size:clamp(1.7rem,7.8vw,2.1rem)!important}
.im2-grid{gap:12px;align-items:stretch}
.im2 .im2-ph{aspect-ratio:auto!important;height:100%;min-height:220px}
.im2-side{display:flex;flex-direction:column}.im2-sr{margin:0 0 6px}.im2-sr>b{font-size:2.8rem}
.im2-rows{flex:1;justify-content:space-between;gap:6px}
.im2-strip{margin:12px 14px 6px;padding:9px 12px}
.im2 .im2-lock{margin:0 14px 10px;text-align:center;justify-content:center}
.im2-apply{margin-top:2px}
/* Before and after: score sits in a panel, not floating */
#flowBody .ba-sc{display:block!important;margin:2px 0 12px!important;padding:0!important;width:100%!important;max-width:none!important}
#flowBody .ba-sc .en-sc{display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:10px!important;width:100%!important;box-sizing:border-box;margin:0!important;padding:10px 14px!important;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(60,40,20,.45);flex-direction:row!important;position:relative}
#flowBody .ba-sc .en-sc::before{content:"Score now";font:800 .74rem "Nunito Sans",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#4E433C;margin-right:2px}
#flowBody .ba-sc .en-sc b{font:900 2.4rem/1 Fraunces,serif!important;color:#2E6B42!important;margin:0!important}
#flowBody .ba-sc .en-sc .medal{font-size:1.5rem!important;margin:0!important;position:static!important}
#flowBody .ba-sc .en-sc .goal70{margin:0 0 0 auto!important;position:static!important}
html.yg #flowBody .ba-sc .en-sc::before{color:#4E433C}
@media (prefers-reduced-motion:reduce){.im2-card{animation:none!important}.im2-ph img,.im2-vig,.im2-warm{transition:none}}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('improve2 ok')
