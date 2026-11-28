# Skill preview: a Steal button in the bottom menu (Vote | Gallery | Compete | Steal).
#  Tapping it opens the steal screen (free to try, first to 5 votes takes the card). If one of your
#  cards is held by a rival, it opens "Win it back" instead and the button shows a red "!" badge.
#  Otherwise a small badge shows the tries left today (hidden when none are left).
# usage: python3 build-skill/navsteal.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- Steal in the bottom menu ----
const NS_IC = '<svg viewBox="0 0 32 28" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"><rect x="3" y="4" width="14" height="20" rx="3" transform="rotate(-12 10 14)" fill="rgba(38,31,28,.14)"/><rect x="14" y="3" width="14" height="20" rx="3" transform="rotate(10 21 13)"/></g><path d="M18 11.5l2.2 2.2 4-4.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" transform="rotate(10 21 13)"/></svg>';
function nsPaint() { const n = document.querySelector('nav.seg'); if (!n) return; let b = $('#segSteal');
  if (!b) { b = document.createElement('button'); b.id = 'segSteal'; b.setAttribute('aria-pressed', 'false'); b.innerHTML = `${NS_IC}<span>Steal</span><i class="ns-b" hidden></i>`; n.appendChild(b);
    b.onclick = () => { const h = S.photos.find(p => p.heldBy); try { if ($('#sheet').classList.contains('on')) closeSheet(); } catch (e) {} setTimeout(() => stealSheet(h ? { back: h.id } : {}), 60); }; }
  const bd = b.querySelector('.ns-b'), held = S.photos.some(p => p.heldBy), left = typeof stlLeft === 'function' ? stlLeft() : 0;
  const t = held ? '!' : left ? String(left) : ''; if (bd.textContent !== t) bd.textContent = t; bd.hidden = !t; bd.classList.toggle('alert', held); }
setInterval(() => { try { nsPaint(); } catch (e) {} }, 1500); setTimeout(() => { try { nsPaint(); } catch (e) {} }, 300);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Steal in the bottom menu */
nav.seg #segSteal{order:9;position:relative}
nav.seg #segSteal svg{width:30px;height:26px}
#segSteal .ns-b{position:absolute;top:4px;right:calc(50% - 26px);min-width:18px;height:18px;padding:0 5px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .68rem/18px "Nunito Sans";font-style:normal;text-align:center;box-sizing:border-box}
#segSteal .ns-b.alert{background:#C8432F;color:#fff}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('navsteal ok')
