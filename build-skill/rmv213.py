# Real Money build, step 216 (after rmv212.py): fixes from the tap-through audit.
#  1. "Enter a final" buttons say what they do: "Vote N steps to the Final" until the photo's steps are done
#     (Stable cards, coins sheet, training and head-to-head results).
#  2. Every Final needs its voting steps. After racing a Final (or finishing training) the photo goes straight back on
#     the Vote screen at "0 of 3 steps to the Final", so votes move it on. Old saves are moved over once.
#  3. Final result: "Race again / Step up" (straight into another Final) replaced by
#     "Vote 3 steps to your next Final" + "Race a $X head-to-head now" (instant cash play stays on head-to-heads).
#  4. Low coins: any training match screen shows "Vote to earn coins · N more to train" instead of a button that refuses;
#     the Stable's "Train now · 50 coins" becomes the same vote button when short.
#  5. "Invite a friend" opens a real invite sheet (link to share or copy, the reward rule) instead of My Photos.
#  6. "Enter your photo" picker: old "Starts when 6 finalists are in · 4 of 6" removed; intro states all the steps.
#  7. Every "Add cash" opens the navy Add cash sheet (the old cream "Add cash to play" pop is retired).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
# 1. labels
RA('data-stf="${p.id}">🏁 Enter a Final</button>', 'data-stf="${p.id}">${finBtn(p)}</button>')
RA('data-stf="${p.id}">🏁 Enter a final</button>', 'data-stf="${p.id}">${finBtn(p)}</button>')
RA('data-tcf="${p.id}">Enter a final</button>', 'data-tcf="${p.id}">${finBtn(p, 1)}</button>')
RA('id="h2F">🏁 Enter a Final</button>', 'id="h2F">${finBtn(p)}</button>')
RA("${cash ? `💵 Race again · $${fee}` : '🏁 Enter a Final'}", "${cash ? `💵 Race again · $${fee}` : finBtn(p)}")
RA("<button class=\"btn block nv-go\" id=\"h2Ag\">${fresh ? '🏁 Enter a Final' :", "<button class=\"btn block nv-go\" id=\"h2Ag\">${fresh ? `⚖️ Vote ${QS_STEPS} steps to the Final` :")
RA("? 'Finals ($2–$20) and cash head-to-heads are open' :", "? `Cash head-to-heads are open · ${QS_STEPS} voting steps to a Final` :")
# 6. picker wording
RA("Pick the category your photo is for. Your voting streaks take it to its qualifier: a live 2-horse race decided by the crowd. Win it and it races in a 6-photo Final for cash. Entry is free.",
   "Pick the category your photo is for. Entry is free. Your votes take it to a live qualifier race. Win it, vote 3 more steps, and it races in a 6-photo Final for cash.")
