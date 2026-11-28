# Skill preview: Live games tiles in the user's mock-up style.
#  Two big tiles side by side (no sideways scroll): photo on top with a navy title chip
#  ("🏆 Pet Challenge", "🤝 Friend Challenge"), a navy panel below with a big gold headline
#  ("$3,926 prize" / "Win $1.70"), one detail line ("Ends in 3h 27m" / "Invite on WhatsApp") and
#  a green cash button ("Play from $1" / WhatsApp icon + "Invite · $1"). The friend tile is green
#  with your best photo vs a friend's photo and a VS badge.
# usage: python3 build-skill/lgx2.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- Live games: big tile style ----
function lgx2() { document.querySelectorAll('#judge .lgx-wrap').forEach(w => { if (w.dataset.l2 === w.dataset.sig) return; w.dataset.l2 = w.dataset.sig; w.classList.add('l2');
  w.querySelectorAll('.lgx').forEach(t => { const ch = t.querySelector('.lgx-chip'), b = t.querySelector('b'), sm = t.querySelector('small:not(.lgx-d)'), em = t.querySelector('em');
    if (ch) ch.textContent = ch.textContent.replace(/^💰/, '🏆').replace(/challenge$/, 'Challenge').replace(/^🤝 Friend Challenge$/i, '🤝 Friend Challenge');
    if (sm && /^Ends /.test(sm.textContent)) sm.textContent = sm.textContent.replace(/^Ends /, 'Ends in ');
    if (em) em.textContent = em.textContent.replace(/^Play · from /, 'Play from ');
    if (t.querySelector('.lgx-wa')) { t.classList.add('fr'); const me = S.photos.filter(x => x.s && !x.heldBy).sort((a, c) => c.s.total - a.s.total)[0], cat = me ? me.cat || 'any' : 'pets', other = (SEED.find(x => x.cat === BATTLE_POOL[cat] && x.src !== (me || {}).src) || SEED[1]).src;
      t.querySelector('.lgx-ph').innerHTML = `<span class="fr-pair"><img src="${me ? me.src : SEED[0].src}" alt=""><i>VS</i><img src="${other}" alt=""></span>${ch ? ch.outerHTML : ''}`;
      if (sm) sm.textContent = 'Invite on WhatsApp'; if (em) em.innerHTML = `${WA_ICON}<span>${em.textContent}</span>`; } }); }); }
new MutationObserver(() => { try { lgx2(); } catch (e) {} }).observe($('#judge'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Live games: big tiles */
html body #judge .lgx-wrap.l2 .lgx-row{display:grid!important;grid-template-columns:1fr 1fr;gap:10px;overflow:visible!important;padding:2px 14px 10px!important}
html body #judge .l2 .lgx{display:flex!important;flex-direction:column!important;width:auto!important;padding:0!important;border-radius:18px!important;overflow:hidden;background:#14213D!important;box-shadow:0 0 0 2px #E0A82E,0 10px 18px -10px rgba(0,0,0,.6)!important;text-align:center!important;align-items:stretch}
html body #judge .l2 .lgx-ph{height:108px!important;margin:0!important;border-radius:0!important}
html body #judge .l2 .lgx-chip{left:8px!important;top:8px!important;right:8px;padding:4px 10px!important;border-radius:99px!important;background:rgba(20,33,61,.92)!important;color:#fff!important;font:900 .74rem/1.15 Fraunces,serif!important;text-align:center;white-space:normal;box-shadow:0 0 0 1px rgba(243,210,122,.5)}
html body #judge .l2 .lgx b{margin:8px 6px 0!important;font:900 1.2rem/1.1 Fraunces,serif!important;color:#F3D27A!important}
html body #judge .l2 .lgx small{margin:2px 6px auto!important;font:700 .78rem "Nunito Sans"!important;color:#E6EDF8!important}
html body #judge .l2 .lgx small.lgx-d{display:none!important}
html body #judge .l2 .lgx em{display:flex!important;align-items:center;justify-content:center;gap:6px;margin:8px 8px 10px!important;padding:8px 0!important;border-radius:99px!important;background:linear-gradient(180deg,#34A866,#1E7A44)!important;color:#fff!important;font:900 .92rem "Nunito Sans"!important;box-shadow:0 4px 10px -6px rgba(33,120,74,.8)}
html body #judge .l2 .lgx em svg{width:18px;height:18px}
html body #judge .l2 .lgx.fr{background:#0F3A2A!important}
html body #judge .l2 .lgx.fr .lgx-ph{background:radial-gradient(circle at 50% 40%,#2E9A5C,#145A36)!important}
.fr-pair{position:absolute;inset:34px 8px 6px;display:flex;align-items:center;justify-content:center;gap:0}
.fr-pair img{width:46%!important;height:100%!important;object-fit:cover;border-radius:8px;border:3px solid #fff;box-shadow:0 4px 8px rgba(0,0,0,.4)}.fr-pair img:first-child{transform:rotate(-5deg)}.fr-pair img:last-child{transform:rotate(5deg)}
.fr-pair i{position:absolute;left:50%;top:55%;transform:translate(-50%,-50%);width:30px;height:30px;border-radius:50%;background:#1F3157;color:#fff;font:900 .72rem/30px Fraunces,serif;font-style:normal;box-shadow:0 0 0 2px #F3D27A;z-index:1}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('lgx2 ok')
