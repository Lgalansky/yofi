# Real Money build, step 145 (after rmv141.py): Stage 5 — daily photo contests (no sponsors).
#  Every day, for each live category (Pets, Nature & landscapes), two contests that close at midnight:
#  - Free daily: free entry, guaranteed prizes 1st $10 · 2nd $6 · 3rd $4 (from PhotoPicks' prize budget).
#  - $2 Cash daily: prize pool = 85% of entries; top 10% paid (1st 20%, 2nd 12%, 3rd 8%, rest share 60%).
#  One entry per photo per contest; starter photos can't enter. The crowd's votes decide; live position on My Photos
#  ("12th of 340 · top 34 paid"). At the result: prize to cash, rosette for top 3 (hung on the frame).
#  Entry points: "Today's contests" card on My Photos and the Play tab, and "Enter today's contest" on a verdict.
#  Simulated: entrant numbers and rankings. Demo: results 10 minutes after entering (labelled).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("${earnHeadHTML()}", "${earnHeadHTML()}${ctCardHTML()}", 2)
RA("<h1 class=\"fn-h\">Play</h1><p class=\"fn-s\">Race real players on the same photo pairs. Your eye against theirs.</p>${gmCardsHTML()}",
   "<h1 class=\"fn-h\">Play</h1><p class=\"fn-s\">Race real players on the same photo pairs. Your eye against theirs.</p>${gmCardsHTML()}${ctCardHTML()}")
RA("<button class=\"btn block db-go\" id=\"vdVote\">⚖️ Vote to move it up</button>",
   "${p.starter ? '' : '<button class=\"btn block db-go cashb\" id=\"vdCt\">🏆 Enter today’s contest</button>'}<button class=\"btn block db-go\" id=\"vdVote\">⚖️ Vote to move it up</button>")
RA("$('#vdVote').onclick = () => { popClose(); go('judge'); renderJudge(); };",
   "$('#vdVote').onclick = () => { popClose(); go('judge'); renderJudge(); }; if ($('#vdCt')) $('#vdCt').onclick = () => { popClose(); setTimeout(() => ctOpen(photoShow(p), p.id), 200); };")
