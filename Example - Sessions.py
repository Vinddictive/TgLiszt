# Import 'SessionManager' class from 'telegram' module (make sure `telegram.py` located in the same directory as your main script)
from telegram import SessionManager


"""++++++++++++++++++++++++++++++++++
  How to create Telethon sessions ↓ 
++++++++++++++++++++++++++++++++++"""
# You can simply do it like this
SessionManager.telethon()

# or you can specify the arguments
api_id = ...
api_hash = "..."
phone = "+123..."
SessionManager.telethon(api_id, api_hash, phone)


"""++++++++++++++++++++++++++++++++++
  How to create Pyrogram sessions ↓ 
++++++++++++++++++++++++++++++++++"""
# Same thing, you simply need to change the method with `pyrogram`
SessionManager.pyrogram()


# NOTE: When you create a session file, string session generated automatically.
# To generate a string session from existing session file, instead of entering your phone number, enter your session file name instead.
