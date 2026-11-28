# Skill preview: make voting exciting (our own look, not a copy of any game).
#  1. Right vote: coins burst out of the photos towards you (zoom + fade) with a gold shock ring,
#     on top of the usual "+5" and fly-to-balance.
#  2. Special photo: now and then a right vote drops a face-down special photo onto the vote. Tap to
#     reveal: a 🃏 Joker (+20 / +50 / +100 coins) or a 🛡 Shield (blocks one steal while you're away,
#     hold up to 3). Then one "Collect" button.
#     New players get their first reveal within their first few right votes.
#  3. Shields: a 🛡 pill in the header shows how many you hold. An overnight steal that hits a
#     shield is blocked; the "While you were away" pop says so.
#  4. Raid: every 10–15 votes the special photo flips to a 🦝 Steal! card; "Start the raid" switches
#     the whole screen to a raid. A random rival's wall of 3
#     photos; tap one to try to steal it; your best photo vs theirs, best of 3 live votes;
#     win and it joins your cards (it earns coins for you); lose and nothing is lost.
#     One button back to voting. Raids are free and don't use your 3 daily steal tries.
# usage: python3 build-skill/votefx.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- exciting voting: coin burst, lucky reveals, shields, raids ----
const VF_MAXSH = 3;
let VF_N = S.eyeN || 0, VF_OK = S.eyeOk || 0, VF_G = S.gems || 0, VF_BUSY = 0;
if (S.vfRaidAt == null || S.vfRaidAt < (S.eyeN || 0)) S.vfRaidAt = (S.eyeN || 0) + 10 + Math.floor(Math.random() * 6);
const vfOverlayOpen = () => VF_BUSY || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || !!$('#raid');
// 1. coins burst towards you
function vfBurst(n) { const card = $('#jcard'), sh = $('#shell'); if (!card || !sh || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const sr = sh.getBoundingClientRect(), r = card.getBoundingClientRect(), x = r.left - sr.left + r.width / 2, y = r.top - sr.top + r.height / 2;
  const L = document.createElement('div'); L.className = 'vf-layer'; sh.appendChild(L);
  for (let i = 0; i < 12; i++) { const c = document.createElement('i'); c.className = 'vf-c'; c.innerHTML = gemIcon(''); c.style.left = x + 'px'; c.style.top = y + 'px'; L.appendChild(c);
    const a = i / 12 * Math.PI * 2 + Math.random() * .4, d = 90 + Math.random() * 110, sc = 1.6 + Math.random() * 1.4;
    c.animate([{ transform: 'translate(-50%,-50%) scale(.2) rotate(0deg)', opacity: 0 }, { transform: `translate(calc(-50% + ${Math.cos(a) * d * .5}px),calc(-50% + ${Math.sin(a) * d * .5}px)) scale(${sc * .6}) rotate(${a * 90}deg)`, opacity: 1, offset: .35 },
      { transform: `translate(calc(-50% + ${Math.cos(a) * d}px),calc(-50% + ${Math.sin(a) * d}px)) scale(${sc}) rotate(${a * 180}deg)`, opacity: 0 }], { duration: 750 + i * 25, easing: 'cubic-bezier(.2,.7,.3,1)', fill: 'forwards' }); }
  const ring = document.createElement('i'); ring.className = 'vf-ring'; ring.style.left = x + 'px'; ring.style.top = y + 'px'; L.appendChild(ring);
  setTimeout(() => L.remove(), 1300); }
// 3. shields
function vfShPaint() { const f = $('#sFlame'); if (!f) return; let b = $('#vfSh'); const n = S.shields || 0;
  if (!b) { b = document.createElement('button'); b.id = 'vfSh'; b.className = 'vf-sh'; b.setAttribute('aria-label', 'Shields'); f.after(b); b.onclick = () => toast(`🛡 ${S.shields || 0} of ${VF_MAXSH} shields · each one blocks a steal while you’re away`); }
  b.hidden = !n; const h = `🛡<b>${n}</b>`; if (b.innerHTML !== h) b.innerHTML = h; }
// 2. lucky reveals
function vfReveal(kind) { const sh = $('#shell'), card = $('#jcard'); if (!sh || !card) return; VF_BUSY = 1;
  const amt = kind === 'coins' ? (r => r < .6 ? 20 : r < .9 ? 50 : 100)(Math.random()) : 0, sr = sh.getBoundingClientRect(), cr = card.getBoundingClientRect();
  const el = document.createElement('div'); el.id = 'vfRev'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Special photo');
  el.innerHTML = `<div class="vf-spot" style="left:${cr.left - sr.left}px;top:${cr.top - sr.top}px;width:${cr.width}px;height:${cr.height}px">
    <button class="vf-flip" aria-label="Tap to reveal"><span class="vf-face back"><i class="vf-sp">✨ SPECIAL PHOTO ✨</i><span class="vf-q">?</span><b class="vf-tap">Tap to reveal</b></span>
      <span class="vf-face front ${kind}"><span class="vf-ic">${kind === 'coins' ? '🃏' : kind === 'steal' ? '🦝' : '🛡'}</span><h3>${kind === 'coins' ? 'Joker!' : kind === 'steal' ? 'Steal!' : 'Shield!'}</h3>
        <p>${kind === 'coins' ? `<b>+${amt}</b> ${gemIcon('vf-gi')}` : kind === 'steal' ? 'Raid a rival and take a photo' : 'Blocks one steal while you’re away'}</p></span></button></div>
    <button class="vf-go ${kind === 'steal' ? 'nav' : ''}" disabled>${kind === 'coins' ? `Collect ${amt}` : kind === 'steal' ? 'Start the raid' : 'Keep my shield'}</button>`;
  sh.appendChild(el); requestAnimationFrame(() => el.classList.add('on'));
  el.querySelector('.vf-flip').onclick = () => { if (el.classList.contains('flip')) return; el.classList.add('flip'); setTimeout(() => { const g = el.querySelector('.vf-go'); g.disabled = false; g.classList.add('in'); }, 650); };
  el.querySelector('.vf-go').onclick = () => { const fr = el.querySelector('.vf-face.front');
    if (kind === 'coins') { S.gems += amt; save(); try { gemExplosion(amt, { mid: 1, from: fr }); } catch (e) { paintGems(); } }
    else if (kind === 'steal') { el.classList.remove('on'); setTimeout(() => { el.remove(); VF_BUSY = 0; raidStart(); }, 250); return; }
    else { S.shields = Math.min(VF_MAXSH, (S.shields || 0) + 1); save(); vfShPaint(); const b = $('#vfSh'); if (b) { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); } }
    VF_G = S.gems; el.classList.remove('on'); setTimeout(() => { el.remove(); VF_BUSY = 0; }, 300); }; }
