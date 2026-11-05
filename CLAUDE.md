# Yofi — working rules for Claude

The whole app is a single file, `index.html`, at the root of the repo.

## Save every version automatically
After every change to the app, before you finish your reply:

1. Commit the change on `main` with a short message that says what changed (for example "Add battle countdown timer").
2. Push to `origin main` straight away.
3. If the app is also published as a Claude artifact, republish it from the updated `index.html` so the two stay the same.

Don't wait to be asked, and don't batch several changes into one commit at the end.
