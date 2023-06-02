### GENERATE SESSION FILE ###
from telethon.sync import TelegramClient

api_id = 26892726
api_hash = 'd80afce6c6f8412ce0e9d1ae5a01f8c7'  # Replace with your API hash

with TelegramClient('my_session.session', api_id, api_hash) as client:
    print("Your session file has been created successfully!")


### GENERATE SESSION STRING ###
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 26892726
api_hash = 'd80afce6c6f8412ce0e9d1ae5a01f8c7'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print(f"Your session string:\n{session_string}")


### CREATE SESSION FILE WITH PYROGRAM ###
from pyrogram import Client

api_id = 26892726
api_hash = 'd80afce6c6f8412ce0e9d1ae5a01f8c7'
with Client('my_session', api_id, api_hash) as app:
    app.send_message('me', 'Hello, Pyrogram!')
