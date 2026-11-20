# Real Money build, step 205 (after rmv201.py): honest money lines; simpler Stable cards; "Form" hidden.
#  Money:
#   - Final lobby: "6 × $2 = $12.00 · prizes $10.20 · PhotoPicks fee $1.80" (follows the entry you pick).
#   - Final result: a net line under the prize ("$2 entry · $5.00 net win") or "$2 entry · lost".
#   - Head-to-head setup: "You both pay $2 · winner takes $3.40 · PhotoPicks fee $0.60".
#  Stable:
#   - A photo that isn't race-ready shows ONE status line and ONE main button for its next step
#     (Vote to move it / Race the rematch / Train now), with training as a quiet second option and its training
#     score only once it has started. "Form" is hidden everywhere (it still works behind the scenes).
#   - One rosette rule on Stable and My Photos: the best rosette the photo has earned.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<p class="qf2-s">Each finalist pays $${fee}. Crowd votes decide the winners.</p>',
   '<p class="qf2-s">6 × $${fee} = <b>${money(6 * fee)}</b> · prizes <b>${money(fee * (QF_PAY[0] + QF_PAY[1]))}</b> · PhotoPicks fee ${money(6 * fee - fee * (QF_PAY[0] + QF_PAY[1]))}<br>Crowd votes decide the winners.</p>')
RA('<small>You both pay $${fee}. ${H2H_V} crowd votes decide it.</small>', '<small>You both pay $${fee} · PhotoPicks fee ${money(2 * fee - fee * H2H_PAY)} · ${H2H_V} crowd votes decide it.</small>')
RA("Head-to-head ${H.w}–${H.l} <i>•</i> Form +${p.form || 0}", "Head-to-head ${H.w}–${H.l}")
RA("<small>You · 💪 +${p.form || 0}</small>", "<small>You</small>")
RA("rz = (p.rz && p.rz[0]) || (H.w > 0) ? rosette(0) : rosette('f')", "rz = rosette(rzList(p).length ? rzList(p)[0] : 'f')")
s = s.replace("function fcNotify() {", r"""(() => { const qr = qfResult; qfResult = function (p, L, ord) { const r = qr.apply(this, arguments); try { const R = p.raced || {}, fee = R.fee || window.__qfFee || 2, box = document.querySelector('#coach.on .qfx .rv-won');
    const line = R.prize ? `$${fee} entry · <b>${money(R.prize - fee)}</b> net win` : `$${fee} entry · lost`;
    if (box) box.insertAdjacentHTML('afterend', `<p class="qr-net">${line}</p>`); else { const sp = document.querySelector('#coach.on .qfx .db-s'); if (sp) sp.insertAdjacentHTML('afterend', `<p class="qr-net">${line}</p>`); } } catch (e) {} return r; }; })();
function stTrain(p) { const q = p.ql, T = p.tq || { w: 0, l: 0 }, inQ = q && !q.done, w = rmqWait(p), rd = rmqReady(p), tr = T.w || T.l;
  const stt = inQ ? `🎀 Qualifying · ${Math.min(QS_STEPS, q.got || 0)} of ${QS_STEPS} steps` : rd || !w ? '🏁 Rematch ready' : `⏱ Free rematch in <span class="rm-t" data-until="${p.rmAt}">${rmqFmt(p.rmAt)}</span>`;
  const main = inQ ? '<button class="btn sx-nv" data-stv>⚖️ Vote to move it</button>' : rd || !w ? `<button class="btn sx-go" data-rmg="${p.id}">🏁 Race the rematch</button>` : `<button class="btn sx-nv" data-sth="${p.id}" data-m="t">🏋️ Train now · ${TQ_COST} coins</button>`;
  const alt = !inQ && !(rd || !w) ? '' : `<button class="sx-alt" data-sth="${p.id}" data-m="t">or train with coins · ${TQ_COST} a match</button>`;
  return `<div class="sx-card"><div class="sx-row"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><span class="sx-st">${stt}</span>${tr ? `<span class="sx-f">🏋️ Training ${T.w}–${T.l} · win ${TQ_WIN} before ${TQ_WIN} losses</span>` : ''}</div></div>
    <div class="sx-btns one">${main}</div>${alt}</div>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """.qf2-s b{color:#F3D98B}.qr-net{margin:6px 0 8px;text-align:center;font:italic 600 1.05rem Fraunces,Georgia,serif;color:#F3D98B}.qr-net b{font-style:normal}
html body .sx-btns.one{grid-template-columns:1fr;margin-top:12px}html body .sx-row .sx-f{font-size:.76rem;white-space:normal;border-radius:10px}
.sx-alt{display:block;margin:8px auto 0;border:0;background:none;font:700 .84rem Nunito,system-ui;color:#2E4F8A;text-decoration:underline;cursor:pointer}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v202 ok')
