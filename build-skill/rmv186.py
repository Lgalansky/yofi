# Real Money build, step 189 (after rmv185.py): "Train for Cash Races" sheet in the owner's navy mock-up style.
#  Navy sheet with ✕, title, "Win 3 before 3 losses to qualify. Unlock head-to-heads and $2–$20 finals.",
#  gold box "🪙 425 coins | 8 matches available", "🪙 50 coins per training match", cream photo cards
#  (photo, name, status, "0 wins · 0 losses") with a blue "Start training" / "Continue training" button
#  (or "Need 50 more coins"), photos already unlocked show "Cash races unlocked · $8.50 won" and a green
#  "Enter a final". Outlined "Invite a friend ›" card and the earn-coins footer.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""function useGems() { const g = Math.floor(S.gems || 0), n = Math.floor(g / TQ_COST), P = stHorses(), O = P.filter(p => !isCashOK(p)), R = P.filter(isCashOK);
  const st = p => { const q = p.ql; return q && !q.done ? 'In qualifying' : q && q.done === 'x' ? 'Missed the cut' : 'Resting'; };
  const tc = p => { const T = p.tq || { w: 0, l: 0 }, go = T.w || T.l;
    return `<div class="t2-c"><div class="t2-r"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><span>${st(p)}</span><small>${T.w} win${T.w === 1 ? '' : 's'} · ${T.l} loss${T.l === 1 ? '' : 'es'}</small></div></div>
      ${g >= TQ_COST ? `<button class="btn t2-b blue" data-tct="${p.id}">${go ? 'Continue training' : 'Start training'}</button>` : `<button class="btn t2-b off" disabled>Need ${TQ_COST - g} more coins</button>`}</div>`; };
  const rc = p => { const w = stWon(p); return `<div class="t2-c"><div class="t2-r"><img src="${p.src}" alt=""><div><b>${esc(rcName(p))}</b><span>Cash races unlocked</span><small>${w ? `${money(w)} won` : 'Ready to race'}</small></div></div><button class="btn t2-b green" data-tcf="${p.id}">Enter a final</button></div>`; };
  openSheet(`<div class="trc t2"><button class="t2-x" data-t2x aria-label="Close">✕</button><h2 class="t2-h">Train for Cash Races</h2>
    <p class="t2-s"><b>Win 3 before 3 losses to qualify.</b><br>Unlock head-to-heads and $2–$20 finals.</p>
    <div class="t2-bal"><span>🪙 <b>${g.toLocaleString()} coins</b></span><i></i><span>${n} match${n === 1 ? '' : 'es'} available</span></div><p class="t2-per">🪙 ${TQ_COST} coins per training match</p>
    ${O.map(tc).join('')}${R.map(rc).join('')}${P.length ? '' : `<div class="t2-c t2-e"><p>📷 Enter a photo (free), then train it here with your coins.</p><button class="btn t2-b blue" data-tcn>Enter a photo · free</button></div>`}
    <button class="t2-inv" data-tci><span><b>Invite a friend</b><small>You each get 100 coins when they judge 15 photos.</small></span><em>›</em></button>
    <p class="t2-f">Earn coins by judging. Get 50 more when a photo qualifies. Coins can’t be bought.</p></div>`);
  const B = $('#sheetBody');
  B.querySelectorAll('[data-t2x]').forEach(b => b.onclick = () => closeSheet());
  B.querySelectorAll('[data-tct]').forEach(b => b.onclick = () => { const p = S.photos.find(x => x.id === b.dataset.tct); closeSheet(); setTimeout(() => h2hOpen(p, 0), 200); });
  B.querySelectorAll('[data-tcf]').forEach(b => b.onclick = () => { const p = S.photos.find(x => x.id === b.dataset.tcf); closeSheet(); setTimeout(() => qfStart(p), 200); });
  B.querySelectorAll('[data-tcn]').forEach(b => b.onclick = () => { closeSheet(); setTimeout(finPick, 200); });
  B.querySelectorAll('[data-tci]').forEach(b => b.onclick = () => { closeSheet(); setTimeout(openFriends, 200); }); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #sheet:has(.t2){background:linear-gradient(180deg,#14224A,#0B1530)!important;color:#EEF1F8}html body #sheet:has(.t2) .grab,html body #sheet:has(.t2) [class*=handle]{background:#8C9AB5!important}
.t2{position:relative;padding:4px 2px 10px;text-align:center}.t2-x{position:absolute;top:-6px;right:0;border:0;background:none;color:#FBF3DC;font-size:1.6rem;cursor:pointer}
html body .t2 h2.t2-h{margin:14px 0 8px;font:900 2.2rem/1.05 Fraunces,Georgia,serif;color:#FBF3DC!important;-webkit-text-fill-color:#FBF3DC!important}
.t2-s{margin:0 0 14px;font:600 1.02rem/1.4 Nunito,system-ui;color:#EEF1F8}.t2-s b{font-size:1.12rem;color:#fff}
.t2-bal{display:flex;align-items:center;justify-content:space-around;padding:12px 10px;border-radius:16px;box-shadow:inset 0 0 0 2px #D9AE4F;font:700 1.05rem Nunito,system-ui;color:#EEF1F8}.t2-bal b{font-size:1.25rem;color:#fff}.t2-bal i{width:1.5px;height:26px;background:#D9AE4F}
.t2-per{margin:10px 0 12px;font:800 1.05rem Nunito,system-ui;color:#EEF1F8}
.t2-c{margin:0 0 12px;padding:12px;border-radius:20px;background:#FBF6EE;text-align:left}.t2-r{display:flex;gap:14px;align-items:center;margin-bottom:10px}.t2-r img{width:104px;height:92px;border-radius:14px;object-fit:cover;flex:none}
.t2-r div{display:flex;flex-direction:column;gap:3px;min-width:0}.t2-r b{font:900 1.6rem/1.05 Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.t2-r span{font:800 1rem Nunito,system-ui;color:#3D2B1F}.t2-r small{font:700 .95rem Nunito,system-ui;color:#5B4A3F}
html body .t2 .btn.t2-b{width:100%!important;min-height:48px!important;margin:0!important;border-radius:14px!important;font:800 1.15rem Nunito,system-ui!important;color:#fff!important;box-shadow:none!important}
html body .t2 .btn.t2-b.blue{background:linear-gradient(180deg,#2347B8,#1A3A99)!important}html body .t2 .btn.t2-b.green{background:linear-gradient(180deg,#2F8A3F,#1F6A2E)!important}html body .t2 .btn.t2-b.off{background:#D8CFC0!important;color:#5B4A3F!important}
.t2-e p{margin:0 0 10px;font:700 .95rem Nunito,system-ui;color:#3D4A5C;text-align:center}
.t2-inv{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;margin:4px 0 0;padding:12px 16px;border:0;border-radius:16px;background:rgba(255,255,255,.04);box-shadow:inset 0 0 0 1.5px #8C9AB5;cursor:pointer;text-align:left;font:inherit;color:#EEF1F8}
.t2-inv b{display:block;font:900 1.3rem Fraunces,Georgia,serif;color:#FBF3DC}.t2-inv small{font:600 .88rem Nunito,system-ui;color:#C9D3E6}.t2-inv em{font-style:normal;font-size:1.6rem;color:#FBF3DC}
.t2-f{margin:14px 6px 0;font:600 .9rem/1.4 Nunito,system-ui;color:#C9D3E6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v186 ok')
