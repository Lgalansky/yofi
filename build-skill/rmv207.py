# Real Money build, step 210 (after rmv206.py): "Tell me when it's ready" + clearer sign-up titles.
#  - A "🔔 Tell me when it's ready" button on the two waits: the free rematch (loss screen) and the Daily Cup (entered card).
#    It asks for browser notifications; the rematch-ready and Cup-results messages then go through notify()
#    (a real notification when the tab is in the background, a toast otherwise).
#  - Sign-up sheet title now matches why it opened: "Create your account to claim your free Final" /
#    "Create your account to enter the Daily Cup" (was "Save your photo" / "…to play for cash").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)
RA("<h2>${opts.real ? ((S.cashTix", "<h2>${opts.fin ? 'Create your account to claim your free Final' : opts.cup ? 'Create your account to enter the Daily Cup' : opts.real ? ((S.cashTix")
RA("qfPick(p, 2), 250), { locked: false, photo: 1 }", "qfPick(p, 2), 250), { locked: false, photo: 1, fin: 1 }")
RA("openSignup(() => setTimeout(finalsTab, 250), { locked: false, real: 1 })", "openSignup(() => setTimeout(finalsTab, 250), { locked: false, real: 1, cup: 1 })")
RA("Or train now to skip the wait.</small></div>", "Or train now to skip the wait.</small>${tmBtn()}</div>")
RA("""<button class="cup-demo" data-cup="demo">""", """${tmBtn()}<button class="cup-demo" data-cup="demo">""")
RA("toast(`🏁 ${rcName(p)}’s rematch is ready`)", "notify('PhotoPicks', `🏁 ${rcName(p)}’s rematch is ready`)")
RA("function fcNotify() {", r"""function tmBtn() { return S.alerts ? '<p class="tm-on">🔔 We’ll tell you when it’s ready</p>' : '<button class="tm-b" data-tm="1">🔔 Tell me when it’s ready</button>'; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-tm]'); if (!b) return; e.preventDefault(); e.stopPropagation();
  const done = on => { S.alertsAsked = true; S.alerts = on; save(); document.querySelectorAll('[data-tm]').forEach(x => x.outerHTML = tmBtn()); toast(on === 'push' ? '🔔 Done. We’ll tell you when it’s ready' : '🔔 We’ll tell you here when it’s ready'); };
  try { if ('Notification' in window && Notification.permission !== 'denied') { Notification.requestPermission().then(r => done(r === 'granted' ? 'push' : 'inapp')).catch(() => done('inapp')); return; } } catch (x) {} done('inapp'); });
setInterval(() => { try { const C = S.cup; if (C && !C.done && !C.told && Date.now() >= C.dl) { C.told = 1; save(); notify('PhotoPicks', '🏆 Daily Cup results are in'); const c = document.getElementById('cupC'); if (c) c.outerHTML = cupCard(); } } catch (e) {} }, 5000);
function fcNotify() {""")
s = s.replace('</style>', """.tm-b{display:block;margin:8px auto 0;padding:7px 16px;border:0;border-radius:999px;background:none;box-shadow:inset 0 0 0 2px #D9AE4F;font:800 .86rem Nunito,system-ui;color:#F3D98B;cursor:pointer}
html body .nv.qw .qw-ph.out{width:56%!important;margin-left:auto!important;margin-right:auto!important}
.tm-on{margin:8px 0 0;text-align:center;font:700 .8rem Nunito,system-ui;color:#C9D3E6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v207 ok')
