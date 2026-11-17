# Real Money build, step 5 (after rmshow.py):
#  - Best in Show has 6 finalists (3 groups, top 2 of each go through); big photos in the catalogue and the pick screen
#  - only 4 show categories: Pets, Nature & landscapes, Garden & flowers, Food (Food waits for sample photos)
#  - group judging shows its prize table
#  - exhibitors: "Enter a photo to compete" costs 200 coins (first one free); prizes are cash for everyone
#  - "My show" tab replaces Compete: every photo, its placings, next show and winnings
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# ---------- shows: 4 categories, 6 finalists ----------
s = s.replace("function fcNotify() {", r"""const SHOWS = [{ k: 'pets', n: 'Pets', seed: ['Pets'] }, { k: 'nature', n: 'Nature & landscapes', seed: ['Nature', 'Travel', 'Wildlife'] }, { k: 'garden', n: 'Garden & flowers', seed: ['Nature', 'Travel'] }, { k: 'food', n: 'Food', seed: ['Food'], soon: 1 }];
const SHOW_ROT = SHOWS.filter(x => !x.soon);
function showName(k) { const x = SHOWS.find(z => z.k === k); return x ? x.n : crownName(k); }
function photoShow(p) { const c = p && p.cat, y = isYoungW(); if (!c) return null;
  if (['pets', 'wildlife'].includes(c)) return 'pets'; if (c === 'food') return 'food';
  if (c === 'garden' || (!y && c === 'fitness')) return 'garden'; if (['landscape', 'sunrise', 'golden', 'hiking'].includes(c) || (!y && c === 'night') || (y && c === 'travel')) return 'nature'; return null; }
var SHOW_ENTRY = 200;
function fcNotify() {""", 1)
RA("RACE_N = 9,", "RACE_N = 6,")
RA("RACE_FIN = [.2, .16, .13, .11, .1, .09, .08, .07, .06],", "RACE_FIN = [.27, .21, .17, .14, .11, .1],")
RA("function ppGame(sl = ppSlot()) { const ks = CATS8.filter(k => k !== 'any'), k = ks[sl % ks.length], r = cpRng(sl * 13 + 7);\n  const pool = SEED.filter(x => x.src && x.cat === BATTLE_POOL[k]),",
   "function ppGame(sl = ppSlot()) { const SH = SHOW_ROT[sl % SHOW_ROT.length], k = SH.k, r = cpRng(sl * 13 + 7);\n  const pool = SEED.filter(x => x.src && SH.seed.includes(x.cat)),")
RA("t: mp.title || `My ${crownName(k)} shot`", "t: mp.title || `My ${showName(k).toLowerCase()} photo`")
s = re.sub(r"crownName\((g|n)\.k\)", lambda m: "showName(%s.k)" % m.group(1), s)
# a photo races in the next show of its own category
RA("const rcSlotFor = p => { const cur = ppSlot(), R = S.races || {}, ks = CATS8.filter(k => k !== 'any'); for (let sl = cur + 1; sl <= cur + ks.length; sl++) if (!R[sl] && fitsTheme(p, ks[sl % ks.length])) return sl; for (let sl = cur + 1; ; sl++) if (!R[sl]) return sl; };",
   "const rcSlotFor = p => { const cur = ppSlot(), R = S.races || {}, k = photoShow(p); for (let sl = cur + 1; sl <= cur + 3 * SHOW_ROT.length; sl++) if (!R[sl] && SHOW_ROT[sl % SHOW_ROT.length].k === k) return sl; for (let sl = cur + 1; ; sl++) if (!R[sl]) return sl; };")
# groups: top 2 go through (3 groups x 2 = 6 finalists)
RA("for (let t = 0; t < 3 && [0, 1, 2].some(j => R.ph[3 * gi + j] && R.ph[3 * gi + j].mine); t++) gi = (gi + 1) % 3;\n  const q = [0, 1, 2].map(j => R.ph[3 * gi + j]).sort((a, b) => b.st - a.st),",
   "for (let t = 0; t < 3 && [0, 1].some(j => R.ph[2 * gi + j] && R.ph[2 * gi + j].mine); t++) gi = (gi + 1) % 3;\n  const q = [0, 1].map(j => R.ph[2 * gi + j]).sort((a, b) => b.st - a.st),")
