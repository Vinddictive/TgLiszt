### TELETHON SESSION FILE ###
from telethon.sync import TelegramClient

api_id = API_ID
api_hash = 'API_HASH'
with TelegramClient('my_session.session', api_id, api_hash) as client:
    print("Your session file has been created successfully!")

------------------------------------------

### TELETHON SESSION FILE WITH 2FA HANDLER ###
from telethon.sync import TelegramClient

api_id = API_ID
api_hash = 'API_HASH'

client = TelegramClient('my_session.session', api_id, api_hash)
client.start('PHONE_NUMBER', '2FA_HERE')

------------------------------------------

### TELETHON SESSION STRING ###
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = API_ID
api_hash = 'API_HASH'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print(f"Your session string:\n{session_string}")

------------------------------------------

### PYROGRAM SESSION FILE ###
from pyrogram import Client

api_id = API_ID
api_hash = 'API_HASH'
with Client('my_session', api_id, api_hash) as app:
    app.send_message('me', 'Hello, Pyrogram!')
