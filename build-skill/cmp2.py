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
// rivals and champions never show one of your own photos
function c2NotMine(src, cat, off = 0) { const mine = new Set(S.photos.flatMap(p => [p.src, p.orig])); if (!mine.has(src)) return src;
  const pool = SEED.filter(x => !mine.has(x.src)), same = pool.filter(x => x.cat === BATTLE_POOL[cat]), list = same.length ? same : pool; return list.length ? list[(hsh(cat + dayKey()) + off) % list.length].src : src; }
function c2Photo() { const L = lgS(), F = fighters(), best = F[0], cat = best ? (best.cat || 'any') : 'any';
  const ks = CATS8.filter(k => k !== 'any').sort((a, b) => (!!lgMine(b) - !!lgMine(a)) || (L.jp[b] - L.jp[a]));
  const jp = ks.map(k => { const y = L.you[k] || 0, m = lgMine(k), any = S.photos.some(p => fitsTheme(p, k)), img = m ? m.src : lgPhoto(lgHold(k).h, k);
    return `<button class="c3-jp ${m ? 'on' : 'off'}" data-lgk="${k}"><img src="${img}" alt=""><span class="c3-cat">${LG_IC[k] || '⭐'} ${esc(crownName(k).split(' ')[0])}</span>${y ? `<span class="c3-st">★ ${y}</span>` : ''}
      <span class="c3-pot"><b>$${Math.round(L.jp[k]).toLocaleString()}</b><em class="${m ? '' : 'nav'}">${m ? 'Play $1+' : any ? 'Needs 70' : '+ Add'}</em></span></button>`; }).join('');
  const T = tSlots(), big = T.find(x => x.gtd >= 100), spr = T.find(x => x.gtd < 100);
  const rv = best ? c2NotMine(battleRival(cat).src, cat) : null, K = best ? kingOf(cat) : null, Ks = K ? c2NotMine(K.src, cat, 1) : '';
  const inc = S.fr && (S.fr.ch || []).find(x => x.st === 'yours');
  const one = (inc ? `<button class="c3-t c3-h2h c3-inc" data-c2r="inc"><span class="c3-pair"><img src="${inc.theirSrc}" alt=""><i>VS</i>${(fcPhotos(inc.f, inc.theme)[0] || best) ? `<img src="${(fcPhotos(inc.f, inc.theme)[0] || best).src}" alt="">` : '<img alt="">'}</span><span class="c3-lb"><b>🤝 @${esc(inc.f)} challenged you</b><em>${stakeTxt(inc.stake)} each</em></span></button>` : '')
    + (best ? `<button class="c3-t c3-h2h" data-c2r="h2h"><span class="c3-pair"><img src="${rv}" alt=""><i>VS</i><img src="${best.src}" alt=""></span><span class="c3-lb"><b>Head-to-head</b><em>$1 → $${(2 * (1 - KING_FEE)).toFixed(2)}</em></span></button>`
    : `<button class="c3-need" data-c2r="need">✨ Get a photo to ${CFG.QUALIFY} to play 1 v 1 <b>›</b></button>`);
  const ban = (id, ic, nm, chip, price, cls) => cls ? `<button class="c3-b ${cls}" data-c2r="${id}"><span class="c3-bi">${ic}</span><span class="c3-bt"><b>${nm}</b><i>${chip}</i></span><em>${price}</em></button>` : `<button class="c3-b c3-sm" data-c2r="${id}"><span class="c3-r1"><span class="c3-bi">${ic}</span><b>${nm}</b></span><span class="c3-r2"><i>${chip}</i><em>${price}</em></span></button>`;
  return `<h3 class="c2-h">💰 Daily jackpots <small>⏱ ${dayLeft()}</small></h3><div class="c3-jps">${jp}</div>
    <h3 class="c2-h">⚔️ 1 v 1 now</h3><div class="c3-one">${one}</div>
    <h3 class="c2-h">🏆 Tournaments</h3><div class="c3-bs">${ban('sd', '⚡', 'Showdown', `5 players · win ${money(sdPrize())}`, '$' + SD_FEE, 'wide')}${big ? ban('bigcup', '🏆', `Big Cup<small>Win $${big.gtd}</small>`, `⏱ ${tLeft(big.at)}`, '$1') : ''}${spr ? ban('sprint', '⏱', `Sprint<small>Win $${spr.gtd}</small>`, spr.now ? '⚡ On join' : `⏱ ${tLeft(spr.at)}`, '$1') : ''}</div>
    <button class="c3-club" data-c2r="clubs">👥 <b>Clubs</b> · weekly pots with friends <span>›</span></button>`; }
