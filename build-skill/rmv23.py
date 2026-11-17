# Real Money build, step 26 (after rmv22.py): PhotoPicks logo in a handwritten script (Pacifico), smaller, top left.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html:not(.yg) body .wm,html.yg body .wm{font-family:Pacifico,'Brush Script MT',cursive!important;font-weight:400!important;letter-spacing:0!important;line-height:1.25!important;color:#A0263A!important;-webkit-text-fill-color:#A0263A!important;background:none!important}
html body #landing .ca-top .wm{font-size:1.55rem!important}html #landing .ca-top{align-items:center!important}html body header.top .wm{font-size:1.2rem!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v23 ok')
