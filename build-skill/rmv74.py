# Real Money build, step 77 (after rmv73.py): photo card message = qualify for the Final and earn a share of 10% of the pool.
#  (The top-2 qualifier step pays nothing, so it is no longer the headline step.)
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
Q = '<p><b>Qualify for the Final</b>Your photo races the qualifiers to reach the hourly Final.</p>'
P = '<p><b>Earn a share of 10%</b>Every finalist’s creator shares 10% of the Final’s prize pool.</p>'
RA('<p><b>Finish in the top 2</b>in your category’s qualifier.</p>', Q)
RA('<p><b>Finish in the top 2</b>in your category’s qualifier, like these two.</p>', Q)
RA('<p><b>Every finalist gets paid</b>Your photo doesn’t have to finish first.</p>', P)
RA('<p><b>Every finalist gets paid</b>Creators share 10% of the Final’s prize pool.</p>', P)
s = s.replace('Enter your photo. Reach the Final. Get paid.', 'Qualify for the Final. Earn a share of the prize.')
open(d + 'yofi-real.html', 'w').write(s); print('rm v74 ok')
