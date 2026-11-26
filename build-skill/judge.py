# Skill preview: voting accuracy as progression, without new clutter.
# The 🔥 pill keeps showing just your streak days. A thin gold ring around the flame fills
# towards your next judge level, and "+1 ✓" pops on it when a vote matches the crowd.
# Tap the pill for your judge card: level, progress to the next one, two goals with coin
# rewards, and a league of players with a similar number of votes (simulated).
# Accuracy = how often your pick matches the crowd, over your last 50 votes.
# Levels: New judge (<20 votes), Good Eye, Sharp Eye 65%+, Expert 75%+ (+1 coin a correct vote),
# Master 85%+ (+2 coins a correct vote).
# usage: python3 build-skill/judge.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- judge score: accuracy over the last 50 votes, levels, goals ----
const JG_WIN = 50, JG_MIN = 20;
const JG_LV = [{ n: 'Good Eye', at: 0, ic: '👀' }, { n: 'Sharp Eye', at: 65, ic: '🎯' }, { n: 'Expert', at: 75, ic: '🏅', bonus: 1 }, { n: 'Master', at: 85, ic: '👑', bonus: 2 }];
const jgHist = () => S.jgH || (S.jgH = []);
const jgN = () => jgHist().length;
const jgAcc = () => { const h = jgHist(); return h.length ? Math.round(h.reduce((a, b) => a + b, 0) / h.length * 100) : 0; };
const jgLv = () => { if (jgN() < JG_MIN) return null; const a = jgAcc(), raw = JG_LV.filter(l => a >= l.at).pop(), had = JG_LV.find(l => l.n === S.jgLvN);
  return had && JG_LV.indexOf(had) > JG_LV.indexOf(raw) && a >= had.at - 3 ? had : raw; }; // a level only drops when you fall 3% below it
const jgNext = () => { const l = jgLv(); if (!l) return null; return JG_LV[JG_LV.indexOf(l) + 1] || null; };
const jgProg = () => { const l = jgLv(); if (!l) return jgN() / JG_MIN; const nx = jgNext(); if (!nx) return 1; return Math.max(0, Math.min(1, (jgAcc() - l.at) / (nx.at - l.at))); };
// goal 1: 8 of your next 10 right (+20 coins); goal 2: reach the next level
const jgBatch = () => S.jgB || (S.jgB = { n: 0, ok: 0 });
let JG_SEEN = S.eyeN || 0, JG_OK = S.eyeOk || 0;
function jgVote(ok) {
  const h = jgHist(); h.push(ok ? 1 : 0); if (h.length > JG_WIN) h.shift();
  const was = S.jgLvN || null, l = jgLv(); let msg = null;
  const b = jgBatch(); b.n++; if (ok) b.ok++;
  if (b.n >= 10) { if (b.ok >= 8) { S.gems += 20; msg = { t: '8 of 10 right!', s: '+20 coins for a sharp eye' }; try { setTimeout(() => _gemExplosionJ(20, { mid: 1, from: $('#sFlame') }), 400); } catch (e) {} } S.jgB = { n: 0, ok: 0 }; }
  if (ok && l && l.bonus) { S.gems += l.bonus; S.jgBonus = (S.jgBonus || 0) + l.bonus; }
  if (l && l.n !== was) { const up = !was || JG_LV.findIndex(x => x.n === l.n) > JG_LV.findIndex(x => x.n === was); S.jgLvN = l.n; if (up && (was || jgN() === JG_MIN)) msg = { t: `You’re ${/^[AEIOU]/.test(l.n) ? 'an' : 'a'} ${l.n}! ${l.ic}`, s: l.bonus ? `+${l.bonus} coin${l.bonus > 1 ? 's' : ''} on every correct vote` : `${jgAcc()}% of your votes match the crowd` }; }
  save(); try { paintGems(); } catch (e) {} jgPaint(ok);
  if (msg) setTimeout(() => toast(`${msg.t} ${msg.s}`), 900);
}
setInterval(() => { const n = S.eyeN || 0; if (n > JG_SEEN) { const ok = (S.eyeOk || 0) > JG_OK; JG_SEEN = n; JG_OK = S.eyeOk || 0; jgVote(ok); } }, 250);
// the pill: days stay the number; the ring is your progress to the next judge level
function jgPaint(pop) { const b = $('#sFlame'); if (!b) return; let r = b.querySelector('.jg-ring'); const fl = b.querySelector('.fl');
  if (!r && fl) { fl.insertAdjacentHTML('beforebegin', '<i class="jg-ring" aria-hidden="true"></i>'); r = b.querySelector('.jg-ring'); }
  if (r) r.style.setProperty('--p', Math.round(jgProg() * 100));
  const l = jgLv(); b.setAttribute('aria-label', `${$('#sFlameN') ? $('#sFlameN').textContent : 0} day streak. Judge score ${l ? jgAcc() + '% · ' + l.n : jgN() + ' of ' + JG_MIN + ' votes'}`);
  if (pop === true) { let t = b.querySelector('.jg-pop'); if (t) t.remove(); b.insertAdjacentHTML('beforeend', '<i class="jg-pop" aria-hidden="true">+1 ✓</i>'); setTimeout(() => { const x = b.querySelector('.jg-pop'); if (x) x.remove(); }, 1300); } }
