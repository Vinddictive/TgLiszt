from telethon.sync import TelegramClient

api_id = API_ID
api_hash = 'API_HASH'
with TelegramClient('my_session.session', api_id, api_hash) as client:
    print("Your session file has been created successfully!")
