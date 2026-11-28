# Skill preview: make voting exciting (our own look, not a copy of any game).
#  1. Right vote: coins burst out of the photos towards you (zoom + fade) with a gold shock ring,
#     on top of the usual "+5" and fly-to-balance.
#  2. Special tile: now and then ONE of the two vote photos is a face-down special tile (no pop-up).
#     Crack it open with 3 taps: tap 1 shudders and cracks it, tap 2 cracks it further and it glows
#     gold (Joker), blue (Steal) or silver (Shield), tap 3 bursts it open in place (no flip) and the
#     prize appears one piece at a time (icon, then title, then amount):
#       🃏 Joker  +20 / +50 / +100 coins (60/30/10%), random; the amount slams in big with glowing
#                rays and sparks, shown as the teal / purple / red Joker card art (assets/joker*.jpg);
#                Big Joker (50) and MEGA Joker (100) get more sparks, a bigger number,
#                and MEGA adds a gold flash and a screen shake; coins fly to your balance
#       🛡 Shield  blocks one steal while you're away (hold up to 3)
#       ⚔️ Challenge  ~1 in 25 right votes when you have a photo at 70+: the Challenge card art
#                (assets/challenge.jpg), then the head-to-head offer opens (you choose to play)
#       🦝 Steal  every 10–15 votes; shows the Steal card art (assets/steal.jpg), then switches to a raid
#     The other photo waits ("Reveal the special photo first") so the tile can't be missed.
#  3. Shields: a 🛡 pill in the header. An overnight steal that hits a shield is blocked and the
#     "While you were away" pop says so.
#  4. Raid: full-screen heist. Flash + slam "RAID!", rotating gold rays and sparkles behind a rival's
#     wall of 3 spot-lit photos. Tap one; your best photo vs it, a score face-off: the wall hides the rival scores ("?"), you pick the one you think
#     scores lowest, then their score is revealed (shake, flash, slam) against your best photo's score;
#     match or beat it to steal it and a "Deciding vote!" moment at 1–1. Win: gold flash, confetti and coin rain,
#     the photo zooms in as a NEW CARD that earns for you. Lose: "So close!", nothing lost.
#     One button back to voting; after a win the card flies into the earnings card at the top of Vote,
#     which turns gold for a few seconds: "<name> is earning for you · 🃏 Stolen card" with a "+8 a vote" chip.
#     Steal tiles are free; steals started from a button (Live games, Payday receipt, Compete, win-back)
#     open this same screen and use one of the 3 daily tries. Win-backs skip the wall: "WON BACK!".
# usage: python3 build-skill/votefx.py in.html out.html
import sys, base64, os
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
JK = {k: 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(ASSETS, f'joker{k}.jpg'), 'rb').read()).decode() for k in (20, 50, 100)}
ST_IMG = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(ASSETS, 'steal.jpg'), 'rb').read()).decode()
CH_IMG = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(ASSETS, 'challenge.jpg'), 'rb').read()).decode()
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = "const JK_IMG = { 20: '" + JK[20] + "', 50: '" + JK[50] + "', 100: '" + JK[100] + "' }, ST_IMG = '" + ST_IMG + "', CHL_IMG = '" + CH_IMG + "';\n" + r'''
// ---- exciting voting: coin burst, special tiles, shields, raids ----
const VF_MAXSH = 3;
let VF_N = S.eyeN || 0, VF_OK = S.eyeOk || 0, VF_G = S.gems || 0, VF_BUSY = 0;
if (S.vfRaidAt == null || S.vfRaidAt < (S.eyeN || 0)) S.vfRaidAt = (S.eyeN || 0) + 10 + Math.floor(Math.random() * 6);
const vfOverlayOpen = () => VF_BUSY || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on') || !!$('#raid');
const vfOrigin = () => { const sh = $('#shell'); let pr = sh.querySelector(':scope > .vf-probe'); if (!pr) { pr = document.createElement('i'); pr.className = 'vf-probe'; sh.appendChild(pr); } return pr.getBoundingClientRect(); };
const vfRel = el => { const o = vfOrigin(), r = el.getBoundingClientRect(); return { x: r.left - o.left, y: r.top - o.top, w: r.width, h: r.height }; };
// 1. coins burst towards you
function vfBurst() { const card = $('#jcard'), sh = $('#shell'); if (!card || !sh || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const r = vfRel(card), x = r.x + r.w / 2, y = r.y + r.h / 2;
  const L = document.createElement('div'); L.className = 'vf-layer'; sh.appendChild(L);
  for (let i = 0; i < 12; i++) { const c = document.createElement('i'); c.className = 'vf-c'; c.innerHTML = gemIcon(''); c.style.left = x + 'px'; c.style.top = y + 'px'; L.appendChild(c);
    const a = i / 12 * Math.PI * 2 + Math.random() * .4, d = 90 + Math.random() * 110, sc = 1.6 + Math.random() * 1.4;
    c.animate([{ transform: 'translate(-50%,-50%) scale(.2)', opacity: 0 }, { transform: `translate(calc(-50% + ${Math.cos(a) * d * .5}px),calc(-50% + ${Math.sin(a) * d * .5}px)) scale(${sc * .6}) rotate(${a * 90}deg)`, opacity: 1, offset: .35 },
      { transform: `translate(calc(-50% + ${Math.cos(a) * d}px),calc(-50% + ${Math.sin(a) * d}px)) scale(${sc}) rotate(${a * 180}deg)`, opacity: 0 }], { duration: 750 + i * 25, easing: 'cubic-bezier(.2,.7,.3,1)', fill: 'forwards' }); }
  const ring = document.createElement('i'); ring.className = 'vf-ring'; ring.style.left = x + 'px'; ring.style.top = y + 'px'; L.appendChild(ring);
  setTimeout(() => L.remove(), 1300); }
// 3. shields
function vfShPaint() { const f = $('#sFlame'); if (!f) return; let b = $('#vfSh'); const n = S.shields || 0;
  if (!b) { b = document.createElement('button'); b.id = 'vfSh'; b.className = 'vf-sh'; b.setAttribute('aria-label', 'Shields'); f.after(b); b.onclick = () => toast(`🛡 ${S.shields || 0} of ${VF_MAXSH} shields · each one blocks a steal while you’re away`); }
  b.hidden = !n; const h = `🛡<b>${n}</b>`; if (b.innerHTML !== h) b.innerHTML = h; }
// 2. the special tile: one of the two vote photos
function vfTile(kind) { const sh = $('#shell'), ph = [...document.querySelectorAll('#jcard button.tot-c')]; if (!sh || ph.length < 2) return; VF_BUSY = 1;
  const k = Math.random() < .5 ? 0 : 1, a = vfRel(ph[k]), b = vfRel(ph[1 - k]);
  const amt = kind === 'coins' ? (r => r < .6 ? 20 : r < .9 ? 50 : 100)(Math.random()) : 0;
  const face = kind === 'coins' ? { ic: '🃏', t: amt === 100 ? 'MEGA Joker!' : amt === 50 ? 'Big Joker!' : 'Joker!', s: `<b class="vf-amt">+${amt}</b> ${gemIcon('vf-gi')}` } : kind === 'steal' ? { ic: '🦝', t: 'Steal!', s: 'Steal time!' } : { ic: '🛡', t: 'Shield!', s: 'Blocks a steal' };
  const el = document.createElement('div'); el.id = 'vfTile';
  el.innerHTML = `<div class="vf-wait" style="left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px"><span>✨ Reveal the special photo first</span></div>
    <button class="vf-flip" style="left:${a.x}px;top:${a.y}px;width:${a.w}px;height:${a.h}px" aria-label="Special photo, tap to reveal">
      <span class="vf-face back"><i class="vf-glow"></i><i class="vf-sp">✨ SPECIAL ✨</i><span class="vf-q">?</span>
        <svg class="vf-crk c1" viewBox="0 0 100 130" preserveAspectRatio="none"><path d="M52 0 L47 22 L56 34 L44 52 L50 63"/><path d="M56 34 L70 40 L78 36"/></svg>
        <svg class="vf-crk c2" viewBox="0 0 100 130" preserveAspectRatio="none"><path d="M50 63 L58 78 L45 96 L53 112 L48 130"/><path d="M44 52 L28 58 L18 54 L6 62"/><path d="M58 78 L76 84 L94 80"/><path d="M45 96 L30 104 L22 118"/></svg>
        <b class="vf-tap">Tap to crack it open</b></span>
      <span class="vf-face front ${kind} ${kind === 'coins' ? 'a' + amt : ''}"><i class="vf-rays"></i>${kind === 'coins' ? `<img class="vf-jk" src="${JK_IMG[amt]}" alt="Joker ${amt} coins">` : kind === 'steal' ? `<img class="vf-jk" src="${ST_IMG}" alt="Steal: take another player’s treasure">` : kind === 'chal' ? `<img class="vf-jk" src="${CHL_IMG}" alt="Challenge: go head-to-head with another player">` : `<span class="vf-ic">${face.ic}</span><h3>${face.t}</h3><p>${face.s}</p>`}</span></button>`;
  sh.appendChild(el); requestAnimationFrame(() => el.classList.add('on'));
  const wt = el.querySelector('.vf-wait'), fp = el.querySelector('.vf-flip'), put = (n, r) => { n.style.left = r.x + 'px'; n.style.top = r.y + 'px'; n.style.width = r.w + 'px'; n.style.height = r.h + 'px'; };
  const follow = () => { if (!el.isConnected) return; const cur = document.querySelectorAll('#jcard button.tot-c'); if (cur.length >= 2) { put(fp, vfRel(cur[k])); put(wt, vfRel(cur[1 - k])); } requestAnimationFrame(follow); }; follow(); // re-find the photos every frame: they can be rebuilt or pushed down
  const done = (ms = 1500) => setTimeout(() => { el.classList.remove('on'); setTimeout(() => { el.remove(); VF_BUSY = 0; }, 250); }, ms);
  let taps = 0; const hue = kind === 'coins' ? 'gold' : kind === 'steal' ? 'blue' : kind === 'chal' ? 'red' : 'silver', tapTx = ['Tap to crack it open', 'Again!', 'One more!'];
  el.querySelector('.vf-flip').onclick = () => { if (el.classList.contains('open')) return; taps++; const fl = el.querySelector('.vf-flip'), r0 = vfRel(fl);
    fl.classList.remove('shud'); void fl.offsetWidth; fl.classList.add('shud');
    if (taps < 3) { el.classList.add('t' + taps); if (taps === 2) el.classList.add('hue-' + hue); el.querySelector('.vf-tap').textContent = tapTx[taps];
      vfPop(sh, r0.x + r0.w / 2, r0.y + r0.h * (taps === 1 ? .3 : .6), taps === 2 ? (hue === 'blue' ? ['#5B8DEF', '#fff'] : hue === 'silver' ? ['#D7DCE3', '#fff'] : ['#F3D27A', '#fff']) : ['#fff', '#F3D27A'], 8 + taps * 6); return; }
    el.classList.add('t3'); vfPop(sh, r0.x + r0.w / 2, r0.y + r0.h / 2, hue === 'blue' ? ['#5B8DEF', '#F3D27A', '#fff'] : hue === 'silver' ? ['#D7DCE3', '#fff', '#9AA6B5'] : ['#F3D27A', '#E0A82E', '#fff'], 34);
    setTimeout(() => el.classList.add('open'), 160); const fr = el.querySelector('.vf-face.front');
    setTimeout(() => {
      if (kind === 'coins') { const b = el.querySelector('.vf-jk'), r = vfRel(fr), cx = r.x + r.w / 2, cy = r.y + r.h / 2;
        el.classList.add('wow', 'a' + amt); b.classList.add('slam');
        const big = amt >= 50, mega = amt === 100;
        vfPop(sh, cx, cy, ['#F3D27A', '#E0A82E', '#fff', '#FF6B6B', '#5B8DEF', '#3CCB8A'], mega ? 60 : big ? 40 : 24);
        if (big) setTimeout(() => vfPop(sh, cx, cy, ['#F3D27A', '#fff'], mega ? 40 : 20), 260);
        if (mega) { const f = document.createElement('i'); f.className = 'vf-flash'; sh.appendChild(f); setTimeout(() => f.remove(), 700); const app = $('#judge'); if (app) { app.classList.remove('vf-quake'); void app.offsetWidth; app.classList.add('vf-quake'); } }
        setTimeout(() => { S.gems += amt; VF_G = S.gems; save(); try { gemExplosion(amt, { mid: 1, from: fr }); } catch (e) { paintGems(); } }, 650);
        done(mega ? 2400 : big ? 2000 : 1700); }
      else if (kind === 'shield') { S.shields = Math.min(VF_MAXSH, (S.shields || 0) + 1); save(); vfShPaint(); const sb = $('#vfSh'); if (sb) { sb.classList.remove('bump'); void sb.offsetWidth; sb.classList.add('bump'); } done(1600); }
      else if (kind === 'chal') { const r = vfRel(fr); vfPop(sh, r.x + r.w / 2, r.y + r.h / 2, ['#C8432F', '#5B8DEF', '#F3D27A', '#fff'], 36); setTimeout(() => { el.remove(); VF_BUSY = 0; try { h2hSheet(); } catch (e) {} }, 1600); }
      else { const r = vfRel(fr); vfPop(sh, r.x + r.w / 2, r.y + r.h / 2, ['#3CCB8A', '#F3D27A', '#fff'], 36); setTimeout(() => { el.remove(); VF_BUSY = 0; raidStart(); }, 1600); } }, 700); }; }
// little burst of sparks
function vfPop(host, x, y, cols, n = 16) { const L = document.createElement('div'); L.className = 'vf-layer'; host.appendChild(L);
  for (let i = 0; i < n; i++) { const p = document.createElement('i'); p.className = 'vf-spk'; p.style.left = x + 'px'; p.style.top = y + 'px'; p.style.background = cols[i % cols.length]; L.appendChild(p);
    const a = Math.random() * Math.PI * 2, d = 50 + Math.random() * 90; p.animate([{ transform: 'translate(-50%,-50%) scale(1)', opacity: 1 }, { transform: `translate(calc(-50% + ${Math.cos(a) * d}px),calc(-50% + ${Math.sin(a) * d}px)) scale(.2)`, opacity: 0 }], { duration: 600 + Math.random() * 300, easing: 'cubic-bezier(.2,.8,.3,1)', fill: 'forwards' }); }
  setTimeout(() => L.remove(), 1000); }
// 4. raids
const RD_POOL = () => { const mine = new Set(S.photos.flatMap(p => [p.src, p.orig])), taken = S.stlTaken || [], out = [];
  GAL.PATH.forEach(c => SEED.filter(x => x.cat === BATTLE_POOL[c] && !mine.has(x.src) && !taken.includes(x.id)).forEach(x => out.push({ key: x.id, src: x.src, nm: x.title || 'Photo', cat: c, sc: 68 + hsh(x.id) % 22 }))); return out; };
const rdStage = el => el.querySelector('.rd-in');
function raidStart() { const me = S.photos.filter(p => p.s && !p.heldBy).sort((a, b) => b.s.total - a.s.total)[0], pool = RD_POOL(); if (!me || pool.length < 3) return;
  const rv = RIVALS[Math.floor(Math.random() * RIVALS.length)], wall = pool.sort(() => Math.random() - .5).slice(0, 3).map(x => ({ ...x, h: rv.h }));
  const sh = $('#shell'), el = document.createElement('div'); el.id = 'raid'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Steal');
  el.innerHTML = `<div class="rd-rays"></div><div class="rd-sparks">${[...Array(22)].map((_, i) => `<i style="left:${(i * 47) % 100}%;top:${(i * 29) % 100}%;animation-delay:${(i * .23 % 2).toFixed(2)}s"></i>`).join('')}</div><i class="rd-flash"></i>
    <div class="rd-in"><div class="rd-ban">STEAL!</div><p class="rd-who"><span class="rd-av">${rv.n[0]}</span>${rv.n}’s gallery · <b>steal one photo</b></p>
    <div class="rd-wall">${wall.map((w, i) => `<button class="rd-card" data-rd="${i}" style="--d:${(.55 + i * .15).toFixed(2)}s"><span class="rd-lamp"></span><span class="rd-fr"><img src="${w.src}" alt=""><i class="rd-sc">?</i><span class="rd-tg"></span></span><b>${esc(w.nm)}</b><small>Score hidden</small></button>`).join('')}</div>
    <p class="rd-hint">👆 Pick the photo you think scores lowest · your best photo scores ${me.s.total} · nothing to lose</p></div>`;
  sh.appendChild(el); requestAnimationFrame(() => { el.classList.add('on'); setTimeout(() => el.classList.add('shake'), 420); });
  el.querySelectorAll('[data-rd]').forEach(b => b.onclick = () => { if (el.dataset.pick) return; el.dataset.pick = 1; b.classList.add('picked'); el.querySelectorAll('.rd-card').forEach(c => c !== b && c.classList.add('gone'));
    const r = vfRel(b); vfPop(el, r.x + r.w / 2, r.y + r.h / 2, ['#F3D27A', '#fff'], 18); setTimeout(() => raidFight(el, me, wall[+b.dataset.rd], rv), 650); }); }
function raidFight(el, me, them, rv) { const won = me.s.total >= them.sc;
  el.classList.remove('shake'); el.classList.add('tense'); rdStage(el).innerHTML = `<div class="rd-ban sm">STEAL</div><p class="rd-who" id="rdSay">Match or beat their score to steal it</p>
    <div class="rd-vs"><figure class="th"><span class="rd-ph"><img src="${them.src}" alt=""><span class="rd-big hide" id="rdTS"><b>?</b><small>score</small></span></span><figcaption>${esc(them.nm)}<small>${rv.n}</small></figcaption></figure><span class="rd-x">VS</span>
      <figure class="me"><span class="rd-ph"><img src="${me.src}" alt=""><span class="rd-big mine"><b>${me.s.total}</b><small>your score</small></span></span><figcaption>${esc(alName(me))}<small>You</small></figcaption></figure></div>
    <p class="rd-drum" id="rdDrum">Revealing their score…</p>`;
  setTimeout(() => { if (!el.isConnected) return; const ts = $('#rdTS'); ts.classList.add('shake'); }, 700);
  setTimeout(() => { if (!el.isConnected) return; const ts = $('#rdTS'); ts.classList.remove('hide', 'shake'); ts.classList.add('show', won ? 'lo' : 'hi'); ts.querySelector('b').textContent = them.sc;
    const fl = el.querySelector('.rd-flash'); fl.classList.remove('go'); void fl.offsetWidth; fl.classList.add('go');
    const r = vfRel(ts); vfPop(el, r.x + r.w / 2, r.y + r.h / 2, ['#F3D27A', '#fff', '#E0A82E'], 30);
    el.querySelector(won ? '.rd-vs .me' : '.rd-vs .th').classList.add('win'); el.querySelector(won ? '.rd-vs .th' : '.rd-vs .me').classList.add('lose');
    $('#rdDrum').innerHTML = won ? `<b class="ok">${me.s.total} ${me.s.total === them.sc ? 'matches' : 'beats'} ${them.sc}!</b>` : `<b class="no">${them.sc} beats ${me.s.total}</b>`; el.classList.remove('tense');
    setTimeout(() => raidDone(el, me, them, rv, won, me.s.total, them.sc), 1700); }, 2300); }
function raidDone(el, me, them, rv, won, m, t) { el.classList.remove('tense');
  if (won && them.back) { them.back.heldBy = null; them.back.heldAt = null; if (S.awayNews && S.awayNews.st) S.awayNews.st = null; save(); }
  else if (won) { S.photos.push({ id: uid(), src: them.src, orig: them.src, cat: them.cat, nm: them.nm, nmAsk: 1, enh: 0, at: Date.now(), card: { from: rv.h }, s: { light: them.sc, comp: them.sc, colour: them.sc, tech: them.sc, total: them.sc } }); S.stlTaken = (S.stlTaken || []).concat(them.key); save(); }
  el.classList.add(won ? 'win' : 'lose'); const fl = el.querySelector('.rd-flash'); fl.classList.remove('go'); void fl.offsetWidth; fl.classList.add('go');
  rdStage(el).innerHTML = `${won ? `<div class="rd-conf" aria-hidden="true">${[...Array(40)].map((_, i) => `<i style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A', '#F59E0B', '#fff'][i % 6]};animation-delay:${(i * .05).toFixed(2)}s;animation-duration:${(1.8 + (i % 5) * .3).toFixed(2)}s"></i>`).join('')}
      ${[...Array(12)].map((_, i) => `<span class="rd-coin" style="left:${(i * 61 + 7) % 92}%;animation-delay:${(.2 + i * .12).toFixed(2)}s">${gemIcon('')}</span>`).join('')}</div>` : ''}
    <div class="rd-ban">${won ? (them.back ? 'WON BACK!' : 'STOLEN!') : 'So close!'}</div>
    <div class="rd-prize ${won ? 'w' : ''}"><img src="${them.src}" alt="">${won ? (them.back ? '<i class="rd-new">✨ BACK IN YOUR GALLERY ✨</i>' : '<i class="rd-new">✨ NEW CARD ✨</i>') : ''}</div>
    <h3 class="rd-h">${won ? (them.back ? `${esc(them.nm)} is yours again!` : `${esc(them.nm)} is yours!`) : `${rv.n} kept ${esc(them.nm)}`}</h3>
    <p class="rd-who">${won ? `It earns you <b>${cardRate(them.sc)} 🟡 a vote</b> from now on · ${m} vs ${t}` : `${t} beat your ${m} · nothing lost · another steal is coming`}</p>
    <button class="rd-go">Back to voting</button>`;
  if (won) setTimeout(() => { const pr = el.querySelector('.rd-prize'); if (pr) { const r = vfRel(pr); vfPop(el, r.x + r.w / 2, r.y + r.h / 2, ['#F3D27A', '#fff', '#E0A82E'], 30); } }, 350);
  el.querySelector('.rd-go').onclick = () => { el.classList.remove('on'); setTimeout(() => el.remove(), 300); try { renderJudge(); } catch (e) {} if (won) setTimeout(() => rdLand(them), 450); }; }
// the stolen card flies into the earnings card at the top of Vote, which celebrates it for a few seconds
function rdLand(c) { const sh = $('#shell'), g = $('#vgGoal'); if (!sh || !g) return; const rate = cardRate(c.sc), gr = vfRel(g), tg = g.querySelector('img') ? vfRel(g.querySelector('img')) : { x: gr.x + 10, y: gr.y + 10, w: 60, h: 70 };
  const fly = document.createElement('img'); fly.className = 'rd-fly'; fly.src = c.src; const W = 150, H = 200, sr = sh.getBoundingClientRect(); fly.style.cssText = `left:${sr.width / 2 - W / 2}px;top:${sr.height / 2 - H / 2}px;width:${W}px;height:${H}px`; sh.appendChild(fly);
  fly.animate([{ transform: 'scale(.4) rotate(-20deg)', opacity: 0 }, { transform: 'scale(1.1) rotate(6deg)', opacity: 1, offset: .3 }, { transform: `translate(${tg.x + tg.w / 2 - sr.width / 2}px,${tg.y + tg.h / 2 - sr.height / 2}px) scale(${tg.w / W}) rotate(0deg)`, opacity: 1 }], { duration: 950, easing: 'cubic-bezier(.5,0,.3,1)', fill: 'forwards' });
  setTimeout(() => { fly.remove(); const until = Date.now() + 7000; vfPop(sh, tg.x + tg.w / 2, tg.y + tg.h / 2, ['#F3D27A', '#fff', '#E0A82E'], 26);
    const paint = () => { const g2 = $('#vgGoal'); if (!g2) return; g2.classList.add('vg-got'); if (!g2.querySelector('.vg-new')) g2.insertAdjacentHTML('beforeend', `<span class="vg-new"><img src="${c.src}" alt=""><span class="vg-nt"><b>${esc(c.nm)} is earning for you</b><small>🃏 Stolen card · in your collection</small></span><span class="vg-nc">+${rate}<small>a vote</small></span><i class="vg-sh"></i></span>`); };
    paint(); const iv = setInterval(() => { if (Date.now() > until) { clearInterval(iv); const g3 = $('#vgGoal'); if (g3) { g3.classList.add('vg-out'); setTimeout(() => { g3.classList.remove('vg-got', 'vg-out'); g3.querySelectorAll('.vg-new').forEach(x => x.remove()); }, 400); } return; } paint(); }, 300); }, 950); }

// every steal uses the same full-screen steal (buttons, receipt, Compete, win-backs); button steals use the 3 daily tries
function raidShell() { const sh = $('#shell'), el = document.createElement('div'); el.id = 'raid'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Steal');
  el.innerHTML = `<div class="rd-rays"></div><div class="rd-sparks">${[...Array(22)].map((_, i) => `<i style="left:${(i * 47) % 100}%;top:${(i * 29) % 100}%;animation-delay:${(i * .23 % 2).toFixed(2)}s"></i>`).join('')}</div><i class="rd-flash"></i><div class="rd-in"></div>`;
  sh.appendChild(el); requestAnimationFrame(() => el.classList.add('on')); return el; }
function raidBack(p) { const me = S.photos.filter(x => x.s && !x.heldBy).sort((a, b) => b.s.total - a.s.total)[0]; if (!me) { toast('Add a photo to your gallery to play for cards'); return; }
  const rv = RIVALS.find(r => r.h === p.heldBy) || { h: p.heldBy, n: rvName(p.heldBy) }, el = raidShell();
  raidFight(el, me, { src: p.src, sc: p.s.total, nm: alName(p), cat: p.cat, h: p.heldBy, back: p }, rv); }
stealSheet = function (o = {}) { try { closeSheet(); } catch (e) {} try { const co = $('#coach'); co.classList.remove('on', 'cr'); co.innerHTML = ''; } catch (e) {}
  if (!stlLeft()) { toast('3 steals a day · new tries tomorrow, or reveal a Steal tile while voting'); return; }
  const back = o.back && S.photos.find(x => x.id === o.back && x.heldBy);
  if (!back && RD_POOL().length < 3) { toast('No cards to steal right now'); return; }
  if (!S.photos.some(x => x.s && !x.heldBy)) { toast('Add a photo to your gallery to play for cards'); return; }
  stlDay().n++; save(); setTimeout(() => back ? raidBack(back) : raidStart(), 120); };
// watch each vote
setInterval(() => { try { const n = S.eyeN || 0; if (n <= VF_N) { VF_G = S.gems; vfShPaint(); return; } const ok = (S.eyeOk || 0) > VF_OK; VF_N = n; VF_OK = S.eyeOk || 0; VF_G = S.gems || 0;
  if (ok) vfBurst();
  let kind = null;
  if (n >= S.vfRaidAt) { S.vfRaidAt = n + 10 + Math.floor(Math.random() * 6); if (RD_POOL().length >= 3) kind = 'steal'; }
  else if (ok) { S.vfR = (S.vfR || 0) + 1; const first = !S.vfFirst && S.vfR >= 4, roll = Math.random(); kind = first ? 'coins' : roll < .08 ? 'coins' : roll < .12 && (S.shields || 0) < VF_MAXSH ? 'shield' : roll < .16 && fighters().length ? 'chal' : null; if (first) S.vfFirst = 1; }
  save(); if (kind) setTimeout(() => { if (!vfOverlayOpen() && $('#panes').dataset.at === 'judge') vfTile(kind); }, 1000);
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
.vf-layer{position:absolute;inset:0;pointer-events:none;z-index:80;overflow:hidden}
.vf-c{position:absolute;width:34px;height:34px;filter:drop-shadow(0 4px 6px rgba(120,80,0,.35))}.vf-c svg{width:100%;height:100%}
.vf-ring{position:absolute;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;border:5px solid #F3D27A;animation:vfRing .7s ease-out forwards}@keyframes vfRing{to{transform:scale(7);opacity:0;border-width:1px}}
.vf-spk{position:absolute;width:10px;height:10px;border-radius:50%;box-shadow:0 0 8px currentColor}
.vf-sh{display:inline-flex;align-items:center;gap:3px;margin-left:6px;padding:4px 10px;border:0;border-radius:99px;background:linear-gradient(180deg,#fff,#D7DCE3);box-shadow:inset 0 0 0 1.5px #B9C2CE;font:900 .9rem "Nunito Sans";color:#2E3440;cursor:pointer}.vf-sh[hidden]{display:none}
.vf-sh.bump{animation:jpPop .5s ease-out}
@keyframes vfIn{from{transform:scale(.3) rotate(-8deg);opacity:0}to{transform:none;opacity:1}}
@keyframes vfWig{0%,80%,100%{transform:none}85%{transform:rotate(-3deg)}90%{transform:rotate(3deg)}95%{transform:rotate(-2deg)}}
@keyframes rdPulse{50%{transform:scale(1.08)}}
/* the special tile sits exactly on one vote photo */
#vfTile{position:absolute;inset:0;z-index:60;pointer-events:none;opacity:0;transition:opacity .2s}#vfTile.on{opacity:1}
#vfTile .vf-wait{position:absolute;pointer-events:auto;border-radius:22px;background:rgba(20,33,61,.55);display:flex;align-items:flex-end;justify-content:center;padding-bottom:14px;box-sizing:border-box}
#vfTile .vf-wait span{padding:6px 12px;border-radius:99px;background:rgba(255,253,249,.92);color:#1F3157;font:800 .74rem "Nunito Sans";text-align:center}
html body #vfTile .vf-flip{position:absolute!important;pointer-events:auto;display:block!important;padding:0!important;margin:0!important;border:0!important;border-radius:22px!important;background:none!important;box-shadow:none!important;cursor:pointer;transform-style:preserve-3d!important;transition:transform .6s cubic-bezier(.3,1.3,.5,1);perspective:1000px;min-height:0!important}
#vfTile:not(.open) .vf-flip{animation:vfFade .25s ease-out}@keyframes vfFade{from{opacity:0}}
#vfTile:not(.open) .vf-face.back{animation:vfBackGlow 1.6s ease-in-out infinite}@keyframes vfBackGlow{50%{box-shadow:inset 0 0 0 4px #F3D27A,0 0 34px 6px rgba(243,210,122,.85)}}
#vfTile.open .vf-flip{transform:none}
html body #vfTile .vf-face{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;margin:0!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:4px;text-align:center;border-radius:22px!important;overflow:hidden;backface-visibility:hidden;-webkit-backface-visibility:hidden}
html body #vfTile .vf-face.back{background:repeating-linear-gradient(45deg,#24396A 0 14px,#1C2E57 14px 28px)!important;box-shadow:inset 0 0 0 4px #E0A82E,0 0 26px rgba(243,210,122,.7)!important}
.vf-sp{position:absolute;top:12px;left:0;right:0;font:900 .7rem "Nunito Sans";font-style:normal;letter-spacing:.1em;color:#F3D27A}
.vf-q{font:900 5rem/1 Fraunces,serif;color:#F3D27A;text-shadow:0 0 30px rgba(243,210,122,.8);animation:rdPulse 1.2s ease-in-out infinite}
.vf-tap{position:absolute;bottom:14px;left:0;right:0;margin:0 auto;width:max-content;padding:7px 14px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .85rem "Nunito Sans";white-space:nowrap;animation:rdPulse 1.2s ease-in-out infinite}
html body #vfTile .vf-face.front{transform:none;background:linear-gradient(180deg,#FFF6DD,#F3D27A)!important;box-shadow:inset 0 0 0 4px #E0A82E,0 0 40px rgba(243,210,122,.8)!important}
html body #vfTile .vf-face.front.steal{background:radial-gradient(circle at 50% 35%,#3A5A9A,#14213D)!important}
html body #vfTile .vf-face.front.shield{background:linear-gradient(180deg,#fff,#D7DCE3)!important;box-shadow:inset 0 0 0 4px #9AA6B5,0 0 40px rgba(215,220,227,.8)!important}
/* crack it open */
.vf-crk{position:absolute;inset:0;width:100%;height:100%;opacity:0;pointer-events:none;transition:opacity .15s}.vf-crk path{fill:none;stroke:#FFF6DD;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;filter:drop-shadow(0 0 3px #fff) drop-shadow(0 0 6px #F3D27A)}
#vfTile.t1 .vf-crk.c1,#vfTile.t2 .vf-crk.c2,#vfTile.t2 .vf-crk.c1{opacity:1}
.vf-glow{position:absolute;inset:0;opacity:0;transition:opacity .25s;background:radial-gradient(circle at 50% 50%,rgba(255,246,221,.55),transparent 65%)}#vfTile.t1 .vf-glow{opacity:.5}#vfTile.t2 .vf-glow{opacity:1}
#vfTile.hue-gold .vf-glow{background:radial-gradient(circle at 50% 50%,rgba(255,214,102,.85),transparent 70%)}#vfTile.hue-blue .vf-glow{background:radial-gradient(circle at 50% 50%,rgba(91,141,239,.9),transparent 70%)}#vfTile.hue-silver .vf-glow{background:radial-gradient(circle at 50% 50%,rgba(230,236,244,.9),transparent 70%)}
html body #vfTile.hue-gold .vf-face.back{box-shadow:inset 0 0 0 4px #E0A82E,0 0 34px 8px rgba(255,214,102,.95)!important}html body #vfTile.hue-blue .vf-face.back{box-shadow:inset 0 0 0 4px #5B8DEF,0 0 34px 8px rgba(91,141,239,.95)!important}html body #vfTile.hue-silver .vf-face.back{box-shadow:inset 0 0 0 4px #C9D1DC,0 0 34px 8px rgba(230,236,244,.95)!important}
html body #vfTile .vf-face{overflow:hidden!important}
#vfTile.t1:not(.open) .vf-flip,#vfTile.t2:not(.open) .vf-flip{animation:none}
html body #vfTile .vf-flip.shud{animation:vfShud .38s ease-in-out!important}@keyframes vfShud{15%{transform:translateX(-5px)}30%{transform:translateX(5px)}45%{transform:translateX(-4px)}60%{transform:translateX(3px)}80%{transform:translateX(-1px)}}
#vfTile.open .vf-flip.shud{animation:none!important}
#vfTile.t2 .vf-q{animation:rdPulse .45s ease-in-out infinite}
/* open in place: the back bursts away, then card, title and amount appear one after another */
html body #vfTile .vf-face.front{opacity:0}
#vfTile.open .vf-face.back{animation:vfBurstOut .22s ease-in forwards}@keyframes vfBurstOut{to{transform:scale(1.08);opacity:0}}
#vfTile.open .vf-face.front{opacity:1;transition:opacity .15s .1s}
#vfTile .vf-face.front .vf-ic,#vfTile .vf-face.front h3,#vfTile .vf-face.front p{opacity:0}
#vfTile.open .vf-face.front .vf-ic{animation:vfStep .45s cubic-bezier(.2,1.7,.4,1) .2s both}
#vfTile.open .vf-face.front h3{animation:vfStep .4s cubic-bezier(.2,1.7,.4,1) .5s both}
#vfTile.open .vf-face.front p{animation:vfStepP .1s linear .75s both}
@keyframes vfStep{from{transform:scale(.3);opacity:0}to{transform:none;opacity:1}}@keyframes vfStepP{from{opacity:0}to{opacity:1}}
#vfTile.wow.a50 .vf-face.front .vf-ic,#vfTile.wow.a100 .vf-face.front .vf-ic{opacity:1}
/* joker card art */
html body #vfTile .vf-face.front.chal{background:#0C1529!important;box-shadow:inset 0 0 0 4px #C8432F,0 0 50px 6px rgba(200,67,47,.7)!important}
html body #vfTile.hue-red .vf-face.back{box-shadow:inset 0 0 0 4px #C8432F,0 0 34px 8px rgba(255,107,107,.9)!important}#vfTile.hue-red .vf-glow{background:radial-gradient(circle at 50% 50%,rgba(255,107,107,.85),transparent 70%)}
/* steal votes: same look as voting (who got each vote), not ticks */
html body #raid .rd-dots i{position:relative;overflow:visible}html body #raid .rd-dots i.me,html body #raid .rd-dots i.them{background:none;animation:rdDot .45s cubic-bezier(.2,1.6,.4,1)}
#raid .rd-dots i img{width:100%;height:100%;border-radius:50%;object-fit:cover}
#raid .rd-dots i.me img{box-shadow:0 0 0 4px #5B8DEF,0 0 20px rgba(91,141,239,.9)}#raid .rd-dots i.them img{box-shadow:0 0 0 4px #E0A82E,0 0 20px rgba(243,210,122,.9)}
#raid .rd-dots i small{position:absolute;left:50%;bottom:-20px;transform:translateX(-50%);font:800 .7rem "Nunito Sans";white-space:nowrap}#raid .rd-dots i.me small{color:#9FBDF5}#raid .rd-dots i.them small{color:#F3D27A}
#raid .rd-tally{margin-top:22px}#raid .rd-tally b:first-child{color:#F3D27A}#raid .rd-tally b:last-child{color:#9FBDF5}
.rd-key{display:flex;gap:70px;margin:0;font:800 .78rem "Nunito Sans"}.rd-key .t{color:#F3D27A}.rd-key .m{color:#9FBDF5}
.vf-probe{position:absolute;left:0;top:0;width:0;height:0;pointer-events:none;visibility:hidden}
@keyframes vfJk{0%{transform:scale(1.6);opacity:0}60%{transform:scale(.97);opacity:1}100%{transform:none;opacity:1}}
html body #vfTile .vf-face.front.coins{background:radial-gradient(circle at 50% 45%,#2B4372,#0C1529)!important;box-shadow:inset 0 0 0 4px #E0A82E,0 0 40px rgba(243,210,122,.8)!important}
html body #vfTile .vf-face.front.coins.a20{box-shadow:inset 0 0 0 4px #4FB3BF,0 0 40px rgba(79,179,191,.85)!important}
html body #vfTile .vf-face.front.coins.a50{box-shadow:inset 0 0 0 4px #B26BE0,0 0 46px rgba(178,107,224,.9)!important}
html body #vfTile .vf-face.front.coins.a100{background:radial-gradient(circle at 50% 45%,#5A1A1A,#140808)!important;box-shadow:inset 0 0 0 4px #F3C24A,0 0 60px 10px rgba(243,194,74,.95)!important}
.vf-jk{position:absolute;inset:0;z-index:1;width:100%;height:100%;max-width:none;object-fit:cover;object-position:50% 55%;border-radius:22px;opacity:0}
#vfTile.open .vf-jk{animation:vfJk .7s cubic-bezier(.2,1.6,.4,1) .15s both}@keyframes vfJk{0%{transform:scale(2.6) rotate(-10deg);opacity:0}55%{transform:scale(.9) rotate(2deg);opacity:1}100%{transform:none;opacity:1}}
html body #vfTile .vf-face.front.steal{background:radial-gradient(circle at 50% 45%,#1E3A5F,#07101F)!important;box-shadow:inset 0 0 0 4px #2E9A5C,0 0 50px 6px rgba(60,203,138,.75)!important}
#vfTile.wow .vf-jk{animation:vfJk .7s cubic-bezier(.2,1.6,.4,1) .15s both}
.vf-amt{display:inline-block}
.vf-rays{position:absolute;left:50%;top:50%;width:300%;height:300%;margin:-150% 0 0 -150%;background:repeating-conic-gradient(rgba(255,255,255,.55) 0 8deg,transparent 8deg 20deg);opacity:0;pointer-events:none}
#vfTile.wow .vf-rays{opacity:1;animation:vfRaysIn .5s ease-out,vfRayP 1.4s ease-in-out .5s infinite}@keyframes vfRayP{50%{opacity:.5}}@keyframes vfRaysIn{from{transform:scale(.2)}}
#vfTile.wow .vf-face.front{animation:vfGlowP 1s ease-in-out infinite}@keyframes vfGlowP{50%{box-shadow:inset 0 0 0 4px #E0A82E,0 0 60px 14px rgba(255,214,102,.95)}}
.vf-amt.slam{animation:vfSlam .7s cubic-bezier(.2,1.7,.4,1) both;color:#1E6B3E!important}@keyframes vfSlam{0%{transform:scale(4) rotate(-12deg);opacity:0}55%{transform:scale(.85) rotate(3deg);opacity:1}100%{transform:scale(1.2)}}
html body #vfTile .vf-face.front.a50 p b{font-size:2.6rem!important}html body #vfTile .vf-face.front.a100 p b{font-size:3.2rem!important;color:#B4231A!important;text-shadow:0 3px 0 #F3D27A,0 0 18px rgba(255,214,102,.9)}
#vfTile .vf-face.front.a50 h3,#vfTile .vf-face.front.a100 h3{font-size:1.65rem}#vfTile .vf-face.front.a100 h3{color:#B4231A}
html body #vfTile .vf-face.front.a100{background:radial-gradient(circle at 50% 40%,#FFF6DD,#F3D27A 55%,#E0A82E)!important}
#vfTile .vf-face.front.a100 .vf-ic{font-size:3rem}#vfTile .vf-face.front.a100 h3{line-height:1.05;margin:2px 0}
#vfTile.wow.a50 .vf-ic,#vfTile.wow.a100 .vf-ic{animation:vfBob 1.2s ease-in-out infinite}@keyframes vfIcon{from{transform:scale(.2) rotate(-30deg)}to{transform:scale(1.05)}}@keyframes vfBob{50%{transform:scale(1.05) rotate(-6deg)}}
.vf-flash{position:absolute;inset:0;z-index:90;background:#FFF3C4;pointer-events:none;animation:rdFlash .6s ease-out forwards}
.vf-quake{animation:rdShake .5s ease-in-out}
.vf-ic{font-size:3.8rem;line-height:1}
.vf-face h3{margin:0;font:900 1.5rem Fraunces,serif;color:#3A2600}.vf-face.steal h3{color:#F3D27A}.vf-face.shield h3{color:#1F3157}
.vf-face p{margin:0 8px;display:flex;align-items:center;justify-content:center;gap:5px;font:800 .9rem "Nunito Sans";color:#4E433C}.vf-face.steal p{color:#E6EDF8}.vf-face p b{font:900 1.8rem Fraunces,serif;color:#2D4E86}.vf-gi{width:24px;height:24px}
/* raid */
#raid{position:absolute;inset:0;z-index:66;overflow:hidden;color:#fff;background:radial-gradient(circle at 50% 28%,#3A5A9A 0%,#1C2E57 42%,#0C1529 100%);opacity:0;transform:scale(1.1);transition:opacity .3s,transform .35s cubic-bezier(.2,1.2,.4,1)}#raid.on{opacity:1;transform:none}
.rd-rays{position:absolute;left:50%;top:22%;width:240vmax;height:240vmax;margin:-120vmax 0 0 -120vmax;background:repeating-conic-gradient(from 0deg,rgba(243,210,122,.09) 0 9deg,transparent 9deg 22deg);animation:rdSpin 24s linear infinite;pointer-events:none}
@keyframes rdSpin{to{transform:rotate(360deg)}}
#raid.win{background:radial-gradient(circle at 50% 30%,#4A6CB0 0%,#203766 45%,#0C1529 100%)}#raid.win .rd-rays{background:repeating-conic-gradient(from 0deg,rgba(255,206,84,.2) 0 9deg,transparent 9deg 22deg);animation-duration:8s}
#raid.lose .rd-rays{background:repeating-conic-gradient(from 0deg,rgba(201,214,238,.08) 0 9deg,transparent 9deg 22deg)}
#raid.tense .rd-rays{animation-duration:4s}
.rd-sparks{position:absolute;inset:0;pointer-events:none}.rd-sparks i{position:absolute;width:4px;height:4px;border-radius:50%;background:#F3D27A;box-shadow:0 0 8px #F3D27A;animation:rdTw 2s ease-in-out infinite}@keyframes rdTw{0%,100%{opacity:.15;transform:scale(.6)}50%{opacity:1;transform:scale(1.4)}}
.rd-flash{position:absolute;inset:0;background:#fff;pointer-events:none;opacity:0;animation:rdFlash .5s ease-out .05s}.rd-flash.go{animation:rdFlash .6s ease-out}#raid.win .rd-flash.go{background:#FFF3C4}@keyframes rdFlash{0%{opacity:.85}100%{opacity:0}}
.rd-in{position:relative;z-index:1;height:100%;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:28px 16px 32px;text-align:center}
#raid.shake .rd-in{animation:rdShake .45s ease-in-out}@keyframes rdShake{20%{transform:translate(-6px,3px)}40%{transform:translate(6px,-3px)}60%{transform:translate(-4px,2px)}80%{transform:translate(3px,-1px)}}
.rd-ban{font:900 3.6rem/1 Fraunces,serif;color:#F3D27A;-webkit-text-stroke:2px #8A5A0A;text-shadow:0 6px 0 #8A5A0A,0 14px 30px rgba(0,0,0,.45),0 0 40px rgba(243,210,122,.5);animation:rdSlam .55s cubic-bezier(.2,1.6,.4,1) both}.rd-ban.sm{font-size:2.2rem}
@keyframes rdSlam{0%{transform:scale(3) rotate(-8deg);opacity:0}60%{transform:scale(.92) rotate(2deg);opacity:1}100%{transform:none}}
.rd-who{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:8px;margin:14px 0 18px;font:700 1rem "Nunito Sans";color:#E6EDF8}.rd-who b{color:#F3D27A}
.rd-av{width:34px;height:34px;border-radius:50%;background:#E0A82E;color:#3A2600;font:900 1rem/34px Fraunces,serif;box-shadow:0 0 0 3px rgba(243,210,122,.35)}
html body #raid .rd-wall{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px;width:100%;max-width:380px}
html body #raid .rd-card{position:relative!important;display:flex!important;flex-direction:column!important;align-items:stretch;min-width:0!important;width:auto!important;margin:0!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;color:#fff!important;min-height:0!important;height:auto!important;cursor:pointer;animation:rdDrop .6s cubic-bezier(.2,1.4,.4,1) var(--d) both}
@keyframes rdDrop{from{transform:translateY(-60px) rotate(-6deg);opacity:0}to{transform:none;opacity:1}}
.rd-lamp{position:absolute;left:50%;top:-34px;width:120%;height:60px;transform:translateX(-50%);background:radial-gradient(ellipse at 50% 0,rgba(255,243,196,.55),transparent 70%);pointer-events:none}
.rd-fr{position:relative;display:block;padding:5px;border-radius:12px;background:linear-gradient(160deg,#F3D27A,#B37A12);box-shadow:0 14px 24px -10px rgba(0,0,0,.7);animation:rdSway 3.2s ease-in-out infinite;transform-origin:50% -20px}
.rd-card:nth-child(2) .rd-fr{animation-delay:-1s}.rd-card:nth-child(3) .rd-fr{animation-delay:-2s}@keyframes rdSway{50%{transform:rotate(1.6deg)}}
.rd-fr img{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:8px}
html body #raid .rd-card b{display:block;margin-top:8px;font:900 .85rem Fraunces,serif;color:#fff!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}html body #raid .rd-card small{display:block;font:700 .68rem "Nunito Sans";color:#C9D6EE!important;white-space:nowrap}
html body #raid .rd-sc{position:absolute!important;top:10px!important;right:10px!important;left:auto!important;width:auto!important;padding:1px 7px;border-radius:99px;background:#FFFDF9;color:#2D2521;font:900 .78rem Fraunces,serif;font-style:normal;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.rd-tg{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;border:3px dashed #F3D27A;box-shadow:0 0 0 3px rgba(20,33,61,.45),0 0 18px rgba(243,210,122,.8);animation:rdTg 1.4s linear infinite}@keyframes rdTg{to{transform:rotate(360deg)}}
.rd-card.picked{animation:rdPick .6s cubic-bezier(.2,1.4,.4,1) forwards!important;z-index:2}@keyframes rdPick{to{transform:scale(1.18)}}.rd-card.gone{opacity:.15;transition:opacity .3s}
.rd-hint{margin:22px 0 0;font:800 .88rem "Nunito Sans";color:#C9D6EE}
.rd-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;width:100%;max-width:380px}.rd-vs figure{margin:0;transition:transform .2s}.rd-vs figure.hit{animation:rdHit .45s ease-out}@keyframes rdHit{30%{transform:scale(1.07)}}
.rd-ph{position:relative;display:block}.rd-ph img{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:16px;box-shadow:0 0 0 3px #E0A82E,0 12px 24px -10px rgba(0,0,0,.7)}.rd-vs .me .rd-ph img{box-shadow:0 0 0 3px #5B8DEF,0 12px 24px -10px rgba(0,0,0,.7)}
.rd-vs figcaption{margin-top:6px;font:900 .95rem Fraunces,serif}.rd-vs figcaption small{display:block;font:700 .75rem "Nunito Sans";color:#C9D6EE}
.rd-x{width:48px;height:48px;border-radius:50%;background:radial-gradient(circle,#FFE8A6,#E0A82E);color:#3A2600;font:900 1.05rem/48px Fraunces,serif;box-shadow:0 0 24px rgba(243,210,122,.8);animation:rdPulse 1s ease-in-out infinite}
.rd-dots{display:flex;gap:16px;margin:24px 0 6px}.rd-dots i{width:58px;height:58px;border-radius:50%;background:rgba(255,255,255,.1);box-shadow:inset 0 0 0 2px rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-style:normal;animation:rdPulse 1s ease-in-out infinite}
.rd-dots i b{font:900 1.5rem "Nunito Sans";color:#C9D6EE}.rd-dots i.w{background:#2E9A5C;box-shadow:0 0 22px rgba(46,154,92,.9);animation:rdDot .45s cubic-bezier(.2,1.6,.4,1)}.rd-dots i.l{background:#C8432F;box-shadow:0 0 22px rgba(200,67,47,.8);animation:rdDot .45s cubic-bezier(.2,1.6,.4,1)}.rd-dots i.w b,.rd-dots i.l b{color:#fff}
@keyframes rdDot{0%{transform:scale(.4)}100%{transform:none}}
html body #raid .rd-big{position:absolute!important;padding:0!important;border:0!important;background:rgba(12,21,41,.82)!important;border-radius:50%!important;width:96px!important;height:96px!important;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;justify-content:center;width:96px;height:96px;border-radius:50%;background:rgba(12,21,41,.82);box-shadow:0 0 0 4px #F3D27A,0 10px 24px rgba(0,0,0,.5)}
html body #raid .rd-big b{font:900 2.6rem/1 Fraunces,serif;color:#fff!important}html body #raid .rd-big small{color:#C9D6EE!important;font:800 .66rem "Nunito Sans";color:#C9D6EE;text-transform:uppercase;letter-spacing:.06em}
.rd-big.mine{box-shadow:0 0 0 4px #5B8DEF,0 10px 24px rgba(0,0,0,.5)}
.rd-big.hide b{color:#F3D27A;animation:rdPulse .6s ease-in-out infinite}.rd-big.shake{animation:rdBigShake .5s linear infinite}@keyframes rdBigShake{25%{transform:translate(-53%,-50%) rotate(-4deg)}75%{transform:translate(-47%,-50%) rotate(4deg)}}
.rd-big.show{animation:rdBigShow .7s cubic-bezier(.2,1.7,.4,1) both}@keyframes rdBigShow{0%{transform:translate(-50%,-50%) scale(2.8);opacity:0}60%{transform:translate(-50%,-50%) scale(.9);opacity:1}100%{transform:translate(-50%,-50%) scale(1.1)}}
html body #raid .rd-big.show.hi{background:#C8432F!important}html body #raid .rd-big.show.lo{background:#4E5D7A!important}html body #raid .rd-big.mine{background:#1F3157!important}
.rd-vs figure.win .rd-ph img{box-shadow:0 0 0 5px #F3D27A,0 0 40px rgba(243,210,122,.9)!important}.rd-vs figure.lose .rd-ph img{filter:grayscale(.7) brightness(.7)}
.rd-drum{margin:26px 0 0;font:800 1.1rem "Nunito Sans";color:#E6EDF8}.rd-drum b{font:900 1.6rem Fraunces,serif}.rd-drum b.ok{color:#F3D27A}.rd-drum b.no{color:#FFB4A6}
.rd-tally{display:flex;gap:12px;align-items:center;font:900 2.4rem Fraunces,serif;color:#fff;margin:6px 0 0}.rd-tally span{color:#C9D6EE}
.rd-dec{display:inline-block;color:#FFE8A6!important;font:900 1.2rem "Nunito Sans";animation:rdPulse .6s ease-in-out infinite}
.rd-prize{position:relative;width:min(190px,50%);margin:26px 0 8px;animation:rdPrize .8s cubic-bezier(.2,1.5,.4,1) both}@keyframes rdPrize{0%{transform:scale(.2) rotate(-200deg);opacity:0}70%{transform:scale(1.06) rotate(4deg);opacity:1}100%{transform:none;opacity:1}}
.rd-prize img{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:18px;box-shadow:0 0 0 4px #9AA6B5}#raid.lose .rd-prize img{filter:grayscale(.6)}
.rd-prize.w img{box-shadow:0 0 0 6px #E0A82E,0 0 60px rgba(243,210,122,.9)}
.rd-new{position:absolute;left:50%;bottom:-14px;transform:translateX(-50%);padding:5px 14px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .78rem "Nunito Sans";letter-spacing:.06em;font-style:normal;white-space:nowrap;box-shadow:0 6px 14px -6px rgba(0,0,0,.6)}
.rd-h{margin:30px 0 0;font:900 1.6rem Fraunces,serif;color:#fff}
#raid.lose .rd-ban{color:#E6EDF8;-webkit-text-stroke:1.5px #4E5D7A;text-shadow:0 5px 0 #4E5D7A,0 14px 30px rgba(0,0,0,.45);font-size:2.6rem}
html body #raid .rd-go{display:block;margin-top:22px;min-width:240px;min-height:54px;padding:0 24px!important;border:0!important;border-radius:999px!important;background:#FFFDF9!important;color:#1F3157!important;font:900 1.05rem "Nunito Sans"!important;box-shadow:0 8px 18px -8px rgba(0,0,0,.6)!important;animation:vfIn .4s cubic-bezier(.2,1.4,.4,1) .6s both}
.rd-conf{position:absolute;inset:0;pointer-events:none;overflow:hidden}.rd-conf i{position:absolute;top:-20px;width:9px;height:14px;border-radius:2px;animation:rdFall linear forwards}@keyframes rdFall{to{transform:translateY(110vh) rotate(720deg)}}
.rd-fly{position:absolute;z-index:85;object-fit:cover;border-radius:14px;box-shadow:0 0 0 4px #E0A82E,0 0 40px rgba(243,210,122,.9);pointer-events:none}
html body #vgGoal.vg-got{position:relative;overflow:hidden;box-shadow:0 0 0 3px #E0A82E,0 0 28px rgba(243,210,122,.8)!important;animation:vgBump .5s cubic-bezier(.2,1.6,.4,1)}@keyframes vgBump{40%{transform:scale(1.05)}}
.vg-new{position:absolute;inset:0;display:flex;align-items:center;gap:12px;padding:10px 12px;box-sizing:border-box;border-radius:inherit;background:linear-gradient(180deg,#FFF6DD,#F7DF9A);text-align:left;animation:vfIn .4s cubic-bezier(.2,1.4,.4,1)}
.vg-new img{width:58px;height:68px;flex:none;border-radius:10px;object-fit:cover;box-shadow:0 0 0 3px #E0A82E;animation:vgCard 1.2s ease-in-out infinite}@keyframes vgCard{50%{transform:rotate(-4deg) scale(1.05)}}
.vg-nt{flex:1;min-width:0}.vg-nt b{display:block;font:900 1.02rem/1.15 Fraunces,serif;color:#3A2600}.vg-nt small{display:block;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font:800 .78rem "Nunito Sans";color:#8A5A0A}
.vg-nc{flex:none;display:flex;flex-direction:column;align-items:center;padding:6px 10px;border-radius:12px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 1.25rem/1 Fraunces,serif;box-shadow:0 4px 10px -6px rgba(160,110,10,.8)}.vg-nc small{font:800 .62rem "Nunito Sans";margin-top:2px}
.vg-sh{position:absolute;top:0;bottom:0;left:-40%;width:35%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.75),transparent);transform:skewX(-18deg);animation:vgShine 1.6s ease-in-out infinite;pointer-events:none}@keyframes vgShine{to{left:120%}}
#vgGoal.vg-out .vg-new{opacity:0;transition:opacity .35s}
.rd-coin{position:absolute;top:-40px;width:30px;height:30px;animation:rdFall 2.2s ease-in forwards}.rd-coin svg{width:100%;height:100%}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('votefx ok')
