# Real Money build, step 7 (after rmv3.py):
#  - "group judging" is called Qualifiers ("Qualifiers · 3pm Pets · 1 of 3")
#  - the Lock in button always looks active (asks for 3 picks if you tap too early)
#  - no "Enter the Best in Show" button on a qualifier result (finalists aren't known yet)
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def R(a, b, n=None):
    global s; c = s.count(a); assert c >= 1 and (n is None or c == n), (a[:90], c); s = s.replace(a, b)

# qualifier pick + result headers
R("<p class=\"pp-k\">🎀 Group ${G.gi + 1} of 3 · the ${raceName(G.ns)} Best in Show</p>", "<p class=\"pp-k\">🎀 Qualifiers · ${raceName(G.ns)} ${esc(showName(ppGame(G.ns).k))} · ${G.gi + 1} of 3</p>", 1)
R("<p class=\"pp-k\">🎀 Group ${G.gi + 1} of 3 · result</p>", "<p class=\"pp-k\">🎀 Qualifiers · ${raceName(G.ns)} ${esc(showName(ppGame(G.ns).k))} · result</p>", 1)
# active Lock in button
R("<button class=\"btn block pc-go\" id=\"gtGo\" ${n3 ? '' : 'disabled'}>", "<button class=\"btn block pc-go\" id=\"gtGo\">", 1)
R("$('#gtGo').onclick = () => { if (picks.length < 3) return;", "$('#gtGo').onclick = () => { if (picks.length < 3) { toast(`Pick your top 3 first · ${3 - picks.length} to go`); return; }", 1)
# no "Enter the Best in Show" on the qualifier result
R("\n    <button class=\"btn block pc-go\" id=\"gtRace\">🎀 Enter the ${raceName(G.ns)} Best in Show</button>", "", 1)
R("$('#gtRace').onclick = () => raceCard(); ", "", 1)
# words everywhere
for a, b in [
 ("`<b>Group judging</b> · pick 3 of 5 ·", "`<b>Qualifiers · ${raceName(ppSlot() + 1)} ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of 5 ·"),
 ("<small>Group judging, then the hourly Best in Show", "<small>Qualifiers, then the hourly Best in Show"),
 ("Group judging is free. Top 2 in a group go through to", "Qualifiers are free. The top 2 in each qualifier go through to"),
 ("Enter it in <b>group judging</b>, free. Top 2 in a group go through", "Enter it in the <b>qualifiers</b>, free. The top 2 in each qualifier go through"),
 ("Top 2 in a group go through.", "Top 2 in each qualifier go through."),
 ("the top 2 in a group go through", "the top 2 in each qualifier go through"),
 ("`Groups: ${hs}` : 'In group judging'", "`Qualifiers: ${hs}` : 'In the qualifiers'"),
 ("`Next group in <b>", "`Next qualifier in <b>"),
 ("to enter group judging`", "to enter the qualifiers`"),
 ("'Enter group judging again'", "'Enter the qualifiers again'"),
 ("`Enter group judging free", "`Enter the qualifiers free"),
 ("decide every group and Best in Show. Group winners get", "decide every qualifier and Best in Show. Qualifier winners get"),
 ("In group judging! First group in", "In the qualifiers! First qualifier in"),
 ("is in group judging! First group in", "is in the qualifiers! First qualifier in"),
 ("in its group. Next group in", "in its qualifier. Next qualifier in"),
 ("🎀 Group result", "🎀 Qualifier result"),
 ("in its group${", "in its qualifier${"),
 ("🎀 Back to group judging · free", "🎀 Back to the qualifiers · free"),
 ("'🎀 Back in group judging!'", "'🎀 Back in the qualifiers!'"),
 ("<small>in group judging</small>", "<small>in the qualifiers</small>"),
 ("Your photos in group judging and the hourly Best in Show", "Your photos in the qualifiers and the hourly Best in Show"),
 ("· next group judging`", "· next qualifier`"),
 ("🎀 Next group for real", "🎀 Next qualifier for real"),
 ("'A group entry'", "'A qualifier entry'"),
 ("'Group win'", "'Qualifier win'"),
 ("already judged this group.", "already judged this qualifier."),
]:
    R(a, b)
open(d + 'yofi-real.html', 'w').write(s); print('rm v4 ok')
