### GENERATE SESSION FILE ###
from telethon.sync import TelegramClient

api_id = 26892726
api_hash = 'd80afce6c6f8412ce0e9d1ae5a01f8c7'  # Replace with your API hash

with TelegramClient('+6285722891689.session', api_id, api_hash) as client:
    print("Your session file has been created successfully!")


### GENERATE SESSION STRING ###
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Replace 'api_id' and 'api_hash' with your own values
api_id = 28369134
api_hash = 'ee44f7d8d05288b83789dc5df185061d'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print(f"Your session string:\n{session_string}")
