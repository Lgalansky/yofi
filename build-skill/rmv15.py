# Real Money build, step 18 (after rmv14.py): vote-first tutorial for new players.
#  S.tut: 1 vote -> (5 votes) 2 first qualifier -> 3 first Final pick (free, no coins) -> 4 result + upload prompt -> 9 done.
#  - New players open on Vote. Qualifiers no longer need the player to have a photo.
#  - First qualifier after 5 votes (then every 10).
#  - First Final pick is free (no coins).
#  - Final result offers: get your own photo in a Final. A player's first photo enters a qualifier free, no 70+ needed.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""const ffree = () => !S.firstEntry && !Object.values(S.rc || {}).some(r => r.st || (r.f && r.f.length));
function tutInit() { if (!S || S.tut != null) return; S.tut = ((S.votes || 0) < 5 && !(S.photos || []).length && !Object.keys(S.pp || {}).length) ? 1 : 9; save(); }
setInterval(() => { try { tutInit();
  if (!S.tut || S.tut >= 9 || S.tutPop || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on')) return;
  const p = (S.photos || []).find(x => photoShow(x) && !rcRec(x.id).st); if (!p || !ffree()) return; S.tutPop = 1; save(); const y = isYoungW();
  celebrate({ src: p.src, score: p.s.total, title: 'Your first qualifier is free', text: `No ${y ? 'enhancing' : 'touch-ups'} needed for your first photo: it goes straight into the <b>${esc(showName(photoShow(p)))}</b> qualifiers. ${y ? 'Judges' : 'Voters'} send the top 2 to the hourly <b>Final</b>, where every finalist’s creator shares <b>10% of the prize pool</b>.`,
    cta: '🎀 Enter it free', onCta: () => { closeFlow(); showEnter(p.id); setTimeout(() => { go('judge'); renderJudge(); toast(`🎀 ${rcName(p)} is in! ${y ? 'Judge' : 'Vote'} to see its qualifier.`); }, 1400); }, later: 'Later' });
} catch (e) {} }, 1500);
function fcNotify() {""", 1)

# open on Vote for new players too
RA("if (S.user && S.gbDone && $('#panes').dataset.at === 'gallery'", "if (S.user && (S.gbDone || (S.tut || 0) < 9) && $('#panes').dataset.at === 'gallery'")
# qualifiers for everyone, first after 5 votes
RA("if (S.gtN >= GATE_EVERY && S.photos && S.photos.length) { S.gtN = 0; S.gatePend = 1; }",
   "if (S.gtN >= (S.tut === 1 ? 5 : GATE_EVERY)) { S.gtN = 0; S.gatePend = 1; if (S.tut === 1) S.tut = 2; }")
RA("need: Math.max(1, GATE_EVERY - (S.gtN || 0)), per: GATE_EVERY", "need: Math.max(1, (S.tut === 1 ? 5 : GATE_EVERY) - (S.gtN || 0)), per: S.tut === 1 ? 5 : GATE_EVERY")
# first qualifier result -> first Final pick free
RA("function gtUpsell() { const g = ppGame(), nm = raceName(g.sl);", "function gtUpsell() { const g = ppGame(), nm = raceName(g.sl);\n  if (S.tut === 2) return `<p class=\"gq-n\">Those photos race for real cash in the hourly Final. Your first pick is on us.</p><button class=\"btn block pc-go\" id=\"gtFin\">🎟️ Your first Final pick · free</button>`;")
RA("const freeOk = (S.gems || 0) >= FREE_BET_COINS && fqLeft() > 0;", "const freeOk = ((S.gems || 0) >= FREE_BET_COINS && fqLeft() > 0) || S.tut === 2;")
RA("${n3 && freeOk ? '' : 'disabled'}>🎟️ Free $1 pick · ${FREE_BET_COINS} 🟡</button>${!fqLeft() ?",
   "${n3 && freeOk ? '' : 'disabled'}>${S.tut === 2 ? '🎟️ Your first Final pick · free' : `🎟️ Free $1 pick · ${FREE_BET_COINS} 🟡`}</button>${S.tut === 2 ? '<p class=\"pp-r\">Your first $1 pick is on us. Top scores share the prize pool in real cash.</p>' : !fqLeft() ?")
RA("if (picks.length < 3 || (S.gems || 0) < FREE_BET_COINS) return;", "if (picks.length < 3 || ((S.gems || 0) < FREE_BET_COINS && S.tut !== 2)) return;")
RA("if (!fqLeft()) return; fqClaim(); rec(1, true);", "if (S.tut === 2) { S.tut = 3; save(); rec(1, true); return; } if (!fqLeft()) return; fqClaim(); rec(1, true);")
# first Final result -> get your own photo in a Final
RA("    <button class=\"btn block ${cashP ? 'pc-go' : 'pc-real'}\" id=\"ppNext\">",
   "    ${S.tut === 3 ? `<div class=\"tut-up\"><b>📷 Get your own photo in a Final</b><span>Every finalist’s creator gets paid. Your first photo goes straight into a qualifier, free.</span><button class=\"btn block pc-go\" id=\"ppUp\">📷 Add a photo</button></div>` : ''}\n    <button class=\"btn block ${cashP ? 'pc-go' : 'pc-real'}\" id=\"ppNext\">")
RA("$('#ppNext').onclick = () => { popClose(); raceCard(); };", "if (S.tut === 3) { S.tut = 4; save(); } if ($('#ppUp')) $('#ppUp').onclick = () => { popClose(); S.frameHint = { cats: ['pets'], lab: 'Pets', frame: 'Pets' }; save(); pickPhoto(true); }; $('#ppNext').onclick = () => { popClose(); raceCard(); };")
# first photo: free entry without 70+
RA("  if (p.s.total < SHOW_MIN) { S.cur = p.id;", "  const ff = ffree(); if (p.s.total < SHOW_MIN && !ff) { S.cur = p.id;")
RA("  const r = rcRec(id); r.st = 'heats'; r.runs = 0;", "  S.firstEntry = 1; if ((S.tut || 9) < 9) S.tut = 9;\n  const r = rcRec(id); r.st = 'heats'; r.runs = 0;")
RA("can = !r.st && SH && !SH.soon && p.s.total >= SHOW_MIN;", "can = !r.st && SH && !SH.soon && (p.s.total >= SHOW_MIN || ffree());")

s = s.replace('</style>', """.tut-up{border-radius:16px;padding:10px 12px;margin:8px 0 10px;text-align:left}.tut-up b{display:block;font-size:1rem}.tut-up span{display:block;font-size:.84rem;margin:2px 0 8px;opacity:.9}
html:not(.yg) .tut-up{background:#E6F0DF;color:#2B2320;box-shadow:inset 0 0 0 1.5px #2F6B3F}html.yg .tut-up{background:#10301F;color:#fff;box-shadow:inset 0 0 0 1.5px #21C77A}
</style>""", 1)
# landing: lead with voting
RA('<h1>Your photos could win real cash</h1><p class="ca-sub">Choose a category to add your first photo.</p>',
   '<h1>Pick the winners. Win real cash.</h1><p class="ca-sub">Vote on photos, predict the crowd’s top 3 and play the hourly Final. Free to start.</p><button class="btn block ca-any ca-vote" onclick="rmStartVote()">🗳️ Start voting · free</button><p class="ca-sub ca-or">Or add your first photo: it goes into a qualifier free.</p>')
s = s.replace("function fcNotify() {", "function rmStartVote() { if (!S.user) S.user = { h: 'guest' + Math.floor(1000 + Math.random() * 9000), guest: 1 }; tutInit(); save(); openApp(); setTimeout(() => { go('judge'); renderJudge(); }, 60); }\nwindow.rmStartVote = rmStartVote;\nfunction fcNotify() {", 1)
s = s.replace('</style>', '.ca-vote{margin:6px 0 4px}.ca-or{margin-top:14px!important}\n</style>', 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v15 ok')
