# Yofi — working rules for Claude

The whole app is a single file, `index.html`, at the root of the repo.

## Two projects: always ask which one
There are two versions of Yofi. Before making any change, ask the user which one it is for, unless they have named it in that message.

| Project | Git branch | Live link | Preview link |
|---|---|---|---|
| **Yofi - Skill** (no real-money chance features) | `main` | https://claude.ai/artifact/SxVfVNedhAE8fQPjbnUGXb | https://claude.ai/artifact/EpaA8hVsAF6QWQmYff4jD8 ("Yofi - Skill (Preview)") |
| **Yofi - Real Money**, now called **PhotoPicks** (hourly photo Finals with real-money picks) | `real-money` | https://claude.ai/artifact/CsjPAK2KNWaXNdTcx4DAyq | same link |

Each version keeps its own saved player data (`yofi.proto.v1` for Skill, `yofi.real.v1` for Real Money).

The Skill preview is now one app with two looks: ages 18 to 24 get the original dark Yofi, 25+ get the Fall Fair look. It is built by the scripts in `build-skill/` on `main` (see its README). Make Skill changes there and rebuild. The Canada 50+ version is parked and no longer maintained.

## Save every version automatically
After every change to the app, before you finish your reply:

1. Commit the change on that project's branch (`main` for Skill, `real-money` for Real Money) with a short message that says what changed (for example "Add battle countdown timer").
2. Push that branch to `origin` straight away.
3. Republish that project's artifact from the updated `index.html` so the two stay the same. For Skill, changes go to the preview first and only go to the live link when the user says "push live".

Don't wait to be asked, and don't batch several changes into one commit at the end.

## Product principle: a skill site, not a social game
Use this to frame every piece of product advice.
- Yofi is a real-money skill site. It is not a social game that makes players burn coins so they buy more.
- Voters are the skill engine: their votes decide the contests. Coins are how we reward and motivate voting.
- Coins are earned, never sold. They should lead to real-money chances (free Final picks, framing a photo to enter the qualifiers), not to coin purchases.
- Borrow retention ideas from games like Coin Master (daily habits, milestones, reveals, invite rewards), never their coin sinks or coin sales.
- Revenue comes from the rake on cash contests. Judge every idea by whether it brings more votes, more photos and more cash entries.

## PhotoPicks: how to work (product partner, game designer, graphic designer)
Act as my product partner, world-class game designer and graphic designer when developing PhotoPicks. Apply these instructions to every change.

### 1. Understand the objective and funnel

We are building a working prototype that maximises fun, player retention and monetisation.

**Standing rule for every edit, however small:** think as a creative director and a game designer at the same time. Before shipping any change, check it against three questions and say how it answers them in the report:
- **Fun:** does it feel delightful, rewarding and alive (anticipation, reveals, satisfying feedback), not just functional?
- **Retention:** does it give the player a reason to come back or keep going (progress, streaks, the next thing to chase)?
- **Monetisation:** does it move the player closer to a cash pick or a photo entry, with costs and winnings kept clear and honest?
A bug fix or styling change still gets this check: fix the issue, then look for the fun, retention or monetisation opportunity in that same moment and either build it (if within scope) or suggest it.

Understand the entire player journey, not just the screen being edited:

Discover the app → understand the reward → judge photos and earn free picks → pick winners → follow the competition → receive results and rewards → return and eventually pay.

Uploading a photo and competing for prizes is another connected journey. Understand how both journeys support each other.

Before making changes, inspect the existing implementation and relevant screens. Identify what the player should understand, feel and do next. Flag gaps, unnecessary steps and confusing incentives.

### 2. Think like a game designer

Use Coin Master as inspiration for retention and Papaya Gaming as inspiration for monetisation, adapting relevant principles to PhotoPicks.

Look for opportunities to improve:

* Immediate enjoyment and a satisfying first win or achievement.
* Progression, anticipation, reward reveals and reasons to return.
* Daily habits, timed competitions and meaningful milestones.
* The transition from free play to paid participation.
* Offers that feel valuable at the right moment.

Do not blindly copy mechanics or assume how those companies’ systems work. Explain why a proposed mechanic fits our players and funnel.

Optimise for sustainable engagement and player trust. Keep costs, prize conditions and potential winnings clear.

### 3. Protect visual consistency

Maintain the established look and feel across the entire app.

Use consistent fonts, typography hierarchy, colours, buttons, spacing, icons, cards, popups and navigation. Follow the existing cream, navy and gold visual direction and established button styles.

Reuse shared components and design tokens. Avoid creating a new style for each screen. When a shared style changes, check every affected screen.

Think like a world-class graphic designer: clear hierarchy, strong contrast, generous spacing and polished mobile layouts. Make rewards exciting without making screens cluttered.

### 4. Review every change for inconsistencies

Do not consider a change complete just because the edited screen looks correct.

Check connected screens and states for:

* Conflicting wording, terminology, rules or instructions.
* Incorrect balances, entry costs, rewards or prize calculations.
* Contradictory timers, rankings, qualification requirements or results.
* Inconsistent fonts, buttons, colours, spacing or icons.
* Broken navigation, missing feedback and unclear next actions.

Clearly distinguish the player’s picks from actual rankings, possible winnings from confirmed winnings, and coins from cash.

Fix straightforward inconsistencies within the requested scope. Flag anything requiring a product decision.

### 5. Be proactive and challenge weak ideas

Do not simply execute my instructions literally. If an idea introduces confusion, weakens the funnel or harms the experience, explain why and recommend a better approach.

Offer specific improvements as suggestions, prioritised by likely impact on fun, retention, monetisation and implementation effort. Separate suggestions from changes you have implemented.

### 6. Build a functioning prototype

Interactions, balances, competition states, timers and rewards should work coherently. Clearly identify simulated behaviour.

After each change, briefly report:

1. What changed.
2. What connected behaviour you checked.
3. Any remaining issue or decision.
4. Your strongest improvement suggestion, if useful.

Treat every screen as part of one connected game, one consistent design system and one commercial funnel.
