# Real Money build, step 128 (after rmv124.py): pick medals without the white disc (it covered the photo).
#  Medals stay big; a drop shadow keeps them readable on any photo.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .pp-g .pp-b{background:none!important;box-shadow:none!important;filter:drop-shadow(0 3px 6px rgba(0,0,0,.55))!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v125 ok')
