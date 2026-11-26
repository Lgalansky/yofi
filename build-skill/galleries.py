# Galleries (Skill, ported from Skill 2). The Touch-ups tab gets two tabs: Gallery and Improve.
# - Gallery: a room per category with 3 frames. Rooms open in order (Pets -> Travel -> Nature -> Family -> Garden
#   -> Baking -> Home); the next room opens when all three photos in the room before it reach Gold.
# - A room's tier is set by its lowest photo: Gold 70-79, Diamond 80-89, Platinum 90+. The room is redecorated to match
#   (gilded walls and lights for Gold, ice for Diamond, pearl for Platinum) and a celebration pop plays when it goes up.
# - Every photo hanging in an open room earns coins when voters pick it: 2 coins x its rate
#   (under 70 x1, 70-74 x2, 75-79 x3, 80-84 x4, 85-89 x5, 90+ x6). A small "Your photo was picked" chip shows the coins fly in.
# - The photo levels are renamed to match: Gold 70, Diamond 80, Platinum 90, Masterpiece 95 (were Bronze/Silver/Gold/Diamond).
# - Improve is the existing touch-up screen, with a line saying what the photo means for its gallery.
# Usage: python3 build-skill/galleries.py [in.html] [out.html]  (defaults to index.html in place)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function galRoom(' in s: sys.exit('galleries already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)

# score count-up: remember the real target so a second render can't freeze it on a half-way number
rep("if (big) { const to2 = +big.textContent, f2 = from == null ? 0 : from,",
    "if (big) { const to2 = +(big.dataset.to || (big.dataset.to = big.textContent)), f2 = from == null ? 0 : from,")
# one set of tier names everywhere
rep("SCORE_LEVELS = [{ at: 70, k: 'bronze', n: 'Bronze', ic: '🥉', fee: 1 }, { at: 80, k: 'silver', n: 'Silver', ic: '🥈', fee: 5 }, { at: 90, k: 'gold', n: 'Gold', ic: '🥇', fee: 10 }, { at: 95, k: 'diamond', n: 'Diamond', ic: '🟡', fee: 20 }]",
    "SCORE_LEVELS = [{ at: 70, k: 'gold', n: 'Gold', ic: '🥇', fee: 1 }, { at: 80, k: 'diamond', n: 'Diamond', ic: '💎', fee: 5 }, { at: 90, k: 'silver', n: 'Platinum', ic: '🏆', fee: 10 }, { at: 95, k: 'gold', n: 'Masterpiece', ic: '🌟', fee: 20 }]")