RA(".slice(0, 2).map((x, i) => ({ src: x.src, t: x.title || 'Untitled', h: QS_NAMES[(ns + i + 3) % QS_NAMES.length] }));",
   ".slice(0, 3).map((x, i) => ({ src: x.src, t: x.title || 'Untitled', h: QS_NAMES[(ns + i + 3) % QS_NAMES.length] }));")
RA("<small>Crowd’s top 3 · qualified ✓</small>", "<small>Crowd’s top 3 · 🥇🥈 go through</small>")
RA("These 3 go through to the <b>${raceName(G.ns)} Best in Show</b>", "The top 2 go through to the <b>${raceName(G.ns)} Best in Show</b>")
RA("Its top 3 photos go through to the", "Its top 2 photos go through to the")
RA("if (pl <= 3) { const sl = rcSlotFor(p);", "if (pl <= 2) { const sl = rcSlotFor(p);")
s = s.replace("· top 3 go through`", "· top 2 go through`").replace("Top 3 in a group go through", "Top 2 in a group go through")
# a group's extra photos come from the same show category first
RA("const fill = ppShuffle(SEED.filter(x => x.src && !used.has(x.src)), rr).slice(0, 3)",
   "const shSeed = (SHOWS.find(z => z.k === R.k) || { seed: [] }).seed, fill = ppShuffle(SEED.filter(x => x.src && !used.has(x.src) && shSeed.includes(x.cat)), rr).concat(ppShuffle(SEED.filter(x => x.src && !used.has(x.src) && !shSeed.includes(x.cat)), rr)).slice(0, 3)")
# group judging prize table on the pick screen
RA("<p class=\"pp-m\">${real ? `Real entry · <b>$${GATE_FEE}</b> · perfect 1-2-3 wins <b>$${GATE_CASH[3]}</b>` : `Free · perfect 1-2-3 wins <b>${GATE_COINS[3]} 🟡</b> · 2 right <b>${GATE_COINS[2]} 🟡</b>`}</p>",
   "<div class=\"gt-tab\"><div class=\"${real ? '' : 'on'}\"><b>Free</b><span>3 right <em>${GATE_COINS[3]} 🟡</em></span><span>2 right <em>${GATE_COINS[2]} 🟡</em></span></div><div class=\"${real ? 'on' : ''}\"><b>For real · $${GATE_FEE}</b><span>3 right <em>$${GATE_CASH[3]}</em></span><span>2 right <em>$${GATE_CASH[2].toFixed(2)}</em></span></div></div><p class=\"gt-tab-n\">“Right” = the right photo in the right place</p>")
# 6-finalist pick grid: 2 across, big photos
s = s.replace('class="pp-g g9"', 'class="pp-g g6"')
RA("Pick the top 3 of 9", "Pick the top 3 of 6")
# show catalogue: big photo cards
RA("<div class=\"rc-l\"><p class=\"rc-cols\"><span>Finalist</span><span>Placings</span><span>Favourite</span></p>${g.ph.map((p, i) => `<div class=\"rc-r ${p.mine ? 'me' : ''}\"><img src=\"${p.src}\" alt=\"\"><span class=\"rc-t\"><b>${esc(p.t)}</b><small>@${esc(p.h)}${p.mine ? ' · you' : ''}</small></span><span class=\"rf\">${formHTML(p.form)}</span><em><i style=\"width:${Math.min(100, bk[i] * 2)}%\"></i>${bk[i]}%</em></div>`).join('')}</div>",
   "<div class=\"rc-g\">${g.ph.map((p, i) => `<div class=\"rc-c ${p.mine ? 'me' : ''}\"><img src=\"${p.src}\" alt=\"\"><b>${esc(p.t)}</b><small>@${esc(p.h)}${p.mine ? ' · you' : ''}</small><div class=\"rc-cf\"><span class=\"rf\">${formHTML(p.form)}</span><em>${bk[i]}% fav</em></div></div>`).join('')}</div>")
# exhibitor prizes are cash for everyone (a free path to real money); doesn't make you a cash player
RA("function raceOwnResult(sl) { const x = S.races[sl], g = ppGame(sl), i = g.ph.findIndex(p => p.mine), cash = isCash(), y = isYoungW();",
   "function raceOwnResult(sl) { const x = S.races[sl], g = ppGame(sl), i = g.ph.findIndex(p => p.mine), cash = true, y = isYoungW();")
