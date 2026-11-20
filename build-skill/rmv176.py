# Real Money build, step 179 (after rmv175.py): from the owner's play-through.
#  - Sign-up comes after your first photo is framed: right after "Framed!", guests get "Save your photo" (with Later).
#  - Qualifier race slowed down: one crowd vote about every second, each shown with the voter ("🗳️ @coco.pup voted for
#    Landscape"), so you can watch it build.
#  - Prize up front: the qualifier race shows what's at stake ("🏆 Win and you're in the Nature & landscapes Final ·
#    1st wins up to $70"); the rivals screen leads with the Final's name and a big gold "1st wins $7.00" that follows the
#    entry you pick.
#  - Stale "Vote 10 times" wording replaced with the streak rule.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA(". Vote 10 times to start its qualifier: a live 2-horse race.", ". Vote 2 in a row with the crowd to move it; 3 steps start its qualifier: a live 2-horse race.")
RA("10 of your votes start a photo’s qualifier: a live 2-horse race.", "Vote 2 in a row with the crowd to move your photo; 3 steps start its qualifier: a live 2-horse race.")
RA("Enter another photo. 10 votes start its qualifier race.", "Enter another photo. Your voting streaks take it to its qualifier race.")
RA("Vote 10 times and it starts its qualifier: a live 2-horse race decided by the crowd.", "Your voting streaks take it to its qualifier: a live 2-horse race decided by the crowd.")
RA("Vote 10 times to start its qualifier race.", "Your voting streaks take it to the start of its qualifier race.")
# sign-up after the first framing
RA("$('#frvGo').onclick = () => { popClose(); setTimeout(done, 200); };",
   "$('#frvGo').onclick = () => { popClose(); if (S.user && S.user.guest && !S.suAsk) { S.suAsk = 1; save(); setTimeout(() => openSignup(() => setTimeout(done, 250), { locked: false, photo: 1 }), 250); return; } setTimeout(done, 200); };")
# slower race + voter line + stake banner
RA("}), 500); }, 380); }; qrCount", "}), 500); }, 1000); }; qrCount")
RA("$('#qrN').textContent = `${A + B} votes in`;", "$('#qrN').textContent = `${A + B} votes in`; { const v = document.getElementById('qrV'); if (v) { const vh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)], me = seq[i - 1]; v.innerHTML = `🗳️ <b>${vh}</b> voted for <b class=\"${me ? 'me' : ''}\">${esc(me ? rcName(p) : o.t)}</b>`; v.classList.remove('pop'); void v.offsetWidth; v.classList.add('pop'); } }")
RA('<p class="qr-n" id="qrN">0 votes in</p>', '<p class="qr-v" id="qrV">🗳️ Waiting for the first vote…</p><p class="qr-n" id="qrN">0 votes in</p>')
RA("<p class=\"qr-s\">First to ${QR_WIN} votes goes to the Final</p>", "<div class=\"qr-stake\">🏆 Win and you’re in the <b>${esc(showName(photoShow(p) || 'pets'))} Final</b><small>1st wins up to <b>${money(20 * QF_PAY[0])}</b> · first to ${QR_WIN} votes</small></div>")
# rivals screen: prize first
RA('<h2 class="db-h">Your rivals</h2>', '<h2 class="db-h qfp-h">${esc(showName(k))} Final</h2><div class="qfp-win"><span>1st wins</span><b>${money(fee * QF_PAY[0])}</b><small>2nd ${money(fee * QF_PAY[1])} · ${fee === 2 ? "up to $70 at a $20 entry" : `$${fee} entry`}</small></div><p class="qfp-k">Your 5 rivals</p>')
s = s.replace('</style>', """.qr-stake{margin:2px 0 10px;padding:10px 12px;border-radius:14px;background:#FFF8E6;box-shadow:inset 0 0 0 2px #D9AE4F;font:800 .95rem/1.3 Nunito,system-ui;color:#5B3D06}.qr-stake b{color:#14213D}.qr-stake small{display:block;margin-top:2px;font:700 .8rem Nunito,system-ui;color:#5B4A3F}.qr-stake small b{color:#2F6B3F}
.qr-v{margin:6px 0 0;min-height:1.4em;font:700 .9rem Nunito,system-ui;color:#3D4A5C}.qr-v b{color:#14213D}.qr-v b.me{color:#9A6B12}.qr-v.pop{animation:qmFl .35s ease-out both}
.qfp-h{margin-bottom:4px!important}.qfp-win{margin:0 0 12px;padding:12px;border-radius:16px;background:linear-gradient(180deg,#22325A,#14213D);box-shadow:0 0 0 2px #D9AE4F,0 6px 18px rgba(20,33,61,.25);color:#C9D3E6}
.qfp-win span{display:block;font:900 .72rem Nunito,system-ui;letter-spacing:.1em;text-transform:uppercase;color:#F3D98B}.qfp-win b{display:block;font:900 2.6rem/1.05 Fraunces,Georgia,serif;color:#F3D98B}.qfp-win small{font:700 .82rem Nunito,system-ui}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v176 ok')
# pass 2: small label no longer repeats the title; safe fallback if a photo has no show category
s = open(d + 'yofi-real.html').read()
RA('<p class="pp-k">🏁 ${esc(showName(k))} Final · 6 photos</p>', '<p class="pp-k">🏁 6-photo race · live crowd vote</p>')
RA('<h2 class="db-h qfp-h">${esc(showName(k))} Final</h2>', '<h2 class="db-h qfp-h">${k ? esc(showName(k)) + " Final" : "The Final"}</h2>')
open(d + 'yofi-real.html', 'w').write(s); print('rm v176 pass2 ok')
