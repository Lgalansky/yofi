# Real Money build, step 176 (after rmv172.py): on 2 in a row, the third streak dot pulses and says "1 more for a step!".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""<span class="pv-dots">${[0, 1, 2].map(i => `<i class="${i < k ? 'on' : ''}"></i>`).join('')}</span>""",
   """<span class="pv-dots">${[0, 1, 2].map(i => `<i class="${i < k ? 'on' : i === 2 && k === 2 ? 'next' : ''}"></i>`).join('')}</span>${k === 2 ? '<em class="pv-1m">1 more for a step!</em>' : ''}""")
s = s.replace('</style>', """.pv-dots i.next{background:#FFF1C9;box-shadow:0 0 0 2px #D9AE4F;animation:pvPulse .9s ease-in-out infinite}@keyframes pvPulse{50%{transform:scale(1.35);box-shadow:0 0 0 3px #D9AE4F,0 0 10px #F3D98B}}
.pv-1m{font-style:normal;font:900 .76rem Nunito,system-ui;color:#9A6B12;animation:qmFl .35s ease-out both}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v173 ok')