RA("<small>Next Final · <b>${finReady(x.sl)}</b></small>", "<small>Live Finals all day · <b>6 photos a race</b></small>")
RA("function fcNotify() {", r"""function finBtn(p, plain) { const n = QS_STEPS - Math.min(QS_STEPS, (p && p.fr && p.fr.s) || 0); return n <= 0 ? `${plain ? '' : '🏁 '}Enter a Final` : `${plain ? '' : '⚖️ '}Vote ${n} step${n === 1 ? '' : 's'} to the Final`; }
function finBack(p) { if (p && isCashOK(p) && !(p.fin && p.fr)) { p.fin = 1; p.fr = { s: 0 }; p.fl = null; } }
try { (S.photos || []).forEach(p => { if (isCashOK(p) && !p.fin && !p.du) finBack(p); }); save(); } catch (e) {}
(() => { const rj = renderJudge; renderJudge = function () { try { let ch = 0; (S.photos || []).forEach(p => { if (isCashOK(p) && !p.fin && !p.du) { finBack(p); ch = 1; } }); if (ch) save(); } catch (e) {} return rj.apply(this, arguments); }; })();
// 2 + 3. after a Final: back to voting steps; replay offers become vote-to-Final + head-to-head
(() => { const qr = qfResult; qfResult = function (p, L, ord) { const r = qr.apply(this, arguments); try { finBack(p); save(); try { qlPaint(); } catch (x) {}
    const fee = window.__qfFee || 2, A = document.getElementById('qrA'); ['qrU', 'qrC'].forEach(id => { const x = document.getElementById(id); if (x) x.remove(); });
    if (A) { A.outerHTML = `<button class="btn block db-go cashb" id="qrV">⚖️ ${QS_STEPS} steps to your next Final</button><button class="btn block db-go rm-up" id="qrH">⚔️ Race a $${fee} head-to-head now</button>`;
      $('#qrV').onclick = () => { popClose(); try { closeFlow(); } catch (x) {} go('judge'); renderJudge(); toast(`⚖️ Vote ${QS_RUN} in a row with the crowd = 1 step · ${QS_STEPS} steps to ${rcName(p)}’s next Final`); };
      $('#qrH').onclick = () => { popClose(); h2hOpen(p, H2H_FEES.includes(fee) ? fee : H2H_FEES[0]); }; } } catch (x) {} return r; }; })();
(() => { const hd = h3Done; h3Done = function (p) { const r = hd.apply(this, arguments); try { if (p && isCashOK(p)) { finBack(p); save(); } } catch (e) {} return r; }; })();
// 4. low coins on any training screen
(() => { const ho = h2hOpen; h2hOpen = function (p, fee) { const r = ho.apply(this, arguments); try { const g = Math.floor(S.gems || 0), b = document.getElementById('h2Go');
    if (!(fee > 0) && b && g < TQ_COST) { b.textContent = `⚖️ Vote to earn coins · ${TQ_COST - g} more to train`; b.onclick = () => { popClose(); try { closeFlow(); } catch (e) {} go('judge'); renderJudge(); }; } } catch (e) {} return r; }; })();
(() => { const sv = stTrain; stTrain = function (p) { let h = sv.apply(this, arguments); try { const g = Math.floor(S.gems || 0); if (g < TQ_COST) {
      h = h.replace(`<button class="btn sx-nv" data-sth="${p.id}" data-m="t">🏋️ Train now · ${TQ_COST} coins</button>`, `<button class="btn sx-nv" data-stv>⚖️ Vote to earn coins · ${TQ_COST - g} more to train</button>`)
           .replace(`>or train with coins · ${TQ_COST} a match</button>`, `>or train with coins · ${TQ_COST} a match (${TQ_COST - g} more needed)</button>`); } } catch (e) {} return h; }; })();
// 5. invite a friend
function inviteSheet() { const code = (S.invCode = S.invCode || ('PP' + Math.random().toString(36).slice(2, 7).toUpperCase())), url = `https://photopicks.app/i/${code}`; save();
  popOpen(`<div class="pp qfx nv inv"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">Invite a friend</span></div><h2 class="nv-h2">You each get 100 coins</h2>
    <p class="qw-o">When your friend joins with your link and votes on 15 photos, you both get <b class="gold">100 coins</b>.</p>
    <div class="inv-box"><small>Your invite link</small><b id="invU">${url}</b></div>
    <button class="btn block nv-go" id="invGo">📤 Share your link</button><div style="text-align:center"><button class="link nv-later" id="invX">Done</button></div><p class="nv-sim">Demo · invites aren’t sent in this prototype</p></div>`);
  $('#invGo').onclick = async () => { const t = 'Judge photos with me on PhotoPicks: we both get 100 coins'; try { if (navigator.share) { await navigator.share({ title: 'PhotoPicks', text: t, url }); return; } } catch (e) { return; }
    try { await navigator.clipboard.writeText(url); toast('🔗 Link copied'); } catch (e) { toast('🔗 Copy your link: ' + url); } };
  $('#invX').onclick = () => popClose(); }
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-tci]'); if (!b) return; e.preventDefault(); e.stopPropagation(); try { closeSheet(); } catch (x) {} setTimeout(inviteSheet, 200); }, true);
// 7. every Add cash -> navy sheet
function addCashNv(amt, what, onBuy) { amt = +amt || 0; const have = +((S.cash || 0) + (S.bonus || 0)).toFixed(2), w = !S.paidCash && !S.bonusGot, bn = w ? 10 : 0;
  const add = amt ? ([5, 10, 20, 50, 100].find(a => have + a + bn >= amt) || 100) : (w ? 5 : 10), left = +(have + add + bn - amt).toFixed(2), m0 = v => money(v).replace(/\.00$/, '');
  const ttl = amt ? String(what).replace(/^(The|A|An) /, '').replace(/^./, c => c.toUpperCase()) : 'Add cash';
  try { if ($('#sheet').classList.contains('on')) closeSheet(); } catch (e) {}
  popOpen(`<div class="pp qfx nv acn"><p class="nv-brand">PhotoPicks</p><div class="nv-pillrow"><span class="nv-pill">${w ? 'Welcome offer' : 'Add cash'}</span></div>
    <h2 class="nv-h2">${esc(ttl)}</h2>
    <p class="qw-o">${amt ? `Entry <b class="gold">${m0(amt)}</b> · you have <b class="gold">${m0(have)}</b>` : `You have <b class="gold">${m0(have)}</b> to play`}</p>
    <div class="acn-box"><div class="h2w-amt">${m0(add)}</div>${w ? '<span class="acn-bn">+ $10 Bonus Cash free</span>' : ''}
      <small>${w ? 'Bonus Cash is spent first on entries and can’t be withdrawn. Your winnings are real cash.' : 'Cash to play. Your winnings are real cash.'}</small>
      <p class="acn-left">${amt ? `After this entry you’ll have <b>${m0(left)}</b> left to play` : `You’ll have <b>${m0(left)}</b> to play: Finals and head-to-heads from $2`}</p></div>
    <button class="btn block nv-go" id="acnGo">Add ${m0(add)}${amt ? ' · enter now' : ''}</button>
    <div style="text-align:center"><button class="link nv-later" id="acnAll">Other amounts</button> <button class="link nv-later" id="acnNo">Not now</button></div><p class="nv-sim">Demo · no real payment is taken</p></div>`);
  $('#acnGo').onclick = () => { popClose(); checkout(`$${add} cash`, add, () => applyOffer(add, 0, w ? 'Welcome offer · $10 Bonus Cash' : `$${add} pack`, () => { S.cashMode = 1; save(); if (w && !S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + 10).toFixed(2); save(); toast('🎁 $10 Bonus Cash added · used first on entries'); } try { paintWallet(); } catch (e) {} if (onBuy) onBuy(); })); };
  $('#acnAll').onclick = () => { popClose(); openStore(null, onBuy, 'cash'); }; $('#acnNo').onclick = () => popClose(); }
(() => { const ro = runOut; runOut = function (kind, title, onBuy) { if (kind === 'cash') { const m = String(title || '').match(/\$(\d+(?:\.\d+)?)/); return addCashNv(m ? +m[1] : 0, m ? 'This entry' : '', onBuy); } return ro.apply(this, arguments); }; })();
function fcNotify() {""")
s = s.replace('</style>', """.inv-box{margin:12px 0 14px;padding:12px;border-radius:14px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(10,16,32,.4);text-align:center}.inv-box small{display:block;font:700 .74rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8C9AB5}.inv-box b{display:block;margin-top:4px;font:800 1rem Nunito,system-ui;color:#F3D98B;word-break:break-all}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v213 ok')
