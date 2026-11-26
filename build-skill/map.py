# Skill preview: the collection map (like a village map).
# A full-screen, playful map of the 7 collections on a winding road: finished stops are gold
# with a tick, the current one bobs with a "You are here" pin, locked ones are grey. Each stop
# shows its 3 slots and its 🎟️ reward (a free $1 cash challenge). Stops pop in one by one and
# the road marches towards you. Shown the first time Gallery opens, from the collection badge
# (now "🗺 2/3 at Gold"), and after a collection is finished: the next stop unlocks on the map
# with confetti. One button: "Fill Travel · 2 to go".
# usage: python3 build-skill/map.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- collection map ----
const MAP_IC = { pets: '🐾', travel: '✈️', night: '🍃', selfie: '👨‍👩‍👧', fitness: '🌷', food: '🧁', style: '🏠' };
function mapState() { const P = GAL.PATH; let cur = P.findIndex(c => galOpen(c) && galRank((S.galBest || {})[c]) < 1); if (cur < 0) cur = P.length - 1;
  return P.map((c, i) => { const r = galRoom(c), gold = r.ph.filter(p => p.s.total >= 70).length, done = galRank((S.galBest || {})[c]) >= 1;
    return { c, i, nm: galNm(c), ic: MAP_IC[c] || '📷', done, open: galOpen(c), cur: i === cur, gold, n: r.ph.length, tix: !!(S.galTix || {})[c + '_Gold'] }; }); }
