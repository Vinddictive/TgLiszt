"""
    Login to telegram app using Telethon session file.
"""


# Import the 'Telegram' class from 'telegram' module
from telegram import Telegram

# Initialize an instance of the 'Telegram' class
tg = Telegram()

session_file = "my_session.session"  # Path to your session file.
api_id = 12345678
api_hash = "e90dbf5k91d616a24b..."

# Call the 'login' method from 'Telegram' class
tg.login(session_file, api_id, api_hash)
