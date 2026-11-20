# Real Money build, step 220 (after rmv216.py): fewer words on the Vote card and the coins sheet.
#  - Vote card: photo name, the route track (🎀 qualifier race, 🏁 Final) and one short goal line with the streak dots.
#    Removed: status badge, coins chip, labels row, "1 more for a step!" text, swipe instructions.
#  - Coins sheet: big balance, then one row per thing coins buy, each with its cost and a button:
#    Daily Cup (100) · free Final entry (250, once) · train a photo (50 a match) · invite a friend (+100). "Vote to earn more" at the bottom.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("function fcNotify() {", r"""function pvStep(p, s, fin) { s = Math.min(QS_STEPS, s || 0); const idx = fin ? QS_STEPS + s : s, N = QS_STEPS * 2, pos = idx / N, k = S.stk || 0, live = !fin && p.ql && p.ql.live, left = QS_STEPS - s;
  const node = i => { const x = i / N * 100, cp = i === QS_STEPS || i === N, done = i <= idx;
    return cp ? `<span class="jc ${done ? 'd' : ''}" style="left:${x}%">${i === N ? '🏁' : '🎀'}</span>` : i ? `<i class="jn ${done ? 'd' : ''} ${i > QS_STEPS ? 'g' : ''}" style="left:${x}%"></i>` : ''; };
  const goal = live ? '🔴 Race live now' : fin ? (left <= 0 ? '🏁 Final ready' : `${left} step${left === 1 ? '' : 's'} to 🏁 Final`) : left <= 0 ? '🎀 Race starting' : `${left} step${left === 1 ? '' : 's'} to 🎀 race`;
  return `<div class="pv-tr jr ${fin ? 'fin' : ''}"><div class="pv-rail"><u style="width:${pos * 100}%"></u>${Array.from({ length: N + 1 }, (_, i) => node(i)).join('')}</div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"></div>
    <div class="pv-k jk"><b class="jg">${goal}</b><span class="pv-dots" title="2 good votes in a row = 1 step">${Array.from({ length: QS_RUN }, (_, i) => `<i class="${i < k ? 'on' : i === QS_RUN - 1 && k === QS_RUN - 1 ? 'next' : ''}"></i>`).join('')}</span></div>`; }
(() => { const pc = pvCard; pvCard = function (p) { let h = pc.apply(this, arguments); try { if (!h.includes('pv-tr jr')) h = h.replace(/<span class="pv-st">[\s\S]*?<\/span>/, '').replace(/<em>🟡[^<]*<\/em>/, '').replace(/<small>A new live race for a place in the Final<\/small>/, '').replace('Its rematch is ready!', '🏁 Rematch ready').replace(/<small>Pick your entry[^<]*<\/small>/, '').replace('🏁 Meet your finalists &amp; race', '🏁 Race your Final').replace('🏁 Meet your finalists & race', '🏁 Race your Final'); if (h.includes('pv-tr jr')) { h = h.replace(/<span class="pv-st">[\s\S]*?<\/span>/, '').replace(/<em>🟡[^<]*<\/em>/, '').replace(/<em>[^<]*<\/em>(\s*<\/div>)/, '$1');
      h = h.replace(/<p class="pv-who">[\s\S]*?<\/p>/, '<p class="pv-who"><span class="w">👉 Swipe to move this one</span></p>'); } } catch (e) {} return h; }; })();
