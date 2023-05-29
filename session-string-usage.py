from telethon.sessions import StringSession
from telethon.sync import TelegramClient

api_id = 16068827  # Replace with your API ID
api_hash = 'a06fb0c81de133e5efcf9d3f1019540c'
session_string = '1BVtsOHcBu32FlZFfw7q4wmarTexcaUX3QgQ3skNgYm_C5a-EdkbGYwXhY570fAozvYGhpyQd_AC_wYze8s45bn8DxwwGVpXBgxe_NfPAWDpqPhOZObY1bi-5KCQEk6Bn4M08AF5J7Cgbn9vuOk9hMr6GUrbU_hqUgHu1tXGTzUQNvEMkXmDWZ5VY21WMYGKbSmmnLImMcr-jtWPj5W4i87fGA3S-Zjuz9Y9IFhjneiYxv-OK0zuVM8zGLfo_mP3DCFd1a8kbwCW30Hab2DL4YEkk8vf6Fb3QrPfUWpLIaqdMwdZ1QdiorGCJL9M_sHUkRKtI5iwCHrhXj5jdVIAonaL3poP17bE='  # Replace with your session string

client = TelegramClient(StringSession(session_string), api_id, api_hash)


async def send_message():
    chat = await client.get_entity('@stellarstars')
    await client.send_message(chat, 'wkwkwkwkwkw')

    await client.disconnect()

with client:
    client.loop.run_until_complete(send_message())
