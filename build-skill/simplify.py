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
