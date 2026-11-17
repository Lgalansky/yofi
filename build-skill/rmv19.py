# Real Money build, step 22 (after rmv18.py): landing page redesign from the user's mock-up.
# Headline + podium of 3 photos, "Judge photos. Get a free pick." (Earn a free pick), "Your photo could win the Final." (Enter your photo),
# "Meet the contenders" cards (live Final + next Finals, prize pools, times), "Watch the hourly Final" link.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

TICKET = '<svg viewBox="0 0 48 32" width="46" height="31" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" aria-hidden="true"><path d="M5 9 L37 3 L40 11 a4.5 4.5 0 0 0 2 8.6 L44 27 L12 31 L9 23 a4.5 4.5 0 0 0-2-8.6z"/><path d="M22 8 l1.6 6 M24.6 17.5 l1.6 6" stroke-dasharray="2.5 3"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M10 8.5v7l6-3.5z" fill="currentColor"/></svg>'
RA('<h1>Pick the winners. Win real cash.</h1><p class="ca-sub">Vote on photos, predict the crowd’s top 3 and play the hourly Final.</p><button class="btn block ca-any ca-vote" onclick="rmStartVote()">🗳️ Start voting · free</button><button class="btn block ca-b2" onclick="rmEnterOwn()">📷 Enter with your own photo and win the prize</button><button class="btn block ca-b2" onclick="rmWatch()">🔴 Watch the hourly Final live</button><div id="caFin" class="ca-fin"></div>',
   '<div class="lp"><h1 class="lp-h">Pick the winning photos.<em>Win real cash.</em></h1><p class="lp-sub">Pick your favourite. Cheer it on in the hourly Final.</p>'
   '<div class="lp-pod" id="lpPod"></div><p class="lp-cap">Which photo will take first place?</p>'
   '<div class="lp-sec"><div class="lp-row"><span class="lp-tk">' + TICKET + '</span><div><h2>Judge photos. Get a free pick.</h2><p>Vote to earn a free pick in the Final and win real cash.</p></div></div>'
   '<button class="lp-btn" onclick="rmStartVote()">Earn a free pick <span aria-hidden="true">→</span></button></div>'
   '<div class="lp-sec lp-c"><h2>Your photo could win the Final.</h2><p>Enter your photo and compete for the cash prize.</p><button class="lp-btn lp-out" onclick="rmEnterOwn()">Enter your photo</button></div>'
   '<div class="lp-ct"><div class="lp-cth"><h2>Meet the contenders</h2><button class="lp-lnk" onclick="rmWatch()">View all →</button></div><p>Choose your favourite. Pick your winner.</p><div class="lp-cg" id="lpCont"></div></div>'
   '<button class="lp-watch" onclick="rmWatch()">' + PLAY + '<span>Watch the hourly Final</span> →</button></div>')

s = s.replace("function fcNotify() {", r"""function lpImg(k) { const c = k === 'pets' ? 'pets' : k === 'garden' ? 'fitness' : 'night', t = document.querySelector(`#landing .ca-grid .ca-t[onclick*="'${c}'"] img`); return t ? t.src : ''; }
function lpWhen(sl) { const t = new Date((sl + 1) * PP_MS), n = new Date(), tm = new Date(n.getFullYear(), n.getMonth(), n.getDate() + 1); return `${t.toDateString() === n.toDateString() ? 'Today' : t.toDateString() === tm.toDateString() ? 'Tomorrow' : t.toLocaleDateString([], { weekday: 'short' })} · ${raceName(sl)}`; }
function lpContHTML() { const cur = ppSlot(), L = [{ sl: cur, live: 1 }].concat(finNext(3).map(x => ({ sl: x.sl })));
  return L.map(x => { const g = ppGame(x.sl), k = g.k;
    return `<div class="lp-cc">${lpImg(k) ? `<img src="${lpImg(k)}" alt="">` : ''}${x.live ? '<i class="lp-live">● Live now</i>' : ''}<b class="lp-cn">${esc(showName(k).split(' & ')[0])}</b><b class="lp-pz">${ppPool(g.players)}</b><small>Final prize pool</small><small>${x.live ? `Ends ${raceName(x.sl)}` : lpWhen(x.sl)}</small>
      ${x.live ? '<button class="lp-lnk" onclick="rmPickNow()">Pick a winner →</button>' : `<button class="lp-lnk" data-caf="${showHint(k).cats[0]}">Enter a photo →</button>`}</div>`; }).join(''); }
function rmPickNow() { rmWatch(); setTimeout(() => { try { popClose(); } catch (e) {} ppOpen(); }, 300); }
window.rmPickNow = rmPickNow;
setInterval(() => { try { if (!S || $('#landing').style.display === 'none') return; const p = document.getElementById('lpPod');
  if (p && !p.dataset.ok && lpImg('pets')) { p.dataset.ok = 1; p.innerHTML = [['pets', '1st', 'g'], ['nature', '2nd', 's'], ['garden', '3rd', 'b']].map(([k, t, c]) => `<div><img src="${lpImg(k)}" alt=""><span class="lp-ros ${c}">${t}</span></div>`).join(''); }
  const c = document.getElementById('lpCont'); if (c) { const h = lpContHTML(); if (c.dataset.h !== h) { c.dataset.h = h; c.innerHTML = h; } } } catch (e) {} }, 1000);
function fcNotify() {""", 1)