// 4. raids
const RD_POOL = () => { const mine = new Set(S.photos.flatMap(p => [p.src, p.orig])), taken = S.stlTaken || [], out = [];
  GAL.PATH.forEach(c => SEED.filter(x => x.cat === BATTLE_POOL[c] && !mine.has(x.src) && !taken.includes(x.id)).forEach(x => out.push({ key: x.id, src: x.src, nm: x.title || 'Photo', cat: c, sc: 68 + hsh(x.id) % 22 }))); return out; };
function raidStart() { const me = S.photos.filter(p => p.s && !p.heldBy).sort((a, b) => b.s.total - a.s.total)[0], pool = RD_POOL(); if (!me || pool.length < 3) return;
  const rv = RIVALS[Math.floor(Math.random() * RIVALS.length)], wall = pool.sort(() => Math.random() - .5).slice(0, 3).map(x => ({ ...x, h: rv.h }));
  const sh = $('#shell'), el = document.createElement('div'); el.id = 'raid'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Raid');
  el.innerHTML = `<div class="rd-in"><div class="rd-ban">🃏 RAID!</div><p class="rd-who"><span class="rd-av">${rv.n[0]}</span>Steal a photo from <b>${rv.n}</b></p>
    <div class="rd-wall">${wall.map((w, i) => `<button class="rd-card" data-rd="${i}" style="animation-delay:${(.5 + i * .15).toFixed(2)}s"><img src="${w.src}" alt=""><i class="rd-sc">${w.sc}</i><span class="rd-tg"></span><b>${esc(w.nm)}</b><small>earns ${cardRate(w.sc)} 🟡 a vote</small></button>`).join('')}</div>
    <p class="rd-hint">Tap a photo to steal it · best of 3 votes · nothing to lose</p></div>`;
  sh.appendChild(el); requestAnimationFrame(() => el.classList.add('on'));
  el.querySelectorAll('[data-rd]').forEach(b => b.onclick = () => raidFight(el, me, wall[+b.dataset.rd], rv)); }
