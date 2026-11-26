# Skill preview: results for games with many players, plus Quick Sprint, in the shared result frame.
# Same frame as the 1 v 1 results (name, headline, prize box, one green button, one link); the middle is
#  - 1 v 1 (Quick Sprint): your eye ring VS theirs, with the scores
#  - many players (Showdown, Crowd Championship, tournaments): your place in the list:
#    the winner, a dashed "paid" line, you highlighted with the players either side, "+N more"
# usage: python3 build-skill/places.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- shared result frame ----
const ORD = n => n + (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] || 'th');
function gsList(rows, total, paidN) { // rows sorted by rank, each { rank, nm, img, val, prize, me }
  const me = rows.find(r => r.me), show = new Set([1]); if (paidN <= 3) for (let k = 2; k <= paidN; k++) show.add(k); if (me) [me.rank - 1, me.rank, me.rank + 1].forEach(k => k >= 1 && k <= total && show.add(k));
  if (!me || me.rank <= 3) [2, 3].forEach(k => k <= total && show.add(k));
  const ks = [...show].sort((a, b) => a - b); let out = '', last = 0;
  const cut = () => `<div class="gpl-cut">${paidN > 1 ? `top ${paidN} paid ↑` : 'paid ↑'}</div>`;
  ks.forEach(k => { const r = rows.find(x => x.rank === k); if (!r) return; if (last && last <= paidN && k > paidN) out += cut(); if (k - last > 1) out += '<div class="gpl-gap">⋮</div>';
    out += `<div class="gpl-r ${r.me ? 'me' : ''} ${k <= paidN ? 'paid' : ''}"><span class="gpl-n">${k}</span>${r.img ? `<span class="gpl-av" style="background-image:url('${r.img}')"></span>` : ''}<b>${r.me ? 'You' : esc(r.nm)}</b>${r.prize ? `<span class="gpl-pz">${r.prize}</span>` : ''}<em>${r.val}</em></div>`;
    last = k; });
  if (last <= paidN && paidN < total) out += cut();
  if (last < total) out += `<div class="gpl-gap">+ ${total - last} more</div>`;
  return `<div class="gpl">${out}</div>`; }
function gsResultSheet(o) { // { ic, nm, sub, head, headSub, won, box:{k,b,s}, mid, go:{t,fn}, link:{t,fn} }
  try { const c = $('#coach'); c.classList.remove('on', 'cr'); c.innerHTML = ''; } catch (e) {}
  openSheet(`<div class="pj gs gr ${o.won ? 'won' : 'lost'}">${o.won ? '<div class="wr-cf" aria-hidden="true">' + [...Array(14)].map((_, i) => `<i style="left:${(i * 37) % 95}%;animation-delay:${(i * .11).toFixed(2)}s"></i>`).join('') + '</div>' : ''}
    <div class="pj-top"><span class="pj-t">${o.ic} ${o.nm}</span><button class="pj-x" data-shclose aria-label="Close">✕</button></div><p class="gs-what">${o.sub}</p>
    <h2 class="gr-h">${o.head}<small>${o.headSub}</small></h2>
    <div class="pj-pot gr-box ${o.won ? '' : 'neu'}"><small class="gs-pl">${o.box.k}</small><b>${o.box.b}</b><span>${o.box.s}</span></div>
    ${o.mid}<button class="btn block ${o.go.free ? 'gr-free' : 'pj-go'}" id="grGo">${o.go.t}</button><button class="link pj-how" id="grLink">${o.link.t}</button></div>`);
  $('#grGo').onclick = o.go.fn; $('#grLink').onclick = o.link.fn || (() => closeSheet()); }
