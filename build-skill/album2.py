# Gallery album, second look (Skill preview). Runs after album.py; the big card view and all rules stay.
# - "My gallery" between gold rules, category pills with icons (burgundy when selected, lock when closed).
# - "Pets collection" in burgundy with a "1/3 filled" (or tier) badge.
# - Stitched cream binder, 2 x 2 sleeves: photo cards in tier foil with a score bubble, name + tier badge,
#   and a burgundy band "2× coins per vote · +20 coins today"; empty sleeves "+ Add a pet photo" with the
#   category icon; the fourth sleeve is a picture of the next collection with a lock and its name.
# - Progress dots (one per photo at the next tier) + "Get 3 pets to Gold (70+) to unlock Travel", then one big button.
# Usage: python3 build-skill/album2.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function alCard(' not in s: sys.exit('run album.py first')
if 'function al2Card(' in s: sys.exit('album2 already applied')

JS = r'''
/* ---------- gallery album, second look ---------- */
const AL2_ONE = { pets: 'pet', travel: 'travel', night: 'nature', selfie: 'family', fitness: 'garden', food: 'baking', style: 'home' };
const AL2_SEED = { travel: 'Travel', night: 'Nature', selfie: 'People', fitness: 'Nature', food: 'Food', style: 'Cities', pets: 'Pets' };
const al2Ic = c => { const P = { pets: '<circle cx="6" cy="9" r="2"/><circle cx="10" cy="5.5" r="2"/><circle cx="14" cy="5.5" r="2"/><circle cx="18" cy="9" r="2"/><path d="M12 11c-3 0-6 4-6 7 0 2 2 2.5 3 2 1-.4 2-1 3-1s2 .6 3 1c1 .5 3 0 3-2 0-3-3-7-6-7z"/>',
  travel: '<path d="M2 16l20-8-3-2-7 3-6-4-2 1 4 5-4 2-2-1-1 1z"/>', night: '<path d="M5 19C5 10 11 5 20 4c0 9-5 15-14 15zM5 19l8-8"/>', selfie: '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M14 20c0-2.5 1.5-4.5 3.5-4.5S21 17.5 21 20"/>',
  fitness: '<circle cx="12" cy="9" r="3"/><path d="M12 3v3M12 12v9M7 6l2 2M17 6l-2 2M8 16c2 0 4 1 4 3M16 16c-2 0-4 1-4 3"/>', food: '<path d="M4 13h16l-2 7H6zM7 13c0-4 2-7 5-7s5 3 5 7M12 6V3"/>', style: '<path d="M3 11l9-7 9 7v9H3zM9 20v-6h6v6"/>' };
  const f = c === 'pets' ? 'currentColor' : 'none'; return `<svg viewBox="0 0 24 24" width="18" height="18" fill="${f}" stroke="currentColor" stroke-width="${c === 'pets' ? 0 : 1.9}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[c] || P.style}</svg>`; };
const al2Seed = c => { const k = AL2_SEED[c]; const x = SEED.find(y => y.cat === k && y.src) || SEED[0]; return x.src; };
function al2Card(p) {
  const v = p.s.total, t = galTier(v), x = galMult(v), d = galToday(p);
  return `<span class="a2-card t-${(t || 'plain').toLowerCase()}"><span class="a2-ph"><img src="${p.src}" alt=""><b class="a2-sc">${v}</b></span></span>
    <span class="a2-cap"><span class="a2-l1"><b>${esc(alName(p))}</b>${t ? `<i class="a2-tb">${t.toUpperCase()}</i>` : ''}</span><span class="a2-l2"><b>${x}×</b> per vote · <em>+${d} today</em></span></span>`;
}
const _renderGalleriesA2 = renderGalleries;
renderGalleries = function () {
  if (AL_OPEN && S.photos.some(x => x.id === AL_OPEN)) return _renderGalleriesA2.apply(this, arguments);
  const st = $('#studio'); st.classList.remove('tallp');
  let c = S.galCat && galOpen(S.galCat) ? S.galCat : (GAL.PATH.filter(galOpen).find(x => galRoom(x).tier !== 'Platinum') || 'pets');
  const r = galRoom(c), one = AL2_ONE[c] || galNm(c).toLowerCase(), nm = galNm(c);
  const tabs = GAL.PATH.map((x, i) => `${i ? '<i class="a2-sep" aria-hidden="true"></i>' : ''}<button data-gc="${x}" class="${x === c ? 'on' : galOpen(x) ? '' : 'lock'}">${al2Ic(x)}<span>${esc(galNm(x))}</span>${galOpen(x) ? '' : '<i class="a2-lk" aria-label="locked">🔒</i>'}</button>`).join('');
  const sleeves = [0, 1, 2].map(i => { const p = r.ph[i];
    return p ? `<button class="a2-sl" data-alc="${p.id}" aria-label="${esc(alName(p))}, ${p.s.total}">${al2Card(p)}</button>`
      : `<button class="a2-sl empty" data-gadd="${c}"><span class="a2-box"><span class="a2-add"><b>+</b><span>Add a ${esc(one)} photo</span><i class="a2-wm">${al2Ic(c)}</i></span></span><span class="a2-cap"><span class="a2-l1"><b>Empty sleeve</b></span><span class="a2-l2">Earns on votes</span></span></button>`; });
  const nx = GAL.PATH[GAL.PATH.indexOf(c) + 1], nxOpen = nx && galOpen(nx);
  sleeves.push(nx ? `<button class="a2-sl a2-nx${nxOpen ? ' open' : ''}" data-gc="${nx}" aria-label="${esc(galNm(nx))} collection${nxOpen ? '' : ', locked'}"><span class="a2-box"><span class="a2-nxi" style="background-image:url('${al2Seed(nx)}')"><span class="a2-nxl">${nxOpen ? '✨' : '🔒'}</span><span class="a2-plq">${esc(galNm(nx))} collection${nxOpen ? '<small>Open now</small>' : ''}</span></span></span><span class="a2-cap"><span class="a2-l1"><b>Next: ${esc(galNm(nx))}</b></span><span class="a2-l2">${nxOpen ? 'Open now' : 'Opens at Gold'}</span></span></button>` : '<span class="a2-sl blank"><span class="a2-box"></span></span>');
  const band = r.full && r.next ? r.next : 70, bandNm = galBand(band);
  const atBand = r.ph.filter(p => p.s.total >= band).length;
  const dots = [0, 1, 2].map(i => `<i class="${i < atBand ? 'on' : ''} b${band}"></i>`).join('');
  const goalTx = !r.full || !r.tier ? `Get 3 ${esc(one === 'pet' ? 'pets' : one + ' photos')} to Gold (70+)${nx ? ` to unlock ${esc(galNm(nx))}` : ''}`
    : r.next ? `Get all 3 to ${bandNm} (${band}+) for ${galMult(band)}× coins per vote` : 'Every photo at Platinum: the top of this collection';
  const badge = !r.full ? `${r.ph.length}/3 filled` : r.tier ? `${r.tier}` : `${r.at}/3 at Gold`;
  let act = '';
  if (!r.full) act = `<button class="btn block a2-go" data-gadd="${c}">Add a ${esc(one)} photo</button>`;
  else if (r.next) { const b = r.ph.filter(p => p.s.total < r.next).sort((a, b) => b.s.total - a.s.total)[0]; act = `<button class="btn block a2-go" data-gimp="${b.id}">Improve ${esc(alName(b))} · ${b.s.total} → ${r.next}</button>`; }
  const opened = GAL.PATH.filter(galOpen).find(x => x !== c && !galRoom(x).ph.length);
  if (r.tier && opened) act = `<button class="btn block a2-go" data-gc="${opened}">Open ${esc(galNm(opened))} collection</button>`;
  st.innerHTML = `<div class="gl al a2">${galSeg('gal')}<nav class="a2-tabs" aria-label="Collections">${tabs}</nav>
    <div class="a2-th"><h3>${esc(nm)} collection</h3><span class="a2-badge t-${(r.tier || 'none').toLowerCase()}">${badge}</span></div>
    <div class="a2-book"><i class="a2-ring"></i><i class="a2-ring"></i><div class="a2-grid">${sleeves.join('')}</div></div>
    <p class="a2-goal"><span class="a2-dots" aria-hidden="true">${dots}</span><span class="a2-gs"></span><span>${goalTx}</span></p>${act}</div>`;
  galWire(st);
  st.querySelectorAll('[data-gc]').forEach(b => b.onclick = () => { const x = b.dataset.gc; if (!galOpen(x)) { const pv = GAL.PATH[GAL.PATH.indexOf(x) - 1]; toast(`${galNm(x)} opens when all 3 ${galNm(pv)} photos reach Gold`); return; } S.galCat = x; save(); renderStudio(); st.scrollTop = 0; });
  st.querySelectorAll('[data-gadd]').forEach(b => b.onclick = () => galAdd(b.dataset.gadd));
  st.querySelectorAll('[data-gimp]').forEach(b => b.onclick = () => galImprove(b.dataset.gimp));
  st.querySelectorAll('[data-alc]').forEach(b => b.onclick = () => { AL_OPEN = b.dataset.alc; renderStudio(); st.scrollTop = 0; });
  const tb = st.querySelector('.a2-tabs .on'); if (tb) tb.scrollIntoView({ inline: 'center', block: 'nearest' });
};
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]

CSS = r'''
/* gallery album, second look */
.a2-h{display:flex;align-items:center;gap:14px;margin:2px 22px 10px;font:900 clamp(2rem,9.5vw,2.5rem)/1 Fraunces,serif;color:#5A1A22!important}
.a2-h::before,.a2-h::after{content:"";flex:1;height:1.5px;background:linear-gradient(90deg,transparent,#C9A050 30%,#C9A050 70%,transparent)}
.a2-tabs{display:flex;align-items:center;gap:6px;margin:0 12px 14px;padding:6px;border-radius:999px;background:#F6EFE2;box-shadow:inset 0 0 0 1px #E6DAC4,0 4px 10px -6px rgba(60,40,20,.35);overflow-x:auto;scrollbar-width:none}.a2-tabs::-webkit-scrollbar{display:none}
.a2-tabs button{flex:none;display:flex;align-items:center;gap:6px;border:0;background:none;padding:8px 12px;border-radius:999px;font:600 1rem "Nunito Sans",sans-serif;color:#4E433C;cursor:pointer}
.a2-tabs button.on{background:linear-gradient(180deg,#9E2F2A,#6E1D22);color:#fff;box-shadow:0 4px 10px -4px rgba(110,29,34,.7)}
.a2-tabs button.lock{color:#6F6258}.a2-lk{font-style:normal;font-size:.85rem}.a2-sep{flex:none;width:1px;height:20px;background:#D8C9AE}
.a2-th{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 18px 12px}
.a2-th h3{margin:0;font:900 clamp(1.6rem,7.6vw,2rem)/1.05 Fraunces,serif;color:#7A1F27!important}
.a2-badge{flex:none;padding:6px 14px;border-radius:999px;background:linear-gradient(180deg,#FFF8E6,#F5E6C2);box-shadow:inset 0 0 0 1.5px #D9B467,0 3px 6px -3px rgba(0,0,0,.3);font:800 1rem Fraunces,serif;color:#24406F}
.a2-badge.t-gold{background:linear-gradient(180deg,#FFF1B0,#E7B940);color:#4A3204}.a2-badge.t-diamond{background:linear-gradient(180deg,#F2F8FF,#BFD6F2);color:#1E3A6E}.a2-badge.t-platinum{background:linear-gradient(180deg,#fff,#D7DCE3);color:#2E3440}
.a2-book{position:relative;margin:0 12px 12px;padding:16px 14px 16px 40px;border-radius:18px;background:linear-gradient(90deg,#E9DFCC 0 26px,#D8CBB2 26px 27px,#F8F2E6 27px);box-shadow:inset 0 0 0 1.5px #DCCFB6,inset 0 0 0 6px #F8F2E6,inset 0 0 0 7.5px rgba(196,170,120,.55),0 18px 30px -18px rgba(60,40,20,.6)}
.a2-book::after{content:"";position:absolute;inset:10px 10px 10px 34px;border:1.5px dashed rgba(196,170,120,.55);border-radius:12px;pointer-events:none}
.a2-ring{position:absolute;left:4px;width:34px;height:18px;border-radius:10px;background:linear-gradient(180deg,#FFF1B0,#D9A93E 45%,#9C6E14 70%,#E9C46A);box-shadow:0 3px 4px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.7)}
.a2-ring:nth-child(1){top:22%}.a2-ring:nth-child(2){top:68%}
.a2-grid{position:relative;z-index:1;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.a2-sl{position:relative;border:0;padding:0;background:none;border-radius:14px;cursor:pointer;min-width:0;aspect-ratio:4/5.1;font-family:"Nunito Sans",sans-serif;color:#2D2521!important}
.a2-sl.empty,.a2-sl.blank{background:linear-gradient(180deg,#FBF7EE,#F3ECDF);box-shadow:inset 0 0 0 1.5px #E2D5BE,inset 0 6px 12px -8px rgba(0,0,0,.15)}
.a2-add{position:absolute;inset:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;border:1.5px dashed #CDBFA8;border-radius:10px;text-align:center;padding:6px}
.a2-add b{font:300 2.6rem/1 "Nunito Sans",sans-serif;color:#24406F}.a2-add span{font:600 1rem/1.2 "Nunito Sans",sans-serif;color:#2D2521}
.a2-wm{color:#D8CBB2;margin-top:4px}.a2-wm svg{width:28px;height:28px}
.a2-card{position:absolute;inset:0;display:flex;flex-direction:column;border-radius:14px;padding:5px;background:linear-gradient(160deg,#EFE6D6,#CDBFA2);box-shadow:0 8px 14px -8px rgba(0,0,0,.55)}
.a2-card.t-gold{background:linear-gradient(135deg,#FFF3B0,#E7B940 22%,#B8862A 42%,#FBE39A 60%,#C99A2E 80%,#FFF1B5)}
.a2-card.t-diamond{background:linear-gradient(120deg,#BFE3FF,#E7C9FF 20%,#FFD6E8 38%,#FFF3C4 55%,#C8FFE6 72%,#BFD9FF 88%,#E7C9FF);background-size:220% 220%;animation:alholo 6s linear infinite}
.a2-card.t-platinum{background:linear-gradient(135deg,#FFFFFF,#D9DEE6 30%,#A7B0BD 50%,#F4F6F9 68%,#C5CCD6 85%,#FFFFFF);background-size:200% 200%;animation:alholo 8s linear infinite}
.a2-ph{position:relative;flex:1;min-height:0;border-radius:10px 10px 0 0;overflow:hidden;background:#EFE6D6}.a2-ph img{display:block;width:100%;height:100%;object-fit:cover}
.a2-sc{position:absolute;right:6px;top:6px;padding:2px 9px;border-radius:999px;background:linear-gradient(180deg,#FFF8E6,#F3E2B8);box-shadow:inset 0 0 0 1.5px #C9A050,0 2px 4px rgba(0,0,0,.3);font:900 1.05rem/1.2 Fraunces,serif;color:#2D2521}
.a2-nm{display:flex;align-items:center;justify-content:space-between;gap:4px;padding:5px 7px 4px;background:#FBF6EC}
.a2-nm b{font:800 .98rem/1 Fraunces,serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;color:#2D2521}
.a2-tb{flex:none;font:900 .52rem "Nunito Sans",sans-serif;font-style:normal;letter-spacing:.03em;padding:2px 5px;border-radius:999px;background:linear-gradient(180deg,#FFF1B0,#D9A93E);box-shadow:inset 0 0 0 1px #9C6E14;color:#4A3204}
.a2-card.t-diamond .a2-tb{background:linear-gradient(180deg,#fff,#BFD6F2);box-shadow:inset 0 0 0 1px #5B7FC0;color:#1E3A6E}.a2-card.t-platinum .a2-tb{background:linear-gradient(180deg,#fff,#D7DCE3);box-shadow:inset 0 0 0 1px #7D8693;color:#2E3440}
.a2-band{display:block;padding:4px 6px 5px;border-radius:0 0 10px 10px;background:linear-gradient(180deg,#8E2530,#6E1D22);text-align:center;color:#fff}
.a2-band b{display:block;font:800 .8rem/1.15 "Nunito Sans",sans-serif;color:#FFE9A8}.a2-band small{display:block;font-size:.68rem;font-weight:600;color:#fff;opacity:.9}
.a2-nxi{position:absolute;inset:0;border-radius:14px;background-size:cover;background-position:center;box-shadow:inset 0 0 0 5px #F3ECDF,inset 0 0 0 6.5px #D8C49E,0 6px 12px -8px rgba(0,0,0,.45);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0}
.a2-nx:not(.open) .a2-nxi{filter:saturate(.85)}
.a2-nxl{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:linear-gradient(180deg,#FFF8E6,#F3E2B8);box-shadow:0 0 0 2px #C9A050,0 3px 6px rgba(0,0,0,.35);font-size:1.05rem;position:relative;z-index:1;margin-bottom:-8px}
.a2-plq{padding:9px 12px 7px;border-radius:10px;background:linear-gradient(180deg,#FFF8E6,#F1E0B8);box-shadow:inset 0 0 0 1.5px #C9A050,inset 0 0 0 3.5px #FFF8E6,0 6px 12px -6px rgba(0,0,0,.5);font:800 .98rem/1.1 Fraunces,serif;color:#2D2521;text-align:center;max-width:86%}
.a2-plq small{display:block;font:700 .7rem "Nunito Sans",sans-serif;color:#2E6B42}
.a2-goal{display:flex;align-items:center;gap:10px;margin:4px 20px 12px;font-size:.92rem;color:#2D2521}
.a2-dots{display:flex;gap:6px;flex:none}.a2-dots i{width:16px;height:16px;border-radius:50%;background:#E4D7BF;box-shadow:inset 0 1px 2px rgba(0,0,0,.15)}
.a2-dots i.on.b70{background:radial-gradient(circle at 35% 30%,#FFF3A8,#E0A82E 60%,#A8761A)}.a2-dots i.on.b80{background:radial-gradient(circle at 35% 30%,#fff,#8FB6EE 60%,#4A70B8)}.a2-dots i.on.b90{background:radial-gradient(circle at 35% 30%,#fff,#C5CCD6 60%,#7D8693)}
.a2-gs{flex:none;width:1.5px;height:22px;background:#CDBFA8}
.a2-go{margin:0 14px;width:calc(100% - 28px)!important;min-height:56px;border-radius:999px!important;font-size:1.25rem!important}
/* photo fills the card; name, tier, rate and today's coins sit under it */
.a2-sl:not(.empty):not(.blank):not(.a2-nx){aspect-ratio:auto;display:flex;flex-direction:column;gap:6px;padding:0}
.a2-sl:not(.empty):not(.blank):not(.a2-nx) .a2-card{position:relative;inset:auto;aspect-ratio:4/4.6;padding:4px}
.a2 .a2-ph{border-radius:10px}
.a2-cap{display:flex;flex-direction:column;gap:2px;padding:0 3px;text-align:left}
.a2-l1{display:flex;align-items:center;justify-content:space-between;gap:4px}.a2-l1 b{font:800 1rem/1.1 Fraunces,serif;color:#2D2521;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.a2-l2{font-size:.78rem;color:#4E433C;white-space:nowrap}.a2-l2 b{color:#7A1F27;font-weight:900}.a2-l2 em{font-style:normal;font-weight:800;color:#2E6B42}
.a2-sl.empty,.a2-sl.a2-nx,.a2-sl.blank{aspect-ratio:4/5.9;align-self:stretch}
.a2-tabs{margin-top:6px}
.a2-th h3{font-size:clamp(1.35rem,6.6vw,1.85rem)!important;white-space:nowrap}
/* whole photos: frames match the 3:4 upright shape uploads are cropped to */
.a2-sl:not(.empty):not(.blank):not(.a2-nx) .a2-card{aspect-ratio:3/4!important}
.a2-sl.empty,.a2-sl.a2-nx,.a2-sl.blank{aspect-ratio:3/4.95!important}
.al-card.big img{aspect-ratio:3/4!important;max-height:58vh}
.im2 .im2-ph{aspect-ratio:3/4!important}
.a2-ph img,.al-card img,.im2-ph img{object-position:center 35%}
/* one-time score tip */
.a2-tip{position:absolute;z-index:5;left:46%;top:38px;width:190px;padding:10px 12px 10px;border-radius:14px;background:#2D4E86;color:#fff;font:600 .8rem/1.35 "Nunito Sans",sans-serif;text-align:left;box-shadow:0 10px 24px -8px rgba(0,0,0,.55);animation:a2tip .4s cubic-bezier(.2,1.4,.4,1)}
.a2-tip::before{content:"";position:absolute;right:18px;top:-7px;width:14px;height:14px;background:#2D4E86;transform:rotate(45deg);border-radius:2px}
.a2-tip b{display:block;font:800 .9rem Fraunces,serif;margin-bottom:2px;color:#FFE9A8}
.a2-tipok{display:block;margin:8px 0 0 auto;border:0;border-radius:999px;background:#fff;color:#2D4E86;font:800 .8rem "Nunito Sans",sans-serif;padding:5px 12px;cursor:pointer}
@keyframes a2tip{from{transform:scale(.85);opacity:0}}
/* every sleeve: a 3:4 box + a two-line caption, so all four are the same size (Safari too) */
.a2-grid>.a2-sl{aspect-ratio:auto!important;width:100%;min-height:0;display:flex;flex-direction:column;gap:6px;padding:0!important;margin:0!important;background:none!important;box-shadow:none!important}
.a2-sl .a2-card{position:relative!important;inset:auto!important;width:100%;aspect-ratio:3/4!important}
.a2-box{position:relative;display:block;width:100%;aspect-ratio:3/4;border-radius:14px}
.a2-sl.empty .a2-box,.a2-sl.blank .a2-box{background:linear-gradient(180deg,#FBF7EE,#F3ECDF);box-shadow:inset 0 0 0 1.5px #E2D5BE,inset 0 6px 12px -8px rgba(0,0,0,.15)}
.a2-sl.empty .a2-l1 b,.a2-sl.a2-nx .a2-l1 b{color:#6F6258}
.a2-tip{display:none!important}
.a2-cap{min-width:0;overflow:hidden}.a2-l2{overflow:hidden;text-overflow:ellipsis}
html.yg .a2-goal{color:#E9E1F7}html.yg .a2-th h3{color:#FF8FC4!important}html.yg .a2-tabs{background:#FBF6EC}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('album2 ok')
