# Real Money build, step 201 (after rmv197.py): head-to-head entries of $2 / $5 / $10 / $20 (was $2 / $5).
#  Winner takes 1.7x: $3.40 / $8.50 / $17.00 / $34.00. Setup screen shows four tiles; results offer the next level up
#  ("Step up · $10 · winner takes $17.00"); the Stable says "Head-to-head · $2–$20". The player enters their own photo;
#  the crowd's votes decide it.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("H2H_FEES = [2, 5]", "H2H_FEES = [2, 5, 10, 20]")
RA("${fee < 5 ? `<button class=\"btn block nv-up\" id=\"h2Up\">⬆️ Step up · $5 · winner takes ${money(5 * H2H_PAY)}</button>`",
   "${H2H_FEES[H2H_FEES.indexOf(fee) + 1] ? `<button class=\"btn block nv-up\" id=\"h2Up\">⬆️ Step up · $${H2H_FEES[H2H_FEES.indexOf(fee) + 1]} · winner takes ${money(H2H_FEES[H2H_FEES.indexOf(fee) + 1] * H2H_PAY)}</button>`")
RA("$('#h2Up').onclick = () => h2hOpen(p, 5);", "$('#h2Up').onclick = () => h2hOpen(p, H2H_FEES[H2H_FEES.indexOf(fee) + 1]);")
RA("Head-to-head entry $2", "Head-to-head · $2–$20")
s = s.replace('</style>', """html body .h2-f{grid-template-columns:repeat(4,1fr)!important;gap:6px}html body .h2-f button b{font-size:1.15rem}html body .h2-f button small{font-size:.62rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v198 ok')
