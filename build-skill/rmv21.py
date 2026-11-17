# Real Money build, step 24 (after rmv20.py): landing page = the user's "PhotoPicks" mock-up.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()

SCALES = '<svg viewBox="0 0 64 56" width="62" height="54" fill="none" aria-hidden="true"><g stroke="#E8A21C" stroke-width="3" stroke-linecap="round"><path d="M44 6l3-5M51 11l5-3M53 19h6"/></g><g stroke="#7A1638" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M28 10v38M16 50h24M10 17h36"/><circle cx="28" cy="10" r="3.5" fill="#FBF3EA"/><path d="M10 17L3 33M10 17l7 16M46 17l-7 16M46 17l7 16"/></g><path d="M2 33h16a8 8 0 0 1-16 0zM38 33h16a8 8 0 0 1-16 0z" fill="#E8A21C" stroke="#7A1638" stroke-width="2.6"/><rect x="18" y="47" width="20" height="5" rx="2.5" fill="#B0124A"/></svg>'
CAMPLUS = '<svg viewBox="0 0 64 56" width="62" height="54" fill="none" aria-hidden="true"><g stroke="#E8A21C" stroke-width="3" stroke-linecap="round"><path d="M38 5l2-5M46 9l5-3M48 17h6"/></g><path d="M5 20a5 5 0 0 1 5-5h7l4-5h14l4 5h3a5 5 0 0 1 5 5v22a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5z" stroke="#7A1638" stroke-width="3.2" stroke-linejoin="round"/><circle cx="25" cy="31" r="8.5" stroke="#B0124A" stroke-width="3.6"/><circle cx="47" cy="44" r="9" fill="#E8A21C" stroke="#7A1638" stroke-width="3"/><path d="M47 39.5v9M42.5 44h9" stroke="#7A1638" stroke-width="3" stroke-linecap="round"/></svg>'
CAM = '<svg viewBox="0 0 48 40" width="46" height="38" aria-hidden="true"><path d="M3 12a4 4 0 0 1 4-4h7l3.5-5h13L34 8h7a4 4 0 0 1 4 4v22a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4z" fill="#7A1638"/><circle cx="24" cy="22" r="9" fill="#F8D6DE"/><circle cx="24" cy="22" r="5.5" fill="#7A1638"/></svg>'
SPARK = '<svg viewBox="0 0 48 40" width="46" height="38" aria-hidden="true"><path d="M17 2l3.6 11.4L32 17l-11.4 3.6L17 32l-3.6-11.4L2 17l11.4-3.6z" fill="#F2B21E"/><path d="M36 18l2.2 6.8L45 27l-6.8 2.2L36 36l-2.2-6.8L27 27l6.8-2.2z" fill="#F2B21E"/></svg>'
MEDAL = '<svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><path d="M12 2h8l6 16h-8zM36 2h-8l-6 16h8z" fill="#B0124A"/><path d="M17 2h4l5 14-2 2zM31 2h-4l-5 14 2 2z" fill="#E0457B"/><circle cx="24" cy="31" r="13" fill="#F2B21E" stroke="#C98A0B" stroke-width="2.5"/><path d="M24 23.5l2.3 4.7 5.2.8-3.8 3.6.9 5.1-4.6-2.4-4.6 2.4.9-5.1-3.8-3.6 5.2-.8z" fill="#FFF3C4"/></svg>'

NEW = ('<div class="lp lp2"><h1 class="lp2-brand">PhotoPicks</h1><p class="lp2-sub">Pick your favourite. Cheer it on in the hourly Final.</p>'
   '<div class="lp-pod" id="lpPod"></div><p class="lp-cap lp2-cap">Which photo will take first place?</p>'
   '<div class="lp2-sec"><div class="lp2-row"><span class="lp2-ic">' + SCALES + '</span><div><h2>Judge photos. Get a free pick.</h2><p>Judge photos to earn a free pick. Pick the winner and win real cash.</p></div></div>'
   '<button class="lp-btn" onclick="rmStartVote()">Judge photos <span aria-hidden="true">→</span></button></div>'
   '<div class="lp2-sec"><div class="lp2-row"><span class="lp2-ic">' + CAMPLUS + '</span><div><h2>Your photo could win the Final.</h2><p>Enter your photo and compete for the cash prize.</p></div></div>'
   '<div class="lp2-steps"><div class="s1">' + CAM + '<b>Upload a photo</b><small>Pets, Nature or Garden</small></div><div class="s2">' + SPARK + '<b>Improve quality &amp; qualify</b><small>Enhance with coins</small></div><div class="s3">' + MEDAL + '<b>Pick the top 3 of 6</b><small>In the hourly Final</small></div></div>'
   '<button class="lp-btn" onclick="rmEnterOwn()">Enter your photo <span aria-hidden="true">→</span></button></div>'
   '<div class="lp-ct"><div class="lp-cth"><h2>Meet the contenders</h2><button class="lp-lnk" onclick="rmWatch()">View all →</button></div><p>Choose your favourite. Pick your winner.</p><div class="lp-cg" id="lpCont"></div></div>')
m = re.findall(r'<div class="lp"><h1 class="lp-h">.*?<div class="lp-cg" id="lpCont"></div></div>', s, flags=re.S); assert len(m) == 1, len(m)
s = s.replace(m[0], NEW)

s = s.replace('</style>', """#landing .ca-top .wm{visibility:hidden}.lp2{color:#7A1638}.lp2-brand{font:800 3rem/1 Fraunces,Georgia,serif;color:#7A1638;margin:0 0 8px;letter-spacing:-.01em}.lp2-sub{font:700 1.2rem/1.3 Fraunces,Georgia,serif;color:#7A1638;margin:0 0 16px}
.lp2-cap{font-family:Fraunces,Georgia,serif;color:#2B2320}.lp2-sec{border-top:1px solid #EBD5C4;padding:20px 0 4px;margin:0 0 18px}.lp2-sec:first-of-type{border-top:0}.lp2-row{display:flex;gap:12px;align-items:flex-start;text-align:left;margin-bottom:14px}.lp2-ic{flex:0 0 auto;margin-top:2px}
.lp2 h2{font:800 1.45rem/1.12 Fraunces,Georgia,serif;color:#7A1638;margin:0 0 6px}.lp2-row p{margin:0;font-size:.95rem;color:#3B2A30}
.lp2-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 16px}.lp2-steps div{border-radius:18px;padding:14px 6px 12px;display:flex;flex-direction:column;align-items:center;gap:4px}.lp2-steps .s1{background:#FBDDE3}.lp2-steps .s2{background:#FDE7C8}.lp2-steps .s3{background:#EEDCEB}
.lp2-steps b{font:800 .98rem/1.15 Fraunces,Georgia,serif;color:#7A1638}.lp2-steps small{font-size:.78rem;color:#3B2A30}
html #landing .lp2 button.lp-btn{background:#A80A43!important;font-size:1.25rem!important;padding:14px 16px!important}
html #landing .lp2 h1.lp2-brand,html #landing .lp2 .lp2-sub{color:#7A1638!important}html #landing .lp2 .lp2-cap+.lp2-sec{border-top:0}
.lp2 .lp-ct{border-top:1px solid #EBD5C4}.lp2 .lp-ct h2{color:#7A1638}html #landing .lp2 button.lp-lnk{color:#B0124A!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v21 ok')
