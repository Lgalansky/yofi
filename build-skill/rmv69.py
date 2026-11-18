# Real Money build, step 72 (after rmv68.py): fixes from the run-through.
#  1. Shop button in the coins menu said "Get more coins" but opens the cash shop: now "Add cash"; shop copy talks about Finals.
#  2. Pops no longer collide: qualifier auto-open, Final results and own-photo results wait until nothing is open
#     (pop, sheet, flow, Choose your Final) and for 2.5 s after anything closes.
#  3. A win is shown once: the extra "Winner!" pop between the reveal and the result is gone (kept for the first ever cash win).
#  4. Age question: PhotoPicks copy (18+) and a navy Continue button instead of the old pink gradient.
#  5. Qualifier result: clearer free-pick line with the coin balance and where to find it.
#  6. Final pick tiles: form numbers labelled "Form" and the legend explains them.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# 1
RA('<button class="link ug-buy" id="ugBuy">Get more coins</button>', '<button class="link ug-buy" id="ugBuy">💵 Add cash</button>')
RA("cash: ['Add cash', 'Play blue ribbon challenges, friends and tournaments. Coins can’t be bought: earn them by voting.']",
   "cash: ['Add cash', 'Pick the hourly Finals with real cash, from $2. Coins can’t be bought: earn them by voting.']")
# 2
RA("function popClose() { const c = $('#coach');", "function busyUI() { const fp = document.getElementById('finPick'); return $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || (fp && fp.classList.contains('on')) || Date.now() - (window.__uiT || 0) < 2500; }\nfunction popClose() { window.__uiT = Date.now(); const c = $('#coach');")
RA("function closeSheet() {", "function closeSheet() { window.__uiT = Date.now();")
i = s.index('function finPick'); j = s.index('\nfunction ', i + 10); seg = s[i:j].replace("o.className = '';", "o.className = ''; window.__uiT = Date.now();"); s = s[:i] + seg + s[j:]
RA("if (!S || !S.gatePend || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || $('#panes').dataset.at !== 'judge') return;",
   "if (!S || !S.gatePend || busyUI() || $('#panes').dataset.at !== 'judge' || Object.values(S.pp || {}).some(x => !x.done && Date.now() >= ppDue(x))) return;")
RA("if (!S || !S.pp || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on')) return;", "if (!S || !S.pp || busyUI()) return;")
RA("if (!S || !S.races || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on')) return;", "if (!S || !S.races || busyUI()) return;")
# 3
RA("() => pay ? heroWin(`+${pay} coins`, `${right} of 3 in the exact spot`, () => gateResultShow(G, picks)) : gateResultShow(G, picks)", "() => gateResultShow(G, picks)")
RA("prize ? (S.firstCash ? heroWin(`You won ${money(prize)}`, `${TR.mine.lab} · real cash`, () => ppResultShow(e)) : (", "prize ? (S.firstCash ? ppResultShow(e) : (")
# 4
RA("We use this to suggest challenges you’ll enjoy. We never show it to other members.", "PhotoPicks is for adults 18+. We use this to tailor what you see, and never show it to other members.")
# 5
RA("<p>🎟️ You have enough for a free Final pick · it’s in your coins</p>", "<p>🎟️ You have <b>${Math.floor(S.gems)} coins</b>: enough for a free Final pick. Tap your coins at the top to use it.</p>")
# 6
RA('<span class="pp-cap"><span class="rf">${formHTML(p.form)}</span>', '<span class="pp-cap"><span class="rf"><small class="rf-l">Form</small>${formHTML(p.form)}</span>')
RA('Popularity: picked to win', 'Form = last 4 finishes · 🔥 = share picking it to win')
s = s.replace('</style>', """html body .ob .btn.block{background:#1E3A6E!important;background-image:none!important;color:#fff!important;-webkit-text-fill-color:#fff;box-shadow:none!important}html body .ob .btn.block:disabled{opacity:.4}
html body .ob h1{color:#14213D!important;-webkit-text-fill-color:#14213D}html body .ob .ob-ages button[aria-pressed="true"]{box-shadow:inset 0 0 0 2px #1E3A6E!important;background:#E3EAF5!important;color:#1E3A6E!important}
html body .ug-buy{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}
.rf-l{font-size:.68rem;font-weight:800;margin-right:3px;opacity:.75;text-transform:uppercase;letter-spacing:.04em}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v69 ok')
