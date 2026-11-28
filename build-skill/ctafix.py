# Skill preview: the touch-up keeps one name from Improve to Before and after (user chose option B).
#  - Improve: while the first photo's welcome gift covers the touch-up, the gold button reads "Boost colour · Free 🎁"
#    (it used to show the 50-coin price under a "first touch-up on us" line).
#  - Improve: the selected touch-up row shows "↑" instead of a projected part score, which the real result rarely matched
#    (it said Colour → 53, then the result was 44 → 64).
#  - Before and after: the navy button uses the touch-up name: "Use Boost colour · Gold 🥇" (was "Touch up · Unlock Gold").
#    It stays navy because nothing more is spent there.
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
      if (on && /→/.test(on.textContent)) { on.innerHTML = '<em>↑</em>'; on.setAttribute('aria-label', 'Raises this score'); }
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
