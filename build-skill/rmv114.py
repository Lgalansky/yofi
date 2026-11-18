# Real Money build, step 117 (after rmv113.py): a winner pick can always be placed.
#  Coin players without 250 coins saw only a greyed-out free-pick button. Now every player gets the stake row and the
#  green "Pick to win · $2" cash button, plus the navy free-pick button when they have the coins (otherwise a line says
#  how many more coins a free pick needs).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
i = s.index("${cash ? `<div class=\"rc-st\" role=\"group\" aria-label=\"Entry\">${RACE_ST.map(v => `<button data-wst=")
j = s.index("<p class=\"pp-r\">Winner pickers share 78%", i)
s = s[:i] + r"""${freeOk && !cash ? `<button class="btn block pc-go pk-go" id="wpFree" ${pick != null ? '' : 'disabled'}>${pick == null ? 'Choose your winner' : `🎟️ Free winner pick · ${FREE_BET_COINS} 🟡`}</button><p class="pp-r">A free pick counts as a $2 pick · or pick with cash:</p>` : ''}
      <div class="rc-st" role="group" aria-label="Entry">${RACE_ST.map(v => `<button data-wst="${v}" aria-pressed="${v === stake}">$${v}</button>`).join('')}</div><button class="btn block pc-go pk-go cashb" id="wpGo" ${pick == null ? 'disabled' : ''}>${pick == null ? 'Choose your winner' : `💵 Pick to win · ${money(stake)}`}</button>
      ${!freeOk && !cash ? `<p class="pp-r">${!fqLeft() ? 'Both free picks used this hour' : `${FREE_BET_COINS - Math.floor(S.gems || 0)} more 🟡 for a free winner pick · ${isYoungW() ? 'judge' : 'vote'} to earn them`}</p>` : ''}
      """ + s[j:]
open(d + 'yofi-real.html', 'w').write(s); print('rm v114 ok')
