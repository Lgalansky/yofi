# Skill preview: Compete › Your photo, laid out like the agreed mock-up.
#  Daily jackpots (photo cards, "From $1" green / "Add photo" white, "Ends in" timer) ·
#  Head-to-head (VS photo card, "Entry $1 · Win $1.70", green "View matchup") ·
#  Challenge a friend (WhatsApp row, green "Invite") · Card challenges panel ("Win Falls back ·
#  Emma won 5–4" with navy "Rematch"; "Steal a card · First to 5 votes wins both cards") ·
#  Tournaments (full-width rows: icon | name, detail, gold "Win $25" | green "Entry $2") · Clubs.
# usage: python3 build-skill/cmp3.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- Compete › Your photo: the agreed layout ----
c2Photo = function () { const L = lgS(), best = fighters()[0], cat = best ? (best.cat || 'any') : 'any';
  const ks = CATS8.filter(k => k !== 'any').sort((a, b) => (!!lgMine(b) - !!lgMine(a)) || (L.jp[b] - L.jp[a]));
  const jp = ks.map(k => { const y = L.you[k] || 0, m = lgMine(k), any = S.photos.some(p => fitsTheme(p, k)), img = m ? m.src : lgPhoto(lgHold(k).h, k);
    return `<button class="c3-jp ${m ? 'on' : 'off'}" data-lgk="${k}"><img src="${img}" alt=""><span class="c3-cat">${LG_IC[k] || '⭐'} ${esc(crownName(k).split(' ')[0])}</span>${y ? `<span class="c3-st">★ ${y}<small>today</small></span>` : ''}
      <span class="c3-pot"><b>$${Math.round(L.jp[k]).toLocaleString()}</b><em class="${m ? '' : 'nav'}">${m ? 'From $1' : any ? 'Needs 70' : 'Add photo'}</em></span></button>`; }).join('');
  const rv = best ? c2NotMine(battleRival(cat).src, cat) : null, win = `$${(2 * (1 - KING_FEE)).toFixed(2)}`;
  const inc = S.fr && (S.fr.ch || []).find(x => x.st === 'yours');
  const h2h = best ? `<div class="c4-card"><button class="c4-pair" data-c2r="h2h"><img src="${rv}" alt=""><i>VS</i><img src="${best.src}" alt=""></button><div class="c4-ft"><span>Entry <b>$1</b> · Win <b class="g">${win}</b></span><button class="c4-go" data-c2r="h2h">View matchup</button></div></div>`
    : `<button class="c3-need" data-c2r="need">✨ Get a photo to ${CFG.QUALIFY} to play 1 v 1 <b>›</b></button>`;
  const incRow = inc ? `<button class="c4-row" data-c2r="inc"><img class="c4-th" src="${inc.theirSrc}" alt=""><span class="c4-tx"><b>@${esc(inc.f)} challenged you</b><small>${stakeTxt(inc.stake)} each · winner takes ${prizeTxt(inc.stake)}</small></span><span class="c4-go">View</span></button>` : '';
  const fr = best ? `<div class="c4-row"><span class="c4-wa">${WA_ICON}</span><span class="c4-tx"><b>Challenge a friend</b><small>Entry $1 · Win <b class="g">${win}</b></small></span><button class="c4-go" data-c2r="friend">Invite</button></div>` : '';
  const held = S.photos.find(p => p.heldBy), rc = typeof rivalCards === 'function' ? rivalCards()[0] : null;
  const cards = (held || rc) ? `<h3 class="c2-h">🃏 Card challenges</h3><div class="c4-panel">${held ? `<div class="c4-crow"><img class="c4-card1" src="${held.src}" alt=""><span class="c4-tx"><b>Win ${esc(alName(held))} back</b><small>${esc(rvName(held.heldBy))} won ${(S.awayNews && S.awayNews.st && S.awayNews.st.score) || '5–4'}</small></span><button class="c4-go nav" data-c2r="steal">Rematch</button></div>` : ''}
    ${rc ? `<button class="c4-crow" data-c2r="stealnew"><span class="c4-fan"><img src="${rc.src}" alt=""><img src="${(rivalCards()[1] || rc).src}" alt=""></span><span class="c4-tx"><b>Steal a card</b><small>First to 5 votes wins both cards</small></span><span class="c4-arr">›</span></button>` : ''}</div>` : '';
  const T = tSlots(), spr = T.find(x => x.gtd < 100);
  const tour = (id, ic, nm, det, win, entry) => `<button class="c4-t" data-c2r="${id}"><span class="c4-ti">${ic}</span><span class="c4-tt"><b>${nm}</b><small>${det}</small><em>Win ${win}</em></span><span class="c4-te">Entry ${entry}</span></button>`;
  return `<h3 class="c2-h">💰 Daily jackpots <small>⏱ Ends in ${dayLeft()}</small></h3><div class="c3-jps">${jp}</div>
    <h3 class="c2-h">⚔️ Head-to-head</h3>${incRow}${h2h}${fr}
    ${cards}
    <h3 class="c2-h">🏆 Tournaments</h3>${spr ? tour('sprint', '⏱', 'Sprint', '16 photos · starts at 16', '$25', '$2') : ''}${tour('sd', '⚡', 'Showdown', '5 photos · one vote', money(sdPrize()), '$' + SD_FEE)}
    <button class="c3-club" data-c2r="clubs">👥 <b>Clubs</b> · weekly prizes with friends <span>›</span></button>`; };
