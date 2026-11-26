# One Compete menu (Skill preview): the bottom menu becomes Vote · Compete · Touch-ups.
# Compete has a tab bar at the top: Challenges (today's photo challenges) | Tournaments (the tournament list).
# Each tab shows the same page as before; the separate Tournaments button is hidden.
# Usage: python3 build-skill/compete.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function cmpBar(' in s: sys.exit('compete already applied')

JS = r'''
/* ---------- one Compete menu with Challenges | Tournaments tabs ---------- */
let CMP_TAB = 'ch';
const cmpBar = t => `<div class="cmp-bar" role="tablist" aria-label="Compete"><button role="tab" data-cmp="ch" aria-selected="${t === 'ch'}">🏅 Challenges</button><button role="tab" data-cmp="tour" aria-selected="${t === 'tour'}">🏆 Tournaments</button></div>`;
const _segTourGo = $('#segCompete').onclick;
function cmpOpen(t) {
  CMP_TAB = t;
  if (t === 'tour') { try { _segTourGo(); } catch (e) {} setTimeout(cmpPaint, 30); }
  else { try { closeSheet(); } catch (e) {} if ($('#flow').classList.contains('on')) { try { closeFlow(); } catch (e) {} } openBattleTab(); setTimeout(cmpPaint, 30); }
  $('#segGallery').setAttribute('aria-pressed', 'true'); $('#segCompete').setAttribute('aria-pressed', 'false');
}
function cmpWire(el) { el.querySelectorAll('[data-cmp]').forEach(b => b.onclick = () => cmpOpen(b.dataset.cmp)); }
function cmpPaint() {
  const fl = $('#flow'), fb = $('#flowBody');
  if (CMP_TAB === 'tour' && fl.classList.contains('on') && fb && !fb.querySelector('.cmp-bar')) { fb.querySelectorAll('.cmp-h').forEach(e => e.remove()); fb.insertAdjacentHTML('afterbegin', cmpBar('tour')); cmpWire(fb); $('#segGallery').setAttribute('aria-pressed', 'true'); $('#segCompete').setAttribute('aria-pressed', 'false'); }
  const g = $('#gallery'); if (g && $('#panes').dataset.at === 'gallery' && GV.tab === 'battle' && !fl.classList.contains('on') && !g.querySelector('.cmp-bar')) { g.querySelectorAll('.cmp-h').forEach(e => e.remove()); g.insertAdjacentHTML('afterbegin', cmpBar('ch')); cmpWire(g); }
}
const _renderGalleryC = renderGallery;
renderGallery = function () { const r = _renderGalleryC.apply(this, arguments); try { if (GV.tab === 'battle') { CMP_TAB = 'ch'; cmpPaint(); } } catch (e) {} return r; };
$('#segGallery').onclick = () => cmpOpen(CMP_TAB === 'tour' ? 'tour' : 'ch');
$('#segCompete').onclick = () => cmpOpen('tour');
const _closeFlowC = closeFlow; closeFlow = function () { const r = _closeFlowC.apply(this, arguments); if (CMP_TAB === 'tour') CMP_TAB = 'ch'; return r; };

// "Use your coins": Touch-ups first, then Compete (games); no coin-for-ticket swap
useGems = function () {
  const I = gemIdeas(), isTU = x => /touch up|enhance|improve/i.test(x.t), gal = I.filter(isTU), cmp = I.filter(x => !isTU(x));
  const row = x => { const i = I.indexOf(x); return `<button class="ug-r" data-ug="${i}"><span class="ug-i">${x.ic}</span><span class="ug-t"><b>${x.t}</b><small>${x.d}</small></span><em class="ug-c${S.gems < x.cost ? ' need' : ''}">${x.cost} 🟡</em></button>`; };
  openSheet(`<div class="ug"><h2>Use your coins</h2><p class="sub">You have <b>${Math.floor(S.gems).toLocaleString()} 🟡</b>. Here’s what they can do for you right now.</p>
    ${I.length ? `${gal.length ? `<h3 class="ug-h">✨ Touch-ups</h3>${gal.map(row).join('')}` : ''}${cmp.length ? `<h3 class="ug-h">🏅 Compete</h3>${cmp.map(row).join('')}` : ''}` : `<p class="ug-none">Upload a photo and your coins can start working for you.</p>`}
    <button class="link ug-buy" id="ugBuy">💵 Get cash</button></div>`);
  document.querySelectorAll('#sheetBody [data-ug]').forEach(b => b.onclick = () => { const x = I[+b.dataset.ug];
    if (isTU(x)) { const ph = S.photos.find(q => q.src === x.src) || S.photos.filter(q => q.s && lowestOpen(q)).sort((a, b) => a.s.total - b.s.total)[0] || cur(); closeSheet(); if (ph) galImprove(ph.id); go('studio'); return; }
    if (S.gems < x.cost) { closeSheet(); runOut('gems', `You need ${x.cost - S.gems} more coins`, null, x.cost - S.gems); return; } x.go(); });
  $('#ugBuy').onclick = () => { closeSheet(); openStore(); };
};

// bottom menu order: Vote · Touch-ups · Compete
(() => { const a = $('#segStudio'), b = $('#segGallery'); if (a && b && b.parentNode === a.parentNode) b.parentNode.insertBefore(a, b); })();
// tournament list: only the next tournament of each kind (same prize and entry)
function cmpDedupe() {
  const rows = document.querySelectorAll('#flowBody .tsr2'); if (!rows.length) return; const seen = new Set();
  rows.forEach(r => { const k = ((r.querySelector('.tsr2-p') || {}).textContent || '') + '|' + ((r.querySelector('.tsr2-e') || {}).textContent || '') + '|' + (r.classList.contains('frrow') ? 'fr' : '');
    if (r.style.display !== 'none' && seen.has(k)) r.style.display = 'none'; else if (!seen.has(k)) { seen.add(k); r.style.display = ''; } });
}
new MutationObserver(() => { try { cmpDedupe(); cmpTourCards(); } catch (e) {} }).observe($('#flowBody'), { childList: true, subtree: true });

// middle menu is Gallery
(() => { const sp = $('#segStudio') && $('#segStudio').querySelector('span'); if (sp) sp.textContent = 'Gallery'; })();
// tournaments as big cards (one per kind); Enter opens that tournament as before
const CMP_IC = {
  watch: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"><circle cx="34" cy="36" r="20"/><path d="M34 36l8-9M28 10h12M34 10v6M50 20l4-4M4 30h10M2 38h12M6 46h10"/></svg>',
  trophy: '<svg viewBox="0 0 64 64" fill="currentColor"><path d="M18 8h28v14a14 14 0 0 1-28 0z"/><path d="M18 12H8a10 10 0 0 0 12 12M46 12h10a10 10 0 0 1-12 12" fill="none" stroke="currentColor" stroke-width="4"/><rect x="29" y="34" width="6" height="12"/><path d="M20 58h24l-3-12H23z"/></svg>',
  crowd: '<svg viewBox="0 0 64 64" fill="currentColor"><circle cx="32" cy="18" r="9"/><circle cx="13" cy="24" r="7"/><circle cx="51" cy="24" r="7"/><path d="M16 56c0-10 7-18 16-18s16 8 16 18zM1 52c0-8 5-14 12-14 3 0 5 1 7 2-4 4-6 8-6 12zM63 52c0-8-5-14-12-14-3 0-5 1-7 2 4 4 6 8 6 12z"/></svg>',
  coin: '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" fill="currentColor"/><circle cx="32" cy="32" r="17" fill="none" stroke="#1F3157" stroke-width="3" opacity=".5"/><path d="M32 22v20" stroke="#1F3157" stroke-width="5" stroke-linecap="round" opacity=".55"/></svg>'
};
function cmpTourCards() {
  const fb = $('#flowBody'); if (CMP_TAB !== 'tour' || !$('#flow').classList.contains('on')) { fb.classList.remove('cmp-t'); return; }
  const rows = [...fb.querySelectorAll('.tsr2')].filter(r => r.style.display !== 'none' && !r.classList.contains('frrow')); if (!rows.length) return;
  const sig = rows.map(r => r.textContent.replace(/\s+/g, '')).join('|'); const old = fb.querySelector('.cmp-cards'); if (old && old.dataset.sig === sig) return;
  const card = (r, i) => { const prize = (r.querySelector('.tsr2-p') || {}).textContent.replace('↑', '').trim(), entry = (r.querySelector('.tsr2-e') || {}).textContent.trim(), when = (r.querySelector('.tsr2-t b') || {}).textContent.trim(), coin = r.classList.contains('gemt') || (r.querySelector('.tsr2-e.pill-coin') != null);
    const crowd = r.classList.contains('chrow'), name = crowd ? 'Crowd Championship' : coin ? 'Coin Cup' : /100/.test(prize) ? 'Big Cup' : 'Sprint', ic = crowd ? CMP_IC.crowd : coin ? CMP_IC.coin : /100/.test(prize) ? CMP_IC.trophy : CMP_IC.watch;
    const pz = coin ? `${prize} 🟡 prize pool` : `${prize.replace('US', '')} prize pool`, en = coin ? `${entry} 🟡 entry` : `${entry} entry`;
    return `<div class="cmp-tc${coin ? ' cmp-c' : ''}"><div class="cmp-ban"><span class="cmp-ic">${ic}</span><span class="cmp-tt"><b>${name}</b><span class="cmp-when">${crowd ? `Ends in ${when}` : /^0?0:|^\d\d:\d\d$/.test(when) && !/h/.test(when) ? `Starts in ${when}` : `Starts in ${when}`}</span></span></div>
      <div class="cmp-ft"><span>${en} · ${pz}</span><button class="cmp-go ${coin ? 'cmp-gold' : 'cmp-green'}" data-ti="${i}">Enter</button></div></div>`; };
  if (old) old.remove();
  fb.classList.add('cmp-t');
  const bar = fb.querySelector('.cmp-bar'); const html = `<div class="cmp-cards" data-sig="${sig}">${rows.map(card).join('')}</div>`;
  if (bar) bar.insertAdjacentHTML('afterend', html); else fb.insertAdjacentHTML('afterbegin', html);
  fb.querySelectorAll('.cmp-go').forEach(b => b.onclick = () => rows[+b.dataset.ti].click());
}
setInterval(() => { try { document.querySelectorAll('.cmp-cards').forEach(c => c.dataset.sig = ''); cmpTourCards(); } catch (e) {} }, 1000);

// tap audit fixes
// 1. Crowd Championship: Enter opens its details first; money is only taken on the green Join button
const _chBuyC = chBuy;
chBuy = function () {
  const E = S.ch || {}, cur = chId(), nxt = cur + 1;
  if (S.geoBlock || (E[cur] && E[cur].score == null) || E[nxt] || (S.cash || 0) < CH_ENTRY) return _chBuyC.apply(this, arguments);
  const at = new Date(nxt * CH_MS).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }), pot = ((document.querySelector('#chRow .tsr2-p') || {}).textContent || '').replace('↑', '').trim();
  openSheet(`<div class="ug"><h2>🏆 Crowd Championship</h2><p class="sub">Pick the photo the crowd chose, pair after pair. The best scores share the prize pool.</p>
    <div class="cmp-tc" style="margin:12px 0"><div class="cmp-ft"><span>Starts at ${at}</span><span>${pot ? pot + ' prize pool' : ''}</span></div></div>
    <button class="btn block pay-cash" id="chJoin">Join for $${CH_ENTRY}</button><div style="text-align:center"><button class="link" data-shclose>Not now</button></div></div>`);
  $('#chJoin').onclick = () => { closeSheet(); _chBuyC(); };
  document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
};
// 2. no "You've got N coins!" pop pushing coin games (coin games live in the coin balance sheet)
gemNudge = function () { return false; };

// one status line, the same on every photo screen
const TIER_IC = { Gold: '🥇', Diamond: '💎', Platinum: '🏆' };
function stLine(v, from) {
  const t = galTier(v), t0 = from == null ? t : galTier(from), pay = GAL.BASE * galMult(v);
  if (from != null && t && t !== t0) return `${TIER_IC[t]} Becomes ${t} · ${pay} coins per vote`;
  return t ? `${TIER_IC[t]} ${t} · ${pay} coins per vote` : 'Not ranked · reach 70 for 🥇 Gold';
}
// big card in the gallery: one status line instead of two
const _renderGalleriesST = renderGalleries;
renderGalleries = function () { const r = _renderGalleriesST.apply(this, arguments);
  const big = document.querySelector('#studio .al-card.big'), P = AL_OPEN && S.photos.find(x => x.id === AL_OPEN);
  if (big && P) { document.querySelectorAll('#studio .al-to, #studio .al-why').forEach(e => e.remove()); big.insertAdjacentHTML('afterend', `<div class="im2-strip st-line"><span class="im2-sh">${stLine(P.s.total)}</span></div>`); }
  return r; };
// Before and after: status of the new version above the Touch up button
const _renderVariantsST = renderVariants;
renderVariants = function () { const r = _renderVariantsST.apply(this, arguments);
  try { const v = EN.variants && EN.variants[EN.sel], act = document.querySelector('#flowBody .actions'); if (v && act && !act.querySelector('.st-line')) act.insertAdjacentHTML('afterbegin', `<div class="im2-strip st-line"><span class="im2-sh">${stLine(v.s.total, EN.p.s.total)}</span></div>`); } catch (e) {}
  try { const g = document.querySelector('#flowBody .goal70'), n = g && +(g.querySelector('span') || g).innerText.replace(/\D/g, ''); if (g && !g.querySelector('.g-ic') && ({ 70: 1, 80: 1, 90: 1 })[n]) g.insertAdjacentHTML('beforeend', ` <i class="g-ic">${({ 70: '🥇', 80: '💎', 90: '🏆' })[n]}</i>`); } catch (e) {}
  return r; };
// every new upload gets a name
S.photos.forEach(p => { if (!p.nmAsk) p.nmAsk = 1; }); save();
function nameAsk() {
  const p = S.photos.find(x => !x.nmAsk && x.s); if (!p || !S.user) return;
  if ($('#flow').classList.contains('on') || $('#sheet').classList.contains('on') || $('#coach').classList.contains('on')) return;
  p.nmAsk = 1; save();
  openSheet(`<div class="ug nm-ask"><img class="nm-ph" src="${p.src}" alt=""><h2>Name your photo</h2><p class="sub">This name shows on its card, in your gallery and when voters pick it.</p>
    <input id="nmIn" maxlength="16" value="${esc(alName(p))}" aria-label="Photo name"><button class="btn block" id="nmGo">Save name</button></div>`);
  const i = $('#nmIn'); setTimeout(() => { i.focus(); i.select(); }, 80);
  const go = () => { const v = i.value.trim(); if (v) p.nm = v; save(); closeSheet(); try { renderStudio(); } catch (e) {} try { vgPaint(); } catch (e) {} };
  $('#nmGo').onclick = go; i.onkeydown = e => { if (e.key === 'Enter') go(); };
}
setInterval(() => { try { nameAsk(); } catch (e) {} }, 800);

// Clubs: show the challenges you can play first; invite comes after (not straight after creating a club)
const CLUB_SEED = 1; // starter pot per category you can play, so it never shows $0.00
let CW_SKIP_INV = false;
const _crewCreateC = crewCreate; crewCreate = function () { CW_SKIP_INV = true; const r = _crewCreateC.apply(this, arguments); setTimeout(() => { CW_SKIP_INV = false; }, 4000); return r; };
const _crewInviteC = crewInvite; crewInvite = function () { if (CW_SKIP_INV) { CW_SKIP_INV = false; try { closeSheet(); } catch (e) {} renderGallery(); return; } return _crewInviteC.apply(this, arguments); };
function clubTidy() {
  const g = $('#gallery'), grid = g && g.querySelector('.tcg'); if (!grid || !g.querySelector('.cw-mem')) return;
  const c = crewCur && crewCur(); if (!c) return; c.pot = c.pot || {}; c.seed = c.seed || {}; let ch = false;
  // starter pots only once 2+ members have each entered: a real (paid) challenge has happened in this club
  const live = (c.members || []).length >= 1 && CATS8.some(k => (c.pot[k] || 0) > (c.seed[k] ? CLUB_SEED : 0));
  CATS8.forEach(k => { const can = S.photos.some(p => fitsTheme(p, k));
    if (live && can && !(c.pot[k] > 0)) { c.pot[k] = CLUB_SEED; c.seed[k] = 1; ch = true; }
    if (!live && c.seed[k]) { c.pot[k] = Math.max(0, +((c.pot[k] || 0) - CLUB_SEED).toFixed(2)); delete c.seed[k]; ch = true; } });
  if (ch) save();
  const cards = [...grid.children], CK = CATS8;
  cards.forEach((el, i) => { const k = CK[i], can = !el.querySelector('.bcc-go.up'), pot = el.querySelector('.bcc-pot'), lab = el.querySelector('.bcc-l');
    if (can && !(c.pot[k] > 0)) { if (pot) pot.textContent = '+$1.70'; if (lab) lab.textContent = 'First challenge adds'; el.classList.add('cw-can'); }
    else if (can) { if (pot) pot.textContent = money(c.pot[k] || 0); if (lab && c.seed[k] && (c.pot[k] || 0) <= CLUB_SEED) lab.textContent = 'Starter pot'; el.classList.add('cw-can'); }
    else { if (pot) pot.style.display = 'none'; if (lab) lab.textContent = 'Add a photo to play'; el.classList.add('cw-cant'); } });
  cards.sort((a, b) => (b.classList.contains('cw-can') ? 1 : 0) - (a.classList.contains('cw-can') ? 1 : 0)).forEach(el => grid.appendChild(el));
  const mem = g.querySelector('.cw-mem'), hdr = g.querySelector('.cw-play');
  if (!hdr) { grid.insertAdjacentHTML('beforebegin', `<h3 class="cw-play">Your challenges</h3>`); g.querySelector('.tcg').insertAdjacentElement('afterend', mem); mem.classList.add('cw-mem-end'); }
}
const _renderGalleryCW = renderGallery;
renderGallery = function () { const r = _renderGalleryCW.apply(this, arguments); try { clubTidy(); } catch (e) {} return r; };

// 1. first-photo screen: if you already picked a category on the landing page, don't ask again
function obuTidy() {
  const h = document.querySelector('.obu-h'), g = document.querySelector('.obu-c'); if (!h || !g || g.dataset.tidy) return;
  const sel = g.querySelector('[aria-pressed="true"]'); if (!sel || !window.__preCat) return;
  g.dataset.tidy = 1; const nm = sel.innerText.replace(/\s+/g, ' ').trim();
  h.innerHTML = `Your photo: <b>${esc(nm)}</b> <button class="link obu-chg" type="button">Change</button>`; g.style.display = 'none';
  h.querySelector('.obu-chg').onclick = () => { g.style.display = ''; h.textContent = 'What’s your photo of?'; };
}
setInterval(() => { try { obuTidy(); } catch (e) {} }, 250);
// sample photos match the category (Nature/Garden were showing people)
try { Object.assign(BATTLE_POOL, { night: 'Nature', fitness: 'Nature', style: 'Travel' }); } catch (e) {}
// 2. the gallery starts with the category of your first photo
function galFirstCat() {
  if (!S.galFirst) { const f = S.photos.filter(p => p.s && GAL.PATH.includes(p.cat)).sort((a, b) => (a.at || 0) - (b.at || 0))[0]; if (f && !Object.keys(S.galBest || {}).length) { S.galFirst = f.cat; save(); } }
  const c = S.galFirst; if (c && GAL.PATH[0] !== c && GAL.PATH.includes(c)) { GAL.PATH.splice(GAL.PATH.indexOf(c), 1); GAL.PATH.unshift(c); if (!S.galCat || !galOpen(S.galCat)) S.galCat = c; }
}
galFirstCat(); setInterval(() => { try { const b = GAL.PATH[0]; galFirstCat(); if (GAL.PATH[0] !== b && $('#panes').dataset.at === 'studio') renderStudio(); } catch (e) {} }, 1000);
new MutationObserver(() => { try { cmpPaint(); } catch (e) {} }).observe($('#flowBody'), { childList: true });
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]
CSS = r'''
/* one Compete menu */
.obu-chg{font-size:.9rem;margin-left:6px;padding:0}
.cw-play{margin:4px 16px 8px;font:900 1.2rem Fraunces,serif;color:#5A1A22}.cw-mem-end{margin-top:14px!important}.cw-cant{opacity:.72}
html body #gallery .cw-can .bcc-go{background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important}
.st-line{margin:12px 14px 8px!important}#flowBody .actions .st-line{margin:0 0 10px!important}
/* Before and after matches Improve: centred bold status, Goal pill with its medal, readable After label */
html body #flowBody .st-line{text-align:center!important;padding:10px 12px!important}html body #flowBody .st-line .im2-sh{margin:0!important;text-align:center;font-weight:700;font-size:.95rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#flowBody .goal70 .g-ic{font-style:normal;margin-left:2px}
html body #flowBody .vcard[aria-pressed="true"] .best{background:#2D4E86!important;color:#fff!important}
/* Vote: same gap above and below the photos block */
html body #vgGoal.vg{margin:6px 0 12px!important}
/* one menu style on Gallery and Compete: tabs at the same spot, same font; section titles in the album burgundy */
html body .gl-seg,html body .cmp-bar{margin:4px 14px 14px!important;width:auto!important}html body .tot-h .gl-seg{margin:0 0 14px!important;width:100%!important}
html body .gl-seg button,html body .cmp-bar button{font:800 1rem "Nunito Sans",sans-serif!important;padding:10px 6px!important}
#studio .tot-h:has(.gl-seg),html body #studio .gl.a2,html body #studio .gl.im2{background:none!important;box-shadow:none!important}html body #studio .gl.a2,html body #studio .gl.im2{margin-top:0!important;padding-top:0!important}
html body #gallery .bt-sw button{font:800 .95rem "Nunito Sans",sans-serif!important}
html body #gallery h1:not(.cmp-h),html body .im2 h2,html body .im2-t{font-family:Fraunces,serif!important;font-weight:900!important;color:#7A1F27!important}
html.yg body #gallery h1:not(.cmp-h),html.yg body .im2 h2,html.yg body .im2-t{color:#fff!important}
.nm-ask{text-align:center}.nm-ph{width:120px;height:160px;object-fit:cover;border-radius:14px;box-shadow:0 0 0 3px #E0A82E;margin:4px auto 10px;display:block}
.nm-ask input{width:100%;box-sizing:border-box;margin:6px 0 12px;padding:12px 14px;border-radius:14px;border:1.5px solid #CDBFA8;font:800 1.2rem Fraunces,serif;text-align:center;background:#FFFDF9;color:#2D2521}
/* Improve photo frame stands out more (drawn outside the photo, so sizes don't change) */
html body .im2 .im2-ph{box-shadow:0 0 0 3px #CDBFA8,0 0 0 6px #FBF6EC,0 12px 22px -12px rgba(0,0,0,.6)!important}
html body .im2 .im2-ph.t-gold{box-shadow:0 0 0 4px #E0A82E,0 0 0 7px #FBEFD2,0 0 0 8.5px #C99A2E,0 0 18px rgba(224,168,46,.55),0 12px 22px -12px rgba(0,0,0,.6)!important}
html body .im2 .im2-ph.t-diamond{box-shadow:0 0 0 4px #7FA7E6,0 0 0 7px #EEF5FF,0 0 0 8.5px #5B7FC0,0 0 20px rgba(127,167,230,.7),0 12px 22px -12px rgba(0,0,0,.6)!important}
html body .im2 .im2-ph.t-platinum{box-shadow:0 0 0 4px #A7B0BD,0 0 0 7px #FFFFFF,0 0 0 8.5px #7D8693,0 0 18px rgba(167,176,189,.7),0 12px 22px -12px rgba(0,0,0,.6)!important}

#btGem{display:none!important}
.cmp-h{text-align:center;margin:6px 16px 10px;font:900 clamp(1.9rem,8.6vw,2.4rem)/1 Fraunces,serif;color:#1F3157}html.yg .cmp-h{color:#fff}
#flowBody.cmp-t>*:not(.cmp-bar):not(.cmp-cards):not(.cmp-h){display:none!important}
.cmp-cards{display:flex;flex-direction:column;gap:14px;margin:0 14px 24px}
.cmp-tc{border-radius:20px;padding:8px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 8px 18px -12px rgba(60,40,20,.5)}
.cmp-ban{display:flex;align-items:center;gap:14px;padding:14px 16px;border-radius:14px;background:linear-gradient(160deg,#1F3157,#14213D)}
.cmp-ic{flex:none;width:96px;height:84px;color:#E9B52F;filter:drop-shadow(0 3px 6px rgba(0,0,0,.35))}.cmp-ic svg{width:100%;height:100%}
.cmp-tt{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:10px}
.cmp-tt b{font:900 clamp(1.6rem,7.2vw,2.1rem)/1.02 Fraunces,serif;color:#fff}
.cmp-when{padding:6px 14px;border-radius:999px;background:#FBF6EC;color:#1F3157;font:800 .95rem Fraunces,serif;white-space:nowrap}
.cmp-ft{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 6px 4px}
.cmp-ft span{font:700 1rem Fraunces,serif;color:#2D2521}
#flowBody .cmp-go{flex:none;border:0;border-radius:12px;padding:10px 20px;font:800 1rem Fraunces,serif;cursor:pointer;color:#fff!important;background:linear-gradient(180deg,#2E9A5C,#21784A)!important;box-shadow:0 6px 14px -8px rgba(33,120,74,.8)!important;min-height:0;width:auto}
#flowBody .cmp-go.cmp-gold{color:#3A2600!important;background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;box-shadow:0 6px 14px -8px rgba(160,110,10,.7)!important}
#flowBody .cmp-tc span,#flowBody .cmp-tc b{position:static}#flowBody .cmp-ft span{display:inline}
html.yg .cmp-tc{background:#FBF6EC}

.ug-h{margin:14px 2px 8px;font:900 1.25rem Fraunces,serif;color:#5A1A22}html.yg .ug-h{color:#FF8FC4}
.ug .ug-r em.ug-c{background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important}.ug .ug-r em.ug-c.need{opacity:.6}
#segCompete{display:none!important}
.cmp-bar{position:sticky;top:0;z-index:4;display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:4px 14px 12px;padding:4px;border-radius:16px;background:#EFE6D6;box-shadow:inset 0 0 0 1.5px #E2D5BE}
.cmp-bar button{border:0;background:none;border-radius:12px;padding:9px 6px;font:800 1rem "Nunito Sans",sans-serif;color:#5F534A;cursor:pointer}
.cmp-bar button[aria-selected="true"]{background:#2D4E86;color:#fff;box-shadow:0 4px 10px -4px rgba(45,78,134,.6)}
html.yg .cmp-bar{background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.14)}html.yg .cmp-bar button{color:#D8CCF0}
html.yg .cmp-bar button[aria-selected="true"]{background:linear-gradient(95deg,#7B3CFF,#FF2D8E);color:#fff}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('compete ok')
