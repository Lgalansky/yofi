# Skill preview: card stealing (like a challenge, but you can lose a card while you're away).
#  - Each gallery photo is a card that earns coins per vote. Rivals (simulated) can steal one
#    while you're away 2h+; you keep the coins it already earned. A stolen card leaves its slot
#    empty (it stops earning and stops counting towards Gold) until you win it back.
#  - Coming back after 2h+: the usual key-moment pop, "While you were away": the coins your cards
#    earned (collected from the jar) and "1 card stolen · Falls · Emma won 5–4", button "Win Falls back".
#  - Steal battles: risk one of your cards vs theirs, first to 5 votes wins both cards (at most 9
#    live votes). No coins or cash at stake, so the button is navy. 3 attempts a day.
#  - Win back a stolen card, or steal a rival's card (Compete › Your photo › Steal a card, and a
#    banner in the gallery room). A stolen card joins your collection and earns for you.
# usage: python3 build-skill/steal.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)

# stolen cards are not entered in cash games; a card held by a rival leaves its slot
rep("const fighters = () => S.photos.filter(p => p.s.total >= CFG.QUALIFY && !p.retired)",
    "const fighters = () => S.photos.filter(p => p.s.total >= CFG.QUALIFY && !p.retired && !p.card && !p.heldBy)")
rep("function galRoom(c) {\n  const ph = S.photos.filter(p => p.cat === c && p.s)",
    "function galRoom(c) {\n  const ph = S.photos.filter(p => p.cat === c && p.s && !p.heldBy)")

