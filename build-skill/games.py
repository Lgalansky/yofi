# Skill preview: every cash game uses one screen, and the list is cut to 4 games.
# The game screen has the same 5 blocks every time:
#   1. icon + name, and one line saying what it is
#   2. green prize box: what you can win + when
#   3. the match: always a VS picture (rival on the left, you on the right)
#   4. stake chips (each says what it wins), or one locked chip when the stake is fixed
#   5. one big green "Play · $2" button + one small link
# Games: Daily jackpot, Head-to-head (with "Challenge a friend instead"; incoming friend
# challenges use the same screen with Accept / Decline), Quick Sprint, Tournaments (Showdown,
# Big Cup, Sprint, Crowd Championship). Champion is cut: the jackpot ribbon holder plays that role.
# usage: python3 build-skill/games.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# rivals in matches never use your photos, and the rival shown on the game screen is the one you play
rep("function battleRival(cat) {\n  const pool = SEED.filter(x => x.cat === BATTLE_POOL[cat]);",
    "function battleRival(cat) {\n  if (window.__rvNext) { const r = SEED.find(x => x.src === window.__rvNext); window.__rvNext = null; if (r) return r; }\n  const mineS = new Set(S.photos.flatMap(p => [p.src, p.orig])), pool = SEED.filter(x => x.cat === BATTLE_POOL[cat] && !mineS.has(x.src));")

# the jackpot screen follows the same pattern: one line under the name, "Play · $2"
rep("<button class=\"pj-x\" data-shclose aria-label=\"Close\">✕</button></div>\n    <div class=\"pj-pot\"><b id=\"pjPot\">",
    "<button class=\"pj-x\" data-shclose aria-label=\"Close\">✕</button></div><p class=\"gs-what\">Win stars, share tonight’s pot · voters pick</p>\n    <div class=\"pj-pot\"><small class=\"gs-pl\">Jackpot</small><b id=\"pjPot\">")
rep("${iHold ? 'Defend your ribbon' : rematch ? 'Rematch' : 'Challenge'} · ${cash ? (free ? 'Free 🎟️' : '$' + LG_FEE) : LG_COIN + ' 🟡'}",
    "${iHold ? 'Defend' : rematch ? 'Rematch' : 'Play'} · ${cash ? (free ? 'Free 🎟️' : '$' + LG_FEE) : LG_COIN + ' 🟡'}")