RA("r.last = { sl, pl, pz, cash: cash ? 1 : 0 };", "r.last = { sl, pl, pz, cash: cash ? 1 : 0 }; S.showWon = +((S.showWon || 0) + pz).toFixed(2);")

# ---------- exhibitors: entering costs 200 coins (first free); My show tab ----------
s = s.replace("function fcNotify() {", r"""function showEnter(id) { const p = (S.photos || []).find(x => x.id === id), y = isYoungW(); if (!p) return; const k = photoShow(p), SH = SHOWS.find(x => x.k === k);
  if (!SH) { toast('Only Pets, Nature & landscapes, Garden & flowers and Food photos can be shown.'); return; }
  if (SH.soon) { toast('Food shows open soon. Enter a Pets, Nature or Garden photo for now.'); return; }
  if (p.s.total < FR_MIN) { S.cur = p.id; save(); go('studio'); renderStudio(); toast(`${y ? 'Enhance' : 'Touch up'} to ${FR_MIN}+ to enter the show`); return; }
  const free = !S.showFreeUsed; if (!free && (S.gems || 0) < SHOW_ENTRY) { runOut('gems', `You need ${SHOW_ENTRY - Math.floor(S.gems || 0)} more coins`, null, SHOW_ENTRY - (S.gems || 0)); return; }
  if (free) S.showFreeUsed = 1; else { S.gems -= SHOW_ENTRY; paintGems(); }
  const r = rcRec(id); r.st = 'heats'; S.hN = Math.max(S.hN || 0, HEAT_EVERY - 2); save(); toast(`🎀 ${rcName(p)} is in group judging! First group in ${HEAT_EVERY - S.hN} ${y ? 'judge' : 'vote'}s.`); myShow(); }
function myShow() { if ($('#sheet').classList.contains('on')) closeSheet(); popClose(); go('gallery'); renderMyShow(); }
function renderMyShow() { const g = $('#gallery'); if (!g) return; $('#ptitle').textContent = 'My show'; const y = isYoungW(), P = (S.photos || []).slice().sort((a, b) => b.s.total - a.s.total), cur = ppSlot(), nx = ppGame(cur);
  const inG = P.filter(p => rcRec(p.id).st === 'heats').length, thr = P.filter(p => rcRec(p.id).st === 'q').length, free = !S.showFreeUsed;
  const card = p => { const r = rcRec(p.id), k0 = photoShow(p), x0 = rcStatus(p), x = !k0 ? { cls: 'n', ic: '📷', t: 'Not a show category', s: 'Only Pets, Nature, Garden and Food photos can enter' } : x0.cls === 'n' ? { cls: 'n', ic: '📷', t: 'Not entered yet', s: `Enter it: the top 2 in a group go through, and Best in Show 🥇🥈🥉 win $10 · $5 · $2` } : x0, f = r.f.map(z => z.pl), k = photoShow(p), SH = SHOWS.find(z => z.k === k), can = !r.st && SH && !SH.soon && p.s.total >= FR_MIN;
    return `<div class="ms-c ${x.cls}"><img src="${p.src}" alt=""><div class="ms-t"><b>${esc(rcName(p))} <em>${p.s.total}</em></b>${SH ? `<span class="ms-k">${SH.n}${SH.soon ? ' · shows open soon' : ''}</span>` : ''}<span>${x.ic} ${x.t}</span><small>${x.s}</small>${f.length ? `<span class="rf">${formHTML(f)}</span>` : ''}${r.last && r.last.pz ? `<span class="ms-w">Won ${money(r.last.pz)}</span>` : ''}</div>
      ${can ? `<button class="btn ms-go" data-msen="${p.id}">Enter<small>${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</small></button>` : r.st === 'q' ? `<button class="btn ms-go ms-w2" data-msw="${r.sl}">${r.sl === cur ? '🔴 Watch' : 'Catalogue'}</button>` : !SH ? '' : p.s.total < FR_MIN && !r.st ? `<button class="btn ms-go ms-up" data-msup="${p.id}">${y ? 'Enhance' : 'Touch up'}<small>to ${FR_MIN}+</small></button>` : ''}</div>`; };
  g.innerHTML = `<div class="ms"><h1 class="ms-h">🎀 My show</h1><p class="ms-sub">Your photos in group judging and the hourly Best in Show</p>
    <div class="ms-sum"><div><b>${money(S.showWon || 0)}</b><small>won</small></div><div><b>${inG}</b><small>in group judging</small></div><div><b>${thr}</b><small>through to Best in Show</small></div></div>
    <button class="ms-next" id="msCat"><span>🎀 Now: the ${raceName(cur)} Best in Show · ${esc(showName(nx.k))}</span><b>Catalogue ›</b></button>
    <button class="btn block ms-add" id="msAdd">📷 Enter a new photo to compete · ${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</button>
    <div class="ms-l">${P.length ? P.map(card).join('') : '<p class="ms-none">No photos yet. Upload one to start showing.</p>'}</div>
    <p class="ms-r">Categories: Pets · Nature & landscapes · Garden & flowers · Food (soon). Top 2 in a group go through. Best in Show 🥇🥈🥉 win <b>$10 · $5 · $2</b> real cash.</p></div>`;
  g.querySelectorAll('[data-msen]').forEach(b => b.onclick = () => showEnter(b.dataset.msen));
  g.querySelectorAll('[data-msw]').forEach(b => b.onclick = () => +b.dataset.msw === cur ? ppOpen() : raceCard());
  g.querySelectorAll('[data-msup]').forEach(b => b.onclick = () => { S.cur = b.dataset.msup; save(); go('studio'); renderStudio(); });
  $('#msCat').onclick = () => raceCard(); $('#msAdd').onclick = () => { S.frameHint = { cats: ['pets'], lab: 'Pets', frame: 'Pets' }; save(); pickPhoto(true); }; }
function showRowHTML() { const free = !S.showFreeUsed, ok = free || (S.gems || 0) >= SHOW_ENTRY;
  return `<button class="ug-r ug-swap" id="msRow"><span class="ug-i">📷</span><span class="ug-t"><b>Enter a photo to compete</b><small>Group judging, then the hourly Best in Show · top 3 win $10 · $5 · $2</small></span><em class="${ok ? '' : 'need'}">${free ? 'Free' : `${SHOW_ENTRY} 🟡`}</em></button>`; }
document.addEventListener('click', e => { if (e.target.closest('#msRow')) { e.preventDefault(); e.stopPropagation(); myShow(); } }, true);
function fcNotify() {""", 1)
RA("function stableOpen() {", "function stableOpen() { myShow(); return;")
RA("$('#segGallery').onclick = () => openBattleTab();", "$('#segGallery').onclick = () => myShow();")
RA('</svg><span>Compete</span><i class="fr-dot" id="frDot" hidden></i></button>', '</svg><span>My show</span><i class="fr-dot" id="frDot" hidden></i></button>')
RA("${raceBetRowHTML()}", "${showRowHTML()}${raceBetRowHTML()}")

