import json
from telethon.sync import TelegramClient

# Configure your API credentials
api_id = API_ID
api_hash = 'API_HASH'

# Connect to Telegram
with TelegramClient('session_name', api_id, api_hash) as client:
    # Get the target group
    group_entity = client.get_entity('@transilk')

    # Retrieve all participants in the group
    participants = client.get_participants(group_entity)

    user_info_list = []

    for participant in participants:
        user_id = participant.id
        username = participant.username if participant.username else ""
        full_name = participant.first_name
        if participant.last_name:
            full_name += " " + participant.last_name

        user_info = {
            'user_id': user_id,
            'username': username,
            'full_name': full_name,
        }
        user_info_list.append(user_info)

    # Save user information to a JSON file
    with open('user_info.json', 'w') as file:
        json.dump(user_info_list, file, indent=4)

    print("User information saved to 'user_info.json' file.")
