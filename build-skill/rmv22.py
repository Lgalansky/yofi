# Real Money build, step 25 (after rmv21.py): brand is PhotoPicks; landing heading "Pick the winning photos. Win real cash."
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA('<h1 class="lp2-brand">PhotoPicks</h1><p class="lp2-sub">Pick your favourite. Cheer it on in the hourly Final.</p>',
   '<h1 class="lp-h">Pick the winning photos.<em>Win real cash.</em></h1><p class="lp-sub">Pick your favourite. Cheer it on in the hourly Final.</p>')
# rename the brand everywhere players can see it (save keys like yofi.real.v1 stay)
s = s.replace('Yofi', 'PhotoPicks').replace('yofi.app', 'photopicks.app')
s = re.sub(r'<title>[^<]*</title>', '<title>PhotoPicks</title>', s, count=1)
s = s.replace('</style>', """html #landing .ca-top .wm{visibility:visible!important}.wm{white-space:nowrap}html header.top .wm{font-size:1.15rem!important;letter-spacing:-.01em}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v22 ok')
