# Real Money build, step 140 (after rmv136.py): Stage 1 of "your photos earn money" — remove picks and side games.
#  Removed from reach (code left in place, entry points redirected):
#  - Cash and coin Final picks (Top 3 and Winner), odds, the free Final pick ticket, the newbie free-pick journey.
#    Any old pick entry point now opens Photo games.
#  - Coin Pick and Quick Sprint (Quick Sprint → Match Race), the game rotation and the unused-coins pop-up.
#  - Energy was already unlimited. Framing is now always free.
#  New player path: vote 10 pairs → "Your first Match Race is on us" (25 🟡 gift, coin Match Race).
#  Finals tab → "Play": Photo games first, then the live Final to watch (finalists, "Vote to decide it").
#  Vote-screen strip: "Your first Match Race · in N votes" for new players, then "Photo games · race real players".
#  Landing, coins menu, Add cash and Final pop-ups reworded: no pick / odds wording.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# new-player journey: 10 votes → free Match Race
RA("if (S.tut === 1 && S.gtN >= FP_VOTES) { S.gtN = 0; S.tut = 2; S.fpPend = 1; }", "if (S.tut === 1 && S.gtN >= FP_VOTES) { S.gtN = 0; S.tut = 9; S.fmPend = 1; }")
# coins menu: no Coin Pick / Quick Sprint
i = s.index("  if (!newbie()) I.push({ ic: '🎯', t: 'Coin Pick',"); j = s.index("\n", i); s = s[:i] + s[j + 1:]
i = s.index("  if (!newbie()) I.push({ ic: '⚡', t: 'Quick Sprint',"); j = s.index("\n", i); s = s[:i] + s[j + 1:]
RA("Keep voting to earn coins for free Final picks.", "Keep voting to earn coins for Photo games.")
RA("Coins get you <b>free Final picks</b> and <b>frame your photos</b>. Tap your free pick to use it.", "Coins get you into <b>Photo games</b>: race real players on photo pairs.")
RA("toast('🟡 Unlocked: free Final picks, Quick Sprint and coin challenges · tap your coins')", "toast('🟡 Unlocked: Photo games · tap your coins')")
RA("'Pick the Finals with real cash, from $2. Coins can’t be bought: earn them by voting.'", "'Play Photo games for real cash, from $1. Coins can’t be bought: earn them by voting.'")
RA("It starts as soon as 6 photos win their qualifiers. Picks open then.", "It starts as soon as 6 photos win their qualifiers. The crowd’s votes decide the order.")
# framing always free
RA("const frameFree = () => !S.frameUsed;", "const frameFree = () => true;")
# race card: watch + vote, no pick
RA("<p class=\"rc-jp\">🎯 Win with 2 photos in the top 3, at least 1 in its exact spot</p><button class=\"btn block pc-go\" id=\"rcGo\">${e ? '🔴 Watch live' : own ? '🔴 Watch your photo run' : `🎀 Pick the top 3 · ${cash ? 'pick from $2' : 'free pick'}`}</button>",
   "<p class=\"rc-jp\">⚖️ The crowd’s votes decide the order · finalists’ creators share the prize</p><button class=\"btn block pc-go\" id=\"rcGo\">⚖️ Vote to decide it</button>")
