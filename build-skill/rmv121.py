# Real Money build, step 124 (after rmv120.py): no screen jump when the photo picker opens.
#  Choosing a category on "Choose your Final" keeps that list on screen, highlights the chosen category
#  ("Choose your photo…") and opens the iPhone photo picker over it. The screen only changes once a photo is
#  chosen: straight to "Preparing your photo…". Cancel the picker and you're still on the list.
#  From the landing page, the app opens behind the list when the list appears, not when the picker opens.
#  (Replaces rmv120's move-to-Gallery-first.)
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("  if (fromStudio && $('#app').classList.contains('on')) { try { if (typeof popClose === 'function' && document.querySelector('#coach.on')) popClose(); if ($('#flow').classList.contains('on')) closeFlow(); if ($('#panes').dataset.at !== 'gallery') go('gallery'); renderMyShow(); } catch (e) {} }\n", "")
# landing: open the app behind the list when the list appears
RA("function rmEnterOwn() { finPick(); }",
   "function rmEnterOwn() { if ($('#landing').style.display !== 'none' || !$('#app').classList.contains('on')) { if (!S.user) { S.user = { h: 'guest' + Math.floor(1000 + Math.random() * 9000), guest: 1 }; tutInit(); save(); } openApp(); go('gallery'); try { renderMyShow(); } catch (e) {} } finPick(); }")
# category tap: keep the list, highlight the choice, open the picker over it
RA("o.querySelectorAll('[data-fpk]').forEach(b => b.onclick = () => { const k = b.dataset.fpk; o.className = ''; window.__uiT = Date.now(); window.__preCat = showHint(k).cats[0];",
   "o.querySelectorAll('[data-fpk]').forEach(b => b.onclick = () => { const k = b.dataset.fpk; o.querySelectorAll('.fp-c').forEach(x => x.classList.toggle('sel', x === b)); window.__uiT = Date.now(); window.__preCat = showHint(k).cats[0];")
RA("<em>${ppPool(g.players)} prize pool</em></span><i aria-hidden=\"true\">›</i></button>",
   "<em>${ppPool(g.players)} prize pool</em><u class=\"fp-sel\">📷 Choose your photo…</u></span><i aria-hidden=\"true\">›</i></button>")
# photo chosen: now leave the list
RA("  img = await fitCrop(img); if (!img) { URL.revokeObjectURL(url); return; }\n",
   "  { const fp = document.getElementById('finPick'); if (fp) fp.className = ''; if (document.querySelector('#coach.on')) try { popClose(); } catch (x) {} }\n  img = await fitCrop(img); if (!img) { URL.revokeObjectURL(url); return; }\n")
s = s.replace('</style>', """#finPick .fp-sel{display:none;text-decoration:none;font-weight:900;color:#1E3A6E;font-size:.85rem;margin-top:2px}
#finPick .fp-c.sel{box-shadow:inset 0 0 0 2.5px #1E3A6E;background:#E3EAF5}#finPick .fp-c.sel .fp-sel{display:block}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v121 ok')
# brand-new player from the landing page: answer the age question first, then the category list appears
s = open(d + 'yofi-real.html').read()
RA("try { renderMyShow(); } catch (e) {} } finPick(); }",
   "try { renderMyShow(); } catch (e) {} } const ag = () => document.querySelector('#ageGate.on'); if (!ag()) { finPick(); return; } const w = setInterval(() => { if (!ag()) { clearInterval(w); finPick(); } }, 250); }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v121 pass2 ok')