JS = r'''
// ---- card stealing ----
const RIVALS = [{ h: 'emma', n: 'Emma' }, { h: 'maya', n: 'Maya' }, { h: 'leo', n: 'Leo' }, { h: 'zara', n: 'Zara' }];
const rvName = h => (RIVALS.find(r => r.h === h) || { n: '@' + h }).n;
const cardRate = sc => GAL.BASE * galMult(sc);
const stlDay = () => { if (!S.stl || S.stl.d !== todayKey()) S.stl = { d: todayKey(), n: 0 }; return S.stl; };
const stlLeft = () => Math.max(0, 3 - stlDay().n);
const myCards = () => GAL.PATH.filter(galOpen).flatMap(c => galRoom(c).ph);
// rival cards you could steal: other players' photos in your open categories
function rivalCards() { const mine = new Set(S.photos.flatMap(p => [p.src, p.orig])), out = [];
  GAL.PATH.filter(galOpen).forEach((c, ci) => { SEED.filter(x => x.cat === BATTLE_POOL[c] && !mine.has(x.src)).slice(0, 2).forEach((x, i) => { const r = RIVALS[(hsh(x.id) + i) % RIVALS.length];
    out.push({ key: x.id, src: x.src, nm: x.title || 'Photo', cat: c, sc: 70 + hsh(x.id) % 18, h: r.h }); }); });
  return out.filter(x => !(S.stlTaken || []).includes(x.key)); }
// a rival steals one of your cards while you're away (2h+), one at a time
function stealAway(force) { if (!S.user) return; const now = Date.now(), last = S.lastSeen || now; S.lastSeen = now; save();
  const away = now - last; if (!force && away < 2 * 36e5) return;
  const held = S.photos.some(p => p.heldBy), cards = myCards(); let st = null;
  if (!held && cards.length >= 1) { const p = cards.slice().sort((a, b) => hsh(a.id + todayKey()) - hsh(b.id + todayKey()))[0], r = RIVALS[hsh(p.id + now) % RIVALS.length];
    if (p.card) { S.photos = S.photos.filter(x => x !== p); } else { p.heldBy = r.h; p.heldAt = now; }
    st = { pid: p.id, nm: alName(p), src: p.src, h: r.h, score: '5–' + (2 + hsh(p.id) % 3), earned: p.gl || 0 }; save(); }
  S.awayNews = { coins: Math.floor(S.vgJar || 0), st, at: now }; save(); }
setInterval(() => { try { if (S.user) { S.lastSeen = Date.now(); save(); } } catch (e) {} }, 20000);
function awayPop() { const N = S.awayNews; if (!N || N.shown || !S.user) return; if ($('#panes').dataset.at !== 'judge' || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on')) return;
  N.shown = 1; save(); const coins = Math.floor(S.vgJar || 0); if (!coins && !N.st) return;
  if (coins) { try { jarCollect(); } catch (e) {} }
  const st = N.st;
  celebrate({ src: st ? st.src : ((myCards()[0] || S.photos[0] || {}).src || ''), score: coins ? '+' + coins : '🃏', title: 'While you were away',
    text: `${coins ? `<b>+${coins} 🟡</b> earned by your cards · added to your wallet` : ''}${coins && st ? '<br><br>' : ''}${st ? `<b>1 card stolen: ${esc(st.nm)}</b><br>${esc(rvName(st.h))} won ${st.score}. You keep the coins it already earned.` : ''}`,
    cta: st ? `Win ${st.nm} back` : 'Back to voting', onCta: () => { if (st) stealSheet({ back: st.pid }); }, later: 'Back to voting' }); }
setInterval(() => { try { awayPop(); } catch (e) {} }, 1500);
setTimeout(() => { try { stealAway(); } catch (e) {} }, 600);
// the steal screen: win back, or steal a rival's card
function stealSheet(o = {}) { const mine = myCards(); if (!mine.length) { toast('Add a photo to your gallery to play for cards'); return; }
  let them, title, back = null;
  if (o.back) { const p = S.photos.find(x => x.id === o.back && x.heldBy); if (!p) { toast('That card is already yours'); return; } back = p; them = { src: p.src, nm: alName(p), sc: p.s.total, h: p.heldBy, cat: p.cat }; title = `Win ${them.nm} back`; }
  else { const list = rivalCards(); them = o.rival || list[0]; if (!them) { toast('No cards to steal right now'); return; } title = `Try to steal ${them.nm}`; }
  const pick = mine.filter(x => x.cat === them.cat).concat(mine.filter(x => x.cat !== them.cat)), mi = Math.min(o.mi || 0, pick.length - 1), me = pick[mi], left = stlLeft();
  gameSheet({ ic: '🃏', nm: title, what: 'First to 5 votes wins both cards', pl: 'Win', prize: back ? `${them.nm} back` : them.nm, chip: `${them.nm} earns ${cardRate(them.sc)} 🟡 per vote`,
    left: gsPh(them.src, them.sc), lcap: `${esc(them.nm)}<small>Held by ${esc(rvName(them.h))}</small>`, right: gsPh(me.src, me.s.total), rcap: `${esc(alName(me))}<small>Your card</small>`,
    fixed: `Risk ${esc(alName(me))}`, fixedSub: `lose and ${esc(rvName(them.h))} takes it · ${left} of 3 left today`,
    go: left ? `Risk ${alName(me)} & challenge` : 'No attempts left today', onGo: () => { if (!stlLeft()) { toast('3 card battles a day · come back tomorrow'); return; } stealBattle(me, them, back); },
    link: pick.length > 1 ? 'Choose another card' : 'Back', onLink: () => pick.length > 1 ? stealSheet({ ...o, rival: o.rival || (back ? null : them), mi: (mi + 1) % pick.length }) : closeSheet() });
  const box = document.querySelector('#sheetBody .gs'); if (!box) return; box.classList.add('stl');
  const others = rivalCards().filter(x => x.key !== them.key).slice(0, 2);
  if (others.length) box.insertAdjacentHTML('beforeend', `<h3 class="stl-h">Steal a card</h3>${others.map(x => `<button class="stl-r" data-stk="${x.key}"><img src="${x.src}" alt=""><span><b>${esc(x.nm)}</b><small>Held by ${esc(rvName(x.h))} · earns ${cardRate(x.sc)} 🟡 a vote</small></span><em>View ›</em></button>`).join('')}`);
  box.querySelectorAll('[data-stk]').forEach(b => b.onclick = () => stealSheet({ rival: rivalCards().find(x => x.key === b.dataset.stk) })); }
// the battle: first to 5 votes
function stealBattle(me, them, back) { const D = stlDay(); D.n++; save();
  const pWin = Math.max(.25, Math.min(.75, .5 + (me.s.total - them.sc) / 40)), won = Math.random() < pWin, seq = []; let a = 0, b = 0;
  while (a < 5 && b < 5) { const mine = Math.random() < (won ? .62 : .38); if (mine) a++; else b++; seq.push(mine); } if ((a === 5) !== won) { [a, b] = [b, a]; for (let i = 0; i < seq.length; i++) seq[i] = !seq[i]; }
  openSheet(`<div class="pj gs stl"><div class="pj-top"><span class="pj-t">🃏 ${back ? `Win ${esc(them.nm)} back` : `Steal ${esc(them.nm)}`}</span></div><p class="gs-what"><span class="lv-live">LIVE</span> First to 5 votes</p>
    <div class="pj-vs"><figure class="pj-them">${gsPh(them.src, them.sc)}<figcaption>${esc(them.nm)}<small>${esc(rvName(them.h))}</small></figcaption></figure><span class="pj-x2">VS</span><figure class="pj-me">${gsPh(me.src, me.s.total)}<figcaption>${esc(alName(me))}<small>You</small></figcaption></figure></div>
    <div class="stl-sc"><b id="stlT">0</b><span>–</span><b id="stlM">0</b></div></div>`);
  let i = 0, x = 0, y = 0; const iv = setInterval(() => { if (!$('#stlM')) { clearInterval(iv); return; } if (seq[i]) y++; else x++; i++; $('#stlM').textContent = y; $('#stlT').textContent = x;
    if (i >= seq.length) { clearInterval(iv); setTimeout(() => stealDone(me, them, back, won, y, x), 700); } }, 650); }
function stealDone(me, them, back, won, mv, tv) { const rn = rvName(them.h);
  if (won) { if (back) { back.heldBy = null; back.heldAt = null; } else { S.photos.push({ id: uid(), src: them.src, orig: them.src, cat: them.cat, nm: them.nm, nmAsk: 1, enh: 0, at: Date.now(), card: { from: them.h }, s: { light: them.sc, comp: them.sc, colour: them.sc, tech: them.sc, total: them.sc } }); S.stlTaken = (S.stlTaken || []).concat(them.key); } }
  else { if (me.card) S.photos = S.photos.filter(p => p !== me); else { me.heldBy = them.h; me.heldAt = Date.now(); } }
  if (S.awayNews && S.awayNews.st && back && won) S.awayNews.st = null; save();
  const fig = (src, nm, sub, w, cls) => `<figure class="${cls} ${w ? 'gr-w' : 'gr-l'}"><span class="pj-ph"><img src="${src}" alt="">${w ? '<i class="gr-tag">🏆 WINNER</i>' : ''}</span><figcaption>${esc(nm)}<small>${sub}</small></figcaption></figure>`;
  gsResultSheet({ ic: '🃏', nm: back ? `Win ${esc(them.nm)} back` : `Steal ${esc(them.nm)}`, sub: 'Final result', won,
    head: won ? (back ? `You won ${esc(them.nm)} back!` : `You stole ${esc(them.nm)}!`) : `${esc(rn)} won`, headSub: `${mv}–${tv}`,
    box: won ? { k: 'Now yours', b: esc(them.nm), s: `It earns you ${cardRate(them.sc)} 🟡 per vote` } : { k: 'You lost', b: esc(alName(me)), s: `${esc(rn)} holds it now · win it back any time` },
    mid: `<div class="pj-vs">${fig(them.src, them.nm, `${tv} votes`, !won, 'pj-them')}<span class="pj-x2">VS</span>${fig(me.src, alName(me), `${mv} votes`, won, 'pj-me')}</div>`,
    go: won ? { t: 'View my collection', free: 1, fn: () => { closeSheet(); S.galCat = them.cat; AL_OPEN = null; TU_GAL = true; save(); go('studio'); renderStudio(); } } : { t: `Win ${alName(me)} back`, free: 1, fn: () => { closeSheet(); setTimeout(() => stealSheet({ back: me.id }), 280); } },
    link: grBack() }); }
// Compete: a Steal a card row; Gallery: a banner when one of your cards is held
const _c2PhotoS = c2Photo;
c2Photo = function () { let h = _c2PhotoS.apply(this, arguments); const held = S.photos.find(p => p.heldBy), rc = rivalCards()[0];
  const row = held ? `<button class="c3-sdr stl-row" data-c2r="steal"><span class="c3-sdi">🃏</span><span class="c3-sdt"><b>Win ${esc(alName(held))} back</b><small>Held by ${esc(rvName(held.heldBy))} · first to 5 votes</small></span><i>${stlLeft()} left</i><em>Play</em></button>`
    : rc ? `<button class="c3-sdr stl-row" data-c2r="steal"><span class="c3-sdi">🃏</span><span class="c3-sdt"><b>Steal a card</b><small>${esc(rc.nm)} · held by ${esc(rvName(rc.h))}</small></span><i>${stlLeft()} left</i><em>Play</em></button>` : '';
  return h.replace('<h3 class="c2-h">🏆 Tournaments</h3>', `<h3 class="c2-h">🃏 Cards</h3>${row}<h3 class="c2-h">🏆 Tournaments</h3>`); };
const _c2RenderS = c2Render;
c2Render = function () { _c2RenderS.apply(this, arguments); const b = document.querySelector('#gallery [data-c2r="steal"]'); if (b) b.onclick = () => { const held = S.photos.find(p => p.heldBy); stealSheet(held ? { back: held.id } : {}); }; };
const _renderGalleriesS = renderGalleries;
renderGalleries = function () { const r = _renderGalleriesS.apply(this, arguments);
  try { const th = document.querySelector('#studio .a2-th'), c = S.galCat, held = S.photos.find(p => p.heldBy && (!c || p.cat === c));
    if (th && held && !document.querySelector('#studio .stl-ban')) { th.insertAdjacentHTML('afterend', `<button class="stl-ban"><img src="${held.src}" alt=""><span><b>${esc(alName(held))} was stolen by ${esc(rvName(held.heldBy))}</b><small>Its slot is empty until you win it back</small></span><em>Win it back ›</em></button>`);
      document.querySelector('#studio .stl-ban').onclick = () => stealSheet({ back: held.id }); }
    document.querySelectorAll('#studio .a2-sl[data-alc]').forEach(b => { const p = S.photos.find(x => x.id === b.dataset.alc); if (p && p.card && !b.querySelector('.stl-tag')) { const ph = b.querySelector('.a2-ph'); if (ph) ph.insertAdjacentHTML('beforeend', `<i class="stl-tag">🃏 Won from ${esc(rvName(p.card.from))}</i>`); } }); } catch (e) {}
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* card stealing */
html body #sheetBody .gs.stl .pj-go,html body #sheetBody .stl .pj-go{background:#2D4E86!important;box-shadow:0 8px 18px -8px rgba(45,78,134,.7)!important}
.gs.stl .sk-row.gs-fix button b{font-size:1.05rem!important;white-space:nowrap}.gs.stl .sk-row.gs-fix button small{text-align:left}
.gs.stl .sk-row.gs-fix button{box-shadow:inset 0 0 0 2px #2D4E86!important;color:#1F3157!important}
.stl-h{margin:16px 2px 8px;font:900 1.1rem Fraunces,serif;color:#7A1F27}
.stl-r,.stl-ban{display:flex;align-items:center;gap:10px;width:100%;padding:8px 10px;margin-bottom:8px;border:0;border-radius:16px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE;text-align:left;cursor:pointer;font-family:inherit}
.stl-r img,.stl-ban img{width:56px;height:56px;flex:none;border-radius:10px;object-fit:cover}.stl-r span,.stl-ban span{flex:1;min-width:0}.stl-r b,.stl-ban b{display:block;font:900 1rem Fraunces,serif;color:#2D2521}.stl-r small,.stl-ban small{font:700 .78rem "Nunito Sans";color:#4E433C}
.stl-r em,.stl-ban em{font-style:normal;font:800 .85rem "Nunito Sans";color:#2D4E86;white-space:nowrap}
.stl-ban{width:calc(100% - 36px);margin:0 18px 12px;background:#FBEFD2;box-shadow:inset 0 0 0 1.5px #E0B860}
.stl-sc{display:flex;justify-content:center;align-items:baseline;gap:14px;margin:6px 0 4px}.stl-sc b{font:900 2.6rem Fraunces,serif;color:#1F3157}.stl-sc span{font:900 1.6rem Fraunces,serif;color:#8A7E72}
.stl-tag{position:absolute;left:6px;top:6px;font:800 .62rem "Nunito Sans";font-style:normal;padding:2px 7px;border-radius:99px;background:#1F3157;color:#fff}
.stl-row em{background:#2D4E86!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('steal ok')
