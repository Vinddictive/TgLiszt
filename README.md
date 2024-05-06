Just updated the repo ✨ I've created `telegram.py` that serves as a wrapper for Telethon and Pyrogram, just to make it easier to use.

## Features
- Create Telethon and Pyrogram sessions.
- Login to telegram app using Telethon session file.
- Scrape members' info such as name, username, etc.
- Retrieve all user created groups and channels.


## Installation

1. **Download the Script:**

   - Download the `telegram.py` script and `requirements.txt`
   - Make sure the both files is in the same directory as your main script.

2. **Install Dependencies:**

   - Navigate to your project directory in the terminal.
   - Run the following command to install dependencies from the `requirements.txt` file:
   
     ```sh
     pip install -r requirements.txt
     ```
3. **Write the Code in Your Main Script:**

   Now that you have installed the dependencies and placed the `telegram.py` script in the same directory as your main script, you can start using the module.
   - Copy the code from the "Example" section below and paste it into your main script.
   - Provide a valid Telethon session file and that it is placed in the same directory as your main script. (Please note that the **'login' method in the 'telegram.py' module supports Telethon session files only.** If you are using a Pyrogram session file, this login method won't work.)
   - Make sure to update the session_file, api_id, and api_hash variables with your actual information before running the code.
   
   The directory will be look something like this:
   
![Image Alt Text](https://i.ibb.co/17cR2Yv/Screenshot-2024-05-06-142811.png)

## Example
```python
# Import the 'Telegram' class from 'telegram.py' module
from telegram import Telegram

session_file = "SESSION_NAME.session"  # Your Telethon session file name
api_id = API_ID  # Your API ID
api_hash = "API_HASH"  # Your API HASH

# Call the 'login' method from 'Telegram' class
Telegram.login(session_file, api_id, api_hash)
```


Check out [`🤖 MyOTP!`](https://www.t.me/myotprobot) telegram bot for easy login using a Telethon session string.
