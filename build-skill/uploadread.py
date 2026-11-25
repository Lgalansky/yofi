# Read chosen photos as data URLs instead of blob: URLs. Some hosts (for example the Claude app's
# page viewer) block blob: images, so a photo picked from the library silently never appeared.
# Usage: python3 build-skill/uploadread.py [in.html] [out.html]  (defaults to index.html in place)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'const fileURL =' in s: sys.exit('uploadread already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("const loadImg = src => new Promise((res, rej) => {",
    "const fileURL = f => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(r.result); r.onerror = rej; r.readAsDataURL(f); });\nconst loadImg = src => new Promise((res, rej) => {")
rep("const url = smp || URL.createObjectURL(f);", "let url; try { url = smp || await fileURL(f); } catch (err) { toast('This photo couldn’t be read. Try another one.'); return; }")
rep("const url = URL.createObjectURL(f); let im;", "const url = await fileURL(f); let im;")
rep("const url = URL.createObjectURL(f); let img; try {", "const url = await fileURL(f).catch(() => ''); let img; try {")
assert 'createObjectURL' not in s
open(p, 'w', encoding='utf-8').write(s); print('uploadread ok')
