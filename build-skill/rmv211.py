# Real Money build, step 214 (after rmv210.py): one-tap "Train again" with progress and coins left.
#  - After a training match, "Train again · 50 coins" charges the coins and starts the next match straight away
#    against a new rival (was: back to the rival screen, then a second tap).
#  - The line under the score now reads "2 of 3 wins · 100 coins left · 2 more matches".
#  - Not enough coins: the button becomes "Vote to earn coins · N more to train" and returns to voting.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "function fcNotify() {"
assert s.count(a) == 1
s = s.replace(a, r"""(() => { const hd = h3Done; h3Done = function (p, o, oh, fee) { const r = hd.apply(this, arguments); try { if (!(fee > 0) && p && !p.cashOK) { const b = document.getElementById('h2Ag'), T = p.tq || { w: 0, l: 0 }, g = Math.floor(S.gems || 0), n = Math.floor(g / TQ_COST), net = document.querySelector('.h3 .h3-net') || document.querySelector('.h3-net');
      const over = !(T.w || T.l);
      if (net) net.innerHTML = `${over ? 'Training run over · start a fresh one' : `<b>${T.w} of ${TQ_WIN} wins</b>`} · ${g} coins left${n ? ` · ${n} more match${n === 1 ? '' : 'es'}` : ''}`;
      if (b) { if (g >= TQ_COST) { b.textContent = `🏋️ ${over ? 'Start a fresh run' : 'Train again'} · ${TQ_COST} coins`;
          b.onclick = () => { if ((S.gems || 0) < TQ_COST) return; const k = photoShow(p) || finCatOf(p) || 'pets', pool = SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src && x.src !== (o && o.src)), x = pool[Math.floor(Math.random() * pool.length)] || { src: p.src, title: 'A rival' };
            S.gems -= TQ_COST; save(); try { paintGems(); } catch (e) {} h2hLive(p, { src: x.src, title: x.title || 'A rival', h: '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)] }, 0); }; }
        else { b.textContent = `⚖️ Vote to earn coins · ${TQ_COST - g} more to train`; b.onclick = () => { try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {} go('judge'); renderJudge(); }; } } } } catch (e) {} return r; }; })();
function fcNotify() {""")
open(d + 'yofi-real.html', 'w').write(s); print('rm v211 ok')