function raidFight(el, me, them, rv) { const pWin = Math.max(.35, Math.min(.75, .55 + (me.s.total - them.sc) / 40)), won = Math.random() < pWin;
  const pick = l => l[Math.floor(Math.random() * l.length)], seq = won ? pick([[1, 1], [0, 1, 1], [1, 0, 1]]) : pick([[0, 0], [1, 0, 0], [0, 1, 0]]);
  el.querySelector('.rd-in').innerHTML = `<div class="rd-ban sm">🃏 RAID</div><p class="rd-who">Best of 3 votes · <b>voters are deciding…</b></p>
    <div class="rd-vs"><figure><span class="rd-ph"><img src="${them.src}" alt=""><i class="rd-sc">${them.sc}</i></span><figcaption>${esc(them.nm)}<small>${rv.n}</small></figcaption></figure><span class="rd-x">VS</span>
      <figure class="me"><span class="rd-ph"><img src="${me.src}" alt=""><i class="rd-sc">${me.s.total}</i></span><figcaption>${esc(alName(me))}<small>You</small></figcaption></figure></div>
    <div class="rd-dots">${[0, 1, 2].map(i => `<i data-dt="${i}"><b>?</b></i>`).join('')}</div><p class="rd-tally"><b id="rdM">0</b> – <b id="rdT">0</b></p>`;
  let i = 0, m = 0, t = 0; const iv = setInterval(() => { if (!el.isConnected) { clearInterval(iv); return; } const v = seq[i], d = el.querySelector(`[data-dt="${i}"]`);
    if (v) m++; else t++; d.className = v ? 'w' : 'l'; d.innerHTML = `<b>${v ? '✓' : '✗'}</b>`; $('#rdM').textContent = m; $('#rdT').textContent = t; i++;
    if (i >= seq.length) { clearInterval(iv); setTimeout(() => raidDone(el, me, them, rv, won, m, t), 900); } }, 1100); }
function raidDone(el, me, them, rv, won, m, t) {
  if (won) { S.photos.push({ id: uid(), src: them.src, orig: them.src, cat: them.cat, nm: them.nm, nmAsk: 1, enh: 0, at: Date.now(), card: { from: rv.h }, s: { light: them.sc, comp: them.sc, colour: them.sc, tech: them.sc, total: them.sc } }); S.stlTaken = (S.stlTaken || []).concat(them.key); save(); }
  el.querySelector('.rd-in').innerHTML = `${won ? '<div class="wr-cf rd-cf" aria-hidden="true">' + [...Array(18)].map((_, i) => `<i style="left:${(i * 37) % 95}%;animation-delay:${(i * .09).toFixed(2)}s"></i>`).join('') + '</div>' : ''}
    <div class="rd-ban ${won ? '' : 'sm'}">${won ? '🏆 STOLEN!' : `${rv.n} kept it`}</div>
    <div class="rd-prize ${won ? 'w' : ''}"><img src="${them.src}" alt="">${won ? '<i class="rd-new">NEW CARD</i>' : ''}</div>
    <h3 class="rd-h">${won ? `${esc(them.nm)} is yours!` : 'Nothing lost'}</h3>
    <p class="rd-who">${won ? `It earns you <b>${cardRate(them.sc)} 🟡 a vote</b> from now on · won ${m}–${t}` : `${t}–${m} · another raid comes along in a few votes`}</p>
    <button class="rd-go">Back to voting</button>`;
  el.querySelector('.rd-go').onclick = () => { el.classList.remove('on'); setTimeout(() => el.remove(), 300); try { renderJudge(); } catch (e) {} }; }
