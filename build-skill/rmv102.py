# Real Money build, step 105 (after rmv101.py): vote reveal shows the big percentages on both photo tiles again
# (no shading), and the "You called it" / "The crowd went the other way" banner is removed. The streak line still updates.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #judge .tot-c .cfx-fill{display:block!important}html body #judge .cfx-b{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v102 ok')