s = s.replace('</style>', """.lp{text-align:center;color:#2B2320}.lp-h{font:800 2.15rem/1.08 Fraunces,Georgia,serif;margin:8px 0 8px;color:#2B2320}.lp-h em{display:block;font-style:normal;color:#2F6B3F;font-size:2.5rem}.lp-sub{margin:0 0 14px;font-size:1rem}
.lp-pod{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;min-height:90px}.lp-pod div{position:relative}.lp-pod img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:16px;display:block}
.lp-ros{position:absolute;left:8px;bottom:8px;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:800 .82rem Fraunces,Georgia,serif;color:#3B2A12;box-shadow:0 2px 6px rgba(0,0,0,.3),inset 0 0 0 3px rgba(255,255,255,.55)}.lp-ros.g{background:radial-gradient(circle at 35% 30%,#FFF1A6,#E8B923 60%,#B8860B)}.lp-ros.s{background:radial-gradient(circle at 35% 30%,#FFFFFF,#C9CDD3 60%,#8E949C)}.lp-ros.b{background:radial-gradient(circle at 35% 30%,#F7C9A0,#C8794A 60%,#8C4A22);color:#fff}
.lp-cap{font-style:italic;margin:8px 0 18px;font-size:.95rem}.lp-sec{margin:0 0 20px}.lp-row{display:flex;gap:12px;align-items:center;text-align:left;margin-bottom:12px}.lp-row h2{font-size:1.3rem!important}.lp-tk{color:#9A2F4E;flex:0 0 auto}.lp h2{font:800 1.4rem/1.15 Fraunces,Georgia,serif;margin:0 0 4px;color:#2B2320}.lp-sec p,.lp-ct>p{margin:0;font-size:.92rem}
.lp-c p{margin:0 0 12px}.lp-btn{display:block;width:100%;border:0;border-radius:999px;padding:13px 16px;font:800 1.15rem Fraunces,Georgia,serif;background:#9A2F4E;color:#fff;cursor:pointer}.lp-btn.lp-out{background:transparent;color:#9A2F4E;box-shadow:inset 0 0 0 2px #9A2F4E}
.lp-ct{border-top:1px solid #E2D3BC;padding-top:16px;text-align:left}.lp-cth{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.lp-ct h2{font-size:1.45rem}.lp-lnk{border:0;background:none;padding:0;color:#9A2F4E;font:800 .95rem inherit;font-family:inherit;cursor:pointer}
.lp-cg{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:12px 0 8px}.lp-cc{flex:0 0 46%;scroll-snap-align:start;position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:1px}.lp-cc img{width:100%;aspect-ratio:1.4;object-fit:cover;border-radius:14px;margin-bottom:6px}
.lp-live{position:absolute;left:8px;top:8px;font-style:normal;font-size:.72rem;font-weight:800;background:#C8102E;color:#fff;padding:2px 8px;border-radius:999px}.lp-cn{font:800 1.15rem Fraunces,Georgia,serif}.lp-pz{font:800 2rem/1.05 Fraunces,Georgia,serif;color:#2F6B3F}.lp-cc small{font-size:.86rem}.lp-cc .lp-lnk{margin-top:4px}
.lp-watch{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;border:0;border-top:1px solid #E2D3BC;background:none;padding:16px 0 6px;margin-top:8px;color:#9A2F4E;font:800 1.05rem inherit;font-family:inherit;cursor:pointer}
#landing .ca-hero>h1,#landing .ca-hero>.ca-sub{display:none!important}
html #landing .lp button.lp-btn{display:block!important;width:100%!important;border:0!important;border-radius:999px!important;padding:13px 16px!important;font:800 1.15rem Fraunces,Georgia,serif!important;background:#9A2F4E!important;color:#fff!important;box-shadow:none!important}
html #landing .lp button.lp-btn.lp-out{background:transparent!important;color:#9A2F4E!important;box-shadow:inset 0 0 0 2px #9A2F4E!important}
html #landing .lp button.lp-lnk{color:#9A2F4E!important;font-weight:800!important;background:none!important;padding:0!important}html #landing .lp button.lp-watch{color:#9A2F4E!important;font-weight:800!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v19 ok')
