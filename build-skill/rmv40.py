# Real Money build, step 43 (after rmv39.py): live Final board after picking.
#  - Your picks are highlighted (green row, medal on the photo, "Your 1st pick" label); bigger photos.
#  - No "Add a free $2" for players who haven't deposited.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("return `<div class=\"rb-r ${p.mine ? 'me' : ''}\"><b class=\"rb-n\">${n + 1}</b><img src=\"${p.src}\" alt=\"\"><span class=\"rb-t\"><b>${esc(p.t)}</b><small>@${esc(p.h)}${p.mine ? ' · your photo' : ''}${pk >= 0 ? ` · your ${PP_MED[pk]}` : ''}</small>",
   "return `<div class=\"rb-r ${p.mine ? 'me' : ''} ${pk >= 0 ? 'pk' : ''}\"><b class=\"rb-n\">${n + 1}</b><span class=\"rb-im\"><img src=\"${p.src}\" alt=\"\">${pk >= 0 ? `<i>${PP_MED[pk]}</i>` : ''}</span><span class=\"rb-t\">${pk >= 0 ? `<u>Your ${['1st', '2nd', '3rd'][pk]} pick</u>` : ''}<b>${esc(p.t)}</b><small>@${esc(p.h)}${p.mine ? ' · your photo' : ''}</small>")
RA("${e && !cash && fqLeft() && (S.gems || 0) >= FREE_BET_COINS ?", "${e && !cash && S.paidCash && fqLeft() && (S.gems || 0) >= FREE_BET_COINS ?")
s = s.replace('</style>', """html .rb-r{grid-template-columns:18px 64px 1fr auto!important;gap:10px!important;padding:6px 8px!important;border-radius:14px;margin:0 -8px}
html .rb-im{position:relative;width:64px;height:64px;display:block}html .rb-r .rb-im img{width:64px!important;height:64px!important;border-radius:12px!important;display:block}
html .rb-im i{position:absolute;right:-6px;bottom:-6px;font-style:normal;font-size:1.5rem;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}
html .rb-r.pk{background:#E6F0DF;box-shadow:inset 0 0 0 2px #2F6B3F}html.yg .rb-r.pk{background:#10301F;box-shadow:inset 0 0 0 2px #21C77A}
html .rb-t u{display:block;text-decoration:none;font-size:.68rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:#2F6B3F}html.yg .rb-t u{color:#21C77A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v40 ok')