RA("$('#rcGo').onclick = () => ppOpen();", "$('#rcGo').onclick = () => { popClose(); go('judge'); renderJudge(); };")
# tab name
i = s.index('<button id="segCompete"'); j = s.index('<span>Finals</span></button>', i); s = s[:j] + '<span>Play</span></button>' + s[j + len('<span>Finals</span></button>'):]
# landing
L = [("<h1 class=\"lp-h\">Pick the winning photos.<em>Win real cash.</em></h1><p class=\"lp-sub\">Pick your favourite. Cheer it on in the Final.</p>",
      "<h1 class=\"lp-h\">Your photos can earn.<em>Your eye can win cash.</em></h1><p class=\"lp-sub\">Vote on photos, race real players, and enter your own shots.</p>"),
     ("<p class=\"lp-cap lp2-cap\">Which photo will take first place?</p>", "<p class=\"lp-cap lp2-cap\">Which photo would the crowd pick?</p>"),
     ("<h2>Start here: judge photos.</h2><p>Judge 10 photos to earn a free pick in the Final. Then add your own photo and race it.</p>",
      "<h2>Start here: vote on photos.</h2><p>Every vote earns coins and sharpens your eye. After 10 votes, your first Match Race is on us.</p>"),
     ("<h2>Pick the winners.</h2><p>A new Final whenever 6 finalists are in. Pick the top 3 of 6 with real cash, from $2. Win with 2 photos in the top 3, at least 1 in its exact spot. Every win pays more than your pick.</p>",
      "<h2>Race real players.</h2><p>Everyone gets the same photo pairs. Pick the crowd’s choice, right and fast. 1 v 1 or up to 50 players, from $1. Win up to 15× in the Grand National.</p>"),
     ("onclick=\"rmPickNow()\">Pick the Final · from $2 <span aria-hidden=\"true\">→</span></button>", "onclick=\"rmPickNow()\">Play Photo games · from $1 <span aria-hidden=\"true\">→</span></button>"),
     ("<h2>Your photo could win the Final.</h2><p>Enter your photo and compete for the cash prize.</p>", "<h2>Your photo could win the Final.</h2><p>Enter your photo free. Win your qualifier, race in the Final, share the prize.</p>"),
     ("<small>Pets, Nature or Garden</small>", "<small>Pets or Nature</small>"),
     ("<small>Frame it for 200 coins</small>", "<small>Framing is free</small>"),
     ("<p>Choose your favourite. Pick your winner.</p>", "<p>Today’s finalists. The crowd’s votes decide the order.</p>"),
     ("<p>Top pickers this week.</p>", "<p>Top players this week.</p>"),
     ("I picked the top 3 in the Garden Final and won $48. I check in every morning with my coffee.", "I won $48 in the Grand National on a Sunday morning. I check in every day with my coffee."),
     ("I judge a few photos with my tea and use my free pick every day. The grandkids think I’m an expert.", "I vote on a few photos with my tea and play a Match Race or two. The grandkids think I’m an expert."),
     ]
