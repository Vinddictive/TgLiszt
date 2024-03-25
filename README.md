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
ts = TelethonSession()

# Define API credentials and user information
api_id = API_ID
api_hash = "API_HASH"
phone = "PHONE_NUMBER"
password = "2FA"  # Optional

# Call the 'session_file' method from 'TelethonSession' class
ts.session_file(api_id, api_hash, phone, password)
```
