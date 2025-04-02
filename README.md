# silly cat

does some mischief

- for any message sent, randomizes all users' display names (except owner and bots, cuz Discord perms lol)
- for any message sent, the author user has a chance to be kicked lmao
- `silly reset <password>`: resets all nicknames back to original (if you entered password correctly heh)
- `silly quiet`: toggles if silly cat will send log message (e.g. successfully did mischief)

### Running
IDK minimum permissions required. It definitely needs manage nicknames, kick members, sending messages, and tracker members joining (to get list of all members). I just set to admin lol

Make sure bot role has appropriate level (I set mine to all the way at top)

Install stuff in `requirements.txt`, add `DISCORD_TOKEN` to `.env`, run `main.py`, and let it roll.

