# Real Money build, step 84 (after rmv80.py): new-player fixes 1–4.
#  1. Cash pick after paying: the pick used to land ~5 s after payment while the Vote screen showed, so it looked lost.
#     Now it lands ~1.6 s after the cash animation, with a "Cash added · placing your pick" toast. Deposit pop: "Add $10"
#     (green) instead of "Buy · $10.00", "Other amounts" instead of "See all packs".
#  2. Upload: the old "Touch up your photo · Score / Goal 70" screen never shows (studio redirects to the Gallery);
#     a new Final-category photo goes straight to one "Frame your photo" step (name + frame together, no score);
#     the extra "Frame it to enter the qualifiers" pop is gone.
#  3. Shared celebration and "you need cash" pops use the navy style (no brown all-caps); numeric photo scores hidden.
#  4. 15 votes: "🎟️ Free pick unlocked!" → "Make my free pick" opens the Final pick screen directly (was 3 screens).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# 1
RA("if (after) setTimeout(after, 4300);", "if (after) { setTimeout(() => toast('✓ Cash added · placing your pick'), 900); setTimeout(after, 1600); }")
RA("`Buy · $${(+cfg.usd).toFixed(2)}`", "`Add $${(+cfg.usd).toFixed(0)}`")
RA('<button class="ro-all" id="roAll">See all packs</button>', '<button class="ro-all" id="roAll">Other amounts</button>')
# 2
s = s.replace("function fcNotify() {", """try { const _go0 = go; go = function (w, ...a) { return _go0.call(this, w === 'studio' ? 'gallery' : w, ...a); }; } catch (e) {}
function fcNotify() {""", 1)
RA("const un = (S.photos || []).find(p => !p.title && !p.nmAsk && p.at && Date.now() - p.at < 864e5); if (un) { un.nmAsk = 1; save(); nameAsk(un); return; }",
   "const un = (S.photos || []).find(p => !p.title && !p.nmAsk && p.at && Date.now() - p.at < 864e5); if (un) { un.nmAsk = 1; save(); if (photoShow(un) && !un.framed) { myShow(); setTimeout(() => frameOpen(un), 300); } else nameAsk(un); return; }")
RA("if (!S.ffGift && !S.firstEntry", "if (false && !S.ffGift && !S.firstEntry")
# 3
RA('<span class="cr-score">${score}</span>', "${score && isNaN(+score) ? `<span class=\"cr-score\">${score}</span>` : ''}")
# 4
RA("title: 'You have unused coins', text: `You’ve judged ${15} photos and earned a <b>free ticket</b>: a free pick in the <b>${raceName(ppGame().sl)} ${esc(showName(ppGame().k))} Final</b>, with real cash prizes. Open your coins to use it.`, cta: '🟡 Open my coins', onCta: () => { closeFlow(); useGems(); }",
   "title: '🎟️ Free pick unlocked!', text: `You judged 15 photos. Your free pick in the <b>${raceName(ppGame().sl)} ${esc(showName(ppGame().k))} Final</b> is ready: pick the top 3 for real cash prizes.`, cta: '🎟️ Make my free pick', onCta: () => { closeFlow(); ppOpen(); }")
s = s.replace('</style>', """html:not(.yg) body #coach .crbox{background:#FBF7F0!important;box-shadow:0 0 0 2.5px #D9AE4F,0 20px 40px -18px rgba(20,33,61,.5)!important}
html:not(.yg) body #coach .crbox h2{font:800 1.9rem/1.08 Fraunces,Georgia,serif!important;text-transform:none!important;letter-spacing:0!important;color:#14213D!important;-webkit-text-fill-color:#14213D!important;filter:none!important}
html:not(.yg) body #coach .crbox p{color:#2B2320!important}html:not(.yg) body #coach .crbox p b{color:#14213D!important}
html:not(.yg) body #coach .crbox .bt-cta,html:not(.yg) body #coach .crbox #crGo{min-height:56px;background:#1E3A6E!important;color:#fff!important;font:800 1.15rem Fraunces,Georgia,serif!important;text-transform:none!important;box-shadow:0 10px 22px -12px rgba(20,33,61,.6)!important;border-radius:999px}
html:not(.yg) body #coach .crbox .bt-no,html:not(.yg) body #coach .crbox .ro-free,html:not(.yg) body #coach .crbox .ro-all{color:#1E3A6E!important;font-weight:800}
html:not(.yg) body #coach .crbox .enh-go{background:#2F6B3F!important;color:#fff!important;text-transform:none!important;font:800 1.2rem Fraunces,Georgia,serif!important}
html:not(.yg) body #coach .crbox .cr-crown{display:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v81 ok')
