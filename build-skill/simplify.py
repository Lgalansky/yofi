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

# ---------- Sign-up offer: $2 bonus cash (entries only, used first; winnings are real cash) ----------
s=open(d+'yofi-simple.html').read()
def RA(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
RA('<b id="cashNum">$0.00</b></span></button>','<b id="cashNum">$0.00</b></span><em id="bonNum" class="bon"></em></button>')
RA("function paintWallet() { $('#cashNum').textContent = '$' + (S.cash || 0).toFixed(2);",
   "function paintWallet() { $('#cashNum').textContent = '$' + (S.cash || 0).toFixed(2); { const bt = $('#bonNum'); if (bt) { bt.textContent = S.bonus > 0 ? '+$' + (+S.bonus).toFixed(2).replace('.00', '') + ' bonus' : ''; bt.style.display = S.bonus > 0 ? '' : 'none'; } }")
RA("if ((S.cash || 0) < stake) { c.classList.remove('on', 'cr');","if ((S.cash || 0) + (S.bonus || 0) < stake) { c.classList.remove('on', 'cr');")
RA("S.cash = +((S.cash || 0) - stake).toFixed(2); save(); paintWallet();",
   "{ const fb = Math.min(S.bonus || 0, stake); S.bonus = +((S.bonus || 0) - fb).toFixed(2); S.cash = +((S.cash || 0) - (stake - fb)).toFixed(2); } save(); paintWallet();")
RA("<small>You and 1 real player get the same 10 pairs · most right wins · ties go to the fastest.</small>",
   "${S.bonus > 0 ? `<p class=\"qs-bon\">🎁 Your $${(+S.bonus).toFixed(2).replace('.00', '')} bonus cash is used first</p>` : ''}<small>You and 1 real player get the same 10 pairs · most right wins · ties go to the fastest.</small>")
RA("${pr ? '🎯 Play for real' :","${pr ? (S.bonus >= 2 ? '🎯 Play for real · on us' : '🎯 Play for real') :")
RA("<p class=\"qs-prac\">${prize ?","${pr && S.bonus >= 2 ? `<p class=\"qs-bon\">🎁 You have <b>$${(+S.bonus).toFixed(2).replace('.00', '')} bonus cash</b>. Your first cash game is on us.</p>` : ''}<p class=\"qs-prac\">${prize ?")
RA("${S.qsTried ? 'from $2' :","${S.qsTried ? (S.bonus >= 2 ? '$2 free' : 'from $2') :")
s=s.replace("function fcNotify() {",r"""setInterval(() => { if (S.obDone && !S.bonusGiven) { S.bonusGiven = 1; S.bonus = (S.bonus || 0) + 2; save(); paintWallet(); setTimeout(() => toast('🎁 Welcome! $2 bonus cash to play your first 1 v 1'), 1500); } }, 2000);
function fcNotify() {""",1)
s=s.replace('</style>',""".bon{display:block;font-style:normal;font-size:.62rem;font-weight:900;line-height:1;margin-left:4px;padding:3px 6px;border-radius:999px;white-space:nowrap}
html:not(.yg) .bon{background:#2F6B3F;color:#fff}html.yg .bon{background:#2EE59D;color:#06261A}
.qs-bon{margin:0 0 8px!important;padding:8px 10px;border-radius:10px;font-size:.82rem;font-weight:700}
html:not(.yg) .qs-bon{background:#EAF3EC;color:#1F4A2B}html.yg .qs-bon{background:#0E3A2A;color:#C9FBE5}
</style>""",1)
open(d+'yofi-simple.html','w').write(s); print('bonus ok')
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
