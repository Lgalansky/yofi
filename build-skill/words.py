# older-audience wording pass over visible text (classes, ids, styles and code tokens are masked first)
import re
def words(s):
    for x,y in [("$('#ptitle').textContent = 'Battle';","$('#ptitle').textContent = 'Challenges';"),("rematch ? 'Revenge' : 'Battle'}","rematch ? 'Rematch' : 'Challenge'}"),("revenge ? 'Revenge' : 'Battle'}","revenge ? 'Rematch' : 'Challenge'}"),("'CASH' : 'GEMS'} WON","'CASH' : 'COINS'} WON"),("'bonus cash' : 'gems'} balance","'bonus cash' : 'coins'} balance"),("'cash' : 'gems'} in a competition","'cash' : 'coins'} in a competition"),("'won' : 'gems'}</em>","'won' : 'coins'}</em>"),("x.k === 'g' ? 'gems' : 'energy'","x.k === 'g' ? 'coins' : 'energy'"),("'+2 POINTS'","'+2 STARS'")]:
        s=s.replace(x,y)
    keep=[]
    def mask(m): keep.append(m.group(0)); return f'\x00{len(keep)-1}\x00'
    for pat in [r'<style>.*?</style>', r'data:[a-z/+]+;base64,[A-Za-z0-9+/=]+', r'\b(?:class|id|for|data-[\w-]+|href|src|aria-controls)="[^"]*"', r"""['"`][\w.#-]+['"`]""", r'#[\w-]+', r'\.\w+']:
        s=re.sub(pat, mask, s, flags=re.S)
    B=r"(?<![\w$-])"; E=r"(?![\w(=:-])"
    R=[(r'⚔️','🏅'),(r'🪙','🟡'),
       (r'Battle for cash','Compete for cash'),(r'Score to battle','Score to compete'),(r'Battle ready!','Ready to compete!'),(r'1v1 Battle','Head-to-head'),(r'Battle time!','Time to compete!'),(r'Let’s battle','Let’s go'),
       (r'Battle is live','Voting is live'),(r'Battles won–lost','Wins–losses'),(r'Lost battle','Lost'),(r'Cash duel','Cash head-to-head'),(r'Gem raid','Coin challenge'),(r'into a battle:','into a challenge:'),(r'take the crown:','take the blue ribbon:'),(r'steal gems from a rival','win coins from a rival'),
       (r'every raid you fight off','every challenge you hold off'),(r'Battle your mates','Challenge your mates'),(r'Battle friends','Challenge friends'),
       (B+r'BATTLES?'+E,'CHALLENGE'),(B+r'Battles'+E,'Challenges'),(B+r'battles'+E,'challenges'),(B+r'Battle'+E,'Challenge'),(B+r'battle'+E,'challenge'),
       (r'Gem store','Coin store'),(r'Gem packs','Coin packs'),(r'gem packs','coin packs'),(r'Gem Competitions','Coin Competitions'),(r'gem bonus','coin bonus'),(r'gem winners','coin winners'),
       (B+r'GEMS'+E,'COINS'),(B+r'Gems'+E,'Coins'),(B+r'gems'+E,'coins'),(B+r'Gem'+E,'Coin'),(B+r'gem'+E,'coin'),
       (r'Category King','Category champion'),(B+r'King'+E,'Champion'),
       (r'real judge votes','member votes'),(r'Real judges decide','Members decide'),(r'Real judges pick','Members pick'),(r'real judges','real members'),(r'Real judges','Real members'),
       (r'Judges vote','Members vote'),(r'Judges still decide','Members still decide'),(r'judges are voting','members are voting'),(r'judges voting','members voting'),(r'as judges vote','as members vote'),
       (r'Judge photos','Vote on photos'),(r'Judge (\d)',r'Vote on \1'),(r'Judge to','Vote to'),(r'Judge with','Vote with'),(r'to Judge','to Vote'),(r'judging coins','voting coins'),(r'judging gems','voting coins'),
       (r'to judge this match','to vote on this match'),(r'energy to judge','energy to vote'),(B+r'Judges'+E,'Members'),(B+r'judges'+E,'members'),(B+r'Judge'+E,'Vote'),(B+r'judge'+E,'vote'),
       (r'🔥 Revenge','Rematch'),(B+r'Revenge'+E,'Rematch'),(B+r'revenge'+E,'rematch'),(B+r'duel'+E,'head-to-head'),(B+r'fight'+E,'challenge'),
       (r'One more point','One more star'),(r'double points','double stars'),(r'no points at stake','no stars at stake'),(r'Most points','Most stars'),(r'highest points','highest stars'),(r'by points','by stars'),(r'5\+ points','5+ stars'),(r'gallery points','gallery stars'),
       (B+r'crowns?'+E,'blue ribbon'),(B+r'Crown'+E,'Blue ribbon')]
    for a,b in R: s=re.sub(a,b,s)
    while '\x00' in s: s = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], s)
    return s