JS = r'''
/* ---------- galleries ---------- */
const GAL = { PATH: ['pets', 'travel', 'night', 'selfie', 'fitness', 'food', 'style'], BASE: 2, PICK: .45,
  MULT: [[90, 6], [85, 5], [80, 4], [75, 3], [70, 2], [0, 1]],
  NAME: { pets: 'Pets', travel: 'Travel', night: 'Nature', selfie: 'Family', fitness: 'Garden', food: 'Baking', style: 'Home' } };
const galMult = v => GAL.MULT.find(m => v >= m[0])[1];
const galNextMult = v => { const up = GAL.MULT.filter(m => m[0] > v && m[1] > galMult(v)); return up.length ? { at: up[up.length - 1][0], x: up[up.length - 1][1] } : null; };
const galTier = v => v >= 90 ? 'Platinum' : v >= 80 ? 'Diamond' : v >= 70 ? 'Gold' : '';
const galRank = t => ['', 'Gold', 'Diamond', 'Platinum'].indexOf(t || '');
const galBand = b => b === 70 ? 'Gold' : b === 80 ? 'Diamond' : 'Platinum';
const galNm = c => GAL.NAME[c] || pcatName(c);
const galToday = p => p.gd === todayKey() ? (p.gt || 0) : 0;
function galRoom(c) {
  const ph = S.photos.filter(p => p.cat === c && p.s).sort((a, b) => b.s.total - a.s.total).slice(0, 3), full = ph.length === 3;
  const min = full ? Math.min(...ph.map(p => p.s.total)) : 0, tier = full ? galTier(min) : '', next = full ? ([70, 80, 90].find(b => min < b) || null) : 70;
  return { c, ph, full, min, tier, next, at: next ? ph.filter(p => p.s.total >= next).length : 3 };
}
const galOpen = c => { const i = GAL.PATH.indexOf(c); return i <= 0 || galRank((S.galBest || {})[GAL.PATH[i - 1]]) >= 1; };
const galLoose = () => S.photos.filter(p => p.s && !GAL.PATH.includes(p.cat));
let TU_GAL = false;
// a room going up a tier (or the first room reaching Gold, which opens the next) gets one celebration
function galCheck() {
  if (!S.user) return; S.galBest = S.galBest || {};
  const init = !S.galInit; let ev = null;
  GAL.PATH.forEach(c => { if (!galOpen(c) || ev) return; const r = galRoom(c); if (galRank(r.tier) > galRank(S.galBest[c])) { const wasOpen = GAL.PATH.filter(galOpen); S.galBest[c] = r.tier; const opened = GAL.PATH.find(x => galOpen(x) && !wasOpen.includes(x)); if (!init) ev = { c, tier: r.tier, opened }; } });
  if (init) { S.galInit = 1; save(); return; }
  if (!ev) return; save();
  const show = (n = 0) => { const co = $('#coach'); if ((co && co.classList.contains('on')) || $('#flow').classList.contains('on')) { if (n < 40) setTimeout(() => show(n + 1), 800); return; } galCele(ev); };
  setTimeout(show, SCORE_ANIM_MS + 200);
}
function galCele({ c, tier, opened }) {
  const co = $('#coach'), r = galRoom(c), band = tier === 'Gold' ? 70 : tier === 'Diamond' ? 80 : 90;
  co.innerHTML = `<div class="crbox wpbox gl-pop" role="dialog" aria-modal="true" aria-labelledby="glpT"><div class="cr-rays wp-rays" aria-hidden="true"></div>
    ${[...Array(24)].map((_, i) => `<i class="wp-cf" style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A', '#F59E0B'][i % 5]};animation-delay:${(i * .09).toFixed(2)}s"></i>`).join('')}
    <div class="gl-trio t-${tier.toLowerCase()}">${r.ph.map(p => `<span class="gl-fr"><img src="${p.src}" alt=""></span>`).join('')}</div>
    <h2 id="glpT">${tier} ${esc(galNm(c))} Collection!</h2>
    <p>All three photos reached <b>${band}</b>. They now earn at least <b>${galMult(band)}× coins</b> every time a voter picks them.${opened ? ` <b>${esc(galNm(opened))} is unlocked.</b>` : ''}</p>
    <button class="bt-cta" id="glpGo">${opened ? `Open ${esc(galNm(opened))}` : 'See the collection'}</button><button class="bt-no" id="glpNo">Back to voting</button></div>`;
  co.classList.add('on', 'cr');
  const close = () => { co.classList.remove('on', 'cr'); co.innerHTML = ''; };
  $('#glpGo').onclick = () => { close(); S.galCat = opened || c; TU_GAL = true; save(); go('studio'); setTimeout(() => { const w = $('.gl-room'); if (w) w.classList.add('cele'); }, 60); };
  $('#glpNo').onclick = () => { close(); go('judge'); try { renderJudge(); } catch (e) {} };
}
// a voter somewhere picks one of your hanging photos: 2 coins x its rate
function galPick() {
  const pool = GAL.PATH.filter(galOpen).flatMap(c => galRoom(c).ph); if (!pool.length || Math.random() > GAL.PICK) return;
  const p = pool[Math.floor(Math.random() * pool.length)], x = galMult(p.s.total), m = GAL.BASE * x, d = todayKey();
  if (p.gd !== d) { p.gd = d; p.gt = 0; } p.gt += m; p.gl = (p.gl || 0) + m; p.gv = (p.gv || 0) + 1; S.gems += m; save();
  const el = document.createElement('div'); el.className = 'gl-pick'; el.setAttribute('role', 'status');
  el.innerHTML = `<img src="${p.src}" alt=""><span><b>Your ${esc(galNm(p.cat))} photo was picked</b><small>${p.s.total} · ${x}× · +${m} coins</small></span>`;
  const bar = document.querySelector('#vgGoal'), onVote = bar && bar.getClientRects().length && $('#panes').dataset.at === 'judge';
  if (onVote) { setTimeout(() => { try { gemExplosion(m, { mid: 1, from: document.querySelector('#vgGoal .vg-n') || bar }); } catch (e) { paintGems(); } }, 120); return; }
  setTimeout(() => { try { gemExplosion(m, { mid: 1 }); } catch (e) { paintGems(); } }, 120);
  setTimeout(() => { el.classList.remove('on'); setTimeout(() => el.remove(), 400); }, 2600);
}
const _voteG = vote;
vote = async function () { const n0 = S.votes; const r = await _voteG.apply(this, arguments); if (S.votes > n0) setTimeout(galPick, 700); return r; };
const galSeg = v => `<div class="gl-seg" role="tablist" aria-label="Touch-ups"><button role="tab" data-gv="gal" aria-selected="${v === 'gal'}">🖼️ Gallery</button><button role="tab" data-gv="imp" aria-selected="${v === 'imp'}">✨ Improve</button></div>`;
function galWire(st) { st.querySelectorAll('[data-gv]').forEach(b => b.onclick = () => { TU_GAL = b.dataset.gv === 'gal'; if (!TU_GAL && S.user) sdSmart(); renderStudio(); st.scrollTop = 0; }); }
function galImprove(id) { const p = S.photos.find(x => x.id === id); if (!p) return; const r = galRoom(p.cat), nx = r.next && p.s.total < r.next ? r.next : nextLvl(p.s.total) && nextLvl(p.s.total).at;
  S.cur = id; TU_GAL = false; WALL = false; window.__sdWhy = nx ? `${esc(galNm(p.cat))} gallery · <b>${nx - p.s.total} point${nx - p.s.total === 1 ? '' : 's'} to ${galBand(nx)}</b>` : ''; save(); renderStudio(); $('#studio').scrollTop = 0; }
function galAdd(c) {
  const loose = galLoose();
  if (!loose.length) { window.__preCat = c; pickPhoto(true); return; }
  openSheet(`<div class="gl-hang"><h2>Hang a ${esc(galNm(c).toLowerCase())} photo</h2><p>Pick one of your photos that isn’t in a gallery yet, or upload a new one.</p>
    <div class="gl-hg">${loose.map(x => `<button data-ghp="${x.id}"><img src="${x.src}" alt=""><b>${x.s.total}</b></button>`).join('')}</div>
    <button class="btn block" id="glUp">Upload a new ${esc(galNm(c).toLowerCase())} photo</button></div>`);
  document.querySelectorAll('#sheetBody [data-ghp]').forEach(b => b.onclick = () => { const x = S.photos.find(y => y.id === b.dataset.ghp); if (x) x.cat = c; save(); closeSheet(); renderStudio(); galCheck(); });
  $('#glUp').onclick = () => { closeSheet(); window.__preCat = c; pickPhoto(true); };
}
function renderGalleries() {
  const st = $('#studio'); st.classList.remove('tallp');
  let c = S.galCat && galOpen(S.galCat) ? S.galCat : (GAL.PATH.filter(galOpen).find(x => galRoom(x).tier !== 'Platinum') || 'pets');
  const r = galRoom(c), tl = r.tier.toLowerCase();
  const path = GAL.PATH.map((x, i) => { const o = galOpen(x), done = galRank((S.galBest || {})[x]) >= 1;
    return `${i ? '<i class="gl-ln"></i>' : ''}<button data-gc="${x}" class="${x === c ? 'on' : done ? 'done' : o ? 'open' : 'lock'}" aria-label="${esc(galNm(x))}${o ? '' : ', locked'}">${x === c ? `<span class="gl-pn">${esc(galNm(x))}</span>` : `<span class="gl-dot">${done ? '✓' : o ? '' : '🔒'}</span><span>${esc(galNm(x))}</span>`}</button>`; }).join('');
  const frames = [0, 1, 2].map(i => { const p = r.ph[i];
    if (!p) return `<button class="gl-f empty" data-gadd="${c}" aria-label="Add a ${esc(galNm(c).toLowerCase())} photo"><span class="gl-fr"><b>+</b></span><span class="gl-pl">Add</span><small>Empty frame</small></button>`;
    const t = galTier(p.s.total); return `<button class="gl-f" data-gimp="${p.id}" aria-label="Improve photo scoring ${p.s.total}"><span class="gl-fr${t ? ' t-' + t.toLowerCase() : ''}"><img src="${p.src}" alt=""></span><span class="gl-pl">${p.s.total}${t ? ` <em>${t}</em>` : ''}</span><small>${galMult(p.s.total)}× · +${galToday(p)} today</small></button>`; }).join('');
  let sub, act = null;
  if (!r.ph.length) { sub = `Hang 3 ${esc(galNm(c).toLowerCase())} photos here`; act = `<button class="btn block gl-go" data-gadd="${c}">Add your first ${esc(galNm(c).toLowerCase())} photo</button>`; }
  else if (!r.full) { sub = `${r.ph.length} of 3 photos · add ${3 - r.ph.length} more`; act = `<button class="btn block gl-go" data-gadd="${c}">Add a photo</button>`; }
  else if (r.next) { sub = `${r.at} of 3 at ${galBand(r.next)}`; const b = r.ph.filter(p => p.s.total < r.next).sort((a, b) => b.s.total - a.s.total)[0];
    act = `<button class="btn block gl-go" data-gimp="${b.id}"><img src="${b.src}" alt="">Improve this photo · ${b.s.total} → ${r.next}</button>`; }
  else sub = 'All three at Platinum · the top of this gallery';
  const nx = GAL.PATH.find(x => !galOpen(x)), opened = GAL.PATH.filter(galOpen).find(x => x !== c && !galRoom(x).ph.length);
  if (r.tier && opened) act = `<button class="btn block gl-go" data-gc="${opened}">Open ${esc(galNm(opened))}</button>`;
  const waiting = nx ? S.photos.filter(x => x.cat === nx).length : 0, prev = nx && GAL.PATH[GAL.PATH.indexOf(nx) - 1];
  const day = S.photos.reduce((a, x) => a + galToday(x), 0);
  st.innerHTML = `<div class="gl">${galSeg('gal')}
    <nav class="gl-path" aria-label="Galleries">${path}</nav>
    <h2 class="gl-t">${r.tier ? `${r.tier} ${esc(galNm(c))} Collection` : esc(galNm(c))}</h2>
    <div class="gl-room r-${c}${tl ? ' t-' + tl : ''}"><div class="gl-wall">${frames}</div>${r.tier ? `<div class="gl-ban"><span>${r.tier.toUpperCase()} ${esc(galNm(c).toUpperCase())}</span><small>COLLECTION</small></div>` : ''}</div>
    <p class="gl-sub">${sub}</p>${act || ''}
    <p class="gl-earn">${day ? `Your photos earned <b>+${day} coins</b> from votes today` : 'Hanging photos earn coins every time a voter picks them'} · Gold ×2–3 · Diamond ×4–5 · Platinum ×6</p>
    ${nx ? `<button class="gl-next r-${nx}" data-gc="${nx}"><span class="gl-nl">🔒 Next: ${esc(galNm(nx))}</span><small>Opens when all 3 ${esc(galNm(prev))} photos reach Gold (70)${waiting ? ` · ${waiting} photo${waiting === 1 ? '' : 's'} waiting` : ''}</small></button>` : ''}</div>`;
  galWire(st);
  st.querySelectorAll('[data-gc]').forEach(b => b.onclick = () => { const x = b.dataset.gc; if (!galOpen(x)) { const pv = GAL.PATH[GAL.PATH.indexOf(x) - 1]; toast(`${galNm(x)} opens when all 3 ${galNm(pv)} photos reach Gold`); return; } S.galCat = x; save(); renderStudio(); st.scrollTop = 0; });
  st.querySelectorAll('[data-gadd]').forEach(b => b.onclick = () => galAdd(b.dataset.gadd));
  st.querySelectorAll('[data-gimp]').forEach(b => b.onclick = () => galImprove(b.dataset.gimp));
}
const _renderStudioG = renderStudio;
renderStudio = function () {
  if (TU_GAL && S.user) { WALL = false; renderGalleries(); galCheck(); return; }
  const r = _renderStudioG.apply(this, arguments);
  try {
    const st = $('#studio'); if (!S.user || !st) return r;
    st.querySelectorAll('.gl-seg').forEach(e => e.remove()); const h0 = st.querySelector('.tot-h'); if (h0) h0.insertAdjacentHTML('afterbegin', galSeg('imp')); else st.insertAdjacentHTML('afterbegin', galSeg('imp')); galWire(st);
    const p = cur(), h = st.querySelector('.tot-h'); st.querySelectorAll('.gl-tie').forEach(e => e.remove());
    if (p && p.s && h && GAL.PATH.includes(p.cat)) { const rm = galRoom(p.cat), x = galMult(p.s.total), nm = galNextMult(p.s.total), hung = rm.ph.includes(p);
      h.insertAdjacentHTML('beforeend', `<p class="gl-tie">🖼 ${hung ? `In your ${esc(galNm(p.cat))} gallery · earns <b>${x}×</b> per vote${nm ? ` · <b>${nm.at}</b> pays ${nm.x}×` : ''}` : galOpen(p.cat) ? `Not hanging yet: your top 3 ${esc(galNm(p.cat))} photos hang in the gallery` : `${esc(galNm(p.cat))} gallery is still locked`}</p>`); }
    galCheck();
  } catch (e) {}
  return r;
};
$('#segStudio').onclick = () => { TU_GAL = true; go('studio'); };
setInterval(() => { try { galCheck(); } catch (e) {} }, 2000);
'''
rep("  shownGems = S.gems;\n})();\n})();", JS + "  shownGems = S.gems;\n})();\n})();")

