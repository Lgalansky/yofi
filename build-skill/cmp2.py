# Skill preview: Compete holds every cash game, in two tabs by what competes.
#  📷 Your photo: Daily jackpots (a pot card per category) · 1 v 1 now (Head-to-head, Beat the
#     champion, Challenge a friend) · Tournaments (5-player Showdown, Sprint, Big Cup) · Clubs
#  🎯 Your eye (shows your judge score): your judge card · Quick Sprint · Crowd Championship
# Every row has a green price button. Coin Cup is gone from Compete (coin games live in the coin
# sheet). The scheduled-tournament list and Clubs keep the same two tabs on top.
# usage: python3 build-skill/cmp2.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- Compete: Your photo | Your eye ----
let C2 = S.cmpTab === 'eye' ? 'eye' : 'photo';
const c2Bar = t => `<div class="cmp-bar c2-bar" role="tablist" aria-label="Compete"><button role="tab" data-c2="photo" aria-selected="${t === 'photo'}">📷 Your photo</button><button role="tab" data-c2="eye" aria-selected="${t === 'eye'}">🎯 Your eye${typeof jgLv === 'function' && jgLv() ? ` <i class="c2-pc">${jgAcc()}%</i>` : ''}</button></div>`;
function c2Wire(el) { el.querySelectorAll('[data-c2]').forEach(b => b.onclick = () => { C2 = b.dataset.c2; S.cmpTab = C2; save(); try { if ($('#flow').classList.contains('on')) closeFlow(); } catch (e) {} GV.tab = 'battle'; go('gallery'); renderGallery(); $('#gallery').scrollTop = 0; }); }
const c2Row = (id, ic, t, d, price) => `<button class="c2-r" data-c2r="${id}"><span class="c2-ic">${ic}</span><span class="c2-tx"><b>${t}</b><small>${d}</small></span><span class="c2-go">${price}</span></button>`;
function c2Photo() { const L = lgS(), F = fighters(), best = F[0], cat = best ? (best.cat || 'any') : 'any';
  const ks = CATS8.filter(k => k !== 'any').sort((a, b) => (!!lgMine(b) - !!lgMine(a)) || (L.jp[b] - L.jp[a]));
  const jp = ks.map(k => { const y = L.you[k] || 0, has = !!lgMine(k), any = S.photos.some(p => fitsTheme(p, k));
    return `<button class="c2-jp ${has ? 'on' : ''}" data-lgk="${k}"><small>${LG_IC[k] || '⭐'} ${esc(crownName(k))}</small><b>$${Math.round(L.jp[k]).toLocaleString()}</b><i>${has ? (y ? `You ${y} ⭐ · ${money(lgShare(k))}` : 'Play from $1') : any ? 'Photo needs 70' : 'Add a photo'}</i></button>`; }).join('');
  const T = tSlots(), big = T.find(x => x.gtd >= 100), spr = T.find(x => x.gtd < 100);
  const one = best ? c2Row('h2h', '⚔️', 'Head-to-head', `${esc(alName(best))} vs a rival · $1 wins $${(2 * (1 - KING_FEE)).toFixed(2)}`, '$1')
      + c2Row('king', '🏅', `Beat the ${esc(catLabel(cat))} champion`, `Bounty pot ${money(kingOf(cat).bounty)}`, '$1')
      + c2Row('friend', '🤝', 'Challenge a friend', `Winner takes ${money(fcPrize({ cur: 'cash', amt: 1 }))}`, '$1')
    : `<button class="c2-r c2-need" data-c2r="need"><span class="c2-ic">✨</span><span class="c2-tx"><b>Get a photo to ${CFG.QUALIFY} to play 1 v 1</b><small>Touch it up in Gallery</small></span><span class="c2-go nav">Go</span></button>`;
  return `<h3 class="c2-h">Daily jackpots <small>pay in ${dayLeft()}</small></h3><div class="c2-jps">${jp}</div>
    <h3 class="c2-h">1 v 1 now</h3>${one}
    <h3 class="c2-h">Tournaments</h3>${c2Row('sd', '⚡', '5-player Showdown', `Winner takes ${money(sdPrize())}`, '$' + SD_FEE)}${big ? c2Row('tour', '🏆', 'Big Cup', `Starts in ${tLeft(big.at)} · $${big.gtd} prize pool`, '$1') : ''}${spr ? c2Row('tour', '⏱', 'Sprint', `Starts in ${tLeft(spr.at)} · $${spr.gtd} prize pool`, '$1') : ''}
    <h3 class="c2-h">With friends</h3>${c2Row('clubs', '👥', 'Clubs', 'Weekly pots with your friends', 'Open')}`; }
