# Real Money build, step 164 (after rmv160.py): the live-Final banner above the pair is removed (owner: "Remove").
#  Pairs from a live Final look like any other pair; no extra box under the round bar.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", """function ldBanner() { const o = document.getElementById('ldB'); if (o) o.remove(); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .ldb{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v161 ok')