CSS = r'''
/* galleries */
.gl{padding:6px 0 28px}
.gl-seg{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:4px 16px 12px;padding:4px;border-radius:16px;background:#EFE6D6;box-shadow:inset 0 0 0 1.5px #E2D5BE}
.gl-seg button{border:0;background:none;border-radius:12px;padding:9px 6px;font:800 1rem "Nunito Sans",sans-serif;color:#5F534A;cursor:pointer}
.gl-seg button[aria-selected="true"]{background:#2D4E86;color:#fff;box-shadow:0 4px 10px -4px rgba(45,78,134,.6)}
.tot-h .gl-seg{margin:0 0 12px;width:100%;align-self:stretch;box-sizing:border-box}
html.yg .gl-seg{background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.14)}html.yg .gl-seg button{color:#D8CCF0}
.gl-path{display:flex;align-items:center;gap:0;overflow-x:auto;padding:2px 16px 8px;scrollbar-width:none}.gl-path::-webkit-scrollbar{display:none}
.gl-path button{flex:none;border:0;background:none;display:flex;flex-direction:column;align-items:center;gap:2px;padding:0 2px;font:700 .8rem "Nunito Sans",sans-serif;color:#5F534A;cursor:pointer}
.gl-dot{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:#EFE6D6;box-shadow:inset 0 0 0 1.5px #D9CBB2;font-size:.8rem}
.gl-path .done .gl-dot{background:#2D4E86;color:#fff;box-shadow:none;font-weight:900}.gl-path .open .gl-dot{background:#fff}
.gl-pn{display:block;padding:6px 14px;border-radius:999px;background:#2D4E86;color:#fff;font:800 .95rem Fraunces,serif;margin:6px 0}
.gl-ln{flex:1 0 14px;height:2px;background:#D9CBB2;margin:0 2px 18px}
html.yg .gl-path button{color:#D8CCF0}html.yg .gl-dot{background:rgba(255,255,255,.1);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.2)}html.yg .gl-ln{background:rgba(255,255,255,.2)}
.gl-t{text-align:center;margin:6px 16px 12px;font:900 clamp(1.7rem,8vw,2.2rem)/1.05 Fraunces,serif}
.gl-room{position:relative;margin:0 12px;border-radius:22px;overflow:hidden;padding:44px 12px 64px;
  background:radial-gradient(120% 60% at 20% 0,rgba(255,255,255,.5),transparent 60%),linear-gradient(180deg,var(--gw1,#EDE3D0),var(--gw2,#DCCDB1));box-shadow:inset 0 0 0 1px rgba(0,0,0,.06),0 14px 30px -18px rgba(60,40,20,.6)}
.gl-room::before{content:"";position:absolute;left:0;right:0;top:0;height:26px;background:repeating-linear-gradient(90deg,#8C6A48 0 34px,#7A5A3B 34px 38px,transparent 38px 92px),linear-gradient(#9A7652,#7C5B3C);opacity:.9}
.gl-room::after{content:"";position:absolute;left:0;right:0;bottom:0;height:54px;background:radial-gradient(60% 80% at 22% 70%,rgba(255,255,255,.55),transparent 60%),linear-gradient(180deg,#E9DFCC,#F5EFE4);box-shadow:0 -1px 0 rgba(0,0,0,.08)}
.gl-room.r-pets{--gw1:#EEE4D2;--gw2:#D9CAB0}.gl-room.r-travel{--gw1:#D6E4F1;--gw2:#A9C2DC}.gl-room.r-night{--gw1:#DCE7D3;--gw2:#B4C9A6}.gl-room.r-selfie{--gw1:#F2DDD5;--gw2:#DDB9AC}
.gl-room.r-fitness{--gw1:#DDEBD6;--gw2:#B8D1AC}.gl-room.r-food{--gw1:#F5E0CA;--gw2:#E3BE98}.gl-room.r-style{--gw1:#E6E1EE;--gw2:#C7BDD8}
.gl-room.t-gold{background:linear-gradient(90deg,rgba(120,80,10,.25),transparent 12%,transparent 88%,rgba(120,80,10,.25)),linear-gradient(180deg,#F6DA8A,#DDB04C 55%,#B98A2E);box-shadow:inset 0 0 0 6px #C99A3A,inset 0 0 0 8px #F7E2A2,0 16px 34px -16px rgba(120,80,10,.7)}
.gl-room.t-diamond{background:radial-gradient(circle at 20% 30%,rgba(255,255,255,.9) 0 2px,transparent 3px),radial-gradient(circle at 75% 20%,rgba(255,255,255,.9) 0 2px,transparent 3px),radial-gradient(circle at 60% 65%,rgba(255,255,255,.8) 0 1.5px,transparent 3px),linear-gradient(180deg,#EEF6FF,#BCD5F2);box-shadow:inset 0 0 0 6px #A9C6EA,inset 0 0 0 8px #F2F8FF,0 16px 34px -16px rgba(40,80,140,.6)}
.gl-room.t-platinum{background:radial-gradient(100% 60% at 50% 0,#FFFFFF,transparent 70%),linear-gradient(180deg,#F7F7F8,#D7DAE0);box-shadow:inset 0 0 0 6px #C3C8D0,inset 0 0 0 8px #FFFFFF,0 16px 34px -16px rgba(60,70,90,.6)}
.gl-room[class*=" t-"]::before{background:none}
.gl-room.cele{animation:glcele 1.4s ease}@keyframes glcele{30%{transform:scale(1.03);box-shadow:0 0 0 6px #FFC93C,0 0 40px rgba(255,201,60,.8)}}
.gl-wall{position:relative;z-index:1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.gl-f{position:relative;border:0;background:none;padding:0;display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;min-width:0;font-family:"Nunito Sans",sans-serif;color:#2D2521}
.gl-fr{position:relative;display:block;width:100%;aspect-ratio:3/4;padding:7px;border-radius:3px;background:linear-gradient(135deg,#B08356,#7A5230 45%,#A57A4C 70%,#6E4524);box-shadow:inset 0 0 0 1px rgba(255,255,255,.3),0 10px 16px -8px rgba(0,0,0,.6)}
.gl-fr img{display:block;width:100%;height:100%;object-fit:cover;border:3px solid #F4EEE2;border-radius:1px}
.gl-fr.t-gold,.gl-trio.t-gold .gl-fr{background:linear-gradient(135deg,#FFF1A8,#E2B13C 30%,#A8761A 55%,#F6D67A 75%,#B98A2A);box-shadow:inset 0 0 0 2px #8A5A0A,inset 0 0 0 4px #FFE9A0,0 12px 18px -8px rgba(0,0,0,.6)}
.gl-fr.t-diamond,.gl-trio.t-diamond .gl-fr{background:linear-gradient(135deg,#FFFFFF,#BFD9FF 35%,#7FA7E6 60%,#E6F1FF);box-shadow:inset 0 0 0 2px #5B7FC0,inset 0 0 0 4px #F2F8FF,0 0 16px rgba(159,210,255,.8),0 12px 18px -8px rgba(0,0,0,.5)}
.gl-fr.t-platinum,.gl-trio.t-platinum .gl-fr{background:linear-gradient(135deg,#FFFFFF,#D7DCE3 40%,#9AA3AF 65%,#F2F4F7);box-shadow:inset 0 0 0 2px #7D8693,inset 0 0 0 4px #FFFFFF,0 12px 18px -8px rgba(0,0,0,.5)}
.gl-room[class*=" t-"] .gl-f::before{content:"";position:absolute;top:-16px;left:50%;width:34px;height:7px;margin-left:-17px;border-radius:3px;background:linear-gradient(#E9C46A,#9C6E14);box-shadow:0 1px 2px rgba(0,0,0,.4)}
.gl-room[class*=" t-"] .gl-f::after{content:"";position:absolute;top:-10px;left:50%;width:120%;height:60%;transform:translateX(-50%);background:radial-gradient(50% 60% at 50% 0,rgba(255,244,200,.55),transparent 70%);pointer-events:none}
.gl-f.empty .gl-fr{background:linear-gradient(135deg,#C9A57A,#8E6A44 50%,#B9946A);display:block}
.gl-f.empty .gl-fr b{display:grid;place-items:center;width:100%;height:100%;background:#F7F2E8;border:3px solid #EFE6D6;font:500 2.4rem/1 "Nunito Sans",sans-serif;color:#2D2521}
.gl-pl{display:inline-flex;align-items:baseline;gap:4px;padding:3px 10px;border-radius:7px;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #D8C49E,0 2px 4px rgba(0,0,0,.15);font:800 1rem/1.2 Fraunces,serif;color:#2D2521;white-space:nowrap}
.gl-pl em{font:800 .62rem "Nunito Sans",sans-serif;font-style:normal;text-transform:uppercase;letter-spacing:.04em;color:#8A5A0A}
.gl-f small{font-size:.72rem;font-weight:700;color:#4E433C;white-space:nowrap}.gl-room.t-gold .gl-f small{color:#4A3204}
.gl-ban{position:relative;z-index:1;margin:16px auto 0;width:max-content;max-width:94%;text-align:center;padding:7px 22px 6px;border-radius:8px;background:linear-gradient(180deg,#FBE7A4,#D9A93E);box-shadow:inset 0 0 0 2px #9C6E14,inset 0 0 0 4px #FFF1C2,0 6px 12px -6px rgba(0,0,0,.6);color:#4A3204}
.gl-room.t-diamond .gl-ban{background:linear-gradient(180deg,#FFFFFF,#BFD6F2);box-shadow:inset 0 0 0 2px #5B7FC0,inset 0 0 0 4px #fff,0 6px 12px -6px rgba(0,0,0,.5);color:#1E3A6E}
.gl-room.t-platinum .gl-ban{background:linear-gradient(180deg,#FFFFFF,#D7DCE3);box-shadow:inset 0 0 0 2px #7D8693,inset 0 0 0 4px #fff,0 6px 12px -6px rgba(0,0,0,.5);color:#2E3440}
.gl-ban span{display:block;font:900 1.02rem/1.1 Fraunces,serif;letter-spacing:.04em}.gl-ban small{display:block;font:800 .7rem "Nunito Sans",sans-serif;letter-spacing:.18em}
.gl-sub{text-align:center;margin:14px 16px 10px;font:900 1.35rem/1.2 Fraunces,serif}
.gl-go{margin:0 16px;width:calc(100% - 32px)!important;display:flex;align-items:center;justify-content:center;gap:10px}.gl-go img{width:34px;height:34px;border-radius:8px;object-fit:cover;box-shadow:0 0 0 2px #fff}
.gl-earn{text-align:center;margin:12px 20px 0;font-size:.86rem;opacity:.85}
.gl-next{position:relative;display:block;width:calc(100% - 24px);margin:16px 12px 0;border:0;border-radius:18px;padding:34px 12px 14px;text-align:center;cursor:pointer;overflow:hidden;color:#2D2521;
  background:radial-gradient(ellipse 18% 70% at 18% 100%,rgba(255,255,255,.55) 60%,transparent 62%),radial-gradient(ellipse 18% 70% at 50% 100%,rgba(255,255,255,.55) 60%,transparent 62%),radial-gradient(ellipse 18% 70% at 82% 100%,rgba(255,255,255,.55) 60%,transparent 62%),linear-gradient(180deg,var(--gw1,#EDE3D0),var(--gw2,#DCCDB1));box-shadow:inset 0 0 0 3px #C9A57A,0 10px 20px -12px rgba(0,0,0,.5)}
.gl-next.r-travel{--gw1:#D6E4F1;--gw2:#A9C2DC}.gl-next.r-night{--gw1:#DCE7D3;--gw2:#B4C9A6}.gl-next.r-selfie{--gw1:#F2DDD5;--gw2:#DDB9AC}.gl-next.r-fitness{--gw1:#DDEBD6;--gw2:#B8D1AC}.gl-next.r-food{--gw1:#F5E0CA;--gw2:#E3BE98}.gl-next.r-style{--gw1:#E6E1EE;--gw2:#C7BDD8}
.gl-nl{display:inline-block;padding:6px 16px;border-radius:10px;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #D8C49E;font:800 1.1rem Fraunces,serif}
.gl-next small{display:block;margin-top:8px;font-weight:700;font-size:.84rem}
.gl-tie{margin:8px 0 0;font-size:.9rem;opacity:.9}
.gl-pick{display:none!important;position:fixed;left:50%;top:118px;z-index:205;display:flex;align-items:center;gap:10px;padding:6px 14px 6px 6px;border-radius:999px;background:#FBF6EC;color:#2D2521;box-shadow:inset 0 0 0 1.5px #D8C49E,0 12px 24px -10px rgba(0,0,0,.45);transform:translate(-50%,-14px);opacity:0;transition:transform .3s,opacity .3s;pointer-events:none;max-width:92vw}
.gl-pick.on{transform:translate(-50%,0);opacity:1}.gl-pick img{width:38px;height:38px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #FFC93C}
.gl-pick b{display:block;font:800 .92rem "Nunito Sans",sans-serif}.gl-pick small{display:block;font-size:.8rem;color:#2E6B42;font-weight:800}
.gl-trio{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:4px 6px 0;position:relative;z-index:2}
.gl-pop{text-align:center}.gl-pop>*:not(.cr-rays):not(.wp-cf){position:relative;z-index:2}.gl-pop h2{margin-top:18px!important}
.gl-hang h2{margin:0 0 6px}.gl-hang p{margin:0 0 12px}.gl-hg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.gl-hg button{position:relative;border:0;padding:0;border-radius:12px;overflow:hidden;aspect-ratio:1;cursor:pointer}.gl-hg img{width:100%;height:100%;object-fit:cover;display:block}
.gl-hg b{position:absolute;left:6px;bottom:6px;padding:2px 8px;border-radius:999px;background:rgba(20,16,14,.75);color:#fff;font-size:.85rem}
html.yg .gl-seg button[aria-selected="true"],html.yg .gl-pn,html.yg .gl-path .done .gl-dot{background:linear-gradient(95deg,#7B3CFF,#FF2D8E);color:#fff}
html.yg .gl-t,html.yg .gl-sub{font-family:"Bricolage Grotesque",sans-serif;font-weight:800}
@media (prefers-reduced-motion:reduce){.gl-room.cele{animation:none}.gl-pick{transition:none}}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('galleries ok')
