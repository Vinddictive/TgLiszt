from telethon.sync import TelegramClient, events

api_id = 28369134
api_hash = 'ee44f7d8d05288b83789dc5df185061d'

session_file = 'C:/Users/dodyx/sessions/new.session'

client = TelegramClient(session_file, api_id, api_hash)


@client.on(events.NewMessage())
async def handle_incoming_message(event):
    sender = await event.get_sender()
    username = sender.username or ''
    print(f'👤 {sender.id} (@{username}): {event.message.message}')


    # Get the input message from the terminal
    while True:
        message = input("🖋️ Send messsage: ")

        # Check if the message is a command to send a message to a specific user
        if message.startswith('/sendto'):
            # Parse the command to extract the username or ID of the user to send the message to
            _, user_identifier, message = message.split(' ', 2)
            user_identifier = user_identifier.strip()

            try:
                if user_identifier.startswith('@'):
                    # If the identifier starts with '@', assume it's a username
                    user = await client.get_entity(user_identifier)
                else:
                    # Otherwise, assume it's an ID and convert it to an integer
                    user = await client.get_entity(int(user_identifier))

                await client.send_message(user, message)
                print(f'Message sent to {user.username} ({user.id})')
            except ValueError:
                print('Invalid username or ID')
        else:
            await client.send_message(event.sender_id, message)


# Start the TelegramClient
with client:
    client.run_until_disconnected()
