# Real Money build, step 106 (after rmv102.py): the vote reveal's climbing fill is back. Each photo fills from the
# bottom to its crowd share (green for the crowd's pick, navy for the other), with the big percentage on top.
# Photos stay at full brightness above the fill; no banner.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #judge .tot-c .cfx-fill i{display:block!important;position:absolute!important;left:0!important;right:0!important;bottom:0!important;top:auto!important;height:0;background:rgba(20,33,61,.5)!important;animation:cfxUp .8s cubic-bezier(.2,.9,.3,1) forwards!important}
html body #judge .tot-c .cfx-fill.w i{background:linear-gradient(0deg,rgba(47,107,63,.8),rgba(47,107,63,.35))!important}html body #judge .tot-c .cfx-fill b{z-index:1}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v103 ok')