s = s.replace('</style>', """.pp-g.g6{grid-template-columns:repeat(2,1fr)!important;gap:8px!important}.pp-g.g6 .pp-t{grid-column:auto!important}.pp-g.g6 .pp-im img{aspect-ratio:4/3!important;height:auto!important}.pp-g.g6 .pp-cap{font-size:.72rem!important;padding:3px 6px 4px!important}.pp-g.g6 .pp-b{font-size:2.2rem!important}
.rc-g{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:4px 0 10px;text-align:left}.rc-c{border-radius:14px;overflow:hidden;padding-bottom:6px}.rc-c img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;margin-bottom:5px}.rc-c>b{display:block;font-size:.88rem;padding:0 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rc-c>small{display:block;font-size:.7rem;padding:0 8px;opacity:.8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rc-cf{display:flex;justify-content:space-between;align-items:center;padding:4px 8px 0}.rc-cf em{font-style:normal;font-weight:900;font-size:.76rem}.rc-c.me{box-shadow:0 0 0 3px #2EA36B}
html:not(.yg) .rc-c{background:#F3ECDF;color:#2B2320}html.yg .rc-c{background:#2A1A52;color:#fff}
.gt-tab{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:2px 0 4px}.gt-tab>div{border-radius:12px;padding:6px 8px;text-align:left;font-size:.8rem;display:flex;flex-direction:column;gap:2px;opacity:.75}.gt-tab>div.on{opacity:1;box-shadow:inset 0 0 0 2px #F2C14E}.gt-tab b{font-size:.78rem}.gt-tab em{font-style:normal;font-weight:900;float:right}.gt-tab-n{margin:0 0 8px;font-size:.7rem;opacity:.75}
html:not(.yg) .gt-tab>div{background:#F3ECDF;color:#2B2320}html.yg .gt-tab>div{background:#2A1A52;color:#fff}
.ms{padding:14px 16px 120px}.ms-h{margin:4px 0 2px;font-size:1.9rem}.ms-sub{margin:0 0 12px;opacity:.8}.ms-sum{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 10px}.ms-sum>div{border-radius:14px;padding:10px 6px;text-align:center}.ms-sum b{display:block;font-size:1.3rem;font-weight:900}.ms-sum small{font-size:.72rem;opacity:.8}
.ms-next{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;border:0;border-radius:14px;padding:12px 14px;margin:0 0 10px;font:inherit;font-size:.86rem;text-align:left;cursor:pointer}.ms-add{margin:0 0 12px!important}
.ms-c{display:grid;grid-template-columns:110px 1fr auto;gap:12px;align-items:center;padding:10px;border-radius:16px;margin:0 0 10px}.ms-c>img{width:110px;height:110px;object-fit:cover;border-radius:12px}.ms-t{display:flex;flex-direction:column;gap:2px;min-width:0}.ms-t>b{font-size:1rem}.ms-t>b em{font-style:normal;font-size:.72rem;font-weight:900;padding:1px 6px;border-radius:6px;background:rgba(127,127,127,.18);margin-left:4px}.ms-k{font-size:.72rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase;opacity:.7}.ms-t>span{font-size:.84rem}.ms-t>small{font-size:.74rem;opacity:.8}.ms-w{font-weight:900;color:#2EA36B}
.ms-go{margin:0!important;padding:9px 12px!important;font-size:.82rem!important;min-height:0!important;width:auto!important;display:flex!important;flex-direction:column;align-items:center;text-transform:none!important}.ms-go small{font-size:.66rem;opacity:.85}.ms-r{font-size:.78rem;opacity:.8;margin:8px 0 0}.ms-none{opacity:.8}
html:not(.yg) .ms{color:#2B2320}html:not(.yg) .ms-sum>div,html:not(.yg) .ms-c,html:not(.yg) .ms-next{background:#F3ECDF;color:#2B2320}html:not(.yg) .ms-c.q{box-shadow:inset 0 0 0 2px #2F6B3F}html:not(.yg) .ms-go{background:#2F6B3F!important;color:#fff!important}html:not(.yg) .ms-w2{background:#2D4E86!important}html:not(.yg) .ms-up{background:#8B6A2A!important}
html.yg .ms{color:#fff}html.yg .ms-sum>div,html.yg .ms-c,html.yg .ms-next{background:#2A1A52;color:#fff}html.yg .ms-c.q{box-shadow:inset 0 0 0 2px #2EE59D}html.yg .ms-go{background:#2EE59D!important;color:#14092B!important}html.yg .ms-w2{background:#C13CFF!important;color:#fff!important}
</style>""", 1)

# My show tab icon: a rosette instead of VS
a = s.index('<button id="segGallery" aria-pressed="false">'); b = s.index('<span>My show</span>', a)
s = s[:a] + '<button id="segGallery" aria-pressed="false"><span class="ms-ic" aria-hidden="true">🎀</span>' + s[b:]
s = s.replace('</style>', '.seg #segGallery .ms-ic{display:block;font-size:1.45rem;line-height:1.1}\n</style>', 1)
# group result: one clear headline
RA("<h2 class=\"pp-h\">${pay ? `You won ${amt}!` : right === 1 ? '1 in the right place' : 'Not this time'}</h2>", "<h2 class=\"pp-h\">${pay ? `You won ${amt}!` : 'Not this time'}</h2>")
open(d + 'yofi-real.html', 'w').write(s); print('rm v2 ok')
