# Upload fallback: some in-app browsers (for example the Claude app's page viewer, Facebook and
# Instagram) never open the photo picker. If tapping an upload button opens nothing within ~1.5 s,
# show a hint under the button pointing to the sample photos and to opening the page in Safari/Chrome.
# Usage: python3 build-skill/uploadhint.py [in.html] [out.html]  (defaults to index.html in place)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'upHintWatch' in s: sys.exit('uploadhint already applied')
JS = r'''
// if the photo picker never opens (in-app browsers), say so and point to the sample photos
(function upHintWatch() {
  document.addEventListener('click', e => {
    const l = e.target.closest('label[for="file"]'); if (!l || e.defaultPrevented) return;
    let opened = false; const f = document.getElementById('file'), mark = () => { opened = true; };
    window.addEventListener('blur', mark, { once: true }); document.addEventListener('visibilitychange', mark, { once: true });
    if (f) { f.addEventListener('change', mark, { once: true }); f.addEventListener('cancel', mark, { once: true }); }
    setTimeout(() => {
      window.removeEventListener('blur', mark); document.removeEventListener('visibilitychange', mark);
      if (opened || !l.isConnected) return;
      let h = l.parentNode.querySelector('.uphint'); if (h) return;
      h = document.createElement('p'); h.className = 'uphint'; h.setAttribute('role', 'status');
      h.innerHTML = `<b>Photo picker didn’t open?</b> This browser may block uploads. ${l.closest('#ageGate') ? 'Tap one of our photos below to try it now, or ' : ''}open this page in Safari or Chrome to use your own.`;
      l.insertAdjacentElement('afterend', h);
    }, 1600);
  });
})();
'''
CSS = '.uphint{margin:10px 0 0;padding:10px 12px;border-radius:12px;background:rgba(233,165,20,.14);border:1px solid rgba(233,165,20,.5);font-size:.9rem;line-height:1.4;text-align:left}.uphint b{display:block}\n'
i = s.rindex('</script>'); s = s[:i] + JS + s[i:]
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('uploadhint ok')
