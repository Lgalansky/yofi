# Moves Skill 2 onto the Skill brand (25+ cream look): Nunito Sans + Fraunces, Skill colours, wallet pills,
# bottom nav, buttons; adds the Skill coin/cash fly-to-wallet and the Skill win pop (Collect -> fly).
# Usage (repo root, on skill-2): python3 build-skill2/brand.py && python3 build-skill2/build.py
import pathlib
p = pathlib.Path(__file__).resolve().parent / 'app.src.html'
s = p.read_text(encoding='utf-8')
if 'function fly(' in s: raise SystemExit('brand already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)

# fonts + tokens
rep('family=Fraunces:opsz,wght@9..144,700;9..144,800&family=Figtree:wght@500;600;700;800;900',
    'family=Fraunces:opsz,wght@9..144,700;9..144,800;9..144,900&family=Nunito+Sans:wght@400;600;700;800;900')
rep(':root{--bg:#F8F3EB;--card:#FFFFFF;--line:#E6DAC3;--ink:#22263A;--muted:#6A6458;--navy:#1F3157;--navy2:#2D4E86;--wine:#8E1F2F;--gold:#E9B52F;--goldlt:#FFF1C9;--cash:#2F7A4A;',
    ':root{--bg:#F8F3EB;--card:#FFFDF9;--line:#EADFCB;--ink:#382D29;--muted:#6F6258;--navy:#2D4E86;--navy2:#24406F;--wine:#9E2F2A;--gold:#E0A82E;--goldlt:#FBEFD2;--cash:#2E6B42;')
s = s.replace('Figtree', '"Nunito Sans"')
rep('font:16px/1.4 "Nunito Sans",system-ui', 'font:17px/1.45 "Nunito Sans",system-ui')
rep('h1,h2,h3{font-family:Fraunces,Georgia,serif;margin:0;letter-spacing:-.01em}',
    'h1,h2,h3{font-family:Fraunces,Georgia,serif;margin:0;letter-spacing:-.01em;color:#2D2521}h1{font-weight:900}')
rep('.logo{font:800 1.9rem/1 Fraunces,serif;color:var(--wine)}', '.logo{font:900 2.5rem/1 Fraunces,serif;color:var(--wine);letter-spacing:-.02em}')

# wallet: two Skill pills (green note + coin)
rep('''.wallet{margin-left:auto;display:flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;background:var(--card);font-weight:800}
.wallet span{display:flex;align-items:center;gap:6px;padding:6px 11px}.wallet span+span{border-left:1.5px solid var(--line)}
.wallet .cash{color:var(--cash)}.wallet .coin{color:#8A6400}''',
'''.wallet{margin-left:auto;display:flex;gap:6px}
.wp{display:flex;align-items:center;gap:6px;height:38px;padding:0 10px;border-radius:12px;background:#F4EDE0;box-shadow:inset 0 0 0 1.5px #CDBB98}
.wp b{font:800 1.12rem/1 Fraunces,serif;letter-spacing:-.01em}.wp.cash b{color:#2E6B42}.wp.coin b{color:#2E508A}
.wp .note{display:block;width:26px;height:17px}.wp .note svg,.note svg{width:100%;height:100%;display:block}.wp .coinic{width:22px;height:22px}''')
rep('<div class="wallet" aria-label="Wallet"><span class="cash" title="Demo cash">$<b id="wCash">0.00</b></span><span class="coin" title="Coins"><i class="coinic"></i><b id="wCoins">0</b></span></div>',
    '<div class="wallet" aria-label="Wallet"><span class="wp cash" title="Demo cash"><i class="note"></i><b id="wCash">$0.00</b></span><span class="wp coin" title="Coins"><i class="coinic"></i><b id="wCoins">0</b></span></div>')
COIN = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9.5' fill='%23E0A82E' stroke='%23A8761A' stroke-width='1.2'/%3E%3Ccircle cx='12' cy='12' r='6.3' fill='none' stroke='%23F6D67A' stroke-width='1.4'/%3E%3Cpath d='M12 8.2v7.6' stroke='%23A8761A' stroke-width='1.8' stroke-linecap='round'/%3E%3C/svg%3E\") center/contain no-repeat"
rep('.coinic{display:inline-block;width:1.05em;height:1.05em;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF3A8,#F3C447 55%,#C88A06);box-shadow:inset 0 -2px 0 rgba(0,0,0,.18);vertical-align:-.15em;flex:none}',
    '.coinic{display:inline-block;width:1.1em;height:1.1em;background:' + COIN + ';vertical-align:-.18em;flex:none}')

# bottom nav, buttons
rep('.tabs{position:fixed;left:0;right:0;bottom:0;z-index:6;background:var(--card);border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom)}',
    '.tabs{position:fixed;left:0;right:0;bottom:0;z-index:6;background:#F7F1E7;border-radius:22px 22px 0 0;box-shadow:0 -1px 0 #F3EBDD,0 -12px 30px -16px rgba(38,31,28,.8);padding:6px 8px max(8px,env(safe-area-inset-bottom))}')
rep('.tabs div{max-width:520px;margin:0 auto;display:flex}', '.tabs div{max-width:520px;margin:0 auto;display:flex;gap:4px}')
rep('.tabs button{flex:1;border:0;background:none;padding:9px 4px 11px;display:flex;flex-direction:column;align-items:center;gap:3px;font-weight:800;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}',
    '.tabs button{flex:1;border:0;background:none;border-radius:16px;padding:7px 4px 6px;display:flex;flex-direction:column;align-items:center;gap:2px;font-weight:800;font-size:.86rem;color:#463933}')
rep('.tabs svg{width:26px;height:26px}.tabs button[aria-current="page"]{color:var(--navy)}', '.tabs svg{width:25px;height:25px}.tabs button[aria-current="page"]{color:var(--navy);background:#E3EAF5}')
rep('.tabs button[aria-current="page"] span{position:relative}.tabs button[aria-current="page"] span::after{content:"";position:absolute;left:0;right:0;bottom:-5px;height:3px;border-radius:2px;background:var(--navy)}', '')
rep('.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:999px;padding:13px 18px;font-weight:800;background:var(--navy);color:#fff;min-height:48px}',
    '.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:14px;padding:13px 18px;font:800 1.08rem/1.15 Fraunces,Georgia,serif;background:var(--navy);color:#fff;min-height:48px;box-shadow:0 6px 16px rgba(45,78,134,.25)}\n.btn.cash{box-shadow:0 6px 16px rgba(46,107,66,.28)}.btn.ghost{box-shadow:none}')
rep('.apply{display:flex;align-items:center;justify-content:space-between;width:100%;border:0;border-radius:999px;background:var(--navy);color:#fff;padding:8px 8px 8px 22px;font-weight:800;font-size:1.15rem;min-height:60px}',
    '.apply{display:flex;align-items:center;justify-content:space-between;width:100%;border:0;border-radius:999px;background:var(--navy);color:#fff;padding:8px 8px 8px 22px;font:800 1.2rem Fraunces,serif;min-height:60px;box-shadow:0 6px 16px rgba(45,78,134,.25)}')

# pops: Skill celebrate look + win pop
rep('.pop{position:fixed;inset:0;z-index:40;display:grid;place-items:center;padding:20px;background:rgba(30,26,22,.62);animation:fade .2s}',
    '.pop{position:fixed;inset:0;z-index:40;display:grid;place-items:center;padding:20px 8px;background:rgba(38,31,28,.78);animation:fade .2s}')
i = s.index('.pbox{position:relative'); j = s.index('@keyframes fall{to{transform:translateY(560px) rotate(540deg);opacity:.2}}') + len('@keyframes fall{to{transform:translateY(560px) rotate(540deg);opacity:.2}}')
s = s[:i] + r'''.pbox{position:relative;width:min(100%,380px);max-height:calc(100vh - 24px);overflow:hidden auto;border-radius:30px;padding:30px 20px 18px;text-align:center;color:#302622;background:radial-gradient(80% 50% at 50% 30%,#EFE3CF,#F5EEE1 70%,#F7F2E8);box-shadow:0 0 0 2px #FFC93C,0 0 40px rgba(255,190,60,.45),0 30px 60px -20px rgba(38,31,28,.8);animation:pin .45s cubic-bezier(.2,1.4,.4,1)}
@keyframes pin{from{transform:scale(.8);opacity:0}}
.pbox .rays{position:absolute;left:50%;top:150px;width:620px;height:620px;margin:-310px 0 0 -310px;background:repeating-conic-gradient(rgba(255,214,120,.16) 0 9deg,transparent 9deg 22deg);animation:spin 18s linear infinite;pointer-events:none}
.pbox.wp .rays{animation-duration:16s;background:repeating-conic-gradient(rgba(255,201,60,.22) 0 9deg,transparent 9deg 22deg)}
@keyframes spin{to{transform:rotate(360deg)}}
.pbox>:not(.rays):not(.cf):not(.drop){position:relative;z-index:2}
.pbox h2{margin:4px 0 8px;font:900 clamp(1.7rem,7.6vw,2.15rem)/1.05 Fraunces,serif;color:#6A3500}
.pbox.wp h2{margin-top:24px;text-transform:uppercase}
.pbox .amt{font:900 2.4rem/1.1 Fraunces,serif;color:#E9A514;margin:4px 0}
.pbox p{margin:6px 0;color:#423530}.pbox p b{color:#2D2521}
.pbox .pimg{width:120px;height:120px;margin:10px auto 4px;border-radius:50%;box-shadow:0 0 0 4px #fff,0 0 0 8px #FFC93C}
.pbox .ribbon{display:inline-block;background:var(--navy);color:#fff;font:800 1.05rem Fraunces;padding:6px 16px;border-radius:8px;margin-top:-14px}
.pbox .trio{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0 6px}.pbox .trio .pic{aspect-ratio:3/4;box-shadow:0 0 0 3px #FFC93C}
.pbox .btn{width:100%;margin-top:12px}.pbox .btn.main{font-size:1.3rem;min-height:58px;text-transform:uppercase;border-radius:999px}
.pbox .btn.sec{background:none;box-shadow:none;color:var(--navy);text-decoration:underline;font:700 1rem "Nunito Sans",sans-serif;min-height:40px;margin-top:4px}
.cf{position:absolute;top:-16px;width:8px;height:13px;border-radius:2px;pointer-events:none;animation:fall 2.4s ease-in infinite}
@keyframes fall{0%{transform:translateY(0) rotate(0)}100%{transform:translateY(620px) rotate(600deg);opacity:.15}}
.drop{position:absolute;top:-40px;pointer-events:none;animation:drop 2.4s cubic-bezier(.45,0,.75,.6) infinite both}
.drop .coinic{width:30px;height:30px;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))}.drop .note{display:block;width:36px;height:23px;filter:drop-shadow(0 3px 4px rgba(0,0,0,.3))}
@keyframes drop{0%{transform:translateY(0) rotate(-20deg);opacity:0}10%{opacity:1}100%{transform:translateY(640px) rotate(220deg);opacity:0}}
.wp-photo{position:relative;width:150px;height:168px;margin:2px auto 0;animation:wppop .55s cubic-bezier(.2,1.5,.4,1) both}
.wp-photo .pic{width:100%;height:100%;border-radius:18px;box-shadow:0 0 0 4px #fff,0 0 0 8px #FFC93C,0 18px 30px -10px rgba(0,0,0,.6)}
.wp-badge{position:absolute;right:-16px;bottom:-14px;width:58px;height:58px;border-radius:50%;display:grid;place-items:center;font-size:1.7rem;background:radial-gradient(circle at 35% 30%,#FFF3A8,#FFC93C 55%,#E79A00);box-shadow:0 0 0 4px #fff,0 8px 18px -6px rgba(0,0,0,.6);animation:wppulse 1.6s ease-in-out infinite}
@keyframes wppop{from{transform:scale(.4);opacity:0}}@keyframes wppulse{50%{transform:scale(1.1)}}
.wp-amt{display:flex;align-items:center;justify-content:center;gap:8px;margin:2px 0 0!important;font:900 2.7rem/1.05 Fraunces,serif;color:#E9A514!important;text-shadow:0 2px 0 rgba(0,0,0,.12)}
.wp-amt.cash{color:#2E9A5C!important}.wp-amt .coinic{width:38px;height:38px}.wp-amt .note{display:block;width:40px;height:26px}
.wp-lbl{margin:4px 0 6px!important;font-size:.95rem}
/* fly to wallet (same motion as Skill) */
.fx{position:fixed;inset:0;pointer-events:none;z-index:60;overflow:hidden}
.fxp{position:absolute;filter:drop-shadow(0 4px 10px rgba(46,80,138,.45))}.fxp.c{filter:drop-shadow(0 4px 10px rgba(46,107,66,.5))}.fxp>*{width:100%!important;height:100%!important;display:block}
.fxbig{position:absolute;transform:translate(-50%,-50%);text-align:center;background:#F6F0E5;border-radius:26px;padding:14px 26px 12px;box-shadow:0 20px 50px -12px rgba(89,72,65,.55);animation:gpop 2.6s ease-out forwards;white-space:nowrap}
.fxbig b{display:flex;align-items:center;justify-content:center;gap:8px;font:800 3.2rem/1 Fraunces,serif;color:#2E508A}.fxbig.c b{color:#2E6B42}.fxbig b .coinic{width:40px;height:40px}.fxbig b .note{display:block;width:46px;height:30px}
.fxbig span{display:block;font-weight:700;margin-top:4px;color:#382D29}
@keyframes gpop{0%{opacity:0;transform:translate(-50%,-50%) scale(.3)}14%{opacity:1;transform:translate(-50%,-50%) scale(1.12)}24%{transform:translate(-50%,-50%) scale(1)}75%{opacity:1;transform:translate(-50%,-50%) scale(1)}100%{opacity:0;transform:translate(-50%,-75%) scale(.9)}}
.fxfloat{position:absolute;z-index:3;transform:translate(-50%,-50%);display:flex;align-items:center;gap:6px;padding:7px 15px 7px 7px;border-radius:999px;font:800 1.9rem/1 Fraunces,serif;color:#fff;background:linear-gradient(135deg,#2E6B42,#0D7A4B);box-shadow:0 0 0 3px rgba(46,107,66,.6),0 12px 30px rgba(46,107,66,.45);animation:gfloat 1.5s cubic-bezier(.3,1.3,.5,1) forwards;white-space:nowrap}
.fxfloat.noimg{padding-left:15px}.fxfloat img{width:36px;height:36px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #fff}.fxfloat .coinic{width:28px;height:28px}
@keyframes gfloat{0%{transform:translate(-50%,-50%) scale(.3);opacity:0}18%{transform:translate(-50%,-60%) scale(1.15);opacity:1}35%{transform:translate(-50%,-62%) scale(1)}80%{opacity:1}100%{transform:translate(-50%,-115%) scale(.95);opacity:0}}
.fxring{position:absolute;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;box-shadow:0 0 0 4px rgba(46,80,138,.6);animation:gring .7s ease-out forwards}@keyframes gring{to{transform:scale(5);opacity:0}}
.wp.bump{animation:bump .5s;box-shadow:inset 0 0 0 1.5px #2E508A,0 0 18px rgba(46,80,138,.6)}.wp.cash.bump{box-shadow:inset 0 0 0 1.5px #2E6B42,0 0 18px rgba(46,107,66,.6)}
@keyframes bump{40%{transform:scale(1.12)}}''' + s[j:]

# JS: wallet display that can lag behind the balance while coins are in the air
rep("function paint() { $('#wCash').textContent = (+S.cash).toFixed(2); $('#wCoins').textContent = Math.floor(S.coins).toLocaleString(); }",
r'''const NOTE = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="2" y="8" width="28" height="17" rx="3" fill="#21C77A"/><rect x="5" y="11" width="22" height="11" rx="2" fill="none" stroke="#0E8F55" stroke-width="1.5"/><circle cx="16" cy="16.5" r="4.2" fill="#FFD84D"/><path d="M16 14v5M17.4 14.9c-.4-.5-2.8-.7-2.8.6 0 1.4 2.8.7 2.8 2.1 0 1.2-2.4 1.1-2.9.5" stroke="#0E8F55" stroke-width="1.1" fill="none" stroke-linecap="round"/></svg>';
const noteIc = () => `<i class="note">${NOTE}</i>`;
const PEND = { coins: 0, cash: 0 };
function paint() { $('#wCash').textContent = money(Math.max(0, S.cash - PEND.cash)); $('#wCoins').textContent = Math.max(0, Math.round(S.coins - PEND.coins)).toLocaleString(); }
const hold = (cur, n) => { PEND[cur] += n; paint(); };
// coins or cash burst from a point and fly into the wallet pill, which counts up as each one lands (Skill gemExplosion/cashExplosion)
function fly(n, cur, o = {}) {
  if (!o.held) hold(cur, n);
  const pill = $(cur === 'cash' ? '.wp.cash' : '.wp.coin'), ic = pill && pill.querySelector('i');
  const release = v => { PEND[cur] = Math.max(0, PEND[cur] - v); if (PEND[cur] < .005) PEND[cur] = 0; paint(); };
  if (!(n > 0) || !ic || matchMedia('(prefers-reduced-motion: reduce)').matches || typeof Element.prototype.animate !== 'function') { release(n); return; }
  const ir = ic.getBoundingClientRect(), tx = ir.left + ir.width / 2, ty = ir.top + ir.height / 2;
  let ox = innerWidth / 2, oy = innerHeight * .42;
  if (o.at) { ox = o.at.x; oy = o.at.y; } else if (o.from && o.from.isConnected) { const r = o.from.getBoundingClientRect(); ox = r.left + r.width / 2; oy = r.top + r.height / 2; }
  const isC = cur === 'cash', icon = () => isC ? NOTE : '<i class="coinic"></i>', amt = isC ? '+' + money(n) : '+' + n.toLocaleString();
  const layer = document.createElement('div'); layer.className = 'fx'; layer.setAttribute('aria-hidden', 'true'); document.body.appendChild(layer);
  if (o.mid) { layer.insertAdjacentHTML('beforeend', `<i class="fxring" style="left:${ox}px;top:${oy}px"></i><div class="fxfloat${o.img ? '' : ' noimg'}" style="left:${ox}px;top:${oy}px">${o.img ? `<img src="${o.img}" alt="">` : ''}${amt}${isC ? noteIc() : '<i class="coinic"></i>'}</div>`); }
  else if (!o.small) layer.insertAdjacentHTML('beforeend', `<div class="fxbig${isC ? ' c' : ''}" style="left:${ox}px;top:${oy}px"><b>${amt}${isC ? noteIc() : '<i class="coinic"></i>'}</b><span>${esc(o.label || (isC ? 'cash added' : 'coins earned'))}</span></div>`);
  const count = o.small ? Math.min(8, Math.max(3, n)) : o.mid ? 12 : isC ? Math.min(18, Math.max(10, Math.round(n / 2))) : Math.min(30, Math.max(14, Math.round(n / 4)));
  let left = n, k = 0;
  for (let q = 0; q < count; q++) {
    const g = document.createElement('i'), sz = o.small ? rnd(14, 22) : o.mid ? rnd(18, 30) : rnd(22, 42);
    g.className = 'fxp' + (isC ? ' c' : ''); g.style.cssText = `left:${ox}px;top:${oy}px;width:${sz}px;height:${isC ? sz * .62 : sz}px;margin:${-(isC ? sz * .31 : sz / 2)}px 0 0 ${-sz / 2}px`; g.innerHTML = icon(); layer.appendChild(g);
    const a = Math.random() * Math.PI * 2, d = o.small ? rnd(28, 70) : o.mid ? rnd(60, 130) : rnd(80, 190), dx = Math.cos(a) * d, dy = Math.sin(a) * d * .85, rot = isC ? rnd(-40, 40) : rnd(-220, 220);
    const an = g.animate([
      { transform: 'translate(0,0) scale(.1) rotate(0deg)', opacity: 0 },
      { transform: `translate(${dx}px,${dy}px) scale(1.1) rotate(${rot}deg)`, opacity: 1, offset: o.small ? .3 : .28 },
      { transform: `translate(${dx * 1.05}px,${dy + 10}px) scale(1) rotate(${rot}deg)`, opacity: 1, offset: o.small ? .45 : .55 },
      { transform: `translate(${tx - ox}px,${ty - oy}px) scale(.3) rotate(${isC ? 0 : rot * 2}deg)`, opacity: .9 }
    ], { duration: (o.small ? 950 : o.mid ? 1350 : 1850) + q * (o.small ? 60 : o.mid ? 45 : 38), easing: 'cubic-bezier(.3,.6,.3,1)', fill: 'forwards' });
    an.onfinish = () => { g.remove(); k++; const step = k >= count ? left : n / count; left -= step; release(step); pill.classList.remove('bump'); void pill.offsetWidth; pill.classList.add('bump'); };
  }
  setTimeout(() => layer.remove(), o.small ? 2300 : o.mid ? 2700 : 4300);
}''')

# pop renderer: one design; win pops add the photo + trophy, falling coins/notes, the count-up and Collect -> fly
i = s.index("  el.innerHTML = `<div class=\"pbox\">${o.confetti"); j = s.index("  if (el.querySelector('[data-pa=\"later\"]'))")
s = s[:i] + r'''  const w = o.win, isC = w && w.cur === 'cash', wic = isC ? noteIc() : '<i class="coinic"></i>', show = v => isC ? money(v) : Math.round(v).toLocaleString();
  el.innerHTML = `<div class="pbox${w ? ' wp' : ''}"><i class="rays" aria-hidden="true"></i>
    ${o.confetti || w ? [...Array(26)].map((_, i) => `<i class="cf" style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A', '#F59E0B'][i % 5]};animation-delay:${(i * .09).toFixed(2)}s;animation-duration:${(2.1 + (i % 5) * .3).toFixed(2)}s"></i>`).join('') : ''}
    ${w ? [...Array(12)].map((_, i) => `<span class="drop" style="left:${(i * 61 + 7) % 92}%;animation-delay:${(.15 + i * .17).toFixed(2)}s">${wic}</span>`).join('') : ''}
    ${w ? `<div class="wp-photo">${o.img ? pic(o.img) : ''}<span class="wp-badge" aria-hidden="true">🏆</span></div>` : ''}
    <h2>${o.title}</h2>
    ${w ? `<p class="wp-amt${isC ? ' cash' : ''}"><span>+<span class="wpN">${show(0)}</span></span>${wic}</p><p class="wp-lbl">${esc(w.label)} · ${isC ? 'added to your cash' : 'added to your coins'}</p>` : ''}
    ${!w && o.amt ? `<div class="amt">${o.amt}</div>` : ''}${o.trio ? `<div class="trio">${o.trio.map(p => pic(p)).join('')}</div>` : ''}
    ${!w && o.img ? pic(o.img, { cls: 'pimg' }) : ''}${o.ribbon ? `<div class="ribbon">${o.ribbon}</div>` : ''}${o.text ? `<p>${o.text}</p>` : ''}
    <button class="btn main" data-pa="go">${o.cta || (w ? (isC ? 'Collect my cash' : 'Collect my coins') : 'OK')}</button>${o.later ? `<button class="btn sec" data-pa="later">${o.later}</button>` : ''}</div>`;
  document.body.appendChild(el); setTimeout(() => el.querySelector('[data-pa="go"]').focus(), 60);
  if (w) { const nEl = el.querySelector('.wpN'), t0 = performance.now(); const tick = t => { if (!nEl.isConnected) return; const k = Math.min(1, (t - t0) / 1100); nEl.textContent = show(w.amt * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); };
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) nEl.textContent = show(w.amt); else requestAnimationFrame(tick); }
  let shut = false; const close = f => { if (shut) return; shut = true; el.remove(); if (w) setTimeout(() => fly(w.amt, w.cur, { held: 1, label: w.label }), 80); if (o.fly) setTimeout(() => fly(o.fly.n, o.fly.cur, { held: 1, label: o.fly.label }), 80); if (f) f(); setTimeout(nextPop, w || o.fly ? 1200 : 350); };
  el.querySelector('[data-pa="go"]').onclick = () => close(o.go);
''' + s[j:]

# voting: +2 for judging flies from your pick; a pick of your photo flies from your goal photo; streak gift flies from the gift
rep("  if (V.busy || V.res) return; V.busy = true;\n  const p = V.pair,",
    "  if (V.busy || V.res) return; V.busy = true;\n  const pb = document.querySelector(`[data-vote=\"${i}\"]`), pr = pb && pb.getBoundingClientRect(), at = pr && { x: pr.left + pr.width / 2, y: pr.top + pr.height * .45 };\n  const p = V.pair,")
rep("  if (S.photos.length && Math.random() < .45) receive(S.photos[rnd(0, S.photos.length - 1)].id, true);\n  V.res = { side: i, hit }; save(); render();",
    "  let picked = null; if (S.photos.length && Math.random() < .45) { const ph = S.photos[rnd(0, S.photos.length - 1)]; picked = { p: ph, m: receive(ph.id) }; hold('coins', picked.m); }\n  hold('coins', CFG.JUDGE); if (gift) hold('coins', gift.c);\n  V.res = { side: i, hit }; save(); render();\n  fly(CFG.JUDGE, 'coins', { held: 1, small: 1, at });\n  if (picked) setTimeout(() => fly(picked.m, 'coins', { held: 1, mid: 1, img: srcOf(picked.p), from: document.querySelector('.goal .pic') }), 550);")
rep("    if (gift) { const tp = target(); pop({ title: 'Streak reward', amt: `+${gift.c} coins`, img: nowAfford && !couldAfford ? tp : null, ribbon: nowAfford && !couldAfford ? `${esc(tp.name)}’s upgrade is ready` : '', confetti: 1, cta: nowAfford && !couldAfford ? 'View upgrade' : 'Keep voting', go: nowAfford && !couldAfford ? () => openImprove(tp.id) : null, later: nowAfford && !couldAfford ? 'Keep voting' : '' }); }",
    "    if (gift) { const tp = target(), up = nowAfford && !couldAfford;\n      if (up) pop({ title: 'Streak reward', amt: `+${gift.c} coins`, img: tp, ribbon: `${esc(tp.name)}’s upgrade is ready`, confetti: 1, cta: 'View upgrade', go: () => openImprove(tp.id), later: 'Keep voting', fly: { n: gift.c, cur: 'coins', label: 'Streak reward' } });\n      else fly(gift.c, 'coins', { held: 1, label: `Streak reward · ${gift.n} in a row`, from: document.querySelector('.streak .gift') }); }")
rep("  if (quiet) toast(`Someone picked ${p.name} · +${m} coins`); return m;", "  return m;")

# cash wins: Skill win pop, cash held until Collect
rep("S.cash += prize; S.results.push(`${mp.name} ${won ? 'beat' : 'lost to'}", "S.cash += prize; hold('cash', prize); S.results.push(`${mp.name} ${won ? 'beat' : 'lost to'}")
rep("      if (won) pop({ title: 'You win!', img: mp, amt: `+${money(prize)}`, confetti: 1, text: `${esc(mp.name)} beat ${esc(i.oname)} ${m}–${t}.`, cta: 'Collect' });",
    "      if (won) pop({ title: 'You win!', img: mp, win: { amt: prize, cur: 'cash', label: `${mp.name} beat ${i.oname} ${m}–${t}` } });")
rep("if (won) { const pot = ch.pot; S.cash += pot;", "if (won) { const pot = ch.pot; S.cash += pot; hold('cash', pot);")
rep("        if (won) pop({ title: 'New champion!', img: mp, amt: `+${money(ch.pot)}`, confetti: 1, text: `${esc(mp.name)} took the ${catName(ch.cat)} crown.`, cta: 'Collect' });",
    "        if (won) pop({ title: 'New champion!', img: mp, win: { amt: ch.pot, cur: 'cash', label: `${catName(ch.cat)} champion pot` } });")
rep("t.won = prize; S.cash += prize;", "t.won = prize; S.cash += prize; hold('cash', prize);")
rep("      if (prize) pop({ title: place === 1 ? 'You win the ' + nm + '!' : `${ord(place)} place`, img: mp, amt: `+${money(prize)}`, confetti: place === 1, cta: 'Collect' });",
    "      if (prize) pop({ title: place === 1 ? 'You win!' : `${ord(place)} place!`, img: mp, win: { amt: prize, cur: 'cash', label: `${nm} ${place === 1 ? 'win' : 'prize'}` } });")

# away earnings: held until the pop closes, then fly
rep("  S.credited = batch.id; save(); paint(); if (!tot) return;", "  S.credited = batch.id; hold('coins', tot); save(); if (!tot) return;")
rep("cta: 'View gallery', go: () => { S.tab = 'gallery'", "fly: { n: tot, cur: 'coins', label: 'Earned while you were away' }, cta: 'View gallery', go: () => { S.tab = 'gallery'")

# wallet SVG note inserted at boot
rep("S = load() || fresh(); roll();", "document.querySelector('.wp.cash .note').innerHTML = NOTE;\nS = load() || fresh(); roll();")
p.write_text(s, encoding='utf-8'); print('brand ok')