function coinSheet() { const g = Math.floor(S.gems || 0), P = S.photos || [], R = P.filter(p => isCashOK(p) && !p.starter), T = P.filter(p => !isCashOK(p) && p.ql && p.ql.done === 'x').slice(0, 2), cs = (() => { try { return cupSt(); } catch (e) { return 'open'; } })();
  const row = (ic, t, cost, btn) => `<div class="cs-r"><span class="cs-ic">${ic}</span><div><b>${t}</b><small>${cost}</small></div>${btn}</div>`;
  const b = (lab, attr, off) => `<button class="btn cs-b ${off ? 'off' : ''}" ${attr} ${off ? 'disabled' : ''}>${lab}</button>`;
  const fin = P.find(p => p.fin && p.fr && p.fr.go), need = n => `${n - g} more`;
  const rows = [row('🏆', 'Daily Cup', `${CUP_COST} coins · $100 prizes`, cs === 'in' ? '<em class="cs-ok">✓ Entered</em>' : cs === 'ready' ? b('Results', 'data-cs="cupres"') : !R.length ? '<em class="cs-no">Qualify first</em>' : g < CUP_COST ? `<em class="cs-no">${need(CUP_COST)}</em>` : b('Enter', 'data-cs="cup"'))];
  if (!S.coinFin) rows.push(row('🎟️', 'Free Final entry', `${FIN_COINS} coins · once`, g < FIN_COINS ? `<em class="cs-no">${need(FIN_COINS)}</em>` : fin ? b('Use', `data-cs="fin" data-pid="${fin.id}"`) : '<em class="cs-ok">✓ Ready</em>'));
  T.forEach(p => rows.push(row(`<img src="${p.src}" alt="">`, `Train ${esc(rcName(p))}`, `${TQ_COST} coins a match · ${(p.tq || { w: 0 }).w}/${TQ_WIN} wins`, g < TQ_COST ? `<em class="cs-no">${need(TQ_COST)}</em>` : b('Train', `data-cs="trn" data-pid="${p.id}"`))));
  rows.push(row('👥', 'Invite a friend', '+100 coins each', b('Invite', 'data-cs="inv"')));
  openSheet(`<div class="trc t2 cs"><button class="t2-x" data-csx aria-label="Close">✕</button><p class="cs-k">Your coins</p><div class="cs-bal"><span>🪙</span>${g.toLocaleString()}</div>
    <div class="cs-l">${rows.join('')}</div><button class="btn block cs-v" data-cs="vote">⚖️ Vote to earn more</button><p class="cs-f">Coins are earned, never sold.</p></div>`);
  const close = () => { try { closeSheet(); } catch (e) {} };
  document.querySelectorAll('[data-csx]').forEach(x => x.onclick = close);
  document.querySelectorAll('#sheet [data-cs]').forEach(x => x.onclick = () => { const k = x.dataset.cs, p = P.find(y => y.id === x.dataset.pid); close();
    setTimeout(() => { if (k === 'cup') { cupEnter(); if (S.cup && !S.cup.done && !document.querySelector('#coach.on, #sheet.on')) finalsTab(); } else if (k === 'cupres') cupFinish(); else if (k === 'fin') qfStart(p); else if (k === 'trn') h2hOpen(p, 0); else if (k === 'inv') inviteSheet(); else if (k === 'vote') { try { closeFlow(); } catch (e) {} go('judge'); renderJudge(); } }, 220); }); }
useGems = coinSheet;
function fcNotify() {""")
s = s.replace('</style>', """html body #qlS .pv-k.jk{flex-wrap:nowrap;justify-content:space-between;margin-top:2px}html body #qlS .pv-k.jk .jg{order:0;flex:1;flex-basis:auto;font:800 .95rem Nunito,system-ui;color:#14213D}
html body #qlS .jl,html body #qlS .pv-1m{display:none!important}.pv-c .pv-t{min-height:24px}
html body #qlS #pvS{align-items:flex-start}html body #qlS .pv-fn{display:flex;align-items:center;gap:10px;margin:8px 0 0}html body #qlS .pv-fn img{width:46px!important;height:46px!important;flex:none;border-radius:12px}html body #qlS .pv-fn b{font:800 1rem Nunito,system-ui!important;color:#14213D}html body #qlS .pv-fn small{font:600 .8rem Nunito,system-ui}html body #qlS .pv-c .btn.pv-go{min-height:44px!important;margin-top:10px!important;font-size:.98rem!important}html body #sheet .trc.cs{border-top:0!important}
.cs .cs-k{margin:2px 0 0;text-align:center;font:800 .74rem Nunito,system-ui;letter-spacing:.12em;text-transform:uppercase;color:#F3D98B}
.cs .cs-bal{display:flex;align-items:center;justify-content:center;gap:8px;margin:2px 0 14px;font:900 2.6rem/1 Fraunces,Georgia,serif;color:#FBF3DC}.cs .cs-bal span{font-size:2rem}
.cs .cs-l{display:grid;gap:8px}.cs .cs-r{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 1.5px rgba(217,174,79,.55)}
.cs .cs-ic{flex:none;width:40px;height:40px;display:grid;place-items:center;border-radius:12px;background:rgba(217,174,79,.15);font-size:1.4rem;overflow:hidden}.cs .cs-ic img{width:100%;height:100%;object-fit:cover}
.cs .cs-r>div{flex:1;min-width:0}.cs .cs-r b{display:block;font:800 1rem Nunito,system-ui;color:#FBF3DC;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cs .cs-r small{font:600 .8rem Nunito,system-ui;color:#C9D3E6}
html body #sheet .cs .btn.cs-b{flex:none;min-width:84px;min-height:40px!important;margin:0!important;padding:0 14px!important;border-radius:999px!important;background:linear-gradient(180deg,#F3D98B,#D9AE4F)!important;color:#14213D!important;font:900 .92rem Nunito,system-ui!important;box-shadow:none!important}
.cs .cs-ok{flex:none;font:800 .86rem Nunito,system-ui;font-style:normal;color:#8FD49E}.cs .cs-no{flex:none;font:700 .82rem Nunito,system-ui;font-style:normal;color:#8C9AB5}
html body #sheet .cs .btn.cs-v{margin:14px 0 4px!important;min-height:50px!important;border-radius:999px!important;background:linear-gradient(180deg,#2F7A3F,#1E5C2E)!important;color:#fff!important;font:900 1rem Nunito,system-ui!important}
.cs .cs-f{margin:4px 0 0;text-align:center;font:600 .74rem Nunito,system-ui;color:#8C9AB5}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v217 ok')
