# Real Money build, step 11 (after rmv7.py):
#  1) Photo entries are free. Up to 3 photos in play at a time (in the qualifiers or through to a Final).
#     A photo gets 3 qualifier tries; if it doesn't go through, it's out and its spot frees up.
#     Every 20 votes earns an extra spot (bank up to 3), used when all 3 spots are full.
#  2) Free $1 Final entry for coin players now costs 250 coins, with a progress bar on the Vote screen.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""var SLOT_BASE = 3, PASS_VOTES = 20, PASS_MAX = 3, HEAT_RUNS = 3;
const inPlay = () => (S.photos || []).filter(p => ['heats', 'q'].includes(rcRec(p.id).st)).length;
function passes() { if (S.pv0 == null) { S.pv0 = S.votes || 0; S.pUsed = 0; } let n = Math.floor(((S.votes || 0) - S.pv0) / PASS_VOTES) - (S.pUsed || 0); if (n > PASS_MAX) { S.pUsed = (S.pUsed || 0) + n - PASS_MAX; n = PASS_MAX; } return Math.max(0, n); }
const passNext = () => { passes(); return PASS_VOTES - (((S.votes || 0) - S.pv0) % PASS_VOTES); };
function spotsHTML() { const n = inPlay(), x = passes(), y = isYoungW(), v = y ? 'judge' : 'vote';
  return `<div class="ms-spots"><div><b>📷 Photos in play: ${n} of ${SLOT_BASE}</b><small>${n < SLOT_BASE ? `Entering is free · ${SLOT_BASE - n} spot${SLOT_BASE - n === 1 ? '' : 's'} open` : x ? `All ${SLOT_BASE} spots full · you have <b>${x} extra spot${x === 1 ? '' : 's'}</b> from ${v}s` : `All ${SLOT_BASE} spots full · ${v} ${passNext()} more for an extra spot`}</small></div><em>${x ? `+${x}` : ''}</em></div>`; }
function fbBarHTML() { if (isCash()) return ''; const g = Math.floor(S.gems || 0), ok = g >= FREE_BET_COINS, pct = Math.min(100, Math.round(100 * g / FREE_BET_COINS));
  return `<button class="fb-bar ${ok ? 'ok' : ''}" id="fbBar"><span class="fb-t"><b>🎟️ ${ok ? 'Your free $1 Final entry is ready' : 'Free $1 Final entry'}</b><em>${ok ? 'Use it ›' : `${g} / ${FREE_BET_COINS} 🟡`}</em></span><i class="fb-tr"><i style="width:${pct}%"></i></i></button>`; }
