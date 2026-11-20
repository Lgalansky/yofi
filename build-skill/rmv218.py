# Real Money build, step 221 (after rmv217.py): coins sheet buttons carry the cost.
#  - Each row: what it is + what you get on the left; the button on the right shows the coin cost ("🪙 100").
#  - Short of coins: the cost button is greyed and the line under the title says how many more.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""function coinSheet() { const g = Math.floor(S.gems || 0), P = S.photos || [], R = P.filter(p => isCashOK(p) && !p.starter), T = P.filter(p => !isCashOK(p) && p.ql && p.ql.done === 'x').slice(0, 2), cs = (() => { try { return cupSt(); } catch (e) { return 'open'; } })();
  const fin = P.find(p => p.fin && p.fr && p.fr.go), more = n => `<u>${n - g} more coins</u>`;
  const row = (ic, t, sub, btn) => `<div class="cs-r"><span class="cs-ic">${ic}</span><div><b>${t}</b><small>${sub}</small></div>${btn}</div>`;
  const cost = (n, attr, ok) => `<button class="btn cs-b ${ok ? '' : 'off'}" ${attr} ${ok ? '' : 'disabled'}>🪙 ${n}</button>`;
  const rows = [row('🏆', 'Daily Cup', cs === 'in' ? 'You’re in tonight’s Cup' : !R.length ? 'Qualify a photo to enter' : g < CUP_COST ? more(CUP_COST) : '$100 in prizes tonight',
    cs === 'in' ? '<em class="cs-ok">✓ Entered</em>' : cs === 'ready' ? '<button class="btn cs-b" data-cs="cupres">Results</button>' : cost(CUP_COST, 'data-cs="cup"', R.length && g >= CUP_COST))];
  if (!S.coinFin) rows.push(row('🎟️', 'Free Final entry', g < FIN_COINS ? more(FIN_COINS) : fin ? 'Use it in your Final now' : 'Use it in your next Final', g >= FIN_COINS && !fin ? '<em class="cs-ok">✓ Ready</em>' : cost(FIN_COINS, fin ? `data-cs="fin" data-pid="${fin.id}"` : '', g >= FIN_COINS && fin)));
  T.forEach(p => rows.push(row(`<img src="${p.src}" alt="">`, `Train ${esc(rcName(p))}`, g < TQ_COST ? more(TQ_COST) : `${(p.tq || { w: 0 }).w}/${TQ_WIN} wins to cash races`, cost(TQ_COST, `data-cs="trn" data-pid="${p.id}"`, g >= TQ_COST))));
  rows.push(row('👥', 'Invite a friend', 'You both get 100 coins', '<button class="btn cs-b" data-cs="inv">+🪙 100</button>'));
  openSheet(`<div class="trc t2 cs"><button class="t2-x" data-csx aria-label="Close">✕</button><p class="cs-k">Your coins</p><div class="cs-bal"><span>🪙</span>${g.toLocaleString()}</div>
    <div class="cs-l">${rows.join('')}</div><button class="btn block cs-v" data-cs="vote">⚖️ Vote to earn more</button><p class="cs-f">Coins are earned, never sold.</p></div>`);
  const close = () => { try { closeSheet(); } catch (e) {} };
  document.querySelectorAll('[data-csx]').forEach(x => x.onclick = close);
  document.querySelectorAll('#sheet [data-cs]').forEach(x => x.onclick = () => { const k = x.dataset.cs, p = P.find(y => y.id === x.dataset.pid); close();
    setTimeout(() => { if (k === 'cup') { cupEnter(); if (S.cup && !S.cup.done && !document.querySelector('#coach.on, #sheet.on')) finalsTab(); } else if (k === 'cupres') cupFinish(); else if (k === 'fin') qfStart(p); else if (k === 'trn') h2hOpen(p, 0); else if (k === 'inv') inviteSheet(); else if (k === 'vote') { try { closeFlow(); } catch (e) {} go('judge'); renderJudge(); } }, 220); }); }
function fcNotify() {""")
s = s.replace('</style>', """html body #sheet .cs .btn.cs-b{min-width:92px;font-size:1rem!important}html body #sheet .cs .btn.cs-b.off{background:rgba(255,255,255,.12)!important;color:#8C9AB5!important}.cs .cs-r small u{text-decoration:none;color:#F3D98B}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v218 ok')
