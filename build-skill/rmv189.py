# Real Money build, step 192 (after rmv188.py): from the newbie play-through.
#  1. First Final free: a player's first Final is a free $2 entry (1st wins $7). Lobby shows "🎁 Your first Final is
#     free" and the button "Enter the final · FREE"; no cash or account needed for that one.
#  2. Votes feel connected: while a photo is qualifying, the pairs you vote on come from that photo's category.
#  3. No daily-rewards popup until the player's first qualifier race is done (the 🔥 button still opens it).
#  Also: finalist card says "Your Final is waiting" (one step, not a second promotion).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("<div><b>Into the Final!</b><small>Pick your entry ($2–$20) · 1st wins up to ${money(20 * QF_PAY[0])}</small></div>",
   "<div><b>Your Final is waiting</b><small>${S.fin1 ? `Pick your entry ($2–$20) · 1st wins up to ${money(20 * QF_PAY[0])}` : '🎁 Your first Final is free · 1st wins $7.00'}</small></div>")
s = s.replace("function fcNotify() {", r"""(() => { const qp = qfPick; qfPick = function (p, fee) { const free = !S.fin1; if (free) fee = 2; const r = qp.call(this, p, fee); if (!free) return r;
  try { const box = document.querySelector('.qf2-win'); if (box) box.insertAdjacentHTML('afterend', '<p class="qf2-free">🎁 Your first Final is free · a $2 entry on us</p>');
    document.querySelectorAll('.qf2-f button').forEach(b => { if (b.dataset.qff !== '2') { b.disabled = true; b.classList.add('lk'); } });
    const s2 = document.querySelector('.qf2-s'); if (s2) s2.textContent = 'Higher entries unlock after your first Final. Crowd votes decide the winners.';
    const g = $('#qfpGo'); g.textContent = 'Enter the final · FREE';
    g.onclick = () => { S.fin1 = 1; save(); window.__qfFee = 2; popClose(); const R = qfRivals(p); setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(R)), 250); }; } catch (e) {} return r; }; })();
(() => { const sp = seedPair; seedPair = function () { const r = sp.apply(this, arguments); try { if (window.__finPair) return r; const t = qsTarget(); if (!t) return r; const k = photoShow(t) || finCatOf(t); if (!k) return r;
  if (r && r[0] && finCatOf(r[0]) === k && r[1] && finCatOf(r[1]) === k) return r;
  const L = ppShuffle(SEED.filter(x => x.src && finCatOf(x) === k && x.src !== t.src), Math.random); if (L.length >= 2) return [L[0], L[1]]; } catch (e) {} return r; }; })();
(() => { const sh = streakHello; streakHello = function () { if (!(S.photos || []).some(p => p.ql && p.ql.done)) return; return sh.apply(this, arguments); }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.qf2-free{margin:-4px 0 10px;padding:8px 12px;border-radius:12px;background:rgba(63,194,90,.15);box-shadow:inset 0 0 0 1.5px #3FC25A;font:800 .95rem Nunito,system-ui;color:#9FE3AE}
html body .qf2-f button.lk{opacity:.4}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v189 ok')
# pass 2: live-Final pairs also follow your photo's category while it's qualifying
s = open(d + 'yofi-real.html').read()
RA("try { if (window.__finPair) return r; const t = qsTarget();", "try { const t = qsTarget();")
RA("if (L.length >= 2) return [L[0], L[1]]; } catch (e) {} return r; }; })();", "if (L.length >= 2) { window.__finPair = false; return [L[0], L[1]]; } } catch (e) {} return r; }; })();")
open(d + 'yofi-real.html', 'w').write(s); print('rm v189 pass2 ok')
