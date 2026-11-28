# Skill preview: a "Live games" row under the vote (option B, below the fold line of the photos).
#  - The vote stays on top; the row replaces the single green card under the photos.
#  - Tiles are short and fixed so every word shows in full (no "…", no wrapping): a chip on the
#    photo says what it is, one big line says what you can win, one small line gives the detail,
#    and the button shows the entry (green = cash, navy = free).
#  - What just happened leads, in gold: a friend's challenge, a stolen card, or a jackpot where
#    your photo won stars today, 5+ right votes in a row (Quick Sprint), or a Crowd Championship
#    starting within 15 minutes. Then Jackpot, Head-to-head, Challenge a friend, Sprint, Steal.
#  - "See all ›" opens Compete.
# usage: python3 build-skill/livegames.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- Live games row under the vote ----
function lgxTiles() { const L = lgS(), best = fighters()[0], cat = best ? (best.cat || 'any') : 'any', out = [], win = `$${(2 * (1 - KING_FEE)).toFixed(2)}`;
  const short = k => crownName(k).split(' ')[0];
  const T = (o) => out.push(o);
  const inc = S.fr && (S.fr.ch || []).find(x => x.st === 'yours');
  if (inc) T({ hot: 1, img: inc.theirSrc, chip: '🤝 Challenge', big: `Win ${prizeTxt(inc.stake)}`, sm: `From @${String(inc.f).slice(0, 11)}`, go: 'View', gs: `${stakeTxt(inc.stake)} each`, fn: () => incSheet(inc) });
  const held = S.photos.find(p => p.heldBy);
  if (held) T({ hot: 1, img: held.src, chip: '🃏 Stolen', big: 'Win it back', sm: 'Free try', go: 'Play', gs: `${stlLeft()} of 3 tries left`, free: 1, fn: () => stealSheet({ back: held.id }) });
  // your eye: 5+ right in a row -> Quick Sprint for cash
  const h = jgHist(); let run = 0; for (let i = h.length - 1; i >= 0 && h[i]; i--) run++;
  if (run >= 5 && S.lgxStrkAt !== (S.votes || 0) - run) T({ hot: 1, icon: '<span class="lgx-em">🔥</span>', chip: `🔥 ${run} right`, big: `Win ${qsM(qsPay(2)[0])}`, sm: 'Quick Sprint', gs: 'Your eye vs a rival', go: 'Play · $2',
    fn: () => { S.lgxStrkAt = (S.votes || 0) - run; save(); QS_SEL = 2; qsSheet(); } });
  // Crowd Championship starting soon
  const nx = chId() + 1, mins = Math.ceil((nx * CH_MS - Date.now()) / 6e4);
  if (mins <= 15 && !(S.ch && S.ch[nx])) { const pool = chPool(chPlayers(nx, nx * CH_MS));
    T({ hot: 1, icon: '<span class="lgx-em">👥</span>', chip: `⏱ ${mins} min`, big: `1st wins $${Math.round(pool * .1).toLocaleString()}`, sm: 'Crowd Championship', gs: 'Top 20% paid', go: `Join · $${CH_ENTRY}`, fn: () => crowdSheet() }); }
  const ks = CATS8.filter(k => k !== 'any').sort((a, b) => ((L.you[b] || 0) - (L.you[a] || 0)) || (!!lgMine(b) - !!lgMine(a)) || (L.jp[b] - L.jp[a]));
  const k = ks[0];
  if (k) { const m = lgMine(k), st = L.you[k] || 0;
    T({ hot: st ? 1 : 0, img: m ? m.src : lgPhoto(lgHold(k).h, k), chip: st ? `★ ${st} today` : `💰 ${short(k)}`, big: `$${Math.round(L.jp[k]).toLocaleString()} pot`, sm: `Ends ${dayLeft()}`, go: 'Play · from $1', gs: 'Win stars tonight',
      fn: () => { if (!lgMine(k) && !S.photos.some(p => fitsTheme(p, k))) { addCatPhoto(k); return; } goCash(); lgCat(k); } }); }
  if (best) T({ pair: [c2NotMine(battleRival(cat).src, cat), best.src], chip: '⚔️ 1 v 1', big: `Win ${win}`, sm: 'Voters pick', go: 'Play · $1', gs: 'Result in minutes', fn: () => h2hSheet() });
  if (best && !inc) T({ wa: 1, chip: '🤝 Friend', big: `Win ${win}`, sm: 'Invite a friend', go: 'Invite · $1', gs: 'Send on WhatsApp', fn: () => { if (S.frSt === 'gem' || S.frSt == null) S.frSt = 1; save(); frDare(); } });
  const spr = tSlots().find(x => x.gtd < 100);
  if (spr) T({ icon: KO_PYR2, chip: '⏱ Sprint', big: 'Win $25', sm: `${Math.min(16, tCount())}/16 joined`, go: 'Join · $2', gs: 'Starts at 16', fn: () => tourSheet('sprint') });
  const rc = typeof rivalCards === 'function' ? rivalCards()[0] : null;
  if (rc && !held) T({ img: rc.src, chip: '🃏 Steal', big: 'Win a card', sm: 'First to 5 votes', go: 'Play · free', gs: `${stlLeft()} of 3 tries left`, free: 1, fn: () => stealSheet({}) });
  return out; }
