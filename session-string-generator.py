from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Replace 'api_id' and 'api_hash' with your own values
api_id = 28369134
api_hash = 'ee44f7d8d05288b83789dc5df185061d'

# Replace 'session_name' with the name you want to give your session file
session_name = 'my_session'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print(f"Session string for '{session_name}':\n{session_string}")
