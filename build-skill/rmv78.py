# Real Money build, step 81 (after rmv77.py): landing page clean-up.
#  - Buttons: navy for free actions (Judge photos, Enter your photo), green for real cash (Pick the Final · from $2);
#    text links navy instead of maroon.
#  - "From camera roll to cash" (AI score, enhance, competitions) removed: the old product, and a repeat of the photo tiles.
#  - Recent winners are realistic picker wins ($64 down to $22), not $250 photo prizes.
#  - Testimonials and FAQ describe Finals, picks and framing (no blue ribbons, stars, pots or scores).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('class="lp-btn" onclick="rmPickNow()"', 'class="lp-btn lp-cash" onclick="rmPickNow()"')
RA('<div class="cs"><h2>From camera roll to cash</h2>', '<div class="cs" style="display:none"><h2>From camera roll to cash</h2>')
RA('Get your first photo scored free.', 'Your first frame is free.')
RA('<p>Real photos. Real prizes.</p>', '<p>Top pickers this week.</p>')
for a, b in [('$250', '$64'), ('$200', '$48'), ('$120', '$31'), ('$95', '$22')]:
    RA(f'<b>{a}</b><span>@', f'<b>{b}</b><span>@')
RA('<p>Your first photo score is free.</p>', '<p>Your first frame is free.</p>')
RA('and your first score is free.', 'and your first frame is free.')
RA('Members vote. Two photos are shown side by side and people tap their favourite. The photo with the most votes wins.',
   'Members judge. Two photos are shown side by side and people tap their favourite. The crowd’s votes decide the order in every qualifier and Final.')
RA('Each photo challenge is $2, and $1.60 of it goes into that category’s prize pot. Collect 3 stars in a category by midnight to share the pot. Cash prizes are paid straight to your account.',
   'Every hour there’s a new Final. Pick the top 3 from $2: get 1 photo in its exact spot, or 2 in the top 3, to win. Pickers share 78% of the pool and the finalists’ creators share 10%. Prizes go straight to your wallet.')
RA('<q>I won $120 with a photo of my tulips. I check in every morning with my coffee.</q>', '<q>I picked the top 3 in the Garden Final and won $48. I check in every morning with my coffee.</q>')
RA('<q>My strawberry cake took the Baking blue ribbon. The grandkids think I’m famous.</q>', '<q>I judge a few photos with my tea and use my free pick every day. The grandkids think I’m an expert.</q>')
RA('<q>Fall colours at the cottage won me $85. It’s the nicest part of my day.</q>', '<q>My autumn photo made the Nature Final and earned me a share of the prize. It’s the nicest part of my day.</q>')
RA('<q>I love seeing other people’s gardens and kitchens. Voting is so relaxing.</q>', '<q>I love seeing other people’s gardens and pets. Judging is so relaxing.</q>')
s = s.replace('</style>', """html body #landing .lp2 button.lp-btn,html body #landing button.lp-btn{background:#1E3A6E!important;color:#fff!important}html body #landing .lp2 button.lp-btn.lp-cash,html body #landing button.lp-btn.lp-cash{background:#2F6B3F!important}
html body #landing .lp-lnk,html body #landing .lp-watch,html body #landing .lp-watch svg{color:#1E3A6E!important}html body #landing .lp2 h2,html body #landing .lp-cth h2,html body #landing .lp2-row h2{color:#14213D!important;-webkit-text-fill-color:#14213D}html body #landing .lp2-ic,html body #landing .lp2-ic svg,html body #landing .lp-ct svg{color:#1E3A6E!important}
html body #landing .lp.lp2,html body #landing .lp2 .lp2-live b,html body #landing .lp2 .lp2-steps b,html body #landing .lp2 .lp2-steps svg,html body #landing .lp2 .lp-cn,html body #landing .lp2 .lp-cc small,html body #landing .lp2 .lp-watch,html body #landing .lp2 .lp-watch span,html body #landing .lp2 .lp-lnk,html body #landing .lp2 .lp2-row svg{color:#14213D!important;-webkit-text-fill-color:currentColor}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v78 ok')
