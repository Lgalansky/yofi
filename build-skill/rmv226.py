# Real Money build, step 229 (after rmv225.py): navy & gold sign-up showing the framed photo.
#  - The required sign-up after framing opens on the player's framed photo (gold frame + name plaque):
#    "Sign up to start racing it" · "<name> is framed and ready for the <category> qualifiers".
#  - Navy & gold sheet: gold welcome-bonus pill, dark inputs, gold age buttons, green "Create account & start racing".
#  - Other sign-up sheets (fallbacks) keep their wording and get the same navy look.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""(() => { const os = openSignup; openSignup = function (then, opts = {}) { const r = os.apply(this, arguments); try { const sh = document.getElementById('sheet'), body = document.getElementById('sheetBody'); if (!sh || !body) return r; sh.classList.add('su-nv');
    if (opts.photo) { const P = (S.photos || []).filter(x => x.framed), p = P[P.length - 1]; const h2 = body.querySelector('h2');
      if (p && h2) { const cat = (() => { try { return showName(photoShow(p) || finCatOf(p) || p.cat); } catch (e) { return ''; } })();
        h2.insertAdjacentHTML('beforebegin', `<div class="su-fr"><div class="su-fm"><img src="${p.src}" alt=""></div><div class="su-pl"><b>${esc(rcName(p))}</b><small>${esc(cat || '')} · framed</small></div></div>`);
        h2.textContent = 'Sign up to start racing it'; h2.insertAdjacentHTML('afterend', `<p class="su-k">${esc(rcName(p))} is framed and ready for the ${esc(cat || '')} qualifiers.</p>`);
        const sub = body.querySelector('p.sub'); if (sub) sub.parentNode.removeChild(sub); } }
    const go = document.getElementById('suGo'); if (go && opts.photo) go.textContent = 'Create account & start racing'; } catch (e) {} return r; }; })();
(() => { const cs = closeSheet; closeSheet = function () { try { document.getElementById('sheet').classList.remove('su-nv'); } catch (e) {} return cs.apply(this, arguments); }; })();
function fcNotify() {""")
s = s.replace('</style>', """html body #sheet.su-nv{background:radial-gradient(130% 60% at 50% 0%,#24376A,#14213D 55%,#0E1830)!important;color:#EEF1F8}
html body #sheet.su-nv .grab{background:rgba(255,255,255,.3)}
html body #sheet.su-nv #sheetBody h2{color:#FBF3DC!important;text-align:center!important;font:900 1.7rem/1.1 Fraunces,Georgia,serif!important;margin:10px 0 4px!important}
.su-fr{display:flex;flex-direction:column;align-items:center;margin:6px 0 4px}
.su-fm{padding:9px;border-radius:12px;background:linear-gradient(135deg,#F3D98B,#C9952D 40%,#F3D98B 70%,#B9852A);box-shadow:0 10px 24px -8px rgba(0,0,0,.6)}.su-fm img{display:block;width:150px;height:150px;object-fit:cover;border-radius:4px;box-shadow:inset 0 0 0 2px rgba(0,0,0,.2)}
.su-pl{margin-top:-8px;padding:5px 16px;border-radius:8px;background:linear-gradient(#F3D98B,#D9AE4F);color:#14213D;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,.35);z-index:1}.su-pl b{display:block;font:900 .95rem Fraunces,Georgia,serif}.su-pl small{font:800 .68rem Nunito,system-ui;letter-spacing:.06em;text-transform:uppercase}
.su-k{margin:0 0 12px;text-align:center;font:600 .92rem/1.35 Nunito,system-ui;color:#C9D3E6}
html body #sheet.su-nv .wbx{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;padding:8px 12px!important;border-radius:999px!important;background:rgba(217,174,79,.15)!important;box-shadow:inset 0 0 0 1.5px #D9AE4F!important;color:#FBF3DC!important;margin:0 0 12px!important}
html body #sheet.su-nv .wbx span{font:900 .72rem Nunito,system-ui!important;color:#F3D98B!important;letter-spacing:.08em}html body #sheet.su-nv .wbx b{font:900 1rem Nunito,system-ui!important;color:#FBF3DC!important}html body #sheet.su-nv .wbx small{display:none}
html body #sheet.su-nv .sub{color:#C9D3E6!important}html body #sheet.su-nv label.field{color:#F3D98B!important;font-weight:800}
html body #sheet.su-nv label.field input{background:rgba(255,255,255,.08)!important;color:#fff!important;border:0!important;box-shadow:inset 0 0 0 1.5px rgba(217,174,79,.5)!important}html body #sheet.su-nv label.field input::placeholder{color:#8C9AB5}
html body #sheet.su-nv .su-age>span{color:#F3D98B}html body #sheet.su-nv .su-age>span small{color:#C9D3E6}
html body #sheet.su-nv .su-age button{background:rgba(255,255,255,.08);color:#EEF1F8;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.2)}html body #sheet.su-nv .su-age button[aria-pressed="true"]{background:linear-gradient(#F3D98B,#D9AE4F);color:#14213D;box-shadow:none}
html body #sheet.su-nv #suGo{min-height:54px!important;border-radius:999px!important;background:linear-gradient(180deg,#2F8A45,#1E6B34)!important;color:#fff!important;font:900 1.08rem Nunito,system-ui!important}
html body #sheet.su-nv .err{color:#FFB4A8!important}html body #sheet.su-nv .link{color:#C9D3E6!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v226 ok')
