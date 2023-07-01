from telethon.sessions import StringSession
from telethon.sync import TelegramClient

api_id = API_ID
api_hash = 'API_HASH'
session_string = '1BVtsOHcBu32FlZFfw7q4wmarTexcaUX3QgQ3skNgYm.....'  # Replace with your session string

client = TelegramClient(StringSession(session_string), api_id, api_hash)


async def send_message():
    chat = await client.get_entity('@john_doe')
    await client.send_message(chat, 'Hello')

    await client.disconnect()

with client:
    client.loop.run_until_complete(send_message())

######################

from telethon.sync import TelegramClient

api_id = API_ID
api_hash = 'API_HASH'
session_file = 'my_session.session'  # Path to your session file

client = TelegramClient(session_file, api_id, api_hash)


async def send_message():
    chat = await client.get_entity('@john_doe')
    await client.send_message(chat, 'Hello')

    await client.disconnect()


with client:
    client.loop.run_until_complete(send_message())
