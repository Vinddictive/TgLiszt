"""
    Scrape members' information such as name, username, etc., from a specified chat (group).
"""


# Import the 'Telegram' class from 'telegram' module
from telegram import Telegram

# Initialize an instance of the 'Telegram' class
tg = Telegram()

api_id = 12345678
api_hash = "e90dbf5k91d616a24b..."
session_file = "my_session.session"  # Path to your session file.
group = "@target_group"  # Group username with '@'

# Call the 'member_scrape' method from 'Telegram' class
tg.member_scrape(api_id, api_hash, session_file, group)