const _paintFlameJ = paintFlame;
paintFlame = function () { const r = _paintFlameJ.apply(this, arguments); jgPaint(); return r; };
// a small league of players who have voted about as much as you (simulated)
function jgLeague() { const a = jgAcc(), n = Math.max(jgN(), S.eyeN || 0), lo = Math.max(0, Math.floor(n / 50) * 50), hi = lo + 50;
  const names = ['nina.paws', 'kai.shoots', 'marco_eats', 'luna_loves', 'theo.snaps', 'ivy.frames', 'sam_wild'];
  const others = names.map((h, i) => ({ h, a: Math.max(40, Math.min(95, a + ((hsh(h + dayKey()) % 17) - 8))) }));
  const all = [...others, { h: 'you', a, me: 1 }].sort((x, y) => y.a - x.a || (y.me ? 1 : -1)); const i = all.findIndex(x => x.me);
  return { rows: all.slice(Math.max(0, i - 1), Math.max(0, i - 1) + 3).map(r => ({ ...r, rank: all.indexOf(r) + 1 })), band: `${lo}–${hi} votes`, rank: i + 1, of: all.length }; }
function judgeCard() { const l = jgLv(), nx = jgNext(), a = jgAcc(), ds = dailyState(), b = jgBatch(), L = jgLeague();
  const head = l ? `<div class="jg-big"><b>${a}%</b><span>${l.ic} ${l.n}<small>${jgN()} recent votes match the crowd ${a}% of the time</small></span></div>`
    : `<div class="jg-big"><b>${jgN()}/${JG_MIN}</b><span>🎯 Judge score<small>Vote ${JG_MIN - jgN()} more to get your score</small></span></div>`;
  const bar = `<div class="jg-lv"><span>${l ? l.n : 'New judge'}</span><span>${nx ? `${nx.n} at ${nx.at}%${nx.bonus ? ` · +${nx.bonus} 🟡 a correct vote` : ''}` : l ? 'Top level' : `Score at ${JG_MIN} votes`}</span></div><div class="jg-bar"><i style="width:${Math.round(jgProg() * 100)}%"></i></div>`;
  const goals = `<div class="jg-gs"><div class="jg-g"><span class="jg-gi">🎯</span><span><b>Get 8 of your next 10 right</b><small>${b.ok}/${b.n} so far</small></span><em>+20 🟡</em></div>
    <div class="jg-g"><span class="jg-gi">${nx ? nx.ic : '🏆'}</span><span><b>${nx ? `Reach ${nx.n} (${nx.at}%)` : l ? 'Stay a Master' : `Vote ${JG_MIN - jgN()} more`}</b><small>${nx && nx.bonus ? `Then every correct vote pays +${nx.bonus} 🟡` : l ? `${l.bonus ? `+${l.bonus} 🟡 every correct vote` : 'Keep matching the crowd'}` : 'Unlocks your judge level'}</small></span><em>${nx && nx.bonus ? `+${nx.bonus} 🟡` : ''}</em></div></div>`;
  const lg = l ? `<div class="jg-lg"><h4>Your league · players with ${L.band}</h4>${L.rows.map(r => `<div class="jg-r ${r.me ? 'me' : ''}"><i>${r.rank}</i><b>${r.me ? 'You' : '@' + esc(r.h)}</b><em>${r.a}%</em></div>`).join('')}</div>` : '';
  openSheet(`<div class="jg"><h2>Your judge score</h2><p class="jg-sub">How often you pick the photo most voters choose · 🔥 ${ds.streak}-day streak</p>${head}${bar}${goals}${lg}
    <button class="btn block jg-go" data-shclose>Keep voting</button></div>`); }
