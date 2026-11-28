# Skill preview: the touch-up keeps one name from Improve to Before and after (user chose option B).
#  - Improve: while the first photo's welcome gift covers the touch-up, the gold button reads "Boost colour · Free 🎁"
#    (it used to show the 50-coin price under a "first touch-up on us" line).
#  - Improve: the selected touch-up row shows "↑" instead of a projected part score, which the real result rarely matched
#    (it said Colour → 53, then the result was 44 → 64).
#  - Before and after: the navy button uses the touch-up name: "Use Boost colour · Gold 🥇" (was "Touch up · Unlock Gold").
#    It stays navy because nothing more is spent there.
#  - Improve: the picked row keeps its current score ("73 ↑"), and the line under the score says what the photo is
#    now ("Milo is 🥇 Gold · earns 4 coins a vote") or what the picked touch-up could make it ("Fix lighting could make
#    Milo 💎 Diamond · 8 coins a vote"), instead of "Diamond photos earn you 8 per vote", which read as already done.
# Usage: python3 build-skill/ctafix.py in.html out.html  (run after gstyle.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''(() => {
  const giftOn = () => S.firstGift === 1 && S.photos.length === 1 && !S.photos[0].enh;
  const _im2 = im2Render;
  im2Render = function () { const r = _im2.apply(this, arguments);
    try {
      const b = document.querySelector('#studio #i2Go'), sp = b && b.querySelector('span');
      if (b && sp && giftOn()) { sp.innerHTML = 'Free 🎁'; b.classList.add('cta-free'); }
      const on = document.querySelector('#studio .im2-row.on .im2-rl b');
      const pp = (S.photos || []).find(x => x.id === S.cur) || (typeof cur === 'function' ? cur() : null), row = document.querySelector('#studio .im2-row.on'), op = pp && row ? im2Opts(pp).find(o => o.k === row.dataset.i2) : null;
      if (on && /→/.test(on.textContent)) { on.innerHTML = `${op ? pp.s[op.part] + ' ' : ''}<em>↑</em>`; on.setAttribute('aria-label', 'Current score, this touch-up raises it'); }
      // the line under the score says what Milo IS now, or what this touch-up COULD make it (never reads as if it already happened)
      const sh = document.querySelector('#studio .im2-sh'); if (sh && pp && pp.s) { const v = pp.s.total, t0 = galTier(v), TI = { Gold: '🥇', Diamond: '💎', Platinum: '🏆' }, nm = esc(alName(pp));
        const to = op ? im2Proj(pp, op) : v, t1 = galTier(to);
        sh.innerHTML = op && t1 && t1 !== t0 ? `${esc(op.v)} could make ${nm} ${TI[t1]} <b>${t1}</b> · ${GAL.BASE * galMult(to)} coins a vote`
          : t0 ? `${nm} is ${TI[t0]} <b>${t0}</b> · earns ${GAL.BASE * galMult(v)} coins a vote` : `${nm} is not ranked yet · reach <b>70</b> for 🥇 Gold`; }
    } catch (e) {}
    return r; };
  const _rv = renderVariants;
  renderVariants = function () { const r = _rv.apply(this, arguments);
    try {
      const b = document.querySelector('#flowBody #useBtn'), sp = b && b.querySelector('span'), e = IM2.EDITS.find(x => x.part === EN.cat);
      if (sp && e) { const tag = document.querySelector('#flowBody .lvtag'), lv = tag ? tag.textContent.replace('!', '').trim() : '';
        const ic = lv.split(' ')[0], nm = lv.split(' ').slice(1).join(' ');
        sp.textContent = `Use ${e.v}${nm ? ` · ${nm} ${ic}` : ''}`; }
    } catch (x) {}
    return r; };
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
open(p, 'w').write(s); print('ctafix ok')
