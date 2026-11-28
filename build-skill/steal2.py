# Skill preview: batch of user changes.
#  1. Compete has one list (the Judge games tab is gone): Daily jackpots, Tournaments (Photo Knockout, Showdown),
#     then Quick games (Photo Duel · Judge Duel · Friend). Crowd Championship was removed (user decision).
#  2. A missed vote says how many agreed with you: "Missed it · 38% picked this one too" (was "62% picked the other").
#  3. Steal wall: no shields shown on the three cards. About 1 in 3 steals, the card you pick turns out to be shielded:
#     it bounces, a shield slams on it, "Sorry, Hilltop village is shielded", and nothing is stolen. Then a sheet offers
#     to shield your best photo ("🛡 Shield Milo" if you have a shield, otherwise how to win one).
#  4. An unopened special tile hides when you leave Vote (it used to float over Compete and Gallery).
#  5. You can only steal from collections you have a photo in (user's idea, option A). Nothing shows up front: pick a
#     card from a collection you haven't started and it's revealed like a shield (shake, 🔒 slams on, "Add a travel photo
#     to steal this"), then a sheet: "Infinity sunset is in Travel" · "📷 Add a travel photo" · "Back to voting".
#     Every wall has at least one card you can steal; surprise shields only land on those.
#  6. The Gallery's next-collection tile shows the reward for filling this one: "🎟️ Free $1 entry · opens at Gold"
#     (filling a collection to Gold already paid a free $1 cash entry and opened the next one; now the tile says so).
# Usage: python3 build-skill/steal2.py in.html out.html  (run after winback.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
def R(a, b):
    global s
    assert s.count(a) == 1, (a[:60], s.count(a)); s = s.replace(a, b)
R("<small>${100 - mine}% picked the other one", "<small>${mine}% picked this one too")
R("${nxOpen ? \'Open now\' : \'Opens at Gold\'}", "${nxOpen ? \'Open now\' : \'🎟️ Free $1 entry · opens at Gold\'}")
R("wall = pool.sort(() => Math.random() - .5).slice(0, 3).map(x => ({ ...x, h: rv.h }));",
  "wall = (() => { const ok = c => S.photos.some(p => p.s && !p.card && !p.heldBy && p.cat === c), sh = pool.sort(() => Math.random() - .5), a = sh.filter(x => ok(x.cat)), b = sh.filter(x => !ok(x.cat));"
  " if (!a.length) return sh.slice(0, 3); return [a[0], ...[...a.slice(1), ...b].sort(() => Math.random() - .5).slice(0, 2)].sort(() => Math.random() - .5); })().map(x => ({ ...x, h: rv.h })); window.__rdWall = wall;")