function showMap(o = {}) { const sh = $('#shell'); if (!sh) return; document.querySelectorAll('#gmap').forEach(e => e.remove());
  const M = mapState(), cur = M.find(m => m.cur) || M[0], W = 390, STEP = 150, top = 150, H = top + M.length * STEP + 40;
  const pos = M.map((m, i) => ({ x: i % 2 ? 278 : 112, y: top + i * STEP })), unlockI = o.unlock ? M.findIndex(m => m.c === o.unlock) : -1;
  const path = pos.map((p, i) => i ? `C ${pos[i - 1].x} ${pos[i - 1].y + STEP * .55}, ${p.x} ${p.y - STEP * .55}, ${p.x} ${p.y}` : `M ${p.x} ${p.y}`).join(' ');
  const curI = M.indexOf(cur), doneLen = curI;
  const node = (m, i) => { const p = pos[i], st = m.done ? 'done' : m.cur ? 'cur' : m.open ? 'open' : 'lock', neu = i === unlockI;
    return `<button class="gm-n ${st} ${neu ? 'neu' : ''}" data-mc="${m.c}" style="left:${p.x - 52}px;top:${p.y - 44}px;animation-delay:${(i * .09).toFixed(2)}s" aria-label="${esc(m.nm)}: ${m.done ? 'complete' : m.open ? m.gold + ' of 3 at Gold' : 'locked'}">
      ${m.cur ? '<span class="gm-pin">YOU ARE HERE</span>' : ''}
      <span class="gm-d"><span class="gm-ic">${m.ic}</span>${m.done ? '<i class="gm-ok">✓</i>' : ''}${!m.open ? '<i class="gm-lk">🔒</i>' : ''}<i class="gm-tx ${m.tix ? 'got' : ''}">${m.tix ? '✓' : '🎟️'}</i>${m.done ? '<i class="gm-tw t1">✦</i><i class="gm-tw t2">✦</i>' : ''}</span>
      <b>${esc(m.nm)}</b><span class="gm-sl">${[0, 1, 2].map(k => `<i class="${k < m.gold ? 'g' : k < m.n ? 'h' : ''}"></i>`).join('')}</span></button>`; };
  const left = Math.max(0, 3 - cur.gold), btn = cur.done ? 'See your collections' : `Fill ${cur.nm} · ${left} to go`;
  const el = document.createElement('div'); el.id = 'gmap'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Your collection map');
  el.innerHTML = `<div class="gm-in"><button class="gm-x" aria-label="Close">✕</button><h2>Your collection map</h2><p class="gm-sub">Get <b>3 photos to 🥇 Gold</b> to finish a collection and open the next</p>
    <div class="gm-scroll"><div class="gm-board" style="height:${H}px">
      <svg class="gm-road" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" aria-hidden="true"><path d="${path}" class="r0"/><path d="${path}" class="r1"/></svg>
      ${['☁️', '🌤', '☁️'].map((c, i) => `<span class="gm-cl" style="top:${160 + i * 330}px;animation-delay:${i * 2}s">${c}</span>`).join('')}
      ${M.map(node).join('')}
      <div class="gm-end" style="top:${top + M.length * STEP - 70}px">🏆 Every collection at Gold · you’re a Yofi legend</div>
    </div></div>
    <div class="gm-key"><span>🥇 3 photos at Gold<br>finishes it</span><span>🎟️ Free $1 cash<br>challenge each</span><span>🟡 Every photo<br>earns per vote</span></div>
    <button class="btn block gm-go">${btn}</button></div>`;
  sh.appendChild(el); requestAnimationFrame(() => el.classList.add('on'));
  // road: gold up to where you are
  const r1 = el.querySelector('.gm-road .r1'); try { const total = r1.getTotalLength(); const seg = el.querySelector('.gm-road .r0'); let at = 0; if (curI > 0) { const tmp = document.createElementNS('http://www.w3.org/2000/svg', 'path'); tmp.setAttribute('d', pos.slice(0, curI + 1).map((p, i) => i ? `C ${pos[i - 1].x} ${pos[i - 1].y + STEP * .55}, ${p.x} ${p.y - STEP * .55}, ${p.x} ${p.y}` : `M ${p.x} ${p.y}`).join(' ')); at = tmp.getTotalLength(); }
    r1.style.strokeDasharray = `${at} ${total}`; r1.style.strokeDashoffset = at; setTimeout(() => { r1.style.transition = 'stroke-dashoffset 1.2s ease-out .3s'; r1.style.strokeDashoffset = 0; }, 30); } catch (e) {}
  const sc = el.querySelector('.gm-scroll'); setTimeout(() => { sc.scrollTo({ top: Math.max(0, pos[curI].y - 250), behavior: 'smooth' }); }, 350);
  const close = () => { el.classList.remove('on'); setTimeout(() => el.remove(), 250); };
  el.querySelector('.gm-x').onclick = close;
  el.querySelector('.gm-go').onclick = () => { close(); S.galCat = cur.c; AL_OPEN = null; TU_GAL = true; save(); go('studio'); try { renderStudio(); } catch (e) {} };
  el.querySelectorAll('[data-mc]').forEach(b => b.onclick = () => { const m = M.find(x => x.c === b.dataset.mc);
    if (!m.open) { b.classList.remove('shake'); void b.offsetWidth; b.classList.add('shake'); toast(`🔒 Finish ${M[Math.max(0, m.i - 1)].nm} to open ${m.nm}`); return; }
    close(); S.galCat = m.c; AL_OPEN = null; TU_GAL = true; save(); go('studio'); try { renderStudio(); } catch (e) {} });
  if (o.unlock) { setTimeout(() => { const n = el.querySelector('.gm-n.neu'); if (n) n.classList.add('go'); const cf = document.createElement('div'); cf.className = 'gm-cf'; cf.innerHTML = [...Array(28)].map((_, i) => `<i style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#E0A82E', '#2D4E86', '#3CCB8A', '#7A1F27'][i % 5]};animation-delay:${(i * .05).toFixed(2)}s"></i>`).join(''); el.appendChild(cf); setTimeout(() => cf.remove(), 3200); }, 1300); }
  S.mapSeen = 1; save();
}
// first time Gallery opens with photos: show the map
const _goM = go;
go = function (t) { const r = _goM.apply(this, arguments); try { if (t === 'studio' && S.user && !S.mapSeen && S.photos.some(p => p.s && GAL.PATH.includes(p.cat))) setTimeout(() => showMap(), 350); } catch (e) {} return r; };
// the collection badge opens the map
const _renderGalleriesM = renderGalleries;
renderGalleries = function () { const r = _renderGalleriesM.apply(this, arguments);
  try { const b = document.querySelector('#studio .a2-th .a2-badge'); if (b && !b.dataset.map) { b.dataset.map = 1; b.insertAdjacentHTML('afterbegin', '<i class="gm-bi">🗺</i>'); b.setAttribute('role', 'button'); b.setAttribute('tabindex', '0'); b.setAttribute('aria-label', b.textContent.trim() + '. Open the collection map'); b.onclick = () => showMap(); } } catch (e) {}
  return r; };
