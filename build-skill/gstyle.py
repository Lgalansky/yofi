# Skill preview: Gallery binder restyled to the user's mock-up.
#  - navy leather binder with a gold stitched edge, a cream page inside, gold binder rings
#  - "Pets Collection" title + "1/3 filled" pill sit on the page, with a gold rule under them
#  - photo cards: gold frame, round gold score medallion, name / tier / "4 coins per vote" on a gold
#    plaque inside the card (no "Earns on votes" overlay)
#  - empty sleeves look like glossy plastic sleeves ("+ Add a pet photo"), no caption under them
#  - the next collection is a navy leather card: photo inset, gold lock, "Travel Collection",
#    "Opens at Gold"
# usage: python3 build-skill/gstyle.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- Gallery binder look ----
function gsBinder() { const st = $('#studio'); if (!st) return; const bk = st.querySelector('.a2-book'); if (!bk) return;
  if (!bk.querySelector('.gs-page')) { const pg = document.createElement('div'); pg.className = 'gs-page'; const th = st.querySelector('.a2-th'), gr = bk.querySelector('.a2-grid');
    if (th) { th.querySelector('h3') && (th.querySelector('h3').textContent = th.querySelector('h3').textContent.replace(/collection$/i, 'Collection')); pg.appendChild(th); } if (gr) pg.appendChild(gr); bk.appendChild(pg); }
  bk.querySelectorAll('.a2-sl:not(.empty):not(.a2-nx)').forEach(sl => { if (sl.dataset.gs) return; sl.dataset.gs = 1; const cd = sl.querySelector('.a2-card'), cp = sl.querySelector('.a2-cap'); if (cd && cp) cd.appendChild(cp);
    const l2 = sl.querySelector('.a2-l2'); if (l2) l2.innerHTML = l2.innerHTML.replace(/^Earns\s*/, ''); });
  bk.querySelectorAll('.a2-nx').forEach(sl => { if (sl.dataset.gs) return; sl.dataset.gs = 1; const box = sl.querySelector('.a2-box'), pl = sl.querySelector('.a2-plq'); const nm = pl ? pl.textContent.replace(/collection$/i, 'Collection') : 'Next Collection';
    if (box) box.insertAdjacentHTML('beforeend', `<b class="gs-nt">${esc(nm)}</b><small class="gs-ns">${esc((sl.querySelector('.a2-l2') || {}).textContent || 'Opens at Gold')}</small>`); }); }
