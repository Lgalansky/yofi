# Real Money build, step 61 (after rmv57.py): invite pop from the user's mock-up.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()

i = s.index('function invOpen'); j = s.index('const send = how', i); old = s[i:j]
I = lambda p, w=40: f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
LINK = I('<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/>')
PIC = I('<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="15.5" cy="9" r="1.6"/><path d="M4 17l5-5 4 4 2.5-2.5L20 17"/>')
COINS = I('<ellipse cx="9" cy="14" rx="6" ry="2.5"/><path d="M3 14v3c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5v-3"/><ellipse cx="15" cy="8" rx="6" ry="2.5"/><path d="M9 8v3c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V8"/>')
GIFT = I('<rect x="3" y="9" width="18" height="4" rx="1"/><path d="M5 13v7h14v-7M12 9v11M12 9c-2-3-6-3-6-1s4 1 6 1zm0 0c2-3 6-3 6-1s-4 1-6 1z"/>', 26)
PPL = I('<circle cx="8.5" cy="8" r="3.2"/><circle cx="16" cy="8" r="3.2"/><path d="M2.5 19c.5-3.4 3-5.3 6-5.3s5.5 1.9 6 5.3M13 14c3.2-.6 7 .9 8.5 5"/>', 26)
WA = '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.5.5 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7s1.8 2.8 4.4 3.9c1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2s.2-1.1.1-1.2-.2-.2-.5-.3z"/></svg>'
STACK = '<span class="iv-stack"><i class="qz3-coin"></i><i class="qz3-coin"></i><i class="qz3-coin"></i></span>'
new = r"""function invOpen() { try { closeSheet(); } catch (e) {} const L = S.inv || [], p = invPaid(), left = INV_MAX - p;
  const st = x => x.st === 'paid' ? `<em class="ok">✓ <i class="qz3-coin"></i> +${INV_PAY}</em>` : x.st === 'joined' ? `<em class="mid">Judging ${Math.min(INV_VOTES - 1, x.v || 0)}/${INV_VOTES}</em>` : '<em>Invite sent</em>';
  popOpen(`<div class="pp inv iv2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k iv-k">""" + PPL + r""" Invite friends</p>
    <p class="iv-e">Earn</p><b class="iv-big">${INV_PAY} coins""" + STACK + r"""</b><p class="iv-sub">for every friend you invite</p><p class="iv-when">When they judge ${INV_VOTES} photos.</p>
    <span class="iv-cap">Earn up to ${(INV_PAY * INV_MAX).toLocaleString()} coins · ${INV_MAX} friends</span>
    <div class="iv-steps"><div><i>1</i>""" + LINK + r"""<b>Share your link</b></div><span></span><div><i>2</i>""" + PIC + r"""<b>They judge ${INV_VOTES} photos</b></div><span></span><div><i>3</i>""" + COINS + r"""<b>You earn ${INV_PAY} coins</b></div></div>
    <p class="iv-gift">""" + GIFT + r""" Your friends start with ${INV_FRIEND} coins</p>
    <button class="btn block iv-wa" id="invWa">""" + WA + r""" Invite on WhatsApp</button><button class="btn block iv-copy" id="invCopy">""" + LINK.replace('width="40" height="40"', 'width="24" height="24"') + r""" Copy invite link</button>
    ${L.length ? `<div class="iv-head"><b>Your invites</b><b>${p * INV_PAY} coins earned</b></div><div class="inv-l">${L.slice().reverse().map(x => `<div class="inv-r">${fav(x.h, 36)}<b>@${esc(x.h)}</b>${st(x)}</div>`).join('')}</div>` : ''}
    <p class="g2-foot">${left > 0 ? `${p} of ${INV_MAX} rewards earned · ${left} left` : 'You’ve earned all 10 rewards'}</p>
    <div style="text-align:center"><button class="link g2-link" id="invNo">⚖️ Judge photos</button></div></div>`);
  """
s = s.replace(old, new)
s = s.replace('</style>', """.iv2 .iv-k{display:flex;align-items:center;justify-content:center;gap:8px}.iv-e{font:800 2.4rem/1 Fraunces,Georgia,serif;color:#1E3A6E;margin:8px 0 0}
.iv-big{display:flex;align-items:center;justify-content:center;gap:8px;font:900 3.6rem/1 Fraunces,Georgia,serif;color:#1E3A6E;margin:2px 0}.iv-stack{position:relative;width:1em;height:.8em;font-size:.75em;flex:none}.iv-stack i{position:absolute;width:.8em!important;height:.8em!important}.iv-stack i:nth-child(1){left:0;top:.25em}.iv-stack i:nth-child(2){left:.3em;top:.05em}.iv-stack i:nth-child(3){left:.15em;top:-.15em}
.iv-sub{font:800 1.55rem/1.1 Fraunces,Georgia,serif;color:#1E3A6E;margin:0 0 4px}.iv-when{margin:0 0 8px}.iv-cap{display:inline-block;background:#F6DFA0;color:#1E3A6E;font-weight:800;border-radius:999px;padding:6px 18px;margin:0 0 12px}
.iv-steps{display:flex;align-items:flex-start;justify-content:space-between;margin:0 0 10px;color:#1E3A6E}.iv-steps>div{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px}.iv-steps>span{flex:0 0 22px;height:2px;background:#E2C27A;margin-top:52px}
.iv-steps i{width:26px;height:26px;border-radius:50%;background:#F6DFA0;font-style:normal;font-weight:900;line-height:26px;color:#1E3A6E}.iv-steps b{font-size:.9rem;line-height:1.2}
.iv-gift{display:flex;align-items:center;justify-content:center;gap:10px;background:#F6EDD8;border-radius:999px;padding:8px 12px;margin:0 0 12px;font-size:.92rem}
html body .iv2 .btn.iv-wa{display:flex;align-items:center;justify-content:center;gap:10px;background:#1E3A6E!important;color:#fff!important}html body .iv2 .btn.iv-copy{display:flex;align-items:center;justify-content:center;gap:10px;background:transparent!important;color:#1E3A6E!important;box-shadow:inset 0 0 0 2px #1E3A6E!important;margin-top:8px}
.iv-head{display:flex;justify-content:space-between;margin:14px 0 4px;padding-top:12px;border-top:1px solid #E2D3BC;color:#1E3A6E;text-transform:uppercase;font-size:.84rem;letter-spacing:.04em}.iv-head b+b{text-transform:none;letter-spacing:0}
.iv2 .inv-r em.ok{background:none;display:flex;align-items:center;gap:6px;font-size:.95rem}.iv2 .inv-r em .qz3-coin{width:1em;height:1em}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v58 ok')
