# Skill preview: win a stolen card back (user chose option A: the stealer never has to bet).
#  Every "Win Palm garden back" (away pop, Gallery banner, Payday receipt) opens one game screen: a normal one-dollar
#  Photo Duel against a rival who chose to play (close to your score), with your best photo from the stolen card's
#  category (or your best photo). "Winner takes $1.70 + card"; winning also brings the card back from the stealer,
#  who risks no money (they just lose a card they got free). Lose: the card stays, gold "Touch up Milo".
# Usage: python3 build-skill/winback.py in.html out.html  (run after cmpjudge.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- win it back: $1 Photo Duel vs the stealer ----
(() => { const WB_FEE = 1, WB_WIN = +(2 * WB_FEE * .85).toFixed(2);
  const _ss = stealSheet;
  stealSheet = function (o = {}) { const held = o && o.back ? S.photos.find(x => x.id === o.back && x.heldBy) : null; if (!held) return _ss.apply(this, arguments);
    try { closeSheet(); } catch (e) {} try { popClose(); } catch (e) {} const co = $('#coach'); if (co && co.classList.contains('on')) { co.classList.remove('on', 'cr'); co.innerHTML = ''; }
    const own = S.photos.filter(p => p.s && !p.heldBy && !p.card).sort((a, b) => b.s.total - a.s.total), me = own.find(p => p.cat === held.cat) || own[0]; if (!me) { toast('Add a photo to play for your card'); return; }
    const who = rvName(held.heldBy), nm = alName(held), rv = RIVALS[hsh(held.id + todayKey()) % RIVALS.length], rh = rv.h === held.heldBy ? RIVALS[(RIVALS.indexOf(rv) + 1) % RIVALS.length].h : rv.h, rk = me.cat || 'any',
      rsrc = (() => { try { return c2NotMine(battleRival(rk).src, rk); } catch (e) { return held.src; } })(), rsc = Math.max(55, Math.min(95, me.s.total + (hsh(held.id + rh) % 7) - 3));
    setTimeout(() => gameSheet({ ic: '⚔️', nm: `Win ${esc(nm)} back`, what: `Win any Photo Duel · ${esc(nm)} comes back from ${esc(who)}`, pl: 'Winner takes', prize: `$${WB_WIN.toFixed(2)} + card`, chip: '⚡ Result in about a minute',
      left: gsPh(rsrc, rsc), lcap: `${esc(rvName(rh))}<small>Close to your score</small>`, right: gsPh(me.src, me.s.total), rcap: `You<small>${esc(alName(me))}</small>`,
      fixed: `$${WB_FEE}`, fixedSub: `win $${WB_WIN.toFixed(2)} and the card`, go: `Win it back · $${WB_FEE}`,
      onGo: () => { closeSheet(); payCash(WB_FEE, `Win ${nm} back`, () => wbPlay(held, me, who, rh, rsc)); } }), 120); };
  function wbPlay(held, me, who, rh, rsc) { const nm = alName(held), d = me.s.total - rsc, pw = Math.max(.25, Math.min(.8, .5 + d * .02)), won = Math.random() < pw;
    const a = won ? 8 + Math.floor(Math.random() * 4) : 5 + Math.floor(Math.random() * 3), b = won ? a - 1 - Math.floor(Math.random() * 3) : a + 1 + Math.floor(Math.random() * 3);
    toast('🗳 Voters are picking…');
    setTimeout(() => { if (won) { held.heldBy = null; held.heldAt = null; S.cash = +((S.cash || 0) + WB_WIN).toFixed(2); save(); try { paintWallet(); } catch (e) {}
        try { winPop(WB_WIN, 'cash', `${nm} is back`); } catch (e) {}
        setTimeout(() => celebrate({ src: held.src, score: '🏆', title: `${nm} is back!`, text: `You beat <b>${esc(rvName(rh))}</b> ${a}–${b}. <b>+$${WB_WIN.toFixed(2)}</b> added to your cash, and ${esc(nm)} is back from ${esc(who)}.`, cta: 'Back to voting', onCta: () => {} }), 1800); }
      else { save(); celebrate({ src: held.src, score: '😤', title: 'So close!', text: `<b>${esc(rvName(rh))}</b> won ${b}–${a}, so ${esc(nm)} stays with ${esc(who)}. Touch up ${esc(alName(me))} and try again.`, cta: `✨ Touch up ${alName(me)}`,
        onCta: () => { S.cur = me.id; TU_GAL = false; WALL = false; AL_OPEN = null; save(); go('studio'); try { renderStudio(); } catch (e) {} }, later: 'Back to voting' }); } }, 2600); }
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
open(p, 'w').write(s); print('winback ok')