const grBack = () => ({ t: 'Back to voting', fn: () => { closeSheet(); go('judge'); } });
// Quick Sprint
const _sprDoneP = sprDone;
sprDone = function (id, right, ms) { const r = _sprDoneP.apply(this, arguments); if (window.__qsPractice) return r;
  try { const O = qsOpp(id), st = window.__qsStake || 2, won = right > O.sc || (right === O.sc && ms <= O.ms), pay = qsPay(st)[0], diff = Math.abs(O.sc - right);
    const ring = (v, lab, cls, nm, t, w) => `<figure class="${cls === 'me' ? 'pj-me' : 'pj-them'} ${w ? 'gr-w' : 'gr-l'}"><span class="pj-ph gs-rg"><span class="c3-ring ${cls}" style="--p:${v}"><b>${lab}</b></span>${w ? '<i class="gr-tag">🏆 WINNER</i>' : ''}</span><figcaption>${nm}<small>⏱ ${(t / 1000).toFixed(1)}s</small></figcaption></figure>`;
    gsResultSheet({ ic: '🎯', nm: 'Quick Sprint', sub: '10 photo pairs · final result', won,
      head: won ? 'You won!' : `@${esc(O.h)} won`, headSub: diff ? `by ${diff} pick${diff === 1 ? '' : 's'} · ${right}–${O.sc}` : `same score · ${won ? 'you were' : 'they were'} faster`,
      box: won ? { k: 'You won', b: qsM(pay), s: 'Added to your cash' } : { k: 'You lost', b: qsM(st), s: 'Vote more to sharpen your eye' },
      mid: `<div class="pj-vs">${ring(O.sc * 10, O.sc + '/10', 'them', '@' + esc(O.h), O.ms, !won)}<span class="pj-x2">VS</span>${ring(right * 10, right + '/10', 'me', 'You', ms, won)}</div>`,
      go: { t: `Play again · ${qsM(st)}`, fn: () => { closeSheet(); QS_SEL = st; qsSheet(); } }, link: grBack() }); } catch (e) {}
  return r; };
// Showdown
const _paintSdRoomP = paintSdRoom;
paintSdRoom = function (r) { const out = _paintSdRoomP.apply(this, arguments);
  try { if (sdState(r).st !== 'done' || !$('#sdBody')) return out; const order = r.seats.slice().sort((a, b) => b.rate - a.rate), me = order.find(x => x.me), w = order[0], place = order.indexOf(me) + 1, prize = sdPrize();
    const rows = order.map((x, k) => ({ rank: k + 1, nm: '@' + x.h, img: x.src, val: x.rate.toFixed(1) + '%', prize: k === 0 ? money(prize) : '', me: x.me }));
    gsResultSheet({ ic: '⚡', nm: 'Showdown', sub: `${esc(catLabel(r.cat))} · final result`, won: place === 1,
      head: place === 1 ? 'You won!' : `You placed ${ORD(place)}`, headSub: place === 1 ? `top vote share of 5 · ${me.rate.toFixed(1)}%` : `${(w.rate - me.rate).toFixed(1)}% behind the winner`,
      box: place === 1 ? { k: 'You won', b: money(prize), s: 'Added to your cash' } : { k: 'You lost', b: money(SD_FEE).replace('.00', ''), s: `Winner took ${money(prize)}` },
      mid: gsList(rows, 5, 1), go: { t: `Play again · ${money(SD_FEE).replace('.00', '')}`, fn: () => { closeSheet(); sdSheet(); } }, link: grBack() }); } catch (e) {}
  return out; };
// Crowd Championship: your run is done; standings so far (results when the hour ends)
const chN = id => chPlayers(id, id * CH_MS), chW = n => Math.max(1, Math.ceil(n * .2));
const CH_PZ = {};
function chPrize(rank, n) { const W = chW(n); if (rank < 1 || rank > W) return 0;
  if (!CH_PZ[n]) { const pool = chPool(n), raw = [];
    for (let k = 1; k <= W; k++) { let v;
      if (W <= 10) v = k === 1 ? pool * .4 : pool * .6 * (W - k + 1) / ((W - 1) * W / 2);
      else if (k === 1) v = pool * .10; else if (k <= 10) v = pool * .30 * (11 - k) / 45;
      else { const m = W - 10, w = q => 1 + (W - q) / m; let sum = 0; for (let q = 11; q <= W; q++) sum += w(q); v = pool * .60 * w(k) / sum; }
      raw.push(+v.toFixed(2)); }
    CH_PZ[n] = raw.sort((a, b) => b - a); } // always highest first, so a better place never pays less
  return CH_PZ[n][rank - 1]; }
window.chPrize = chPrize;
const CH_NM = ['kai.shoots', 'nina.paws', 'ivy.frames', 'theo.snaps', 'sam_wild', 'luna_loves', 'marco_eats', 'dogdad'];
function chRowsAt(id, rank, score, n) { const rows = [], W = chW(n);
  const add = (k, me) => { if (k < 1 || k > n || rows.some(r => r.rank === k)) return; const sc = me ? score : k === 1 ? CH_N : Math.max(0, Math.min(CH_N, score + (k > rank ? -1 : 0)));
    const pz = chPrize(k, n); rows.push({ rank: k, me, nm: '@' + CH_NM[(k + id) % CH_NM.length], val: sc + '/' + CH_N, prize: pz ? '$' + pz.toFixed(2).replace('.00', '') : '' }); };
  add(rank, 1); [1, rank - 1, rank + 1].forEach(k => add(k)); return { rows: rows.sort((a, b) => a.rank - b.rank), W }; }
