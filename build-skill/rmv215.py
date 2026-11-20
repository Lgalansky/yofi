# Real Money build, step 218 (after rmv214.py): the age question moves out of the Final.
#  - Sign-up now asks for the age group (six quick buttons, required, 18+), so the Final, cash entries and
#    the Cup no longer stop for it.
#  - Players who already have an account but no age on file are asked once when they open the app (when nothing
#    else is on screen), not mid-race.
#  - The age check before any cash play stays as a backstop.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("""<label class="field">Email<input id="suE" type="email" autocomplete="email" placeholder="you@example.com"></label>
    <p class="err" id="suErr"></p>""",
   """<label class="field">Email<input id="suE" type="email" autocomplete="email" placeholder="you@example.com"></label>
    ${S.ageBr && S.obDone ? '' : `<div class="su-age"><span>Age group <small>· PhotoPicks is for adults 18+</small></span><div>${OB_AGES.map(a => `<button type="button" data-sua="${a}" aria-pressed="${a === S.ageBr}">${a}</button>`).join('')}</div></div>`}
    <p class="err" id="suErr"></p>""")
RA("""    if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(em)) { $('#suErr').textContent = 'Enter an email like name@example.com.'; return; }""",
   """    if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(em)) { $('#suErr').textContent = 'Enter an email like name@example.com.'; return; }
    if (document.querySelector('.su-age') && !window.__suAge) { $('#suErr').textContent = 'Pick your age group. PhotoPicks is for adults 18+.'; return; }
    if (window.__suAge) { S.ageBr = window.__suAge; window.__suAge = null; S.likes0 = null; S.crews = []; S.crewCur = null; S.age18 = 1; S.adult = 1; S.obDone = 1; save(); try { setLook(); youngPass(); paintTop(); } catch (e) {} }""")
RA("function fcNotify() {", r"""document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-sua]'); if (!b) return; e.preventDefault(); window.__suAge = b.dataset.sua;
  document.querySelectorAll('[data-sua]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false')); const er = document.getElementById('suErr'); if (er && /age/.test(er.textContent)) er.textContent = ''; });
setTimeout(() => { try { if (S.user && !S.user.guest && !(S.obDone && S.ageBr)) qsWhenFree(() => { if (!(S.obDone && S.ageBr)) ageGate(); }); } catch (e) {} }, 1500);
function fcNotify() {""")
s = s.replace('</style>', """.su-age{margin:4px 0 6px}.su-age>span{display:block;margin-bottom:6px;font:800 .9rem Nunito,system-ui;color:#14213D}.su-age>span small{font-weight:600;color:#6B5B4B}
.su-age>div{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.su-age button{min-height:40px;border:0;border-radius:12px;background:#FBF6EE;box-shadow:inset 0 0 0 1.5px #E2D5C2;font:700 .86rem Nunito,system-ui;color:#3D2B1F;cursor:pointer}
.su-age button[aria-pressed="true"]{background:#14213D;color:#F3D98B;box-shadow:inset 0 0 0 2px #D9AE4F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v215 ok')