JS = r'''
// ---- one game screen for every cash game ----
const gsPh = (src, sc) => `<span class="pj-ph"><img src="${src}" alt="">${sc != null ? `<i class="pj-sc">${sc}</i>` : ''}</span>`;
const gsRing = (v, lab, cls) => `<span class="pj-ph gs-rg"><span class="c3-ring ${cls}" style="--p:${v}"><b>${lab}</b></span></span>`;
const gsTile = (ic, t) => `<span class="pj-ph gs-tl"><span>${ic}</span><b>${t}</b></span>`;
function gameSheet(o) {
  const chips = o.fixed ? `<div class="sk-row gs-fix"><button role="radio" aria-checked="true" disabled><b>${o.fixed}</b><small>${o.fixedSub || ''}</small></button></div>`
    : o.stakes ? `<div class="sk-row" role="radiogroup" aria-label="Entry">${o.stakes.map(x => `<button role="radio" aria-checked="${x.v === o.sel}" data-gst="${x.v}" class="${x.lock ? 'lock' : ''}"><b>$${x.v}</b><small>${x.sub}</small></button>`).join('')}</div>` : '';
  openSheet(`<div class="pj gs">
    <div class="pj-top"><span class="pj-t">${o.ic} ${o.nm}</span><button class="pj-x" data-shclose aria-label="Close">✕</button></div><p class="gs-what">${o.what}</p>
    <div class="pj-pot"><small class="gs-pl">${o.pl}</small><b>${o.prize}</b><span>${o.chip}</span></div>
    <div class="pj-vs"><figure class="pj-them">${o.left}<figcaption>${o.lcap}</figcaption></figure><span class="pj-x2">VS</span><figure class="pj-me">${o.right}<figcaption>${o.rcap}</figcaption></figure></div>
    ${chips}<button class="btn block pj-go" id="gsGo">${o.go}</button>${o.link ? `<button class="link pj-how" id="gsLink">${o.link}</button>` : ''}</div>`);
  document.querySelectorAll('#sheetBody [data-gst]').forEach(b => b.onclick = () => o.onPick(+b.dataset.gst));
  $('#gsGo').onclick = o.onGo; if ($('#gsLink')) $('#gsLink').onclick = o.onLink;
}
const gsNeedPhoto = () => { toast(`Get a photo to ${CFG.QUALIFY}+ to play`); try { closeSheet(); } catch (e) {} TU_GAL = true; go('studio'); renderStudio(); };
const gsHow = t => () => toast(t);
// Head-to-head (friend challenges fold in here)
let H2H_ST = 1, H2H_RV = null;
function h2hSheet() { const me = fighters()[0]; if (!me) { gsNeedPhoto(); return; } const cat = me.cat || 'any';
  if (!H2H_RV || S.photos.some(p => p.src === H2H_RV)) H2H_RV = battleRival(cat).src;
  if (!tierOpen(H2H_ST)) H2H_ST = 1; const tkt = H2H_ST === 1 && (S.cashTix || 0) > 0, win = f => money(+(2 * f * (1 - KING_FEE)).toFixed(2));
  gameSheet({ ic: '⚔️', nm: 'Head-to-head', what: 'Your photo vs a rival’s · voters pick', pl: 'Winner takes', prize: win(H2H_ST), chip: '⚡ Result in about 2 min',
    left: gsPh(H2H_RV), lcap: 'A rival<small>Close to your score</small>', right: gsPh(me.src, me.s.total), rcap: `You<small>${esc(alName(me))}</small>`,
    stakes: [1, 5, 10].map(v => { const L = SCORE_LEVELS.find(x => x.fee === v); return { v, lock: !tierOpen(v), sub: tierOpen(v) ? `win ${win(v)}` : `🔒 ${L ? L.at + '+' : ''}` }; }), sel: H2H_ST,
    onPick: v => { if (!tierOpen(v)) { tierLockPop(v, me); return; } H2H_ST = v; h2hSheet(); },
    go: tkt ? 'Play · Free 🎟️' : `Play · $${H2H_ST}`, onGo: () => { const rv = H2H_RV; H2H_RV = null; window.__rvNext = rv; openCashBattle(H2H_ST, null, me); setTimeout(() => { const b = $('#duGo') || $('#duBuy'); if (b) b.click(); }, 40); },
    link: 'Challenge a friend instead', onLink: () => { closeSheet(); fcNew(); } }); }
// an incoming friend challenge: same screen, the stake is fixed by your friend
function incSheet(c) { const ph = fcPhotos(c.f, c.theme)[0];
  gameSheet({ ic: '🤝', nm: `@${esc(c.f)} challenged you`, what: `${esc(themeName(c.theme).replace('Best ', ''))} · your photo vs theirs · voters pick`, pl: 'Winner takes', prize: prizeTxt(c.stake), chip: '⏳ Answer within 24h',
    left: gsPh(c.theirSrc, c.theirScore), lcap: `@${esc(c.f)}<small>Their photo</small>`, right: ph ? gsPh(ph.src, ph.s.total) : gsTile('📷', 'Add one'), rcap: ph ? `You<small>${esc(alName(ph))}</small>` : 'You',
    fixed: `${stakeTxt(c.stake)} each`, fixedSub: `stake set by @${esc(c.f)}`, go: `Accept · ${stakeTxt(c.stake)}`,
    onGo: () => { if (!ph) { fcAccept(c); return; } const st = c.stake;
      if (st.cur === 'cash' ? (S.cash || 0) < st.amt : S.gems < st.amt) { closeSheet(); if (st.cur === 'cash') openStore(`You need $${st.amt} cash for this challenge.`); else runOut('gems', `You need ${st.amt - S.gems} more coins`, null, st.amt - S.gems); return; }
      const F = frS(); F.rec = F.rec || {}; F.rec[c.f] = F.rec[c.f] || { used: [] }; F.rec[c.f].used = F.rec[c.f].used || [];
      if (st.cur === 'cash') { S.cash = +((S.cash || 0) - st.amt).toFixed(2); paintWallet(); } else { S.gems -= st.amt; paintGems(); }
      F.rec[c.f].used.push(ph.id); c.myPid = ph.id; c.st = 'ready'; save(); closeSheet(); fcBattle(c); },
    link: 'Decline', onLink: () => { c.st = 'declined'; save(); closeSheet(); toast(`Declined @${c.f}’s challenge`); try { vcPaint(); } catch (e) {} } }); }
// Quick Sprint (your eye)
let QS_SEL = 2;
function qsSheet() { const l = typeof jgLv === 'function' && jgLv(), a = l ? jgAcc() : 0, rv = l ? Math.max(50, a - 1 - hsh(dayKey() + 'qs') % 4) : 0;
  gameSheet({ ic: '🎯', nm: 'Quick Sprint', what: 'Pick the crowd’s photo in 10 pairs · most right wins', pl: 'Winner takes', prize: qsM(qsPay(QS_SEL)[0]), chip: '⚡ About 30 seconds',
    left: gsRing(l ? rv : 50, l ? rv + '%' : '?', 'them'), lcap: 'A rival<small>Similar eye</small>', right: gsRing(l ? a : 50, l ? a + '%' : '?', 'me'), rcap: `You<small>${l ? l.n : 'New judge'}</small>`,
    stakes: [2, 5, 10].map(v => ({ v, sub: `win ${qsM(qsPay(v)[0])}` })), sel: QS_SEL, onPick: v => { QS_SEL = v; qsSheet(); },
    go: `Play · $${QS_SEL}`, onGo: () => { closeSheet(); window.__qsReal = 1; sprEnter(QS_SEL); },
    link: 'How it works', onLink: gsHow('10 photo pairs. Pick the one most voters chose. Most right wins; a tie goes to the faster player.') }); }
// Showdown: a room of 5
function sdSheet() { const a = sdActive(); if (a) { openSdRoom(a.id); return; } const me = fighters()[0]; if (!me) { gsNeedPhoto(); return; }
  const room = `<span class="pj-ph gs-room">${[0, 1, 2, 3].map(() => '<i>?</i>').join('')}</span>`;
  gameSheet({ ic: '⚡', nm: 'Showdown', what: '5 photos, one room · voters pick', pl: 'Winner takes', prize: money(sdPrize()), chip: '⏱ About 15 minutes',
    left: room, lcap: '4 rivals<small>Close to your score</small>', right: gsPh(me.src, me.s.total), rcap: `You<small>${esc(alName(me))}</small>`,
    fixed: money(SD_FEE), fixedSub: `5 players · winner takes ${money(sdPrize())}`, go: `Play · ${money(SD_FEE).replace('.00', '')}`,
    onGo: () => payCash(SD_FEE, 'A Showdown', () => { const r = sdNew(); r.lastSt = sdState(r).st; save(); openSdRoom(r.id); }),
    link: 'How it works', onLink: gsHow('Your photo takes a seat. When 5 have joined, voters pick and the highest vote share wins.') }); }
// Big Cup / Sprint (scheduled)
function tourSheet(kind) { const T = tSlots(), t = kind === 'big' ? T.find(x => x.gtd >= 100) : T.find(x => x.gtd < 100), me = fighters()[0]; if (!t) return; if (!me) { gsNeedPhoto(); return; }
  const nm = kind === 'big' ? 'Big Cup' : 'Sprint';
  gameSheet({ ic: kind === 'big' ? '🏆' : '⏱', nm, what: 'A scheduled tournament · voters pick the winners', pl: 'Prize pool', prize: `$${t.gtd}`, chip: t.now ? '⚡ Starts 1 min after you join' : `⏱ Starts in ${tLeft(t.at)}`,
    left: gsTile('👥', 'Everyone entered'), lcap: 'The field<small>Top photos share it</small>', right: gsPh(me.src, me.s.total), rcap: `You<small>${esc(alName(me))}</small>`,
    fixed: '$1', fixedSub: `one entry · $${t.gtd} prize pool`, go: 'Play · $1',
    onGo: () => { closeSheet(); cmpOpen('tour'); setTimeout(() => { const c = [...document.querySelectorAll('#flowBody .cmp-tc')].find(x => (x.querySelector('.cmp-tt b') || {}).textContent === nm); const b = c && c.querySelector('.cmp-go'); if (b) b.click(); setTimeout(() => { const j = $('#tkGo'); if (j) j.click(); }, 600); }, 450); },
    link: 'How it works', onLink: gsHow('Enter one photo. When it starts, voters judge every entry and the top photos share the prize pool.') }); }
// Crowd Championship (your eye)
function crowdSheet() { const l = typeof jgLv === 'function' && jgLv(), a = l ? jgAcc() : 0, nxt = chId() + 1, at = new Date(nxt * CH_MS).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }), pool = chPool(chPlayers(nxt, nxt * CH_MS));
  gameSheet({ ic: '👥', nm: 'Crowd Championship', what: `Pick the crowd’s favourites · 1st wins about $${Math.round(pool * .1).toLocaleString()}`, pl: 'Prize pool', prize: `$${pool.toLocaleString()}`, chip: `⏱ Starts at ${at}`,
    left: gsTile('👥', 'Every judge'), lcap: 'The field<small>Top 20% share</small>', right: gsRing(l ? a : 50, l ? a + '%' : '?', 'me'), rcap: `You<small>${l ? l.n : 'New judge'}</small>`,
    fixed: `$${CH_ENTRY}`, fixedSub: 'one entry', go: `Play · $${CH_ENTRY}`, onGo: () => { closeSheet(); chBuy(); setTimeout(() => { const b = $('#chJoin'); if (b) b.click(); }, 60); },
    link: 'How it works', onLink: gsHow('At the start time you get a run of photo pairs. Pick the one the crowd chose. The top 20% of scores share the pot.') }); }
// the Vote card opens the same screens; Champion and the separate friend card are gone
const _vcCardG = vcCard;
vcCard = function () { let c = _vcCardG.apply(this, arguments); if (!c) return c;
  const fr = S.fr && (S.fr.ch || []).find(x => x.st === 'yours');
  if (fr && /challenged you/.test(c.t)) return { ...c, t: `🤝 @${fr.f} challenged you`, s: `${stakeTxt(fr.stake)} each · winner takes ${prizeTxt(fr.stake)}`, cta: 'View', go: () => incSheet(fr) };
  if (/champion|Challenge a friend/i.test(c.t)) { const me = fighters()[0]; if (!me) return c; c = { img: me.src, t: `${alName(me)} vs a rival`, s: `Head-to-head · $1 wins $${(2 * (1 - KING_FEE)).toFixed(2)}`, cta: 'View', go: h2hSheet }; }
  if (/vs a rival/.test(c.t)) c.go = h2hSheet; else if (/eye|Quick Sprint/.test(c.t + ' ' + c.s)) c.go = qsSheet; else if (/Showdown/.test(c.t)) c.go = sdSheet; else if (/Quick tournament/.test(c.t)) c.go = () => tourSheet('sprint');
  return c; };
setTimeout(() => { try { vcPaint(); } catch (e) {} }, 500);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* the shared game screen */
.gs-what{margin:2px 0 0;font:700 .86rem "Nunito Sans";color:#4E433C}
.gs-pl{display:block;font:800 .7rem "Nunito Sans";letter-spacing:.07em;text-transform:uppercase;color:#2E6B42;margin-bottom:2px}
.gs-rg{display:flex!important;align-items:center;justify-content:center;background:linear-gradient(160deg,#EEF3FB,#DCE6F6)!important}.gs-rg .c3-ring{width:78%;height:auto;aspect-ratio:1}.gs-rg .c3-ring b{width:76%;height:76%}
.gs-tl{display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:6px;background:linear-gradient(160deg,#2B4372,#14213D)!important;color:#fff}.gs-tl span{font-size:2.6rem}.gs-tl b{font:900 .95rem Fraunces,serif;color:#fff}
.gs-room{display:grid!important;grid-template-columns:1fr 1fr;gap:5px;padding:6px;box-sizing:border-box;background:#EFE6D6!important}.gs-room i{display:flex;align-items:center;justify-content:center;border-radius:9px;background:linear-gradient(160deg,#2B4372,#14213D);color:#fff;font:900 1.4rem Fraunces,serif;font-style:normal}
.sk-row.gs-fix{grid-template-columns:1fr}html body .sk-row.gs-fix button{background:#FFFDF9!important;box-shadow:inset 0 0 0 2px #2E9A5C!important;color:#21784A!important;opacity:1;flex-direction:row;justify-content:center;gap:8px}.sk-row.gs-fix button small{color:#4E433C!important}
.gs .pj-t,.pj .pj-t{font-size:clamp(1.15rem,5.6vw,1.5rem);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
html body #sheetBody .pj-go .vs-ic,html body #sheetBody .pj-go svg{display:none}
.pj .pj-win{display:none}
.sk-row button.lock{background:#F3EDE2;box-shadow:inset 0 0 0 1.5px #E2D5BE;color:#8A7E72}.sk-row button.lock small{color:#8A7E72}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('games ok')