function chRows(id, right) { const n = chN(id), est = Math.max(1, Math.round(n * Math.pow(Math.max(0, CH_N - right) / CH_N, 1.4) * .9) + 1), R = chRowsAt(id, Math.min(n, est), right, n);
  return { N: n, me: Math.min(n, est), rows: R.rows, paid: R.W }; }
const _chDoneP = chDone;
chDone = function (id, right, ms) { const r = _chDoneP.apply(this, arguments);
  try { const F = chRows(id, right), at = new Date((id + 1) * CH_MS).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }), inP = F.me <= F.paid, pool = chPool(F.N);
    gsResultSheet({ ic: '👥', nm: 'Crowd Championship', sub: `Your run is in · results at ${at}`, won: false,
      head: `${right}/15 right`, headSub: `You’re ${ORD(F.me)} of ${F.N} so far`,
      box: { k: 'Prize pool', b: `$${pool.toLocaleString()}`, s: inP ? `In the paid places · about ${money(chPrize(F.me, F.N))}` : `Top 20% get paid · 1st wins ${money(chPrize(1, F.N))}` },
      mid: gsList(F.rows, F.N, F.paid), go: { t: 'Keep voting', free: 1, fn: () => { closeSheet(); go('judge'); } }, link: { t: 'How it works', fn: () => toast('Everyone plays the same photo pairs. When the hour ends, 1st wins 10% of the pot, places 2–10 share 30% and the rest of the top 20% share 60%.') } }); } catch (e) {}
  return r; };
// Tournament (knockout of 16): result when it ends
function tourResultSheet() { const T = S.tour; if (!T) return; const R0 = tResult(T), ch = tChamp(T), N = T.n || 16, won = R0.k === 'win', fin = R0.k === 'final';
  const place = won ? 1 : fin ? 2 : Math.pow(2, T_LAST - T.out) + 1, reached = won ? 'Won' : fin ? 'Final' : T_NAMES[T.out];
  const fName = ['ella.travels', 'dogdad', 'nina.paws', 'kai.shoots'][hsh(String(T.at || 1)) % 4];
  const rows = [{ rank: 1, nm: won ? 'You' : '@' + ch.h, me: won, val: 'Won', prize: tAmt(tPay('win', N)) }, { rank: 2, nm: fin ? 'You' : '@' + fName, me: fin, val: 'Final', prize: tAmt(tPay('final', N)) }];
  if (place > 2) rows.push({ rank: place, me: 1, val: reached }, { rank: place - 1, nm: '@' + ['sam_wild', 'ivy.frames', 'theo.snaps'][place % 3], val: reached }, { rank: Math.min(N, place + 1), nm: '@' + ['luna_loves', 'marco_eats', 'catlover22'][place % 3], val: reached });
  gsResultSheet({ ic: '🏆', nm: T.slot && T.slot.gtd >= 100 ? 'Big Cup' : 'Sprint', sub: 'Knockout of ' + N + ' · final result', won: won || fin,
    head: won ? 'You won!' : fin ? 'Finalist!' : `You reached ${reached}`, headSub: won ? `Champion of ${N}` : fin ? `2nd of ${N}` : `Top ${Math.pow(2, T_LAST - T.out + 1)} of ${N}`,
    box: R0.amt ? { k: 'You won', b: tAmt(R0.amt), s: 'Added to your cash' } : { k: 'You lost', b: money(T.fee || 1).replace('.00', ''), s: `Champion @${esc(ch.h)} took ${tAmt(tPay('win', N))}` },
    mid: gsList(rows.sort((a, b) => a.rank - b.rank), N, 2), go: { t: `Play again · $${T.fee || 1}`, fn: () => { tTier(T.fee || 1); S.tour = null; save(); closeSheet(); tourSheet(T.slot && T.slot.gtd >= 100 ? 'big' : 'sprint'); } }, link: grBack() }); }