// finishing a collection: "Open Travel" shows the next stop unlocking on the map
const _galCeleM = galCele;
galCele = function (ev) { const r = _galCeleM.apply(this, arguments);
  try { if (ev.opened) { const no = $('#glpNo'); if (no) { no.textContent = `See ${galNm(ev.opened)} on the map`; no.onclick = () => { const co = $('#coach'); co.classList.remove('on', 'cr'); co.innerHTML = ''; go('studio'); setTimeout(() => showMap({ unlock: ev.opened }), 300); }; } } } catch (e) {}
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* collection map */
#gmap{position:absolute;inset:0;z-index:60;background:rgba(40,28,16,.5);opacity:0;transition:opacity .25s}#gmap.on{opacity:1}
#gmap .gm-in{position:absolute;inset:0;display:flex;flex-direction:column;background:radial-gradient(circle at 25% 15%,#FFF8E6,#F5E8CC 55%,#EAD7B0);overflow:hidden}
#gmap .gm-in::before{content:"";position:absolute;inset:0;background:repeating-radial-gradient(circle at 80% 90%,rgba(122,31,39,.025) 0 2px,transparent 2px 14px);pointer-events:none}
#gmap h2{margin:22px 54px 2px;text-align:center;font:900 1.6rem Fraunces,serif;color:#7A1F27;position:relative}
#gmap .gm-sub{margin:0 26px 6px;text-align:center;font-size:.9rem;color:#4E433C;position:relative}
#gmap .gm-x{position:absolute;right:14px;top:14px;z-index:3;width:38px;height:38px;border:0;border-radius:50%;background:#FFFDF9;box-shadow:0 2px 8px rgba(0,0,0,.2);font:900 1rem "Nunito Sans";color:#2D2521;cursor:pointer}
#gmap .gm-scroll{flex:1;overflow-y:auto;overflow-x:hidden;position:relative;-webkit-overflow-scrolling:touch}
#gmap .gm-board{position:relative;width:390px;margin:0 auto}
#gmap .gm-road{position:absolute;left:0;top:0}
#gmap .gm-road path{fill:none;stroke-linecap:round}
#gmap .gm-road .r0{stroke:#D9C49B;stroke-width:12;stroke-dasharray:2 18;animation:gmMarch 1.2s linear infinite}
#gmap .gm-road .r1{stroke:#E0A82E;stroke-width:12}
@keyframes gmMarch{to{stroke-dashoffset:-20}}
#gmap .gm-cl{position:absolute;left:-40px;font-size:2.2rem;opacity:.55;animation:gmCloud 18s linear infinite;pointer-events:none}
@keyframes gmCloud{to{transform:translateX(470px)}}
#gmap .gm-n{position:absolute;width:104px;border:0;background:none;padding:0;text-align:center;cursor:pointer;animation:gmPop .5s cubic-bezier(.2,1.5,.4,1) both;font-family:inherit}
@keyframes gmPop{0%{transform:scale(.2);opacity:0}100%{transform:none;opacity:1}}
#gmap .gm-d{position:relative;display:flex;align-items:center;justify-content:center;width:88px;height:88px;margin:0 auto;border-radius:50%;background:#FFFDF9;box-shadow:0 8px 16px -8px rgba(60,40,20,.6),inset 0 0 0 4px #E2D5BE}
#gmap .gm-ic{font-size:2.3rem;line-height:1}
#gmap .gm-n b{display:block;margin-top:6px;font:900 1.05rem Fraunces,serif;color:#2D2521}
#gmap .gm-sl{display:flex;justify-content:center;gap:4px;margin-top:4px}#gmap .gm-sl i{width:13px;height:13px;border-radius:4px;background:#E2D5BE}#gmap .gm-sl i.h{background:#CDB98F}#gmap .gm-sl i.g{background:linear-gradient(180deg,#F3D27A,#E0A82E);box-shadow:0 0 6px rgba(224,168,46,.7)}
#gmap .gm-n.done .gm-d{background:linear-gradient(180deg,#FFF6DA,#F3D27A);box-shadow:0 8px 16px -8px rgba(160,110,10,.7),inset 0 0 0 4px #E0A82E}
#gmap .gm-ok{position:absolute;left:-4px;top:-4px;width:28px;height:28px;border-radius:50%;background:#2E9A5C;color:#fff;font:900 .95rem/28px "Nunito Sans";font-style:normal;box-shadow:0 2px 5px rgba(0,0,0,.3)}
#gmap .gm-tw{position:absolute;font-style:normal;color:#FFF;text-shadow:0 0 6px #E0A82E;animation:gmTw 1.8s ease-in-out infinite}#gmap .gm-tw.t1{right:4px;top:8px}#gmap .gm-tw.t2{left:8px;bottom:6px;animation-delay:.9s;font-size:.8rem}
@keyframes gmTw{0%,100%{opacity:0;transform:scale(.4)}50%{opacity:1;transform:scale(1.2)}}
#gmap .gm-n.cur .gm-d{box-shadow:0 0 0 7px rgba(45,78,134,.16),0 10px 20px -8px rgba(45,78,134,.7),inset 0 0 0 4px #2D4E86;animation:gmBob 1.8s ease-in-out infinite}
@keyframes gmBob{0%,100%{transform:translateY(0) scale(1.08)}50%{transform:translateY(-6px) scale(1.08)}}
#gmap .gm-pin{position:absolute;left:50%;top:-30px;transform:translateX(-50%);z-index:2;white-space:nowrap;font:900 .7rem "Nunito Sans";letter-spacing:.05em;padding:4px 10px;border-radius:99px;background:#2D4E86;color:#fff;box-shadow:0 3px 8px rgba(45,78,134,.5)}
#gmap .gm-pin::after{content:"";position:absolute;left:50%;bottom:-5px;margin-left:-5px;border:5px solid transparent;border-top-color:#2D4E86;border-bottom:0}
#gmap .gm-n.lock .gm-ic{filter:grayscale(1);opacity:.45}#gmap .gm-n.lock b{color:#8A7E72}
#gmap .gm-lk{position:absolute;right:-2px;bottom:-2px;font-style:normal;font-size:1.2rem;background:#FFFDF9;border-radius:50%;width:30px;height:30px;line-height:30px;box-shadow:0 2px 5px rgba(0,0,0,.2)}
#gmap .gm-tx{position:absolute;right:-10px;top:-6px;font-style:normal;font-size:1rem;padding:2px 6px;border-radius:99px;background:#DDF1E2;box-shadow:0 2px 6px rgba(0,0,0,.25);overflow:hidden}
#gmap .gm-tx::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 35%,rgba(255,255,255,.8) 50%,transparent 65%);transform:translateX(-120%);animation:jarShine 2.6s ease-in-out infinite}
#gmap .gm-tx.got{background:#2E9A5C;color:#fff;font:900 .8rem "Nunito Sans"}
#gmap .gm-n.shake{animation:gmShake .4s}
@keyframes gmShake{0%,100%{transform:none}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
#gmap .gm-n.neu .gm-d{filter:grayscale(1)}#gmap .gm-n.neu.go .gm-d{animation:gmUnlock 1s cubic-bezier(.2,1.4,.4,1) forwards}
@keyframes gmUnlock{0%{filter:grayscale(1);transform:scale(1)}40%{transform:scale(1.35)}100%{filter:none;transform:scale(1.08)}}
#gmap .gm-end{position:absolute;left:30px;right:30px;text-align:center;font:800 .82rem "Nunito Sans";color:#7A1F27;opacity:.8}
#gmap .gm-key{display:flex;justify-content:space-between;gap:6px;margin:6px 16px 8px;padding:9px 10px;border-radius:14px;background:rgba(255,253,249,.94);box-shadow:inset 0 0 0 1.5px #E2D5BE;font:800 .72rem/1.25 "Nunito Sans";color:#4E433C;position:relative}
#gmap .gm-go{margin:0 16px 18px;width:auto;position:relative}
#gmap .gm-cf{position:absolute;inset:0;pointer-events:none;overflow:hidden}#gmap .gm-cf i{position:absolute;top:-12px;width:9px;height:14px;border-radius:2px;animation:gmCf 2.6s ease-in forwards}
@keyframes gmCf{to{transform:translateY(900px) rotate(540deg)}}
.a2-badge[data-map]{cursor:pointer}.gm-bi{font-style:normal;margin-right:5px}
@media (prefers-reduced-motion:reduce){#gmap *{animation:none!important;transition:none!important}}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('map ok')
