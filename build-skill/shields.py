# Skill preview: stealing, part 2 (user chose A for both).
#  1. Stolen cards are trophies. They no longer fill a collection's 3 Gold slots (collections need your own photos);
#     they show in a "🃏 Trophies" row on their collection's binder page and still earn coins on every vote.
#  2. Shields are earned, never bought, and you choose which card they protect.
#     Earn: only from the special tile while voting (hold up to 3). Streaks and judge ranks don't give shields (user decision).
#     Use: tap the 🛡 pill (or the Gallery's "🛡 Shield Milo" chip) and put a shield on a card. An overnight steal
#     that targets a shielded card is blocked and the shield breaks ("Your shield stopped Emma stealing Milo").
#     Shields you haven't placed no longer block anything. Shielded cards show 🛡 in the Gallery.
#     See it: every steal wall has one rival card behind a glowing blue shield ("🛡 Shielded"); tapping it bounces
#     off, and the hint line explains "Shielded cards can't be stolen · shields from special tiles protect yours too".
# Usage: python3 build-skill/shields.py in.html out.html  (run after signup.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
a = "const ph = S.photos.filter(p => p.cat === c && p.s && !p.heldBy)"
assert s.count(a) == 1
s = s.replace(a, "const ph = S.photos.filter(p => p.cat === c && p.s && !p.heldBy && !p.card)")
JS = r'''
// ---- shields you place, trophies for stolen cards ----
(() => {
  const shPlaced = () => S.photos.filter(p => p.shield && !p.heldBy);
  const shTarget = () => { const c = riskable().filter(p => !p.shield); return c.sort((a, b) => b.s.total - a.s.total)[0] || null; };
  const shPut = p => { if (!p || !(S.shields > 0)) return; S.shields--; p.shield = 1; save(); try { vfShPaint(); } catch (e) {} toast(`🛡 ${alName(p)} is shielded · it blocks one steal`); try { renderStudio(); } catch (e) {} };
  window.__shPut = shPut;
  function shSheet() { const n = S.shields || 0, on = shPlaced(), t = shTarget();
    openSheet(`<div class="shs"><h2 class="shs-h">🛡 Shields</h2><p class="shs-p">A shield on a card blocks one steal while you’re away, then breaks.</p>
      <div class="shs-row"><b>${n}</b><span>ready to use<small>Hold up to ${VF_MAXSH}</small></span></div>
      ${on.length ? `<div class="shs-on">${on.map(p => `<span><img src="${p.src}" alt="">🛡 ${esc(alName(p))}</span>`).join('')}</div>` : ''}
      <p class="shs-earn">Win shields from ✨ special tiles while you vote.</p>
      ${n && t ? `<button class="btn block shs-go" id="shGo">🛡 Shield ${esc(alName(t))}</button><div style="text-align:center"><button class="link" data-shclose>Not now</button></div>` : `<button class="btn block shs-go" data-shclose>Keep voting</button>`}</div>`);
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
    if ($('#shGo')) $('#shGo').onclick = () => { closeSheet(); shPut(t); }; }
  window.__shSheet = shSheet;
  const _pt = vfShPaint;
  vfShPaint = function () { _pt.apply(this, arguments); const b = $('#vfSh'); if (!b) return; const n = (S.shields || 0) + shPlaced().length;
    b.hidden = !n; const h = `🛡<b>${n}</b>`; if (b.innerHTML !== h) b.innerHTML = h; b.onclick = shSheet; b.setAttribute('aria-label', `Shields: ${S.shields || 0} ready, ${shPlaced().length} in use`); };
  // an overnight steal: blocked only if the card it targets carries a shield
  const _sa = stealAway;
  stealAway = function (force) { if (!S.user) return _sa.apply(this, arguments);
    const now = Date.now(), last = S.lastSeen || now, away = now - last;
    if ((force || away >= 2 * 36e5) && !S.photos.some(p => p.heldBy)) { const cards = riskable();
      if (cards.length) { const p = cards.slice().sort((a, b) => hsh(a.id + todayKey()) - hsh(b.id + todayKey()))[0];
        if (p.shield) { const r = RIVALS[hsh(p.id + now) % RIVALS.length]; p.shield = 0; S.lastSeen = now;
          S.awayNews = { coins: Math.floor(S.vgJar || 0), st: null, blocked: { h: r.h, nm: alName(p) }, at: now }; save(); try { vfShPaint(); } catch (e) {} return; } } }
    const k = S.shields; S.shields = 0; try { return _sa.apply(this, arguments); } finally { S.shields = k; save(); } };
  // Gallery: shielded badge, trophies row, "Shield Milo" chip
  function shGal() { const st = document.querySelector('#studio'); if (!st) return; const page = st.querySelector('.gs-page'); if (!page) return;
    st.querySelectorAll('.a2-sl[data-alc]').forEach(b => { const p = S.photos.find(x => x.id === b.dataset.alc); const has = b.querySelector('.sh-bdg');
      if (p && p.shield && !has) { const ph = b.querySelector('.a2-ph') || b; ph.insertAdjacentHTML('beforeend', '<i class="sh-bdg" title="Shielded">🛡</i>'); } else if (p && !p.shield && has) has.parentNode.removeChild(has); });
    const c = S.galCat, tro = S.photos.filter(p => p.card && !p.heldBy && p.s && (!c || p.cat === c)), sig = tro.map(p => p.id).join(',') + '|' + (S.shields || 0);
    let row = page.querySelector('.tro-row'); if (row && row.dataset.sig === sig) return; if (row) row.parentNode.removeChild(row);
    const t = shTarget(), chip = (S.shields || 0) > 0 && t ? `<button class="sh-chip" data-shput="${t.id}">🛡 Shield ${esc(alName(t))}</button>` : '';
    if (!tro.length && !chip) return;
    page.insertAdjacentHTML('beforeend', `<div class="tro-row" data-sig="${sig}">${tro.length ? `<div class="tro-in"><span class="tro-ims">${tro.slice(0, 3).map(p => `<img src="${p.src}" alt="">`).join('')}</span><span class="tro-tx"><b>🃏 Trophies · ${tro.length} stolen card${tro.length === 1 ? '' : 's'}</b><small>Earn ${tro.map(p => GAL.BASE * galMult(p.s.total)).reduce((a, b) => a + b, 0)} coins a vote</small></span></div>` : ''}${chip}</div>`);
    const b = page.querySelector('[data-shput]'); if (b) b.onclick = e => { e.stopPropagation(); shPut(S.photos.find(x => x.id === b.dataset.shput)); }; }
  new MutationObserver(() => { try { shGal(); } catch (e) {} }).observe($('#studio'), { childList: true, subtree: true });
  // steal wall: some rival cards carry a shield and can't be picked
  new MutationObserver(() => { try { const el = document.getElementById('raid'); if (!el || el.dataset.shd) return; const cs = [...el.querySelectorAll('.rd-card[data-rd]')]; if (cs.length < 3) return; el.dataset.shd = 1;
    { const c = cs[Math.floor(Math.random() * cs.length)]; const hn = el.querySelector('.rd-hint'); if (hn) hn.insertAdjacentHTML('beforeend', '<br><b class="rd-shn">🛡 Shielded cards can’t be stolen · shields from ✨ special tiles protect yours too</b>'); c.classList.add('rd-shd'); const sm = c.querySelector('small'); if (sm) sm.textContent = '🛡 Shielded';
      const fr = c.querySelector('.rd-fr'); if (fr) fr.insertAdjacentHTML('beforeend', '<i class="rd-shb">🛡</i>'); c.onclick = e => { e.stopPropagation(); c.classList.remove('rd-bonk'); void c.offsetWidth; c.classList.add('rd-bonk'); toast(`🛡 ${(c.querySelector('b') || {}).textContent || 'That card'} is shielded · pick another`); }; } } catch (e) {} }).observe($('#shell'), { childList: true });
  // a blocked steal with nothing else to report still gets its own moment
  const _ap = awayPop;
  awayPop = function () { const N = S.awayNews;
    if (N && !N.shown && N.blocked && !N.st && !Math.floor(S.vgJar || 0) && S.user && $('#panes').dataset.at === 'judge' && !$('#coach').classList.contains('on') && !$('#sheet').classList.contains('on') && !$('#flow').classList.contains('on')) {
      N.shown = 1; save(); const p = S.photos.find(x => alName(x) === N.blocked.nm) || S.photos[0] || {};
      celebrate({ src: p.src || '', score: '🛡', title: 'Shield held!', text: `<b>${esc(rvName(N.blocked.h))}</b> tried to steal <b>${esc(N.blocked.nm)}</b> while you were away. Your shield stopped it and broke.`, cta: 'Back to voting', onCta: () => {} }); return; }
    return _ap.apply(this, arguments); };
  setTimeout(() => { try { vfShPaint(); } catch (e) {} }, 500);
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
html body #sheetBody .shs{text-align:left;color:#14213D}.shs-h{margin:2px 0 6px!important;text-align:center;font:900 1.8rem Fraunces,Georgia,serif!important;color:#14213D!important}
.shs-p{margin:0 0 12px;text-align:center;font-size:.95rem;color:#4E433C}.shs-row{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:16px;background:#FBF6EC;box-shadow:inset 0 0 0 1.5px #D9B467}
.shs-row b{font:900 2.2rem/1 Fraunces,Georgia,serif;color:#14213D}.shs-row span{font:800 1rem "Nunito Sans",sans-serif}.shs-row small{display:block;font-weight:600;font-size:.8rem;color:#6B5B4B}
.shs-on{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 0}.shs-on span{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 4px;border-radius:999px;background:#EEF2FA;font:800 .85rem "Nunito Sans",sans-serif;color:#24406F}.shs-on img{width:28px;height:28px;border-radius:50%;object-fit:cover}
.shs-earn{margin:12px 0 14px;font-size:.88rem;color:#4E433C;text-align:center}html body #sheetBody .shs .shs-go{background:#14213D!important;color:#fff!important;font-family:"Nunito Sans",sans-serif!important}
.sh-bdg{position:absolute;top:6px;left:6px;z-index:3;display:grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#FFF6DA;font-style:normal;font-size:.85rem;box-shadow:0 0 0 2px #D9AE4F,0 2px 5px rgba(0,0,0,.3)}
.tro-row{margin-top:10px;display:flex;flex-direction:column;gap:8px}.tro-in{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:12px;background:#FFF6DA;box-shadow:inset 0 0 0 1.5px #E0B860}
.tro-ims{display:flex}.tro-ims img{width:40px;height:40px;border-radius:8px;object-fit:cover;box-shadow:0 0 0 2px #B3261E;margin-right:-8px}.tro-tx{margin-left:10px;min-width:0}.tro-tx b{display:block;font:800 .88rem "Nunito Sans",sans-serif;color:#6A3500}.tro-tx small{font-size:.76rem;color:#6B5B4B}
html body .sh-chip{align-self:center;border:0;border-radius:999px;padding:8px 16px;background:#14213D;color:#fff;font:800 .9rem "Nunito Sans",sans-serif;cursor:pointer}
#raid .rd-card.rd-shd{opacity:.7;filter:grayscale(.35)}#raid .rd-card.rd-shd .rd-fr{box-shadow:0 0 0 3px #8FB6EE,0 0 18px rgba(143,182,238,.8)!important}#raid .rd-card.rd-bonk{animation:rdBonk .45s}@keyframes rdBonk{20%{transform:translateX(-8px) rotate(-3deg)}50%{transform:translateX(8px) rotate(3deg)}80%{transform:translateX(-4px)}}#raid .rd-shn{display:inline-block;margin-top:6px;color:#BFD6FF;font-weight:800}#raid .rd-shb{position:absolute;top:8px;right:8px;z-index:3;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;background:#14213D;font-style:normal;box-shadow:0 0 0 2px #D9AE4F}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('shields ok')