$('#sFlame').onclick = () => judgeCard();
setTimeout(() => { try { jgPaint(); } catch (e) {} }, 400);
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* judge ring on the streak pill */
#sFlame{position:relative}#sFlame.cold .jg-ring{filter:none;opacity:1}
#sFlame .jg-ring{position:absolute;left:3px;top:50%;width:26px;height:26px;margin-top:-13px;border-radius:50%;background:conic-gradient(#E0A82E calc(var(--p,0)*1%),#E7DCC7 0);-webkit-mask:radial-gradient(circle,transparent 9px,#000 9.5px);mask:radial-gradient(circle,transparent 9px,#000 9.5px);pointer-events:none;transition:background .6s}
#sFlame .jg-pop{position:absolute;left:50%;top:-12px;transform:translateX(-50%);font:900 .68rem "Nunito Sans",sans-serif;font-style:normal;white-space:nowrap;color:#21784A;background:#DDF1E2;padding:1px 6px;border-radius:99px;animation:jgPop 1.3s ease-out forwards;pointer-events:none}
@keyframes jgPop{0%{opacity:0;transform:translate(-50%,6px)}20%{opacity:1;transform:translate(-50%,0)}80%{opacity:1}100%{opacity:0;transform:translate(-50%,-6px)}}
/* judge card */
.jg h2{margin:0;text-align:center;font:900 1.6rem Fraunces,serif;color:#1F3157}.jg-sub{text-align:center;margin:2px 0 12px;font-size:.88rem;color:#4E433C}
.jg-big{display:flex;align-items:center;justify-content:center;gap:14px;margin-bottom:10px}.jg-big b{font:900 3.2rem/1 Fraunces,serif;color:#1F3157}.jg-big span{font:900 1.15rem Fraunces,serif;color:#1F3157}.jg-big small{display:block;max-width:170px;font:700 .78rem/1.3 "Nunito Sans",sans-serif;color:#4E433C;margin-top:3px}
.jg-lv{display:flex;justify-content:space-between;gap:8px;font:800 .78rem "Nunito Sans",sans-serif;color:#4E433C;margin:0 2px 5px}.jg-bar{height:10px;border-radius:9px;background:#E7DCC7;overflow:hidden;margin-bottom:12px}.jg-bar i{display:block;height:100%;background:linear-gradient(90deg,#E0A82E,#F3D27A);border-radius:9px}
.jg-gs{display:grid;gap:8px;margin-bottom:12px}.jg-g{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:14px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE}.jg-gi{font-size:1.4rem}.jg-g span:nth-child(2){flex:1}.jg-g b{display:block;font:800 .95rem "Nunito Sans",sans-serif;color:#2D2521}.jg-g small{font:700 .78rem "Nunito Sans",sans-serif;color:#4E433C}.jg-g em{font-style:normal;font:900 .95rem Fraunces,serif;color:#8A5A0A;white-space:nowrap}
.jg-lg{background:#FFFDF9;border-radius:14px;box-shadow:inset 0 0 0 1.5px #E2D5BE;padding:8px 10px;margin-bottom:12px}.jg-lg h4{margin:0 0 4px;font:800 .72rem "Nunito Sans",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#4E433C}
.jg-r{display:flex;align-items:center;gap:10px;padding:5px 6px;font-weight:700}.jg-r i{font-style:normal;width:20px;color:#4E433C}.jg-r b{flex:1;font-weight:800}.jg-r em{font-style:normal;font:900 1rem Fraunces,serif;color:#1F3157}.jg-r.me{background:#E6EDF8;border-radius:10px}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('judge ok')
