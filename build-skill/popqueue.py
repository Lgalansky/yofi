# One pop at a time (Skill). 26 different pops all draw into the same #coach overlay, so a pop
# that fires while another is open used to replace it (e.g. the daily-rewards pop wiping a lucky box).
# - Reward and result pops (wins, boxes, card printed / tier up) wait in a queue and open one after
#   another, 0.9 s after the previous one closes.
# - "Nudge" pops (daily rewards, streak, welcome, gifts, level-ups, tickets, deposit offer, away,
#   mystery, ready-to-compete) are dropped if another pop showed in the last 90 s or one is waiting.
# - Nudges wait while a full screen (upload, results) is open, for up to 30 s.
# - Pops the player opens themselves (menus, how-it-works, pickers) are not touched.
# - Card win banners don't show over an open pop (the coins are still paid).
# - Box pops (lucky box, mystery drop) open at most once every 12 votes; runs in between pay a small coin burst.
# Usage: python3 build-skill/popqueue.py [in.html] [out.html]  (run after cards.py)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'const POPQ =' in s: sys.exit('popqueue already applied')
assert 'function cardPop(' in s, 'run cards.py first'
NAG = ['streakPop', 'welcomePop', 'giftPop', 'levelsPop', 'ticketPop', 'firstDepositOffer', 'awayPop', 'mysteryPop', 'showCompReady']
KEEP = ['miniDrop', 'luckyDrop', 'chestOpen', 'winPop', 'celebrate', 'cardPop']
wraps = '\n'.join(f"if (typeof {n} === 'function') {n} = popWrap('{n}', {n});" for n in NAG + KEEP)
JS = r'''
/* ---------- one pop at a time ---------- */
const POPQ = { q: [], last: 0, closedAt: 0 }, POP_NAG = ''' + repr(NAG).replace("'", '"') + r''';
const popBusy = () => $('#coach').classList.contains('on') || ((document.getElementById('ageGate') || {}).className === 'on');
function popPump() {
  if (popBusy() || !POPQ.q.length) return;
  const wait = 900 - (Date.now() - POPQ.closedAt); if (wait > 0) { setTimeout(popPump, wait + 30); return; }
  const [f, args, self] = POPQ.q.shift(); POPQ.last = Date.now(); f.apply(self, args);
}
function popWrap(name, f) {
  const run = function (tries) {
    const nag = POP_NAG.includes(name), self = this, args = arguments[1];
    if (nag && $('#flow').classList.contains('on') && tries < 20) { setTimeout(() => run.call(self, tries + 1, args), 1500); return; }
    return inner.apply(self, args);
  };
  const inner = function () {
    const nag = POP_NAG.includes(name);
    if (nag && (Date.now() - POPQ.last < 90000 || POPQ.q.length || popBusy())) return;
    if (popBusy() || POPQ.q.length) { POPQ.q.push([f, arguments, this, name]); return; }
    POPQ.last = Date.now(); return f.apply(this, arguments);
  };
  return function () { return run.call(this, 0, arguments); };
}
// box pops at most once every 12 votes; in between, a right-picks run pays a small coin burst instead
const BOX_GAP = 12;
function boxPace(name, f) {
  return function (kind) {
    if (S.boxAtV != null && (S.votes || 0) - S.boxAtV < BOX_GAP) { const n = ({ 3: 10, 5: 20, 10: 40 })[kind] || 15; S.gems += n; save(); gemExplosion(n, { label: kind ? `${kind === 5 ? 6 : kind} right in a row` : 'Bonus' }); return; }
    S.boxAtV = S.votes || 0; save(); return f.apply(this, arguments);
  };
}
// the coins nudge points at the loop: touch up your best-value card (always possible), never a locked game
if (typeof gemNudge === 'function') gemNudge = function (force) {
  if (!S.user || (S.votes || 0) < 12 || popBusy() || $('#sheet').classList.contains('on') || Date.now() - POPQ.last < 90000) return false;
  const mark = Math.floor(S.gems / 100) * 100; if (!force && (mark <= (S.gnMark || 0) || (S.votes || 0) - (S.gnVote || 0) < 40)) return false;
  const c = S.photos.filter(x => x.s && !photoLock(x) && lowestOpen(x) && S.gems >= fixCost(x)).sort((a, b) => CARD_T[cardTier(b.s.total)].x - CARD_T[cardTier(a.s.total)].x || b.s.total - a.s.total)[0];
  if (!c) return false; S.gnMark = mark; S.gnVote = S.votes || 0; save();
  const k = cardTier(c.s.total), nx = CARD_T[k + 1];
  celebrate({ src: c.src, score: CARD_T[k].n, title: `You’ve got ${Math.floor(S.gems).toLocaleString()} coins!`, text: nx ? `Touch up your <b>${CARD_T[k].n}</b> card. It’s <b>${nx.at - c.s.total}</b> points from <b>${nx.n} ×${nx.x}</b>, which pays more on every vote it wins.` : 'Touch up your card to keep it on top.',
    cta: `Touch it up · ${fixCost(c)} 🟡`, onCta: () => { S.cur = c.id; S.pcView = 'touch'; save(); go('studio'); renderStudio(); }, later: 'Later' });
  return true;
};
if (typeof miniDrop === 'function') miniDrop = boxPace('miniDrop', miniDrop);
if (typeof luckyDrop === 'function') luckyDrop = boxPace('luckyDrop', luckyDrop);
''' + wraps + r'''
new MutationObserver(() => { if (!$('#coach').classList.contains('on')) { POPQ.closedAt = Date.now(); setTimeout(popPump, 930); } else document.querySelectorAll('.pc-ban').forEach(e => e.remove()); }).observe($('#coach'), { attributes: true, attributeFilter: ['class'] });
'''
end = "  shownGems = S.gems;\n})();\n})();"
assert s.count(end) == 1
s = s.replace(end, JS + end)
a = "document.body.appendChild(b); setTimeout(() => b.classList.add('on'), 20);"
assert s.count(a) == 1
s = s.replace(a, "document.querySelectorAll('.pc-ban').forEach(e => e.remove()); if (popBusy()) { setTimeout(paintGems, 300); paintCardStrip(); return; } document.body.appendChild(b); setTimeout(() => b.classList.add('on'), 20);")
open(p, 'w', encoding='utf-8').write(s); print('popqueue ok')
