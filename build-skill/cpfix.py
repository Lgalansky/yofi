# Skill preview: tournaments that need other players live in Compete, not on Vote; and the
#  Crowd Championship / Quick Sprint picks give clear feedback.
#  - Live games row on Vote: no Crowd Championship countdown tile and no Sprint tile any more
#    (they stay in Compete).
#  - Every pick: a big "✓ Right!" (green) or "✗ Missed" (red) stamp on the photo you tapped, a
#    burst of sparks on a right pick, the crowd's % on both photos, and the progress dots turn
#    green / red so you can see how the run is going.
#  - Championship tip text: "Everyone gets the same 15 pairs · top 20% share the prize".
#  - End of a Championship run: a celebration pop first ("You're in the money!" / "Great eye!" /
#    "Run complete", big "13/15", your place so far and when results land), then the standings.
#  - Vote screen: in the "So close! / Missed it" box the crowd's % is bold ("55% picked the other one").
# usage: python3 build-skill/cpfix.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)

# Live games: drop the tournaments that need other players
rep("  if (mins <= 15 && !(S.ch && S.ch[nx])) {", "  if (0 && mins <= 15 && !(S.ch && S.ch[nx])) {")
rep("  if (spr) T({ icon: KO_PYR2,", "  if (0 && spr) T({ icon: KO_PYR2,")
# pick feedback
rep("let i = 0, right = 0; const t0 = Date.now(), c = $('#coach');", "let i = 0, right = 0, res = []; const t0 = Date.now(), c = $('#coach');")
rep("<i class=\"${j < i ? 'd' : ''} ${j === i ? 'n' : ''}\"></i>", "<i class=\"${j < i ? 'd ' + (res[j] ? 'w' : 'l') : ''} ${j === i ? 'n' : ''}\"></i>")
rep("<small>Same 10 pairs as your opponent · most right wins · ties go to the fastest</small>",
    "<small>${champ ? `Everyone gets the same ${NN} pairs · top 20% share the prize` : 'Same 10 pairs as your opponent · most right wins · ties go to the fastest'}</small>")
rep("c.querySelectorAll('[data-cp]').forEach(b2 => b2.classList.add(((b2.dataset.cp === 'a') === (p.pa >= 50)) ? 'crowd' : 'lose')); btn.classList.add(win ? 'ok' : 'bad');\n      if (win) right++; i++;",
    "c.querySelectorAll('[data-cp]').forEach(b2 => b2.classList.add(((b2.dataset.cp === 'a') === (p.pa >= 50)) ? 'crowd' : 'lose')); btn.classList.add(win ? 'ok' : 'bad');\n      btn.insertAdjacentHTML('beforeend', `<b class=\"cpr-res ${win ? 'ok' : 'bad'}\">${win ? '✓ Right!' : '✗ Missed'}</b>`);\n      if (win) try { const r0 = vfRel(btn); vfPop($('#shell'), r0.x + r0.w / 2, r0.y + r0.h / 2, ['#3CCB8A', '#F3D27A', '#fff'], 18); } catch (e) {}\n      res.push(win); { const d = c.querySelectorAll('.cpr-steps i')[i]; if (d) d.className = 'd ' + (win ? 'w' : 'l'); }\n      if (win) right++; i++;")

JS = r'''
// ---- vote result: the crowd's % in bold ----
function cfPct() { document.querySelectorAll('#judge .tot-miss small:not([data-pb])').forEach(e => { e.dataset.pb = 1; e.innerHTML = e.innerHTML.replace(/(\d+%)/, '<b class="tot-pct">$1</b>'); }); }
new MutationObserver(() => { try { cfPct(); } catch (e) {} }).observe($('#judge'), { childList: true, subtree: true });
// ---- Championship: a celebration when your run is in, before the standings ----
const _chDoneCF = chDone;
chDone = function (id, right, ms) { const r = _chDoneCF.apply(this, arguments);
  try { const F = chRows(id, right), at = new Date((id + 1) * CH_MS).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }), inP = F.me <= F.paid;
    setTimeout(() => { try { waShow({ title: inP ? 'You’re in the money!' : right >= 10 ? 'Great eye!' : 'Run complete!', big: `${right}/${CH_N}`,
      label: `${ORD(F.me)} of ${F.N} so far · ${inP ? `about ${money(chPrize(F.me, F.N))} if it holds` : 'top 20% get paid'} · results at ${at}`, src: (S.photos.find(p => p.s) || {}).src }); } catch (e) {} }, 350); } catch (e) {}
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* crowd picks: clear right / wrong */
html body #judge .tot-miss small b.tot-pct{display:inline;font:900 1.15em "Nunito Sans";color:#1F3157}
.cpr-p button{position:relative}
.cpr-res{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);z-index:3;padding:10px 18px;border-radius:16px;font:900 1.35rem "Nunito Sans";white-space:nowrap;color:#fff;box-shadow:0 10px 24px -8px rgba(0,0,0,.6);animation:cprStamp .45s cubic-bezier(.2,1.7,.4,1) both;pointer-events:none}
.cpr-res.ok{background:#2E9A5C}.cpr-res.bad{background:#C8432F}
html body .cpr-p button.lose{opacity:1!important;filter:none!important}html body .cpr-p button.lose img{opacity:.45;filter:grayscale(.5)}
@keyframes cprStamp{0%{transform:translate(-50%,-50%) scale(2.4) rotate(-10deg);opacity:0}60%{transform:translate(-50%,-50%) scale(.92) rotate(2deg);opacity:1}100%{transform:translate(-50%,-50%) scale(1) rotate(-3deg)}}
html body .cpr-p button.ok img{box-shadow:0 0 0 5px #2E9A5C!important}html body .cpr-p button.bad img{box-shadow:0 0 0 5px #C8432F!important}
html body .cpr-steps i.d.w{background:#2E9A5C!important}html body .cpr-steps i.d.l{background:#C8432F!important}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('cpfix ok')
