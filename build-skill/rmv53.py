# Real Money build, step 56 (after rmv52.py): invite friends to judge, earn 100 coins each.
#  - Coins menu row "👥 Invite a friend to judge · +100 coins each" (after the new-player flow).
#  - Pop: how it works, share on WhatsApp / copy link, your invites (Sent -> Joined -> Judged 15 photos · +100).
#  - The friend gets 50 coins to start. You're paid when they've judged 15 photos. Up to 10 paid invites.
#  - Prototype: invited friends join after ~30s and finish judging after ~60s; a pop announces "+100 coins".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("    ${raceBetRowHTML()}${I.length ?", "    ${raceBetRowHTML()}${invRowHTML()}${I.length ?")
s = s.replace("function fcNotify() {", r"""const INV_PAY = 100, INV_FRIEND = 50, INV_VOTES = 15, INV_MAX = 10, INV_FR_NAMES = ['sam_snaps', 'ella.travels', 'jade.k', 'tom_frames', 'nana_bakes', 'catlover22', 'linda.blooms', 'max.adventures'];
const invPaid = () => (S.inv || []).filter(x => x.st === 'paid').length;
function invRowHTML() { if (newbie()) return ''; const p = invPaid(), w = (S.inv || []).filter(x => x.st !== 'paid').length;
  return `<button class="ug-r ug-swap" id="invRow"><span class="ug-i">👥</span><span class="ug-t"><b>Invite a friend to judge</b><small>+${INV_PAY} coins each when they judge ${INV_VOTES} photos${w ? ` · ${w} on the way` : ''}${p ? ` · ${p} paid` : ''}</small></span><em>+${INV_PAY} 🟡</em></button>`; }
function invLink() { const h = (S.user && S.user.h) || 'friend'; return `https://photopicks.app/j/${encodeURIComponent(h)}`; }
function invOpen() { try { closeSheet(); } catch (e) {} const L = S.inv || [], p = invPaid(), left = INV_MAX - p;
  const st = x => x.st === 'paid' ? `<em class="ok">✓ +${INV_PAY} coins</em>` : x.st === 'joined' ? `<em class="mid">Joined · judging ${Math.min(INV_VOTES - 1, x.v || 0)}/${INV_VOTES}</em>` : '<em>Invite sent</em>';
  popOpen(`<div class="pp inv"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button><p class="pp-k">👥 Invite friends</p>
    <h2 class="pp-h">Get ${INV_PAY} coins for every friend who judges</h2>
    <div class="inv-how"><div><i>1</i><b>Send your link</b><small>WhatsApp or anywhere</small></div><div><i>2</i><b>They judge ${INV_VOTES} photos</b><small>They start with ${INV_FRIEND} coins</small></div><div><i>3</i><b>You get ${INV_PAY} coins</b><small>Up to ${INV_MAX} friends</small></div></div>
    <button class="btn block pc-go" id="invWa">📲 Invite on WhatsApp</button><button class="link inv-copy" id="invCopy">🔗 Copy my invite link</button>
    ${L.length ? `<p class="g2-row">Your invites · ${p * INV_PAY} coins earned</p><div class="inv-l">${L.slice().reverse().map(x => `<div class="inv-r">${fav(x.h, 36)}<b>@${esc(x.h)}</b>${st(x)}</div>`).join('')}</div>` : ''}
    <p class="g2-foot">${left > 0 ? `${left} paid invite${left === 1 ? '' : 's'} left` : 'You’ve reached the invite limit'}</p>
    <div style="text-align:center"><button class="link g2-link" id="invNo">⚖️ Judge photos</button></div></div>`);
  const send = how => { if (left <= 0) { toast('You’ve reached the invite limit'); return; } const used = new Set((S.inv || []).map(x => x.h)), h = INV_FR_NAMES.find(n => !used.has(n)) || ('friend' + ((S.inv || []).length + 1));
    S.inv = (S.inv || []).concat({ h, st: 'sent', at: Date.now(), via: how }); save();
    if (how === 'wa') { const msg = `📸 Judge photos on PhotoPicks and pick the hourly Final for real cash prizes. Join with ${INV_FRIEND} free coins:\n${invLink()}`; try { window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank'); } catch (e) {} toast('✓ Sent on WhatsApp. We’ll tell you when they join.'); }
    else { try { navigator.clipboard.writeText(invLink()); } catch (e) {} toast('✓ Link copied. Paste it to a friend.'); } setTimeout(invOpen, 400); };
  $('#invWa').onclick = () => send('wa'); $('#invCopy').onclick = () => send('copy'); $('#invNo').onclick = () => { popClose(); go('judge'); renderJudge(); };
  document.querySelectorAll('#coach [data-shclose]').forEach(b => b.onclick = () => popClose()); }
document.addEventListener('click', e => { if (e.target.closest('#invRow')) { e.preventDefault(); e.stopPropagation(); invOpen(); } }, true);
setInterval(() => { try { if (!S || !S.inv) return; const now = Date.now(); let ch = 0;
  S.inv.forEach(x => { if (x.st === 'sent' && now - x.at > 30000) { x.st = 'joined'; x.jat = now; ch = 1; toast(`👥 @${x.h} joined PhotoPicks from your invite`); }
    if (x.st === 'joined') { x.v = Math.floor((now - x.jat) / 2000); if (x.v >= INV_VOTES && invPaid() < INV_MAX) { x.st = 'paid'; x.pend = 1; S.gems = (S.gems || 0) + INV_PAY; ch = 1; setTimeout(paintGems, 50); } } });
  if (ch) save();
  const pd = S.inv.find(x => x.pend); if (pd && !$('#coach').classList.contains('on') && !$('#sheet').classList.contains('on') && !$('#flow').classList.contains('on')) { pd.pend = 0; save();
    popOpen(`<div class="pp rvw"><p class="rvw-k">👥 Friend bonus</p><b class="rvw-amt">+${INV_PAY} coins</b><p class="rvw-s">Your friend <b>@${esc(pd.h)}</b> judged ${INV_VOTES} photos. Thanks for bringing them to PhotoPicks!</p><button class="btn block rvw-go" id="invMore">👥 Invite another friend</button><div style="text-align:center"><button class="link g2-link" id="invOk">⚖️ Keep judging</button></div></div>`); rvConfetti(document.querySelector('.rvw'), 50); $('#invMore').onclick = () => invOpen(); $('#invOk').onclick = () => popClose(); setTimeout(() => gemExplosion && gemExplosion(INV_PAY, { label: 'Friend invite' }), 400); } } catch (e) {} }, 2000);
function fcNotify() {""", 1)
s = s.replace('</style>', """.inv{text-align:center}.inv-how{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:6px 0 12px}.inv-how div{background:#E3EAF5;border-radius:14px;padding:12px 6px 9px;position:relative}
.inv-how i{position:absolute;top:-9px;left:50%;transform:translateX(-50%);width:20px;height:20px;border-radius:50%;background:#1E3A6E;color:#fff;font-style:normal;font-size:.72rem;font-weight:800;line-height:20px}.inv-how b{display:block;font-size:.84rem;color:#1E3A6E;line-height:1.2}.inv-how small{display:block;font-size:.72rem;opacity:.8;margin-top:2px}
.inv-copy{display:block;margin:8px auto 10px;font-weight:800;color:#1E3A6E!important}.inv-l{text-align:left;margin:0 0 6px}.inv-r{display:flex;align-items:center;gap:10px;padding:6px 2px;border-bottom:1px solid #E2D3BC}.inv-r b{flex:1;font-size:.92rem}
.inv-r em{font-style:normal;font-size:.78rem;padding:2px 9px;border-radius:999px;background:#EEE6D8}.inv-r em.mid{background:#FFF0C7}.inv-r em.ok{background:#E3EAF5;color:#1E3A6E;font-weight:800}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v53 ok')
