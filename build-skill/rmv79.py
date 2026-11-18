# Real Money build, step 82 (after rmv78.py): align the remaining screens with PhotoPicks.
#  - Voting uses only photos from the Final categories (Pets, Nature & landscapes, Garden & flowers), and the prompt names
#    that category ("Pets · tap your pick") instead of old challenge names like "Best Travel & Cottage".
#  - Coins menu: "Coin challenge" (put your 72 photo against a rival) removed; photo scores no longer exist.
#  - Finalists page: "Show your photos, free · Photos need 70+" becomes the framing message.
#  - Account: Wins–losses and Qualified photos become Prize money and Framed photos; "Competitions" opens the Finals tab;
#    "Coin store" removed (coins are never sold).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
FIN_OK = "(i => !!finCatOf(SEED[i]))"
RA("S.order = JPOOL.slice().sort(() => Math.random() - 0.5);", f"S.order = (JPOOL.filter({FIN_OK}).length > 5 ? JPOOL.filter({FIN_OK}) : JPOOL.slice()).sort(() => Math.random() - 0.5);")
s = s.replace("function fcNotify() {", f"""function finCatOf(x) {{ const z = x && SHOW_ROT.find(z => (z.seed || []).includes(x.cat)); return z ? z.k : null; }}
try {{ if (S && S.order && S.order.some(i => !{FIN_OK}(i))) {{ const o = S.order.filter({FIN_OK}); if (o.length > 5) {{ S.order = o; S.jIdx = 0; save(); }} }} }} catch (e) {{}}
function fcNotify() {{""", 1)
RA("${esc(CHAL[pa.cat] || 'Photo challenge')}", "${esc(finCatOf(pa) ? showName(finCatOf(pa)) : (CHAL[pa.cat] || 'Photo'))}")
RA("if (f && !isCash() && !newbie()) I.push({ ic: '🏅', t: 'Coin challenge'", "if (false && f) I.push({ ic: '🏅', t: 'Coin challenge'")
RA("<b>📷 Show your photos, free</b><span>Top 2 in each qualifier go through. Finalists’ creators share <b>10% of the prize pool</b><br>Photos need ${SHOW_MIN}+ · entry is free</span>",
   "<b>📷 Your photo could be a finalist</b><span>Frame a photo to enter its category’s qualifiers and earn a share of <b>10% of the prize pool</b><br>${frameFree() ? 'Your first frame is free' : `Framing costs ${FRAME_COINS} coins`}</span>")
RA("<div><b>${S.bw}–${S.bl}</b><span>Wins–losses</span></div><div><b>${qn}</b><span>Qualified photos</span></div>",
   "<div><b>${money((S.earn || []).reduce((a, e) => a + e.amt, 0))}</b><span>Prize money</span></div><div><b>${(S.photos || []).filter(p => p.framed).length}</b><span>Framed photos</span></div>")
RA('<button class="btn quiet block" id="mC">Competitions</button><button class="btn quiet block" id="mS">Coin store</button>',
   '<button class="btn quiet block" id="mC">🎀 Finals</button><button class="btn quiet block" id="mS" style="display:none">Coin store</button>')
RA("$('#mC').onclick = () => openComps(null);", "$('#mC').onclick = () => { closeSheet(); finalsTab(); };")
open(d + 'yofi-real.html', 'w').write(s); print('rm v79 ok')