for a, b in L: RA(a, b)
i = s.index("<summary>How do entries and cash prizes work?"); j = s.index("</details>", i)
s = s[:i] + "<summary>How do cash games and prizes work?<i aria-hidden=\"true\"></i></summary><p>Photo games are races between real players on the same photo pairs: pick the photo the crowd chose, right and fast. Entries start at $1 and the prize table is shown before you play. PhotoPicks keeps a 15% fee; the rest is prize money. Entering your own photo is free, and finalists’ creators share the Final’s prize.</p>" + s[j:]
s = s.replace("<div class=\"cs-car\" id=\"csCar\">", "<p class=\"cs-proto\">Example stories (prototype)</p><div class=\"cs-car\" id=\"csCar\">", 1)
# overrides: every old pick / side-game entry point leads to Photo games
s = s.replace("function fcNotify() {", r"""function rotPeek() { return null; }
function freePickUp() {}
function sprintUp() {}
function qsPop() {}
function sprPractice() { try { closeFlow(); } catch (e) {} gmOpen('match', 0); }
function gateOpen() { gmHub(); }
function ppOpen() { try { popClose(); } catch (e) {} setTimeout(gmHub, 150); }
function winOpen() { try { popClose(); } catch (e) {} setTimeout(gmHub, 150); }
function fqStart() { try { closeSheet(); popClose(); } catch (e) {} setTimeout(gmHub, 150); }
function coinTour() { useGems(); }
function rmPickNow() { rmStartVote(); setTimeout(gmHub, 300); }
window.rmPickNow = rmPickNow;
try { if (S && (S.tut === 2 || S.tut === 3)) { S.tut = 9; S.fpPend = 0; save(); } } catch (e) {}
function upNext() { if (!S || !S.user || S.geoBlock) return null;
  if (S.tut === 1) { const nd = Math.max(1, FP_VOTES - (S.gtN || 0)); return { ic: '⚔️', t: '<b>Your first Match Race</b> · free · race 1 player', k: 'fm', need: nd, per: FP_VOTES, em: `in ${nd} vote${nd === 1 ? '' : 's'}` }; }
  return { ic: '🏇', t: '<b>Photo games</b> · race real players', k: 'gm', need: 0, per: 1, em: 'Play' }; }
function upNow() { const x = upNext(); if (!x) return; if (x.k === 'fm') { toast(`${isYoungW() ? 'Judge' : 'Vote'} ${x.need} more for your free Match Race`); return; } gmHub(); }
setInterval(() => { try { if (!S || !S.fmPend || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || $('#panes').dataset.at !== 'judge' || (typeof judging !== 'undefined' && judging)) return; S.fmPend = 0; save();
  celebrate({ src: (SEED.find(z => z.src && z.cat === 'Pets') || {}).src || '', score: '⚔️', title: 'Your first Match Race is on us', text: `You’ve voted on ${FP_VOTES} pairs. Now race a player on the <b>same 10 photo pairs</b>: pick the crowd’s choice, right and fast. Win <b>43 🟡</b>.`,
    cta: '⚔️ Race now · free', onCta: () => { closeFlow(); S.gems = (S.gems || 0) + 25; save(); paintGems(); gmOpen('match', 0); setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 80); }, later: 'Later' }); } catch (e) {} }, 1200);
function finalsTab() { const cur = ppSlot(), g = ppGame(cur), y = isYoungW();
  openFlow(`<div class="fnx"><h1 class="fn-h">Play</h1><p class="fn-s">Race real players on the same photo pairs. Your eye against theirs.</p>${gmCardsHTML()}
    <div class="fn-live"><div class="fn-top"><span class="fn-k">● Live now · ${raceName(cur)} Final</span><b class="fn-cat">${SHOW_IC[g.k] || '🎀'} ${esc(showName(g.k))}</b></div>
      <div class="fn-ph">${g.ph.map(p => `<img src="${p.src}" alt="">`).join('')}</div>
      <p class="fn-s2">${y ? 'Judges' : 'Voters'} decide the order. The finalists’ creators share the prize.</p>
      <button class="btn block fn-nv" id="fnVote">⚖️ Vote to decide it</button><div style="text-align:center"><button class="link fn-lk" id="fnCard">See the finalists ›</button></div></div>
    <details class="g4-how2 fn-how"><summary>How Finals work</summary><p>Photos that win their qualifiers race in a Final, 6 at a time. ${y ? 'Judges' : 'Voters'} decide the order. The finalists’ creators share the prize. Enter your own photo for free from your Gallery.</p></details></div>`, false);
  $('#flow').classList.add('astab'); ['segJudge', 'segStudio', 'segGallery'].forEach(id => $('#' + id).setAttribute('aria-pressed', 'false')); $('#segCompete').setAttribute('aria-pressed', 'true'); setTimeout(() => { $('#ptitle').textContent = 'Play'; }, 0);
  const B = $('#flowBody'); B.querySelector('#fnVote').onclick = () => { closeFlow(); go('judge'); renderJudge(); }; B.querySelector('#fnCard').onclick = () => raceCard(); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.fn-ph{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin:8px 0}.fn-ph img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px}.fn-s2{font-size:.86rem;text-align:center;margin:4px 0 10px}
.cs-proto{font-size:.72rem;opacity:.6;text-align:center;margin:-4px 0 6px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v137 ok')
# landing: the live Final's pick pool line no longer belongs under "Race real players"
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #lpLive{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v137 pass2 ok')
# coins menu: no "Free Final pick" row
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", "function raceBetRowHTML() { return ''; }\nfunction fcNotify() {", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v137 pass3 ok')