function lgxPaint() { const j = $('#judge'); if (!j) return; const foot = j.querySelector('.jfoot') || j.querySelector('#jcard'); if (!foot) return;
  let w = j.querySelector('.lgx-wrap'); const tiles = lgxTiles(), sig = tiles.map(t => t.chip + t.big + t.sm).join('|');
  if (w && w.nextElementSibling === foot && w.dataset.sig === sig) return;
  if (!tiles.length) { if (w) w.remove(); return; }
  const ph = t => t.pair ? `<img src="${t.pair[0]}" alt=""><img src="${t.pair[1]}" alt=""><span class="lgx-vs">VS</span>` : t.icon ? `<span class="lgx-ic">${t.icon}</span>` : t.wa ? `<span class="lgx-ic lgx-wa">${WA_ICON}</span>` : `<img src="${t.img}" alt="">`;
  const html = `<div class="lgx-h"><span><i class="lgx-dot"></i>Live games</span><button class="lgx-all">See all ›</button></div><div class="lgx-row">${tiles.map((t, i) => `<button class="lgx ${t.hot ? 'hot' : ''} ${t.pair ? 'two' : ''}" data-lgx="${i}"><span class="lgx-ph">${ph(t)}<i class="lgx-chip">${t.chip}</i></span><b>${t.big}</b><small>${esc(t.sm)}</small>${t.gs ? `<small class="lgx-d">${esc(t.gs)}</small>` : ''}<em class="${t.free ? 'nav' : ''}">${t.go}</em></button>`).join('')}</div>`;
  if (!w) { w = document.createElement('div'); w.className = 'lgx-wrap'; } w.innerHTML = html; w.dataset.sig = sig; foot.before(w);
  w.querySelectorAll('[data-lgx]').forEach(b => b.onclick = () => tiles[+b.dataset.lgx].fn());
  w.querySelector('.lgx-all').onclick = () => { GV.tab = 'battle'; go('gallery'); renderGallery(); }; }
new MutationObserver(() => { try { const j = $('#judge'), w = j && j.querySelector('.lgx-wrap'), f = j && (j.querySelector('.jfoot') || j.querySelector('#jcard')); if (!w || w.nextElementSibling !== f) lgxPaint(); } catch (e) {} }).observe($('#judge'), { childList: true });
setInterval(() => { try { if ($('#panes').dataset.at === 'judge') lgxPaint(); } catch (e) {} }, 2000);
setTimeout(() => { try { lgxPaint(); } catch (e) {} }, 400);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Live games row under the vote */
html body #judge > .vc{display:none!important}
.lgx-wrap{margin:8px 0 6px}
.lgx-h{display:flex;justify-content:space-between;align-items:center;margin:0 16px 4px}
.lgx-h span{display:flex;align-items:center;gap:6px;font:900 .8rem "Nunito Sans";letter-spacing:.06em;text-transform:uppercase;color:#1E6B3E}
.lgx-dot{width:8px;height:8px;border-radius:50%;background:#2E9A5C;box-shadow:0 0 0 3px rgba(46,154,92,.25)}
.lgx-all{border:0;background:none;padding:0;font:800 .85rem "Nunito Sans";color:#2D4E86;cursor:pointer}
.lgx-row{display:flex;gap:10px;overflow-x:auto;padding:2px 16px 8px;scrollbar-width:none;scroll-snap-type:x mandatory}.lgx-row::-webkit-scrollbar{display:none}
.lgx{flex:none;width:142px;scroll-snap-align:start;display:flex;flex-direction:column;align-items:stretch;gap:0;padding:7px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;text-align:left;font-family:inherit;cursor:pointer;box-sizing:border-box}
.lgx.hot{background:#FFF3D6;box-shadow:inset 0 0 0 2px #E0A82E}
.lgx-ph{position:relative;display:flex;height:96px;border-radius:10px;overflow:hidden;margin-bottom:6px;background:linear-gradient(160deg,#2B4372,#14213D);align-items:center;justify-content:center}
.lgx-ph img{width:100%;height:100%;object-fit:cover}.lgx.two .lgx-ph img{width:50%}
.lgx-vs{display:none;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:24px;height:24px;border-radius:50%;background:#2D4E86;color:#fff;font:900 .6rem/24px Fraunces,serif;text-align:center;box-shadow:0 0 0 2px #FFFDF9}
.lgx-ic{display:flex;align-items:center;justify-content:center}.lgx-ic .ko-pyr{width:56px;height:48px}.lgx-wa{background:#fff;width:100%;height:100%;color:#25A35A}.lgx-wa svg{width:48px;height:48px}
.lgx-chip{position:absolute;left:5px;top:5px;padding:2px 7px;border-radius:99px;background:rgba(20,33,61,.85);color:#fff;font:800 .66rem "Nunito Sans";font-style:normal;white-space:nowrap}
.lgx.hot .lgx-chip{background:#E0A82E;color:#3A2600}
.lgx b{font:900 1.02rem/1.2 Fraunces,serif;color:#1E6B3E;white-space:nowrap}
.lgx small{font:700 .74rem/1.3 "Nunito Sans";color:#4E433C;white-space:nowrap}
.lgx em{margin-top:6px;text-align:center;padding:6px 0;border-radius:10px;background:linear-gradient(180deg,#2E9A5C,#21784A);color:#fff;font:900 .82rem "Nunito Sans";font-style:normal}
.lgx em.nav{background:#2D4E86}
.lgx-em{font-size:2.6rem;line-height:1}.lgx.hot .lgx-ph{background:linear-gradient(160deg,#F3D27A,#E0A82E)}
.lgx small.lgx-d{color:#6A5E55;font-weight:600}
html body #judge .lgx-all{color:#2D4E86!important;background:none!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('livegames ok')
