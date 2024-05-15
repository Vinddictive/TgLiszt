        # ===== Create telegram sessions. ===== #


# Import 'SessionManager' class from 'telegram' module
from telegram import SessionManager

""" TELETHON SESSIONS """
# Call 'telethon' method from 'SessionManager' class
SessionManager.telethon(session_file=True)  # Create Telethon session file.
# SessionManager.telethon(session_string=True)  # Generate Telethon string session.


""" PYROGRAM SESSIONS """
# # Call 'pyrogram' method from 'SessionManager' class
# SessionManager.pyrogram(session_file=True)  # Create Pyrogram session file.
# SessionManager.pyrogram(session_string=True)  # Generate Pyrogram string session.
