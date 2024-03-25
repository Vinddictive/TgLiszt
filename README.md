Just updated the repo ✨ I've created `telegram.py` that serves as a wrapper for Telethon and Pyrogram, just to make it easier to use.

## Features
- Create Telethon and Pyrogram sessions.
- Login to telegram app using Telethon session file.
- Scrape members' info such as name, username, etc.
- Retrieve all user created groups and channels.

## Example
```python
# Import the necessary classes from 'telegram' module
from telegram import Telegram, TelethonSession, PyrogramSession

# Initialize instances
tg = Telegram()

session_file = "my_session.session"  # Path to your session file.
api_id = 12345678
api_hash = "e90dbf5k91d616a24b..."

# Call the 'login' method from 'Telegram' class
tg.login(session_file, api_id, api_hash)
```


Check out [`🤖 MyOTP!`](https://www.t.me/myotprobot) telegram bot for easy login using a Telethon session string!