// watch each vote
setInterval(() => { try { const n = S.eyeN || 0; if (n <= VF_N) { VF_G = S.gems; vfShPaint(); return; } const ok = (S.eyeOk || 0) > VF_OK, gained = Math.max(0, (S.gems || 0) - VF_G); VF_N = n; VF_OK = S.eyeOk || 0; VF_G = S.gems || 0;
  if (ok) { vfBurst(gained || CFG.VOTE); S.vfR = (S.vfR || 0) + 1;
    const first = !S.vfFirst && S.vfR >= 4, roll = Math.random(), kind = first ? 'coins' : roll < .08 ? 'coins' : roll < .12 && (S.shields || 0) < VF_MAXSH ? 'shield' : null;
    if (kind && n < S.vfRaidAt) { if (first) S.vfFirst = 1; save(); setTimeout(() => { if (!vfOverlayOpen()) vfReveal(kind); }, 900); } }
  if (n >= S.vfRaidAt) { S.vfRaidAt = n + 10 + Math.floor(Math.random() * 6); save(); setTimeout(() => { if (!vfOverlayOpen() && $('#panes').dataset.at === 'judge' && RD_POOL().length >= 3) vfReveal('steal'); }, 1100); }
} catch (e) {} }, 200);
// a shield blocks an overnight steal
const _stealAwayVF = stealAway;
stealAway = function (force) { if (S.user && (S.shields || 0) > 0) { const now = Date.now(), last = S.lastSeen || now, away = now - last;
    if ((force || away >= 2 * 36e5) && !S.photos.some(p => p.heldBy) && riskable().length) { const p = riskable()[0], r = RIVALS[hsh(p.id + now) % RIVALS.length];
      S.shields--; S.lastSeen = now; S.awayNews = { coins: Math.floor(S.vgJar || 0), st: null, blocked: { h: r.h, nm: alName(p) }, at: now }; save(); return; } }
  return _stealAwayVF.apply(this, arguments); };
