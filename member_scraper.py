"""

        Gathering member's info from specified group.
        Watch the demo here: https://www.youtube.com/watch?v=FyrhRElpS0I

"""

from telethon.sync import TelegramClient
import json
import csv

api_id = API_ID
api_hash = 'API_HASH'

session = 'my_session.session'
target_group = "@group_username"  # Group username with @


def json_save():
    user_info_json = []
    for participant in participants:
        if not participant.bot:
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
            user_info_json.append(user_info)

        with open('user_info.json', 'w') as file:
            json.dump(user_info_json, file, indent=4)

    print("User information saved to 'user_info.json' file.")


def csv_save():
    user_info_csv = []
    for participant in participants:
        if not participant.bot:
            user_id = participant.id
            username = participant.username if participant.username else "-"
            full_name = participant.first_name
            if participant.last_name:
                full_name += " " + participant.last_name
    
            user_info_csv.append([user_id, username, full_name])
    
        with open('user_info.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'full_name'])
            writer.writerows(user_info_csv)

    print("User information saved to 'user_info.csv' file.")


with TelegramClient(session, api_id, api_hash) as client:
    user_entity = client.get_me()
    user_username = user_entity.username if user_entity.username else user_entity.id

    try:
        group_entity = client.get_entity(target_group)

        group_name = group_entity.title
        group_username = group_entity.username if group_entity.username else group_entity.id
        participant_count = client.get_participants(group_entity, limit=0).total
        creation_date = group_entity.date.strftime('%B %d, %Y')
        group_id = group_entity.id

        print(
            f"""
    ● Login as @{user_username}
    
        [ Group Info ]
        Name: {group_name}
        ID: {group_id}
        Username: @{group_username}
        Participants: {participant_count}
        Creation Date: {creation_date}
            """
        )

        while True:
            print("[1] JSON\n[2] CSV")
            save_as = input("Save as file. (1/2)? :  ")
            try:
                member_limit = int(input("Participants limit (e.g 200) :  "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
            participants = client.get_participants(group_entity, limit=member_limit)

            if save_as == "1":
                json_save()
                break
            elif save_as == "2":
                csv_save()
                break
            else:
                print("Invalid input. Type 1 to save as JSON. Type 2 to save as CSV file.")
                continue
    except ValueError:
        print("The group username does not exist or invalid.")