setInterval(() => { const c = document.getElementById('fbBar'); if (!c || !S) return; const h = fbBarHTML(); if (!h) { c.remove(); return; } const t = document.createElement('div'); t.innerHTML = h; const n = t.firstElementChild; if (n.innerHTML !== c.innerHTML) { c.className = n.className; c.innerHTML = n.innerHTML; } }, 800);
document.addEventListener('click', e => { if (e.target.closest('#fbBar')) { e.preventDefault(); e.stopPropagation(); if ((S.gems || 0) >= FREE_BET_COINS) ppOpen(); else toast(`${isYoungW() ? 'Judge' : 'Vote'} and win free qualifiers to earn coins. ${FREE_BET_COINS - Math.floor(S.gems || 0)} 🟡 to go.`); } }, true);
function fcNotify() {""", 1)

# 1) free entries with spots
RA("const free = !S.showFreeUsed; if (!free && (S.gems || 0) < SHOW_ENTRY) { runOut('gems', `You need ${SHOW_ENTRY - Math.floor(S.gems || 0)} more coins`, null, SHOW_ENTRY - (S.gems || 0)); return; }\n  if (free) S.showFreeUsed = 1; else { S.gems -= SHOW_ENTRY; paintGems(); }\n  const r = rcRec(id); r.st = 'heats';",
   "if (inPlay() >= SLOT_BASE) { if (!passes()) { toast(`All ${SLOT_BASE} spots are in play. ${y ? 'Judge' : 'Vote'} ${passNext()} more to earn an extra spot.`); return; } S.pUsed = (S.pUsed || 0) + 1; }\n  const r = rcRec(id); r.st = 'heats'; r.runs = 0;")
RA("else toast(`🎀 ${rcName(p)} finished ${ppOrd(pl)} in its qualifier. Next qualifier in ${HEAT_EVERY} votes.`);",
   "else { r.runs = (r.runs || 0) + 1; if (r.runs >= HEAT_RUNS) { r.st = null; toast(`🎀 ${rcName(p)} finished ${ppOrd(pl)} · that was its last qualifier try. Its spot is free for a new photo.`); } else toast(`🎀 ${rcName(p)} finished ${ppOrd(pl)} in its qualifier · ${HEAT_RUNS - r.runs} ${HEAT_RUNS - r.runs === 1 ? 'try' : 'tries'} left.`); }")
RA("if (r.st === 'heats') return { cls: 'h', ic: '🎀', t: hs ? `Qualifiers: ${hs}` : 'In the qualifiers', s: `Next qualifier in",
   "if (r.st === 'heats') return { cls: 'h', ic: '🎀', t: hs && r.runs ? `Qualifiers: ${hs} · ${HEAT_RUNS - r.runs} ${HEAT_RUNS - r.runs === 1 ? 'try' : 'tries'} left` : `In the qualifiers · ${HEAT_RUNS} tries`, s: `Next qualifier in")
RA("$('#roAgain').onclick = () => { r.st = 'heats'; save(); toast('🎀 Back in the qualifiers!'); stableOpen(); };",
   "$('#roAgain').onclick = () => { popClose(); showEnter(x.pid); };")
RA("Enter<small>${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</small>", "Enter<small>free</small>")
RA("📷 Enter a new photo to compete · ${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</button>",
   "📷 Enter a new photo to compete · free</button>${spotsHTML()}")
RA("<em class=\"${ok ? '' : 'need'}\">${free ? 'Free' : `${SHOW_ENTRY} 🟡`}</em>", "<em>Free</em>")
RA("Win a qualifier and you get <b>10% of its real entries</b>.</p></div>`;",
   "Win a qualifier and you get <b>10% of its real entries</b>. Entering is free: up to ${SLOT_BASE} photos in play, ${HEAT_RUNS} qualifier tries each, and an extra spot for every ${PASS_VOTES} ${isYoungW() ? 'judge' : 'vote'}s.</p></div>`;")

# 2) free $1 Final entry at 250 coins + progress bar on the Vote screen
RA("FREE_BET_COINS = 500;", "FREE_BET_COINS = 250;")
RA("${qsChipHTML()}<div class=\"tot-h\">", "${qsChipHTML()}${fbBarHTML()}<div class=\"tot-h\">")
RA("pick the top 3 of 9`", "pick the top 3 of 6`")

s = s.replace('</style>', """.ms-spots{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:-4px 0 12px;padding:8px 12px;border-radius:14px;text-align:left;background:rgba(127,127,127,.1)}.ms-spots b{display:block;font-size:.9rem}.ms-spots small{font-size:.76rem;opacity:.85}.ms-spots em{font-style:normal;font-weight:900;font-size:1.1rem}
.fb-bar{display:block;width:100%;margin:6px 0 8px;padding:9px 12px 10px;border-radius:14px;border:0;font:inherit;text-align:left;cursor:pointer}.fb-t{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.fb-t b{font-size:.9rem}.fb-t em{font-style:normal;font-weight:800;font-size:.85rem;white-space:nowrap}.fb-tr{display:block;height:8px;border-radius:5px;margin-top:6px;overflow:hidden}.fb-tr i{display:block;height:100%;border-radius:5px;transition:width .5s}
html:not(.yg) .fb-bar{background:#FFF6DC;color:#2B2320;box-shadow:inset 0 0 0 1.5px #E2B33C}html:not(.yg) .fb-tr{background:#F0E2B8}html:not(.yg) .fb-tr i{background:#E2A21C}html:not(.yg) .fb-bar.ok{background:#E8F3EA;box-shadow:inset 0 0 0 2px #2F6B3F}html:not(.yg) .fb-bar.ok .fb-tr i{background:#2F6B3F}
html.yg .fb-bar{background:#2A2208;color:#fff;box-shadow:inset 0 0 0 1.5px #F5C342}html.yg .fb-tr{background:#4A3C12}html.yg .fb-tr i{background:#F5C342}html.yg .fb-bar.ok{background:#10301F;box-shadow:inset 0 0 0 2px #21C77A}html.yg .fb-bar.ok .fb-tr i{background:#21C77A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v8 ok')