JS = r'''
// ---- one Compete list ----
(() => { C2 = 'photo'; S.cmpTab = 'photo';
  const _cp = c2Photo;
  c2Photo = function () { const h = _cp.apply(this, arguments);
    try { const t = document.createElement('div'); t.innerHTML = h; const rows = t.querySelectorAll('.c4-t'), last = rows[rows.length - 1];
      let win = ''; try { const nx = chId() + 1; win = `Win $${Math.round(chPool(chPlayers(nx, nx * CH_MS)) * .1).toLocaleString()}`; } catch (e) { win = 'Top 20% paid'; }
      const row = `<button class="c4-t" data-c2r="crowd"><span class="c4-ti">👥</span><span class="c4-tt"><b>Crowd Championship</b><small>Judges vs the crowd</small><em>${win}</em></span><span class="c4-te">Entry $${typeof CH_ENTRY !== 'undefined' ? CH_ENTRY : 2}</span></button>`;
      // Crowd Championship removed (user decision)
      return t.innerHTML; } catch (e) { return h; } };
})();
// ---- an unopened special tile stays on Vote (it used to float over other tabs) ----
setInterval(() => { try { const t = document.getElementById('vfTile'); if (t) t.style.visibility = $('#panes').dataset.at === 'judge' ? '' : 'hidden'; } catch (e) {} }, 250);
// ---- steal: a surprise shield on the card you pick ----
(() => {
  function shOffer(nm, who) { const t = riskable().filter(p => !p.shield).sort((a, b) => b.s.total - a.s.total)[0], n = S.shields || 0;
    openSheet(`<div class="shs shp"><div class="shp-ic">🛡</div><h2 class="shs-h">Sorry, ${esc(nm)} is shielded</h2><p class="shs-p">${esc(who)} protected it, so nothing was stolen. Protect your best photo the same way.</p>
      ${t ? `<div class="shp-card"><img src="${t.src}" alt=""><span><b>${esc(alName(t))}</b><small>Earns ${GAL.BASE * galMult(t.s.total)} coins a vote</small></span></div>` : ''}
      ${n && t ? `<button class="btn block shs-go" id="shOf">🛡 Shield ${esc(alName(t))}</button><div style="text-align:center"><button class="link" data-shclose>Back to voting</button></div>`
        : `<p class="shs-earn">${t && t.shield ? '' : 'No shields yet · win them from ✨ special tiles while you vote.'}</p><button class="btn block shs-go" data-shclose>Back to voting</button>`}</div>`);
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
    if ($('#shOf')) $('#shOf').onclick = () => { closeSheet(); window.__shPut && window.__shPut(t); }; }
  function lkOffer(w, cn) {
    openSheet(`<div class="shs shp"><div class="shp-ic">🔒</div><h2 class="shs-h">${esc(w.nm)} is in ${esc(cn)}</h2><p class="shs-p">You can only steal from collections you’ve started. Add your own ${esc(cn.toLowerCase())} photo, then ${esc(cn)} cards like this one are yours to steal, and they earn coins on every vote.</p>
      <div class="shp-card"><img src="${w.src}" alt=""><span><b>${esc(w.nm)}</b><small>${esc(cn)} · about ${GAL.BASE * galMult(w.sc || 70)} coins a vote</small></span></div>
      <button class="btn block shs-go" id="lkGo">📷 Add a ${esc(cn.toLowerCase())} photo</button><div style="text-align:center"><button class="link" data-shclose>Back to voting</button></div></div>`);
    document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
    $('#lkGo').onclick = () => { closeSheet(); setTimeout(() => addCatPhoto(w.cat), 250); }; }
  new MutationObserver(() => { try { const el = document.getElementById('raid'); if (!el || el.dataset.sh2) return; const cs = [...el.querySelectorAll('.rd-card[data-rd]')]; if (cs.length < 3) return; el.dataset.sh2 = 1;
    const W = window.__rdWall || [], own = c => S.photos.some(p => p.s && !p.card && !p.heldBy && p.cat === c);
    cs.forEach((c, i) => { const w = W[+c.dataset.rd]; if (!w || own(w.cat)) return; const cn = galNm(w.cat); c.dataset.lk = 1;
      c.addEventListener('click', e => { if (el.dataset.pick) return; e.stopImmediatePropagation(); e.preventDefault(); el.dataset.pick = 1;
        c.classList.add('picked', 'rd-lock', 'rd-bonk'); el.querySelectorAll('.rd-card').forEach(x => x !== c && x.classList.add('gone'));
        const fr = c.querySelector('.rd-fr'); if (fr) fr.insertAdjacentHTML('beforeend', '<i class="rd-shb rd-slam">🔒</i>'); const sm = c.querySelector('small'); if (sm) sm.textContent = `🔒 ${cn} collection`;
        const hn = el.querySelector('.rd-hint'); if (hn) hn.innerHTML = `<b class="rd-shn">🔒 Add a ${esc(cn.toLowerCase())} photo to steal this</b>`;
        setTimeout(() => { try { el.remove(); } catch (x) {} try { VF_BUSY = 0; } catch (x) {} lkOffer(w, cn); }, 1900); }, true); });
    const free = cs.filter(c => !c.dataset.lk); if (!free.length) return;
    if (!window.__shForce && Math.random() >= .35) return; const c = window.__shForce ? free[0] : free[Math.floor(Math.random() * free.length)];
    c.addEventListener('click', e => { if (el.dataset.pick) return; e.stopImmediatePropagation(); e.preventDefault(); el.dataset.pick = 1;
      const nm = (c.querySelector('b') || {}).textContent || 'That photo', who = ((el.querySelector('.rd-who') || {}).textContent || '').split('’')[0].replace(/^\s*\S\s*/, '').trim() || 'They';
      c.classList.add('picked', 'rd-shd', 'rd-bonk'); el.querySelectorAll('.rd-card').forEach(x => x !== c && x.classList.add('gone'));
      const fr = c.querySelector('.rd-fr'); if (fr) fr.insertAdjacentHTML('beforeend', '<i class="rd-shb rd-slam">🛡</i>'); const sm = c.querySelector('small'); if (sm) sm.textContent = '🛡 Shielded';
      const hn = el.querySelector('.rd-hint'); if (hn) hn.innerHTML = `<b class="rd-shn">🛡 Sorry, ${esc(nm)} is shielded</b>`;
      setTimeout(() => { try { el.remove(); } catch (x) {} try { VF_BUSY = 0; } catch (x) {} shOffer(nm, who); }, 1900); }, true); } catch (e) {} }).observe($('#shell'), { childList: true });
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
html body .c2-bar{display:none!important}
#raid .rd-card.rd-lock .rd-fr img{filter:grayscale(1) brightness(.55)}#raid .rd-card.rd-lock .rd-sc{display:none}
#raid .rd-lk{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-style:normal;font-size:1.6rem}#raid .rd-lk small{font:900 .8rem "Nunito Sans",sans-serif;color:#fff}
#raid .rd-lkn{display:inline-block;margin-top:6px;color:#F3D27A;font-weight:800}
#raid .rd-card.rd-shd{opacity:1!important;filter:none!important}#raid .rd-card.rd-shd .rd-fr{box-shadow:0 0 0 3px #8FB6EE,0 0 22px rgba(143,182,238,.9)!important}
#raid .rd-card.rd-bonk{animation:rdBonk .45s}@keyframes rdBonk{20%{transform:translateX(-8px) rotate(-3deg)}50%{transform:translateX(8px) rotate(3deg)}80%{transform:translateX(-4px)}}
#raid .rd-shb{position:absolute;top:50%;left:50%;z-index:3;display:grid;place-items:center;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;background:#14213D;font-style:normal;font-size:2rem;box-shadow:0 0 0 3px #D9AE4F,0 0 24px rgba(143,182,238,.9)}
#raid .rd-slam{animation:rdSlam .5s cubic-bezier(.2,1.6,.4,1)}@keyframes rdSlam{from{transform:scale(3);opacity:0}}
#raid .rd-shn{display:inline-block;font:900 1.2rem Fraunces,Georgia,serif;color:#BFD6FF}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('steal2 ok')