function c2Eye() { const l = typeof jgLv === 'function' ? jgLv() : null, a = l ? jgAcc() : 0, nx = l && jgNext();
  return `<button class="c2-judge" data-c2r="judge"><span class="c2-jb">${l ? a + '%' : jgN() + '/' + JG_MIN}</span><span class="c2-tx"><b>${l ? `${l.ic} ${l.n}` : '🎯 Judge score'}</b><small>${l ? (nx ? `${nx.n} at ${nx.at}%${nx.bonus ? ` · +${nx.bonus} 🟡 a correct vote` : ''}` : 'Top level') : `Vote ${JG_MIN - jgN()} more to get your score`}</small></span><span class="c2-arr">›</span></button>
    <p class="c2-why">Your eye = how often you pick the photo most voters choose. Play it for cash:</p>
    <h3 class="c2-h">1 v 1 now</h3>${c2Row('qs', '🎯', 'Quick Sprint', `${l ? `Your ${a}% eye vs a rival · ` : ''}10 pairs · $2 wins $3.20`, '$2')}
    <h3 class="c2-h">Tournaments</h3>${c2Row('crowd', '👥', 'Crowd Championship', 'Pick the crowd’s favourites · top scores share the pot', '$' + (typeof CH_ENTRY !== 'undefined' ? CH_ENTRY : 2))}
    <button class="link c2-vote" data-c2r="vote">Every vote trains your eye · Keep voting</button>`; }
function c2Render() { const g = $('#gallery'); if (!g || GV.tab !== 'battle') return;
  g.innerHTML = `<div class="c2">${c2Bar(C2)}${C2 === 'eye' ? c2Eye() : c2Photo()}</div>`; c2Wire(g);
  g.querySelectorAll('[data-lgk]').forEach(b => b.onclick = () => { const k = b.dataset.lgk; if (!lgMine(k) && !S.photos.some(p => fitsTheme(p, k))) { addCatPhoto(k); return; } goCash(); lgCat(k); });
  const best = fighters()[0], cat = best ? (best.cat || 'any') : 'any';
  const act = { h2h: () => openCashBattle(1, null, best), king: () => openKing(cat), friend: () => fcNew(), sd: () => openShowdown(), tour: () => cmpOpen('tour'),
    clubs: () => { GV.tab = 'friends'; renderGallery(); $('#gallery').scrollTop = 0; }, need: () => { TU_GAL = true; go('studio'); renderStudio(); },
    judge: () => judgeCard(), qs: () => { window.__qsReal = 1; sprEnter(); }, crowd: () => chBuy(), vote: () => go('judge') };
  g.querySelectorAll('[data-c2r]').forEach(b => b.onclick = () => { const f = act[b.dataset.c2r]; if (f) f(); }); }
const _renderGalleryC2 = renderGallery;
renderGallery = function () { const r = _renderGalleryC2.apply(this, arguments);
  try { if (GV.tab === 'battle') c2Render(); else if (GV.tab === 'friends') { const g = $('#gallery'); g.querySelectorAll('.cmp-bar').forEach(e => e.remove()); g.insertAdjacentHTML('afterbegin', c2Bar('photo')); c2Wire(g); } } catch (e) {}
  return r; };
