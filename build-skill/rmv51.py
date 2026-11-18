# Real Money build, step 54 (after rmv50.py): results reveal ends on a "Continue" button (no auto-jump).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("<p class=\"rv-me\" id=\"rvMe\">&nbsp;</p><div style=\"text-align:center\"><button class=\"link rv-skip\" id=\"rvSkip\">Skip ›</button></div></div>`);",
   "<p class=\"rv-me\" id=\"rvMe\">&nbsp;</p><button class=\"btn block rv-go\" id=\"rvGo\" hidden>Continue →</button><div style=\"text-align:center\"><button class=\"link rv-skip\" id=\"rvSkip\">Skip ›</button></div></div>`);")
RA("  $('#rvSkip').onclick = fin;", "  $('#rvSkip').onclick = fin; $('#rvGo').onclick = fin;")
RA("  at(1900 + 3 * 1300 + 700, fin); }",
   "  at(1900 + 3 * 1300 + 400, () => { const g = $('#rvGo'), k = $('#rvSkip'); if (g) g.hidden = false; if (k) k.hidden = true; }); }")
s = s.replace('</style>', """html body .rv .btn.rv-go{background:#24563A!important;color:#fff!important;-webkit-text-fill-color:#fff!important;font:800 1.2rem Fraunces,Georgia,serif;margin-top:6px;animation:rvPop .5s cubic-bezier(.2,1.6,.4,1)}.rv{min-height:0!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v51 ok')
