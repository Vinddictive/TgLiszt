from telethon.sync import TelegramClient, events
import re

api_id = 28369134
api_hash = 'ee44f7d8d05288b83789dc5df185061d'
session_file = 'session.session'

client = TelegramClient(session_file, api_id, api_hash)


@client.on(events.NewMessage(from_users=777000))
async def handle_incoming_message(event):
    # Extract OTP from the message using regular expression
    otp = re.search(r'\b(\d{5})\b', event.raw_text)
    if otp:
        print("Your login code:", otp.group(0))

print("Listening for messages...")

with client:
    client.run_until_disconnected()
