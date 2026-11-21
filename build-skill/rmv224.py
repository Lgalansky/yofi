# Real Money build, step 227 (after rmv223.py): Option 1 + first Final free (user choice).
#  - Final lobby: a player's first Final entry is free (no coins, no cash). The entry picker, fee maths and coin offer
#    are hidden; one button "🎟️ Enter free · your first Final" (account required). From the second Final the $2–$20 picker returns.
#  - Final result: one button "🐎 See <name> in your stable" (+ "Back to voting" link). Free entries say "Free entry".
#  - Stable opens with a "🏁 Final complete" note, scrolled to that photo; its ladder now includes "🏁 Final · 4th".
#  - The 250-coin free-entry offer is retired (coins sheet row, Welcome back line).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("if (!S.coinFin) rows.push(row('🎟️', 'Free Final entry'", "if (false) rows.push(row('🎟️', 'Free Final entry'", 2)
RA("`Your first Final is free with ${FIN_COINS} coins`", "'Your first Final is free'")
RA("function fcNotify() {", r"""(() => { const qp = qfPick; qfPick = function (p, fee) { if (S.coinFin) return qp.apply(this, arguments); const r = qp.call(this, p, 2); try { const box = document.querySelector('#coach.on .qf2'); if (!box) return r; const gone = x => x && x.parentNode && x.parentNode.removeChild(x);
    const rules = box.querySelectorAll('.nv-rule'); if (rules[1]) gone(rules[1]); ['.qf2-f', '.qf2-s', '#qfpCoin', '.nv-coinp', '.qf2-free'].forEach(q => box.querySelectorAll(q).forEach(gone));
    const sim = box.querySelector('.nv-sim'); if (sim) sim.textContent = 'Demo · other finalists simulated';
    const go = document.getElementById('qfpGo'); if (!go) return r; go.insertAdjacentHTML('beforebegin', `<p class="qf2-fr">🎟️ <b>Your first Final is free</b><small>No entry fee · 1st wins ${money(2 * QF_PAY[0])} cash</small></p>`);
    go.textContent = '🎟️ Enter free · your first Final';
    go.onclick = () => { if (S.user && S.user.guest) { popClose(); openSignup(() => setTimeout(() => qfPick(p, 2), 250), { locked: false, photo: 1, fin: 1 }); return; }
      S.coinFin = 1; save(); window.__qfFee = 2; window.__qfFree = 1; popClose(); const R = qfRivals(p); setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(R)), 250); }; } catch (e) {} return r; }; })();
(() => { const qr = qfResult; qfResult = function (p) { const free = window.__qfFree; window.__qfFree = 0; const r = qr.apply(this, arguments); try { const box = document.querySelector('#coach.on .qfx') || document.querySelector('#coach.on'); if (!box) return r; const gone = x => x && x.parentNode && x.parentNode.removeChild(x);
    if (free) { const w = document.createTreeWalker(box, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) n.nodeValue = n.nodeValue.replace(/\$2 entry/g, 'Free entry'); } const Rr = p.raced || {}; if (free) [...box.querySelectorAll('p,div,span')].filter(e => /^Free entry ·/.test(e.textContent.trim()) && e.textContent.length < 60).forEach(host => { host.innerHTML = Rr.prize ? `Free entry · <b>${money(Rr.prize)}</b> won` : 'Free entry · no prize this time'; });
    box.querySelectorAll('.btn').forEach(gone); gone(box.querySelector('.rn-end')); const R = p.raced || {}, nm = esc(rcName(p)), J = document.getElementById('qrJ');
    const html = `<button class="btn block nv-go" id="qrS">🐎 See ${nm} in your stable</button>`; if (J && J.parentNode) J.parentNode.insertAdjacentHTML('beforebegin', html); else box.insertAdjacentHTML('beforeend', html);
    document.getElementById('qrS').onclick = () => { popClose(); window.__stFocus = p.id; window.__stNote = `🏁 Final complete · ${ppOrd(R.rank || 0)}${R.prize ? ` · won ${money(R.prize)}` : ''} · ${nm}’s run is on your trophy wall`; finalsTab(); };
    if (J) J.onclick = () => { popClose(); go('judge'); renderJudge(); }; } catch (e) {} return r; }; })();
(() => { const ft = finalsTab; finalsTab = function () { const r = ft.apply(this, arguments); try { const note = window.__stNote, id = window.__stFocus; window.__stNote = null; window.__stFocus = null; if (!note) return r;
    const sub = document.querySelector('#flow .sx .sx-sub'); if (sub) sub.insertAdjacentHTML('afterend', `<p class="st-note">${note}</p>`);
    const p = (S.photos || []).find(x => x.id === id); if (p) setTimeout(() => { const c = [...document.querySelectorAll('#flow .sx-hero, #flow .sx-card')].find(e => { const im = e.querySelector('img'); return im && im.getAttribute('src') === p.src; }); if (c) { c.scrollIntoView({ behavior: 'smooth', block: 'start' }); c.classList.add('st-hl'); } }, 350); } catch (e) {} return r; }; })();
(() => { const sl = stLadder; stLadder = function (p) { let h = sl.apply(this, arguments); try { if (p && p.raced) { const R = p.raced; h = h.replace('<div class="ld goal', `<div class="ld d"><i>🏁</i><div><b>Final · ${ppOrd(R.rank)}</b><small>${R.prize ? `Won ${money(R.prize)}` : 'Run complete · rosette on the frame'}</small></div></div><div class="ld goal`); } } catch (e) {} return h; }; })();
function fcNotify() {""")
s = s.replace('</style>', """.qf2-fr{margin:14px 0 26px;padding:14px;border-radius:18px;text-align:center;background:linear-gradient(180deg,#FBF3DC,#F3D98B);color:#14213D;font:900 1.2rem Fraunces,Georgia,serif}.qf2-fr b{display:block;color:#14213D}.qf2-fr small{display:block;margin-top:3px;font:700 .9rem Nunito,system-ui;color:#5B4A3F}
.st-note{margin:6px 14px 10px;padding:9px 12px;border-radius:12px;background:#14213D;color:#F3D98B;font:800 .85rem Nunito,system-ui;text-align:center}
.st-hl{animation:stHl 2.2s ease-out}@keyframes stHl{0%{box-shadow:0 0 0 0 rgba(217,174,79,.9)}40%{box-shadow:0 0 0 8px rgba(217,174,79,.45)}100%{box-shadow:0 0 0 0 rgba(217,174,79,0)}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v224 ok')