function c2Eye() { const l = typeof jgLv === 'function' ? jgLv() : null, a = l ? jgAcc() : 0, nx = l && jgNext(), rvA = l ? Math.max(50, a - 1 - hsh(dayKey() + 'qs') % 4) : 0, pr = l ? Math.round(jgProg() * 100) : Math.round(jgN() / JG_MIN * 100);
  const ring = (v, lab, cls) => `<span class="c3-ring ${cls || ''}" style="--p:${v}"><b>${lab}</b></span>`;
  return `<button class="c3-eye" data-c2r="judge">${ring(l ? a : pr, l ? a + '%' : jgN() + '/' + JG_MIN)}<span class="c3-et"><small>Your eye</small><b>${l ? `${l.ic} ${l.n}` : '🎯 New judge'}</b><span class="c3-bar"><i style="width:${pr}%"></i></span><em>${l ? (nx ? `${nx.n} at ${nx.at}%${nx.bonus ? ` · +${nx.bonus} 🟡` : ''}` : 'Top level') : `${JG_MIN - jgN()} votes to your score`}</em></span></button>
    <h3 class="c2-h">⚔️ 1 v 1 now</h3>
    <button class="c3-qs" data-c2r="qs"><span class="c3-qv">${ring(l ? a : 50, l ? a + '%' : '?', 'me')}<i>VS</i>${ring(l ? rvA : 50, l ? rvA + '%' : '?', 'them')}</span><span class="c3-lb"><b>🎯 Quick Sprint</b><em>$2 → $3.20</em></span></button>
    <h3 class="c2-h">🏆 Tournaments</h3><div class="c3-bs"><button class="c3-b wide" data-c2r="crowd"><span class="c3-bi">👥</span><span class="c3-bt"><b>Crowd Championship</b><i>Pick the crowd’s favourites</i></span><em>$${typeof CH_ENTRY !== 'undefined' ? CH_ENTRY : 2}</em></button></div>
    <button class="link c2-vote" data-c2r="vote">Every vote trains your eye · Keep voting</button>`; }
