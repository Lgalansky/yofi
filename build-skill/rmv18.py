# Real Money build, step 21 (after rmv17.py): website + newbie flow + Final pick screen changes.
# Landing: no "Free to start."; buttons Start voting / Enter with your own photo and win the prize / Watch the hourly Final live;
#   next 6 Finals in a horizontal scrolling row; Skill leftovers ("Or choose any photo") hidden.
# Newbie: no interest picker; category picker shows only the Final categories; every new upload is asked for a name;
#   vote cards show the photo name; first photo gets 150 coins to improve it, and once improved it goes straight into
#   the next Final in its category (no qualifiers).
# Final pick: each finalist shows photo name + @username; 🔥 popularity %; no real-money button for coin players.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

# ---------- landing
RA('Vote on photos, predict the crowd’s top 3 and play the hourly Final. Free to start.', 'Vote on photos, predict the crowd’s top 3 and play the hourly Final.')
RA('<p class="ca-sub ca-or">Or add your first photo: it goes into a qualifier free.</p>',
   '<button class="btn block ca-b2" onclick="rmEnterOwn()">📷 Enter with your own photo and win the prize</button><button class="btn block ca-b2" onclick="rmWatch()">🔴 Watch the hourly Final live</button>')
s = s.replace("function fcNotify() {", r"""function rmEnterOwn() { const k = finNext(1)[0].k; window.__preCat = showHint(k).cats[0]; yWL(); }
function rmWatch() { if (!S.user) S.user = { h: 'guest' + Math.floor(1000 + Math.random() * 9000), guest: 1 }; tutInit(); save(); openApp(); setTimeout(() => { go('judge'); renderJudge(); raceCard(); }, 80); }
window.rmEnterOwn = rmEnterOwn; window.rmWatch = rmWatch;
function fcNotify() {""", 1)
# horizontal row of the next 6 Finals
RA("return `<p class=\"caf-h\">Next Finals · tap one to add your photo</p><div class=\"caf-g\">${SHOW_ROT.map(x => ({ k: x.k, sl: finFor(x.k) })).sort((a, b) => a.sl - b.sl).map(x => {",
   "return `<p class=\"caf-h\">Next Finals · tap one to enter your photo</p><div class=\"caf-g\">${finNext(6).map(x => {")

# ---------- newbie flow
RA("if (S.likes || !S.obDone) { f.click(); return; }", "{ f.click(); return; }")
RA("${PICKCATS.map(k =>", "${(isYoungW() ? ['pets', 'travel'] : ['pets', 'night', 'fitness']).map(k =>")
RA("Pick the competition category it fits. Not sure? Choose Any category and it can enter the open competitions.", "Pick the Final it’s for: Pets, Nature & landscapes or Garden & flowers.")
RA('<span class="tot-o">@', '<span class="tot-o">${x.title ? `<b>${esc(x.title)}</b> · ` : \'\'}@')
RA("if (!p || !ffree()) return; S.tutPop = 1;", "if (true) return; S.tutPop = 1;")
RA("const ffree = () => !S.firstEntry", "const ffree = () => !S.ffPid && !S.firstEntry")
RA("if (p && p.s.total >= SHOW_MIN && photoShow(p) && !rcRec(p.id).st && inPlay() < SLOT_BASE)", "if (p && p.id !== S.ffPid && p.s.total >= SHOW_MIN && photoShow(p) && !rcRec(p.id).st && inPlay() < SLOT_BASE)")
RA("Every finalist’s creator gets paid. Your first photo goes straight into a qualifier, free.", "Every finalist’s creator gets paid. We’ll give you 150 coins to improve your first photo, then it goes straight into a Final.")
s = s.replace("function fcNotify() {", r"""const FF_GIFT = 150;
function nameAsk(p) { const y = isYoungW();
  openSheet(`<div class="nm"><img src="${p.src}" alt=""><h2>Name your photo</h2><p>Voters and pickers see this name, and it’s shown with your photo in the Final.</p><input id="nmIn" maxlength="28" placeholder="e.g. Beach buddy" autocomplete="off"><button class="btn block pc-go" id="nmGo">Save name</button></div>`);
  const go2 = () => { const v = ($('#nmIn').value || '').trim(); p.title = v || `${crownName(p.cat || 'any')} photo`; save(); closeSheet(); if (typeof renderStudio === 'function') try { renderStudio(); } catch (e) {} };
  $('#nmGo').onclick = go2; $('#nmIn').onkeydown = e => { if (e.key === 'Enter') go2(); }; setTimeout(() => { try { $('#nmIn').focus(); } catch (e) {} }, 200); }
setInterval(() => { try {
  if (!S || !S.user || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || $('#landing').style.display !== 'none') return;
  const un = (S.photos || []).find(p => !p.title && !p.nmAsk && p.at && Date.now() - p.at < 864e5); if (un) { un.nmAsk = 1; save(); nameAsk(un); return; }
  const y = isYoungW();
  if (!S.ffGift && !S.firstEntry && !Object.values(S.rc || {}).some(r => r.st || (r.f && r.f.length))) { const p = (S.photos || []).find(x => photoShow(x) && x.title && !rcRec(x.id).st); if (p) { const sl = rcSlotFor(p);
    S.ffGift = 1; S.ffPid = p.id; S.ffBase = p.s.total; S.gems = (S.gems || 0) + FF_GIFT; save(); paintGems();
    celebrate({ src: p.src, score: p.s.total, title: `${FF_GIFT} coins to improve your photo`, text: `${y ? 'Enhance' : 'Touch up'} <b>${esc(p.title)}</b> and it goes <b>straight into the ${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>, no qualifiers. Every finalist’s creator shares <b>10% of the prize pool</b>, and the top 3 win <b>$10 · $5 · $2</b>.`,
      cta: `✨ ${y ? 'Enhance' : 'Improve'} my photo`, onCta: () => { closeFlow(); S.cur = p.id; save(); go('studio'); renderStudio(); }, later: 'Later' }); return; } }
  if (S.ffPid && !S.ffDone) { const p = (S.photos || []).find(x => x.id === S.ffPid); if (!p) { S.ffDone = 1; save(); return; }
    if (p.s.total > S.ffBase && !rcRec(p.id).st && photoShow(p)) { S.ffDone = 1; S.firstEntry = 1; S.tut = 9; const sl = rcSlotFor(p); S.races = S.races || {}; S.races[sl] = { pid: p.id, at: Date.now() }; const r = rcRec(p.id); r.st = 'q'; r.sl = sl; save();
      celebrate({ src: p.src, score: p.s.total, title: 'Through to the Final!', text: `<b>${esc(p.title)}</b> improved to <b>${p.s.total}</b> and goes straight into the <b>${raceName(sl)} ${esc(showName(photoShow(p)))} Final</b>. Watch it live, and pick the top 3 in the Final that’s on now.`,
        cta: '🎀 See the Finalists', onCta: () => { closeFlow(); raceCard(); }, later: y ? 'Keep judging' : 'Keep voting', onLater: () => { closeFlow(); go('judge'); renderJudge(); } }); } }
} catch (e) {} }, 1500);
function fcNotify() {""", 1)