const _c2RenderC4 = c2Render;
c2Render = function () { _c2RenderC4.apply(this, arguments); const b = document.querySelector('#gallery [data-c2r="stealnew"]'); if (b) b.onclick = () => stealSheet({});
  document.querySelectorAll('#gallery [data-c2r="h2h"]').forEach(x => x.onclick = () => h2hSheet()); };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Compete › Your photo, agreed layout */
html body #gallery .c3-pot em{font-size:.86rem;padding:5px 14px}
.c4-card{margin:0 14px 10px;border-radius:18px;overflow:hidden;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(0,0,0,.5)}
.c4-pair{position:relative;display:grid;grid-template-columns:1fr 1fr;width:100%;height:150px;padding:0;border:0;cursor:pointer;background:none}.c4-pair img{width:100%;height:150px;object-fit:cover}
.c4-pair i{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:#2D4E86;color:#fff;font:900 1rem/48px Fraunces,serif;font-style:normal;text-align:center;box-shadow:0 0 0 4px #FFFDF9}
.c4-ft{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 12px}.c4-ft span{font:800 .92rem "Nunito Sans";color:#2D2521}
b.g{color:#1E6B3E}
html body #gallery .c4-go{flex:none;border:0;cursor:pointer;padding:9px 16px;border-radius:12px;background:linear-gradient(180deg,#2E9A5C,#21784A)!important;color:#fff!important;font:900 .92rem "Nunito Sans";box-shadow:0 4px 10px -6px rgba(33,120,74,.8)}
html body #gallery .c4-go.nav{background:#2D4E86!important;box-shadow:0 4px 10px -6px rgba(45,78,134,.8)}
.c4-row{display:flex;align-items:center;gap:12px;width:calc(100% - 28px);margin:0 14px 10px;padding:10px 12px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;text-align:left;font-family:inherit;cursor:pointer;box-sizing:border-box}
.c4-wa{flex:none;width:42px;height:42px;color:#25A35A;display:flex;align-items:center;justify-content:center}.c4-wa svg{width:36px;height:36px}
.c4-th{width:46px;height:46px;border-radius:10px;object-fit:cover;flex:none}
.c4-tx{flex:1;min-width:0}.c4-tx b{display:block;font:900 1.05rem Fraunces,serif;color:#2D2521}.c4-tx small{display:block;font:700 .82rem "Nunito Sans";color:#4E433C}
.c4-panel{margin:0 14px 10px;border-radius:18px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;padding:4px 12px}
.c4-crow{display:flex;align-items:center;gap:12px;width:100%;padding:10px 0;border:0;background:none;text-align:left;font-family:inherit;cursor:pointer}.c4-crow+.c4-crow{border-top:1.5px solid #EFE6D6}
.c4-card1{width:56px;height:70px;flex:none;border-radius:10px;object-fit:cover;box-shadow:0 0 0 3px #E0A82E,0 4px 8px rgba(0,0,0,.25);transform:rotate(-4deg)}
.c4-fan{position:relative;width:64px;height:70px;flex:none}.c4-fan img{position:absolute;width:44px;height:58px;border-radius:8px;object-fit:cover;box-shadow:0 0 0 2.5px #E0A82E,0 4px 8px rgba(0,0,0,.25)}.c4-fan img:first-child{left:0;top:8px;transform:rotate(-10deg)}.c4-fan img:last-child{right:0;top:2px;transform:rotate(8deg)}
.c4-arr{font:900 1.5rem "Nunito Sans";color:#2D4E86}
html body #gallery .c4-t{background:linear-gradient(160deg,#2B4372,#14213D)!important;color:#fff!important}html body #gallery .c4-tt b{color:#fff!important}html body #gallery .c4-tt small{color:#E6EDF8!important}html body #gallery .c4-tt em{color:#F3D27A!important}
.c4-t{display:flex;align-items:center;gap:12px;width:calc(100% - 28px);margin:0 14px 10px;padding:12px 14px;border:0;border-radius:18px;background:linear-gradient(160deg,#2B4372,#14213D);color:#fff;text-align:left;font-family:inherit;cursor:pointer;box-shadow:0 8px 16px -10px rgba(20,33,61,.8);box-sizing:border-box}
.c4-ti{flex:none;width:44px;padding-right:12px;border-right:1.5px solid rgba(255,255,255,.25);font-size:1.7rem;text-align:center}
.c4-tt{flex:1;min-width:0}.c4-tt b{display:block;font:900 1.15rem Fraunces,serif;color:#fff}.c4-tt small{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font:700 .78rem "Nunito Sans";color:#E6EDF8}.c4-tt em{display:block;font:900 1rem "Nunito Sans";font-style:normal;color:#F3D27A;margin-top:2px}
.c4-te{flex:none;padding:9px 12px;border-radius:12px;background:linear-gradient(180deg,#2E9A5C,#21784A);font:900 .9rem "Nunito Sans";white-space:nowrap}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('cmp3 ok')