const _awayPopVF = awayPop;
awayPop = function () { const N = S.awayNews, b = N && !N.shown && N.blocked; const r = _awayPopVF.apply(this, arguments);
  if (b && N.shown) { const p = document.querySelector('#coach.on p'); if (p) p.insertAdjacentHTML('beforeend', `${p.textContent.trim() ? '<br><br>' : ''}<b>🛡 Your shield stopped ${esc(rvName(b.h))} stealing ${esc(b.nm)}</b>`); }
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* exciting voting */
.vf-layer{position:absolute;inset:0;pointer-events:none;z-index:70;overflow:hidden}
.vf-c{position:absolute;width:34px;height:34px;filter:drop-shadow(0 4px 6px rgba(120,80,0,.35))}.vf-c svg{width:100%;height:100%}
.vf-plus{position:absolute;transform:translate(-50%,-50%);font:900 3.4rem/1 Fraunces,serif;color:#F3D27A;-webkit-text-stroke:2px #8A5A0A;text-shadow:0 6px 0 #8A5A0A,0 10px 18px rgba(0,0,0,.35);animation:vfPlus 1s cubic-bezier(.2,1.4,.4,1) forwards}
@keyframes vfPlus{0%{transform:translate(-50%,-50%) scale(.3);opacity:0}30%{transform:translate(-50%,-60%) scale(1.25);opacity:1}70%{transform:translate(-50%,-75%) scale(1);opacity:1}100%{transform:translate(-50%,-110%) scale(.9);opacity:0}}
.vf-ring{position:absolute;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;border:5px solid #F3D27A;animation:vfRing .7s ease-out forwards}@keyframes vfRing{to{transform:scale(7);opacity:0;border-width:1px}}
.vf-sh{display:inline-flex;align-items:center;gap:3px;margin-left:6px;padding:4px 10px;border:0;border-radius:99px;background:linear-gradient(180deg,#fff,#D7DCE3);box-shadow:inset 0 0 0 1.5px #B9C2CE;font:900 .9rem "Nunito Sans";color:#2E3440;cursor:pointer}.vf-sh[hidden]{display:none}
.vf-sh.bump{animation:jpPop .5s ease-out}
#vfRev{position:absolute;inset:0;z-index:65;background:rgba(20,33,61,.55);opacity:0;transition:opacity .25s}#vfRev.on{opacity:1}
.vf-spot{position:absolute;display:flex;align-items:center;justify-content:center;perspective:1000px}
.vf-flip{position:relative;width:min(240px,70%);height:100%;padding:0;border:0;background:none;cursor:pointer;transform-style:preserve-3d;transition:transform .7s cubic-bezier(.3,1.3,.5,1);animation:vfIn .5s cubic-bezier(.2,1.4,.4,1)}#vfRev.flip .vf-flip{transform:rotateY(180deg)}
@keyframes vfIn{from{transform:scale(.3) rotate(-8deg)}to{transform:none}}
.vf-face{position:absolute;inset:0;border-radius:24px;backface-visibility:hidden;-webkit-backface-visibility:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;text-align:center;box-shadow:0 20px 40px -12px rgba(0,0,0,.6)}
.vf-face.back{background:linear-gradient(160deg,#2B4372,#14213D);box-shadow:inset 0 0 0 5px #E0A82E,0 20px 40px -12px rgba(0,0,0,.6)}.vf-face.back span{font:900 5rem Fraunces,serif;color:#F3D27A}.vf-face.back small{font:800 .8rem "Nunito Sans";letter-spacing:.1em;text-transform:uppercase;color:#E6EDF8}
.vf-face.front{transform:rotateY(180deg);background:linear-gradient(180deg,#FFF6DD,#F3D27A);box-shadow:inset 0 0 0 5px #E0A82E,0 0 50px rgba(243,210,122,.7)}.vf-face.front.steal{background:linear-gradient(180deg,#2B4372,#14213D)!important;box-shadow:inset 0 0 0 5px #E0A82E,0 0 50px rgba(243,210,122,.7)!important}.vf-face.steal h3{color:#F3D27A!important}.vf-face.steal p{color:#E6EDF8!important}
.vf-face.front.shield{background:linear-gradient(180deg,#fff,#D7DCE3);box-shadow:inset 0 0 0 5px #9AA6B5,0 0 50px rgba(215,220,227,.7)}
.vf-ic{font-size:4.6rem;line-height:1}.vf-face h3{margin:0;font:900 1.7rem Fraunces,serif;color:#3A2600}.vf-face.shield h3{color:#1F3157}.vf-face p{margin:0 14px;display:flex;align-items:center;justify-content:center;gap:6px;font:800 1rem "Nunito Sans";color:#4E433C}.vf-face p b{font:900 2rem Fraunces,serif;color:#2D4E86}.vf-gi{width:28px;height:28px}
.vf-go{min-width:220px;padding:14px 24px;border:0;border-radius:999px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 1.05rem "Nunito Sans";box-shadow:0 8px 18px -8px rgba(160,110,10,.8);cursor:pointer;transition:opacity .2s}.vf-go:disabled{opacity:0}
#raid{position:absolute;inset:0;z-index:66;background:radial-gradient(circle at 50% 20%,#2B4372,#14213D 70%);color:#fff;opacity:0;transform:scale(1.08);transition:opacity .3s,transform .3s;overflow-y:auto}#raid.on{opacity:1;transform:none}
.rd-in{position:relative;min-height:100%;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;padding:56px 18px 30px;text-align:center}
.rd-ban{font:900 3rem/1 Fraunces,serif;color:#F3D27A;-webkit-text-stroke:1.5px #8A5A0A;text-shadow:0 5px 0 #8A5A0A,0 10px 24px rgba(0,0,0,.4);animation:vfPlusIn .6s cubic-bezier(.2,1.5,.4,1) both}.rd-ban.sm{font-size:2rem}
@keyframes vfPlusIn{from{transform:scale(.2) rotate(-6deg);opacity:0}to{transform:none;opacity:1}}
.rd-who{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:8px;margin:14px 0 18px;font:700 1rem "Nunito Sans";color:#E6EDF8}.rd-who b{color:#F3D27A}
.rd-av{width:34px;height:34px;border-radius:50%;background:#E0A82E;color:#3A2600;font:900 1rem/34px Fraunces,serif}
.rd-wall{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%}
.rd-card{position:relative;display:flex;flex-direction:column;align-items:stretch;padding:6px 6px 8px;border:0;border-radius:16px;background:#FFFDF9;color:#2D2521;font-family:inherit;cursor:pointer;animation:jpIn .5s cubic-bezier(.2,1.3,.4,1) both;box-shadow:0 10px 20px -10px rgba(0,0,0,.6)}
.rd-card img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:11px}.rd-card b{margin-top:6px;font:900 .82rem Fraunces,serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rd-card small{font:700 .66rem "Nunito Sans";color:#4E433C}
.rd-sc{position:absolute;top:10px;right:10px;padding:1px 7px;border-radius:99px;background:#FFFDF9;color:#2D2521;font:900 .78rem Fraunces,serif;font-style:normal;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.rd-tg{position:absolute;left:50%;top:38%;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;border:3px dashed #F3D27A;box-shadow:0 0 0 3px rgba(20,33,61,.45),0 0 18px rgba(243,210,122,.8);animation:rdTg 1.4s linear infinite}@keyframes rdTg{to{transform:rotate(360deg)}}
.rd-hint{margin:16px 0 0;font:800 .85rem "Nunito Sans";color:#C9D6EE}
.rd-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;width:100%}.rd-vs figure{margin:0}.rd-ph{position:relative;display:block}.rd-ph img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:16px;box-shadow:0 0 0 3px #E0A82E}.rd-vs .me .rd-ph img{box-shadow:0 0 0 3px #5B8DEF}
.rd-vs figcaption{margin-top:6px;font:900 .95rem Fraunces,serif}.rd-vs figcaption small{display:block;font:700 .75rem "Nunito Sans";color:#C9D6EE}
.rd-x{width:44px;height:44px;border-radius:50%;background:#F3D27A;color:#3A2600;font:900 1rem/44px Fraunces,serif}
.rd-dots{display:flex;gap:14px;margin:22px 0 6px}.rd-dots i{width:54px;height:54px;border-radius:50%;background:rgba(255,255,255,.12);box-shadow:inset 0 0 0 2px rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-style:normal;animation:rdPulse 1s ease-in-out infinite}
.rd-dots i b{font:900 1.4rem "Nunito Sans";color:#C9D6EE}.rd-dots i.w{background:#2E9A5C;box-shadow:0 0 18px rgba(46,154,92,.8);animation:jpPop .4s}.rd-dots i.l{background:#C8432F;animation:jpPop .4s}.rd-dots i.w b,.rd-dots i.l b{color:#fff}
@keyframes rdPulse{50%{transform:scale(1.08)}}
.rd-tally{font:900 2rem Fraunces,serif;color:#fff;margin:4px 0}
.rd-prize{position:relative;width:180px;margin:18px 0 6px;animation:vfIn .6s cubic-bezier(.2,1.4,.4,1)}.rd-prize img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:18px;box-shadow:0 0 0 4px #9AA6B5}.rd-prize.w img{box-shadow:0 0 0 5px #E0A82E,0 0 40px rgba(243,210,122,.8)}
.rd-new{position:absolute;left:50%;bottom:-12px;transform:translateX(-50%);padding:4px 12px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .74rem "Nunito Sans";letter-spacing:.08em;font-style:normal;white-space:nowrap}
.rd-h{margin:16px 0 0;font:900 1.6rem Fraunces,serif;color:#fff}
.rd-go{margin-top:auto;min-width:240px;padding:15px 24px;border:0;border-radius:999px;background:#FFFDF9;color:#1F3157;font:900 1.05rem "Nunito Sans";cursor:pointer;box-shadow:0 8px 18px -8px rgba(0,0,0,.6)}
.rd-cf{position:absolute;inset:0;pointer-events:none}
.vf-face.back{background:repeating-linear-gradient(45deg,#24396A 0 14px,#1C2E57 14px 28px)!important}
.vf-sp{position:absolute;top:14px;left:0;right:0;font:900 .72rem "Nunito Sans";font-style:normal;letter-spacing:.1em;color:#F3D27A}
.vf-q{font:900 6rem/1 Fraunces,serif;color:#F3D27A;text-shadow:0 0 30px rgba(243,210,122,.8);animation:rdPulse 1.2s ease-in-out infinite}
.vf-tap{position:absolute;bottom:18px;left:0;right:0;margin:0 auto;width:max-content;padding:8px 18px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .95rem "Nunito Sans";white-space:nowrap;animation:rdPulse 1.2s ease-in-out infinite}
#vfRev:not(.flip) .vf-flip{animation:vfIn .5s cubic-bezier(.2,1.4,.4,1),vfWig 2.4s ease-in-out .6s infinite}@keyframes vfWig{0%,80%,100%{transform:none}85%{transform:rotate(-3deg)}90%{transform:rotate(3deg)}95%{transform:rotate(-2deg)}}
html body #vfRev .vf-flip{display:block!important;width:min(240px,70%)!important;height:100%!important;min-height:0!important;padding:0!important;margin:0!important;border:0!important;border-radius:24px!important;background:none!important;box-shadow:none!important;transform-style:preserve-3d!important}
html body #vfRev .vf-face{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;margin:0!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;border-radius:24px!important;overflow:hidden}
html body #vfRev .vf-face.back{background:repeating-linear-gradient(45deg,#24396A 0 14px,#1C2E57 14px 28px)!important;box-shadow:inset 0 0 0 5px #E0A82E,0 0 40px rgba(243,210,122,.55),0 20px 40px -12px rgba(0,0,0,.6)!important}
html body #vfRev .vf-go{opacity:0}html body #vfRev .vf-go.in{opacity:1;animation:vfIn .4s cubic-bezier(.2,1.4,.4,1)}
/* beat the app's general button styles */
html body #vfRev .vf-go{position:absolute;left:50%;bottom:150px;transform:translateX(-50%);z-index:2;display:block;min-width:220px;min-height:52px;padding:0 24px!important;border:0!important;border-radius:999px!important;background:linear-gradient(180deg,#F3D27A,#E0A82E)!important;color:#3A2600!important;font:900 1.05rem "Nunito Sans"!important;box-shadow:0 8px 18px -8px rgba(160,110,10,.8)!important;opacity:1}
html body #vfRev .vf-go:disabled{opacity:0!important}
html body #vfRev .vf-go.nav{background:#2D4E86!important;color:#fff!important;box-shadow:0 8px 18px -8px rgba(45,78,134,.8)!important}
html body #raid .rd-wall{grid-template-columns:repeat(3,minmax(0,1fr))!important}
html body #raid .rd-card{min-width:0!important;width:auto!important;margin:0!important;padding:6px 6px 8px!important;border:0!important;border-radius:16px!important;background:#FFFDF9!important;color:#2D2521!important;box-shadow:0 10px 20px -10px rgba(0,0,0,.6)!important;display:flex!important;flex-direction:column!important;position:relative!important;min-height:0!important;height:auto!important}
html body #raid .rd-card b{color:#2D2521!important;display:block}html body #raid .rd-card small{color:#4E433C!important;display:block;white-space:nowrap}
html body #raid .rd-sc{position:absolute!important;top:10px!important;right:10px!important;left:auto!important;width:auto!important}
html body #raid .rd-go{display:block;min-width:240px;min-height:54px;padding:0 24px!important;border:0!important;border-radius:999px!important;background:#FFFDF9!important;color:#1F3157!important;font:900 1.05rem "Nunito Sans"!important;box-shadow:0 8px 18px -8px rgba(0,0,0,.6)!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('votefx ok')
