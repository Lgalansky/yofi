# Simpler Vote page (test copy): only the Wins track on the page; energy and tickets in the wallet;
# energy bar only when low; no head-to-head countdown; progress dots only on Compete; 1 free entry a day from voting.
d='/tmp/claude-0/-home-user-yofi/c69be753-0b48-5242-b029-4f4be89f4655/scratchpad/'
s=open(d+'yofi-preview.html').read()
def R(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
# 1 ticket a day from voting
R("S.votes++; S.tixV = (S.tixV || 0) + 1; if (S.tixV >= TIX_EVERY) { S.tixV = 0; S.cashTix = (S.cashTix || 0) + 1; setTimeout(() => { paintTix(); ticketPop(); }, 1600); }",
  "S.votes++; if (S.tixDay !== todayKey()) { S.tixDay = todayKey(); S.tixToday = 0; } if (!S.tixToday) { S.tixV = (S.tixV || 0) + 1; if (S.tixV >= TIX_EVERY) { S.tixV = 0; S.tixToday = 1; S.cashTix = (S.cashTix || 0) + 1; setTimeout(() => { paintTix(); ticketPop(); }, 1600); } }")
R("const pr = document.getElementById('tixProg'); if (pr) pr.textContent = `${v}/${TIX_EVERY}`;",
  "const pr = document.getElementById('tixProg'); const done = S.tixDay === todayKey() && S.tixToday; if (pr) pr.textContent = done ? '✓ today' : `${v}/${TIX_EVERY}`;")
# energy bar only when low
R('<div class="jf-en"><div class="en-top">','<div class="jf-en ${energy() > 10 ? \'en-hide\' : \'en-low\'}"><div class="en-top">')
R("function paintEnPill() { const b = document.getElementById('enNum'); if (b && S) b.textContent = energy(); }","function paintEnPill() { const b = document.getElementById('enNum'); if (b && S) { const e = energy(); b.textContent = e; const p = document.getElementById('enPill'); if (p) p.classList.toggle('low', e <= 10); } }")
s=s.replace('</style>',"""#judge .jf-en{display:none!important}
html .wb.enpl.low{background:#FFE7CF!important;box-shadow:inset 0 0 0 2px #E8822E!important;color:#7A3A00!important;animation:enlow 1.6s ease-in-out infinite}
html.yg .wb.enpl.low{background:#3A1F12!important;color:#FFB36B!important}
@keyframes enlow{50%{box-shadow:inset 0 0 0 2px #E8822E,0 0 12px rgba(232,130,46,.6)}}
@media (prefers-reduced-motion:reduce){html .wb.enpl.low{animation:none}}
#judge .nxu{display:none!important}
html:not([data-at="gallery"]) .stopc.crb.hp{display:none!important}
</style>""",1)
s=s.replace("function fcNotify() {","setInterval(() => { const p = document.getElementById('panes'); if (p) document.documentElement.dataset.at = p.dataset.at || ''; }, 300);\nfunction fcNotify() {",1)
# free entries panel explains the daily limit
s=s.replace("<b>Every ${TIX_EVERY} votes = 1 free entry</b>","<b>Every ${TIX_EVERY} votes = 1 free entry (1 a day)</b>")
open(d+'yofi-simple.html','w').write(s); print('simple ok')

# ---------- energy and tickets move off the main menu onto the Vote page ----------
s=open(d+'yofi-simple.html').read()
def R2(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R2('<div class="tot-h">${nextUpHTML()}','<div class="vstrip"><button class="vs-en ${energy() <= 10 ? \'low\' : \'\'}" id="vsEn" aria-label="Energy. Tap to buy more"><span>⚡</span><b>${energy()}</b><i>+</i></button><button class="vs-tk" id="vsTk" aria-label="Free tournament entries"><span>🎟️</span><b>${S.cashTix || 0}</b><small>${S.tixDay === todayKey() && S.tixToday ? \'✓ today\' : `${S.tixV || 0}/${TIX_EVERY} to next free entry`}</small></button></div><div class="tot-h">${nextUpHTML()}')
s=s.replace("function fcNotify() {","""document.addEventListener('click', e => { if (e.target.closest('#vsEn')) enQuick(); else if (e.target.closest('#vsTk')) useTickets(); });
setInterval(() => { const e = document.querySelector('#vsEn b'); if (e && S) { const n = energy(); e.textContent = n; e.parentElement.classList.toggle('low', n <= 10); } const t = document.querySelector('#vsTk'); if (t && S) { t.querySelector('b').textContent = S.cashTix || 0; t.querySelector('small').textContent = S.tixDay === todayKey() && S.tixToday ? '✓ today' : `${S.tixV || 0}/${TIX_EVERY} to next free entry`; } }, 700);
function fcNotify() {""",1)
s=s.replace('</style>',"""html #shell > .wallet #enPill,html #shell > .wallet #tixPill{display:none!important}
.vstrip{display:flex;justify-content:space-between;gap:8px;margin:0 2px 8px}.vstrip button{display:flex;align-items:center;gap:6px;height:34px;padding:0 12px;border:0;border-radius:999px;font:inherit;cursor:pointer}
.vstrip b{font-weight:900}.vs-en i{font-style:normal;font-weight:900;display:grid;place-items:center;width:20px;height:20px;border-radius:50%;margin-left:2px}.vs-tk small{font-size:.75rem;opacity:.8}
html:not(.yg) .vstrip button{background:#F7F1E7;box-shadow:inset 0 0 0 1.5px #CDBB98;color:#2B2320}html:not(.yg) .vs-en i{background:#2D4E86;color:#fff}
html.yg .vstrip button{background:#1E1236;box-shadow:inset 0 0 0 1.5px #3A2760;color:#fff}html.yg .vs-en i{background:linear-gradient(135deg,#FF2D8E,#7B3CFF);color:#fff}
html .vstrip .vs-en.low{background:#FFE7CF!important;box-shadow:inset 0 0 0 2px #E8822E!important;color:#7A3A00!important}html.yg .vstrip .vs-en.low{background:#3A1F12!important;color:#FFB36B!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('strip ok')

# ---------- Freerolls: 1 ticket per 50 votes (max 1 an hour), a Freeroll schedule, reminders, top 20 by score go to the final ----------
s=open(d+'yofi-simple.html').read()
def R3(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R3("const TIX_EVERY = 25;","const TIX_EVERY = 50;")
# earning: every 50 votes, at most 1 ticket per hour
R3("if (S.tixDay !== todayKey()) { S.tixDay = todayKey(); S.tixToday = 0; } if (!S.tixToday) {",
   "const hk = frHourKey(); if (S.tixDay !== hk) { S.tixDay = hk; S.tixToday = 0; } if (!S.tixToday) {")
R3("S.tixV = (S.tixV || 0) + 1; if (S.tixV >= TIX_EVERY) { S.tixV = 0; S.tixToday = 1; S.cashTix = (S.cashTix || 0) + 1; setTimeout(() => { paintTix(); ticketPop(); }, 1600); }",
   "S.tixV = (S.tixV || 0) + 1; if (S.tixV >= TIX_EVERY) { S.tixV = 0; S.tixToday = 1; S.cashTix = (S.cashTix || 0) + 1; setTimeout(frEarnPop, 1600); }")
s=s.replace("const done = S.tixDay === todayKey() && S.tixToday;","const done = S.tixDay === frHourKey() && S.tixToday;")
s=s.replace("S.tixDay === todayKey() && S.tixToday ? '✓ today'","S.tixDay === frHourKey() && S.tixToday ? `next in ${frMinsLeft()}m`")
s=s.replace("S.tixDay === todayKey() && S.tixToday ? \\'✓ today\\'","S.tixDay === frHourKey() && S.tixToday ? `next in ${frMinsLeft()}m`")
s=s.replace("`${S.tixV || 0}/${TIX_EVERY} to next free entry`","`${S.tixV || 0}/${TIX_EVERY} votes`")
s=s.replace("<b>Every ${TIX_EVERY} votes = 1 free entry (1 a day)</b>","<b>Every ${TIX_EVERY} votes = 1 Freeroll ticket (1 an hour)</b>")
FR = r"""
// ---------- Freerolls ----------
const FR_PRIZE = [10, 6, 4], FR_FINAL = 20;
const frHourKey = (t = Date.now()) => { const x = new Date(t); return `${x.getFullYear()}-${x.getMonth()}-${x.getDate()}-${x.getHours()}`; };
const frMinsLeft = () => 60 - new Date().getMinutes();
function frSlots() { const h = new Date(); h.setMinutes(0, 0, 0); const out = [];
  for (let i = 1; i <= 4; i++) { const st = h.getTime() + i * 3600e3; out.push({ id: 'fr' + st, start: st, fin: st + 50 * 60e3, end: st + 3600e3 }); } return out; }
const frTime = t => new Date(t).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
const frIn = ms => { const m = Math.max(0, Math.round(ms / 60e3)); return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`; };
function frEarnPop() { paintTix && paintTix(); const n = S.cashTix || 0;
  celebrate({ src: (fighters()[0] || {}).src || '', score: '🎟️', title: 'You earned a free ticket!', text: `${TIX_EVERY} votes done. Use it to enter an <b>hourly Freeroll</b> · <b>$20 guaranteed</b>, no cash needed. You have <b>${n}</b> ticket${n === 1 ? '' : 's'}.`,
    cta: '🏆 Choose a Freeroll', onCta: () => frSchedule(), later: 'Keep voting' }); }
function frSchedule() { const L = frSlots(), E = S.frE || {}, n = S.cashTix || 0;
  openSheet(`<div class="ug frs"><h2>🏆 Freerolls</h2><p class="sub">Free photo competitions every hour · <b>$20 guaranteed</b> · 1 🎟️ to enter. You have <b>🎟️ ${n}</b>.</p>
    <div class="frs-how"><span>1</span><p>Enter a photo with a ticket.</p><span>2</span><p>The <b>top ${FR_FINAL}</b> by Yofi score reach the final.</p><span>3</span><p>Voters pick the winners in the last 10 minutes: <b>$10 · $6 · $4</b>.</p></div>
    <div class="frs-l">${L.map(f => { const e = E[f.id]; return `<div class="frs-r ${e ? 'in' : ''}"><div class="frs-t"><b>${frTime(f.start)} Freeroll</b><small>$20 guaranteed · starts in ${frIn(f.start - Date.now())}</small></div>
      ${e ? `<button class="frs-bell ${e.bell ? 'on' : ''}" data-frb="${f.id}" aria-pressed="${!!e.bell}">${e.bell ? '🔔 On' : '🔕 Remind me'}</button><span class="frs-ok">Entered ✓</span>` : `<button class="frs-go" data-fre="${f.id}" ${n ? '' : 'disabled'}>Enter · 1 🎟️</button>`}</div>`; }).join('')}</div>
    ${n ? '' : `<p class="frs-need">No tickets yet · ${TIX_EVERY - (S.tixV || 0)} more votes to your next one.</p>`}</div>`, { full: false });
  document.querySelectorAll('#sheetBody [data-fre]').forEach(b => b.onclick = () => frEnter(L.find(x => x.id === b.dataset.fre)));
  document.querySelectorAll('#sheetBody [data-frb]').forEach(b => b.onclick = () => { const e = (S.frE || {})[b.dataset.frb]; e.bell = !e.bell; save(); toast(e.bell ? '🔔 We’ll tell you when the final starts' : 'Reminder off'); frSchedule(); }); }
function frEnter(f) { const P = S.photos.slice().sort((a, b) => b.s.total - a.s.total);
  if (!P.length) { closeSheet(); toast('Add a photo first, then enter the Freeroll.'); pickPhoto(true); return; }
  openSheet(`<div class="ug frp"><h2>Enter the ${frTime(f.start)} Freeroll</h2><p class="sub">Pick your photo. The <b>top ${FR_FINAL}</b> by score go to the final, so use your best one.</p>
    <div class="frp-g">${P.slice(0, 6).map((p, i) => `<button data-frp="${p.id}" aria-pressed="${i === 0}"><img src="${p.src}" alt=""><b>${p.s.total}</b></button>`).join('')}</div>
    <button class="btn block" id="frpGo">Enter · use 1 🎟️</button><div style="text-align:center"><button class="link" id="frpBack">Back</button></div></div>`, { full: false });
  let sel = P[0].id; document.querySelectorAll('#sheetBody [data-frp]').forEach(b => b.onclick = () => { sel = b.dataset.frp; document.querySelectorAll('#sheetBody [data-frp]').forEach(x => x.setAttribute('aria-pressed', x === b)); });
  $('#frpBack').onclick = frSchedule;
  $('#frpGo').onclick = () => { if (!(S.cashTix > 0)) { toast('You need a ticket'); return; } const p = S.photos.find(x => x.id === sel); S.cashTix--; S.frE = S.frE || {};
    S.frE[f.id] = { pid: p.id, score: p.s.total, start: f.start, fin: f.fin, end: f.end, bell: true }; save(); paintTix && paintTix(); closeSheet();
    celebrate({ src: p.src, score: p.s.total, title: 'You’re in!', text: `Your photo is entered in the <b>${frTime(f.start)} Freeroll</b>. The top ${FR_FINAL} by score reach the final at <b>${frTime(f.fin)}</b>. 🔔 We’ll tell you when it starts.`, cta: 'Keep voting', onCta: () => go('judge'), later: 'See Freerolls', onLater: frSchedule }); }; }
// reminder: when the final of an entered Freeroll starts
setInterval(() => { if (!S || !S.frE) return; const now = Date.now();
  Object.entries(S.frE).forEach(([id, e]) => { if (e.bell && !e.told && now >= e.fin && now < e.end) { e.told = 1; save();
      const rank = e.rank || (e.rank = Math.max(1, Math.round((100 - e.score) * 22 + Math.random() * 30))); const inF = rank <= FR_FINAL, p = S.photos.find(x => x.id === e.pid);
      celebrate({ src: p ? p.src : '', score: '🏆', title: inF ? 'You made the final!' : 'The Freeroll final is live', text: inF ? `Your photo is <b>#${rank}</b> by score. Voting decides the <b>$10 · $6 · $4</b> winners in the next 10 minutes.` : `Your photo finished <b>#${rank}</b> by score. Watch the top ${FR_FINAL} battle it out and vote for your favourite.`, cta: '👀 Watch the final', onCta: () => go('judge'), later: 'Later' }); } }); }, 5000);
"""
R3("function fcNotify() {", FR+"function fcNotify() {")
# ticket sheet and Tournaments page lead to the Freeroll schedule
R3("function useTickets() {", "function useTickets() { return frSchedule(); }\nfunction useTicketsOld() {")
R3("return `<div class=\"tsh\"><h1>Tournaments</h1><p>Guaranteed prizes</p>${nt ? `<button class=\"tsh-tix\" id=\"tshTix\">🎟️ ${nt} free entr${nt === 1 ? 'y' : 'ies'} · <b>Use</b></button>` : ''}</div>",
   "return `<div class=\"tsh\"><h1>Tournaments</h1><p>Guaranteed prizes</p><button class=\"tsh-tix tsh-fr\" id=\"tshTix\">🏆 Freerolls · $20 every hour · 🎟️ ${nt} · <b>${nt ? 'Enter' : 'See'}</b></button></div>")
s=s.replace('</style>',"""#sheetBody .frs-how{display:grid;grid-template-columns:24px 1fr;gap:6px 10px;align-items:center;margin:10px 0 14px}.frs-how span{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;font-weight:900;font-size:.8rem}.frs-how p{margin:0;font-size:.9rem}
.frs-l{display:grid;gap:8px}.frs-r{display:flex;align-items:center;gap:8px;padding:12px;border-radius:14px}.frs-t{flex:1;min-width:0;display:flex;flex-direction:column}.frs-t small{font-size:.8rem;opacity:.8}
.frs-go{border:0;border-radius:999px;padding:9px 14px;font:inherit;font-weight:900;cursor:pointer;color:#fff}.frs-go:disabled{opacity:.4}.frs-bell{border:0;border-radius:999px;padding:7px 10px;font:inherit;font-size:.8rem;font-weight:800;cursor:pointer}.frs-ok{font-weight:900;font-size:.85rem}.frs-need{text-align:center;margin:12px 0 0;opacity:.8}
.frp-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0 16px}.frp-g button{position:relative;border:0;padding:0;border-radius:12px;overflow:hidden;cursor:pointer;aspect-ratio:3/4}.frp-g img{width:100%;height:100%;object-fit:cover;display:block}.frp-g b{position:absolute;right:6px;bottom:6px;padding:2px 8px;border-radius:999px;background:rgba(0,0,0,.6);color:#fff;font-size:.8rem}.frp-g button[aria-pressed="true"]{outline:3px solid #D9A441;outline-offset:-3px}
html:not(.yg) .frs-r{background:#fff;box-shadow:inset 0 0 0 1.5px #CDBB98}html:not(.yg) .frs-r.in{box-shadow:inset 0 0 0 2px #2F6B3F}html:not(.yg) .frs-go{background:#2D4E86}html:not(.yg) .frs-bell{background:#EEF2F9;color:#2D4E86}html:not(.yg) .frs-bell.on{background:#FFF3D1;color:#7A5212}html:not(.yg) .frs-ok{color:#2F6B3F}html:not(.yg) .frs-how span{background:#2D4E86;color:#fff}
html.yg .frs-r{background:#1E1236;box-shadow:inset 0 0 0 1.5px #3A2760}html.yg .frs-r.in{box-shadow:inset 0 0 0 2px #2EE59D}html.yg .frs-go{background:linear-gradient(135deg,#FF2D8E,#7B3CFF)}html.yg .frs-bell{background:#2A1A46;color:#fff}html.yg .frs-bell.on{background:#FFC93C;color:#2A1600}html.yg .frs-ok{color:#2EE59D}html.yg .frs-how span{background:#FF2D8E;color:#fff}
.tsh-fr{background:#2F6B3F!important;color:#fff!important}html.yg .tsh-fr{background:linear-gradient(135deg,#FF2D8E,#7B3CFF)!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('freeroll ok')
s=open(d+'yofi-simple.html').read()
a="return !p || p.closest('script,style,textarea,input,.wm') ? NodeFilter.FILTER_REJECT"
assert s.count(a)==1, s.count(a)
s=s.replace(a,"return !p || p.closest('script,style,textarea,input,.wm,.frs,.frp') ? NodeFilter.FILTER_REJECT")
s=s.replace('</style>','#sheetBody .frs-go,#sheetBody .frs-go *{color:#fff!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s)

# ---------- Freerolls live in the tournament schedule as highlighted rows ----------
s=open(d+'yofi-simple.html').read()
def R4(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R4("  const nt = (S && S.cashTix) || 0;\n  return `<div class=\"tsh\"><h1>Tournaments</h1><p>Guaranteed prizes</p><button class=\"tsh-tix tsh-fr\" id=\"tshTix\">🏆 Freerolls · $20 every hour · 🎟️ ${nt} · <b>${nt ? 'Enter' : 'See'}</b></button></div>",
   """  const nt = (S && S.cashTix) || 0, E = (S && S.frE) || {};
  const frRows = frSlots().slice(0, 2).map(f => { const e = E[f.id]; return `<button class="tsr2 frrow ${e ? 'in' : ''}" data-frrow="${f.id}"><span class="tsr2-t"><span class="fr-tag">FREEROLL</span><b data-tat="${f.start}">${tLeft(f.start)}</b></span>
      <span class="tsr2-p">US$20</span><span class="tsr2-n">${PPL}<small>Top ${FR_FINAL}</small></span><span class="tsr2-e">${e ? (e.bell ? '🔔 ✓' : '✓') : '🎟️ 1'}</span></button>`; }).join('');
  return `<div class="tsh"><h1>Tournaments</h1><p>Guaranteed prizes</p><button class="tsh-tix tsh-fr" id="tshTix">🎟️ ${nt} Freeroll ticket${nt === 1 ? '' : 's'} · ${nt ? '<b>Use below</b>' : `${TIX_EVERY - ((S && S.tixV) || 0)} votes to the next`}</button></div>""")
R4("<div class=\"tsl2\">${rows}</div>`;","<div class=\"tsl2\">${frRows}${rows}</div>`;")
R4("{ const SL = tSlots(); body.querySelectorAll('[data-tsl]')",
   "body.querySelectorAll('[data-frrow]').forEach(b => b.onclick = () => { const f = frSlots().find(x => x.id === b.dataset.frrow), e = (S.frE || {})[b.dataset.frrow]; if (e) { e.bell = !e.bell; save(); toast(e.bell ? '🔔 We’ll tell you when the final starts' : 'Reminder off'); openComps(); return; } if (!(S.cashTix > 0)) { toast(`You need a Freeroll ticket · ${TIX_EVERY - (S.tixV || 0)} more votes`); return; } frEnter(f); });\n  { const SL = tSlots(); body.querySelectorAll('[data-tsl]')")
# tickets now lead to the schedule page, not a separate sheet
R4("function useTickets() { return frSchedule(); }","function useTickets() { if ($('#sheet').classList.contains('on')) closeSheet(); openComps(); }")
s=s.replace("cta: '🏆 Choose a Freeroll', onCta: () => frSchedule(),","cta: '🏆 Choose a Freeroll', onCta: () => openComps(),")
s=s.replace("later: 'See Freerolls', onLater: frSchedule","later: 'See tournaments', onLater: () => openComps()")
s=s.replace("$('#frpBack').onclick = frSchedule;","$('#frpBack').onclick = () => closeSheet();")
s=s.replace('</style>',""".tsr2.frrow .fr-tag{display:block;font-size:.58rem;font-weight:900;letter-spacing:.08em;padding:1px 6px;border-radius:6px;margin-bottom:2px}.tsr2.frrow .tsr2-t{flex-direction:column;align-items:flex-start!important;gap:0!important}.tsr2.frrow .tsr2-t svg{display:none}.tsr2.frrow .tsr2-n small{font-size:.75rem;font-weight:800}
html:not(.yg) .tsr2.frrow{background:#FFF3D1!important;box-shadow:inset 0 0 0 2px #D9A441!important}html:not(.yg) .tsr2.frrow .fr-tag{background:#D9A441;color:#2B2320}html:not(.yg) .tsr2.frrow .tsr2-e{background:#2F6B3F!important;color:#fff!important}
html.yg .tsr2.frrow{background:#2A1A10!important;box-shadow:inset 0 0 0 2px #FFC93C!important}html.yg .tsr2.frrow .fr-tag{background:#FFC93C;color:#2A1600}html.yg .tsr2.frrow .tsr2-e{background:linear-gradient(135deg,#FFC93C,#E9A514)!important;color:#2A1600!important}
.tsr2.frrow.in .tsr2-e{background:transparent!important;box-shadow:inset 0 0 0 2px currentColor}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('fr table ok')
s=open(d+'yofi-simple.html').read()
s=s.replace('</style>','html .wallet.cxw{display:none!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s)

# ---------- swap 1,000 coins for a Freeroll ticket (1 an hour); no vote counter; energy bar back with the loot boxes; ×10 box like the others ----------
s=open(d+'yofi-simple.html').read()
def R5(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
# votes no longer earn tickets
R5("if (S.tixDay !== hk) { S.tixDay = hk; S.tixToday = 0; } if (!S.tixToday) {","if (S.tixDay !== hk) { S.tixDay = hk; S.tixToday = 0; } if (false) {")
# remove the slim line (energy + ticket counter) and bring back the energy bar
s=s.replace('#judge .jf-en{display:none!important}','').replace('#judge .jf-en.en-hide{display:none!important}','')
s=s.replace('</style>','#judge .vstrip{display:none!important}\n</style>',1)
# ×10 box: same look and size as ×3 and ×6
R5("${[2, 5, 9].includes(i) ? 'm m' + (i === 5 ? 5 : i + 1) : ''}","${[2, 5, 9].includes(i) ? 'm m' + (i === 2 ? 3 : 5) : ''}")
s=s.replace("grid-template-columns:1fr 1fr 46px 1fr 1fr 46px 1fr 1fr 1fr 52px!important","grid-template-columns:1fr 1fr 46px 1fr 1fr 46px 1fr 1fr 1fr 46px!important")
# the swap
SW = r"""
const TIX_COINS = 1000;
const swapReady = () => S.swapHr !== frHourKey();
function swapTicket() { if (!swapReady()) { toast(`You can swap again in ${frMinsLeft()} min`); return; }
  if (S.gems < TIX_COINS) { toast(`You need ${(TIX_COINS - Math.floor(S.gems)).toLocaleString()} more coins`); return; }
  window.__spent = true; S.gnMark = 99999; S.gnVote = (S.votes || 0) + 999; S.gems -= TIX_COINS; S.swapHr = frHourKey(); S.cashTix = (S.cashTix || 0) + 1; save(); paintGems(); if ($('#sheet').classList.contains('on')) closeSheet();
  toast(`🎟️ Freeroll ticket added · −${TIX_COINS.toLocaleString()} coins`); setTimeout(() => { openComps(); setTimeout(() => { const r = document.querySelector('[data-frrow]'); if (r) { r.scrollIntoView({ block: 'center' }); r.classList.add('pulse'); } }, 300); }, 400); }
const swapRowHTML = () => `<button class="ug-r ug-swap" id="ugSwap"><span class="ug-i">🎟️</span><span class="ug-t"><b>Freeroll ticket</b><small>${swapReady() ? 'Free entry to an hourly $20 Freeroll · 1 an hour' : `Next swap in ${frMinsLeft()} min`}</small></span><em class="${S.gems < TIX_COINS || !swapReady() ? 'need' : ''}">${TIX_COINS.toLocaleString()} 🟡</em></button>`;
document.addEventListener('click', e => { if (e.target.closest('#ugSwap')) { e.preventDefault(); swapTicket(); } });
"""
R5("function fcNotify() {", SW+"function fcNotify() {")
R5("${I.length ? I.map((x, i) => `<button class=\"ug-r\" data-ug=","${swapRowHTML()}${I.length ? I.map((x, i) => `<button class=\"ug-r\" data-ug=")
# Tournaments banner: no vote counter, offer the swap
R5("${nt ? '<b>Use below</b>' : `${TIX_EVERY - ((S && S.tixV) || 0)} votes to the next`}","${nt ? '<b>Use below</b>' : (swapReady() ? `<b>Swap ${TIX_COINS.toLocaleString()} 🟡</b>` : `next swap in ${frMinsLeft()}m`)}")
s=s.replace("if ($('#tshTix')) $('#tshTix').onclick = () => useTickets();","if ($('#tshTix')) $('#tshTix').onclick = () => { if (!(S.cashTix > 0)) swapTicket(); };",1)
s=s.replace("toast(`You need a Freeroll ticket · ${TIX_EVERY - (S.tixV || 0)} more votes`); return;","toast(`Swap ${TIX_COINS.toLocaleString()} coins for a Freeroll ticket first`); useGems(); return;",1)
s=s.replace('</style>','.tsr2.frrow.pulse{animation:frp 1s ease-in-out 3}@keyframes frp{50%{transform:scale(1.03)}}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('swap ok')

# ---------- + on coins inline; energy + opens the wallet (shop); ×10 box icon in the same family ----------
s=open(d+'yofi-simple.html').read()
s=s.replace('</style>','html #shell > .wallet #gemPill .gplus{transform:none!important;align-self:center!important;margin-left:8px!important}\n</style>',1)
a="if ($('#enPlus')) $('#enPlus').onclick = () => outOfEnergy();"; assert s.count(a)==1
s=s.replace(a,"if ($('#enPlus')) $('#enPlus').onclick = () => openStore();")
a="i === 9 ? '<u>🧰</u>×10' : ''"; assert s.count(a)==1, s.count(a)
s=s.replace(a,"i === 9 ? '<u class=\"bx10\">🎁</u>×10' : ''")
s=s.replace('</style>','html .stk-steps i.m u.bx10{font-size:1.25rem!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('fix ok')
s=open(d+'yofi-simple.html').read()
a="i === 2 ? '<u>📦</u>×3'"; assert s.count(a)==1
s=s.replace(a,"i === 2 ? '<u>🎁</u>×3'")
open(d+'yofi-simple.html','w').write(s)

# ---------- "Use your coins" only lists coin spends; first photo in a new category earns +100 coins ----------
s=open(d+'yofi-simple.html').read()
def R6(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
a=s.index("    ${(() => { const miss = CATS8.filter(k => k !== 'any' && !S.photos.some(p => p.cat === k)); return miss.length ? `<div class=\"ug-cat\">")
b=s.index("})()}\n", a)+len("})()}\n")
s=s[:a]+s[b:]
R6("📷 Upload photo</button>","📷 Upload <i class=\"nc-b\">+100</i></button>",3)
R6("function showResult(p, o = {}) {","""function showResult(p, o = {}) {
  if (o.fresh && !o.first && p && p.cat && p.cat !== 'any' && !(S.catBonus || []).includes(p.cat) && S.photos.filter(x => x.cat === p.cat).length === 1) {
    S.catBonus = (S.catBonus || []).concat(p.cat); S.gems += 100; save(); setTimeout(() => { paintGems(); gemExplosion(100, { label: `New category · ${crownName(p.cat)}` }); }, 2600); }""")
s=s.replace('</style>','.bcc-go .nc-b{font-style:normal;font-weight:900;padding:1px 6px;border-radius:999px;margin-left:2px;background:rgba(255,255,255,.25)}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('newcat ok')

# ---------- interests before the first photo: the button itself opens the photo library (native tap, works on iPhone) ----------
s=open(d+'yofi-simple.html').read()
def R7(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R7('<button class="btn block" id="obGo2" ${picked.size ? \'\' : \'disabled\'}>${window.__obAfter ? \'Continue\' : \'Start playing\'} · ${picked.size} picked</button>',
   '${window.__obAfter ? `<label class="btn block ob-pick" id="obGo2" for="file" role="button">📷 Choose my photo · ${picked.size} picked</label>` : `<button class="btn block" id="obGo2" ${picked.size ? \'\' : \'disabled\'}>Start playing · ${picked.size} picked</button>`}')
R7("g.querySelector('#obGo2').onclick = () => { if (window.__obAfter) { const f = window.__obAfter; window.__obAfter = null; S.likes = [...picked]; save(); obSort(); g.className = ''; setTimeout(() => g.remove(), 300); f(); return; }",
   "g.querySelector('#obGo2').onclick = () => { if (window.__obAfter) { window.__obAfter = null; S.likes = [...picked]; save(); obSort(); g.className = ''; setTimeout(() => g.remove(), 300); return; }")
R7("const l = e.target.closest('label[for=\"file\"]'); if (l && S.obDone && !S.likes)","const l = e.target.closest('label[for=\"file\"]'); if (l && !l.closest('#ageGate') && S.obDone && !S.likes)")
s=s.replace('</style>','#ageGate label.ob-pick{display:flex!important;align-items:center;justify-content:center;cursor:pointer;text-align:center}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('pick ok')

# ---------- Crowd Picks (coins, fixed payout, in the voting loop) + Crowd Sprints (cash, pooled, every 15 min) ----------
s=open(d+'yofi-simple.html').read()
def R8(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
CR = r"""
// ---------- Crowd Picks & Crowd Sprints (pairs with settled crowd results, so no extra voting needed) ----------
const CP_STAKE = 50, CP_PAY = { 3: 2, 4: 3, 5: 6 }, SPR_MS = 15 * 60e3, SPR_N = 10, SPR_FEE = .15;
function cpRng(seed) { let x = seed % 2147483647 || 7; return () => (x = x * 16807 % 2147483647) / 2147483647; }
function cpPairs(n, seed, close) { const r = cpRng(seed), P = SEED.filter(x => x.src), out = [];
  for (let i = 0; i < n; i++) { const a = P[Math.floor(r() * P.length)]; let b = P[Math.floor(r() * P.length)]; if (b === a) b = P[(P.indexOf(a) + 3) % P.length];
    const share = close ? 52 + Math.floor(r() * 15) : 56 + Math.floor(r() * 22), aWins = r() < .5; out.push({ a, b, pa: aWins ? share : 100 - share }); } return out; }
const sprId = (t = Date.now()) => Math.floor(t / SPR_MS);
function sprPlayers(id, t = Date.now()) { const r = cpRng(id * 31 + 5), base = 14 + Math.floor(r() * 40), frac = Math.min(1, (t - id * SPR_MS) / SPR_MS); return base + Math.floor(frac * (60 + r() * 220)); }
const sprPool = n => Math.floor(n * (1 - SPR_FEE));
const sprLeft = id => Math.max(0, (id + 1) * SPR_MS - Date.now());
const mmss = ms => { const t = Math.ceil(ms / 1000); return `${Math.floor(t / 60)}:${String(t % 60).padStart(2, '0')}`; };
function cpRun(mode) { const sprint = mode === 'sprint', id = sprId(), pairs = sprint ? cpPairs(SPR_N, id * 97 + 13, true) : cpPairs(5, Date.now() % 100000, false);
  let i = 0, right = 0; const t0 = Date.now(), c = $('#coach');
  const draw = () => { const p = pairs[i];
    c.innerHTML = `<div class="cpr" role="dialog" aria-modal="true"><div class="cpr-h"><b>${sprint ? '🎯 Crowd Sprint' : '🎯 Crowd Picks'}</b><span>${sprint ? `Pair ${i + 1} of ${SPR_N} · ${right} right` : `${right} in a row${CP_PAY[right] ? ` · ×${CP_PAY[right]}` : ''}`}</span></div>
      <p class="cpr-q">Which one did the crowd pick?</p>
      <div class="cpr-p">${[['a', p.a, p.pa], ['b', p.b, 100 - p.pa]].map(([k, x, sh]) => `<button data-cp="${k}"><img src="${x.src}" alt=""><span class="cpr-pc" data-sh="${sh}"></span></button>`).join('<span class="cpr-vs">VS</span>')}</div>
      <div class="cpr-steps">${[...Array(sprint ? SPR_N : 5)].map((_, j) => `<i class="${j < i ? 'd' : ''} ${j === i ? 'n' : ''}"></i>`).join('')}</div>
      <div class="cpr-act" id="cprAct">${!sprint ? `<small>Stake ${CP_STAKE} 🟡 · 3 right ×2 · 4 right ×3 · 5 right ×6</small>` : `<small>Same pairs for every player this round · most right wins</small>`}</div></div>`;
    c.classList.add('on', 'cr'); c.onclick = null;
    c.querySelectorAll('[data-cp]').forEach(btn => btn.onclick = () => { if (c.querySelector('.cpr-p.done')) return; const pick = btn.dataset.cp, win = (pick === 'a') === (p.pa >= 50);
      c.querySelector('.cpr-p').classList.add('done'); c.querySelectorAll('.cpr-pc').forEach(e => e.textContent = e.dataset.sh + '%');
      c.querySelectorAll('[data-cp]').forEach(b2 => b2.classList.add(((b2.dataset.cp === 'a') === (p.pa >= 50)) ? 'crowd' : 'lose')); btn.classList.add(win ? 'ok' : 'bad');
      if (win) right++; i++;
      setTimeout(() => { if (sprint) { if (i < SPR_N) draw(); else sprDone(id, right, Date.now() - t0); return; }
        if (!win) { cpEnd(right, 0); return; }
        if (i >= 5) { cpEnd(right, CP_PAY[5]); return; }
        if (right >= 3) { const hd = c.querySelector('.cpr-h span'); if (hd) hd.textContent = `${right} in a row · ×${CP_PAY[right]}`; $('#cprAct').innerHTML = `<button class="bt-cta" id="cpCash">Cash out ${CP_STAKE * CP_PAY[right]} 🟡</button><button class="bt-no" id="cpNext">Keep going · ×${CP_PAY[right + 1]} next</button>`;
          $('#cpCash').onclick = () => cpEnd(right, CP_PAY[right]); $('#cpNext').onclick = draw; } else draw(); }, 1100); }); };
  draw(); }
function cpStart() { if (S.gems < CP_STAKE) { toast(`You need ${CP_STAKE} coins`); return; } S.gems -= CP_STAKE; save(); paintGems(); cpRun('coins'); }
function cpEnd(right, mult) { const c = $('#coach'), won = CP_STAKE * (mult || 0); if (won) { S.gems += won; save(); }
  const ups = right >= 4 && S.cpUp !== todayKey() && !S.geoBlock; if (ups) { S.cpUp = todayKey(); save(); }
  const id = sprId(), n = sprPlayers(id);
  c.innerHTML = `<div class="cpr cpr-end"><h2>${won ? (right >= 5 ? '5 in a row!' : 'Cashed out!') : 'So close!'}</h2><p>${won ? `You read the crowd: <b>+${won} 🟡</b>` : `${right} right before a miss. Your ${CP_STAKE} 🟡 stake is gone.`}</p>
    ${ups ? `<div class="ups" id="cpUps">💵 <span><b>You’ve got a good eye</b><small>Next Crowd Sprint in ${mmss(sprLeft(id))} · $1 entry · $${sprPool(n)} and growing</small></span><span class="go">Try it</span></div>` : ''}
    <button class="bt-cta" id="cpAgain">🎯 Play again · ${CP_STAKE} 🟡</button><button class="bt-no" id="cpBack">Keep voting</button></div>`;
  if (won) setTimeout(() => { paintGems(); gemExplosion(won, { label: 'Crowd Picks' }); }, 300);
  $('#cpAgain').onclick = () => { c.classList.remove('on', 'cr'); cpStart(); }; $('#cpBack').onclick = () => c.classList.remove('on', 'cr');
  if ($('#cpUps')) $('#cpUps').onclick = () => { c.classList.remove('on', 'cr'); openComps(); }; }
function crowdPop() { celebrate({ src: (SEED[6] || {}).src, score: '🎯', title: 'Crowd Picks!', text: `Pick the photo most people chose, 5 in a row. Stake <b>${CP_STAKE} coins</b>, win up to <b>${CP_STAKE * 6} 🟡</b>. Cash out after 3.`, cta: `🎯 Play · ${CP_STAKE} 🟡`, onCta: cpStart, later: 'Keep voting' }); }
function sprEnter() { const id = sprId(), E = S.cs = S.cs || {};
  if (S.geoBlock) { toast('Cash contests aren’t available in your state'); return; }
  if (E[id]) { toast('You’ve played this round · results when it closes'); return; }
  if (sprLeft(id) < 70e3) { toast('This round is closing · join the next one'); return; }
  if ((S.cash || 0) < 1) { openStore('A Crowd Sprint costs $1 cash.'); return; }
  S.cash = +((S.cash || 0) - 1).toFixed(2); E[id] = { at: Date.now() }; save(); paintWallet(); if ($('#sheet').classList.contains('on')) closeSheet(); cpRun('sprint'); }
function sprDone(id, right, ms) { const e = (S.cs || {})[id] || {}; e.score = right; e.ms = ms; S.cs[id] = e; save(); const c = $('#coach');
  c.innerHTML = `<div class="cpr cpr-end"><h2>${right}/${SPR_N} right</h2><p>Results when the round closes in <b>${mmss(sprLeft(id))}</b>. Top 20% share the prize pool.</p><button class="bt-cta" id="cpBack">Keep voting</button></div>`;
  $('#cpBack').onclick = () => c.classList.remove('on', 'cr'); }
function sprSettle() { if (!S || !S.cs) return; Object.entries(S.cs).forEach(([k, e]) => { const id = +k; if (e.paid || e.score == null || Date.now() < (id + 1) * SPR_MS) return;
  const n = sprPlayers(id, (id + 1) * SPR_MS), r = cpRng(id * 7 + 3); let above = 0, tie = 0; for (let i = 0; i < n - 1; i++) { let sc = 0; for (let j = 0; j < SPR_N; j++) if (r() < .6) sc++; if (sc > e.score) above++; else if (sc === e.score) tie++; }
  const rank = 1 + above + Math.floor(tie * Math.min(1, e.ms / 60000)), W = Math.max(1, Math.ceil(n * .2)), pool = sprPool(n);
  let prize = 0; if (rank <= W) { const sum = W * (W + 1) / 2; prize = Math.max(.5, +(pool * (W - rank + 1) / sum).toFixed(2)); }
  e.paid = 1; e.rank = rank; e.prize = prize; e.n = n; if (prize) S.cash = +((S.cash || 0) + prize).toFixed(2); save(); paintWallet();
  if (!$('#coach').classList.contains('on')) celebrate({ src: (SEED[1] || {}).src, score: '🎯', title: prize ? `You won $${prize.toFixed(2)}!` : 'Crowd Sprint results', text: `You finished <b>#${rank}</b> of ${n} with ${e.score}/${SPR_N}. ${prize ? 'Added to your cash.' : `The top ${W} won this time.`}`, cta: '🎯 Play the next Sprint · $1', onCta: () => openComps(), later: 'Keep voting' }); }); }
setInterval(sprSettle, 4000);
const sprRowHTML = () => { const id = sprId(), n = sprPlayers(id), e = (S.cs || {})[id];
  return `<button class="tsr2 sprow" id="sprRow"><span class="tsr2-t"><em class="sp-tag">CROWD SPRINT</em><b data-spl>${mmss(sprLeft(id))}</b></span><span class="tsr2-p">$${sprPool(n)}<small class="sp-up">↑</small></span><span class="tsr2-n">${n}</span><span class="tsr2-e">${S.geoBlock ? '🚫' : e ? (e.score != null ? `✓ ${e.score}/10` : '…') : '$1'}</span></button>`; };
document.addEventListener('click', e => { if (e.target.closest('#sprRow')) { e.preventDefault(); sprEnter(); } });
setInterval(() => { const b = document.querySelector('#sprRow [data-spl]'); if (b) b.textContent = mmss(sprLeft(sprId())); }, 1000);
"""
R8("function fcNotify() {", CR+"function fcNotify() {")
R8("S.votes++;","S.votes++; S.cpN = (S.cpN || 0) + 1;")
R8("if (!comboHit && S.votes >= 12 && fighters().length && tUnlocked() && S.since >= CFG.BATTLE_EVERY) {",
   "if (!comboHit && S.votes >= 15 && (S.cpN || 0) >= 20) { S.cpN = 0; save(); renderJudge(); judging = false; crowdPop(); return; }\n  if (!comboHit && S.votes >= 12 && fighters().length && tUnlocked() && S.since >= CFG.BATTLE_EVERY) {")
R8('<div class="tsl2">${frRows}${rows}</div>','<div class="tsl2">${sprRowHTML()}${frRows}${rows}</div>')
s=s.replace("${swapRowHTML()}","${swapRowHTML()}<button class=\"ug-r\" id=\"ugCp\"><span class=\"ug-i\">🎯</span><span class=\"ug-t\"><b>Crowd Picks</b><small>Pick the crowd’s favourite 5 in a row · win up to ×6</small></span><em>${CP_STAKE} 🟡</em></button>",1)
s=s.replace("document.addEventListener('click', e => { if (e.target.closest('#sprRow'))","document.addEventListener('click', e => { if (e.target.closest('#ugCp')) { e.preventDefault(); if ($('#sheet').classList.contains('on')) closeSheet(); cpStart(); } });\ndocument.addEventListener('click', e => { if (e.target.closest('#sprRow'))",1)
s=s.replace('</style>',""".cpr{width:100%;max-width:420px;margin:auto;padding:18px 14px;border-radius:24px;text-align:center}.cpr-h{display:flex;justify-content:space-between;align-items:center;font-size:.9rem;margin:0 0 6px}.cpr-h b{font-size:1.05rem}
.cpr-q{margin:0 0 10px;font-weight:800;font-size:1.15rem}.cpr-p{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:10px}.cpr-p button{position:relative;border:0;padding:0;border-radius:16px;overflow:hidden;aspect-ratio:3/4;cursor:pointer;transition:transform .2s,opacity .2s}
.cpr-p img{width:100%;height:100%;object-fit:cover;display:block}.cpr-vs{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:.85rem}
.cpr-pc{position:absolute;left:8px;right:8px;bottom:8px;padding:6px;border-radius:12px;font:900 1.4rem/1 inherit;color:#fff;background:rgba(0,0,0,.55)}.cpr-pc:empty{display:none}
.cpr-p button.crowd{box-shadow:inset 0 0 0 4px #2EE59D}.cpr-p button.lose{opacity:.55}.cpr-p button.bad{box-shadow:inset 0 0 0 4px #F0384F}.cpr-p button.ok{transform:scale(1.03)}
.cpr-steps{display:flex;justify-content:center;gap:5px;margin:12px 0 8px}.cpr-steps i{width:10px;height:10px;border-radius:50%;background:rgba(127,127,127,.3)}.cpr-steps i.d{background:#2F6B3F}.cpr-steps i.n{box-shadow:0 0 0 2px #D9A441}
.cpr-act{display:grid;gap:8px;min-height:24px}.cpr-act small{font-size:.8rem;opacity:.8}.cpr-end h2{margin:4px 0 6px;font-size:2rem}.cpr-end p{margin:0 0 14px}.cpr-end{display:grid;gap:8px}.cpr .ups{margin:0 0 6px}
html:not(.yg) .cpr{background:#FBF7F0;color:#2B2320;box-shadow:0 0 0 2px #D9A441}html:not(.yg) .cpr-vs{background:#2D4E86;color:#fff}html:not(.yg) .cpr-end h2{font-family:Fraunces,Georgia,serif;color:#2D4E86}
html.yg .cpr{background:#1E1236;color:#fff;box-shadow:0 0 0 2px #FFC93C}html.yg .cpr-vs{background:linear-gradient(135deg,#FF3FA4,#8B3CFF);color:#fff}html.yg .cpr-end h2{color:#FFC93C}html.yg .cpr-steps i.d{background:#2EE59D}
.ups{padding:12px;border-radius:16px;text-align:left;display:flex;gap:10px;align-items:center;cursor:pointer}.ups b{display:block}.ups small{font-size:.8rem;opacity:.85}.ups .go{margin-left:auto;white-space:nowrap;padding:8px 12px;border-radius:999px;font-weight:900}
html:not(.yg) .ups{background:#EAF3EC;box-shadow:inset 0 0 0 1.5px #2F6B3F;color:#2B2320}html:not(.yg) .ups .go{background:#2F6B3F;color:#fff}html.yg .ups{background:#0E3A2A;box-shadow:inset 0 0 0 1.5px #2EE59D;color:#fff}html.yg .ups .go{background:#2EE59D;color:#06261A}
.tsr2.sprow .tsr2-t{flex-direction:column;align-items:flex-start!important;gap:0!important}.tsr2.sprow .sp-tag{position:static!important;font-style:normal;display:block;font-size:.58rem;font-weight:900;letter-spacing:.06em;padding:1px 6px;border-radius:6px;margin-bottom:2px}.sp-up{font-weight:900;margin-left:2px;color:#2EE59D}
html:not(.yg) .tsr2.sprow{background:#EAF3EC!important;box-shadow:inset 0 0 0 2px #2F6B3F!important}html:not(.yg) .tsr2.sprow .sp-tag{background:#2F6B3F;color:#fff}html:not(.yg) .tsr2.sprow .tsr2-e{background:#2F6B3F!important;color:#fff!important}html:not(.yg) .sp-up{color:#2F6B3F}
html.yg .tsr2.sprow{background:#0E3A2A!important;box-shadow:inset 0 0 0 2px #2EE59D!important}html.yg .tsr2.sprow .sp-tag{background:#2EE59D;color:#06261A}html.yg .tsr2.sprow .tsr2-e{background:#2EE59D!important;color:#06261A!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('crowd ok')

# ---------- quick Sprints on the Vote page; hourly Crowd Championship (prebuy) in Tournaments ----------
s=open(d+'yofi-simple.html').read()
def R9(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
# cpRun handles the hourly championship too
a=s.index("function cpRun(mode) {"); b=s.index("\nfunction cpStart()", a); run=s[a:b]
run=run.replace("const sprint = mode === 'sprint', id = sprId(), pairs = sprint ? cpPairs(SPR_N, id * 97 + 13, true)","const champ = mode === 'champ', sprint = mode === 'sprint' || champ, NN = champ ? CH_N : SPR_N, id = champ ? chId() : sprId(), pairs = sprint ? cpPairs(NN, id * (champ ? 131 : 97) + 13, true)")
run=run.replace("SPR_N","NN").replace("${sprint ? '🎯 Crowd Sprint' : '🎯 Crowd Picks'}","${champ ? '🏆 Crowd Championship' : sprint ? '🎯 Crowd Sprint' : '🎯 Crowd Picks'}")
run=run.replace("sprDone(id, right, Date.now() - t0)","(champ ? chDone : sprDone)(id, right, Date.now() - t0)")
s=s[:a]+run+s[b:]
CH = r"""
// hourly Crowd Championship: buy your seat ahead, play when the hour starts, results at the end of the hour
const CH_MS = 3600e3, CH_ENTRY = 2, CH_N = 15;
const chId = (t = Date.now()) => Math.floor(t / CH_MS);
function chPlayers(id, t = Date.now()) { const r = cpRng(id * 53 + 11), base = 180 + Math.floor(r() * 300), frac = Math.max(0, Math.min(1, 1 - ((id * CH_MS) - t) / CH_MS)); return base + Math.floor(frac * (400 + r() * 900)); }
const chPool = n => Math.floor(n * CH_ENTRY * (1 - SPR_FEE));
const hm = ms => { const m = Math.max(0, Math.ceil(ms / 60e3)); return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`; };
function chBuy() { const E = S.ch = S.ch || {}, cur = chId(), nxt = cur + 1;
  if (S.geoBlock) { toast('Cash contests aren’t available in your state'); return; }
  if (E[cur] && E[cur].score == null) { chPlay(); return; }
  if (E[nxt]) { toast('🔔 You’re booked · we’ll tell you when it starts'); return; }
  if ((S.cash || 0) < CH_ENTRY) { openStore(`The Crowd Championship costs $${CH_ENTRY} cash.`); return; }
  S.cash = +((S.cash || 0) - CH_ENTRY).toFixed(2); E[nxt] = { at: Date.now() }; save(); paintWallet();
  toast(`🏆 Booked for the ${new Date(nxt * CH_MS).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })} Crowd Championship · we’ll remind you`); if ($('#panes').dataset.at === 'comps' || document.getElementById('chRow')) openComps(); }
function chPlay() { const e = (S.ch || {})[chId()]; if (!e || e.score != null) return; if ($('#sheet').classList.contains('on')) closeSheet(); document.querySelectorAll('.coach.on').forEach(c => c.classList.remove('on', 'cr')); cpRun('champ'); }
function chDone(id, right, ms) { const e = S.ch[id]; e.score = right; e.ms = ms; save(); const c = $('#coach');
  c.innerHTML = `<div class="cpr cpr-end"><h2>${right}/${CH_N} right</h2><p>Results when the hour ends in <b>${hm((id + 1) * CH_MS - Date.now())}</b>. Top 20% share the prize pool.</p><button class="bt-cta" id="cpBack">Keep voting</button></div>`;
  $('#cpBack').onclick = () => c.classList.remove('on', 'cr'); }
setInterval(() => { if (!S || !S.ch) return; const now = Date.now();
  Object.entries(S.ch).forEach(([k, e]) => { const id = +k;
    if (!e.told && now >= id * CH_MS && now < (id + 1) * CH_MS && e.score == null && !$('#coach').classList.contains('on')) { e.told = 1; save();
      celebrate({ src: (SEED[1] || {}).src, score: '🏆', title: 'Your Crowd Championship is live!', text: `${CH_N} photo pairs · $${chPool(chPlayers(id))} prize pool · play any time this hour.`, cta: '🏆 Play now', onCta: chPlay, later: 'Later' }); }
    if (!e.paid && e.score != null && now >= (id + 1) * CH_MS) { const n = chPlayers(id, id * CH_MS), r = cpRng(id * 19 + 3); let above = 0, tie = 0;
      for (let i = 0; i < n - 1; i++) { let sc = 0; for (let j = 0; j < CH_N; j++) if (r() < .6) sc++; if (sc > e.score) above++; else if (sc === e.score) tie++; }
      const rank = 1 + above + Math.floor(tie * Math.min(1, e.ms / 90000)), W = Math.max(1, Math.ceil(n * .2)), pool = chPool(n); let prize = 0; if (rank <= W) { const sum = W * (W + 1) / 2; prize = Math.max(1, +(pool * (W - rank + 1) / sum).toFixed(2)); }
      e.paid = 1; e.rank = rank; e.prize = prize; if (prize) S.cash = +((S.cash || 0) + prize).toFixed(2); save(); paintWallet();
      if (!$('#coach').classList.contains('on')) celebrate({ src: (SEED[1] || {}).src, score: '🏆', title: prize ? `You won $${prize.toFixed(2)}!` : 'Championship results', text: `You finished <b>#${rank}</b> of ${n} with ${e.score}/${CH_N}. ${prize ? 'Added to your cash.' : `The top ${W} won this time.`}`, cta: '🏆 Book the next one', onCta: () => openComps(), later: 'Keep voting' }); } }); }, 4000);
const chRowHTML = () => { const cur = chId(), E = S.ch || {}, live = E[cur] && E[cur].score == null, nxt = cur + 1, booked = E[nxt], id = live ? cur : nxt, n = chPlayers(id);
  const lab = live ? `<b>LIVE</b>` : `<b data-chl>${hm(nxt * CH_MS - Date.now())}</b>`;
  return `<button class="tsr2 chrow" id="chRow"><span class="tsr2-t"><em class="sp-tag ch-tag">CROWD CHAMPIONSHIP</em>${lab}</span><span class="tsr2-p">$${chPool(n)}<small class="sp-up">↑</small></span><span class="tsr2-n">${n}</span><span class="tsr2-e">${S.geoBlock ? '🚫' : live ? '▶ Play' : booked ? '🔔 ✓' : `$${CH_ENTRY}`}</span></button>`; };
document.addEventListener('click', e => { if (e.target.closest('#chRow')) { e.preventDefault(); chBuy(); } else if (e.target.closest('#qsChip')) { e.preventDefault(); sprEnter(); } });
const qsChipHTML = () => { if (S.geoBlock) return ''; const id = sprId(), e = (S.cs || {})[id], n = sprPlayers(id);
  return `<button class="qs-chip" id="qsChip">🎯 <span><b>Quick Sprint</b> · 10 pairs · ${e && e.score != null ? `you got ${e.score}/10 · results in <i data-qsl>${mmss(sprLeft(id))}</i>` : `$${sprPool(n)} pool · <i data-qsl>${mmss(sprLeft(id))}</i> left`}</span><em>${e ? '✓' : '$1'}</em></button>`; };
setInterval(() => { document.querySelectorAll('[data-qsl]').forEach(x => x.textContent = mmss(sprLeft(sprId()))); }, 1000);
"""
R9("function fcNotify() {", CH+"function fcNotify() {")
# Tournaments: hourly championship row instead of the quick sprint
R9('<div class="tsl2">${sprRowHTML()}${frRows}${rows}</div>','<div class="tsl2">${chRowHTML()}${frRows}${rows}</div>')
# Vote page: quick sprint chip under the wins track
R9('<div class="vh" id="jRes" aria-live="polite"></div>','${qsChipHTML()}<div class="vh" id="jRes" aria-live="polite"></div>')
# the gentle upsell and the sprint result point to the quick sprint on the Vote page
s=s.replace("if ($('#cpUps')) $('#cpUps').onclick = () => { c.classList.remove('on', 'cr'); openComps(); };","if ($('#cpUps')) $('#cpUps').onclick = () => { c.classList.remove('on', 'cr'); sprEnter(); };",1)
s=s.replace("cta: '🎯 Play the next Sprint · $1', onCta: () => openComps(),","cta: '🎯 Play the next Sprint · $1', onCta: () => { go('judge'); sprEnter(); },",1)
s=s.replace("Next Crowd Sprint in ${mmss(sprLeft(id))} · $1 entry","Quick Sprint · ${mmss(sprLeft(id))} left · $1 entry",1)
s=s.replace('</style>',""".qs-chip{display:flex;align-items:center;gap:8px;width:100%;margin:10px 0 0;padding:10px 12px;border:0;border-radius:14px;font:inherit;font-size:.85rem;text-align:left;cursor:pointer}.qs-chip i{font-style:normal;font-weight:800}.qs-chip em{margin-left:auto;font-style:normal;font-weight:900;padding:5px 12px;border-radius:999px}
html:not(.yg) .qs-chip{background:#EAF3EC;box-shadow:inset 0 0 0 1.5px #2F6B3F;color:#2B2320}html:not(.yg) .qs-chip em{background:#2F6B3F;color:#fff}
html.yg .qs-chip{background:#0E3A2A;box-shadow:inset 0 0 0 1.5px #2EE59D;color:#fff}html.yg .qs-chip em{background:#2EE59D;color:#06261A}
.tsr2.chrow .tsr2-t{flex-direction:column;align-items:flex-start!important;gap:0!important}.tsr2.chrow .ch-tag{position:static!important;font-style:normal;display:block;font-size:.5rem;font-weight:900;letter-spacing:.04em;padding:1px 5px;border-radius:6px;margin-bottom:2px;white-space:nowrap}
html:not(.yg) .tsr2.chrow{background:#EAF3EC!important;box-shadow:inset 0 0 0 2px #2F6B3F!important}html:not(.yg) .tsr2.chrow .ch-tag{background:#2F6B3F;color:#fff}html:not(.yg) .tsr2.chrow .tsr2-e{background:#2F6B3F!important;color:#fff!important}
html.yg .tsr2.chrow{background:#0E3A2A!important;box-shadow:inset 0 0 0 2px #2EE59D!important}html.yg .tsr2.chrow .ch-tag{background:#2EE59D;color:#06261A}html.yg .tsr2.chrow .tsr2-e{background:#2EE59D!important;color:#06261A!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('champ ok')
s=open(d+'yofi-simple.html').read()
a="if (sprLeft(id) < 70e3) { toast('This round is closing · join the next one'); return; }"; assert s.count(a)==1
s=s.replace(a,"if (sprLeft(id) < 30e3) { toast(`Next Quick Sprint starts in ${mmss(sprLeft(id))}`); return; }")
s=s.replace('</style>','#judge .qs-chip{margin:8px 0 4px}\n</style>',1)
open(d+'yofi-simple.html','w').write(s)
s=open(d+'yofi-simple.html').read()
a="<b>Quick Sprint</b> · 10 pairs · ${e && e.score != null ? `you got ${e.score}/10 · results in <i data-qsl>${mmss(sprLeft(id))}</i>` : `$${sprPool(n)} pool · <i data-qsl>${mmss(sprLeft(id))}</i> left`}"
assert s.count(a)==1
s=s.replace(a,"<b>Quick Sprint</b> · ${e && e.score != null ? `${e.score}/10 · results <i data-qsl>${mmss(sprLeft(id))}</i>` : `$${sprPool(n)} · <i data-qsl>${mmss(sprLeft(id))}</i>`}")
s=s.replace('#judge .qs-chip{margin:8px 0 4px}','#judge .qs-chip{margin:6px 0 2px;padding:6px 10px!important;font-size:.8rem!important;white-space:nowrap}#judge .qs-chip em{padding:3px 10px!important}',1)
open(d+'yofi-simple.html','w').write(s)
s=open(d+'yofi-simple.html').read()
a='${qsChipHTML()}<div class="vh" id="jRes" aria-live="polite"></div>'; assert s.count(a)==1
s=s.replace(a,'<div class="vh" id="jRes" aria-live="polite"></div>')
a='<div class="tot-h">${nextUpHTML()}'; assert s.count(a)==1
s=s.replace(a,'${qsChipHTML()}<div class="tot-h">${nextUpHTML()}')
s=s.replace('#judge .qs-chip{margin:6px 0 2px;','#judge .qs-chip{margin:0 0 6px;',1)
open(d+'yofi-simple.html','w').write(s)

# ---------- Quick Sprint: play any time, instant result against 9 players who played the same pairs; fixed prizes per group of 10 ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("NN = champ ? CH_N : NN","NN = champ ? CH_N : SPR_N")
RA("sprint ? '🎯 Crowd Sprint'","sprint ? '🎯 Quick Sprint'")
RA("id = champ ? chId() : sprId()","id = champ ? chId() : sprint ? (window.__qsSet || sprId()) : sprId()")
# replace sprEnter and sprDone
a=s.index("function sprEnter() {"); b=s.index("\nfunction sprDone(", a); s=s[:a]+r"""function sprEnter() {
  if (S.geoBlock) { toast('Cash contests aren’t available in your state'); return; }
  if ((S.cash || 0) < 1) { openStore('A Quick Sprint costs $1 cash.'); return; }
  S.cash = +((S.cash || 0) - 1).toFixed(2); save(); paintWallet(); if ($('#sheet').classList.contains('on')) closeSheet();
  window.__qsSet = Math.floor(Math.random() * 900000) + 1000; cpRun('sprint'); }"""+s[b:]
a=s.index("function sprDone(id, right, ms) {"); b=s.index("\nfunction ", a+10); s=s[:a]+r"""const QS_PAY = [5, 2.5, 1], QS_NAMES = ['nana_bakes', 'max.adventures', 'coco.pup', 'linda.blooms', 'dogdad', 'luna_loves', 'pawprincess', 'catlover22', 'ella.travels', 'sam_snaps', 'jade.k', 'tom_frames'];
function sprDone(id, right, ms) { const r = cpRng(id * 7 + 1), pool = QS_NAMES.slice().sort(() => r() - .5).slice(0, 9);
  const opp = pool.map(h => { let sc = 0; for (let j = 0; j < SPR_N; j++) if (r() < .6) sc++; return { h, sc, ms: 14000 + Math.floor(r() * 26000) }; });
  const all = opp.concat([{ h: 'You', sc: right, ms, me: 1 }]).sort((x, y) => y.sc - x.sc || x.ms - y.ms), rank = all.findIndex(x => x.me) + 1, prize = QS_PAY[rank - 1] || 0;
  if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); save(); setTimeout(paintWallet, 200); }
  const c = $('#coach'), ord = n => n + (n === 1 ? 'st' : n === 2 ? 'nd' : n === 3 ? 'rd' : 'th');
  c.innerHTML = `<div class="cpr cpr-end qs-res"><h2>${prize ? `You won $${prize.toFixed(2)}!` : `${ord(rank)} of 10`}</h2><p>${right}/${SPR_N} right · ${(ms / 1000).toFixed(1)}s · ${prize ? `${ord(rank)} place` : 'top 3 win cash'}</p>
    <div class="qs-lb">${all.map((x, i) => `<div class="${x.me ? 'me' : ''}"><span>${i + 1}</span><b>${x.me ? 'You' : '@' + esc(x.h)}</b><small>${x.sc}/10 · ${(x.ms / 1000).toFixed(1)}s</small><em>${QS_PAY[i] ? '$' + QS_PAY[i].toFixed(2) : ''}</em></div>`).join('')}</div>
    <button class="bt-cta" id="qsAgain">🎯 Play again · $1</button><button class="bt-no" id="cpBack">Keep voting</button></div>`;
  if (prize) setTimeout(() => cashExplosion && cashExplosion(prize, { label: 'Quick Sprint' }), 400);
  $('#qsAgain').onclick = () => { c.classList.remove('on', 'cr'); sprEnter(); }; $('#cpBack').onclick = () => c.classList.remove('on', 'cr'); }"""+s[b:]
# Vote page line: no clock
a=s.index("const qsChipHTML = () => {"); b=s.index("</button>`; };", a)+len("</button>`; };")
s=s[:a]+"const qsChipHTML = () => S.geoBlock ? '' : `<button class=\"qs-chip\" id=\"qsChip\">🎯 <span><b>Quick Sprint</b> · 10 pairs · win up to $5 · instant</span><em>$1</em></button>`;"+s[b:]
RA("Quick Sprint · ${mmss(sprLeft(id))} left · $1 entry · $${sprPool(n)} and growing","Quick Sprint · $1 · win up to $5, result instantly")
s=s.replace("<small>Same pairs for every player this round · most right wins</small>","<small>Same 10 pairs as your 9 opponents · most right wins · ties go to the fastest</small>",1)
s=s.replace('</style>',""".qs-lb{display:grid;gap:3px;margin:4px 0 10px;max-height:46vh;overflow:auto;text-align:left}.qs-lb div{display:grid;grid-template-columns:22px 1fr auto 52px;gap:8px;align-items:center;padding:6px 10px;border-radius:10px;font-size:.85rem}
.qs-lb span{font-weight:900;opacity:.6}.qs-lb small{opacity:.75}.qs-lb em{font-style:normal;font-weight:900;text-align:right}.qs-lb div.me{font-weight:900}
html:not(.yg) .qs-lb div{background:#fff}html:not(.yg) .qs-lb div.me{background:#FFF3D1;box-shadow:inset 0 0 0 2px #D9A441}html:not(.yg) .qs-lb em{color:#2F6B3F}
html.yg .qs-lb div{background:#160B2E}html.yg .qs-lb div.me{background:#2A1A46;box-shadow:inset 0 0 0 2px #FFC93C}html.yg .qs-lb em{color:#2EE59D}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('instant ok')

# ---------- Quick Sprint stakes: $2 / $5 tables, 20% rake, top 3 paid 62.5/25/12.5% of what's left ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
a=s.index("function sprEnter() {"); b=s.index("\nconst QS_PAY", a); s=s[:a]+r"""const QS_STAKES = [2, 5], QS_RAKE = .2, QS_SPLIT = [.625, .25, .125];
const qsPay = st => QS_SPLIT.map(f => +(st * 10 * (1 - QS_RAKE) * f).toFixed(2));
const qsM = v => '$' + (v % 1 ? v.toFixed(2) : v);
function sprEnter(stake) {
  if (S.geoBlock) { toast('Cash contests aren’t available in your state'); return; }
  const c = $('#coach');
  if (!stake) { if ($('#sheet').classList.contains('on')) closeSheet();
    c.innerHTML = `<div class="cpr qs-pick" role="dialog" aria-modal="true"><div class="cpr-h"><b>🎯 Quick Sprint</b><span>10 players · instant</span></div>
      <p class="cpr-q">Pick your table</p>
      <div class="qs-st">${QS_STAKES.map(st => { const p = qsPay(st); return `<button data-qst="${st}"><b>${qsM(st)}</b><span>1st <i>${qsM(p[0])}</i> · 2nd ${qsM(p[1])} · 3rd ${qsM(p[2])}</span></button>`; }).join('')}</div>
      <div class="cpr-act"><small>Same 10 pairs for all 10 players · most right wins · ties go to the fastest. Top 3 paid.</small><button class="bt-no" id="qsX">Not now</button></div></div>`;
    c.classList.add('on', 'cr'); c.onclick = null;
    c.querySelectorAll('[data-qst]').forEach(bt => bt.onclick = () => sprEnter(+bt.dataset.qst)); $('#qsX').onclick = () => c.classList.remove('on', 'cr'); return; }
  if ((S.cash || 0) < stake) { c.classList.remove('on', 'cr'); openStore(`This Quick Sprint table costs ${qsM(stake)} cash.`); return; }
  S.cash = +((S.cash || 0) - stake).toFixed(2); save(); paintWallet(); if ($('#sheet').classList.contains('on')) closeSheet();
  window.__qsStake = stake; window.__qsSet = Math.floor(Math.random() * 900000) + 1000; cpRun('sprint'); }"""+s[b:]
RA("const QS_PAY = [5, 2.5, 1], ","const ")
RA("prize = QS_PAY[rank - 1] || 0;","QS_PAY = qsPay(window.__qsStake || 5), prize = QS_PAY[rank - 1] || 0;")
RA("<em>${QS_PAY[i] ? '$' + QS_PAY[i].toFixed(2) : ''}</em>","<em>${QS_PAY[i] ? qsM(QS_PAY[i]) : ''}</em>")
RA("<h2>${prize ? `You won $${prize.toFixed(2)}!`","<h2>${prize ? `You won ${qsM(prize)}!`")
RA("<button class=\"bt-cta\" id=\"qsAgain\">🎯 Play again · $1</button>","<button class=\"bt-cta\" id=\"qsAgain\">🎯 Play again · ${qsM(window.__qsStake || 5)}</button>")
RA("$('#qsAgain').onclick = () => { c.classList.remove('on', 'cr'); sprEnter(); };","$('#qsAgain').onclick = () => { c.classList.remove('on', 'cr'); sprEnter(window.__qsStake || 5); };")
RA("<b>Quick Sprint</b> · 10 pairs · win up to $5 · instant</span><em>$1</em>","<b>Quick Sprint</b> · win up to $25 · instant</span><em>from $2</em>")
RA("Quick Sprint · $1 · win up to $5, result instantly","Quick Sprint · from $2 · win up to $25, result instantly")
s=s.replace('</style>',""".qs-st{display:grid;gap:8px;margin:6px 0 10px}.qs-st button{display:flex;align-items:center;gap:12px;padding:12px 14px;border:0;border-radius:14px;font:inherit;text-align:left;cursor:pointer}
.qs-st b{font-size:1.35rem;min-width:52px}.qs-st span{font-size:.85rem}.qs-st i{font-style:normal;font-weight:900}.qs-pick .cpr-act small{display:block;margin-bottom:6px}
html:not(.yg) .qs-st button{background:#fff;box-shadow:inset 0 0 0 1.5px #2F6B3F;color:#2B2320}html:not(.yg) .qs-st b,html:not(.yg) .qs-st i{color:#2F6B3F}
html.yg .qs-st button{background:#0E3A2A;box-shadow:inset 0 0 0 1.5px #2EE59D;color:#fff}html.yg .qs-st b,html.yg .qs-st i{color:#2EE59D}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('stakes ok')
s=open(d+'yofi-simple.html').read(); s=s.replace("'🎯 Play the next Sprint · $1'","'🎯 Play a Quick Sprint · from $2'",1); open(d+'yofi-simple.html','w').write(s)

# ---------- Crowd Picks retired from the loop: one free Quick Sprint practice for newbies, then real Quick Sprint invites only (every 50 votes, 15 min apart) ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("if (!comboHit && S.votes >= 15 && (S.cpN || 0) >= 20) { S.cpN = 0; save(); renderJudge(); judging = false; crowdPop(); return; }",
   "if (!comboHit && !S.geoBlock && S.votes >= 15 && (S.cpN || 0) >= (S.qsTried ? 50 : 20) && Date.now() - (S.qsPopAt || 0) > 15 * 60000) { S.cpN = 0; S.qsPopAt = Date.now(); save(); renderJudge(); judging = false; qsPop(); return; }")
RA("function crowdPop() {", r"""function sprPractice() { if ($('#sheet').classList.contains('on')) closeSheet(); window.__qsPractice = 1; window.__qsStake = 2; window.__qsSet = Math.floor(Math.random() * 900000) + 1000; cpRun('sprint'); }
function qsPop() { if (!S.qsTried) celebrate({ src: (SEED[6] || {}).src, score: '🎯', title: 'Try Quick Sprint free', text: `Pick the photo the crowd chose in <b>10 pairs</b>. Have a free practice, then play real players for cash: <b>$2</b> or <b>$5</b> tables, win up to <b>$25</b>.`, cta: '🎯 Practise free', onCta: sprPractice, later: 'Keep voting' });
  else celebrate({ src: (SEED[6] || {}).src, score: '🎯', title: 'Quick Sprint', text: `10 pairs against 9 real players. Top 3 win cash: up to <b>$10</b> on the $2 table, <b>$25</b> on the $5 table.`, cta: '🎯 Play · from $2', onCta: () => sprEnter(), later: 'Keep voting' }); }
function crowdPop() {""")
# Use your coins: no Crowd Picks row
RA("""<button class="ug-r" id="ugCp"><span class="ug-i">🎯</span><span class="ug-t"><b>Crowd Picks</b><small>Pick the crowd’s favourite 5 in a row · win up to ×6</small></span><em>${CP_STAKE} 🟡</em></button>""","")
RA("window.__qsStake = stake; window.__qsSet","window.__qsPractice = 0; window.__qsStake = stake; window.__qsSet")
RA("sprint ? '🎯 Quick Sprint'","sprint ? (window.__qsPractice ? '🎯 Free practice' : '🎯 Quick Sprint')")
# results: practice pays nothing and says what it would have won
RA("if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); save(); setTimeout(paintWallet, 200); }",
   "const pr = window.__qsPractice; if (pr) { S.qsTried = 1; save(); } if (prize && !pr) { S.cash = +((S.cash || 0) + prize).toFixed(2); save(); setTimeout(paintWallet, 200); }")
RA("<h2>${prize ? `You won ${qsM(prize)}!` : `${ord(rank)} of 10`}</h2><p>",
   "<h2>${pr ? (prize ? `You’d have won ${qsM(prize)}!` : `You’d be ${ord(rank)} of 10`) : prize ? `You won ${qsM(prize)}!` : `${ord(rank)} of 10`}</h2>${pr ? `<p class=\"qs-prac\">Free practice · prizes shown for the $2 table</p>` : ''}<p>")
RA("<button class=\"bt-cta\" id=\"qsAgain\">🎯 Play again · ${qsM(window.__qsStake || 5)}</button>",
   "<button class=\"bt-cta\" id=\"qsAgain\">${pr ? '🎯 Play for real' : `🎯 Play again · ${qsM(window.__qsStake || 5)}`}</button>")
RA("sprEnter(window.__qsStake || 5); };","pr ? sprEnter() : sprEnter(window.__qsStake || 5); };")
RA("if (prize) setTimeout(() => cashExplosion","if (prize && !pr) setTimeout(() => cashExplosion")
# Vote page line: new players try it free
RA("instant</span><em>from $2</em>","instant</span><em>${S.qsTried ? 'from $2' : 'Try free'}</em>")
RA("else if (e.target.closest('#qsChip')) { e.preventDefault(); sprEnter(); }","else if (e.target.closest('#qsChip')) { e.preventDefault(); S.qsTried ? sprEnter() : sprPractice(); }")
s=s.replace('</style>',""".qs-prac{margin:-4px 0 4px!important;font-size:.78rem;font-weight:800;opacity:.8}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('practice ok')

# ---------- First Quick Sprint is played for coins (100 in, 500/200/100 out), then cash ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("function sprPractice() { if ($('#sheet').classList.contains('on')) closeSheet();",
   "const QS_COIN = 100, QS_COIN_PAY = [500, 200, 100];\nfunction sprPractice() { if ($('#sheet').classList.contains('on')) closeSheet(); if ((S.gems || 0) < QS_COIN) { toast(`You need ${QS_COIN} coins`); return; } S.gems -= QS_COIN; save(); paintGems();")
RA("title: 'Try Quick Sprint free', text: `Pick the photo the crowd chose in <b>10 pairs</b>. Have a free practice, then play real players for cash: <b>$2</b> or <b>$5</b> tables, win up to <b>$25</b>.`, cta: '🎯 Practise free'",
   "title: 'Try Quick Sprint', text: `Pick the photo the crowd chose in <b>10 pairs</b>, against 9 players. Your first one is for coins: <b>${QS_COIN}</b> in, top 3 win up to <b>${QS_COIN_PAY[0]}</b>. Then play for cash: <b>$2</b> or <b>$5</b> tables, win up to <b>$25</b>.`, cta: `🎯 Play · ${QS_COIN} ${gemIcon('')}`")
RA("'🎯 Free practice'","'🎯 Quick Sprint · coins'")
# results: coin prizes for the first game
RA("if (pr) { S.qsTried = 1; save(); }","if (pr) { S.qsTried = 1; QS_PAY = QS_COIN_PAY; prize = QS_PAY[rank - 1] || 0; if (prize) { S.gems = (S.gems || 0) + prize; setTimeout(paintGems, 200); } save(); }")
RA("QS_PAY = qsPay(window.__qsStake || 5), prize = QS_PAY[rank - 1] || 0;","_qz = 0; let QS_PAY = qsPay(window.__qsStake || 5), prize = QS_PAY[rank - 1] || 0;")
RA("<h2>${pr ? (prize ? `You’d have won ${qsM(prize)}!` : `You’d be ${ord(rank)} of 10`) :",
   "<h2>${pr ? (prize ? `You won ${prize} ${gemIcon('')}` : `${ord(rank)} of 10`) :")
RA("<p class=\"qs-prac\">Free practice · prizes shown for the $2 table</p>","<p class=\"qs-prac\">${prize ? `On the $2 table that’s ${qsM(qsPay(2)[rank - 1])} cash` : 'Top 3 win · on the $2 table 1st wins $10'}</p>")
RA("<em>${QS_PAY[i] ? qsM(QS_PAY[i]) : ''}</em>","<em>${QS_PAY[i] ? (pr ? QS_PAY[i] + ' ' + gemIcon('') : qsM(QS_PAY[i])) : ''}</em>")
RA("${S.qsTried ? 'from $2' : 'Try free'}","${S.qsTried ? 'from $2' : `${QS_COIN} ${gemIcon('')}`}")
s=s.replace("</style>",""".qs-res h2 svg,.qs-lb em svg,.qs-chip em svg,#crGo svg,svg[class=""]{width:1em;height:1em;vertical-align:-.15em}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('coins practice ok')

# ---------- Quick Sprint in voting is 1 v 1: same 10 pairs, best score wins, 20% rake ($2 wins $3.20, $5 wins $8; first one 100 coins wins 160) ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("const qsPay = st => QS_SPLIT.map(f => +(st * 10 * (1 - QS_RAKE) * f).toFixed(2));","const qsPay = st => [+(st * 2 * (1 - QS_RAKE)).toFixed(2)];")
RA("QS_COIN_PAY = [500, 200, 100]","QS_COIN_PAY = [160]")
RA(".sort(() => r() - .5).slice(0, 9);",".sort(() => r() - .5).slice(0, 1);")
RA("text: `Pick the photo the crowd chose in <b>10 pairs</b>, against 9 players. Your first one is for coins: <b>${QS_COIN}</b> in, top 3 win up to <b>${QS_COIN_PAY[0]}</b>. Then play for cash: <b>$2</b> or <b>$5</b> tables, win up to <b>$25</b>.`",
   "text: `1 v 1 against a real player. Pick the photo the crowd chose in <b>10 pairs</b>, best score wins. Your first one is for coins: <b>${QS_COIN}</b> in, win <b>${QS_COIN_PAY[0]}</b>. Then play for cash: <b>$2</b> wins <b>$3.20</b>, <b>$5</b> wins <b>$8</b>.`")
RA("text: `10 pairs against 9 real players. Top 3 win cash: up to <b>$10</b> on the $2 table, <b>$25</b> on the $5 table.`",
   "text: `1 v 1 against a real player · 10 pairs · about 30 seconds. <b>$2</b> wins <b>$3.20</b>, <b>$5</b> wins <b>$8</b>.`")
RA("<b>🎯 Quick Sprint</b><span>10 players · instant</span>","<b>🎯 Quick Sprint</b><span>1 v 1 · instant</span>")
RA("<p class=\"cpr-q\">Pick your table</p>","<p class=\"cpr-q\">Pick your stake</p>")
RA("<span>1st <i>${qsM(p[0])}</i> · 2nd ${qsM(p[1])} · 3rd ${qsM(p[2])}</span>","<span>Beat 1 player, win <i>${qsM(p[0])}</i></span>")
RA("<small>Same 10 pairs for all 10 players · most right wins · ties go to the fastest. Top 3 paid.</small>","<small>You and 1 real player get the same 10 pairs · most right wins · ties go to the fastest.</small>")
RA("<small>Same 10 pairs as your 9 opponents · most right wins · ties go to the fastest</small>","<small>Same 10 pairs as your opponent · most right wins · ties go to the fastest</small>")
RA("(prize ? `You won ${prize} ${gemIcon('')}` : `${ord(rank)} of 10`) : prize ? `You won ${qsM(prize)}!` : `${ord(rank)} of 10`}",
   "(prize ? `You won ${prize} ${gemIcon('')}` : 'So close!') : prize ? `You won ${qsM(prize)}!` : 'So close!'}")
RA("'Top 3 win · on the $2 table 1st wins $10'","'On the $2 table the winner gets $3.20'")
RA("${prize ? `${ord(rank)} place` : 'top 3 win cash'}","${prize ? 'you win' : `@${esc(all.find(x => !x.me).h)} won`}")
RA("<b>Quick Sprint</b> · win up to $25 · instant</span>","<b>Quick Sprint</b> · 1 v 1 · win up to $8</span>")
s=s.replace("Quick Sprint · from $2 · win up to $25, result instantly","Quick Sprint · 1 v 1 from $2 · win up to $8",1)
s=s.replace('</style>',""".qs-lb{max-height:none}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('h2h ok')
s=open(d+'yofi-simple.html').read()
assert s.count('<b>+$${amt.toLocaleString()}</b>')==1
s=s.replace('<b>+$${amt.toLocaleString()}</b>','<b>+$${amt % 1 ? amt.toFixed(2) : amt.toLocaleString()}</b>')
s=s.replace("'🎯 Play for real · on us'","'🎯 Play on us'",1)
open(d+'yofi-simple.html','w').write(s); print('fmt ok')

# ---------- After the first free coin challenge: introduce the category cash pot ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("const cupNext = () => ({ label: '🟡 Earn more coins by judging', go: () => { closeFlow(); go('judge'); renderJudge(); $('#judge').scrollTop = 0; } });",
   "const cupNext = () => ({ label: '🏆 Next: win real cash', go: () => { closeFlow(); potIntro(p); } });")
RA("Your first challenge is <b>free</b>, win <b>${GB_FREE_WIN} coins</b>.`, cta: 'Start now · Free'",
   "Your first challenge is <b>free</b>, win <b>${GB_FREE_WIN} coins</b>. Then go for today’s <b>cash pot</b>.`, cta: 'Start now · Free'")
RA("function openGemBattle(stake, after, opt = {}) {", r"""function potIntro(p) { const L = lgS(), k = (p && CATS8.find(x => fitsTheme(p, x))) || CATS8[0], H = lgHold(k), hp = H.h === 'you' ? '' : lgPhoto(H.h, k);
  setTimeout(() => { openSheet(`<div class="pi"><button class="pi-x" data-shclose aria-label="Close"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <p class="pi-k">Next step · real cash</p><h2 class="pi-h">Win today’s cash pot</h2>
    <div class="pi-card"><span class="pi-c">${gi(k)}<b>${esc(crownName(k))}</b></span><b class="pi-pot">$${Math.round(L.jp[k]).toLocaleString()}</b><small>in today’s pot · paid at midnight · <span data-wk>${dayLeft()}</span> left</small>
      <div class="pi-vs"><figure><img src="${p ? p.src : ''}" alt=""><figcaption>You</figcaption></figure><i>VS</i><figure><img src="${hp}" alt=""><figcaption>@${esc(H.h)}<br>${CRW}blue ribbon</figcaption></figure></div></div>
    <ol class="pi-st"><li><span>1</span><p><b>$1</b> a challenge. <b>85¢</b> goes into today’s pot.</p></li><li><span>2</span><p>Win <b>+1 ⭐</b>, lose <b>−1 ⭐</b>. Beat the blue ribbon holder and <b>your photo goes on the card</b>.</p></li><li><span>3</span><p>At midnight the <b>most ⭐</b> wins <b>half the pot</b>. Everyone on <b>5+ ⭐</b> shares the other half.</p></li></ol>
    <button class="btn block pi-go" id="piGo">${VS_IC}Challenge for the pot · $1</button><div style="text-align:center"><button class="link pi-later" id="piLater">Later · earn coins by judging</button></div></div>`);
    $('#piGo').onclick = () => { closeSheet(); go('gallery'); setTimeout(() => lgCat(k), 350); };
    $('#piLater').onclick = () => { closeSheet(); go('judge'); renderJudge(); $('#judge').scrollTop = 0; };
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet()); }, 380); }
function openGemBattle(stake, after, opt = {}) {""")
s=s.replace('</style>',""".pi{position:relative;padding:6px 4px 4px;text-align:center}.pi-x{position:absolute;right:0;top:0;border:0;background:none;color:inherit;padding:4px;cursor:pointer}
.pi-k{margin:4px 0 2px;font-size:.72rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.pi-h{margin:0 0 12px;font-size:1.6rem;line-height:1.1}
.pi-card{border-radius:18px;padding:12px 12px 10px;margin-bottom:12px}.pi-c{display:inline-flex;align-items:center;gap:6px;font-size:.9rem}.pi-c svg{width:20px;height:20px}
.pi-pot{display:block;font-size:2.6rem;line-height:1.05;margin:4px 0 0}.pi-card>small{display:block;font-size:.78rem;opacity:.85;margin-bottom:10px}
.pi-vs{display:flex;align-items:center;justify-content:center;gap:8px}.pi-vs figure{margin:0;flex:1;max-width:130px}.pi-vs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:14px;display:block}
.pi-vs figcaption{font-size:.75rem;font-weight:800;margin-top:4px;line-height:1.25}.pi-vs figcaption .crw-ic{width:12px;height:14px;vertical-align:-2px;margin-right:2px}.pi-vs>i{font-style:normal;font-weight:900;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;flex:none}
.pi-st{list-style:none;margin:0 0 14px;padding:0;display:grid;gap:8px;text-align:left}.pi-st li{display:flex;gap:10px;align-items:flex-start}.pi-st li>span{flex:none;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:.8rem}.pi-st p{margin:0;font-size:.9rem;line-height:1.35}
.pi-later{margin-top:8px}
html:not(.yg) .pi-k{color:#2F6B3F}html:not(.yg) .pi-card{background:#fff;box-shadow:inset 0 0 0 2px #D9A441}html:not(.yg) .pi-pot{color:#2F6B3F}html:not(.yg) .pi-vs>i{background:#2D4E86;color:#fff}html:not(.yg) .pi-st li>span{background:#2D4E86;color:#fff}html:not(.yg) .pi-vs img{box-shadow:0 0 0 2px #2D4E86}
html.yg .pi-k{color:#2EE59D}html.yg .pi-card{background:#1B0F33;box-shadow:inset 0 0 0 2px #FFC93C}html.yg .pi-pot{color:#2EE59D}html.yg .pi-vs>i{background:#FFC93C;color:#1B0F33}html.yg .pi-st li>span{background:#C13CFF;color:#fff}html.yg .pi-vs img{box-shadow:0 0 0 2px #C13CFF}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('pot intro ok')

# ---------- Quick Sprint screens redone: stake picker, exciting run (clock, race vs opponent, +1, shake, % reveal, dots), Round complete table ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
i=s.index('function sprEnter(stake) {'); j=s.index('function sprDone('); k=s.index('\nfunction ', j+10)
names=s[s.index('const QS_NAMES',i):].split('\n',1)[0]
s=s[:i]+names+'\n'+r"""const QS_X = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';
function sprEnter(stake) {
  if (S.geoBlock) { toast('Cash contests aren’t available in your state'); return; }
  const c = $('#coach');
  if (!stake) { if ($('#sheet').classList.contains('on')) closeSheet();
    let sel = QS_STAKES.includes(window.__qsStake) ? window.__qsStake : QS_STAKES[0];
    c.innerHTML = `<div class="cpr qs2 qs2-pick" role="dialog" aria-modal="true"><button class="qs2-x" id="qsX" aria-label="Close">${QS_X}</button>
      <h2 class="qs2-t">🎯 Quick Sprint</h2><p class="qs2-sub">1 vs 1 · 10 photo pairs</p><h3 class="qs2-q">Choose your entry</h3>
      <div class="qs2-st">${QS_STAKES.map(st => `<button data-qst="${st}"><span><small>Entry</small><b class="e">${qsM(st)}</b></span><i></i><span><small>Winner gets</small><b>${qsM(qsPay(st)[0])}</b></span><em class="rd"></em></button>`).join('')}</div>
      <p class="qs2-rule">Most correct answers wins.<br>Tied score? Fastest player wins.</p>
      <button class="bt-cta qs2-go" id="qsPlay"></button><button class="bt-no" id="qsNo">Not now</button></div>`;
    c.classList.add('on', 'cr'); c.onclick = null;
    const paint = () => { c.querySelectorAll('[data-qst]').forEach(b => b.classList.toggle('on', +b.dataset.qst === sel)); $('#qsPlay').textContent = `Play · ${qsM(sel)} entry`; };
    c.querySelectorAll('[data-qst]').forEach(b => b.onclick = () => { sel = +b.dataset.qst; paint(); }); paint();
    $('#qsPlay').onclick = () => sprEnter(sel); $('#qsX').onclick = $('#qsNo').onclick = () => c.classList.remove('on', 'cr'); return; }
  if ((S.cash || 0) < stake) { c.classList.remove('on', 'cr'); openStore(`Quick Sprint entry is ${qsM(stake)} cash.`); return; }
  S.cash = +((S.cash || 0) - stake).toFixed(2); save(); paintWallet(); if ($('#sheet').classList.contains('on')) closeSheet();
  window.__qsPractice = 0; window.__qsStake = stake; window.__qsSet = Math.floor(Math.random() * 900000) + 1000; qsRun(); }
function qsOpp(id) { const r = cpRng(id * 7 + 1), h = QS_NAMES[Math.floor(r() * QS_NAMES.length)], seq = [...Array(SPR_N)].map(() => r() < .62); return { h, seq, sc: seq.filter(Boolean).length, ms: 18000 + Math.floor(r() * 22000) }; }
function qsRun() { const id = window.__qsSet, pr = window.__qsPractice, pairs = cpPairs(SPR_N, id * 97 + 13, true), O = qsOpp(id), c = $('#coach'), res = [];
  const prize = pr ? `${QS_COIN_PAY[0]} ${gemIcon('')}` : qsM(qsPay(window.__qsStake || 2)[0]);
  let i = 0, right = 0, lock = false; const t0 = Date.now();
  c.innerHTML = `<div class="cpr qs2 qs2-run" role="dialog" aria-modal="true"><h2 class="qs2-t">🎯 Quick Sprint${pr ? ' <small>· coins</small>' : ''}</h2>
    <div class="qs2-prize"><small>🏆 Winner gets</small><b>${prize}</b></div>
    <div class="qs2-stat"><span id="qsPair"></span><span id="qsClock">⏱ 0.0s</span><span class="g" id="qsRight"></span></div>
    <p class="qs2-race" id="qsRace"></p>
    <h3 class="qs2-q">Which photo did the crowd pick?</h3>
    <div class="qs2-p" id="qsP"></div>
    <div class="qs2-fb" id="qsFb"><span class="qs2-fbi">👆</span><span><b>Tap your pick</b><small>Same 10 pairs @${esc(O.h)} played</small></span></div>
    <div class="qs2-dots" id="qsDots"></div><p class="qs2-next" id="qsNext"></p></div>`;
  c.classList.add('on', 'cr'); c.onclick = null;
  const clk = setInterval(() => { const e = $('#qsClock'); if (!e) { clearInterval(clk); return; } e.textContent = '⏱ ' + ((Date.now() - t0) / 1000).toFixed(1) + 's'; }, 100);
  const dots = () => { $('#qsDots').innerHTML = [...Array(SPR_N)].map((_, j) => `<i class="${j < res.length ? (res[j] ? 'ok' : 'bad') : j === res.length ? 'now' : ''}">${j < res.length ? (res[j] ? '✓' : '✕') : ''}</i>`).join(''); };
  const race = () => { const o = O.seq.slice(0, res.length).filter(Boolean).length, df = right - o;
    $('#qsRace').innerHTML = res.length ? `vs <b>@${esc(O.h)}</b> · ${o} correct by now · <span class="${df > 0 ? 'up' : df < 0 ? 'dn' : ''}">${df > 0 ? `you’re ${df} ahead 🔥` : df < 0 ? `you’re ${-df} behind` : 'neck and neck'}</span>` : `vs <b>@${esc(O.h)}</b> · real player · same 10 pairs`; };
  const draw = () => { const p = pairs[i]; lock = false;
    $('#qsPair').textContent = `Pair ${i + 1} of ${SPR_N}`; $('#qsRight').textContent = `${right} correct`; race(); dots(); $('#qsNext').textContent = '';
    const P = $('#qsP'); P.innerHTML = [['a', p.a, p.pa], ['b', p.b, 100 - p.pa]].map(([k, x, sh]) => `<button data-cp="${k}"><img src="${x.src}" alt=""><span class="cpr-pc" data-sh="${sh}"></span><em class="qs2-ck"></em></button>`).join('<span class="qs2-vs">VS</span>');
    P.classList.remove('done'); P.classList.add('in'); setTimeout(() => P.classList.remove('in'), 320);
    P.querySelectorAll('[data-cp]').forEach(btn => btn.onclick = () => { if (lock) return; lock = true;
      const win = (btn.dataset.cp === 'a') === (p.pa >= 50), sh = Math.max(p.pa, 100 - p.pa); res.push(win); if (win) right++; i++;
      P.classList.add('done'); P.querySelectorAll('.cpr-pc').forEach(e => e.textContent = e.dataset.sh + '%');
      P.querySelectorAll('[data-cp]').forEach(b2 => b2.classList.add(((b2.dataset.cp === 'a') === (p.pa >= 50)) ? 'crowd' : 'not'));
      btn.classList.add(win ? 'ok' : 'bad'); if (win) btn.insertAdjacentHTML('beforeend', '<b class="qs2-plus">+1</b>');
      const F = $('#qsFb'); F.className = 'qs2-fb ' + (win ? 'ok' : 'bad');
      F.innerHTML = win ? `<span class="qs2-fbi">✓</span><span><b>Correct!</b><small>You picked the crowd favourite · ${sh}%</small></span>` : `<span class="qs2-fbi">✕</span><span><b>Not this one</b><small>The crowd picked the other photo · ${sh}%</small></span>`;
      $('#qsRight').textContent = `${right} correct`; race(); dots();
      try { navigator.vibrate && navigator.vibrate(win ? 15 : [30, 40, 30]); } catch (e) {}
      $('#qsNext').textContent = i < SPR_N ? 'Next pair…' : 'Counting up…';
      setTimeout(() => { if (!$('#qsP')) return;
        if (i < SPR_N) { F.className = 'qs2-fb'; F.innerHTML = `<span class="qs2-fbi">👆</span><span><b>Tap your pick</b><small>${SPR_N - i} pair${SPR_N - i > 1 ? 's' : ''} to go</small></span>`; draw(); }
        else { clearInterval(clk); sprDone(id, right, Date.now() - t0); } }, 1050); }); };
  draw(); }
function sprDone(id, right, ms) { const O = qsOpp(id), pr = window.__qsPractice, st = window.__qsStake || 2;
  const all = [{ h: O.h, sc: O.sc, ms: O.ms }, { h: 'You', sc: right, ms, me: 1 }].sort((x, y) => y.sc - x.sc || x.ms - y.ms), won = !!all[0].me, pay = pr ? QS_COIN_PAY[0] : qsPay(st)[0];
  if (pr) { S.qsTried = 1; if (won) { S.gems = (S.gems || 0) + pay; setTimeout(paintGems, 200); } save(); }
  else if (won) { S.cash = +((S.cash || 0) + pay).toFixed(2); save(); setTimeout(paintWallet, 200); }
  const c = $('#coach'), diff = Math.abs(O.sc - right), rw = x => x === all[0] ? (pr ? `${pay} ${gemIcon('')}` : qsM(pay)) : '—';
  const box = pr ? `<div class="qs2-box cash"><p class="qs2-bk">🎯 Real cash</p><h3>Now play for real</h3><b class="qs2-big">${qsM(qsPay(2)[0])}</b><span>Winner’s prize</span><small>$2 entry · 1 vs 1 · 10 pairs</small></div>`
    : won ? `<div class="qs2-box win"><p class="qs2-bk">🏆 You won</p><b class="qs2-big">${qsM(pay)}</b><span>Added to your cash</span></div>`
    : `<div class="qs2-box lose"><p class="qs2-bk">So close</p><h3>${diff ? `@${esc(O.h)} won by ${diff}` : `@${esc(O.h)} won on time`}</h3><small>New pairs, new opponent. Run it back?</small></div>`;
  c.innerHTML = `<div class="cpr qs2 qs2-res ${won ? 'won' : 'lost'}" role="dialog" aria-modal="true"><button class="qs2-x" id="qsX" aria-label="Close">${QS_X}</button>
    <h2 class="qs2-t big">Round complete</h2><p class="qs2-sub" id="qsHead">${won ? (pr ? `You won ${pay} ${gemIcon('')}` : `You beat @${esc(O.h)}!`) : `@${esc(O.h)} took this one`}</p>
    <table class="qs2-tb"><thead><tr><th></th><th>Player</th><th>Correct</th><th>Time</th><th>Reward</th></tr></thead><tbody>${all.map((x, j) => `<tr class="${x.me ? 'me' : ''}"><td>${j + 1}</td><td>${x.me ? 'You' : '@' + esc(x.h)}</td><td>${x.sc}/${SPR_N}</td><td>${(x.ms / 1000).toFixed(1)}s</td><td class="rw">${rw(x)}</td></tr>`).join('')}</tbody></table>
    ${box}<button class="bt-cta qs2-go" id="qsAgain">${pr ? 'Play for cash' : `Play again · ${qsM(st)}`}</button><button class="bt-no" id="cpBack">Keep voting</button></div>`;
  if (won && !pr) setTimeout(() => cashExplosion && cashExplosion(pay, { label: 'Quick Sprint' }), 400);
  const shut = () => c.classList.remove('on', 'cr');
  $('#qsAgain').onclick = () => { shut(); pr ? sprEnter() : sprEnter(st); }; $('#cpBack').onclick = shut; $('#qsX').onclick = shut; }"""+s[k:]
RA("window.__qsSet = Math.floor(Math.random() * 900000) + 1000; cpRun('sprint'); }","window.__qsSet = Math.floor(Math.random() * 900000) + 1000; qsRun(); }")
s=s.replace('</style>',""".qs2{position:relative;text-align:center}.qs2-x{position:absolute;right:8px;top:8px;border:0;background:none;color:inherit;padding:4px;cursor:pointer;z-index:2}
.qs2-t{margin:0 0 8px;font-size:1.35rem}.qs2-t.big{font-size:1.75rem;margin:4px 0 6px}.qs2-t small{font-size:.8rem;opacity:.7}
.qs2-sub{margin:0 0 10px;font-size:.92rem;font-weight:700}.qs2-sub svg{width:1em;height:1em;vertical-align:-.15em}.qs2 .qs2-q{margin:8px 0 10px;font-size:1.12rem;line-height:1.2;height:auto;white-space:normal;overflow:visible}
.qs2-prize{border-radius:16px;padding:7px 10px 9px;margin:0 0 8px}.qs2-prize small{display:block;font-size:.72rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.qs2-prize b{display:block;font-size:2.1rem;line-height:1.05}.qs2-prize svg{width:.8em;height:.8em;vertical-align:-.05em}
.qs2-stat{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;border-radius:999px;padding:7px 14px;font-size:.74rem;font-weight:900;letter-spacing:.05em;text-transform:uppercase}.qs2-stat span:first-child{text-align:left}.qs2-stat span:last-child{text-align:right}#qsClock{font-variant-numeric:tabular-nums}
.qs2-race{margin:6px 0 0;font-size:.78rem;min-height:1.2em}.qs2-race span{font-weight:900}
.qs2-p{display:grid;grid-template-columns:1fr auto 1fr;align-items:center}.qs2-p.in button{animation:qsIn .3s ease-out}
.qs2-p button{position:relative;border:0;padding:0;background:none;cursor:pointer;transition:transform .15s}.qs2-p button:active{transform:scale(.97)}
.qs2-p img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:16px;display:block;transition:box-shadow .2s,filter .2s}
.qs2-vs{width:40px;height:40px;margin:0 -12px;z-index:1;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:.85rem;border:3px solid}
.qs2-p .cpr-pc{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);font-weight:900;font-size:.9rem;padding:3px 10px;border-radius:999px;background:rgba(0,0,0,.65);color:#fff;opacity:0;transition:opacity .2s}.qs2-p.done .cpr-pc{opacity:1}
.qs2-p button.crowd img{box-shadow:0 0 0 4px #2F9E55,0 0 20px rgba(47,158,85,.65)}.qs2-p button.bad img{box-shadow:0 0 0 4px #D6453D}.qs2-p button.bad{animation:qsShake .35s}.qs2-p button.not:not(.bad) img{filter:grayscale(.6) brightness(.8)}
.qs2-p button.crowd .qs2-ck{position:absolute;right:8px;top:8px;width:30px;height:30px;border-radius:50%;background:#2F9E55;border:2px solid #fff;display:grid;place-items:center;animation:qsPlus .4s ease-out}.qs2-p button.crowd .qs2-ck::after{content:'✓';color:#fff;font-weight:900;font-style:normal}
.qs2-plus{position:absolute;left:8px;top:8px;padding:2px 10px;border-radius:999px;background:#2F9E55;color:#fff;font-size:1.1rem;animation:qsPlus .6s ease-out}
@keyframes qsIn{from{transform:scale(.9);opacity:0}to{transform:none;opacity:1}}@keyframes qsPlus{0%{transform:scale(.3);opacity:0}60%{transform:scale(1.3);opacity:1}100%{transform:none}}@keyframes qsShake{0%,100%{transform:none}25%{transform:translateX(-7px)}75%{transform:translateX(7px)}}@keyframes qsPop{0%{transform:scale(.95)}50%{transform:scale(1.04)}100%{transform:none}}
.qs2-fb{display:flex;align-items:center;gap:12px;text-align:left;border-radius:16px;padding:9px 14px;margin:12px 0 10px;min-height:60px;box-sizing:border-box}.qs2-fb b{display:block;font-size:1.15rem;line-height:1.15}.qs2-fb small{font-size:.8rem}
.qs2-fbi{flex:none;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:1.1rem}.qs2-fb.ok{animation:qsPop .35s}.qs2-fb.ok .qs2-fbi{background:#2F9E55;color:#fff}.qs2-fb.bad .qs2-fbi{background:#D6453D;color:#fff}
.qs2-dots{display:flex;justify-content:center;gap:6px}.qs2-dots i{width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:.72rem;font-weight:900;color:#fff}.qs2-dots i.ok{background:#2F9E55}.qs2-dots i.bad{background:#D6453D}.qs2-dots i.now{box-shadow:0 0 0 3px #D9A441}
.qs2-next{margin:8px 0 0;font-style:italic;font-size:.85rem;min-height:1.1em;opacity:.7}
.qs2-st{display:grid;gap:10px;margin:0 0 12px}.qs2-st button{display:grid;grid-template-columns:auto 1px 1fr auto;gap:16px;align-items:center;text-align:left;padding:12px 16px;border-radius:16px;border:2px solid;cursor:pointer;font:inherit}
.qs2-st small{display:block;font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase}.qs2-st b{display:block;font-size:2rem;line-height:1.05}.qs2-st i{align-self:stretch;opacity:.25;background:currentColor}
.qs2-st .rd{width:26px;height:26px;border-radius:50%;border:2px solid;display:grid;place-items:center;box-sizing:border-box}.qs2-st button.on .rd::after{content:'✓';font-style:normal;font-weight:900;font-size:.9rem}
.qs2-rule{font-size:.9rem;margin:0 0 12px;line-height:1.4}
.qs2-tb{width:100%;border-collapse:separate;border-spacing:0 4px;font-size:.86rem;margin:0 0 10px}.qs2-tb th{font-size:.74rem;font-weight:900;text-align:left;padding:4px 6px}.qs2-tb td{padding:10px 6px;text-align:left;font-weight:700}
.qs2-tb th:first-child,.qs2-tb td:first-child{width:14px;padding-right:0}.qs2-tb td:first-child{border-radius:10px 0 0 10px}.qs2-tb td:last-child{border-radius:0 10px 10px 0}.qs2-tb .rw{font-weight:900;white-space:nowrap}.qs2-tb .rw svg{width:1em;height:1em;vertical-align:-.15em}.qs2-tb tr.me td{font-weight:900}
.qs2-box{border-radius:16px;padding:12px 14px 14px;margin:0 0 12px}.qs2-bk{margin:0;font-size:.74rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase}.qs2-box h3{margin:4px 0 2px;font-size:1.25rem}
.qs2-big{display:block;font-size:2.6rem;line-height:1.05}.qs2-box span{display:block;font-weight:800}.qs2-box small{display:block;margin-top:4px;font-size:.82rem;opacity:.8}
html:not(.yg) .qs2-t,html:not(.yg) .qs2-q,html:not(.yg) .qs2-box h3{color:#1F2F55}html:not(.yg) .qs2-prize{background:#1F2F55;color:#fff;box-shadow:inset 0 0 0 2px #D9A441}html:not(.yg) .qs2-prize small{color:#F2D58A}
html:not(.yg) .qs2-stat{background:#F3EBDD;box-shadow:inset 0 0 0 1.5px #E2D6BF;color:#2B2320}html:not(.yg) .qs2-stat .g{color:#2F6B3F}html:not(.yg) .qs2-race{color:#5B4E45}html:not(.yg) .qs2-race .up{color:#2F6B3F}html:not(.yg) .qs2-race .dn{color:#9E2F2A}
html:not(.yg) .qs2-vs{background:#1F2F55;color:#fff;border-color:#fff}html:not(.yg) .qs2-fb{background:#F3EBDD;color:#2B2320}html:not(.yg) .qs2-fbi{background:#fff}html:not(.yg) .qs2-fb.ok{background:#DDF0E1;color:#1F4A2B}html:not(.yg) .qs2-fb.bad{background:#F8E1DF;color:#7A2420}html:not(.yg) .qs2-dots i:not(.ok):not(.bad){background:#EEE6D8;box-shadow:inset 0 0 0 1.5px #D8CCB6}html:not(.yg) .qs2-dots i.now{box-shadow:0 0 0 3px #D9A441}
html:not(.yg) .qs2-st button{background:#fff;border-color:#D8CCB6;color:#2B2320}html:not(.yg) .qs2-st b{color:#2F6B3F}html:not(.yg) .qs2-st button.on{background:#E6F3E9;border-color:#2F6B3F}html:not(.yg) .qs2-st .rd{border-color:#2B2320}html:not(.yg) .qs2-st button.on .rd{background:#2F6B3F;border-color:#2F6B3F;color:#fff}html:not(.yg) .qs2-rule{color:#2B2320}
html:not(.yg) .qs2-tb th{color:#1F2F55}html:not(.yg) .qs2-tb td{background:#fff;color:#2B2320}html:not(.yg) .qs2-tb tr.me td{background:#FFF3D1}html:not(.yg) .qs2-tb .rw{color:#2F6B3F}
html:not(.yg) .qs2-box.cash,html:not(.yg) .qs2-box.win{background:#E6F3E9}html:not(.yg) .qs2-big,html:not(.yg) .qs2-bk{color:#2F6B3F}html:not(.yg) .qs2-box span{color:#1F4A2B}html:not(.yg) .qs2-box.lose{background:#F3EBDD}html:not(.yg) .qs2-box.lose .qs2-bk{color:#9E2F2A}html:not(.yg) .qs2-sub{color:#1F2F55}
html.yg .qs2-t,html.yg .qs2-q,html.yg .qs2-box h3{color:#fff}html.yg .qs2-prize{background:linear-gradient(135deg,#FF3E9A,#8B3DFF);color:#fff;box-shadow:inset 0 0 0 2px #FFC93C}html.yg .qs2-prize small{color:#FFE9A6}
html.yg .qs2-stat{background:#241544;color:#fff}html.yg .qs2-stat .g{color:#2EE59D}html.yg .qs2-race{color:#C9B8FF}html.yg .qs2-race .up{color:#2EE59D}html.yg .qs2-race .dn{color:#FF7A9A}
html.yg .qs2-vs{background:#FFC93C;color:#1B0F33;border-color:#1B0F33}html.yg .qs2-fb{background:#241544;color:#fff}html.yg .qs2-fbi{background:#3A2766}html.yg .qs2-fb.ok{background:#0E3A2A;color:#C9FBE5}html.yg .qs2-fb.bad{background:#3A1020;color:#FFC2CC}html.yg .qs2-dots i:not(.ok):not(.bad){background:#2A1A46}
html.yg .qs2-st button{background:#1B0F33;border-color:#3A2766;color:#fff}html.yg .qs2-st b{color:#2EE59D}html.yg .qs2-st button.on{background:#0E3A2A;border-color:#2EE59D}html.yg .qs2-st .rd{border-color:#fff}html.yg .qs2-st button.on .rd{background:#2EE59D;border-color:#2EE59D;color:#06261A}html.yg .qs2-rule{color:#E9E2FF}
html.yg .qs2-tb th{color:#C9B8FF}html.yg .qs2-tb td{background:#241544;color:#fff}html.yg .qs2-tb tr.me td{background:#3A2766}html.yg .qs2-tb .rw{color:#2EE59D}
html.yg .qs2-box.cash,html.yg .qs2-box.win{background:#0E3A2A}html.yg .qs2-big,html.yg .qs2-bk{color:#2EE59D}html.yg .qs2-box span{color:#C9FBE5}html.yg .qs2-box.lose{background:#241544}html.yg .qs2-box.lose .qs2-bk{color:#FF7A9A}html.yg .qs2-sub{color:#E9E2FF}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('qs ui ok')

# ---------- One newbie progression: upload → improve → qualify → free challenge → voting; the voting loop's first challenge pop is the cash pot intro; Quick Sprint only after that ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("label: '🏆 Next: win real cash', go: () => { closeFlow(); potIntro(p); } });",
   "label: '🟡 Next: vote and earn coins', go: () => { closeFlow(); S.cpN = 0; save(); go('judge'); renderJudge(); $('#judge').scrollTop = 0; } });")
RA(" Then go for today’s <b>cash pot</b>.`, cta: 'Start now · Free'","`, cta: 'Start now · Free'")
RA("if (!comboHit && !S.geoBlock && S.votes >= 15 && (S.cpN || 0) >= (S.qsTried ? 50 : 20) && Date.now() - (S.qsPopAt || 0) > 15 * 60000) {",
   "if (!comboHit && !S.geoBlock && S.potSeen && S.votes >= 15 && (S.cpN || 0) >= (S.qsTried ? 50 : 20) && Date.now() - (S.qsPopAt || 0) > 15 * 60000) {")
# the voting loop's challenge pop: the first cash one is the full pot intro
RA("function openBattle() {\n  S.btAlt = !S.btAlt; save();",
   "function openBattle() {\n  if (!S.potSeen && !openBattle.skipCash && !S.minor && !S.geoBlock) { const pp = S.photos.filter(q => q.s && q.s.total >= CFG.QUALIFY).sort((a, b) => b.s.total - a.s.total)[0]; if (pp) { S.potSeen = 1; S.cpN = 0; save(); potIntro(pp); return; } }\n  S.btAlt = !S.btAlt; save();")
RA("const qsChipHTML = () => S.geoBlock ? '' :","const qsChipHTML = () => (S.geoBlock || !S.potSeen) ? '' :")
RA("Later · earn coins by judging","Not now · keep voting")
RA("<p class=\"pi-k\">Next step · real cash</p><h2 class=\"pi-h\">Win today’s cash pot</h2>","<p class=\"pi-k\">New · real cash challenges</p><h2 class=\"pi-h\">Win today’s cash pot</h2>")
open(d+'yofi-simple.html','w').write(s); print('flow1 ok')

# ---------- Daily cash challenge card (pot intro + voting-loop pop) and new pot challenge result, from the user's designs ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
# 1) potIntro becomes the new card
i=s.index('function potIntro(p) {'); j=s.index('\nfunction openGemBattle(', i)
s=s[:i]+r"""function potIntro(p) { potCard((p && CATS8.find(x => fitsTheme(p, x))) || CATS8[0]); }
function potCard(k) { const L = lgS(), H = lgHold(k), iHold = H.h === 'you', y = L.you[k] || 0, R = lgRank(k), K = R[0], mine = lgMine(k);
  const opp = iHold ? (R.find(r => !r.me) || {}).h : H.h; if (!mine || !opp) { lgCat(k); return; }
  const os = (R.find(r => r.h === opp) || {}).n || 0, lead = K && !K.me && K.h === opp && os > 0, rev = !iHold && (H.hist || [])[0] === 'you', cnt = y > 0 || os > 0, onVote = $('#panes').dataset.at === 'judge';
  setTimeout(() => { openSheet(`<div class="pc"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pc-k">Daily cash challenge</p><h2 class="pc-h">Your photo. Real cash.</h2>
    <p class="pc-pl">Today’s prize pool</p><b class="pc-pot">$${Math.round(L.jp[k]).toLocaleString()}</b>
    <span class="pc-time"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>Ends at midnight · <span data-wk>${dayLeft()}</span> left</span>
    <p class="pc-cat">${gi(k)}<b>${esc(crownName(k))}</b></p>
    <div class="pc-vs"><figure><img src="${mine.src}" alt=""><figcaption>You</figcaption>${cnt ? `<strong>${y}<i>⭐</i></strong>` : ''}</figure><span class="pc-x2">VS</span>
      <figure><img src="${lgPhoto(opp, k)}" alt=""><figcaption>${iHold ? '' : CRW}@${esc(opp)}</figcaption>${lead ? '<em class="pc-lead">Current leader</em>' : ''}${cnt ? `<strong>${os}<i>⭐</i></strong>` : ''}</figure></div>
    <p class="pc-wl"><span>Win <b>+1</b> ⭐</span><i></i><span>Lose <b>−1</b> ⭐</span></p>
    <div class="pc-two"><h3>Two ways to win at midnight</h3><div><span><b>⭐ 5+ stars</b><small>Share 50% of the pool</small></span><i></i><span><b>🏆 Most stars</b><small>Win 50% of the pool</small></span></div></div>
    <button class="btn block pc-go" id="pcGo">${VS_IC}${iHold ? 'Defend your blue ribbon' : rev ? 'Rematch' : 'Challenge now'} · $1</button>
    <div style="text-align:center"><button class="link pc-later" id="pcLater">${onVote ? (isYoungW() ? 'Keep judging' : 'Keep voting') : 'Not now'}</button></div></div>`);
    $('#pcGo').onclick = () => { closeSheet(); if (rev) { revengePrep(null, k, opp); return; } lgPay(() => lgFight(k, opp, !iHold)); };
    $('#pcLater').onclick = () => closeSheet();
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet()); }, 380); }"""+s[j:]
# 2) the voting loop's cash pop uses the same card
a=s.index("celebrate({ src: mine ? lgMine(k).src : lgPhoto(H.h, k), score: '🏅'"); b=s.index("later: 'Not now' });", a)+len("later: 'Not now' });")
s=s[:a]+"potCard(k);"+s[b:]
# 3) new result screen
a=s.index("$('#lb').innerHTML = `<div class=\"wr ${won ? 'w' : 'l'}\">"); b=s.index("paintWallet(); if ($('#panes').dataset.at === 'gallery' && GV.tab === 'battle') renderGallery();", a)
s=s[:a]+r"""const onVote = $('#panes').dataset.at === 'judge', rib = `<span class="pz-rib">${CRW}</span>`;
      $('#lb').innerHTML = `<div class="pz ${won ? 'w' : 'l'}"><button class="pz-xx" data-shclose aria-label="Close">${QS_X}</button>${won ? '<div class="wr-cf" aria-hidden="true">' + [...Array(10)].map((_, i) => `<i style="left:${(i * 37) % 95}%;animation-delay:${(i * .13).toFixed(2)}s"></i>`).join('') + '</div>' : ''}
        <p class="pz-k"><i></i>${esc(crownName(k).toUpperCase())}<i></i></p>
        <h1 class="pz-h">This round goes to…</h1><p class="pz-w">${won ? 'You!' : '@' + esc(h)}${CRW}</p>
        <div class="pz-vs"><figure class="${won ? 'win' : ''}"><div class="pz-im"><img src="${me.src}" alt="">${won ? rib : ''}</div><figcaption>You</figcaption>${won ? '<em class="pz-wb">Winner</em>' : '<em class="pz-wb no"></em>'}<strong>${mv}<small>votes</small></strong></figure>
          <span class="pz-x"><i></i>VS<i></i></span>
          <figure class="${won ? '' : 'win'}"><div class="pz-im"><img src="${src}" alt="">${won ? '' : rib}</div><figcaption>@${esc(h)}</figcaption>${won ? '<em class="pz-wb no"></em>' : '<em class="pz-wb">Winner</em>'}<strong>${tv}<small>votes</small></strong></figure></div>
        <p class="pz-sub">${sub}</p>
        <div class="pz-pool"><small>Today’s prize pool</small><b>$${L.jp[k].toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b><hr>
          <div class="pz-ys"><span>Your stars</span><b>${Math.min(y, LG_SHARE)} / ${LG_SHARE}</b></div>
          <div class="pz-stars">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= y ? 'on' : ''}">⭐</i>`).join('')}</div>
          <p>${y >= LG_SHARE ? `You’re in · <b>${money(lgShare(k))}</b> so far. Keep winning to grow it.` : `Finish with ${LG_SHARE}+ stars to share half the pool.`}${!won && lost ? ' <span class="pz-lost">−1 star for this loss</span>' : ''}</p><em>Pays at midnight</em></div>
        ${won ? `<button class="btn block pz-go" id="lbMore">${VS_IC}Challenge again · $1</button>` : `<button class="btn block pz-go" id="lbRev">${VS_IC}Rematch · $1</button>`}
        <div style="text-align:center"><button class="link pz-back" data-shclose>${onVote ? (isYoungW() ? 'Keep judging' : 'Keep voting') : 'Back to challenges'}</button></div></div>`;
      """+s[b:]
RA("if ($('#lbMore')) $('#lbMore').onclick = () => lgCat(k);","if ($('#lbMore')) $('#lbMore').onclick = () => { closeSheet(); potCard(k); };")
s=s.replace('</style>',""".pc{position:relative;text-align:center;padding:4px 2px 2px}.pc-x,.pz-xx{position:absolute;right:0;top:0;border:0;background:none;color:inherit;padding:4px;cursor:pointer;z-index:3}
.pc-k{margin:6px 0 2px;font-size:.78rem;font-weight:900;letter-spacing:.14em;text-transform:uppercase}.pc-h{margin:0 0 8px;padding-bottom:8px;font-size:1.75rem;line-height:1.1;border-bottom:2px solid #D9A441}
.pc-pl{margin:4px 0 0;font-weight:800;font-size:1rem}.pc-pot{display:block;font-size:3.2rem;line-height:1.05;margin:0 0 6px}
.pc-time{display:inline-flex;align-items:center;gap:8px;padding:5px 16px;border-radius:999px;font-size:.88rem;font-weight:700;font-variant-numeric:tabular-nums}
.pc-cat{display:flex;align-items:center;justify-content:center;gap:8px;margin:10px 0 8px;font-size:1.05rem}.pc-cat svg{width:22px;height:22px}
.pc-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:6px}.pc-vs figure{margin:0}.pc-vs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:16px;display:block}
.pc-vs figcaption{margin-top:6px;font-weight:800;font-size:.95rem}.pc-vs figcaption .crw-ic{width:14px;height:17px;vertical-align:-3px;margin-right:3px}
.pc-x2{align-self:center;margin-top:-30px;width:42px;height:42px;border-radius:50%;display:grid;place-items:center;font-weight:900}
.pc-lead{display:inline-block;margin-top:3px;padding:2px 10px;border-radius:999px;font-style:normal;font-size:.78rem;font-weight:800}
.pc-vs strong{display:block;font-size:2.3rem;line-height:1.1;margin-top:2px}.pc-vs strong i{font-style:normal;font-size:.8em;margin-left:2px}
.pc-wl{display:flex;justify-content:center;align-items:center;gap:16px;margin:10px 0;font-size:1rem}.pc-wl i{width:1px;height:24px;opacity:.35;background:currentColor}
.pc-two{border-radius:16px;padding:10px 12px;margin:0 0 12px}.pc-two h3{margin:0 0 6px;font-size:1.1rem}.pc-two div{display:grid;grid-template-columns:1fr 1px 1fr;gap:10px;align-items:center}.pc-two div i{align-self:stretch;opacity:.3;background:currentColor}
.pc-two b{display:block;font-size:1.05rem}.pc-two small{font-size:.8rem}.pc-later{margin-top:8px}
.pz{position:relative;text-align:center;padding:6px 4px 4px}.pz-k{display:flex;align-items:center;justify-content:center;gap:12px;margin:4px 0;font-size:.82rem;font-weight:900;letter-spacing:.2em}.pz-k i{width:32px;height:2px;background:#D9A441}
.pz-h{margin:2px 0 0;font-size:1.9rem;line-height:1.1}.pz-w{display:flex;align-items:center;justify-content:center;gap:6px;margin:2px 0 10px;font-size:1.6rem;font-weight:800}.pz-w .crw-ic{width:26px;height:32px}
.pz-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:6px}.pz-vs figure{margin:0}.pz-im{position:relative}.pz-im img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:16px;display:block}
.pz-rib{position:absolute;right:-8px;top:-12px;z-index:2}.pz-rib .crw-ic,.pz-rib svg{width:38px!important;height:46px!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))}.pz-vs figcaption{margin-top:6px;font-weight:800;font-size:1rem}
.pz-wb{display:inline-block;min-height:18px;margin-top:2px;padding:1px 12px;border-radius:999px;font-style:normal;font-size:.72rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.pz-wb.no{background:none!important}
.pz-vs strong{display:block;font-size:2.6rem;line-height:1.05}.pz-vs strong small{font-size:.9rem;font-weight:700;margin-left:6px}
.pz-x{display:flex;flex-direction:column;align-items:center;gap:6px;align-self:center;margin-top:-40px;font-weight:900;font-size:1.3rem}.pz-x i{width:22px;height:2px;background:#D9A441}
.pz-sub{margin:6px 0 10px;font-size:.88rem;font-weight:700}
.pz-pool{border-radius:18px;padding:12px 14px;margin:0 0 12px}.pz-pool>small{display:block;font-size:.78rem;font-weight:900;letter-spacing:.16em;text-transform:uppercase}.pz-pool>b{display:block;font-size:2.4rem;line-height:1.1}
.pz-pool hr{border:0;height:1px;margin:8px 0;opacity:.3;background:currentColor}.pz-ys{display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:1.05rem}.pz-ys b{font-size:1.4rem}
.pz-stars{display:flex;justify-content:center;gap:10px;margin:4px 0 6px;font-size:1.9rem}.pz-stars i{font-style:normal;filter:grayscale(1);opacity:.3}.pz-stars i.on{filter:none;opacity:1;animation:qsPlus .5s ease-out}
.pz-pool p{margin:0;font-size:.9rem}.pz-pool em{display:block;margin-top:2px;font-size:.8rem;font-style:normal;opacity:.7}.pz-lost{display:block;font-weight:800;margin-top:2px}.pz-back{margin-top:8px}
html:not(.yg) .pc-k{color:#2F6B3F}html:not(.yg) .pc-h,html:not(.yg) .pz-h,html:not(.yg) .pz-w,html:not(.yg) .pc-two h3,html:not(.yg) .pz-k{color:#2B1D14}html:not(.yg) .pc-pot,html:not(.yg) .pz-pool>b,html:not(.yg) .pc-two b{color:#2F6B3F}
html:not(.yg) .pc-time{background:#FFF8E7;box-shadow:inset 0 0 0 1.5px #E5C77A;color:#2B2320}html:not(.yg) .pc-time svg{color:#C98A12}html:not(.yg) .pc-cat{color:#2B2320}
html:not(.yg) .pc-vs img,html:not(.yg) .pz-im img{box-shadow:0 0 0 3px #2D4E86}html:not(.yg) .pz-vs figure.win .pz-im img{box-shadow:0 0 0 3px #D9A441}html:not(.yg) .pc-x2{background:#2D4E86;color:#fff}
html:not(.yg) .pc-lead{background:#DCE6F7;color:#2D4E86}html:not(.yg) .pc-vs strong,html:not(.yg) .pz-vs strong{color:#1F3F8F}html:not(.yg) .pz-vs strong small{color:#2B2320}html:not(.yg) .pc-wl{color:#2B2320}
html:not(.yg) .pc-two{background:#FFF8E7;box-shadow:inset 0 0 0 1.5px #E5C77A;color:#2B2320}html:not(.yg) .pz-wb{background:#2D4E86;color:#fff}html:not(.yg) .pz-x{color:#2B1D14}
html:not(.yg) .pz-pool{background:#fff;box-shadow:inset 0 0 0 1.5px #E6D9C4;color:#2B2320}html:not(.yg) .pz-sub{color:#5B4E45}html:not(.yg) .pz-lost{color:#9E2F2A}
html.yg .pc-k{color:#2EE59D}html.yg .pc-h,html.yg .pz-h,html.yg .pz-w,html.yg .pc-two h3,html.yg .pz-k{color:#fff}html.yg .pc-pot,html.yg .pz-pool>b,html.yg .pc-two b{color:#2EE59D}
html.yg .pc-time{background:#241544;box-shadow:inset 0 0 0 1.5px #FFC93C;color:#fff}html.yg .pc-time svg{color:#FFC93C}html.yg .pc-cat{color:#fff}
html.yg .pc-vs img,html.yg .pz-im img{box-shadow:0 0 0 3px #C13CFF}html.yg .pz-vs figure.win .pz-im img{box-shadow:0 0 0 3px #FFC93C}html.yg .pc-x2{background:#FFC93C;color:#1B0F33}
html.yg .pc-lead{background:#3A2766;color:#E9E2FF}html.yg .pc-vs strong,html.yg .pz-vs strong{color:#FFC93C}html.yg .pz-vs strong small{color:#E9E2FF}html.yg .pc-wl{color:#E9E2FF}
html.yg .pc-two{background:#241544;box-shadow:inset 0 0 0 1.5px #FFC93C;color:#E9E2FF}html.yg .pz-wb{background:#FFC93C;color:#1B0F33}html.yg .pz-x{color:#fff}
html.yg .pz-pool{background:#1B0F33;box-shadow:inset 0 0 0 1.5px #3A2766;color:#E9E2FF}html.yg .pz-sub{color:#C9B8FF}html.yg .pz-lost{color:#FF7A9A}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('pot card ok')

# ---------- Progress bars: one solid gold everywhere; coin icons next to amounts smaller ----------
s=open(d+'yofi-simple.html').read()
s=s.replace('</style>',""".en-bar i,.aset-bar i,.pbar i,.rv-bar>i>i,.stk-fill,.ut0-bar i{background:#FBC20A!important;box-shadow:inset 0 -2px 0 rgba(160,110,0,.25)}
.qs2-prize svg{width:.55em!important;height:.55em!important;vertical-align:.1em!important;margin-left:4px}
.qs-chip em svg,.qs2-tb .rw svg,.qs2-sub svg,.qs-res h2 svg,#crGo svg,svg[class=""]{width:.8em!important;height:.8em!important;vertical-align:-.05em!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('gold ok')

# ---------- Category cards: the leader number is stars, not ribbons ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("<span class=\"t\">${CRW}<b>${me ? 'You' : K.n}</b></span>","<span class=\"t\" aria-label=\"Top player has ${K.n} stars\"><span class=\"st-ic\">⭐</span><b>${K.n}</b></span>")
RA("<em>${r.n} 🏅</em>","<em>${r.n} ⭐</em>")
s=s.replace('</style>',""".bcc-pl .t .st-ic{font-style:normal;font-size:.9em;margin-right:3px}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('stars ok')

# ---------- No +100 coins for uploading to a new category ----------
s=open(d+'yofi-simple.html').read()
n1=s.count(' <i class="nc-b">+100</i>'); s=s.replace(' <i class="nc-b">+100</i>','')
n2=s.count(' · <i class="nc-b">+100 🟡</i>'); s=s.replace(' · <i class="nc-b">+100 🟡</i>','')
a="if (o.fresh && !o.first && p && p.cat && p.cat !== 'any' && !(S.catBonus"
assert s.count(a)==1; s=s.replace(a,"if (false && o.fresh && !o.first && p && p.cat && p.cat !== 'any' && !(S.catBonus")
open(d+'yofi-simple.html','w').write(s); print('no +100 ok', n1, n2)

# ---------- Tournaments: "How tournaments work" link explaining each type ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA('<div class="tsh"><h1>Tournaments</h1><p>Guaranteed prizes</p>','<div class="tsh"><h1>Tournaments</h1><p>Guaranteed prizes</p><button class="link tsh-how" id="tshHow">ⓘ How tournaments work</button>')
s=s.replace("function fcNotify() {",r"""function tHowOpen() { const c = $('#coach'), coin = gemIcon('');
  const T = (cls, ic, name, when, entry, lines) => `<div class="th-t ${cls}"><div class="th-hd"><span class="th-ic">${ic}</span><b>${name}</b><em>${entry}</em></div><p class="th-when">${when}</p><ul>${lines.map(l => `<li>${l}</li>`).join('')}</ul></div>`;
  c.innerHTML = `<div class="cpr th" role="dialog" aria-modal="true" aria-labelledby="thH"><button class="qs2-x" id="thX" aria-label="Close">${QS_X}</button>
    <h2 class="th-h" id="thH">How tournaments work</h2><p class="th-sub">Four kinds of tournament. Each row on the schedule is colour coded.</p>
    ${T('t-ch', '🏆', 'Crowd Championship', 'Every hour · top of the schedule', `$${CH_ENTRY}`, [`<b>${CH_N} photo pairs.</b> Pick the photo the crowd chose.`, 'Book ahead, then play any time during the hour. We remind you when it’s live.', '<b>85%</b> of entries go into the prize pool, so it grows as people join.', 'Most right wins, ties go to the fastest. Results at the end of the hour.'])}
    ${T('t-fr', '🎟️', 'Freeroll', 'Every hour · gold rows', '🎟️ Free', ['Enter with a <b>Freeroll ticket</b>. Swap <b>1,000 coins</b> for one, once an hour.', 'Your best photo is ranked by its score.', `The <b>top ${FR_FINAL}</b> go through to a live final.`, `Final prizes: <b>$${FR_PRIZE[0]}</b> · <b>$${FR_PRIZE[1]}</b> · <b>$${FR_PRIZE[2]}</b> in real cash.`])}
    ${T('t-ko', '⚔️', 'Knockout tournament', `Every 30 minutes · ${isYoungW() ? 'pink' : 'blue'} rows`, '$1', [`<b>${T_N} players</b>, your best photo against theirs.`, '<b>4 head-to-head rounds</b>, each decided live by member votes.', 'Win every round to take the <b>guaranteed prize</b>.', '<b>$25</b> every half hour, <b>$100</b> on the hour.'])}
    ${T('t-gm', coin, 'Coin tournament', 'Every hour · purple rows', `${coin} 100`, ['Same knockout format, played for coins.', `Win the <b>${coin} 5,000</b> prize.`, 'Good practice before cash tournaments.'])}
    <p class="th-ft">Cash prizes go straight to your cash balance. 18+ only, and cash tournaments aren’t available in every state.</p>
    <button class="bt-cta" id="thOk">Got it</button></div>`;
  c.classList.add('on', 'cr'); c.onclick = e => { if (e.target === c) c.classList.remove('on', 'cr'); };
  $('#thX').onclick = $('#thOk').onclick = () => c.classList.remove('on', 'cr'); }
document.addEventListener('click', e => { if (e.target.closest('#tshHow')) { e.preventDefault(); e.stopPropagation(); tHowOpen(); } }, true);
function fcNotify() {""",1)
s=s.replace('</style>',""".tsh-how{display:block;margin:6px auto 0;font-size:.9rem;font-weight:700}
.th{position:relative;text-align:left;max-height:84vh;overflow:auto}.th-h{margin:4px 30px 2px 0;font-size:1.45rem}.th-sub{margin:0 0 12px;font-size:.88rem}
.th-t{border-radius:16px;padding:10px 12px;margin:0 0 10px}.th-hd{display:flex;align-items:center;gap:8px}.th-ic{font-size:1.2rem;line-height:1}.th-ic svg{width:1.1em;height:1.1em}
.th-hd b{font-size:1.05rem}.th-hd em{margin-left:auto;font-style:normal;font-weight:900;padding:3px 10px;border-radius:999px;white-space:nowrap;font-size:.85rem}.th-hd em svg{width:.85em!important;height:.85em!important;vertical-align:-.05em}
.th-when{margin:2px 0 6px;font-size:.78rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;opacity:.8}.th-t ul{margin:0;padding-left:18px;display:grid;gap:4px}.th-t li{font-size:.88rem;line-height:1.35}.th-t li svg{width:.85em!important;height:.85em!important;vertical-align:-.05em}
.th-ft{font-size:.78rem;margin:4px 0 12px;opacity:.8}
html:not(.yg) .th-h{color:#1F2F55}html:not(.yg) .th-sub,html:not(.yg) .th-ft{color:#5B4E45}html:not(.yg) .th-t{color:#2B2320}
html:not(.yg) .th-t.t-ch{background:#E6F3E9;box-shadow:inset 0 0 0 1.5px #2F6B3F}html:not(.yg) .th-t.t-ch em{background:#2F6B3F;color:#fff}
html:not(.yg) .th-t.t-fr{background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #D9A441}html:not(.yg) .th-t.t-fr em{background:#FBC20A;color:#2B1D14}
html:not(.yg) .th-t.t-ko{background:#E8EEF8;box-shadow:inset 0 0 0 1.5px #2D4E86}html:not(.yg) .th-t.t-ko em{background:#2D4E86;color:#fff}
html:not(.yg) .th-t.t-gm{background:#EFEAF8;box-shadow:inset 0 0 0 1.5px #6B5BB5}html:not(.yg) .th-t.t-gm em{background:#6B5BB5;color:#fff}
html.yg .th-h{color:#fff}html.yg .th-sub,html.yg .th-ft{color:#C9B8FF}html.yg .th-t{color:#E9E2FF}
html.yg .th-t.t-ch{background:#0E3A2A;box-shadow:inset 0 0 0 1.5px #2EE59D}html.yg .th-t.t-ch em{background:#2EE59D;color:#06261A}
html.yg .th-t.t-fr{background:#3A2A0A;box-shadow:inset 0 0 0 1.5px #FFC93C}html.yg .th-t.t-fr em{background:#FFC93C;color:#1B0F33}
html.yg .th-t.t-ko{background:#1E1236;box-shadow:inset 0 0 0 1.5px #FF3FA4}html.yg .th-t.t-ko em{background:linear-gradient(95deg,#FF3FA4,#8B3CFF);color:#fff}
html.yg .th-t.t-gm{background:#1C1840;box-shadow:inset 0 0 0 1.5px #4A4AB0}html.yg .th-t.t-gm em{background:linear-gradient(95deg,#7A5CFF,#3B6CF5);color:#fff}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('t how ok')

# ---------- More winners: 3+ stars (was 5) share the 50%, split by stars ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA('LG_SHARE = 5','LG_SHARE = 3')
RA('Collect 5 stars in a category by midnight to share the pot','Collect 3 stars in a category by midnight to share the pot')
RA("'Earn 5 stars to share the pot'","'Earn 3 stars to share the pot'")
RA('<p>Everyone with <b>5+ stars</b> shares the other <b>50%</b>, by stars.</p>','<p>Everyone with <b>3+ stars</b> shares the other <b>50%</b>. More stars, bigger share.</p>')
RA('🏆 Most stars wins 50% · 5+ stars share 50%','🏆 Most stars wins 50% · 3+ stars share 50%')
RA('Everyone with 5+ stars shares the other 50%, by stars.','Everyone with 3+ stars shares the other 50%, by stars.')
RA('<b>⭐ 5+ stars</b><small>Share 50% of the pool</small>','<b>⭐ 3+ stars</b><small>Share 50% of the pool</small>')
RA('${[1, 2, 3, 4, 5].map(i => `<i class="${i <= y ? \'on\' : \'\'}">⭐</i>`).join(\'\')}','${[...Array(LG_SHARE)].map((_, j) => `<i class="${j < y ? \'on\' : \'\'}">⭐</i>`).join(\'\')}')
open(d+'yofi-simple.html','w').write(s); print('share3 ok')

# ---------- Improved: Quick Sprint result, pot challenge card, pot challenge result ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("else { clearInterval(clk); sprDone(id, right, Date.now() - t0); }","else { clearInterval(clk); window.__qsRes = res.slice(); sprDone(id, right, Date.now() - t0); }")
# 1) Quick Sprint result
i=s.index('function sprDone(id, right, ms) { const O = qsOpp(id)'); j=s.index('\nfunction ', i+10)
s=s[:i]+r"""function sprDone(id, right, ms) { const O = qsOpp(id), pr = window.__qsPractice, st = window.__qsStake || 2, mine = window.__qsRes || [];
  const won = right > O.sc || (right === O.sc && ms <= O.ms), pay = pr ? QS_COIN_PAY[0] : qsPay(st)[0], diff = Math.abs(O.sc - right), oh = '@' + esc(O.h);
  if (pr) { S.qsTried = 1; if (won) { S.gems = (S.gems || 0) + pay; setTimeout(paintGems, 200); } save(); }
  else if (won) { S.cash = +((S.cash || 0) + pay).toFixed(2); save(); setTimeout(paintWallet, 200); }
  const c = $('#coach'), amt = pr ? `${pay} ${gemIcon('')}` : qsM(pay), pk = n => `${n} pick${n === 1 ? '' : 's'}`;
  const head = won ? `You won ${amt}!` : diff === 0 ? 'Lost on time!' : diff === 1 ? 'So close!' : 'Not this time';
  const sub = won ? (diff ? `You beat ${oh} by ${pk(diff)}` : `Same score, you were ${((O.ms - ms) / 1000).toFixed(1)}s faster`) : (diff ? `${oh} won by ${pk(diff)}` : `Same score, ${oh} was ${((ms - O.ms) / 1000).toFixed(1)}s faster`);
  const side = (nm, sc, t, w) => `<div class="${w ? 'w' : ''}"><small>${nm}</small><b>${sc}<em>/${SPR_N}</em></b><span>⏱ ${(t / 1000).toFixed(1)}s</span>${w ? '<i class="qs3-badge">Winner</i>' : ''}</div>`;
  const split = mine.map((v, j) => v !== O.seq[j]), row = (nm, arr) => `<div><b>${nm}</b><span>${arr.map((v, j) => `<i class="${v ? 'ok' : 'bad'} ${split[j] ? 'df' : ''}">${v ? '✓' : '✕'}</i>`).join('')}</span></div>`;
  const up = pr ? `<div class="qs3-up"><span class="qs3-upi">🎯</span><div><b>Ready for real cash?</b><small>$2 entry · 1 vs 1 · winner gets <b>${qsM(qsPay(2)[0])}</b></small></div></div>`
    : won ? `<div class="qs3-up win"><span class="qs3-upi">💵</span><div><b>${qsM(pay)} added to your cash</b><small>Play again or keep voting</small></div></div>` : '';
  c.innerHTML = `<div class="cpr qs2 qs3 ${won ? 'won' : 'lost'}" role="dialog" aria-modal="true"><button class="qs2-x" id="qsX" aria-label="Close">${QS_X}</button>
    ${won ? '<div class="wr-cf" aria-hidden="true">' + [...Array(10)].map((_, i) => `<i style="left:${(i * 37) % 95}%;animation-delay:${(i * .13).toFixed(2)}s"></i>`).join('') + '</div>' : ''}
    <p class="qs3-k">🎯 Quick Sprint${pr ? ' · coins' : ''}</p><h2 class="qs3-h" id="qsHead">${head}</h2><p class="qs3-sub">${sub}</p>
    <div class="qs3-sb">${side('You', right, ms, won)}<span class="qs3-vs">VS</span>${side(oh, O.sc, O.ms, !won)}</div>
    ${mine.length ? `<div class="qs3-cmp">${row('You', mine)}${row(oh, O.seq)}<p>Highlighted: the ${pk(split.filter(Boolean).length).replace('pick', 'pair')} where you split</p></div>` : ''}
    ${up}<button class="bt-cta qs2-go" id="qsAgain">${pr ? `Play for ${qsM(qsPay(2)[0])}` : `Play again · ${qsM(st)} entry`}</button><button class="bt-no" id="cpBack">${isYoungW() ? 'Keep judging' : 'Keep voting'}</button></div>`;
  if (won && !pr) setTimeout(() => cashExplosion && cashExplosion(pay, { label: 'Quick Sprint' }), 400);
  const shut = () => c.classList.remove('on', 'cr');
  $('#qsAgain').onclick = () => { shut(); pr ? sprEnter() : sprEnter(st); }; $('#cpBack').onclick = shut; $('#qsX').onclick = shut; }"""+s[j:]
# 2) Pot challenge card
i=s.index('function potCard(k) {'); j=s.index('\nfunction openGemBattle(', i)
s=s[:i]+r"""function potCard(k) { const L = lgS(), H = lgHold(k), iHold = H.h === 'you', y = L.you[k] || 0, R = lgRank(k), K = R[0], mine = lgMine(k);
  const opp = iHold ? (R.find(r => !r.me) || {}).h : H.h; if (!mine || !opp) { lgCat(k); return; }
  const os = (R.find(r => r.h === opp) || {}).n || 0, lead = K && !K.me && K.h === opp && os > 0, rev = !iHold && (H.hist || [])[0] === 'you', onVote = $('#panes').dataset.at === 'judge', need = Math.max(0, LG_SHARE - y);
  const stars = n => [...Array(LG_SHARE)].map((_, j) => `<i class="${j < n ? 'on' : ''}">⭐</i>`).join('');
  setTimeout(() => { openSheet(`<div class="pc pc2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pc-k">${gi(k)}<span>Daily cash challenge · ${esc(crownName(k))}</span></p><h2 class="pc-h">Your photo. Real cash.</h2>
    <div class="pc2-pool"><b>$${Math.round(L.jp[k]).toLocaleString()}</b><span>today’s prize pool<em>⏱ Pays at midnight · <span data-wk>${dayLeft()}</span> left</em></span></div>
    <div class="pc-vs pc2-vs"><figure><img src="${mine.src}" alt=""><figcaption>You</figcaption><small>${y} ⭐ today</small></figure><span class="pc-x2">VS</span>
      <figure><img src="${lgPhoto(opp, k)}" alt=""><figcaption>@${esc(opp)}</figcaption><small>${iHold ? `${os} ⭐ today` : `${CRW}Blue ribbon · held ${heldFor(H.since)} · ${H.def} defence${H.def === 1 ? '' : 's'}`}</small>${lead ? '<em class="pc-lead">Stars leader</em>' : ''}</figure></div>
    <div class="pc2-stake"><div class="w"><b>Win</b><span>+1 ⭐${iHold ? ' · keep your blue ribbon' : ' · your photo takes the blue ribbon'}</span></div><div class="l"><b>Lose</b><span>${y ? '−1 ⭐' : 'nothing to lose yet'}</span></div></div>
    <div class="pc2-me"><span class="pc2-st">${stars(y)}</span><p><b>${Math.min(y, LG_SHARE)}/${LG_SHARE} stars</b> · ${need ? `${need} more win${need === 1 ? '' : 's'} to share the pool` : 'you’re sharing the pool · more stars, bigger share'}</p></div>
    <p class="pc2-how">🏆 Most stars wins <b>50%</b> · ⭐ ${LG_SHARE}+ stars share <b>50%</b></p>
    <button class="btn block pc-go" id="pcGo">${VS_IC}${iHold ? 'Defend your blue ribbon' : rev ? 'Rematch' : 'Challenge now'} · $1</button>
    <div style="text-align:center"><button class="link pc-later" id="pcLater">${onVote ? (isYoungW() ? 'Keep judging' : 'Keep voting') : 'Not now'}</button></div></div>`);
    $('#pcGo').onclick = () => { closeSheet(); if (rev) { revengePrep(null, k, opp); return; } lgPay(() => lgFight(k, opp, !iHold)); };
    $('#pcLater').onclick = () => closeSheet();
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet()); }, 380); }"""+s[j:]
# 3) Pot challenge result
a=s.index("const onVote = $('#panes').dataset.at === 'judge', rib = "); b=s.index("paintWallet(); if ($('#panes').dataset.at === 'gallery' && GV.tab === 'battle') renderGallery();", a)
s=s[:a]+r"""const onVote = $('#panes').dataset.at === 'judge', rib = `<span class="pz-rib">${CRW}</span>`, pm = Math.round(mv / N * 100), need = Math.max(0, LG_SHARE - y);
      const SC = me.s || {}, SN = { light: 'lighting', comp: 'composition', colour: 'colour', subject: 'subject', tech: 'sharpness' }, wk = !won ? Object.keys(SN).filter(x => SC[x] != null).sort((p, q) => SC[p] - SC[q])[0] : null;
      const ph = (img, nm, w) => `<figure class="${w ? 'win' : ''}"><div class="pz-im"><img src="${img}" alt="">${w ? rib : ''}</div><figcaption>${nm}</figcaption>${w ? '<em class="pz-wb">Winner</em>' : ''}</figure>`;
      $('#lb').innerHTML = `<div class="pz pz2 ${won ? 'w' : 'l'}"><button class="pz-xx" data-shclose aria-label="Close">${QS_X}</button>${won ? '<div class="wr-cf" aria-hidden="true">' + [...Array(10)].map((_, i) => `<i style="left:${(i * 37) % 95}%;animation-delay:${(i * .13).toFixed(2)}s"></i>`).join('') + '</div>' : ''}
        <p class="pz-k"><i></i>${esc(crownName(k).toUpperCase())}<i></i></p>
        <h1 class="pz-h">${won ? 'You won!' : tv - mv <= 4 ? 'So close!' : `@${esc(h)} takes it`}</h1><p class="pz2-s">${sub}</p>
        <div class="pz2-vs">${ph(me.src, 'You', won)}<span class="pz2-x">VS</span>${ph(src, '@' + esc(h), !won)}</div>
        <div class="pz2-bar"><i style="width:${pm}%"><b>${mv}</b></i><i style="width:${100 - pm}%"><b>${tv}</b></i></div><p class="pz2-bl"><span>You · ${pm}%</span><span>${30} votes</span><span>@${esc(h)} · ${100 - pm}%</span></p>
        ${won ? `<p class="pz2-gain">+${g} ⭐${took ? ' · 🎗 your photo is on the card' : ''}</p>` : lost ? '<p class="pz2-gain l">−1 ⭐</p>' : '<p class="pz2-gain z">No stars lost: you had none yet</p>'}
        <div class="pc2-me pz2-me"><span class="pc2-st">${[...Array(LG_SHARE)].map((_, j) => `<i class="${j < y ? 'on' : ''}">⭐</i>`).join('')}</span><p><b>${Math.min(y, LG_SHARE)}/${LG_SHARE} stars</b> · ${need ? `${need} more win${need === 1 ? '' : 's'} to share the pool` : `you’re in · <b>${money(lgShare(k))}</b> so far`}</p><small>Prize pool <b>$${Math.round(L.jp[k]).toLocaleString()}</b> · pays at midnight</small></div>
        ${wk ? `<button class="pz2-tip" id="lbTip"><span class="pz2-ti">💡</span><span><b>Your ${SN[wk]} scored ${SC[wk]}</b><small>That’s your photo’s weakest area. Touch it up to win more votes.</small></span><em>Touch up ›</em></button>` : ''}
        ${won ? `<button class="btn block pz-go" id="lbMore">${VS_IC}Challenge again · $1</button>` : `<button class="btn block pz-go" id="lbRev">${VS_IC}Rematch · $1</button>`}
        <div style="text-align:center"><button class="link pz-back" data-shclose>${onVote ? (isYoungW() ? 'Keep judging' : 'Keep voting') : 'Back to challenges'}</button></div></div>`;
      """+s[b:]
RA("if ($('#lbMore')) $('#lbMore').onclick = () => { closeSheet(); potCard(k); };","if ($('#lbMore')) $('#lbMore').onclick = () => { closeSheet(); potCard(k); };\n      if ($('#lbTip')) $('#lbTip').onclick = () => { closeSheet(); S.cur = me.id; save(); WALL = false; go('studio'); renderStudio(); };")
s=s.replace('</style>',""".qs3{text-align:center}.qs3-k{margin:2px 30px 2px;font-size:.74rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase}.qs3-h{margin:0;font-size:1.9rem;line-height:1.1}.qs3-h svg{width:.7em!important;height:.7em!important}.qs3-sub{margin:4px 0 12px;font-size:.92rem;font-weight:700}
.qs3-sb{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;margin:0 0 10px}.qs3-sb>div{position:relative;border-radius:16px;padding:10px 6px 8px}.qs3-sb small{display:block;font-weight:800;font-size:.85rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qs3-sb b{display:block;font-size:2.4rem;line-height:1.05}.qs3-sb b em{font-style:normal;font-size:.45em;opacity:.6}.qs3-sb span{font-size:.8rem;font-weight:700}
.qs3-badge{position:absolute;top:-9px;left:50%;transform:translateX(-50%);padding:1px 10px;border-radius:999px;font-style:normal;font-size:.66rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap}.qs3-vs{font-weight:900;font-size:.9rem;opacity:.7}
.qs3-cmp{border-radius:14px;padding:8px 10px;margin:0 0 10px;text-align:left}.qs3-cmp>div{display:grid;grid-template-columns:78px 1fr;align-items:center;gap:6px;margin:3px 0}.qs3-cmp>div b{font-size:.78rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qs3-cmp>div span{display:flex;gap:3px}
.qs3-cmp i{flex:1;max-width:22px;aspect-ratio:1;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:.62rem;font-weight:900;color:#fff;opacity:.45}.qs3-cmp i.ok{background:#2F9E55}.qs3-cmp i.bad{background:#D6453D}.qs3-cmp i.df{opacity:1;box-shadow:0 0 0 2px #FBC20A}.qs3-cmp p{margin:4px 0 0;font-size:.74rem;text-align:center;opacity:.8}
.qs3-up{display:flex;align-items:center;gap:10px;text-align:left;border-radius:14px;padding:10px 12px;margin:0 0 12px}.qs3-upi{font-size:1.4rem}.qs3-up b{display:block;font-size:1rem}.qs3-up small{font-size:.82rem}
.qs2 .bt-cta,.pz-go,.pc-go{text-transform:none!important;letter-spacing:0!important}
.pc2 .pc-k{display:flex;align-items:center;justify-content:center;gap:6px;margin-right:24px;margin-left:24px}.pc2 .pc-k svg{width:16px;height:16px;flex:none}.pc2 .pc-h{font-size:1.6rem;margin-bottom:10px}
.pc2-pool{display:flex;align-items:center;justify-content:center;gap:12px;margin:0 0 12px}.pc2-pool>b{font-size:2.5rem;line-height:1}.pc2-pool>span{text-align:left;font-weight:800;font-size:.9rem;line-height:1.3}.pc2-pool em{display:block;font-style:normal;font-weight:700;font-size:.78rem;white-space:nowrap}
.pc2-vs small{display:block;font-size:.74rem;font-weight:700;line-height:1.3;margin-top:2px}.pc2-vs small .crw-ic{width:11px;height:14px;vertical-align:-2px;margin-right:2px}
.pc2-stake{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 8px}.pc2-stake>div{border-radius:12px;padding:7px 8px}.pc2-stake b{display:block;font-size:.72rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase}.pc2-stake span{font-size:.84rem;font-weight:700;line-height:1.25}
.pc2-me{display:flex;flex-direction:column;align-items:center;gap:2px;margin:0 0 6px}.pc2-st{display:flex;gap:8px;font-size:1.5rem}.pc2-st i{font-style:normal;filter:grayscale(1);opacity:.3}.pc2-st i.on{filter:none;opacity:1}.pc2-me p{margin:0;font-size:.88rem}.pc2-me small{font-size:.78rem;opacity:.8}
.pc2-how{margin:4px 0 12px;font-size:.82rem}
.pz2-s{margin:2px 0 10px;font-size:.88rem;font-weight:700}.pz2-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:8px}.pz2-vs figure{margin:0}.pz2-vs figcaption{margin-top:5px;font-weight:800;font-size:.92rem}.pz2-x{align-self:center;margin-top:-26px;font-weight:900}
.pz2-bar{display:flex;height:30px;border-radius:999px;overflow:hidden;margin:12px 0 4px}.pz2-bar i{display:flex;align-items:center;padding:0 12px;min-width:44px;box-sizing:border-box;transition:width .6s}.pz2-bar i:last-child{justify-content:flex-end}.pz2-bar b{color:#fff;font-size:1rem}
.pz2-bl{display:flex;justify-content:space-between;margin:0 0 8px;font-size:.76rem;font-weight:700}.pz2-gain{margin:2px 0 8px;font-weight:900;font-size:1.15rem}.pz2-gain.z{font-size:.85rem;font-weight:700;opacity:.8}
.pz2-me{border-radius:16px;padding:10px 12px;margin:0 0 10px}
.pz2-tip{display:flex;align-items:center;gap:10px;width:100%;text-align:left;border:0;border-radius:14px;padding:10px 12px;margin:0 0 12px;font:inherit;cursor:pointer}.pz2-ti{font-size:1.3rem}.pz2-tip b{display:block;font-size:.92rem}.pz2-tip small{font-size:.78rem;line-height:1.3}.pz2-tip em{margin-left:auto;font-style:normal;font-weight:900;font-size:.82rem;white-space:nowrap}
html:not(.yg) .qs3-k{color:#2F6B3F}html:not(.yg) .qs3-h{color:#1F2F55}html:not(.yg) .qs3-sub{color:#5B4E45}html:not(.yg) .qs3-sb>div{background:#fff;box-shadow:inset 0 0 0 1.5px #E6D9C4;color:#2B2320}html:not(.yg) .qs3-sb>div.w{background:#FFF6DC;box-shadow:inset 0 0 0 2px #D9A441}html:not(.yg) .qs3-sb b{color:#1F2F55}html:not(.yg) .qs3-badge{background:#2D4E86;color:#fff}
html:not(.yg) .qs3-cmp{background:#F3EBDD;color:#2B2320}html:not(.yg) .qs3-up{background:#E6F3E9;color:#1F4A2B}
html:not(.yg) .pc2-pool>b{color:#2F6B3F}html:not(.yg) .pc2-pool>span{color:#2B2320}html:not(.yg) .pc2-pool em{color:#5B4E45}html:not(.yg) .pc2-vs small{color:#5B4E45}
html:not(.yg) .pc2-stake .w{background:#E6F3E9;color:#1F4A2B}html:not(.yg) .pc2-stake .l{background:#F3EBDD;color:#5B4E45}html:not(.yg) .pc2-me{color:#2B2320}html:not(.yg) .pc2-how{color:#5B4E45}
html:not(.yg) .pz2-s{color:#5B4E45}html:not(.yg) .pz2-x{color:#2B1D14}html:not(.yg) .pz2-bar i:first-child{background:#2D4E86}html:not(.yg) .pz2-bar i:last-child{background:#C98A12}html:not(.yg) .pz2-bl{color:#5B4E45}
html:not(.yg) .pz2-gain{color:#2F6B3F}html:not(.yg) .pz2-gain.l{color:#9E2F2A}html:not(.yg) .pz2-gain.z{color:#5B4E45}html:not(.yg) .pz2-me{background:#fff;box-shadow:inset 0 0 0 1.5px #E6D9C4}html:not(.yg) .pz2-tip{background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #E5C77A;color:#2B2320}html:not(.yg) .pz2-tip em{color:#2D4E86}
html.yg .qs3-k{color:#2EE59D}html.yg .qs3-h{color:#fff}html.yg .qs3-sub{color:#C9B8FF}html.yg .qs3-sb>div{background:#241544;color:#E9E2FF}html.yg .qs3-sb>div.w{background:#2A1A46;box-shadow:inset 0 0 0 2px #FFC93C}html.yg .qs3-sb b{color:#fff}html.yg .qs3-badge{background:#FFC93C;color:#1B0F33}
html.yg .qs3-cmp{background:#241544;color:#E9E2FF}html.yg .qs3-up{background:#0E3A2A;color:#C9FBE5}
html.yg .pc2-pool>b{color:#2EE59D}html.yg .pc2-pool>span{color:#fff}html.yg .pc2-pool em{color:#C9B8FF}html.yg .pc2-vs small{color:#C9B8FF}
html.yg .pc2-stake .w{background:#0E3A2A;color:#C9FBE5}html.yg .pc2-stake .l{background:#241544;color:#C9B8FF}html.yg .pc2-me{color:#E9E2FF}html.yg .pc2-how{color:#C9B8FF}
html.yg .pz2-s{color:#C9B8FF}html.yg .pz2-x{color:#fff}html.yg .pz2-bar i:first-child{background:#C13CFF}html.yg .pz2-bar i:last-child{background:#FF8A00}html.yg .pz2-bl{color:#C9B8FF}
html.yg .pz2-gain{color:#2EE59D}html.yg .pz2-gain.l{color:#FF7A9A}html.yg .pz2-gain.z{color:#C9B8FF}html.yg .pz2-me{background:#1B0F33;box-shadow:inset 0 0 0 1.5px #3A2766}html.yg .pz2-tip{background:#241544;box-shadow:inset 0 0 0 1.5px #FFC93C;color:#E9E2FF}html.yg .pz2-tip em{color:#FFC93C}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('improve2 ok')

# ---------- Losing a challenge never costs a star (no star loss from challenges or raids) ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("else { P.cr[k]++; if (L.you[k]) { L.you[k]--; lost = 1; } }","else { P.cr[k]++; }")
RA("'Win +1 star'} · lose −1 star</p>","'Win +1 star'} · lose and you keep your stars</p>")
RA("""lost ? '<p class="pz2-gain l">−1 ⭐</p>' : '<p class="pz2-gain z">No stars lost: you had none yet</p>'""","""'<p class="pz2-gain z">You keep your stars. Losing never costs a star.</p>'""")
RA("<div class=\"l\"><b>Lose</b><span>${y ? '−1 ⭐' : 'nothing to lose yet'}</span></div>","<div class=\"l\"><b>Lose</b><span>you keep your stars</span></div>")
RA("<p>Win <b>+1 star</b>, lose <b>−1 star</b>.</p>","<p>Win <b>+1 star</b>. Lose and you keep your stars.</p>")
RA("takeCrown(k, P.h); if (L.you[k]) L.you[k]--; save();","takeCrown(k, P.h); save();")
RA("const ks = CATS8.filter(k => (L.you[k] || 0) > 0 && lgMine(k)); if (!ks.length) { save(); return; }","const ks = []; if (!ks.length) { save(); return; } // stars are never taken away")
open(d+'yofi-simple.html','w').write(s); print('no star loss ok')

# ---------- Shared 50% split equally between everyone on 3+ stars ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA("const lgShare = k => { const L = lgS(), y = L.you[k] || 0, top = lgKing(k); return y < LG_SHARE ? 0 : +(L.jp[k] * (1 - LG_KING) * y / (L.q[k] + y) + (top.me ? L.jp[k] * LG_KING : 0)).toFixed(2); };",
   "const lgQn = k => Math.max(2, Math.round(lgS().jp[k] / 16)); // demo: players on 3+ stars today grows with the pool (about $16 of pool per qualifier at $2 a challenge)\nconst lgShare = k => { const L = lgS(), y = L.you[k] || 0, top = lgKing(k); return y < LG_SHARE ? 0 : +(L.jp[k] * (1 - LG_KING) / lgQn(k) + (top.me ? L.jp[k] * LG_KING : 0)).toFixed(2); };")
RA("shares the other <b>50%</b>. More stars, bigger share.</p>","shares the other <b>50%</b> equally.</p>")
RA("Everyone with 3+ stars shares the other 50%, by stars.","Everyone with 3+ stars shares the other 50% equally.")
RA("'you’re sharing the pool · more stars, bigger share'","`you’re in · an equal share with ${lgQn(k) - 1} others`")
RA("⭐ ${LG_SHARE}+ stars share <b>50%</b></p>","⭐ ${LG_SHARE}+ stars share <b>50%</b> equally</p>")
open(d+'yofi-simple.html','w').write(s); print('equal ok')

# ---------- Prize pools: 20% rake (80c of $1 to the pool); most stars wins 30%, 3+ stars share 70% equally ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
RA("LG_KING = .5, LG_CUT = .85; // every $1 battle: 85¢ to today's pot, 15¢ house.","LG_KING = .3, LG_CUT = .8; // every $1 challenge: 80¢ to today's pot, 20¢ house. Most stars 30%, 3+ stars share 70%.")
RA("<b>85¢</b> goes into that category’s daily cash pot.","<b>80¢</b> goes into that category’s daily cash pot.")
RA("wins <b>50%</b> of the pot.</p>","wins <b>30%</b> of the pot.</p>")
RA("shares the other <b>50%</b> equally.</p>","share the other <b>70%</b> equally.</p>")
RA("🏆 Most stars wins 50% · 3+ stars share 50%","🏆 Most stars wins 30% · 3+ stars share 70%")
RA("· <b>+1 star</b> · 85¢ goes into today’s pot","· <b>+1 star</b> · 80¢ goes into today’s pot")
RA("At midnight the highest score takes 50% of the pot. Everyone with 3+ stars shares the other 50% equally.","At midnight the most stars takes 30% of the pot. Everyone with 3+ stars shares the other 70% equally.")
RA("🏆 Most stars wins <b>50%</b> · ⭐ ${LG_SHARE}+ stars share <b>50%</b> equally","🏆 Most stars wins <b>30%</b> · ⭐ ${LG_SHARE}+ stars share <b>70%</b> equally")
RA("every $1 challenge adds 85c","every $1 challenge adds 80c")
RA("${frSt() === 1 ? '85¢' : money(.85 * frSt())} goes into the club pot","${frSt() === 1 ? '80¢' : money(.8 * frSt())} goes into the club pot")
open(d+'yofi-simple.html','w').write(s); print('split ok')

# ---------- 15 votes per photo challenge (was 30); pot challenges cost $2 (was $1) ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
RA("N = 30", "N = 15", 5)
RA("16 + Math.floor(Math.random() * 4) : 10 + Math.floor(Math.random() * 5)", "8 + Math.floor(Math.random() * 3) : 4 + Math.floor(Math.random() * 4)", 5)
RA("a = 16 + Math.floor(Math.random() * 3)", "a = 8 + Math.floor(Math.random() * 3)", 2)
RA("${30 - a}", "${15 - a}", 2)
RA("<span>${30} votes</span>", "<span>${N} votes</span>")
# $2 pot challenges
RA("const LG_SHARE = 3, LG_KING = .3, LG_CUT = .8;", "const LG_FEE = 2, LG_SHARE = 3, LG_KING = .3, LG_CUT = .8;")
RA("payCash(1, 'A challenge', then);", "payCash(LG_FEE, 'A challenge', then);")
RA("if (cur === 'cash') L.jp[k] = +(L.jp[k] + LG_CUT).toFixed(2);", "if (cur === 'cash') L.jp[k] = +(L.jp[k] + LG_CUT * LG_FEE).toFixed(2);")
RA("S.lg.jp[k] = +(S.lg.jp[k] + LG_CUT * (1 + Math.floor(Math.random() * 6))).toFixed(2);", "S.lg.jp[k] = +(S.lg.jp[k] + LG_CUT * LG_FEE * (1 + Math.floor(Math.random() * 6))).toFixed(2);")
RA("Every challenge costs <b>$1</b>. <b>80¢</b> goes into that category’s daily cash pot.", "Every challenge costs <b>$2</b>. <b>$1.60</b> goes into that category’s daily cash pot.")
RA("· <b>+1 star</b> · 80¢ goes into today’s pot", "· <b>+1 star</b> · $1.60 goes into today’s pot")
RA("Today’s photo challenges`} · $1</button>", "Today’s photo challenges`} · $2</button>")
RA("'Challenge now'} · $1</button>", "'Challenge now'} · $2</button>")
RA("id=\"lbMore\">${VS_IC}Challenge again · $1</button>", "id=\"lbMore\">${VS_IC}Challenge again · $2</button>")
RA("id=\"lbRev\">${VS_IC}Rematch · $1</button>", "id=\"lbRev\">${VS_IC}Rematch · $2</button>")
RA("Rematch · ${c ? frLab() : '$1'}</button>", "Rematch · ${c ? frLab() : '$2'}</button>")
RA("cta: 'Rematch · $1', onCta: () => revengePrep(null, k, P.h)", "cta: 'Rematch · $2', onCta: () => revengePrep(null, k, P.h)")
open(d+'yofi-simple.html','w').write(s); print('v15 $2 ok')

# ---------- $2 challenge price everywhere a player can see it ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
n=s.count('Each entry is $1 and most of it goes into that day’s prize pot.'); assert n>=1
s=s.replace('Each entry is $1 and most of it goes into that day’s prize pot.','Each photo challenge is $2, and $1.60 of it goes into that category’s prize pot.')
RA("Entries are $1. Prize pots pay at midnight.","Photo challenges are $2. Prize pots pay at midnight.")
RA("cta: 'Rematch · $1', onCta: () => lgPay(() => lgFight(k, P.h, false, true))","cta: 'Rematch · $2', onCta: () => lgPay(() => lgFight(k, P.h, false, true))")
RA("// every $1 challenge: 80¢ to today's pot, 20¢ house.","// every $2 challenge: $1.60 to today's pot, 40¢ house.")
open(d+'yofi-simple.html','w').write(s); print('price2 ok', n)

# ---------- Amounts and scores on the new screens use the site's money font ----------
s=open(d+'yofi-simple.html').read()
SEL=".pc-pot,.pc2-pool>b,.pc-vs strong,.pz-pool>b,.pz-vs strong,.qs2-prize b,.qs2-big,.qs2-st b,.qs3-sb b,.qs3-h,.pz2-bar b,.pz2-gain:not(.z),.qs2-tb .rw,.pz2-me p b,.pc2-me p b,.qs3-up b b,.th-hd em,.qs2-stat"
sel=lambda pre: ",".join(pre+" "+x for x in SEL.split(","))
s=s.replace('</style>',sel("html:not(.yg)")+"{font-family:\"Fraunces\",serif!important;font-weight:900!important;letter-spacing:0}\n"+sel("html.yg")+"{font-family:\"Bricolage Grotesque\",sans-serif!important;font-weight:900!important}\nhtml:not(.yg) .qs2-stat{font-weight:800!important;letter-spacing:.03em}\n</style>",1)
open(d+'yofi-simple.html','w').write(s); print('font ok')

# ---------- Replace the 🟡 emoji (and 💎 in the young look) with the real coin/gem icon everywhere ----------
s=open(d+'yofi-simple.html').read()
s=s.replace("function fcNotify() {",r"""(function coinIcons() {
  const bad = () => window.__young ? /🟡|💎/ : /🟡/;
  const fix = root => { if (!root || typeof gemIcon !== 'function') return; const re = bad(), list = [];
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => re.test(n.nodeValue) && !(n.parentElement && n.parentElement.closest('script,style,textarea,input,option,title')) ? 1 : 2 });
    while (w.nextNode()) list.push(w.currentNode);
    list.forEach(n => { if (!n.parentNode) return; const parts = n.nodeValue.split(window.__young ? /🟡|💎/ : /🟡/), f = document.createDocumentFragment();
      parts.forEach((p, i) => { if (i) { const sp = document.createElement('span'); sp.className = 'coin-ic'; sp.innerHTML = gemIcon(''); f.appendChild(sp); } if (p) f.appendChild(document.createTextNode(p)); });
      n.parentNode.replaceChild(f, n); }); };
  let busy = false; const mo = new MutationObserver(ms => { if (busy) return; busy = true;
    ms.forEach(m => { if (m.type === 'characterData') fix(m.target.parentNode); else m.addedNodes.forEach(x => x.nodeType === 1 ? fix(x) : x.parentNode && fix(x.parentNode)); });
    mo.takeRecords(); busy = false; });
  const go = () => { fix(document.body); mo.observe(document.body, { childList: true, subtree: true, characterData: true }); };
  if (document.body) go(); else document.addEventListener('DOMContentLoaded', go);
})();
function fcNotify() {""",1)
s=s.replace('</style>',""".coin-ic{display:inline-flex;align-items:center;vertical-align:-.12em;line-height:1}.coin-ic svg{width:.95em!important;height:.95em!important;vertical-align:0!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('coin icons ok')

# ---------- Your day: stars and prize pools instead of share/ribbons; 3 dots; shares shown as estimates ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
RA("const dots = y => [1, 2, 3, 4, 5].map(i => `<i class=\"${i <= y ? 'on' : ''}\"></i>`).join('');","const dots = y => [...Array(LG_SHARE)].map((_, i) => `<i class=\"${i < y ? 'on' : ''}\"></i>`).join('');")
RA("""body = `<div class="yd-sum"><div class="${inP.length ? 'hot' : ''}"><b class="gr">${money(inP.length ? tot : 0)}</b><small>Current share</small></div><div><b>🏅 ${held}</b><small>Blue ribbons held</small></div><div><b>⏱ ${dayLeft()}</b><small>Until payout</small></div></div>
    <p class="yd-big">Have <em>${LG_SHARE} stars</em> at midnight to share the pot.</p>""",
   """const stT = rows.reduce((a, r) => a + r.y, 0), pools = CATS8.reduce((a, k) => a + (L.jp[k] || 0), 0);
    body = `<div class="yd-sum"><div class="${stT ? 'hot' : ''}"><b>⭐ ${stT}</b><small>Stars today</small></div><div><b class="gr">$${Math.round(pools).toLocaleString()}</b><small>Prize pools</small></div><div><b>⏱ ${dayLeft()}</b><small>Until payout</small></div></div>
    ${inP.length ? `<p class="yd-big">You’ve qualified in <em>${inP.length} categor${inP.length === 1 ? 'y' : 'ies'}</em>. About <em>${money(tot)}</em> if it ended now.</p><p class="yd-est">An estimate: it changes as more players reach ${LG_SHARE} stars before midnight.</p>` : `<p class="yd-big">Have <em>${LG_SHARE} stars</em> at midnight to share the pot.</p>`}""")
RA("let html = '<span class=\"hp-d\"><i></i><i></i><i></i><i></i><i></i></span>'","let html = '<span class=\"hp-d\"><i></i><i></i><i></i></span>'")
RA("<span class=\"hp-d\">${[1, 2, 3, 4, 5].map(i => `<i class=\"${i <= best.y ? 'on' : ''}\"></i>`).join('')}</span>","<span class=\"hp-d\">${[...Array(LG_SHARE)].map((_, i) => `<i class=\"${i < best.y ? 'on' : ''}\"></i>`).join('')}</span>")
RA("html = `<span class=\"hp-ok\">✓ ${money(t)}</span>","html = `<span class=\"hp-ok\">✓ ≈${money(t)}</span>")
RA("lab = `In ${inP.length} pot${inP.length === 1 ? '' : 's'}, ${money(t)} so far`;","lab = `In ${inP.length} pot${inP.length === 1 ? '' : 's'}, about ${money(t)} if it ended now`;")
RA("`you’re in · <b>${money(lgShare(k))}</b> so far`","`you’re in · about <b>${money(lgShare(k))}</b> if it ended now`")
s=s.replace('</style>',""".yd-est{margin:-6px 0 12px;text-align:center;font-size:.8rem;opacity:.75}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('your day ok')

# ---------- First-time prize pool intro (newbies): simpler card, button above the fold; regular card after that ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
RA("function potIntro(p) { potCard((p && CATS8.find(x => fitsTheme(p, x))) || CATS8[0]); }", r"""function potIntro(p) { const k = (p && CATS8.find(x => fitsTheme(p, x))) || CATS8[0], L = lgS(), H = lgHold(k), mine = lgMine(k);
  if (!mine || H.h === 'you') { potCard(k); return; }
  const opp = H.h, onVote = $('#panes').dataset.at === 'judge', cn = esc(crownName(k));
  setTimeout(() => { openSheet(`<div class="pn"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <span class="pn-new">New · Daily prize pools</span><h2 class="pn-h">Win real cash with your photo</h2>
    <div class="pn-pool"><small>${gi(k)} Today’s ${cn} prize pool</small><b>$${Math.round(L.jp[k]).toLocaleString()}</b><em>⏱ Pays at midnight · <span data-wk>${dayLeft()}</span> left</em></div>
    <ol class="pn-st"><li><span>1</span><p><b>Challenge for $2.</b> Your photo against another. Members vote.</p></li>
      <li><span>2</span><p><b>Win ${LG_SHARE} to qualify.</b> Lose and you keep your stars.</p></li>
      <li><span>3</span><p><b>Share 70% of the pool</b> at midnight. Most stars wins 30%.</p></li></ol>
    <div class="pn-vs"><img src="${mine.src}" alt=""><span class="pn-x">VS</span><img src="${lgPhoto(opp, k)}" alt=""><p><b>You vs @${esc(opp)}</b><small>${CRW}holds the ${cn} blue ribbon</small></p></div>
    <button class="btn block pc-go" id="pnGo">${VS_IC}Challenge now · $${LG_FEE}</button>
    <div style="text-align:center"><button class="link pc-later" id="pnLater">${onVote ? (isYoungW() ? 'Keep judging' : 'Keep voting') : 'Not now'}</button></div></div>`);
    $('#pnGo').onclick = () => { closeSheet(); lgPay(() => lgFight(k, opp, true)); };
    $('#pnLater').onclick = () => closeSheet();
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet()); }, 380); }""")
s=s.replace('</style>',""".pn{position:relative;text-align:center;padding:4px 2px 2px}.pn-new{display:inline-block;margin:6px 0 6px;padding:4px 12px;border-radius:999px;font-size:.74rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase}
.pn-h{margin:0 26px 10px;font-size:1.6rem;line-height:1.1}.pn-pool{border-radius:18px;padding:10px 12px;margin:0 0 12px}.pn-pool small{display:flex;align-items:center;justify-content:center;gap:6px;font-weight:800;font-size:.88rem}.pn-pool small svg{width:16px;height:16px}
.pn-pool b{display:block;font-size:2.8rem;line-height:1.05;margin:2px 0}.pn-pool em{font-style:normal;font-size:.82rem;font-weight:700}
.pn-st{list-style:none;margin:0 0 12px;padding:0;display:grid;gap:8px;text-align:left}.pn-st li{display:flex;gap:10px;align-items:flex-start}.pn-st li>span{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:.85rem}.pn-st p{margin:2px 0 0;font-size:.92rem;line-height:1.35}
.pn-vs{display:flex;align-items:center;gap:8px;border-radius:16px;padding:8px 10px;margin:0 0 12px;text-align:left}.pn-vs img{width:52px;height:52px;border-radius:12px;object-fit:cover;flex:none}.pn-x{font-weight:900;font-size:.8rem;flex:none}.pn-vs p{margin:0 0 0 4px;line-height:1.25}.pn-vs b{display:block;font-size:.92rem}.pn-vs small{font-size:.78rem}.pn-vs small .crw-ic{width:11px;height:14px;vertical-align:-2px;margin-right:3px}
html:not(.yg) .pn-new{background:#FBC20A;color:#2B1D14}html:not(.yg) .pn-h{color:#1F2F55}html:not(.yg) .pn-pool{background:#E6F3E9;box-shadow:inset 0 0 0 2px #2F6B3F;color:#1F4A2B}html:not(.yg) .pn-pool b{color:#2F6B3F;font-family:"Fraunces",serif;font-weight:900}
html:not(.yg) .pn-st li>span{background:#2D4E86;color:#fff}html:not(.yg) .pn-st p{color:#2B2320}html:not(.yg) .pn-vs{background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #E5C77A;color:#2B2320}html:not(.yg) .pn-vs img{box-shadow:0 0 0 2px #2D4E86}
html.yg .pn-new{background:#FFC93C;color:#1B0F33}html.yg .pn-h{color:#fff}html.yg .pn-pool{background:#0E3A2A;box-shadow:inset 0 0 0 2px #2EE59D;color:#C9FBE5}html.yg .pn-pool b{color:#2EE59D;font-family:"Bricolage Grotesque",sans-serif;font-weight:900}
html.yg .pn-st li>span{background:#C13CFF;color:#fff}html.yg .pn-st p{color:#E9E2FF}html.yg .pn-vs{background:#241544;box-shadow:inset 0 0 0 1.5px #FFC93C;color:#E9E2FF}html.yg .pn-vs img{box-shadow:0 0 0 2px #C13CFF}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('newbie pot ok')

# ---------- New Daily rewards (streak) pop from the user's design; Freeroll rows say clearly if you can enter or are in ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
i=s.index('function streakPop() {'); j=s.index('\nfunction ', i+10)
old=s[i:j]; a0=old.index('const ART = ['); a1=old.index('];', a0)+2; ART=old[a0:a1]
s=s[:i]+"function streakPop() {\n  const ds = dailyState(), n = Math.min(3, ds.D.sn || 0), done = ds.doneToday, st = ds.streak || 0, inToday = ds.D.last === ds.t, had = (ds.D.streak || 0) > 0 && !st, G = gemIcon('');\n  "+ART+r"""
  const vw = isYoungW() ? 'Judge' : 'Vote', vd = isYoungW() ? 'judged' : 'voted';
  const k = i => ds.D.got.includes(i) ? 'got' : i === ds.si ? 'now' : i < ds.si ? 'miss' : 'later';
  const card = (nm, i) => { const q = k(i); return `<div class="dr-c ${q}"><small>${nm}</small><span class="dr-a">${q === 'got' ? '<b class="dr-ok">✓</b>' : q === 'miss' ? '<b class="dr-ms">✕</b>' : ART[i]}</span><em>${q === 'got' ? 'Done' : q === 'miss' ? 'Missed' : q === 'now' ? 'Now' : 'Later'}</em></div>`; };
  const stLine = st ? `<b>${st}-day streak</b>${inToday ? '<span class="dr-pill ok">✓ Today complete</span>' : `<span class="dr-pill">${vw} 3 today</span>`}` : `<b>${had ? 'Your streak ended' : 'Start a streak'}</b><span class="dr-pill">${vw} 3 today</span>`;
  const stSub = st ? (inToday ? 'Come back tomorrow to keep your streak.' : 'Vote on 3 photos today to keep it alive.') : 'Vote on 3 photos today to light your first 🔥';
  const c = $('#coach');
  c.innerHTML = `<div class="cpr dr" role="dialog" aria-modal="true" aria-labelledby="drT"><button class="qs2-x" id="drX" aria-label="Close">${QS_X}</button>
    <p class="dr-k">Daily rewards</p>
    ${done ? `<h2 class="dr-h" id="drT">${SESS[ds.si]} reward collected</h2><p class="dr-big ok">${G}+${STREAK_GEMS} coins ✓</p><span class="dr-when">${ds.si < 3 ? `Next reward from ${SESS_AT[ds.si + 1]}` : 'Next reward after midnight'}</span>`
      : `<h2 class="dr-h" id="drT">Vote on 3 photos to earn</h2><p class="dr-big">${G}+${STREAK_GEMS} coins</p><span class="dr-when">${SESS[ds.si]} · available now</span>
         <div class="dr-bars">${[0, 1, 2].map(x => `<i class="${x < n ? 'on' : ''}"></i>`).join('')}</div><p class="dr-n">${n} of 3 photos ${vd}</p>`}
    <button class="bt-cta dr-go" id="drGo">⚖️ ${done ? `Keep ${isYoungW() ? 'judging' : 'voting'}` : n ? `${vw} ${3 - n} more` : `${vw} now`}</button>
    <div class="dr-th"><b>Today’s rewards</b><span>${ds.gotToday} of 4 completed</span></div>
    <div class="dr-g">${SESS.map(card).join('')}</div>
    <p class="dr-note">Vote on 3 photos in each session to earn ${STREAK_GEMS} coins.</p>
    <div class="dr-st"><span class="dr-fl">🔥</span><div><div class="dr-sl">${stLine}</div><small>${stSub}</small></div></div>
    <button class="link dr-how" id="drHow">How it works</button>
    <p class="dr-hw" id="drHw" hidden>There are 4 sessions a day: night (from midnight), morning (6am), afternoon (noon) and evening (6pm). Vote on 3 photos in a session to collect its coins. Vote on 3 photos on any day to add a day to your streak. Miss a day and the streak starts again.</p>
    <button class="bt-no" id="drLater">Later</button></div>`;
  c.classList.add('on', 'cr');
  const close = () => c.classList.remove('on', 'cr');
  $('#drGo').onclick = () => { close(); go('judge'); };
  $('#drLater').onclick = $('#drX').onclick = close;
  $('#drHow').onclick = () => { $('#drHw').hidden = !$('#drHw').hidden; };
  c.onclick = e => { if (e.target === c) close(); };
}"""+s[j:]
# Freeroll rows: clear status
RA("""<button class="tsr2 frrow ${e ? 'in' : ''}" data-frrow="${f.id}"><span class="tsr2-t"><span class="fr-tag">FREEROLL</span>""",
   """<button class="tsr2 frrow ${e ? 'in' : nt ? 'can' : 'need'}" data-frrow="${f.id}"><span class="tsr2-t"><span class="fr-tag">${e ? 'YOU’RE IN ✓' : 'FREEROLL'}</span>""")
RA("""<span class="tsr2-e">${e ? (e.bell ? '🔔 ✓' : '✓') : '🎟️ 1'}</span></button>`; }).join('');""",
   """<span class="tsr2-e">${e ? (e.bell ? '🔔 On' : '🔔 Remind') : nt ? '🎟️ Enter' : '🔒 Ticket'}</span></button>`; }).join('');""")
s=s.replace('</style>',""".dr{position:relative;text-align:center}.dr-k{margin:4px 30px 4px;font-size:.78rem;font-weight:900;letter-spacing:.2em;text-transform:uppercase}.dr-h{margin:0;font-size:1.55rem;line-height:1.15}
.dr-big{margin:2px 0 6px;font-size:2.4rem;font-weight:900;line-height:1.1}.dr-big svg{width:.85em!important;height:.85em!important;vertical-align:-.1em!important;margin-right:6px}
.dr-when{display:inline-block;padding:4px 14px;border-radius:999px;font-size:.78rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px}
.dr-bars{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:2px 10px 4px}.dr-bars i{height:12px;border-radius:999px}.dr-n{margin:0 0 10px;font-size:.88rem}
.dr-go{margin-bottom:12px}.dr-th{display:flex;justify-content:space-between;align-items:baseline;margin:4px 2px 8px}.dr-th b{font-size:1.15rem}.dr-th span{font-weight:900;font-size:.95rem}
.dr-g{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.dr-c{border-radius:14px;padding:8px 2px 6px;display:flex;flex-direction:column;align-items:center;gap:2px}.dr-c small{font-size:.74rem;font-weight:800}
.dr-a{height:38px;display:grid;place-items:center}.dr-a svg{width:36px;height:36px}.dr-ok,.dr-ms{font-size:1.8rem;line-height:1}.dr-c em{font-style:normal;font-size:.72rem;font-weight:900;text-transform:uppercase;letter-spacing:.04em}
.dr-note{margin:6px 0 10px;font-size:.8rem;opacity:.85}.dr-st{display:flex;align-items:center;gap:10px;text-align:left;padding-top:10px;border-top:1px solid rgba(127,113,103,.3)}.dr-fl{font-size:2rem}
.dr-sl{display:flex;align-items:center;flex-wrap:wrap;gap:6px 8px}.dr-sl b{font-size:1.2rem}.dr-pill{padding:3px 10px;border-radius:999px;font-size:.76rem;font-weight:800}.dr-st small{font-size:.82rem}
.dr-how{margin:8px auto 0;display:block}.dr-hw{font-size:.8rem;text-align:left;margin:6px 0 0;line-height:1.4}
html:not(.yg) .dr-k{color:#5B4E45}html:not(.yg) .dr-h,html:not(.yg) .dr-th b,html:not(.yg) .dr-sl b{color:#2B1D14}html:not(.yg) .dr-big{color:#2D4E86;font-family:"Fraunces",serif}html:not(.yg) .dr-big.ok{color:#2F6B3F}
html:not(.yg) .dr-when{background:#FFE9B0;color:#2B1D14}html:not(.yg) .dr-bars i{background:#F3EBDD;box-shadow:inset 0 0 0 1.5px #D8CCB6}html:not(.yg) .dr-bars i.on{background:#FBC20A;box-shadow:none}html:not(.yg) .dr-n,html:not(.yg) .dr-note,html:not(.yg) .dr-st small,html:not(.yg) .dr-hw{color:#5B4E45}
html:not(.yg) .dr-th span{color:#2F6B3F}html:not(.yg) .dr-c{background:#FFFDF8;box-shadow:inset 0 0 0 1.5px #E6D9C4;color:#2B2320}html:not(.yg) .dr-c.now{background:#E3ECFA;box-shadow:inset 0 0 0 2.5px #2D4E86}html:not(.yg) .dr-c.now em{color:#1F2F55}
html:not(.yg) .dr-c.miss{background:#EFEAE2;color:#5B4E45}html:not(.yg) .dr-ms{color:#5B4E45}html:not(.yg) .dr-ok{color:#2F9E55}html:not(.yg) .dr-c.later em{color:#7F7167;font-weight:700}html:not(.yg) .dr-c.got em{color:#2F6B3F}
html:not(.yg) .dr-pill{background:#FFE9B0;color:#5B3A00}html:not(.yg) .dr-pill.ok{background:#DDF0E1;color:#1F4A2B}
html.yg .dr-k{color:#C9B8FF}html.yg .dr-h,html.yg .dr-th b,html.yg .dr-sl b{color:#fff}html.yg .dr-big{color:#FFC93C;font-family:"Bricolage Grotesque",sans-serif}html.yg .dr-big.ok{color:#2EE59D}
html.yg .dr-when{background:#3A2A0A;color:#FFC93C}html.yg .dr-bars i{background:#2A1A46}html.yg .dr-bars i.on{background:#FBC20A}html.yg .dr-n,html.yg .dr-note,html.yg .dr-st small,html.yg .dr-hw{color:#C9B8FF}
html.yg .dr-th span{color:#2EE59D}html.yg .dr-c{background:#1E1236;box-shadow:inset 0 0 0 1.5px #3A2766;color:#E9E2FF}html.yg .dr-c.now{background:#2A1A46;box-shadow:inset 0 0 0 2.5px #FF3FA4}html.yg .dr-c.now em{color:#FF3FA4}
html.yg .dr-c.miss{background:#160B2E;color:#8E7DB8}html.yg .dr-ms{color:#8E7DB8}html.yg .dr-ok{color:#2EE59D}html.yg .dr-c.got em{color:#2EE59D}html.yg .dr-c.later em{color:#8E7DB8}
html.yg .dr-pill{background:#3A2A0A;color:#FFC93C}html.yg .dr-pill.ok{background:#0E3A2A;color:#2EE59D}
.tsr2.frrow.in.in{box-shadow:inset 0 0 0 2.5px #2F9E55!important}html .tsr2.frrow.in .fr-tag.fr-tag{background:#2F9E55!important;color:#fff!important}html .tsr2.frrow.in .tsr2-e.tsr2-e{background:#fff!important;color:#2F6B3F!important;box-shadow:inset 0 0 0 2px #2F9E55}
html .tsr2.frrow.need .tsr2-e.tsr2-e{background:#CFC6B8!important;color:#4A3F37!important}html.yg .tsr2.frrow.need .tsr2-e.tsr2-e.tsr2-e{background:#3A2766!important;color:#C9B8FF!important}
.tsr2.frrow .tsr2-e{font-size:.9rem!important;white-space:nowrap}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('streak + freeroll ok')

# ---------- Real-money focus: no coin sales, free first touch-up per photo, photo lives (5 losses), no energy cap, "Your eye" score ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# 1) Free first touch-up on every photo
RA("const fixCost = p => !p ? CFG.COST :","const fixLab = p => fixCost(p) ? fixCost(p) + ' 🟡' : 'Free';\nconst fixCost = p => p && !p.tu1 ? 0 : fixCost0(p);\nconst fixCost0 = p => !p ? CFG.COST :")
RA("S.gems -= cost; save(); paintGems(); const firstRun","S.gems -= cost; p.tu1 = 1; save(); paintGems(); const firstRun")
RA("${fixCost(p)} 🟡","${fixLab(p)}",4)
RA("${fixCost(p)} ${G}","${fixCost(p) ? fixCost(p) + ' ' + G : 'Free'}")
RA("${gemIcon()}${fixCost(p)}","${fixCost(p) ? gemIcon() + fixCost(p) : 'Free'}",2)
RA("${gemIcon()}${cost}","${cost ? gemIcon() + cost : 'Free'}")
# 2) No coin sales: cash packs are cash only; coin "+" and "need coins" lead to earning by voting
RA("checkout(`$${k.cash} cash + ${k.gems.toLocaleString()} coins + ${CASH_EN[i]} energy`, k.cash, () => buyPack(i, onBuy));","checkout(`$${k.cash} cash`, k.cash, () => buyPack(i, onBuy));")
RA("if (CASH_EN[i]) { energy(); S.en += CASH_EN[i]; S.enAt = Date.now(); }","")
RA("setTimeout(() => { addGems(k.gems, `${k.t} pack`); if ($('#panes').dataset.at === 'studio' && !$('#flow').classList.contains('on')) setTimeout(renderStudio, 1900); }, 2300);","")
RA("tile('💵', '$' + k.cash, 'Cash', 'cs') + tile(GEM, k.gems.toLocaleString(), 'Free coins', 'gm') + tile('⚡', CASH_EN[i], 'Free energy', 'en')","tile('💵', '$' + k.cash, 'Cash to play', 'cs')")
RA("sub: `cash to play + ${coins.toLocaleString()} free coins`","sub: 'cash to play'")
RA("checkout(`$${cash} cash + ${coins.toLocaleString()} coins`, cash, () => applyOffer(cash, coins,","checkout(`$${cash} cash`, cash, () => applyOffer(cash, 0,",2)
RA("buy: () => checkout(`${GEM_PACKS[0].gems.toLocaleString()} coins`, GEM_PACKS[0].usd, () => { S.paidCash = true; addGems(GEM_PACKS[0].gems, `${GEM_PACKS[0].gems} coin pack`); if (onBuy) setTimeout(onBuy, 2000); }),",
   "buy: () => { c.classList.remove('on', 'cr'); if ($('#flow').classList.contains('on')) closeFlow(); go('judge'); renderJudge(); },")
RA("big: `${gemIcon('')}${GEM_PACKS[0].gems.toLocaleString()}`, sub: `coins · enough for ${Math.floor(GEM_PACKS[0].gems / 50)} improvements`,","big: `${gemIcon('')}+${STREAK_GEMS}`, sub: 'every session of 3 votes, plus coins for every vote',")
RA("<button class=\"enh-go\" id=\"roBuy\">${kind === 'energy' ? `Pay $${cfg.usd} from cash` : `Buy · $${(+cfg.usd).toFixed(2)}`}</button>","<button class=\"enh-go\" id=\"roBuy\">${kind === 'energy' ? `Pay $${cfg.usd} from cash` : kind === 'gems' ? (isYoungW() ? '⚖️ Judge to earn' : '⚖️ Vote to earn') : `Buy · $${(+cfg.usd).toFixed(2)}`}</button>")
RA("<button class=\"ro-all\" id=\"roAll\">See all packs</button></div>`;","${kind === 'gems' ? '<p class=\"ro-note\">Coins can’t be bought. Earn them by voting.</p>' : '<button class=\"ro-all\" id=\"roAll\">See all packs</button>'}</div>`;")
RA("if (e.target.closest('#gemPill .gplus') || e.target.closest('#walletPlus')) { e.preventDefault(); e.stopPropagation(); openStore(); }","if (e.target.closest('#gemPill .gplus')) { e.preventDefault(); e.stopPropagation(); runOut('gems', 'Earn coins by voting'); } else if (e.target.closest('#walletPlus')) { e.preventDefault(); e.stopPropagation(); openStore(); }")
# 3) No energy cap
RA("function energy() { const now = Date.now(); if (S.en == null) { S.en = EN_MAX; S.enAt = now; }","function energy() { S.en = EN_MAX; S.enAt = Date.now(); return EN_MAX; const now = Date.now(); if (S.en == null) { S.en = EN_MAX; S.enAt = now; }")
# 4) Photo lives: 5 losses in cash pot challenges, then the photo retires
RA("const fighters = () => S.photos.filter(p => p.s.total >= CFG.QUALIFY)","const PH_LIVES = 5, livesLeft = p => Math.max(0, PH_LIVES - (p.losses || 0)), livesHTML = p => `<span class=\"lv\" aria-label=\"${livesLeft(p)} lives left\">${[...Array(PH_LIVES)].map((_, i) => `<i class=\"${i < livesLeft(p) ? 'on' : ''}\">${i < livesLeft(p) ? '❤️' : '🤍'}</i>`).join('')}</span>`;\nconst fighters = () => S.photos.filter(p => p.s.total >= CFG.QUALIFY && !p.retired)")
RA("else { P.cr[k]++; }","else { P.cr[k]++; me.losses = (me.losses || 0) + 1; if (me.losses >= PH_LIVES) me.retired = Date.now(); }")
RA("<small>${y} ⭐ today</small></figure><span class=\"pc-x2\">VS</span>","<small>${y} ⭐ today</small><small class=\"pc-lv\">${livesHTML(mine)} ${livesLeft(mine)} li${livesLeft(mine) === 1 ? 'fe' : 'ves'}</small></figure><span class=\"pc-x2\">VS</span>")
RA("${wk ? `<button class=\"pz2-tip\"","${!won ? (me.retired ? `<div class=\"pz2-ret\"><b>📷 This photo has retired</b><span>${PH_LIVES} losses · it keeps its record in your gallery. Upload a new ${esc(crownName(k).toLowerCase())} photo to keep going for today’s pool. Your stars stay.</span><button class=\"btn block\" id=\"lbNew\">📷 Upload a new photo</button></div>` : `<p class=\"pz2-lv\">${livesHTML(me)} <b>${livesLeft(me)} li${livesLeft(me) === 1 ? 'fe' : 'ves'} left</b> on this photo</p>`) : ''}\n        ${wk && !me.retired ? `<button class=\"pz2-tip\"")
RA("` : `<button class=\"btn block pz-go\" id=\"lbRev\">${VS_IC}Rematch · $2</button>`}","` : me.retired ? '' : `<button class=\"btn block pz-go\" id=\"lbRev\">${VS_IC}Rematch · $2</button>`}")
RA("if ($('#lbTip')) $('#lbTip').onclick","if ($('#lbNew')) $('#lbNew').onclick = () => { closeSheet(); addCatPhoto(k); };\n      if ($('#lbTip')) $('#lbTip').onclick")
# 5) Your eye: agreement with the crowd, shown on the Vote page
RA("const agree = pct[pick] >= 50, mine = pct[pick];","const agree = pct[pick] >= 50, mine = pct[pick]; S.eyeN = (S.eyeN || 0) + 1; if (agree) S.eyeOk = (S.eyeOk || 0) + 1;")
RA("<div class=\"vh\" id=\"jRes\" aria-live=\"polite\"></div>","${(S.eyeN || 0) >= 10 ? `<p class=\"eye\">👁️ <b>Your eye: ${Math.round((S.eyeOk || 0) / S.eyeN * 100)}%</b> agree with the crowd${S.potSeen && !S.geoBlock ? ' · that’s your Quick Sprint edge' : ''}</p>` : `<p class=\"eye\">👁️ Vote ${10 - (S.eyeN || 0)} more to see how often you agree with the crowd</p>`}<div class=\"vh\" id=\"jRes\" aria-live=\"polite\"></div>")
s=s.replace('</style>',""".jf-en,.vs-en{display:none!important}.ro-note{margin:10px 0 0;font-size:.85rem;opacity:.8;text-align:center}
.lv{display:inline-flex;gap:1px;font-size:.72rem;vertical-align:-.05em}.lv i{font-style:normal}.pc-lv{display:block;margin-top:2px}.pz2-lv{margin:0 0 10px;font-size:.88rem}
.pz2-ret{border-radius:16px;padding:12px 14px;margin:0 0 10px;text-align:center}.pz2-ret b{display:block;font-size:1.05rem;margin-bottom:4px}.pz2-ret span{display:block;font-size:.85rem;line-height:1.35;margin-bottom:10px}
.eye{margin:8px 0 0;text-align:center;font-size:.85rem}
html:not(.yg) .pz2-ret{background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #E5C77A;color:#2B2320}html:not(.yg) .eye{color:#5B4E45}html:not(.yg) .eye b{color:#2D4E86}html:not(.yg) .pz2-lv{color:#5B4E45}
html.yg .pz2-ret{background:#241544;box-shadow:inset 0 0 0 1.5px #FFC93C;color:#E9E2FF}html.yg .eye{color:#C9B8FF}html.yg .eye b{color:#FFC93C}html.yg .pz2-lv{color:#C9B8FF}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('real money focus ok')
s=open(d+'yofi-simple.html').read(); assert s.count("$('#roAll').onclick")==1; s=s.replace("$('#roAll').onclick","if ($('#roAll')) $('#roAll').onclick"); open(d+'yofi-simple.html','w').write(s); print('roAll ok')
s=open(d+'yofi-simple.html').read()
for a,b in [("tournaments. A small coin bonus included'","tournaments. Coins can’t be bought: earn them by voting.'"),
 ("<span class=\"enp-t\">${cfg.tag || 'Most popular'}</span>","${kind === 'gems' ? '' : `<span class=\"enp-t\">${cfg.tag || 'Most popular'}</span>`}"),
 ("<button class=\"ro-free ${cfg.freeCls || ''}\" id=\"roFree\">${cfg.free}</button>","<button class=\"ro-free ${cfg.freeCls || ''}\" id=\"roFree\" ${kind === 'gems' ? 'hidden' : ''}>${cfg.free}</button>"),
 ('`<i class="${i < livesLeft(p) ? \'on\' : \'\'}">${i < livesLeft(p) ? \'❤️\' : \'🤍\'}</i>`','`<span class="lvh ${i < livesLeft(p) ? \'on\' : \'\'}">${i < livesLeft(p) ? \'❤️\' : \'🤍\'}</span>`')]:
    assert s.count(a)==1,(a[:60],s.count(a)); s=s.replace(a,b)
s=s.replace('</style>','.lv .lvh{display:inline!important;width:auto!important;height:auto!important;background:none!important;font-size:.85rem}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('polish ok')
s=open(d+'yofi-simple.html').read()
a="${i < livesLeft(p) ? '❤️' : '🤍'}</span>"; assert s.count(a)==1
s=s.replace(a,"<svg viewBox=\"0 0 24 24\" width=\"13\" height=\"13\" aria-hidden=\"true\"><path d=\"M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.8 4.5c2.2 0 3.7 1.2 5.2 3 1.5-1.8 3-3 5.2-3 3.8 0 5.9 3.9 4.4 7.3C19.5 16.4 12 21 12 21z\"/></svg></span>")
s=s.replace('</style>','.lv{gap:2px!important;align-items:center}.lv .lvh svg{display:block;fill:#D9D2C7}.lv .lvh.on svg{fill:#D6453D}html.yg .lv .lvh svg{fill:#3A2766}html.yg .lv .lvh.on svg{fill:#FF4F7B}\n.ro-free[hidden]{display:none!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('hearts ok')
s=open(d+'yofi-simple.html').read()
a='`<span class="lv" aria-label'; assert s.count(a)==1; s=s.replace(a,'`<span class="plv" aria-label')
s=s.replace('</style>','.plv{display:inline-flex!important;gap:2px;align-items:center;vertical-align:-2px;margin-right:3px}.plv .lvh svg{display:block;fill:#D9D2C7}.plv .lvh.on svg{fill:#D6453D}html.yg .plv .lvh svg{fill:#3A2766}html.yg .plv .lvh.on svg{fill:#FF4F7B}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('plv ok')
s=open(d+'yofi-simple.html').read(); a="const fixCost = p => p && !p.tu1 ? 0 : fixCost0(p);"; assert s.count(a)==1; s=s.replace(a,"const fixCost = p => fixCost0(p);"); open(d+'yofi-simple.html','w').write(s); print('touch-ups cost coins ok')

# ---------- Menu order Vote · Compete · Touch-ups · Tournaments; returning players open on Vote; first deposit gets the first $2 challenge on us ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
RA("big: `$${cash}`, sub: 'cash to play', usd: cash,","big: w ? `$${cash} <small class=\"ro-plus\">+ $2 free</small>` : `$${cash}`, sub: w ? 'cash to play · your first $2 challenge is on us' : 'cash to play', usd: cash,")
RA("checkout(`$${cash} cash`, cash, () => applyOffer(cash, 0, w ? 'Welcome offer' : '$5 pack', onBuy))","checkout(`$${cash} cash`, cash, () => applyOffer(cash + (w ? 2 : 0), 0, w ? 'Welcome offer · $2 free' : '$5 pack', onBuy))")
s=s.replace("function fcNotify() {",r"""(function navOrder() {
  const run = () => { const nav = document.querySelector('nav.seg'), j = $('#segJudge'), g = $('#segGallery'), st = $('#segStudio'), sw = document.querySelector('nav.seg .segsw'), pair = document.querySelector('nav.seg .segpair');
    if (!nav || !j || !g) return; nav.insertBefore(j, g); if (sw) sw.style.display = 'none'; if (pair && st) { nav.insertBefore(st, pair); pair.style.display = 'none'; }
    // returning players open on Vote; new players keep the upload path
    setTimeout(() => { try { if (S.user && S.gbDone && $('#panes').dataset.at === 'gallery' && !$('#flow').classList.contains('on')) { go('judge'); renderJudge(); } } catch (e) {} }, 400); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else setTimeout(run, 0);
})();
function fcNotify() {""",1)
s=s.replace('</style>','.ro-plus{font-size:.45em;vertical-align:.5em;margin-left:4px;padding:2px 8px;border-radius:999px;background:#2F6B3F!important;color:#fff!important;-webkit-text-fill-color:#fff!important}html.yg .ro-plus{background:#2EE59D!important;color:#06261A!important;-webkit-text-fill-color:#06261A!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('nav order ok')
s=open(d+'yofi-simple.html').read()
a="openStore(`${what} costs ${money(amt)} cash.`, () => (S.cash || 0) >= amt && then()); return false; }"
assert s.count(a)==1
s=s.replace(a,"openStore(`${what} costs ${money(amt)} cash.`, () => { if ((S.cash || 0) >= amt) { S.cash = +((S.cash || 0) - amt).toFixed(2); save(); paintWallet(); then(); } }); return false; }")
open(d+'yofi-simple.html','w').write(s); print('pay after deposit ok')

# ---------- Test fixes: calmer pops (one extra pop per 8 votes), invite after first cash challenge, raids only after 10 min, sign-up carries on ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# 1) pacing: optional pops (coin nudge, lucky drop) wait until 8 votes after the last pop
RA("function gemNudge(force) {","const popPaced = () => (S.votes || 0) - (S.lastPopV == null ? -99 : S.lastPopV) < 8;\nfunction gemNudge(force) {\n  if (!force && popPaced()) return false;")
RA("function luckyDrop() {\n  const LM = S.lastMult || 1, sure = 30 * LM, c = $('#coach');","function luckyDrop() {\n  const LM = S.lastMult || 1, sure = 30 * LM, c = $('#coach');\n  if (popPaced()) { S.gems += sure; save(); gemExplosion(sure, { label: 'Lucky drop · 4 in a row' }); return; }")
s=s.replace("function fcNotify() {",r"""(function popClock() { const C = $('#coach'); if (!C) return; new MutationObserver(() => { if (C.classList.contains('on') && $('#panes').dataset.at === 'judge' && S) { S.lastPopV = S.votes || 0; } }).observe(C, { attributes: true, attributeFilter: ['class'] });
  const SH = $('#sheet'); if (SH) new MutationObserver(() => { if (SH.classList.contains('on') && $('#panes').dataset.at === 'judge' && S) { S.lastPopV = S.votes || 0; } }).observe(SH, { attributes: true, attributeFilter: ['class'] }); })();
function fcNotify() {""",1)
# 2) Invite a friend only after the first cash challenge
RA("if (!comboHit && S.votes >= 10 && !S.frIntro && S.gbDone && S.user && fighters().length) {","if (!comboHit && S.votes >= 10 && !S.frIntro && S.gbDone && S.lgPlayed && !popPaced() && S.user && fighters().length) {")
RA("const L = lgS(), P = L.pl.find(p => p.h === h), me = S.photos.find(x => x.id === pid) || lgMine(k), cur = lgCurOf(), N = 15; if (!P || !me) return;","const L = lgS(), P = L.pl.find(p => p.h === h), me = S.photos.find(x => x.id === pid) || lgMine(k), cur = lgCurOf(), N = 15; if (!P || !me) return; S.lgPlayed = (S.lgPlayed || 0) + 1;")
# 3) Blue ribbon raids: 10 minutes after you take it, not 45 seconds
RA("if (won && !L.raidAt) L.raidAt = Date.now() + 45000;","if (won && !L.raidAt) L.raidAt = Date.now() + 10 * 60000;")
# 4) Sign-up carries on with what you tapped
RA("e.preventDefault(); e.stopImmediatePropagation(); openSignup(); }, true);","e.preventDefault(); e.stopImmediatePropagation(); const tid = t.id; openSignup(() => setTimeout(() => { const n = tid && document.getElementById(tid); if (n) n.click(); }, 450)); }, true);")
open(d+'yofi-simple.html','w').write(s); print('pacing ok')

# ---------- Prize pops prompt uploads; loot boxes never give energy; coin challenge buttons say Free; upload page after interests ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# 1) prize pool pop for a category you have no photo in
RA("function potCard(k) {", r"""function potUp(k) { const L = lgS(), H = lgHold(k), cn = esc(crownName(k)), onVote = $('#panes').dataset.at === 'judge';
  setTimeout(() => { openSheet(`<div class="pc pc2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pc-k">${gi(k)}<span>Daily cash challenge · ${cn}</span></p><h2 class="pc-h">Your photo. Real cash.</h2>
    <div class="pc2-pool"><b>$${Math.round(L.jp[k]).toLocaleString()}</b><span>today’s prize pool<em>⏱ Pays at midnight · <span data-wk>${dayLeft()}</span> left</em></span></div>
    <div class="pc-vs pc2-vs"><figure><button class="pu-add" id="puAdd" aria-label="Upload a ${cn} photo"><span>+</span><small>Your ${cn.toLowerCase()} photo</small></button><figcaption>You</figcaption></figure><span class="pc-x2">VS</span>
      <figure><img src="${lgPhoto(H.h, k)}" alt=""><figcaption>@${esc(H.h)}</figcaption><small>${CRW}${isYoungW() ? 'Crown' : 'Blue ribbon'} · held ${heldFor(H.since)}</small></figure></div>
    <p class="pu-t">You don’t have a <b>${cn.toLowerCase()}</b> photo yet. Upload one, get it to ${CFG.QUALIFY}+, then challenge for this pool.</p>
    <button class="btn block pc-go" id="puGo">📷 Upload a ${cn.toLowerCase()} photo</button>
    <div style="text-align:center"><button class="link pc-later" id="puLater">${onVote ? (isYoungW() ? 'Keep judging' : 'Keep voting') : 'Not now'}</button></div></div>`);
    $('#puGo').onclick = $('#puAdd').onclick = () => { closeSheet(); addCatPhoto(k); };
    $('#puLater').onclick = () => closeSheet();
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet()); }, 380); }
function potCard(k) {""")
RA("const opp = iHold ? (R.find(r => !r.me) || {}).h : H.h; if (!mine || !opp) { lgCat(k); return; }\n  const os","const opp = iHold ? (R.find(r => !r.me) || {}).h : H.h; if (!mine) { potUp(k); return; } if (!opp) { lgCat(k); return; }\n  const os")
RA("const L = lgS(), ks = CATS8.filter(k => lgMine(k));","const L = lgS(), ks = CATS8.filter(k => lgMine(k)), miss = CATS8.filter(k => k !== 'any' && !lgMine(k)).sort((a, b) => (L.jp[b] || 0) - (L.jp[a] || 0));\n    S.puAlt = !S.puAlt; save(); if (miss.length && S.potSeen && (!ks.length || S.puAlt)) { potUp(miss[0]); return; }")
# 2) loot boxes: coins only, never energy
RA("const P = kind === 3 ? [{ w: .6, k: 'g', n: 15 * LM }, { w: .3, k: 'e', n: 5 }, { w: .1, k: 'g', n: 50 * LM }]","const P = kind === 3 ? [{ w: .6, k: 'g', n: 15 * LM }, { w: .3, k: 'g', n: 25 * LM }, { w: .1, k: 'g', n: 50 * LM }]")
RA(": [{ w: .5, k: 'g', n: 25 * LM }, { w: .3, k: 'e', n: 10 }, { w: .15, k: 'g', n: 100 * LM }, { w: .05, k: 'e', n: 25 }];",": [{ w: .5, k: 'g', n: 25 * LM }, { w: .3, k: 'g', n: 40 * LM }, { w: .15, k: 'g', n: 100 * LM }, { w: .05, k: 'g', n: 150 * LM }];")
RA("energy(); S.en += rar.e; const tk","const tk")
RA("""<div class="ch-it" style="animation-delay:.45s"><b>+${rar.e}</b><small>⚡ energy</small></div>""","")
# 3) coin challenge start buttons say Free
RA("`Challenge for ${stake} 🟡`","`Free challenge · ${stake} 🟡`")
RA("cta: bme ? 'Challenge · 25 🟡'","cta: bme ? 'Free challenge · 25 🟡'")
RA('id="gbAgain">Play again for coins','id="gbAgain">Play again free · coins')
RA('id="gbAgain">Play again</button>','id="gbAgain">Play again · Free</button>')
RA("if (!opt.revenge) $('#gbAgain').onclick","if (!opt.revenge && /coins|Free/.test($('#gbAgain').textContent)) $('#gbAgain').onclick")
# 4) after interests: an upload page; the phone's photo picker only opens when the player taps
RA("""${window.__obAfter ? `<label class="btn block ob-pick" id="obGo2" for="file" role="button">📷 Choose my photo · ${picked.size} picked</label>` :""","""${window.__obAfter ? `<button class="btn block" id="obGo2" type="button">Continue · ${picked.size} picked</button>` :""")
RA("if (window.__obAfter) { window.__obAfter = null; S.likes = [...picked]; save(); obSort(); g.className = ''; setTimeout(() => g.remove(), 300); return; }",
   "if (window.__obAfter) { window.__obAfter = null; S.likes = [...picked]; save(); obSort(); obUpload(g); return; }")
RA("function obDone(g) {", r"""function obUpload(g) { const L = lgS(), k = CATS8.find(x => x !== 'any') || 'any', ex = SEED.filter(x => x.src).slice(0, 3);
  g.innerHTML = `<div class="ag-in ob obu"><div class="ob-prog"><i class="on"></i><i class="on"></i><i class="on"></i></div>
    <h1>Upload your first photo</h1><p>Pick one you love. We’ll score it and help you improve it, then your <b>first challenge is free</b>.</p>
    <div class="obu-ex">${ex.map(x => `<img src="${x.src}" alt="">`).join('')}</div>
    <ul class="obu-l"><li>📷 Any photo from your phone</li><li>✨ Free score in seconds</li><li>🏆 Today’s ${esc(crownName(k))} prize pool: <b>$${Math.round(L.jp[k] || 0).toLocaleString()}</b></li></ul>
    <label class="btn block ob-pick" id="obUp" for="file" role="button">📷 Upload photo · Free</label></div>`;
  const f = $('#file'), done = () => { f.removeEventListener('change', done); g.className = ''; setTimeout(() => g.remove(), 300); };
  f.addEventListener('change', done); }
function obDone(g) {""")
s=s.replace('</style>',""".pu-add{width:100%;aspect-ratio:1;border-radius:16px;border:2.5px dashed;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer;font:inherit;background:none}.pu-add span{font-size:2.4rem;line-height:1;font-weight:300}.pu-add small{font-size:.78rem;font-weight:700;padding:0 6px}
.pu-t{margin:12px 0;font-size:.92rem;line-height:1.4}
.obu-ex{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:14px 0}.obu-ex img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:14px}
.obu-l{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:8px;font-size:1rem}
html:not(.yg) .pu-add{border-color:#2D4E86;color:#2D4E86;background:#F3EBDD}html:not(.yg) .pu-t{color:#2B2320}
html.yg .pu-add{border-color:#C13CFF;color:#E9E2FF;background:#241544}html.yg .pu-t{color:#E9E2FF}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('four ok')
s=open(d+'yofi-simple.html').read(); a="cta: 'Let’s go', onCta: () => bt.classList.add('on')"; assert s.count(a)==1; s=s.replace(a,"cta: 'Let’s go · Free', onCta: () => bt.classList.add('on')"); open(d+'yofi-simple.html','w').write(s); print('lets go free ok')
# ---------- Quick Sprint: $10 and $20 tables ----------
s=open(d+'yofi-simple.html').read()
for a,b,n in [("const QS_STAKES = [2, 5],","const QS_STAKES = [2, 5, 10, 20],",1),("win up to $8","win up to $32",2),
 ("<b>$2</b> wins <b>$3.20</b>, <b>$5</b> wins <b>$8</b>.","<b>$2</b> wins <b>$3.20</b>, up to <b>$20</b> wins <b>$32</b>.",2)]:
    assert s.count(a)==n,(a,s.count(a)); s=s.replace(a,b)
s=s.replace('</style>','.qs2-pick .qs2-st{gap:7px}.qs2-pick .qs2-st button{padding:8px 14px}.qs2-pick .qs2-st b{font-size:1.6rem!important}\n</style>',1)
open(d+'yofi-simple.html','w').write(s); print('stakes 10 20 ok')

# ---------- Freeroll: one entry per photo per day, rank vs the top-20 cut-off, touch up to climb ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
i=s.index('function frEnter(f) {'); j=s.index('\n// reminder: when the final of an entered Freeroll starts', i)
s=s[:i]+r"""const FR_CUT = 85, frRank = sc => Math.max(1, Math.round(FR_FINAL * Math.pow(1.35, FR_CUT - sc)));
const frUsed = () => { const d = dayKey(); if (!S.frU || S.frU.d !== d) S.frU = { d, p: [] }; return S.frU.p; };
function frEnter(f) { const P = S.photos.slice().sort((a, b) => b.s.total - a.s.total), used = frUsed();
  if (!P.length) { closeSheet(); toast('Add a photo first, then enter the Freeroll.'); pickPhoto(true); return; }
  const open = P.filter(p => !used.includes(p.id));
  const tile = p => { const u = used.includes(p.id), r = frRank(p.s.total), inF = r <= FR_FINAL;
    return `<button data-frp="${p.id}" ${u ? 'disabled' : ''} aria-pressed="false" class="${u ? 'used' : inF ? 'in' : ''}"><img src="${p.src}" alt=""><b>${p.s.total}</b><small>${u ? 'Entered today' : `≈ #${r.toLocaleString()}`}</small></button>`; };
  openSheet(`<div class="ug frp frp2"><h2>Enter the ${frTime(f.start)} Freeroll</h2>
    <p class="sub">Pick a photo. The <b>top ${FR_FINAL}</b> by score go to the final, and members vote for the <b>$${FR_PRIZE.join(' · $')}</b> winners.</p>
    <div class="frp-cut">🏁 Top ${FR_FINAL} cut-off: about <b>${FR_CUT}+</b> · each photo can enter <b>once a day</b></div>
    <div class="frp-g">${P.slice(0, 9).map(tile).join('')}</div>
    <div id="frpInfo" class="frp-info"></div>
    ${open.length ? `<button class="btn block" id="frpGo">Enter · use 1 🎟️</button>` : ''}
    <button class="btn block frp-up" id="frpUp">📷 Upload a new photo</button>
    <div style="text-align:center"><button class="link" id="frpBack">Back</button></div></div>`, { full: false });
  let sel = open.length ? open[0].id : null;
  const paint = () => { document.querySelectorAll('#sheetBody [data-frp]').forEach(x => x.setAttribute('aria-pressed', x.dataset.frp === sel)); const p = S.photos.find(x => x.id === sel), I = $('#frpInfo');
    if (!p) { I.innerHTML = `<b>All your photos have entered today.</b> Upload a new one to play this Freeroll.`; return; }
    const r = frRank(p.s.total), gap = FR_CUT - p.s.total;
    I.innerHTML = r <= FR_FINAL ? `✅ <b>Top ${FR_FINAL} spot</b> · this ${p.s.total} photo is about <b>#${r}</b> by score` : `This ${p.s.total} photo is about <b>#${r.toLocaleString()}</b>. <b>${gap} more points</b> gets it into the top ${FR_FINAL}. <button class="link frp-tu" id="frpTu">✨ Touch up to climb · ${fixLab(p)}</button>`;
    if ($('#frpTu')) $('#frpTu').onclick = () => { closeSheet(); S.cur = p.id; save(); WALL = false; go('studio'); renderStudio(); toast(`Touch up to ${FR_CUT}+, then enter the Freeroll`); }; };
  document.querySelectorAll('#sheetBody [data-frp]').forEach(b => b.onclick = () => { if (b.disabled) return; sel = b.dataset.frp; paint(); }); paint();
  $('#frpBack').onclick = () => closeSheet();
  $('#frpUp').onclick = () => { closeSheet(); pickPhoto(true); };
  if ($('#frpGo')) $('#frpGo').onclick = () => { if (!(S.cashTix > 0)) { toast('You need a ticket'); return; } const p = S.photos.find(x => x.id === sel); if (!p) return; S.cashTix--; S.frE = S.frE || {}; frUsed().push(p.id);
    const r = frRank(p.s.total); S.frE[f.id] = { pid: p.id, score: p.s.total, start: f.start, fin: f.fin, end: f.end, bell: true, rank: Math.max(1, Math.round(r * (0.85 + Math.random() * 0.3))) }; save(); paintTix && paintTix(); closeSheet();
    celebrate({ src: p.src, score: p.s.total, title: 'You’re in!', text: `Your ${p.s.total} photo is entered in the <b>${frTime(f.start)} Freeroll</b>, about <b>#${r.toLocaleString()}</b> by score${r <= FR_FINAL ? ': on track for the final' : ` (top ${FR_FINAL} make the final)`}. The final starts at <b>${frTime(f.fin)}</b>. 🔔 We’ll tell you when it starts.`, cta: 'Keep voting', onCta: () => go('judge'), later: 'See tournaments', onLater: () => openComps() }); }; }"""+s[j:]
RA("const rank = e.rank || (e.rank = Math.max(1, Math.round((100 - e.score) * 22 + Math.random() * 30)));","const rank = e.rank || (e.rank = frRank(e.score));")
s=s.replace('</style>',""".frp2 .frp-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}.frp2 .frp-g button{position:relative;padding:0;border:0;border-radius:14px;overflow:hidden;cursor:pointer;background:none}
.frp2 .frp-g img{width:100%;aspect-ratio:1;object-fit:cover;display:block}.frp2 .frp-g b{position:absolute;left:6px;top:6px;padding:1px 8px;border-radius:999px;background:rgba(0,0,0,.65);color:#fff;font-size:.85rem}
.frp2 .frp-g small{display:block;padding:4px 2px;font-size:.74rem;font-weight:800;text-align:center}.frp2 .frp-g button[aria-pressed="true"]{box-shadow:0 0 0 3px #FBC20A}.frp2 .frp-g button.used{opacity:.45;cursor:default}
.frp-cut{border-radius:12px;padding:8px 10px;font-size:.84rem}.frp-info{font-size:.88rem;line-height:1.4;margin:0 0 10px;min-height:2.6em}.frp-tu{display:block;margin-top:4px;font-weight:800}.frp-up{margin-top:8px}
html:not(.yg) .frp2 .frp-g small{background:#F3EBDD;color:#5B4E45}html:not(.yg) .frp2 .frp-g button.in small{background:#DDF0E1;color:#1F4A2B}html:not(.yg) .frp-cut{background:#FFF6DC;color:#2B2320}html:not(.yg) .frp-info{color:#2B2320}
html:not(.yg) .frp-up{background:#fff!important;color:#2D4E86!important;box-shadow:inset 0 0 0 2px #2D4E86!important}
html.yg .frp2 .frp-g small{background:#241544;color:#C9B8FF}html.yg .frp2 .frp-g button.in small{background:#0E3A2A;color:#2EE59D}html.yg .frp-cut{background:#241544;color:#E9E2FF}html.yg .frp-info{color:#E9E2FF}
html.yg .frp-up{background:transparent!important;color:#fff!important;box-shadow:inset 0 0 0 2px #C13CFF!important}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('freeroll photo ok')
s=open(d+'yofi-simple.html').read(); s=s.replace('</style>','.frp2 .frp-g button{aspect-ratio:auto!important;height:auto!important;display:flex!important;flex-direction:column}.frp2 .frp-g button img{flex:none}.frp2 .frp-g button small{position:static!important;display:block!important}\n</style>',1); open(d+'yofi-simple.html','w').write(s); print('fr labels ok')
s=open(d+'yofi-simple.html').read(); s=s.replace('</style>','.frp2 .frp-g button small{position:absolute!important;left:0;right:0;bottom:0;padding:5px 2px!important;font-size:.76rem!important}\n</style>',1); open(d+'yofi-simple.html','w').write(s); print('fr labels 2 ok')

# ---------- Coins to Freeroll in one flow: coin pill / row → photo picker → Enter · 1,000 coins ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
# picker: pay with coins when there is no ticket
RA("${open.length ? `<button class=\"btn block\" id=\"frpGo\">Enter · use 1 🎟️</button>` : ''}",
   "${open.length ? (S.cashTix > 0 ? `<button class=\"btn block\" id=\"frpGo\">Enter · use 1 🎟️</button>` : swapReady() && S.gems >= TIX_COINS ? `<button class=\"btn block\" id=\"frpGo\">Enter · ${TIX_COINS.toLocaleString()} 🟡</button><p class=\"frp-bal\">You have ${Math.floor(S.gems).toLocaleString()} 🟡 · one coin entry an hour</p>` : `<button class=\"btn block\" id=\"frpGo\" disabled>Enter · ${TIX_COINS.toLocaleString()} 🟡</button><p class=\"frp-bal\">${!swapReady() ? `You’ve used this hour’s coin entry. Next one in ${frMinsLeft()} min.` : `You need ${(TIX_COINS - Math.floor(S.gems)).toLocaleString()} more 🟡. ${isYoungW() ? 'Judge' : 'Vote'} to earn them.`}</p>`) : ''}")
RA("if ($('#frpGo')) $('#frpGo').onclick = () => { if (!(S.cashTix > 0)) { toast('You need a ticket'); return; }",
   "if ($('#frpGo')) $('#frpGo').onclick = () => { if (!(S.cashTix > 0)) { if (!swapReady() || S.gems < TIX_COINS) return; S.gems -= TIX_COINS; S.swapHr = frHourKey(); S.cashTix = (S.cashTix || 0) + 1; window.__spent = true; S.gnMark = 99999; S.gnVote = (S.votes || 0) + 999; paintGems(); }")
# the next Freeroll you have not entered
RA("const frUsed = () =>","const frNext = () => frSlots().find(f => !(S.frE || {})[f.id]) || frSlots()[0];\nconst frUsed = () =>")
# swapping from the coin pill / tournaments pill goes straight to the photo picker
RA("function swapTicket() { if (!swapReady()) {","function swapTicket() { if ($('#sheet').classList.contains('on')) closeSheet(); setTimeout(() => frEnter(frNext()), 350); return; if (!swapReady()) {")
RA("<b>Freeroll ticket</b><small>${swapReady() ? 'Free entry to an hourly $20 Freeroll · 1 an hour' : `Next swap in ${frMinsLeft()} min`}</small>",
   "<b>Enter the ${frTime(frNext().start)} Freeroll</b><small>${swapReady() ? `Your photo · $${FR_PRIZE.reduce((a, b) => a + b, 0)} cash prizes · 1 an hour` : `Next coin entry in ${frMinsLeft()} min`}</small>")
# tournament rows: no ticket → picker (pays with coins)
RA("if (!(S.cashTix > 0)) { toast(`Swap ${TIX_COINS.toLocaleString()} coins for a Freeroll ticket first`); useGems(); return; } frEnter(f);","frEnter(f);")
RA("if ($('#tshTix')) $('#tshTix').onclick = () => { if (!(S.cashTix > 0)) swapTicket(); };","if ($('#tshTix')) $('#tshTix').onclick = () => frEnter(frNext());")
s=s.replace('</style>',".frp-bal{margin:6px 0 0;text-align:center;font-size:.8rem;opacity:.85}\n</style>",1)
open(d+'yofi-simple.html','w').write(s); print('fr flow ok')
s=open(d+'yofi-simple.html').read()
def RA(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a),n); s=s.replace(a,b)
RA("frrow ${e ? 'in' : nt ? 'can' : 'need'}","frrow ${e ? 'in' : nt || (swapReady() && S.gems >= TIX_COINS) ? 'can' : 'need'}")
RA("nt ? '🎟️ Enter' : '🔒 Ticket'}","nt ? '🎟️ Enter' : swapReady() && S.gems >= TIX_COINS ? `${TIX_COINS.toLocaleString()} 🟡` : `🔒 ${TIX_COINS.toLocaleString()} 🟡`}")
RA("""🎟️ ${nt} Freeroll ticket${nt === 1 ? '' : 's'} · ${nt ? '<b>Use below</b>' : (swapReady() ? `<b>Swap ${TIX_COINS.toLocaleString()} 🟡</b>` : `next swap in ${frMinsLeft()}m`)}</button>""",
   """${nt ? `🎟️ ${nt} Freeroll ticket${nt === 1 ? '' : 's'} · <b>Enter below</b>` : swapReady() ? `🎟️ Enter your photo · <b>${TIX_COINS.toLocaleString()} 🟡</b>` : `🎟️ Next coin entry in ${frMinsLeft()}m`}</button>""")
open(d+'yofi-simple.html','w').write(s); print('fr rows ok')
s=open(d+'yofi-simple.html').read()
for a,b in [("· one coin entry an hour</p>","· one ${isYoungW() ? 'gem' : 'coin'} entry an hour</p>"),("You’ve used this hour’s coin entry.","You’ve used this hour’s ${isYoungW() ? 'gem' : 'coin'} entry.")]:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(d+'yofi-simple.html','w').write(s); print('gem words ok')
