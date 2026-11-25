# Gallery as a card album (Skill preview). Runs after galleries.py and keeps all of its rules
# (rooms open in order, tier set by the lowest photo, vote earnings); only the look changes:
# - "My gallery": category tabs, the collection title, and a binder page with clear sleeves holding your photos as cards.
#   Card foil shows the tier: plain under 70, gold foil, holographic Diamond, silver Platinum.
#   The fourth sleeve shows the next collection (locked, or ready to open).
# - Tapping a card opens it big: name, score and tier, its coin rate, points to the next tier, and "Improve <name>".
# - Photos get names (Milo, Cleo, Pip...) that you can change on the big card; names are used in pops and the vote chip.
# Usage: python3 build-skill/album.py [in.html] [out.html]  (defaults to index.html in place)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function renderGalleries(' not in s: sys.exit('run galleries.py first')
if 'function alCard(' in s: sys.exit('album already applied')

JS = r'''
/* ---------- gallery album ---------- */
const AL_NAMES = { pets: ['Milo', 'Cleo', 'Pip', 'Luna', 'Rex', 'Bella', 'Max', 'Daisy'], travel: ['Coast', 'Kyoto', 'Alps', 'Lisbon', 'Santorini', 'Havana'], night: ['Falls', 'Pines', 'Summit', 'Meadow', 'Aurora'],
  selfie: ['Sunday', 'Picnic', 'Beach day', 'Birthday', 'Grandma'], fitness: ['Roses', 'Tulips', 'Orchard', 'Bloom'], food: ['Sourdough', 'Tart', 'Feast', 'Pancakes'], style: ['Loft', 'Nook', 'Kitchen', 'Snug'] };
function alName(p) {
  if (p.nm) return p.nm;
  const used = S.photos.filter(x => x.cat === p.cat && x.nm).map(x => x.nm), list = AL_NAMES[p.cat] || ['Photo'];
  p.nm = list.find(n => !used.includes(n)) || (list[0] + ' ' + (used.length + 1)); save(); return p.nm;
}
const alTierCls = v => (galTier(v) || 'plain').toLowerCase();
function alCard(p, big) {
  const v = p.s.total, t = galTier(v), x = galMult(v);
  if (big) return `<div class="al-card big t-${alTierCls(v)}"><div class="al-in"><div class="al-top"><input class="al-nm" id="alNm" value="${esc(alName(p))}" maxlength="16" aria-label="Photo name"><span class="al-gem" aria-hidden="true">${t === 'Diamond' ? '💎' : t === 'Platinum' ? '🏆' : t === 'Gold' ? '🥇' : ''}</span><span class="al-sc"><b>${v}</b><em>${t || 'No tier yet'}</em></span></div>
    <img src="${p.src}" alt=""><div class="al-bot"><b>${x}× coins</b><span>${GAL.BASE * x} coins per vote received</span></div></div></div>`;
  return `<span class="al-card t-${alTierCls(v)}"><span class="al-in"><img src="${p.src}" alt=""><i class="al-tag">${v}${t ? ' · ' + t : ''}</i><span class="al-cap"><b>${esc(alName(p))}</b></span></span></span>`;
}
let AL_OPEN = null;
renderGalleries = function () {
  const st = $('#studio'); st.classList.remove('tallp');
  const P = AL_OPEN && S.photos.find(x => x.id === AL_OPEN);
  if (P) {
    const v = P.s.total, nb = [70, 80, 90].find(b => v < b), x = galMult(v);
    st.innerHTML = `<div class="gl al">${galSeg('gal')}<button class="al-back" id="alBack">‹ ${esc(galNm(P.cat))} collection</button>${alCard(P, 1)}
      <p class="al-to"><span>${nb ? `${nb - v} point${nb - v === 1 ? '' : 's'} to ${galBand(nb)}` : 'Platinum · the top tier'}</span></p>
      ${galNextMult(v) ? `<p class="al-why">At ${galNextMult(v).at} it earns ${galNextMult(v).x}× (${GAL.BASE * galNextMult(v).x} coins a vote)</p>` : ''}
      <button class="btn block gl-go" id="alImp">Improve ${esc(alName(P))}</button></div>`;
    galWire(st);
    $('#alBack').onclick = () => { AL_OPEN = null; renderStudio(); st.scrollTop = 0; };
    $('#alImp').onclick = () => { AL_OPEN = null; galImprove(P.id); };
    const n = $('#alNm'); n.onchange = () => { const v2 = n.value.trim(); if (v2) { P.nm = v2; save(); } else n.value = alName(P); };
    n.onkeydown = e => { if (e.key === 'Enter') n.blur(); };
    return;
  }
  let c = S.galCat && galOpen(S.galCat) ? S.galCat : (GAL.PATH.filter(galOpen).find(x => galRoom(x).tier !== 'Platinum') || 'pets');
  const r = galRoom(c);
  const tabs = GAL.PATH.map(x => `<button data-gc="${x}" class="${x === c ? 'on' : galOpen(x) ? '' : 'lock'}">${esc(galNm(x))}${galOpen(x) ? '' : ' <i aria-label="locked">🔒</i>'}</button>`).join('<i class="al-bar" aria-hidden="true"></i>');
  const sleeves = [0, 1, 2].map(i => { const p = r.ph[i];
    return p ? `<button class="al-sl" data-alc="${p.id}" aria-label="${esc(alName(p))}, ${p.s.total}">${alCard(p)}<small>${galToday(p)} coin${galToday(p) === 1 ? '' : 's'} today</small></button>`
      : `<button class="al-sl empty" data-gadd="${c}"><span class="al-add"><b>+</b>Add a ${esc(galNm(c).toLowerCase())} photo</span><small>Empty sleeve</small></button>`; });
  const nx = GAL.PATH[GAL.PATH.indexOf(c) + 1], nxOpen = nx && galOpen(nx);
  sleeves.push(nx ? `<button class="al-sl al-nx${nxOpen ? ' open' : ''}" data-gc="${nx}"><span class="al-nxi"><b>${nxOpen ? '✨' : '🔒'}</b>Next: ${esc(galNm(nx))}<em>${nxOpen ? 'Open now' : `All 3 ${esc(galNm(c))} photos at Gold (70)`}</em></span></button>` : '<span class="al-sl blank"></span>');
  let sub, act = '';
  if (!r.ph.length) { sub = `Add 3 ${esc(galNm(c).toLowerCase())} photos to start this collection`; act = `<button class="btn block gl-go" data-gadd="${c}">Add your first ${esc(galNm(c).toLowerCase())} photo</button>`; }
  else if (!r.full) { sub = `${r.ph.length} of 3 photos · ${3 - r.ph.length} sleeve${3 - r.ph.length === 1 ? '' : 's'} to fill`; act = `<button class="btn block gl-go" data-gadd="${c}">Add a photo</button>`; }
  else if (r.next) { sub = `${r.at} of 3 at ${galBand(r.next)}`; const b = r.ph.filter(p => p.s.total < r.next).sort((a, b) => b.s.total - a.s.total)[0];
    act = `<button class="btn block gl-go" data-gimp="${b.id}"><img src="${b.src}" alt="">Improve ${esc(alName(b))} · ${b.s.total} → ${r.next}</button>`; }
  else sub = 'All three at Platinum';
  const opened = GAL.PATH.filter(galOpen).find(x => x !== c && !galRoom(x).ph.length);
  if (r.tier && opened) act = `<button class="al-link" data-gc="${opened}">Open ${esc(galNm(opened))} →</button>`;
  const day = S.photos.reduce((a, x) => a + galToday(x), 0);
  st.innerHTML = `<div class="gl al">${galSeg('gal')}<h2 class="al-h">My gallery</h2><nav class="al-tabs" aria-label="Collections">${tabs}</nav>
    <h3 class="al-t">${r.tier ? `${r.tier} ${esc(galNm(c))} Collection` : `${esc(galNm(c))} Collection`}</h3><p class="al-sub">${sub}</p>
    <div class="al-book t-${(r.tier || 'none').toLowerCase()}"><i class="al-ring"></i><i class="al-ring"></i><i class="al-ring"></i><div class="al-grid">${sleeves.join('')}</div></div>
    ${act}<p class="gl-earn">${day ? `Your photos earned <b>+${day} coins</b> from votes today` : 'Your cards earn coins every time a voter picks them'} · Gold ×2–3 · Diamond ×4–5 · Platinum ×6</p></div>`;
  galWire(st);
  st.querySelectorAll('[data-gc]').forEach(b => b.onclick = () => { const x = b.dataset.gc; if (!galOpen(x)) { const pv = GAL.PATH[GAL.PATH.indexOf(x) - 1]; toast(`${galNm(x)} opens when all 3 ${galNm(pv)} photos reach Gold`); return; } S.galCat = x; save(); renderStudio(); st.scrollTop = 0; });
  st.querySelectorAll('[data-gadd]').forEach(b => b.onclick = () => galAdd(b.dataset.gadd));
  st.querySelectorAll('[data-gimp]').forEach(b => b.onclick = () => galImprove(b.dataset.gimp));
  st.querySelectorAll('[data-alc]').forEach(b => b.onclick = () => { AL_OPEN = b.dataset.alc; renderStudio(); st.scrollTop = 0; });
  const tb = st.querySelector('.al-tabs .on'); if (tb) tb.scrollIntoView({ inline: 'center', block: 'nearest' });
};
// names in the vote chip, the Improve hint and the collection pop
const _galPickA = galPick;
galPick = function () { const n0 = document.querySelectorAll('.gl-pick').length; _galPickA(); const el = [...document.querySelectorAll('.gl-pick')].pop();
  if (el && document.querySelectorAll('.gl-pick').length > n0) { const img = el.querySelector('img'), p = S.photos.find(x => x.src === img.getAttribute('src')); if (p) el.querySelector('b').textContent = `${alName(p)} was picked`; } };
const _galImproveA = galImprove;
galImprove = function (id) { _galImproveA(id); const p = S.photos.find(x => x.id === id); if (p && window.__sdWhy) { window.__sdWhy = window.__sdWhy.replace(/^[^·]+gallery/, esc(alName(p))); renderStudio(); } };
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]

CSS = r'''
/* gallery album */
.al-h{text-align:center;margin:2px 16px 6px;font:900 clamp(1.9rem,9vw,2.4rem)/1.05 Fraunces,serif}
.al-tabs{display:flex;align-items:center;justify-content:safe center;gap:4px;overflow-x:auto;padding:0 16px 4px;scrollbar-width:none}.al-tabs::-webkit-scrollbar{display:none}
.al-tabs button{flex:none;border:0;background:none;padding:6px 8px 7px;font:600 1.05rem Fraunces,serif;color:#2D2521;cursor:pointer;border-bottom:2.5px solid transparent}
.al-tabs button.on{color:#9E2F2A;border-bottom-color:#9E2F2A;font-weight:800}.al-tabs button.lock{color:#8C8077}.al-tabs i{font-style:normal;font-size:.8rem}
.al-bar{flex:none;width:1px;height:18px;background:#CDBFA8}
html.yg .al-tabs button{color:#E9E1F7}html.yg .al-tabs button.on{color:#FF7AB8;border-bottom-color:#FF7AB8}html.yg .al-tabs button.lock{color:#9A8FB3}
.al-t{text-align:center;margin:12px 16px 0;font:900 clamp(1.45rem,7vw,1.85rem)/1.1 Fraunces,serif}
.al-sub{text-align:center;margin:2px 16px 12px;font:600 1.02rem Fraunces,serif;opacity:.75}
.al-book{position:relative;margin:0 12px 14px;padding:14px 12px 14px 38px;border-radius:12px;background:linear-gradient(90deg,#E6DCCB 0 24px,#D9CDB8 24px 25px,#F7F2E9 25px);box-shadow:inset 0 0 0 1px rgba(120,100,70,.18),0 18px 30px -18px rgba(60,40,20,.55),4px 0 0 -1px #EFE7D9,8px 0 0 -2px #E5DBC9}
.al-ring{position:absolute;left:6px;width:30px;height:14px;border-radius:8px;background:linear-gradient(180deg,#FFF1B0,#D9A93E 45%,#9C6E14 70%,#E9C46A);box-shadow:0 2px 3px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.7)}
.al-ring:nth-child(1){top:14%}.al-ring:nth-child(2){top:48%}.al-ring:nth-child(3){top:82%}
.al-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.al-sl{position:relative;border:0;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px 8px 6px;border-radius:10px;min-width:0;color:#2D2521;font-family:"Nunito Sans",sans-serif;
  background:linear-gradient(165deg,rgba(255,255,255,.85),rgba(255,255,255,.45) 45%,rgba(255,255,255,.7));box-shadow:inset 0 0 0 1.5px rgba(196,184,160,.75),inset 0 10px 16px -12px rgba(0,0,0,.18),0 1px 0 rgba(255,255,255,.8)}
.al-sl::after{content:"";position:absolute;inset:0;border-radius:10px;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.55) 42%,transparent 54%);pointer-events:none}
.al-sl small{font:600 .82rem Fraunces,serif;color:#4E433C}
.al-sl.blank{box-shadow:inset 0 0 0 1.5px rgba(196,184,160,.5)}
.al-card{position:relative;display:block;width:100%;border-radius:12px;padding:4px;background:linear-gradient(160deg,#EFE6D6,#D8CBB2);box-shadow:0 6px 12px -6px rgba(0,0,0,.45)}
.al-card.t-gold{background:linear-gradient(135deg,#FFF3B0,#E7B940 25%,#B8862A 45%,#FBE39A 60%,#C99A2E 80%,#FFF1B5)}
.al-card.t-diamond{background:linear-gradient(120deg,#BFE3FF,#E7C9FF 20%,#FFD6E8 38%,#FFF3C4 55%,#C8FFE6 72%,#BFD9FF 88%,#E7C9FF);background-size:220% 220%;animation:alholo 6s linear infinite;box-shadow:0 0 12px rgba(160,200,255,.7),0 6px 12px -6px rgba(0,0,0,.4)}
.al-card.t-platinum{background:linear-gradient(135deg,#FFFFFF,#D9DEE6 30%,#A7B0BD 50%,#F4F6F9 68%,#C5CCD6 85%,#FFFFFF);background-size:200% 200%;animation:alholo 8s linear infinite}
@keyframes alholo{0%{background-position:0% 50%}100%{background-position:220% 50%}}
.al-in{position:relative;display:block;border-radius:9px;overflow:hidden;background:#FBF7EF}
.al-tag{position:absolute;right:5px;top:5px;font-style:normal;font-size:.68rem;font-weight:800;padding:2px 7px;border-radius:999px;background:rgba(251,246,236,.94);box-shadow:inset 0 0 0 1px #D8C49E,0 2px 4px rgba(0,0,0,.2);white-space:nowrap;color:#2D2521}
.al-in img{display:block;width:100%;aspect-ratio:4/4.3;object-fit:cover}
.al-cap{display:block;padding:5px 6px 6px;text-align:left}
.al-cap b{font:800 1.02rem/1 Fraunces,serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.al-cap i{flex:none;font-style:normal;font-size:.68rem;font-weight:800;padding:2px 6px;border-radius:999px;background:#FBF6EC;box-shadow:inset 0 0 0 1px #D8C49E;white-space:nowrap}
.al-sl.empty .al-add{display:grid;place-items:center;align-content:center;gap:4px;width:100%;aspect-ratio:4/5.1;border-radius:10px;border:2px dashed #CDBFA8;font:700 .82rem "Nunito Sans",sans-serif;color:#6F6258;text-align:center;padding:6px}
.al-add b{font:400 2.2rem/1 "Nunito Sans",sans-serif;color:#2D4E86}
.al-nx .al-nxi{display:grid;place-items:center;align-content:center;gap:4px;width:100%;aspect-ratio:4/5.1;border-radius:10px;background:linear-gradient(180deg,#EFE7D9,#E2D6C2);font:800 1rem Fraunces,serif;text-align:center;padding:8px;color:#5F534A}
.al-nx .al-nxi b{font-size:1.5rem}.al-nx .al-nxi em{font:700 .74rem "Nunito Sans",sans-serif;font-style:normal;opacity:.85}
.al-nx.open .al-nxi{background:linear-gradient(180deg,#FFF3C4,#F3D27A);color:#4A3204}
.al-link{display:block;margin:2px auto 0;border:0;background:none;font:700 1.15rem Fraunces,serif;color:#2D2521;text-decoration:underline;text-underline-offset:4px;cursor:pointer;padding:8px}
html.yg .al-link{color:#fff}
.al-back{display:block;border:0;background:none;margin:0 16px 8px;padding:4px 0;font:600 1.05rem Fraunces,serif;color:inherit;cursor:pointer}
.al-card.big{width:auto;margin:0 16px;padding:7px;border-radius:22px}
.al-card.big .al-in{border-radius:16px;padding:10px 10px 0}
.al-top{display:flex;align-items:center;gap:8px;padding:2px 4px 10px}
.al-nm{flex:1;min-width:0;border:0;background:none;font:900 clamp(1.9rem,9vw,2.5rem)/1 Fraunces,serif;color:#2D2521;padding:0;border-bottom:1.5px dashed transparent}
.al-nm:focus{outline:none;border-bottom-color:#CDBFA8}
.al-gem{font-size:1.4rem;opacity:.85}
.al-sc{display:flex;flex-direction:column;align-items:flex-end;padding-left:10px;border-left:1.5px solid #E2D5BE}.al-sc b{font:900 2.3rem/1 Fraunces,serif;color:#2D2521}.al-sc em{font:600 .95rem Fraunces,serif;font-style:italic;color:#2D2521}
.al-card.big img{border-radius:12px;aspect-ratio:1/1}
.al-bot{display:flex;align-items:center;gap:12px;padding:12px 8px 14px}.al-bot b{font:900 1.9rem/1 Fraunces,serif;color:#2D2521;padding-right:12px;border-right:1.5px solid #E2D5BE;white-space:nowrap}.al-bot span{font:600 1rem/1.25 Fraunces,serif;color:#2D2521}
.al-to{display:flex;align-items:center;gap:12px;margin:18px 24px 4px;font:600 1.15rem Fraunces,serif}.al-to::before,.al-to::after{content:"";flex:1;height:1px;background:#CDBFA8}
.al-why{text-align:center;margin:0 16px 12px;font-size:.9rem;opacity:.8}
.gl-trio .gl-fr{border-radius:12px;padding:4px;background:linear-gradient(160deg,#EFE6D6,#D8CBB2)}.gl-trio .gl-fr img{border:0;border-radius:9px}
.gl-trio.t-diamond .gl-fr{background:linear-gradient(120deg,#BFE3FF,#E7C9FF 20%,#FFD6E8 38%,#FFF3C4 55%,#C8FFE6 72%,#BFD9FF 88%,#E7C9FF);background-size:220% 220%;animation:alholo 6s linear infinite}
.al-sl,.al-cap b,.al-nm,.al-sc b,.al-sc em,.al-bot b,.al-bot span{color:#2D2521!important}.al-sl small{color:#4E433C!important}.al-add{color:#6F6258!important}
@media (prefers-reduced-motion:reduce){.al-card{animation:none!important}}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('album ok')
