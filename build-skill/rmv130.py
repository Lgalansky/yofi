# Real Money build, step 133 (after rmv129.py): one signal per fact in the pick result reveal.
#  The podium showed the place ("2nd"), a "2" rosette and "✓ Exact match" for the same photo, and "Your picks"
#  repeated the rosette and "Exact match". Now: the podium shows the real place plus "Your 2nd pick" with the gold
#  border when you got it; "Your picks" below says "✓ Exact match". No rosettes on picks: rosettes are only for
#  your own photos (rmv128).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("${hit ? `<i class=\"rv-rz\">${rosette(o.win ? 'w' : k)}</i>` : ''}", "")
RA("${top[i] === p ? `<i class=\"rv-rz sm\">${rosette(i)}</i>` : ''}", "")
s = s.replace('</style>', """html body .rv-pod.rv-exs{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v130 ok')
