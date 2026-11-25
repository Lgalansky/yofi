# Winner pop for every challenge win: confetti, falling coins (or notes for cash), the winning photo,
# the prize counting up, then one "Collect" button that flies the coins/cash into the balance.
# Usage: python3 build-skill/winpop.py [in.html] [out.html]  (defaults to index.html in place)
import re, sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src; s = open(src, encoding='utf-8').read()
if 'function winPop(' in s: sys.exit('winpop already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)

JS = r'''
// one celebration for every challenge win; the coins/cash fly to the balance when the player collects
function winPop(amt, cur, label, o = {}) {
  const boom = () => cur === 'cash' ? cashExplosion(amt, { label }) : gemExplosion(amt, { label });
  const c = $('#coach');
  if (!amt || amt <= 0 || !c || c.classList.contains('on')) { boom(); return; }
  const src = o.src || (document.querySelector('#sheetBody .kg2-ph.me img, #sheetBody .pc-vs figure.won img, #sheetBody .won img, #flow .kg2-ph.me img') || {}).src;
  const isCash = cur === 'cash', show = v => isCash ? money(v) : Math.round(v).toLocaleString();
  const ic = isCash ? '<span class="wp-bill">$</span>' : gemIcon('wp-ci');
  const title = o.title || (/prize/i.test(label) ? 'Prize won!' : 'You win!');
  c.innerHTML = `<div class="crbox wpbox" role="dialog" aria-modal="true" aria-labelledby="wpT">
    <div class="cr-rays wp-rays" aria-hidden="true"></div>
    ${[...Array(26)].map((_, i) => `<i class="wp-cf" style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A', '#F59E0B'][i % 5]};animation-delay:${(i * .09).toFixed(2)}s;animation-duration:${(2.1 + (i % 5) * .3).toFixed(2)}s"></i>`).join('')}
    ${[...Array(12)].map((_, i) => `<span class="wp-drop" style="left:${(i * 61 + 7) % 92}%;animation-delay:${(.15 + i * .17).toFixed(2)}s">${ic}</span>`).join('')}
    ${src ? `<div class="wp-photo"><img src="${src}" alt="Your photo"><span class="wp-badge">🏆</span></div>` : '<div class="wp-trophy" aria-hidden="true">🏆</div>'}
    <h2 id="wpT">${esc(title)}</h2>
    <p class="wp-amt ${isCash ? 'cash' : ''}"><span>+<span id="wpN">${show(0)}</span></span>${ic}</p>
    <p class="wp-lbl">${esc(label)} · ${isCash ? 'added to your cash' : 'added to your coins'}</p>
    <button class="bt-cta" id="wpGo">${isCash ? 'Collect my cash' : 'Collect my coins'}</button></div>`;
  c.classList.add('on', 'cr');
  const el = $('#wpN'), t0 = performance.now(), D = 1100;
  const tick = now => { if (!el.isConnected) return; const k = Math.min(1, (now - t0) / D); el.textContent = show(amt * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) el.textContent = show(amt); else requestAnimationFrame(tick);
  let done = false; const close = () => { if (done) return; done = true; c.classList.remove('on', 'cr'); c.innerHTML = ''; setTimeout(boom, 80); };
  $('#wpGo').onclick = close; c.onclick = e => { if (e.target === c) close(); };
}
'''
rep('function celebrate({ src, score, title, text, cta, onCta, later, onLater }) {', JS + 'function celebrate({ src, score, title, text, cta, onCta, later, onLater }) {')

# every challenge win goes through the pop
for a, b in [
  ("if (won && !opt.revenge) setTimeout(() => gemExplosion(prize, { label: 'Coin challenge win' }), 300);", "if (won && !opt.revenge) setTimeout(() => winPop(prize, 'gems', 'Coin challenge win'), 500);"),
  ("if (won) setTimeout(() => cashExplosion(prize, { label: 'Head-to-head win' }), 300);", "if (won) setTimeout(() => winPop(prize, 'cash', 'Head-to-head win'), 500);"),
  ("if (rivWon) cashExplosion(rivWon, { label: 'Rivalry pot' }); paintWallet(); } else if (c.stake.cur === 'cash') { cashExplosion(prize, { label: 'Friend challenge' }); paintWallet(); } else gemExplosion(prize + bonus, { label: 'Friend challenge' }); }, 300);",
   "if (rivWon) winPop(rivWon, 'cash', 'Rivalry pot'); paintWallet(); } else if (c.stake.cur === 'cash') { winPop(prize, 'cash', 'Friend challenge'); paintWallet(); } else winPop(prize + bonus, 'gems', 'Friend challenge'); }, 500);"),
  ("gemExplosion(FR_GEM * 2, { label: '🟡 Coin challenge won' }); }, 9000);", "winPop(FR_GEM * 2, 'gems', 'Coin challenge won'); }, 9000);"),
  ("if (won && !pr) setTimeout(() => cashExplosion && cashExplosion(pay, { label: 'Quick Sprint' }), 400);", "if (won && !pr) setTimeout(() => winPop(pay, 'cash', 'Quick Sprint win'), 500);"),
  ("try { cashExplosion(FC_PRIZE, { label: 'Free cash ' + CH }); } catch (e) {}", "try { winPop(FC_PRIZE, 'cash', 'Free cash ' + CH); } catch (e) {}"),
  ("setTimeout(() => cashExplosion(pot, { label: `${catLabel(cat)} bounty` }), 300);", "setTimeout(() => winPop(pot, 'cash', `${catLabel(cat)} bounty`), 500);"),
  ("setTimeout(() => cashExplosion(prize, { label: 'Showdown win' }), 300);", "setTimeout(() => winPop(prize, 'cash', 'Showdown win'), 500);"),
  ("setTimeout(() => cashExplosion(R0.amt, { label: won ? 'Tournament win' : 'Tournament prize' }), 300);", "setTimeout(() => winPop(R0.amt, 'cash', won ? 'Tournament win' : 'Tournament prize'), 500);"),
]:
    rep(a, b)

CSS = r'''
.wpbox{position:relative;overflow:hidden;text-align:center}
.wpbox .wp-rays{animation:wpspin 16s linear infinite!important;opacity:1}
@keyframes wpspin{to{transform:rotate(360deg)}}
.wp-cf{position:absolute;top:-16px;width:8px;height:13px;border-radius:2px;z-index:1;pointer-events:none;animation:wpfall 2.4s ease-in infinite}
@keyframes wpfall{0%{transform:translateY(0) rotate(0)}100%{transform:translateY(620px) rotate(600deg);opacity:.15}}
.wp-drop{position:absolute;top:-40px;z-index:1;pointer-events:none;animation:wpdrop 2.4s cubic-bezier(.45,0,.75,.6) infinite both}
.wp-drop .wp-ci{width:30px;height:30px;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))}
@keyframes wpdrop{0%{transform:translateY(0) rotate(-20deg);opacity:0}10%{opacity:1}100%{transform:translateY(640px) rotate(220deg);opacity:0}}
.wp-bill{display:inline-grid;place-items:center;width:34px;height:22px;border-radius:4px;background:linear-gradient(180deg,#5FD18E,#2E9A5C);color:#fff;font:900 .9rem/1 system-ui,sans-serif;box-shadow:0 3px 6px rgba(0,0,0,.3);vertical-align:middle}
.wpbox > :not(.wp-rays):not(.wp-cf):not(.wp-drop){position:relative;z-index:2}
.wp-photo{position:relative;width:150px;height:168px;margin:6px auto 0;animation:wppop .55s cubic-bezier(.2,1.5,.4,1) both}
.wp-photo img{width:100%;height:100%;object-fit:cover;border-radius:18px;box-shadow:0 0 0 4px #fff,0 0 0 8px #FFC93C,0 18px 30px -10px rgba(0,0,0,.6)}
.wp-badge{position:absolute;right:-16px;bottom:-14px;width:58px;height:58px;border-radius:50%;display:grid;place-items:center;font-size:1.7rem;background:radial-gradient(circle at 35% 30%,#FFF3A8,#FFC93C 55%,#E79A00);box-shadow:0 0 0 4px #fff,0 8px 18px -6px rgba(0,0,0,.6);animation:wppulse 1.6s ease-in-out infinite}
.wp-trophy{font-size:4.2rem;line-height:1;margin:8px 0 0;animation:wppop .55s cubic-bezier(.2,1.5,.4,1) both}
@keyframes wppop{from{transform:scale(.4);opacity:0}}
@keyframes wppulse{50%{transform:scale(1.1)}}
.wpbox h2{margin-top:24px!important}
.wp-amt{display:flex;align-items:center;justify-content:center;gap:8px;margin:2px 0 0!important;font:900 2.6rem/1.05 "Archivo Black","Arial Black",sans-serif!important;color:#E9A514!important;text-shadow:0 2px 0 rgba(0,0,0,.18)}
.wp-amt.cash{color:#2E9A5C!important}
.wp-amt .wp-ci{width:38px;height:38px}
.wp-lbl{margin:4px 0 14px!important;font-size:.95rem!important;opacity:.85}
@media (prefers-reduced-motion:reduce){.wp-cf,.wp-drop{display:none}.wpbox .wp-rays,.wp-badge,.wp-photo,.wp-trophy{animation:none!important}}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('winpop ok')
