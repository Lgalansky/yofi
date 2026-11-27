# Skill preview: three tidy-ups from the user's phone screenshots.
#  1. The Improve button now matches the app's shared gold coin button: centred bold label,
#     "Fix lighting · 50 🟡", same height and shape as every other main button (no dark price chip).
#  2. The first-photo welcome gift is a small moment, said once: coins fly from the score into the
#     balance (no big banner that spilled off-screen), and one gold line under the score says
#     "🎁 Welcome gift · first touch-up on us" until that touch-up is used.
#     Every big "+N coins" banner is also kept inside the screen.
#  3. Cards won in a steal: "🃏 Won from Maya" replaces the "Earns on votes" pill at the bottom
#     of the photo, so it no longer covers the score badge.
# usage: python3 build-skill/cardfix.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

# 2. the first-photo gift: small fly-in instead of the big banner
a = "gemExplosion(gift, { label: S.photos.length === 1 ? 'Welcome gift · enough for your first touch-up' : 'Daily upload bonus', from: $('#i2Score') })"
assert s.count(a) == 1
s = s.replace(a, "(S.photos.length === 1 ? gemExplosion(gift, { mid: 1, from: $('#i2Score') }) : gemExplosion(gift, { label: 'Daily upload bonus', from: $('#i2Score') }))")

JS = r'''
// ---- welcome gift line on Improve; won-card label on the gallery card ----
function cfTidy() {
  const st = document.querySelector('#studio .im2'); if (st && S.firstGift === 1 && S.photos.length === 1 && !S.photos[0].enh) {
    const ln = [...st.querySelectorAll('div,p')].find(x => /^Earns you/.test((x.textContent || '').trim()) && x.children.length < 8);
    if (ln && !ln.dataset.cf) { ln.dataset.cf = 1; ln.classList.add('cf-gift'); ln.innerHTML = '🎁 <b>Welcome gift</b> · first touch-up on us'; } }
  document.querySelectorAll('#studio .a2-sl[data-alc]').forEach(b => { const p0 = S.photos.find(x => x.id === b.dataset.alc); if (!p0 || !p0.card) return;
    const tg = b.querySelector('.stl-tag'); if (tg) tg.remove(); const e = b.querySelector('.a2-earn'); if (e && !e.dataset.cf) { e.dataset.cf = 1; e.classList.add('cf-won'); e.innerHTML = `<small>🃏 Won from ${esc(rvName(p0.card.from))}</small>`; } });
}
new MutationObserver(() => { try { cfTidy(); } catch (e) {} }).observe($('#studio'), { childList: true, subtree: true });
setTimeout(() => { try { cfTidy(); } catch (e) {} }, 300);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Improve: the shared gold coin button */
html body .im2 #i2Go.im2-apply,html body .im2 .im2-apply{justify-content:center!important;gap:8px;min-height:54px;height:auto!important;padding:0 24px!important;border-radius:999px;font:900 1.05rem "Nunito Sans"!important;letter-spacing:0}
html body .im2 .im2-apply span{background:none!important;box-shadow:none!important;padding:0!important;height:auto!important;font:900 1.05rem "Nunito Sans"!important;color:inherit!important;display:inline-flex;align-items:center;gap:4px}
html body .im2 .im2-apply span::before{content:"·";margin-right:4px}
html body .im2 .im2-apply .im2-coin{width:18px;height:18px}
/* welcome gift line */
html body .im2 .cf-gift{background:linear-gradient(180deg,#FFF1C9,#F8E2A6)!important;color:#5A3D00!important;font:800 .9rem "Nunito Sans"!important;box-shadow:inset 0 0 0 1.5px #E8C771}
html body .im2 .cf-gift b{color:#3A2600}
/* big coin banners stay on screen */
.gembig{max-width:calc(100% - 32px);box-sizing:border-box;white-space:normal;text-align:center}
.gembig b{font-size:clamp(2.4rem,14vw,3.6rem)!important}.gembig span{font-size:.95rem!important}
/* won-card label sits where "Earns on votes" was */
html body #studio .a2-earn.cf-won{background:#1F3157!important;color:#fff!important}html body #studio .a2-earn.cf-won small{color:#fff!important;letter-spacing:0;text-transform:none}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('cardfix ok')