function c2Render() { const g = $('#gallery'); if (!g || GV.tab !== 'battle') return;
  g.innerHTML = `<div class="c2">${c2Bar(C2)}${C2 === 'eye' ? c2Eye() : c2Photo()}</div>`; c2Wire(g);
  g.querySelectorAll('[data-lgk]').forEach(b => b.onclick = () => { const k = b.dataset.lgk; if (!lgMine(k) && !S.photos.some(p => fitsTheme(p, k))) { addCatPhoto(k); return; } goCash(); lgCat(k); });
  const best = fighters()[0], cat = best ? (best.cat || 'any') : 'any';
  const act = { h2h: () => h2hSheet(), inc: () => { const c = S.fr && (S.fr.ch || []).find(x => x.st === 'yours'); if (c) incSheet(c); }, sd: () => sdSheet(), bigcup: () => tourSheet('big'), sprint: () => tourSheet('sprint'), tour: () => cmpOpen('tour'),
    clubs: () => { GV.tab = 'friends'; renderGallery(); $('#gallery').scrollTop = 0; }, need: () => { TU_GAL = true; go('studio'); renderStudio(); },
    judge: () => judgeCard(), qs: () => qsSheet(), crowd: () => crowdSheet(), vote: () => go('judge') };
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
CSS += '''
html body #gallery .c3-b,html body #gallery .c3-eye{background:linear-gradient(160deg,#2B4372,#14213D)!important;color:#fff!important;border:0!important}
html body #gallery .c3-b *,html body #gallery .c3-eye .c3-et b{color:#fff}html body #gallery .c3-bt i{color:#2D2521!important}html body #gallery .c3-et em{color:#E6EDF8!important}html body #gallery .c3-et small{color:#C9D6EE!important}
html body #gallery .c3-b{display:flex!important;width:auto!important;padding:12px!important;min-width:0}
html body #gallery .c3-b em{flex:none}
html body #gallery .c3-t .c3-lb{flex-wrap:wrap}
html body #gallery .c3-t:not(.c3-h2h) .c3-lb{flex-direction:column;align-items:flex-start;gap:5px}
html body #gallery .c3-t:not(.c3-h2h) .c3-lb b{font-size:.98rem}
html body #gallery .c3-b.c3-sm{flex-direction:column;align-items:stretch;gap:8px;padding:11px 12px!important}.c3-sm .c3-r1{display:flex;align-items:center;gap:8px}.c3-sm .c3-r1 .c3-bi{font-size:1.5rem}.c3-sm .c3-r1 b{font:900 1.1rem Fraunces,serif}.c3-sm .c3-r1 b small{display:block;font:800 .74rem "Nunito Sans";color:#F3D27A!important;margin-top:1px}.c3-sm .c3-r2{display:flex;align-items:center;justify-content:space-between}html body #gallery .c3-sm .c3-r2 i{font:800 .74rem "Nunito Sans";font-style:normal;color:#2D2521!important;background:#FFF3D6;padding:2px 8px;border-radius:99px}.c3-sm .c3-r2 em{font-style:normal;font:900 .85rem "Nunito Sans";padding:5px 9px;border-radius:10px;background:linear-gradient(180deg,#2E9A5C,#21784A)}

/* look and feel: pictures first */
.c3-jps{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding:2px 14px 8px;scrollbar-width:none}.c3-jps::-webkit-scrollbar{display:none}
.c3-jp{position:relative;flex:none;width:142px;height:190px;border:0;padding:0;border-radius:18px;overflow:hidden;scroll-snap-align:start;cursor:pointer;background:#2D2521;box-shadow:0 8px 16px -10px rgba(0,0,0,.6)}
.c3-jp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.c3-jp::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.25),transparent 35%,transparent 45%,rgba(10,30,18,.88))}
.c3-jp.on{box-shadow:0 0 0 3px #2E9A5C,0 8px 16px -10px rgba(0,0,0,.6)}.c3-jp.off img{filter:grayscale(.5) brightness(.85)}
.c3-cat{position:absolute;left:8px;top:8px;z-index:1;font:800 .76rem "Nunito Sans";color:#2D2521;background:rgba(255,253,249,.92);padding:3px 8px;border-radius:99px}
.c3-st{position:absolute;right:8px;top:8px;z-index:1;font:900 .8rem "Nunito Sans";color:#3A2600;background:linear-gradient(180deg,#F3D27A,#E0A82E);padding:3px 8px;border-radius:99px}
.c3-pot{position:absolute;left:8px;right:8px;bottom:8px;z-index:1;text-align:left}.c3-pot b{display:block;font:900 1.55rem/1 Fraunces,serif;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.5)}
.c3-pot em{display:inline-block;margin-top:6px;font:900 .78rem "Nunito Sans";font-style:normal;color:#fff;padding:4px 10px;border-radius:99px;background:linear-gradient(180deg,#2E9A5C,#21784A)}.c3-pot em.nav{background:rgba(255,253,249,.92);color:#2D2521}
.c3-one{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 14px}
.c3-t{position:relative;border:0;padding:0;border-radius:18px;overflow:hidden;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(0,0,0,.5);cursor:pointer;text-align:left;font-family:inherit}
.c3-h2h{grid-column:1/-1}
.c3-pair{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;height:120px}.c3-pair img{width:100%;height:120px;object-fit:cover}.c3-pair i{position:relative;z-index:1;width:40px;height:40px;margin:0 -20px;border-radius:50%;background:#2D4E86;color:#fff;font:900 .9rem/40px Fraunces,serif;font-style:normal;text-align:center;box-shadow:0 0 0 3px #FFFDF9}
.c3-im{position:relative;display:block;height:96px}.c3-im img{width:100%;height:100%;object-fit:cover}.c3-md{position:absolute;left:6px;top:6px;font-style:normal;font-size:1.3rem}
.c3-fr{display:flex;align-items:center;justify-content:center;background:linear-gradient(160deg,#EEF3FB,#DCE6F6)}.c3-fr span{font-size:2.6rem}
.c3-lb{display:flex;align-items:center;justify-content:space-between;gap:6px;padding:8px 10px}.c3-lb b{font:900 1rem Fraunces,serif;color:#2D2521}.c3-lb em{font-style:normal;font:900 .8rem "Nunito Sans";color:#fff;padding:5px 9px;border-radius:10px;background:linear-gradient(180deg,#2E9A5C,#21784A);white-space:nowrap}
.c3-need{display:block;width:calc(100% - 28px);margin:0 14px;padding:14px;border:0;border-radius:16px;background:#FBEFD2;font:800 .95rem "Nunito Sans";color:#2D2521;cursor:pointer}
.c3-bs{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 14px}
.c3-b{display:flex;align-items:center;gap:10px;border:0;padding:12px;border-radius:18px;background:linear-gradient(160deg,#2B4372,#14213D);color:#fff;cursor:pointer;text-align:left;font-family:inherit;box-shadow:0 8px 16px -10px rgba(20,33,61,.8)}
.c3-b.wide{grid-column:1/-1}.c3-bi{font-size:1.9rem;filter:drop-shadow(0 2px 4px rgba(0,0,0,.4))}.c3-bt{flex:1;min-width:0}.c3-bt b{display:block;font:900 1.05rem Fraunces,serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.c3-bt i{display:inline-block;margin-top:3px;font:800 .72rem "Nunito Sans";font-style:normal;color:#2D2521;background:#FFF3D6;padding:1px 7px;border-radius:99px}
.c3-b em{font-style:normal;font:900 .85rem "Nunito Sans";padding:6px 9px;border-radius:10px;background:linear-gradient(180deg,#2E9A5C,#21784A)}
.c3-club{display:flex;align-items:center;gap:6px;width:calc(100% - 28px);margin:12px 14px 0;padding:12px 14px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;font:600 .9rem "Nunito Sans";color:#4E433C;cursor:pointer}.c3-club b{color:#2D2521}.c3-club span{margin-left:auto;font:900 1.3rem "Nunito Sans";color:#2D4E86}
.c3-ring{flex:none;width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:conic-gradient(#E0A82E calc(var(--p)*1%),rgba(255,255,255,.25) 0)}.c3-ring b{width:66px;height:66px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#1F3157;color:#fff;font:900 1.25rem Fraunces,serif}
.c3-eye{display:flex;align-items:center;gap:14px;width:calc(100% - 28px);margin:4px 14px 0;padding:14px;border:0;border-radius:20px;background:linear-gradient(160deg,#2B4372,#14213D);color:#fff;cursor:pointer;text-align:left;font-family:inherit;box-shadow:0 10px 20px -12px rgba(20,33,61,.9)}
.c3-et{flex:1;min-width:0}.c3-et small{font:800 .7rem "Nunito Sans";letter-spacing:.08em;text-transform:uppercase;color:#C9D6EE}.c3-et b{display:block;font:900 1.3rem Fraunces,serif}.c3-et em{display:block;font-style:normal;font:700 .78rem "Nunito Sans";color:#E6EDF8}
.c3-bar{display:block;height:7px;border-radius:9px;background:rgba(255,255,255,.18);margin:6px 0 5px;overflow:hidden}.c3-bar i{display:block;height:100%;background:linear-gradient(90deg,#E0A82E,#F3D27A)}
.c3-qs{display:block;width:calc(100% - 28px);margin:0 14px;padding:0;border:0;border-radius:18px;overflow:hidden;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(0,0,0,.5);cursor:pointer;font-family:inherit}
.c3-qv{display:flex;align-items:center;justify-content:center;gap:14px;padding:16px;background:linear-gradient(160deg,#EEF3FB,#DCE6F6)}.c3-qv i{font:900 1.1rem Fraunces,serif;font-style:normal;color:#2D4E86}
.c3-ring.me{background:conic-gradient(#E0A82E calc(var(--p)*1%),#C9D6EE 0)}.c3-ring.them{background:conic-gradient(#9E2F2A calc(var(--p)*1%),#E7DCC7 0)}.c3-ring.them b{background:#5A1A22}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('cmp2 ok')