// the tournament list (opened from Big Cup / Sprint) keeps the same two tabs; Coin Cup and Crowd Championship are not listed there
cmpPaint = function () { const fl = $('#flow'), fb = $('#flowBody');
  if (CMP_TAB === 'tour' && fl.classList.contains('on') && fb && !fb.querySelector('.c2-bar')) { fb.querySelectorAll('.cmp-bar, .cmp-h').forEach(e => e.remove()); fb.insertAdjacentHTML('afterbegin', c2Bar('photo')); c2Wire(fb); $('#segGallery').setAttribute('aria-pressed', 'true'); $('#segCompete').setAttribute('aria-pressed', 'false'); }
  if (fb) fb.querySelectorAll('.cmp-tc').forEach(c => { const n = (c.querySelector('.cmp-tt b') || {}).textContent || ''; if (/Coin Cup|Crowd Championship/.test(n)) c.style.display = 'none'; }); };
new MutationObserver(() => { try { if (CMP_TAB === 'tour') cmpPaint(); } catch (e) {} }).observe($('#flowBody'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Compete: Your photo | Your eye */
.c2{padding:0 0 24px}
.c2-pc{font-style:normal;font:900 .72rem "Nunito Sans";padding:1px 6px;border-radius:99px;background:#E6EDF8;color:#2D4E86;margin-left:3px}
.cmp-bar button[aria-selected="true"] .c2-pc{background:rgba(255,255,255,.22);color:#fff}
html body .c2 .c2-h{display:flex;justify-content:space-between;align-items:baseline;margin:16px 16px 8px!important;font:900 1.15rem Fraunces,serif;color:#7A1F27}.c2-h small{font:700 .78rem "Nunito Sans";color:#4E433C}
.c2-jps{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 14px}
.c2-jp{border:0;cursor:pointer;text-align:left;padding:10px 12px;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;font-family:inherit}
.c2-jp.on{box-shadow:inset 0 0 0 2px #2D4E86,0 6px 14px -10px rgba(45,78,134,.6)}
.c2-jp small{display:block;font:800 .8rem "Nunito Sans";color:#2D2521;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.c2-jp b{display:block;font:900 1.45rem/1.1 Fraunces,serif;color:#1E6B3E;margin:2px 0}.c2-jp i{display:block;font-style:normal;font:800 .76rem "Nunito Sans";color:#2D4E86}
.c2-jp:not(.on) i{color:#8A7E72}
.c2-r{display:flex;align-items:center;gap:10px;width:calc(100% - 28px);margin:0 14px 8px;padding:10px 12px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;cursor:pointer;text-align:left;font-family:inherit}
.c2-ic{flex:none;width:42px;height:42px;border-radius:12px;background:#EFE6D6;display:flex;align-items:center;justify-content:center;font-size:1.35rem}
.c2-tx{flex:1;min-width:0}.c2-tx b{display:block;font:800 .98rem "Nunito Sans";color:#2D2521}.c2-tx small{display:block;font:600 .8rem "Nunito Sans";color:#4E433C;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.c2-go{flex:none;padding:8px 13px;border-radius:12px;background:linear-gradient(180deg,#2E9A5C,#21784A);color:#fff;font:900 .9rem "Nunito Sans";box-shadow:0 4px 10px -6px rgba(33,120,74,.8)}
.c2-go.nav,.c2-r[data-c2r="clubs"] .c2-go{background:#2D4E86;box-shadow:none}
.c2-judge{display:flex;align-items:center;gap:12px;width:calc(100% - 28px);margin:4px 14px 6px;padding:12px 14px;border:0;border-radius:18px;background:linear-gradient(180deg,#EEF3FB,#DCE6F6);box-shadow:inset 0 0 0 1.5px #9FB6DD;cursor:pointer;text-align:left;font-family:inherit}
.c2-jb{flex:none;min-width:64px;height:64px;padding:0 6px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#1F3157;color:#fff;font:900 1.25rem Fraunces,serif;box-shadow:0 0 0 4px rgba(224,168,46,.5)}
.c2-judge .c2-tx b{font:900 1.15rem Fraunces,serif;color:#1F3157}.c2-arr{font:900 1.5rem "Nunito Sans";color:#2D4E86}
.c2-why{margin:6px 18px 0;font-size:.86rem;color:#4E433C}
.c2-vote{display:block;margin:12px auto 0;font:800 .9rem "Nunito Sans"}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('cmp2 ok')
