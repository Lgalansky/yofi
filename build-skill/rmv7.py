# Real Money build, step 10 (after rmv6.py):
#  - the hourly 6-photo show is now "the Final" (the 3-of-5 voting rounds are the Qualifiers).
#    The knockout tournament's last round keeps its own "Best in Show" name.
#  - "My show" tab is now "Gallery".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# split off the knockout tournament code, which keeps "Best in Show"
cut = s.index('the final is Best in Show\nfunction tTodayHTML')
a, b = s[:cut], s[cut:]
for x, y in [
    ('Through to Best in Show!', 'Through to the Final!'),
    ('through to Best in Show</small>', 'through to the Final</small>'),
    ('every qualifier and Best in Show', 'every qualifier and Final'),
    ('in Best in Show`', 'in the Final`'),
    ('Best in Show top 3 win', 'The Final’s top 3 win'),
    ('. Best in Show 🥇🥈🥉 win', '. The Final’s 🥇🥈🥉 win'),
    ('and Best in Show 🥇🥈🥉 win', 'and the Final’s 🥇🥈🥉 win'),
    ('Best in Show', 'Final'),
    ('🎀 Show catalogue', '🎀 Finalists'),
    ("'Show catalogue'", "'Finalists'"),
    ("'Catalogue'", "'Finalists'"),
    ("<b>Catalogue ›</b>", "<b>Finalists ›</b>"),
    ("'Not in a show yet'", "'Not entered yet'"),
    ("${raceName(g.sl)} show</small>", "${raceName(g.sl)} Final</small>"),
    (" · shows open soon", " · opens soon"),
]:
    assert x in a, x
    a = a.replace(x, y)
s = a + b
assert s.count('Best in Show') == b.count('Best in Show')

# My show -> Gallery
RA('<span class="ms-ic" aria-hidden="true">🎀</span><span>My show</span>', '<span class="ms-ic" aria-hidden="true">🖼️</span><span>Gallery</span>')
RA("$('#ptitle').textContent = 'My show';", "$('#ptitle').textContent = 'Gallery';")
RA('<h1 class="ms-h">🎀 My show</h1>', '<h1 class="ms-h">🖼️ Gallery</h1>')
RA('🎀 My show entries', '🖼️ Your gallery', 4)
assert 'My show' not in s, s[s.index('My show') - 60:s.index('My show') + 40]
open(d + 'yofi-real.html', 'w').write(s); print('rm v7 ok')
