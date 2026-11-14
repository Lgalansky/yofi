# Yofi — working rules for Claude

The whole app is a single file, `index.html`, at the root of the repo.

## Two projects: always ask which one
There are two versions of Yofi. Before making any change, ask the user which one it is for, unless they have named it in that message.

| Project | Git branch | Live link | Preview link |
|---|---|---|---|
| **Yofi - Skill** (no real-money chance features) | `main` | https://claude.ai/artifact/SxVfVNedhAE8fQPjbnUGXb | https://claude.ai/artifact/EpaA8hVsAF6QWQmYff4jD8 ("Yofi - Skill (Preview)") |
| **Yofi - Real Money** (licensed: mystery prize spins, shared jackpots) | `real-money` | https://claude.ai/artifact/CsjPAK2KNWaXNdTcx4DAyq | same link |

Each version keeps its own saved player data (`yofi.proto.v1` for Skill, `yofi.real.v1` for Real Money).

## Save every version automatically
After every change to the app, before you finish your reply:

1. Commit the change on that project's branch (`main` for Skill, `real-money` for Real Money) with a short message that says what changed (for example "Add battle countdown timer").
2. Push that branch to `origin` straight away.
3. Republish that project's artifact from the updated `index.html` so the two stay the same. For Skill, changes go to the preview first and only go to the live link when the user says "push live".

Don't wait to be asked, and don't batch several changes into one commit at the end.
