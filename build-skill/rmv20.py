# Real Money build, step 23 (after rmv19.py): fixes to the new-photo flow + "How it works" on the landing page.
#  - "Enter your photo" no longer guesses the category: after upload, the player picks the Final category (Pets / Nature / Garden).
#  - The 150 coins come from the sign-up welcome bonus (100 + 50), so the first-photo pop no longer adds a second 150.
#  - Studio/Gallery status for the first photo: "Touch up to go straight to the Final".
#  - Landing: 3-step "How it works": upload, improve it to qualify, pick the top 3 of 6 in the hourly Final.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# ask the Final category after upload
RA("function rmEnterOwn() { const k = finNext(1)[0].k; window.__preCat = showHint(k).cats[0]; yWL(); }", "function rmEnterOwn() { window.__preCat = null; yWL(); }")
RA("  const un = (S.photos || []).find(p => !p.title && !p.nmAsk && p.at && Date.now() - p.at < 864e5); if (un) {",
   "  const nc = (S.photos || []).find(p => !photoShow(p) && !p.catAsk && p.at && Date.now() - p.at < 864e5); if (nc) { nc.catAsk = 1; save(); askCategory(nc, () => { closeFlow(); save(); try { renderStudio(); } catch (e) {} }, true); return; }\n  const un = (S.photos || []).find(p => !p.title && !p.nmAsk && p.at && Date.now() - p.at < 864e5); if (un) {")
# no second 150: the sign-up welcome bonus is the 150
RA("S.gems = (S.gems || 0) + FF_GIFT; save(); paintGems();", "save();")
RA("text: `${y ? 'Enhance' : 'Touch up'} <b>${esc(p.title)}</b> and it goes",
   "text: `${S.user && S.user.guest ? `Create your free account and get <b>${FF_GIFT} coins</b> to improve <b>${esc(p.title)}</b>.` : `Use your coins to ${y ? 'enhance' : 'touch up'} <b>${esc(p.title)}</b>.`} Once it improves it goes")
RA("title: `${FF_GIFT} coins to improve your photo`", "title: 'Improve it, then straight to the Final'")
# status line for the first photo
RA("if (p.s.total < SHOW_MIN) return { cls: 'low'",
   "if (p.id === S.ffPid && !S.ffDone && photoShow(p)) return { cls: 'low', ic: '✨', t: 'Touch up to go straight to the Final', s: `Any improvement sends it to the <b>${raceName(rcSlotFor(p))} ${esc(showName(photoShow(p)))} Final</b>` };\n  if (p.s.total < SHOW_MIN) return { cls: 'low'")
# landing: how it works
RA('<p class="lp-cap">Which photo will take first place?</p>',
   '<p class="lp-cap">Which photo will take first place?</p><div class="lp-how"><div><i>1</i><b>📷 Upload a photo</b><small>Pets, Nature or Garden</small></div><div><i>2</i><b>✨ Improve it to qualify</b><small>Touch it up with coins</small></div><div><i>3</i><b>🥇 Pick the top 3 of 6</b><small>in the hourly Final</small></div></div>')
s = s.replace('</style>', """.lp-how{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 22px;text-align:center}.lp-how div{background:#FFFFFF;border-radius:14px;padding:10px 6px 9px;box-shadow:inset 0 0 0 1px #EADCC6;position:relative}
.lp-how i{position:absolute;top:-9px;left:50%;transform:translateX(-50%);width:20px;height:20px;border-radius:50%;background:#9A2F4E;color:#fff;font-style:normal;font-size:.72rem;font-weight:800;line-height:20px}.lp-how b{display:block;font-size:.84rem;line-height:1.2;margin-top:4px}.lp-how small{display:block;font-size:.72rem;opacity:.8;margin-top:2px}
</style>""", 1)
# prompts can show over the touch-up screen (not over the scan/crop)
RA("  if (!S || !S.user || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || $('#landing').style.display !== 'none') return;\n  const nc",
   "  if (!S || !S.user || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || ($('#flow').classList.contains('on') && ($('#flow .scan') || $('#flow .pcats') || !$('#flow .scr2, #flow .ba, #flow [class*=\"ba-\"]'))) || $('#landing').style.display !== 'none') return;\n  const nc")
# the first photo's own pop handles it: no Skill "first challenge free" pop
RA("  if (p && p.id !== S.ffPid && p.s.total >= SHOW_MIN && photoShow(p)", "  if (p && p.id === S.ffPid) return;\n  if (p && p.id !== S.ffPid && p.s.total >= SHOW_MIN && photoShow(p)")
open(d + 'yofi-real.html', 'w').write(s); print('rm v20 ok')