RA("gi(k)}<span>${pcatName(k)}</span></button>`).join", "gi(k)}<span>${esc(showName(photoShow({ cat: k })) || pcatName(k))}</span></button>`).join")
# ---------- Final pick screen
RA('<span class="pp-cap"><span class="rf">${formHTML(p.form)}</span><b>${bk[i]}%</b></span>',
   '<span class="pp-nm"><b>${esc(p.t)}</b><small>@${esc(p.h)}</small></span><span class="pp-cap"><span class="rf">${formHTML(p.form)}</span><b class="pop" title="Popularity: share of players picking it to win">🔥 ${bk[i]}%</b></span>')
RA('<div class="pp-g g6">', '<p class="pp-leg">🔥 Popularity: % of players picking it to win</p><div class="pp-g g6">')
RA('<em>${bk[i]}% fav</em>', '<em>🔥 ${bk[i]}%</em>')
RA("\n        <button class=\"btn block pc-real\" id=\"ppReal\" ${n3 ? '' : 'disabled'}>💵 Pick for real · from $1</button>", "")
RA("${e && e.free && !cash ? `<button class=\"btn block pc-real\" id=\"ppMore\">💵 Add to your pick · from $1</button>` : ''}", "")

s = s.replace('</style>', """html #landing button.btn.ca-b2{margin:8px 0 0!important;background:#FFFFFF!important;background-image:none!important;color:#2D4E86!important;box-shadow:inset 0 0 0 2px #2D4E86!important;font-size:1rem!important}
#landing .ca-tap,#landing .ca-free,#landing .ca-any:not(.ca-vote){display:none!important}#landing .ca-fin{margin-top:18px}
.caf-g{display:flex!important;overflow-x:auto;gap:10px;scroll-snap-type:x mandatory;padding:2px 2px 8px;-webkit-overflow-scrolling:touch}.caf-g .caf-t{flex:0 0 42%;scroll-snap-align:start}
.nm{text-align:center;padding:4px 4px 10px}.nm img{width:120px;height:120px;object-fit:cover;border-radius:16px;display:block;margin:0 auto 10px}.nm h2{margin:0 0 4px}.nm p{margin:0 0 12px;opacity:.85;font-size:.92rem}
.nm input{width:100%;box-sizing:border-box;font:inherit;font-size:1.05rem;padding:12px 14px;border-radius:14px;border:1.5px solid rgba(127,127,127,.45);margin:0 0 12px;background:#fff;color:#2B2320}
.pp-nm{display:block;text-align:left;padding:5px 6px 0;line-height:1.15}.pp-nm b{display:block;font-size:.84rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pp-nm small{font-size:.72rem;opacity:.8}
.pp-leg{font-size:.74rem;opacity:.8;margin:2px 0 6px}.tot-o b{font-weight:800}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v18 ok')