s = s.replace("function fcNotify() {", r"""const CT_DEMO = 10 * 60e3, CT_FREE = [10, 6, 4];
const ctDay = () => new Date().toDateString();
const ctLeft = () => { const m = new Date(); m.setHours(24, 0, 0, 0); const r = m - Date.now(); return `${Math.floor(r / 3600e3)}h ${Math.floor(r / 60e3) % 60}m`; };
function ctN(cat, tier) { const r = cpRng(ppHash(ctDay() + cat + tier)), h = new Date().getHours() + new Date().getMinutes() / 60; return Math.round((tier === 'f' ? 700 : 120) * (0.35 + h / 24) * (0.85 + r() * .3)); }
function ctPool(n) { return +(n * 2 * .85).toFixed(2); }
function ctPrize(tier, n, rank) { if (tier === 'f') return CT_FREE[rank - 1] || 0; const pool = ctPool(n), paid = Math.max(3, Math.floor(n / 10));
  if (rank > paid) return 0; if (rank <= 3) return +(pool * [.2, .12, .08][rank - 1]).toFixed(2); return +(pool * .6 / (paid - 3)).toFixed(2); }
function ctTable(tier, n) { if (tier === 'f') return `1st <b>$10</b> · 2nd <b>$6</b> · 3rd <b>$4</b> · guaranteed`; const paid = Math.max(3, Math.floor(n / 10));
  return `1st <b>${money(ctPrize('c', n, 1))}</b> · 2nd <b>${money(ctPrize('c', n, 2))}</b> · 3rd <b>${money(ctPrize('c', n, 3))}</b> · 4th–${paid}th <b>${money(ctPrize('c', n, 4))}</b>`; }
function ctRank(e, final) { const p = (S.photos || []).find(x => x.id === e.pid), pct = (p && p.vd && p.vd.pct) || 58, r = cpRng(ppHash(e.k + e.pid)), base = pct + (r() - .5) * 22;
  const drift = final ? 0 : (cpRng(ppHash(e.k + Math.floor(Date.now() / 120000)))() - .5) * 8, sc = base + drift, q = Math.max(.002, Math.min(.98, 1 - (sc - 42) / 44));
  return Math.max(1, Math.min(e.n, Math.round(e.n * q * (final && r() < .12 ? .02 : 1)))); }
function ctEntries() { return Object.values(S.ct || {}); }
function ctCardHTML() { if (!S || !(S.photos || []).some(p => p.framed && !p.starter) && !(S.photos || []).length) return `<div class="ctc"><p class="ctc-k">🏆 Today’s photo contests</p><p class="ctc-s">Enter your best photo free. The crowd’s votes decide. Closes in ${ctLeft()}.</p><div class="ctc-g">${SHOW_ROT.map(z => `<button data-ct="${z.k}"><b>${SHOW_IC[z.k] || '🎀'} ${esc(z.n)}</b><small>Free · $20 prizes · ${money(ctPool(ctN(z.k, 'c')))} cash contest</small></button>`).join('')}</div></div>`;
  const mine = ctEntries().filter(e => !e.done && e.day === ctDay());
  return `<div class="ctc"><p class="ctc-k">🏆 Today’s photo contests · closes in ${ctLeft()}</p>${mine.map(e => { const p = (S.photos || []).find(x => x.id === e.pid), rk = ctRank(e), paid = e.tier === 'f' ? 3 : Math.max(3, Math.floor(e.n / 10));
      return `<div class="ctc-e ${rk <= paid ? 'ok' : ''}"><img src="${p ? p.src : ''}" alt=""><span><b>${esc(p ? rcName(p) : 'Your photo')} · ${e.tier === 'f' ? 'Free' : '$2'} ${esc(showName(e.cat))}</b><small>Now <b>${ppOrd(rk)}</b> of ${e.n} · top ${paid} paid${rk <= paid ? ` · would win ${money(ctPrize(e.tier, e.n, rk))}` : ''}</small></span></div>`; }).join('')}
    <div class="ctc-g">${SHOW_ROT.map(z => `<button data-ct="${z.k}"><b>${SHOW_IC[z.k] || '🎀'} ${esc(z.n)}</b><small>Free · $20 prizes · ${money(ctPool(ctN(z.k, 'c')))} cash contest</small></button>`).join('')}</div></div>`; }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-ct]'); if (b) { e.preventDefault(); try { closeFlow(); } catch (x) {} ctOpen(b.dataset.ct); } });
function ctOpen(cat, pid0) { cat = cat || SHOW_ROT[0].k; const P = (S.photos || []).filter(p => p.framed && !p.starter && photoShow(p) === cat); let pid = pid0 && P.some(p => p.id === pid0) ? pid0 : (P[0] || {}).id;
  const draw = () => { const nf = ctN(cat, 'f'), nc = ctN(cat, 'c'), has = t => !!(S.ct || {})[ctDay() + cat + t + pid];
    popOpen(`<div class="pp ctx"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">🏆 Today’s ${esc(showName(cat))} contests</p><h2 class="db-h">Best ${esc(showName(cat))} photo</h2>
      <p class="db-s">The crowd’s votes decide. Closes in <b>${ctLeft()}</b>.</p>
      ${P.length ? `<p class="ct-l">Your photo</p><div class="ct-ph">${P.map(p => `<button data-ctp="${p.id}" class="${p.id === pid ? 'on' : ''}"><img src="${p.src}" alt=""><small>${esc(rcName(p))}${p.vd ? ` · ${p.vd.pct}%` : ''}</small></button>`).join('')}</div>` : `<p class="ct-none">You need a framed ${esc(showName(cat))} photo to enter.</p>`}
      <div class="ct-t"><div><b>🎟️ Free daily</b><small>${nf} entries · ${ctTable('f', nf)}</small></div>${P.length ? (has('f') ? '<em>Entered ✓</em>' : '<button class="btn db-go" id="ctF">Enter free</button>') : ''}</div>
      <div class="ct-t cash"><div><b>💵 $2 cash daily</b><small>${nc} entries · <b>${money(ctPool(nc))}</b> prize pool · top 10% paid<br>${ctTable('c', nc)}</small></div>${P.length ? (has('c') ? '<em>Entered ✓</em>' : '<button class="btn db-go cashb" id="ctC">Enter · $2</button>') : ''}</div>
      ${P.length ? '' : '<button class="btn block db-go" id="ctUp">📷 Add a photo</button>'}
      <p class="db-sim">15% PhotoPicks fee on cash entries · Starter photos can’t enter · Demo: results about 10 min after entering</p></div>`);
    document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose());
    document.querySelectorAll('#coach [data-ctp]').forEach(b => b.onclick = () => { pid = b.dataset.ctp; window.__keepScroll = 1; draw(); });
    if ($('#ctUp')) $('#ctUp').onclick = () => { popClose(); setTimeout(finPick, 200); };
    const enter = tier => { const k = ctDay() + cat + tier + pid; S.ct = S.ct || {}; S.ct[k] = { k, cat, tier, pid, day: ctDay(), at: Date.now(), n: tier === 'f' ? nf : nc }; save(); toast(tier === 'f' ? '🏆 Entered free · the crowd decides' : '🏆 Entered the $2 contest'); window.__keepScroll = 1; draw(); };
    if ($('#ctF')) $('#ctF').onclick = () => enter('f');
    if ($('#ctC')) $('#ctC').onclick = () => needAge(() => { popClose(); payCash(2, 'A $2 photo contest entry', () => setTimeout(() => { enter('c'); }, 250)); }); };
  draw(); }
function ctResult(e) { e.done = 1; const rk = ctRank(e, true), prize = ctPrize(e.tier, e.n, rk), p = (S.photos || []).find(x => x.id === e.pid); e.rank = rk; e.prize = prize;
  if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); try { earnAdd({ kind: 'c', pid: e.pid, t: p ? p.title : '', amt: prize, place: rk }); } catch (x) {} } if (p && rk <= 3) rzAdd(p, rk - 1); save(); window.__nudgeAt = Date.now();
  const paid = e.tier === 'f' ? 3 : Math.max(3, Math.floor(e.n / 10));
  popOpen(`<div class="pp"><p class="pp-k">🏆 ${e.tier === 'f' ? 'Free' : '$2'} ${esc(showName(e.cat))} contest · result</p><h2 class="db-h">${esc(p ? rcName(p) : 'Your photo')} finished ${ppOrd(rk)} of ${e.n}</h2>
    <div class="re-ok">${p ? `<img src="${p.src}" alt="">` : ''}${rk <= 3 ? `<i class="re-rz">${rosette(rk - 1)}</i>` : ''}</div>
    ${prize ? `<div class="rv-won"><span>Cash won</span><b>${money(prize)}</b></div>` : `<p class="db-s">Top ${paid} were paid. ${rk <= paid * 2 ? 'So close! ' : ''}A stronger photo or a different category could get you there.</p>`}
    ${rk <= 3 ? `<p class="re-rzl">🎀 ${['Gold', 'Silver', 'Bronze'][rk - 1]} rosette won · it hangs on its frame</p>` : ''}
    <button class="btn block db-go" id="crAgain">🏆 Enter today’s contests</button><div style="text-align:center"><button class="link pc-later" id="crAdd">📷 Add another photo</button></div></div>`);
  if (prize) setTimeout(() => { try { paintWallet(); cashExplosion(prize, { label: 'Photo contest' }); } catch (x) {} }, 350);
  $('#crAgain').onclick = () => { popClose(); setTimeout(() => ctOpen(e.cat), 200); }; $('#crAdd').onclick = () => { popClose(); setTimeout(finPick, 200); }; }
setInterval(() => { try { if (!S || !S.ct || !$('#app').classList.contains('on') || !freeScreen() || !popGap()) return; const e = ctEntries().find(x => !x.done && Date.now() - x.at > CT_DEMO); if (e) ctResult(e); } catch (x) {} }, 2000);
function fcNotify() {""", 1)
s = s.replace('</style>', """.ctc{margin:6px 0 14px;padding:12px 14px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 2px #D9AE4F}
.ctc-k{margin:0 0 6px;font-weight:900;letter-spacing:.05em;text-transform:uppercase;font-size:.74rem;color:#9A6B12}.ctc-s{margin:0 0 8px;font-size:.86rem}
.ctc-g{display:grid;grid-template-columns:1fr 1fr;gap:8px}html body .ctc-g button{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:10px;border:0;border-radius:12px;background:#14213D!important;color:#fff!important;text-align:left;cursor:pointer;font:inherit}
html body .ctc-g b{color:#F3D98B!important;-webkit-text-fill-color:#F3D98B;font-size:.92rem}html body .ctc-g small{font-size:.72rem;color:#E6ECF7!important;-webkit-text-fill-color:#E6ECF7}
.ctc-e{display:flex;align-items:center;gap:10px;padding:8px;margin:0 0 8px;border-radius:12px;background:#FBF7F0;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.ctc-e.ok{box-shadow:inset 0 0 0 2px #2F6B3F;background:#F1F6EC}
.ctc-e img{width:44px;height:44px;border-radius:8px;object-fit:cover}.ctc-e span{display:flex;flex-direction:column;font-size:.82rem}.ctc-e small{font-size:.76rem}
.ct-l{margin:6px 0 4px;font-weight:900;font-size:.76rem;text-transform:uppercase;letter-spacing:.06em;color:#14213D;text-align:left}
.ct-ph{display:flex;gap:8px;overflow-x:auto;margin:0 0 10px}html body .ct-ph button{flex:none;width:84px;border:0;padding:0;background:none;border-radius:10px;cursor:pointer;opacity:.55}html body .ct-ph button.on{opacity:1}
.ct-ph img{width:84px;height:100px;object-fit:cover;border-radius:10px;display:block}.ct-ph button.on img{box-shadow:0 0 0 3px #D9AE4F}.ct-ph small{display:block;font-size:.7rem;margin-top:3px}
.ct-t{display:flex;align-items:center;gap:10px;padding:10px 12px;margin:0 0 8px;border-radius:14px;background:#FBF7F0;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.ct-t.cash{background:#F1F6EC;box-shadow:inset 0 0 0 1.5px #2F6B3F}
.ct-t div{flex:1;display:flex;flex-direction:column}.ct-t div b{color:#14213D}.ct-t small{font-size:.76rem;line-height:1.4}.ct-t em{font-style:normal;font-weight:900;color:#2F6B3F;white-space:nowrap}
html body .ppop .ct-t .btn{width:auto;flex:none;padding:10px 14px;font-size:.9rem;margin:0}
.ct-none{font-size:.88rem;margin:6px 0 10px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v142 ok')
# pass 2: prize split always steps down; final result = live position without the drift (no lucky jump)
s = open(d + 'yofi-real.html').read()
RA("if (rank > paid) return 0; if (rank <= 3) return +(pool * [.2, .12, .08][rank - 1]).toFixed(2); return +(pool * .6 / (paid - 3)).toFixed(2); }",
   "if (rank > paid) return 0; const w = k => k <= 3 ? [30, 18, 12][k - 1] : Math.min(8, 40 / Math.max(1, paid - 3)), tot = 60 + (paid - 3) * w(4); return Math.floor(pool * w(rank) / tot * 100) / 100; }")
RA("return Math.max(1, Math.min(e.n, Math.round(e.n * q * (final && r() < .12 ? .02 : 1)))); }", "return Math.max(1, Math.min(e.n, Math.round(e.n * q))); }")
RA("const drift = final ? 0 : (cpRng(ppHash(e.k + Math.floor(Date.now() / 120000)))() - .5) * 8,", "const drift = final ? 0 : (cpRng(ppHash(e.k + Math.floor(Date.now() / 120000)))() - .5) * 4 * Math.max(0, 1 - (Date.now() - e.at) / CT_DEMO),")
RA("const paid = Math.max(3, Math.floor(n / 10));\n  return `1st", "const paid = Math.max(3, Math.floor(n / 10));\n  return paid <= 3 ? `1st <b>${money(ctPrize('c', n, 1))}</b> · 2nd <b>${money(ctPrize('c', n, 2))}</b> · 3rd <b>${money(ctPrize('c', n, 3))}</b>` : `1st")
RA("· 4th–${paid}th <b>${money(ctPrize('c', n, 4))}</b>`; }", "· ${paid === 4 ? '4th' : `4th–${paid}th`} <b>${money(ctPrize('c', n, 4))}</b> each`; }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v142 pass2 ok')
