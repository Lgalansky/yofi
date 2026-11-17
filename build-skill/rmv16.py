# Real Money build, step 19 (after rmv15.py): show new players the next Final categories.
#  - "Next Finals" strip (time + category) on: the landing page, the end-of-tutorial card, the first-photo pop and Gallery.
#  - "Add a photo" at the end of the tutorial opens the category of the next Final.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""const SHOW_IC = { pets: '🐾', nature: '🏞️', garden: '🌷', food: '🍰' };
function finNext(n) { const cur = ppSlot(), out = []; for (let sl = cur + 1; out.length < (n || 3); sl++) { const k = ppGame(sl).k; out.push({ sl, k }); } return out; }
function finSchedHTML(n, lab) { return `<div class="fsch"><small>${lab || 'Next Finals'}</small><div>${finNext(n).map(x => `<span>${SHOW_IC[x.k] || '🎀'} <b>${raceName(x.sl)}</b> ${esc(showName(x.k))}</span>`).join('')}</div></div>`; }
function showHint(k) { const y = isYoungW(), c = k === 'pets' ? ['pets'] : k === 'garden' ? ['fitness'] : k === 'nature' ? [y ? 'travel' : 'night'] : ['food']; return { cats: c, lab: showName(k), frame: showName(k) }; }
setInterval(() => { try { const el = document.getElementById('caSched'); if (el && S) { const h = finSchedHTML(3, 'Next Finals · enter a photo in one of these'); if (el.innerHTML !== h) el.innerHTML = h; } } catch (e) {} }, 1000);
function fcNotify() {""", 1)

# landing
RA('<p class="ca-sub ca-or">Or add your first photo: it goes into a qualifier free.</p>',
   '<p class="ca-sub ca-or">Or add your first photo: it goes into a qualifier free.</p><div id="caSched"></div>')
# end-of-tutorial card
RA("<span>Every finalist’s creator gets paid. Your first photo goes straight into a qualifier, free.</span><button class=\"btn block pc-go\" id=\"ppUp\">📷 Add a photo</button>",
   "<span>Every finalist’s creator gets paid. Your first photo goes straight into a qualifier, free.</span>${finSchedHTML(3)}<button class=\"btn block pc-go\" id=\"ppUp\">📷 Add a ${esc(showName(finNext(1)[0].k).toLowerCase())} photo</button>")
RA("S.frameHint = { cats: ['pets'], lab: 'Pets', frame: 'Pets' }; save(); pickPhoto(true); }; $('#ppNext')",
   "S.frameHint = showHint(finNext(1)[0].k); save(); pickPhoto(true); }; $('#ppNext')")
# first-photo pop: say which Final it's going for
RA("it goes straight into the <b>${esc(showName(photoShow(p)))}</b> qualifiers. ${y ? 'Judges' : 'Voters'} send the top 2 to the hourly <b>Final</b>,",
   "it goes straight into the qualifiers for the <b>${raceName(rcSlotFor(p))} ${esc(showName(photoShow(p)))} Final</b>. ${y ? 'Judges' : 'Voters'} send the top 2 to that <b>Final</b>,")
# Gallery
RA("<b>Finalists ›</b></button>", "<b>Finalists ›</b></button>${finSchedHTML(3)}")

s = s.replace('</style>', """.fsch{margin:8px 0 10px;text-align:left}.fsch small{display:block;font-size:.7rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;opacity:.75;margin-bottom:5px}.fsch div{display:flex;flex-wrap:wrap;gap:6px}.fsch span{font-size:.82rem;padding:5px 10px;border-radius:999px;white-space:nowrap}

.fsch span{display:inline-block!important;margin:0!important;opacity:1!important;font-size:.82rem!important}.fsch span b{display:inline!important;font-size:inherit!important}
#caSched .fsch{text-align:center;margin:4px 0 14px}#caSched .fsch div{justify-content:center}
html:not(.yg) .fsch span{background:#FFF3D6;color:#2B2320;box-shadow:inset 0 0 0 1px #E8C46A}html.yg .fsch span{background:#2A2208;color:#fff;box-shadow:inset 0 0 0 1px #F5C342}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v16 ok')
