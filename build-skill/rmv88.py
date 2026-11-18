# Real Money build, step 91 (after rmv87.py): results reveal could not scroll on shorter screens.
#  The reveal card clipped its own content (overflow hidden, fixed height), so the summary, your picks and Continue were
#  cut off with nothing to scroll. Now the card grows with its content, the pop scrolls, and Continue / Skip stay pinned
#  to the bottom of the pop so the player can always move on. Reveal photos are a little shorter so it fits more phones.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #coach .pp.rv{overflow:visible!important;height:auto!important;max-height:none!important;min-height:0!important}
html body #coach .rv .rv-go,html body #coach .rv .rv-skip{position:sticky;bottom:10px;z-index:6}html body #coach .rv .rv-go{box-shadow:0 10px 24px -8px rgba(20,33,61,.55)!important}
html body #coach .rv .rv-slot{aspect-ratio:1/1!important}html body #coach .rv .rv-yp img{aspect-ratio:4/3;max-height:84px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v88 ok')
