# Vote goal bar (Skill preview). Runs after galleries.py and album.py.
# One line at the top of Vote, in place of the "Coming up" chip, ties voting to your gallery:
#   "20 more coins to improve Milo" (progress bar) -> "Milo's upgrade is ready · View upgrade", or
#   "Get Pip to 80 to complete Diamond Pets", "Get Milo to 85 to earn 5×", "Add 1 more Pets photo".
# Tapping it opens that photo's big card in the Gallery (or the add-photo flow). The "Coming up" chip
# comes back only when there is no goal (every open collection at Platinum).
# Usage: python3 build-skill/votegoal.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function alCard(' not in s: sys.exit('run galleries.py and album.py first')
if 'function vgGoal(' in s: sys.exit('vote goal already applied')

JS = r'''
/* ---------- vote goal bar ---------- */
const vgToGallery = c => { if (!S.user) { galAdd(c); return; } S.galCat = c; AL_OPEN = null; TU_GAL = true; save(); go('studio'); };
function vgGoal() {
  if (!S.user || !S.photos.length) return { t: 'Add your first photo', s: 'Your photos earn coins every time a voter picks them', act: () => vgToGallery('pets') };
  const open = GAL.PATH.filter(galOpen);
  const c = S.galCat && galOpen(S.galCat) && galRoom(S.galCat).tier !== 'Platinum' ? S.galCat : (open.find(x => galRoom(x).tier !== 'Platinum') || null);
  if (!c) return null;
  const r = galRoom(c), nm = galNm(c);
  if (!r.ph.length) return { t: `Add your first ${nm.toLowerCase()} photo`, s: `Start your ${nm} collection: 3 photos, earning on every vote`, act: () => vgToGallery(c) };
  if (!r.full) { const n = 3 - r.ph.length; return { p: r.ph[0], t: `Add ${n} more ${nm} photo${n === 1 ? '' : 's'}`, s: `${r.ph.length} of 3 · complete the collection to earn more`, act: () => vgToGallery(c) }; }
  const cand = r.ph.filter(x => x.s.total < r.next && lowestOpen(x) && !photoLock(x)).sort((a, b) => b.s.total - a.s.total);
  const p = cand[0]; if (!p) return null;
  const name = alName(p), cost = fixCost(p), have = Math.floor(S.gems), card = () => { AL_OPEN = p.id; TU_GAL = true; save(); go('studio'); };
  if (have >= cost) return { p, ready: 1, t: `${name}’s upgrade is ready`, s: `${p.s.total} → ${r.next} · ${cost} coins`, act: card };
  const nx = galNextMult(p.s.total), base = { p, bar: have / cost, n: `${have}/${cost}`, act: card };
  if (r.ph.filter(x => x.s.total < r.next).length === 1) return { ...base, t: `Get ${name} to ${r.next} to complete ${galBand(r.next)} ${nm}`, s: `${cost - have} more coins for the next touch-up` };
  if (nx && nx.at - p.s.total <= 4) return { ...base, t: `Get ${name} to ${nx.at} to earn ${nx.x}× per vote`, s: `Earning ${galMult(p.s.total)}× now · ${cost - have} more coins to improve` };
  return { ...base, t: `${cost - have} more coins to improve ${name}`, s: `${r.at} of 3 ${nm} photos at ${galBand(r.next)}` };
}
function vgPaint() {
  const j = $('#judge'); if (!j) return; let el = $('#vgGoal'); const g = vgGoal();
  j.classList.toggle('has-goal', !!g);
  if (!g) { if (el) el.remove(); return; }
  if (!el) { el = document.createElement('button'); el.id = 'vgGoal'; el.className = 'vg'; const anchor = j.querySelector('#qsChip') || j.querySelector('.tot-h'); if (anchor) anchor.insertAdjacentElement('beforebegin', el); else j.prepend(el); }
  const was = el.classList.contains('ready');
  el.classList.toggle('ready', !!g.ready);
  el.innerHTML = `${g.p ? `<img src="${g.p.src}" alt="">` : '<span class="vg-ic" aria-hidden="true">📷</span>'}<span class="vg-tx"><b>${g.bar != null ? gemIcon('vg-ci') : ''}${esc(g.t)}</b>${g.bar != null ? `<span class="vg-row"><span class="vg-bar"><i style="width:${Math.min(100, Math.round(g.bar * 100))}%"></i></span><em>${g.n}</em></span>` : `<small>${esc(g.s)}</small>`}</span>${g.ready ? '<span class="vg-cta">View upgrade</span>' : g.p ? '' : '<span class="vg-cta">Add</span>'}`;
  el.setAttribute('aria-label', g.t + (g.s ? '. ' + g.s : ''));
  el.onclick = () => g.act && g.act();
  if (g.ready && !was) { el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
}
const _renderJudgeV = renderJudge;
renderJudge = function () { const r = _renderJudgeV.apply(this, arguments); try { vgPaint(); } catch (e) {} return r; };
const _voteV = vote;
vote = async function () { const r = await _voteV.apply(this, arguments); try { vgPaint(); setTimeout(vgPaint, 1600); } catch (e) {} return r; };
setInterval(() => { try { if ($('#panes') && $('#panes').dataset.at === 'judge') vgPaint(); } catch (e) {} }, 2500);
/* the top bar rotates through 3 notifications, one per vote: earnings (ticks up live), add photos, improve */
const vgImprove = vgGoal;
const vgDayTotal = () => S.photos.reduce((a, x) => a + galToday(x), 0);
function vgEarn() {
  const hung = GAL.PATH.filter(galOpen).flatMap(c => galRoom(c).ph); if (!hung.length) return null;
  const tot = vgDayTotal(), top = hung.slice().sort((a, b) => galToday(b) - galToday(a) || b.s.total - a.s.total)[0];
  return { p: top, earn: tot, t: `Your photos earned <span class="vg-n">+${tot}</span> coins today`,
    s: galToday(top) ? `Top earner: ${alName(top)} · +${galToday(top)} at ${galMult(top.s.total)}× per vote` : `${hung.length} photo${hung.length === 1 ? '' : 's'} earning every time a voter picks them`,
    act: () => vgToGallery(top.cat) };
}
function vgAdd() {
  if (!S.user || !S.photos.length) return vgImprove();
  const open = GAL.PATH.filter(galOpen);
  const c = open.find(x => !galRoom(x).full); if (!c) return null;
  const r = galRoom(c), nm = galNm(c), n = 3 - r.ph.length;
  return r.ph.length ? { p: r.ph[0], t: `Add ${n} more ${nm} photo${n === 1 ? '' : 's'} to earn more`, s: `Every photo in your ${nm} collection earns on votes`, act: () => vgToGallery(c) }
    : { t: `Start your ${nm} collection`, s: `Add ${nm.toLowerCase()} photos · each one earns on every vote`, act: () => vgToGallery(c) };
}
function vgImp() {
  const g = vgImprove(); if (g && (g.bar != null || g.ready)) return g;
  const hung = GAL.PATH.filter(galOpen).flatMap(c => galRoom(c).ph).filter(x => lowestOpen(x) && !photoLock(x) && x.s.total < 99);
  const p = hung.sort((a, b) => a.s.total - b.s.total)[0]; if (!p) return null;
  const name = alName(p), cost = fixCost(p), have = Math.floor(S.gems), nb = [70, 80, 90].find(b => p.s.total < b), nx = galNextMult(p.s.total), card = () => { AL_OPEN = p.id; TU_GAL = true; save(); go('studio'); };
  if (have >= cost) return { p, ready: 1, t: `${name}’s upgrade is ready`, s: `${p.s.total}${nb ? ` → ${nb} for ${galBand(nb)}` : ''} · ${cost} coins`, act: card };
  return { p, bar: have / cost, n: `${have}/${cost}`, act: card, t: nx ? `Improve ${name} to ${nx.at} to earn ${nx.x}× per vote` : `${cost - have} more coins to improve ${name}`, s: '' };
}
vgGoal = function () {
  if (!S.user || !S.photos.length) return vgImprove();
  const L = [vgEarn, vgAdd, vgImp], k = (S.vgTurn || 0) % 3;
  for (let i = 0; i < 3; i++) { const g = L[(k + i) % 3](); if (g) return g; }
  return vgImprove();
};
const vgEsc = esc; let VG_TICK = null;
const _vgPaintR = vgPaint;
vgPaint = function () {
  _vgPaintR();
  const el = $('#vgGoal'), g = vgGoal(); if (!el || !g) return;
  if (g.earn != null) { const b = el.querySelector('.vg-tx b'); if (b) b.innerHTML = gemIcon('vg-ci') + g.t; el.classList.add('earn');
    if (VG_TICK) { const n = el.querySelector('.vg-n'), { from, to } = VG_TICK, t0 = performance.now(); VG_TICK = null;
      el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
      const tick = t => { if (!n.isConnected) return; const k = Math.min(1, (t - t0) / 900); n.textContent = '+' + Math.round(from + (to - from) * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); };
      n.textContent = '+' + from; requestAnimationFrame(tick); } }
  else el.classList.remove('earn');
};
const _voteR = vote;
vote = async function () { const n0 = S.votes; if (!V_BUSY_R) { V_BUSY_R = 1; } const r = await _voteR.apply(this, arguments); V_BUSY_R = 0; if (S.votes > n0) { S.vgTurn = ((S.vgTurn || 0) + 1) % 3; save(); try { vgPaint(); } catch (e) {} } return r; };
let V_BUSY_R = 0;
// a photo of yours gets picked: switch the bar to earnings and tick the total up
const _galPickR = galPick;
galPick = function () { const t0 = vgDayTotal(); _galPickR.apply(this, arguments); const t1 = vgDayTotal();
  if (t1 > t0) { S.vgTurn = 0; save(); VG_TICK = { from: t0, to: t1 }; try { vgPaint(); } catch (e) {} } };
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]

CSS = r'''
/* vote goal bar */
#judge.has-goal #qsChip{display:none!important}
.vg{display:flex;align-items:center;gap:12px;width:calc(100% - 28px);margin:6px 14px 4px;padding:8px 12px 8px 8px;border:0;border-radius:18px;text-align:left;cursor:pointer;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(60,40,20,.5);font-family:"Nunito Sans",sans-serif;color:#2D2521!important}
.vg img{flex:none;width:50px;height:50px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #fff,0 0 0 3.5px #D8C49E}
.vg-ic{flex:none;display:grid;place-items:center;width:50px;height:50px;border-radius:50%;background:#EFE6D6;font-size:1.5rem}
.vg-tx{flex:1;min-width:0}.vg-tx b{display:flex;align-items:center;gap:6px;font:800 .98rem/1.2 "Nunito Sans",sans-serif;color:#2D2521}
.vg-ci{flex:none;width:18px;height:18px}
.vg-tx small{display:block;margin-top:2px;font-size:.82rem;color:#6F6258}
.vg-row{display:flex;align-items:center;gap:8px;margin-top:6px}.vg-bar{flex:1;height:9px;border-radius:5px;background:#E9DFCC;overflow:hidden}.vg-bar i{display:block;height:100%;border-radius:5px;background:linear-gradient(90deg,#2D4E86,#3F68AE);transition:width .5s}
.vg-row em{flex:none;font-style:normal;font-size:.8rem;font-weight:700;color:#6F6258}
.vg-cta{flex:none;padding:8px 12px;border-radius:999px;background:#2D4E86;color:#fff;font:800 .85rem "Nunito Sans",sans-serif;white-space:nowrap}
.vg.ready{background:linear-gradient(180deg,#FFF6DA,#FBEBC0);box-shadow:inset 0 0 0 2px #E0A82E,0 0 0 3px rgba(255,201,60,.25),0 8px 18px -10px rgba(160,110,10,.6)}
.vg.pop{animation:vgpop .7s cubic-bezier(.2,1.5,.4,1)}@keyframes vgpop{40%{transform:scale(1.04)}}
html.yg .vg{background:#FBF6EC!important}html.yg .vg.ready{background:linear-gradient(180deg,#FFF6DA,#FBEBC0)!important}.vg .vg-tx b{color:#2D2521!important}.vg .vg-tx small,.vg .vg-row em{color:#6F6258!important}.vg .vg-cta{color:#fff!important}
.vg.earn{background:linear-gradient(180deg,#F3FAF2,#E3F1E7)!important;box-shadow:inset 0 0 0 1.5px #A9D3B4,0 6px 14px -10px rgba(46,107,66,.5)}.vg.earn .vg-n{color:#2E6B42;font-weight:900}.vg.earn img{box-shadow:0 0 0 2px #fff,0 0 0 3.5px #7FB98E}
@media (prefers-reduced-motion:reduce){.vg.pop{animation:none}.vg-bar i{transition:none}}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('vote goal ok')