new MutationObserver(() => { try { gsBinder(); } catch (e) {} }).observe($('#studio'), { childList: true, subtree: true });
setTimeout(() => { try { gsBinder(); } catch (e) {} }, 300);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Gallery binder look */
html body #studio .a2-book{position:relative;margin:6px 10px 14px;padding:12px 12px 14px 22px!important;border:0!important;border-radius:26px!important;background:radial-gradient(circle at 30% 20%,#2B3D66,#16213D 75%)!important;box-shadow:inset 0 0 0 2px #0E1730,inset 0 0 0 7px #1D2B4F,0 18px 30px -16px rgba(0,0,0,.6)!important}
html body #studio .a2-book::before{content:"";position:absolute;inset:6px;border-radius:21px;border:1.5px dashed rgba(224,168,46,.55);pointer-events:none}
html body #studio .gs-page{position:relative;padding:14px 12px 14px 30px;border-radius:18px;background:linear-gradient(180deg,#FBF5EA,#F3E9D6);box-shadow:inset 0 0 0 1.5px #E2D2B3,0 4px 10px -6px rgba(0,0,0,.5)}
html body #studio .gs-page .a2-th{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 2px 12px!important;padding:0 0 10px!important;border-bottom:2px solid #D8B25A}
html body #studio .gs-page .a2-th h3{margin:0!important;min-width:0;font:900 1.2rem/1.05 Fraunces,serif!important;white-space:nowrap;color:#8E1F1F!important}
html body #studio .gs-page .a2-badge{flex:none;white-space:nowrap;padding:3px 8px!important;font-size:.74rem!important;border-radius:99px!important;background:#FFF6DD!important;box-shadow:inset 0 0 0 1.5px #D8B25A!important;color:#1F3157!important;font:900 .82rem Fraunces,serif!important}
html body #studio .a2-grid{margin:0!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;gap:12px!important}
html body #studio .a2-ring{left:-6px!important;width:52px!important;height:24px!important;margin-top:-12px;border-radius:50%!important;background:none!important;border:5px solid transparent!important;border-top-color:#F7D98A!important;border-right-color:#C8962A!important;border-bottom-color:#8A5A0A!important;border-left-color:#B07F1E!important;box-shadow:0 3px 5px rgba(0,0,0,.45),inset 0 1px 2px rgba(0,0,0,.4)!important;transform:rotate(-6deg);z-index:3}
html body #studio .a2-ring::after{content:"";position:absolute;right:-1px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:#3A2E1A;box-shadow:inset 0 1px 2px #000}
/* filled card */
html body #studio .a2-sl:not(.empty):not(.a2-nx) .a2-card{position:relative;display:block;padding:5px!important;border-radius:16px!important;background:linear-gradient(160deg,#F7DB8E,#C8962A 55%,#F3D27A)!important;box-shadow:0 10px 18px -10px rgba(0,0,0,.6)!important}
html body #studio .a2-sl .a2-card .a2-ph{border-radius:12px!important;overflow:hidden}
html body #studio .a2-sl .a2-earn,html body #studio .a2-sl .a2-ti{display:none!important}
html body #studio .a2-sl .a2-sc{top:8px!important;right:8px!important;left:auto!important;width:46px;height:46px;padding:0!important;border-radius:50%!important;display:flex!important;align-items:center;justify-content:center;background:radial-gradient(circle at 35% 30%,#FFF3C4,#E0A82E)!important;color:#2D2521!important;font:900 1.15rem Fraunces,serif!important;box-shadow:0 0 0 2px #fff,0 0 0 4px #C8962A,0 4px 8px rgba(0,0,0,.35)!important}
html body #studio .a2-card .a2-cap{display:block!important;margin:5px 0 0!important;padding:6px 8px 7px!important;border-radius:10px;background:linear-gradient(180deg,#FFF6DD,#F3E2B0);box-shadow:inset 0 0 0 1px #D8B25A;text-align:left}
html body #studio .a2-card .a2-l1{display:flex;align-items:center;justify-content:space-between;gap:6px}html body #studio .a2-card .a2-l1 b{font:900 1.05rem Fraunces,serif!important;color:#2D2521!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body #studio .a2-card .a2-tb{flex:none;padding:1px 8px!important;border-radius:99px;background:linear-gradient(180deg,#F7DB8E,#E0A82E)!important;color:#5A3D00!important;font:900 .62rem "Nunito Sans"!important;font-style:normal}
html body #studio .a2-card .a2-l2{display:flex!important;align-items:center;gap:4px;margin-top:2px;font:700 .74rem "Nunito Sans"!important;color:#4E433C!important;white-space:nowrap}html body #studio .a2-card .a2-l2 b{font:900 .95rem Fraunces,serif!important;color:#2D2521!important}html body #studio .a2-card .a2-l2 svg{width:14px;height:14px;order:-1}
html body #studio .a2-book::after,html body #studio .gs-page::after{display:none!important}
/* equal sleeves: the card's photo shrinks so the plaque fits inside */
html body #studio .a2-sl{display:flex!important;flex-direction:column!important}
html body #studio .a2-sl:not(.empty):not(.a2-nx) .a2-card{display:flex!important;flex-direction:column!important;flex:1}
html body #studio .a2-sl .a2-card .a2-ph{flex:1 1 auto;min-height:0;height:auto!important}html body #studio .a2-sl .a2-card .a2-ph img{height:100%!important;width:100%;object-fit:cover}
html body #studio .a2-sl.empty .a2-box,html body #studio .a2-nx .a2-box{flex:1;aspect-ratio:auto!important;height:auto!important;min-height:0}
/* empty sleeve */
html body #studio .a2-sl.empty .a2-cap,html body #studio .a2-nx .a2-cap{display:none!important}
html body #studio .a2-sl.empty .a2-box{border-radius:16px!important;background:linear-gradient(135deg,rgba(255,255,255,.9) 0%,rgba(255,255,255,.25) 35%,rgba(255,255,255,.05) 55%,rgba(255,255,255,.55) 100%),#EFE6D6!important;box-shadow:inset 0 0 0 1.5px #E2D2B3,inset 0 0 0 7px rgba(255,255,255,.55),0 4px 10px -6px rgba(0,0,0,.35)!important;border:0!important}
html body #studio .a2-sl.empty .a2-add{border:1.5px dashed rgba(180,160,120,.6)!important;border-radius:12px!important;background:none!important}
/* next collection: navy leather */
html body #studio .a2-nx .a2-box{display:flex!important;flex-direction:column;align-items:center;padding:10px 8px 12px!important;border-radius:16px!important;background:radial-gradient(circle at 50% 20%,#2B3D66,#16213D)!important;box-shadow:inset 0 0 0 1.5px #0E1730,0 6px 12px -8px rgba(0,0,0,.6)!important;border:0!important;position:relative}
html body #studio .a2-nx .a2-box::before{content:"";position:absolute;inset:4px;border-radius:13px;border:1.5px dashed rgba(224,168,46,.55);pointer-events:none}
html body #studio .a2-nx .a2-nxi{position:relative;width:100%;height:auto!important;aspect-ratio:16/10;border-radius:10px!important;box-shadow:0 0 0 2px #D8B25A!important;flex:none}
html body #studio .a2-nx .a2-plq{display:none!important}
html body #studio .a2-nx .a2-nxl{position:absolute!important;left:50%!important;bottom:-18px!important;top:auto!important;transform:translateX(-50%)!important;width:40px!important;height:40px!important;border-radius:50%!important;display:flex!important;align-items:center;justify-content:center;background:radial-gradient(circle at 35% 30%,#FFE8A6,#C8962A)!important;box-shadow:0 0 0 2px #16213D,0 3px 6px rgba(0,0,0,.5)!important;font-size:1.05rem}
.gs-nt{display:block;margin-top:24px;font:900 1.15rem/1.1 Fraunces,serif;color:#F3D27A;text-align:center}
.gs-nt::before,.gs-nt::after{content:"❦";font-size:.8rem;color:#C8962A;margin:0 4px;vertical-align:middle}
.gs-ns{display:block;margin-top:6px;padding-top:6px;border-top:1px solid rgba(216,178,90,.6);font:700 .78rem "Nunito Sans";color:#E6EDF8}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('gstyle ok')
