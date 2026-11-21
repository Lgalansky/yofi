# Real Money build, step 225 (after rmv221.py): landing page from the user's mock-up (copy corrected for accuracy).
#  - Headline: "Can you spot the crowd favourite?" + "Tap the photo you think got the most votes." + the 3-photo guess.
#  - Navy race card: "🏁 Live races" · "Race your photo for real cash." · "Beat a rival to reach the six-photo Final." ·
#    trophy under stadium lights · green "📷 Enter your photo →" · "First entry free · Finals from $2".
#    (Mock-up said "Daily Cup" and "Free entry to the Final": the Daily Cup is the separate coins prize pot and Final
#    entries cost $2–$20, so the card says "Live races" and "Finals from $2".)
#  - Link: "Vote on photos to earn coins →" goes straight into voting (guest).
#  - Winners ticker under it; the old "Start here" block is removed (the card replaces it).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""function lpVote() { if (!S.user) { S.user = { h: 'guest' + Math.floor(1000 + Math.random() * 9000), guest: 1 }; try { tutInit(); } catch (e) {} save(); } openApp(); setTimeout(() => { go('judge'); renderJudge(); }, 60); }
window.lpVote = lpVote;
function lp3() { const L = document.querySelector('#landing .lp.lp2'); if (!L || L.dataset.v3) return; const h = L.querySelector('.lp-h'), sub = L.querySelector('.lp-sub'), cap = document.getElementById('lpCap'), tk = document.getElementById('lpTick'); if (!h || !cap) return; L.dataset.v3 = 1;
  h.innerHTML = 'Can you spot <em>the crowd favourite?</em>'; if (sub) sub.textContent = 'Tap the photo you think got the most votes.';
  cap.classList.add('lp3-cap'); if (/Tap the photo/.test(cap.textContent)) cap.textContent = '';
  const st = L.querySelector('.lp2-sec'); if (st && /Start here/.test(st.textContent)) st.parentNode.removeChild(st);
  cap.insertAdjacentHTML('afterend', `<div class="lp3-card"><i class="lp3-l a"></i><i class="lp3-l b"></i><i class="lp3-l c"></i><span class="lp3-tr" aria-hidden="true">🏆</span>
      <p class="lp3-k">🏁 Live races</p><h2>Race your photo for real cash.</h2><p class="lp3-s">Beat a rival to reach the six-photo Final.</p>
      <button class="lp3-go" onclick="rmEnterOwn()">📷 Enter your photo <span aria-hidden="true">→</span></button><p class="lp3-f">First entry free · Finals from $2</p></div>
    <button class="lp3-v" onclick="lpVote()">Vote on photos to earn coins <span aria-hidden="true">→</span></button>`);
  if (tk) { const v = L.querySelector('.lp3-v'); v.insertAdjacentElement('afterend', tk); } }
setInterval(() => { try { if ($('#landing').style.display !== 'none') lp3(); } catch (e) {} }, 400);
function fcNotify() {""")
s = s.replace('</style>', """#landing .lp.lp2 .lp-h{font-size:2.15rem!important;letter-spacing:-.01em;line-height:1.02!important;text-align:left!important;margin:8px 0 6px!important;color:#231A15}#landing .lp.lp2 .lp-h em{display:block;font-style:normal;color:#1E6B34}
#landing .lp.lp2 .lp-sub{text-align:left!important;margin:0 0 14px!important;font:500 1.05rem/1.4 Nunito,system-ui!important;color:#5B4A3F!important}
#landing .lp3-cap:empty{display:none}#landing .lp3-cap{margin:10px 0 0!important}
.lp3-card{position:relative;overflow:hidden;margin:18px 0 0;padding:20px 18px 16px;border-radius:24px;text-align:left;color:#fff;background:radial-gradient(120% 90% at 85% 10%,#2A3E70 0%,#16244A 45%,#0E1830 100%);box-shadow:0 14px 30px -12px rgba(14,24,48,.55)}
.lp3-l{position:absolute;width:120px;height:60px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,250,220,.55),rgba(255,250,220,0));filter:blur(2px);pointer-events:none}.lp3-l.a{right:-20px;top:-14px}.lp3-l.b{right:90px;top:6px;width:80px;height:40px;opacity:.7}.lp3-l.c{right:40px;top:44px;width:60px;height:30px;opacity:.5}
.lp3-tr{position:absolute;right:10px;top:58px;font-size:5.2rem;line-height:1;filter:drop-shadow(0 6px 14px rgba(243,201,90,.55));animation:lp3T 3s ease-in-out infinite}@keyframes lp3T{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-6px) rotate(3deg)}}
.lp3-k{display:inline-block;margin:0 0 8px;padding-bottom:4px;border-bottom:2px solid #D9AE4F;font:900 .9rem Fraunces,Georgia,serif;font-style:italic;letter-spacing:.12em;text-transform:uppercase;color:#FBF3DC}
.lp3-card h2{position:relative;margin:0 0 6px;max-width:72%;font:900 1.85rem/1.05 Fraunces,Georgia,serif;color:#fff}
.lp3-s{position:relative;margin:0 0 16px;max-width:75%;font:600 .95rem/1.35 Nunito,system-ui;color:#DDE3F0}
.lp3-go{position:relative;display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:58px;border:0;border-radius:999px;background:linear-gradient(180deg,#2F8A45,#1E6B34);color:#fff;font:900 1.3rem Fraunces,Georgia,serif;cursor:pointer;box-shadow:0 8px 18px -6px rgba(30,107,52,.7);animation:lp3G 2.6s ease-in-out infinite}
@keyframes lp3G{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}.lp3-f{position:relative;margin:10px 0 0;text-align:center;font:600 .9rem Nunito,system-ui;color:#DDE3F0}
.lp3-v{display:block;margin:16px auto 6px;border:0;background:none;font:800 1.05rem Nunito,system-ui;color:#14213D;text-decoration:underline;text-underline-offset:4px;cursor:pointer}
#landing .lp-tick{margin-top:10px}
html body #landing .lp.lp2 .lp3-card h2{color:#fff!important;-webkit-text-fill-color:#fff!important;background:none!important;font:900 1.85rem/1.05 Fraunces,Georgia,serif!important;text-align:left!important;margin:0 0 6px!important;max-width:70%!important}
html body #landing .lp.lp2 .lp3-card .lp3-go{display:flex!important;align-items:center;justify-content:center;gap:8px;width:100%!important;min-height:58px!important;margin:0!important;border:0!important;border-radius:999px!important;background:linear-gradient(180deg,#2F8A45,#1E6B34)!important;color:#fff!important;font:900 1.3rem Fraunces,Georgia,serif!important;box-shadow:0 8px 18px -6px rgba(30,107,52,.7)!important}
html body #landing .lp.lp2 .lp-h{font-size:1.95rem!important}html body #landing .lp.lp2 .lp-sub{font-size:1rem!important}
#landing .lp3-card h2{color:#fff!important;font:900 1.85rem/1.05 Fraunces,Georgia,serif!important;text-align:left!important;margin:0 0 6px!important}
#landing .lp3-card .lp3-k{color:#FBF3DC!important;text-align:left!important}#landing .lp3-card .lp3-s{color:#DDE3F0!important;text-align:left!important;font:600 .95rem/1.35 Nunito,system-ui!important}
#landing .lp3-card .lp3-f{color:#DDE3F0!important;text-align:center!important}#landing .lp3-card .lp3-go{color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v222 ok')
