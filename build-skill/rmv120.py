# Real Money build, step 123 (after rmv119.py): the photo picker always opens over your Gallery.
#  Tapping "Enter a photo" / a category from the Vote screen, the Finals tab or a pop used to open the iPhone photo
#  picker over whatever screen you were on (e.g. two photos to vote on). pickPhoto now moves you to the Gallery
#  (your creator page) first, from any entry point, then opens the picker.
#  Also: Finals tab "How Finals work" no longer says "Every hour".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""  if (S.photos.length >= CFG.MAX_PHOTOS) { makeRoom(fromStudio); return; }
  intakeFromStudio = !!fromStudio;""",
   """  if (fromStudio && $('#app').classList.contains('on')) { try { if (typeof popClose === 'function' && document.querySelector('#coach.on')) popClose(); if ($('#flow').classList.contains('on')) closeFlow(); if ($('#panes').dataset.at !== 'gallery') go('gallery'); renderMyShow(); } catch (e) {} }
  if (S.photos.length >= CFG.MAX_PHOTOS) { makeRoom(fromStudio); return; }
  intakeFromStudio = !!fromStudio;""")
RA("<p>Every hour, 6 photos that came through the qualifiers race in a Final.",
   "<p>A Final starts as soon as 6 photos come through the qualifiers, and they race.")
open(d + 'yofi-real.html', 'w').write(s); print('rm v120 ok')
