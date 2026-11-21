# Real Money build, step 236 (after rmv232.py): one button colour rule across the app (user rule).
#  GREEN = real money (cash entries, head-to-heads, Finals, challenges, deposits, Play for Real, withdraw).
#  GOLD/YELLOW = coins (training, Daily Cup entry, anything priced in 🪙).
#  NEUTRAL = free actions (vote, start voting, race it again, see your stable): navy on light screens, cream on dark screens.
#  Applied automatically to every main button as screens open; fee pickers, links and disabled buttons are left alone.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""const PK_CASH = /\$\d|play for real|deposit|add cash|withdraw|enter the final|first final|head-to-head|race (the|your) final|enter a final|meet your finalists|accept/i, PK_COIN = /🪙|🟡|\bcoins?\b/i;
function pkTag(b) { if (!b || b.disabled || b.classList.contains('off') || b.closest('.qf2-f, .qfp-f, .h2-f, .tot, nav, .lp-pod, .su-age') || b.matches('.link, .nv-later, .pc-later, .h3-x, .t2-x, .qs2-x, .cg-n, .tm-b, .snd-t')) return;
  const t = (b.innerText || b.textContent || '').trim(); if (!t) return;
  let k = b.matches('[data-ldc], [data-chy], [data-wbf], [data-qfr]') ? 'cash' : b.matches('[data-cup]') ? 'coin' : PK_COIN.test(t) ? 'coin' : PK_CASH.test(t) ? 'cash' : b.matches('[data-ldc], [data-chy]') ? 'cash' : 'free';
  if (PK_COIN.test(t) && PK_CASH.test(t)) k = /\$\d|cash|deposit|play for real/i.test(t) ? 'cash' : 'coin';
  const dark = !!b.closest('.nv, .wbk, .h2r, .qls2, #sheet.su-nv, .cup2, .cup, .pg-goal.on, .qfx.h3, .trn3, .acn, .wo');
  b.classList.remove('pk-cash', 'pk-coin', 'pk-free', 'pk-dark'); b.classList.add('pk-' + k); if (dark) b.classList.add('pk-dark'); }
function pkAll() { document.querySelectorAll('#coach .btn, #sheet .btn, #flow .btn, #qlS .btn, #cupC .btn, .ld-b, .wbk-b, .cs-b, #finPick .btn').forEach(pkTag); }
(() => { let q = 0; new MutationObserver(() => { if (q) return; q = 1; requestAnimationFrame(() => { q = 0; try { pkAll(); } catch (e) {} }); }).observe(document.body, { childList: true, subtree: true, characterData: true }); setTimeout(pkAll, 500); })();
function fcNotify() {""")
s = s.replace('</style>', """html body :is(#flow,#coach,#sheet,#qlS,#cupC,#app,#finPick,body) .pk-cash.pk-cash.pk-cash.pk-cash,html body .pk-cash.pk-cash.pk-cash.pk-cash.pk-cash{background:linear-gradient(180deg,#2F8A45,#1E6B34)!important;color:#fff!important;box-shadow:0 6px 14px -6px rgba(30,107,52,.6)!important;border:0!important}
html body :is(#flow,#coach,#sheet,#qlS,#cupC,#app,#finPick,body) .pk-coin.pk-coin.pk-coin.pk-coin,html body .pk-coin.pk-coin.pk-coin.pk-coin.pk-coin{background:linear-gradient(180deg,#F6DE94,#D9AE4F)!important;color:#14213D!important;box-shadow:0 6px 14px -6px rgba(201,149,45,.6)!important;border:0!important}
html body :is(#flow,#coach,#sheet,#qlS,#cupC,#app,#finPick,body) .pk-free.pk-free.pk-free.pk-free,html body .pk-free.pk-free.pk-free.pk-free.pk-free{background:linear-gradient(180deg,#22325A,#14213D)!important;color:#fff!important;box-shadow:0 6px 14px -8px rgba(20,33,61,.6)!important;border:0!important}
html body :is(#flow,#coach,#sheet,#qlS,#cupC,#app,#finPick,body) .pk-free.pk-dark.pk-dark.pk-dark.pk-dark,html body .pk-free.pk-dark.pk-dark.pk-dark.pk-dark.pk-dark{background:#FBF3DC!important;color:#14213D!important;box-shadow:none!important}
html body :is(#flow,#coach,#sheet,#qlS,#cupC,#app,#finPick,body) .pk-cash.pk-cash.pk-cash *,html body :is(#flow,#coach,#sheet,#qlS,#cupC,#app,#finPick,body) .pk-free.pk-free:not(.pk-dark) *{color:inherit!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v233 ok')
