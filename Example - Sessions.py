"""
    Create telegram sessions.
"""


# Import the necessary classes from the 'telegram' module
from telegram import TelethonSession, PyrogramSession

# Initialize instances TelethonSession and PyrogramSession
ts = TelethonSession()
ps = PyrogramSession()

# Define API credentials and user information
api_id = 12345678
api_hash = "e90dbf5k91d616a24b..."
phone = "+14155552671"
password = "mypassword123"


""" TELETHON SESSIONS """
# Call the method from 'TelethonSession' class
ts.session_file(api_id, api_hash, phone, password)  # Create Telethon session file
# ts.session_string(api_id, api_hash)  # Get Telethon session string


""" PYROGRAM SESSIONS """
# # Call the method from 'PyrogramSession' class
# ps.session_file(api_id, api_hash, phone)  # Create Pyrogram session file. If the account has 2FA enabled, it will be prompted automatically.
# ps.session_string(api_id, api_hash, phone)  # Get Pyrogram session string
