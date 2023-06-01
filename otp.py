from telethon.sessions import StringSession  # Function if you want to use session string
from telethon.sync import TelegramClient, events
import re

api_id = 28369134
api_hash = 'ee44f7d8d05288b83789dc5df185061d'
your_session = 'my_session.session'

client = TelegramClient(your_session, api_id, api_hash)
# client = TelegramClient(StringSession(your_session), api_id, api_hash) # Use this if you want to use session string

@client.on(events.NewMessage(from_users=777000))
async def handle_incoming_message(event):
    # Extract OTP from the message using regular expression
    otp = re.search(r'\b(\d{5})\b', event.raw_text)
    if otp:
        print("Your login code:", otp.group(0))

print("Listening for messages...")

with client:
    client.run_until_disconnected()
