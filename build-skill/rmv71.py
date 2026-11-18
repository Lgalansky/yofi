# Real Money build, step 74 (after rmv70.py): Final result no longer repeats the reveal.
#  The crowd's top 3, your picks and the rule line were shown again right after the reveal; they are removed.
#  The result keeps: You won / summary chip / cash won / winner, then pool & winners, payouts, creator card, next steps.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
i = s.index('<p class="fr2-row">Crowd’s top 3</p>'); assert s.count('<p class="fr2-row">Crowd’s top 3</p>') == 1
k = s.index('<p class="fr2-rule">', i); j = s.index('</p>', k) + 4
assert j - i < 1500, j - i
s = s[:i] + s[j:].lstrip()
# the winner line repeats the creator card's winner when that card is shown
s = s.replace('</style>', '.fr2:has(.cw2) .fr2-win{display:none}\n</style>', 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v71 ok')