new MutationObserver(() => { try { const b = $('#sheetBody'), d = b && b.querySelector('.tk-res'); if (d && b.querySelector('#tkAgain') && !d.dataset.gr) { d.dataset.gr = 1; tourResultSheet(); } } catch (e) {} }).observe($('#sheetBody'), { childList: true, subtree: true });

// Crowd Championship: the final result when the hour ends
function chFinal(id) { const e = (S.ch || {})[id]; if (!e || e.rank == null) return; e.grShown = 1; save();
  const n = chN(id), W = chW(n), R = chRowsAt(id, e.rank, e.score, n), won = e.prize > 0;
  gsResultSheet({ ic: '👥', nm: 'Crowd Championship', sub: `${new Date(id * CH_MS).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })} · final result`, won,
    head: won ? 'You won!' : `You placed ${ORD(e.rank)}`, headSub: `${ORD(e.rank)} of ${n} · ${e.score}/${CH_N} right`,
    box: won ? { k: 'You won', b: money(e.prize), s: 'Added to your cash' } : { k: 'You lost', b: '$' + CH_ENTRY, s: `Top ${W} got paid · ${W - e.rank < 0 ? (e.rank - W) + ' places off' : ''}`.replace(/ · $/, '') },
    mid: gsList(R.rows, n, W), go: { t: `Play the next one · $${CH_ENTRY}`, fn: () => { closeSheet(); crowdSheet(); } }, link: grBack() }); }
function chNote(id) { const e = S.ch[id]; let b = $('#sdNote'); if (!b) { b = document.createElement('button'); b.id = 'sdNote'; b.className = 'sd-note'; document.body.appendChild(b); }
  b.innerHTML = `<span class="sd-ni">👥</span><span><b>${e.prize ? `You won ${money(e.prize)}!` : 'Your Crowd Championship results'}</b><small>${ORD(e.rank)} of ${chN(id)} · tap to see the standings</small></span><em>View</em>`;
  b.onclick = () => { b.classList.remove('on'); chFinal(id); }; requestAnimationFrame(() => b.classList.add('on')); setTimeout(() => b.classList.remove('on'), 9000); }
const _celebrateCH = celebrate;
celebrate = function (o) { if (o && /with \d+\/\d+\./.test(o.text || '') && /finished <b>#/.test(o.text || '')) return; return _celebrateCH.apply(this, arguments); };
setInterval(() => { try { Object.entries(S.ch || {}).forEach(([k, e]) => { if (e.paid && !e.grShown && !e.grNote) { e.grNote = 1; save(); if (!$('#sheet').classList.contains('on') && !$('#coach').classList.contains('on')) chFinal(+k); else chNote(+k); } }); } catch (e) {} }, 1500);

'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* placing list */
.gpl{border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;padding:5px;margin-bottom:12px}
.gpl-r{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:11px;font:800 .9rem "Nunito Sans";color:#2D2521}
.gpl-n{min-width:24px;padding:0 5px;box-sizing:border-box;height:24px;flex:none;border-radius:99px;background:#EFE6D6;text-align:center;font:900 .74rem/24px "Nunito Sans"}
.gpl-r.paid .gpl-n{background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600}
.gpl-av{width:32px;height:32px;flex:none;border-radius:8px;background-size:cover;background-position:center}
.gpl-r b{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.gpl-r em{font-style:normal;font:900 .92rem Fraunces,serif;color:#1F3157}
.gpl-pz{font:900 .72rem "Nunito Sans";padding:2px 8px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600}
.gpl-r.me{background:#E6EDF8;box-shadow:inset 0 0 0 2px #2D4E86}.gpl-r.me .gpl-n{background:#2D4E86;color:#fff}
.gpl-cut{margin:2px 10px;padding-top:2px;border-top:1.5px dashed #7FBE91;text-align:center;font:800 .68rem "Nunito Sans";color:#2E6B42}
.gpl-gap{text-align:center;font:800 .8rem "Nunito Sans";color:#8A7E72;padding:1px 0}
html body #sheetBody .gr-free{background:#2D4E86!important;color:#fff!important}
.gr .gs-rg .c3-ring{width:80%}
'''
a = "if (rank <= W) { const sum = W * (W + 1) / 2; prize = Math.max(1, +(pool * (W - rank + 1) / sum).toFixed(2)); }"
assert s.count(a) == 1, 'payout'
s = s.replace(a, 'prize = window.chPrize ? window.chPrize(rank, n) : 0;')
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('places ok')
