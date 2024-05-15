import sqlite3
import json
import csv
import sys
import re

try:
    import pyperclip
except ModuleNotFoundError:
    print("Error: Pyperclip library is not installed. Please install it using 'pip install pyperclip'")
    sys.exit()

try:
    from telethon.sync import TelegramClient, events
    from telethon.sessions import StringSession
    from telethon.tl.types import Channel
    from telethon import functions
    import telethon.errors
except ModuleNotFoundError:
    print("Error: Telethon library is not installed. Please install it using 'pip install telethon'")
    sys.exit()

try:
    from pyrogram import Client, filters
except ModuleNotFoundError:
    print("Error: Pyrogram library is not installed. Please install it using 'pip install pyrogram'")
    sys.exit()


class SessionManager:
    @staticmethod
    def telethon(session_file: bool = False, session_string: bool = False) -> None:
        """
        Create new Telethon sessions.
        :param session_file: Create Telethon session file.
        :param session_string: Generate Telethon string session.
        """
        if session_file:
            api_id_sf = int(input("Enter your API ID: "))
            api_hash_sf = input("Enter your API HASH: ")
            phone = input("Enter your phone number in international format: ")
            password = input("Enter 2-Step Verification: ")
            client1 = TelegramClient(f'{phone}.session', api_id_sf, api_hash_sf)
            client1.start(phone, password)
            print("\n   🟢 Success!")

        elif session_string:
            print("\n   1. Create string session by logging in\n   2. Generate string session from a session file\n")
            session_method = input("Choose how you want to create the session string (Type 1 or 2): ")

            if session_method == "1":
                api_id_ssl = int(input("\nEnter your API ID: "))
                api_hash_ssl = str(input("Enter your API hash: "))
                phone_ssl = input("Enter your phone number in international format: ")
                password_ssl = input("Enter 2-Step Verification: ")
                with TelegramClient(StringSession(), api_id_ssl, api_hash_ssl).start(phone=phone_ssl, password=password_ssl) as client_ssl:
                    session_string_ssl = client_ssl.session.save()
                    pyperclip.copy(session_string_ssl)  # Auto copy the string to Clipboard
                    print(f"\n{session_string_ssl}\n")
                    print(f"    🟢 Success!\n"
                          f"     The session string has been copied to the clipboard.")

            elif session_method == "2":
                api_id = int(input("\nEnter your API ID: "))
                api_hash = input("Enter your API hash: ")
                session_name = input("Enter your Telethon session file name: ")
                try:
                    client = TelegramClient(session_name, api_id, api_hash)
                    string = StringSession.save(client.session)
                    pyperclip.copy(string)
                    print(f"\n{string}\n")
                    print(f"    🟢 Success!\n"
                          f"     The session string has been copied to the clipboard.")
                except sqlite3.OperationalError:
                    print("\nUnable to generate the session string. Please ensure you are using a Telethon session file.")
            else:
                print("Invalid input.")
        else:
            print("Invalid input.")

    @staticmethod
    def pyrogram(session_file: bool = False, session_string: bool = False) -> None:
        """
        Create new Pyrogram sessions.
        :param session_file: Create Pyrogram session file.
        :param session_string: Generate Pyrogram string session.
        """
        if session_file:
            api_id = int(input("Enter your API ID: "))
            api_hash = input("Enter your API HASH: ")
            phone = input("Enter your phone number in international format: ")
            with Client(phone, api_id, api_hash, phone_number=phone) as client:
                client.send_message('me', 'Hi!')
                print("\n   🟢 Success!")

        elif session_string:
            print("\n   1. Create string session by logging in\n   2. Generate string session from a session file\n")
            session_method = input("Choose how you want to create the session string (Type 1 or 2): ")

            if session_method == "1":
                api_id = int(input("\nEnter your API ID: "))
                api_hash = input("Enter your API HASH: ")
                phone = input("Enter your phone number in international format: ")
                with Client(phone, api_id, api_hash, phone_number=phone) as client:
                    pg_string = client.export_session_string()
                    pyperclip.copy(pg_string)
                    print(f"\n{pg_string}\n")
                    print(f"    🟢 Success!\n"
                          f"     The session string has been copied to the clipboard.")
            elif session_method == "2":
                try:
                    api_id = int(input("\nEnter your API ID: "))
                    api_hash = input("Enter your API HASH: ")
                    name = input("Enter your Pyrogram session file name: ")
                    with Client(name, api_id, api_hash) as client:
                        pg_string = client.export_session_string()
                        pyperclip.copy(pg_string)
                        print(f"\n{pg_string}\n")
                        print(f"    🟢 Success!\n"
                              f"     The session string has been copied to the clipboard.")
                except sqlite3.OperationalError:
                    print("\nUnable to generate the session string. Please ensure you are using a Pyrogram session file.")
            else:
                print("Invalid input.")
        else:
            print("Invalid input.")


class Telegram:
    @staticmethod
    def login():
        """
        Login to Telegram using Telethon session file.
        """
        api_id = int(input("Enter your API ID: "))
        api_hash = input("Enter your API HASH: ")
        session_name = input("Enter your Telethon session file name: ")
        try:
            client = TelegramClient(session_name, api_id, api_hash)
            client.connect()
            if client.is_user_authorized():
                print("\n🟢 User Authorized")

                @client.on(events.NewMessage(from_users=777000))  # '777000' is the ID of Telegram Notification Service.
                async def handle_incoming_message(event):
                    otp = re.search(r'\b(\d{5})\b', event.raw_text)
                    if otp:
                        print("OTP received ✅\nYour login code:", otp.group(0))
                        client.disconnect()
                print("Please login to your telegram app. [Listening for OTP...]\n")
                with client:
                    client.run_until_disconnected()
            else:
                print("\n🔴 Authorization Failed\n"
                      "Invalid Telethon session file or the session has expired.")
        except sqlite3.OperationalError:
            print("\nUnable to generate the session string. Please ensure you are using a Telethon session file.")

    @staticmethod
    def userinfo():
        """
        Retrieves information about the current user. (Only support Telethon session file.)
        """
        try:
            api_id = int(input("Enter your API ID: "))
            api_hash = input("Enter your API HASH: ")
            session_name = input("Enter your Telethon session file name: ")
            with TelegramClient(session_name, api_id, api_hash) as client:
                me = client.get_me()

                name = me.first_name if me.first_name else "-"
                username = f'@{me.username}' if me.username else "-"
                user_id = me.id
                phone_number = me.phone
                # You can add more details as needed
                print(
                    f"\n  [ACCOUNT's INFO]\n\n"
                    f"  Name: {name}\n"
                    f"  Username: {username}\n"
                    f"  ID: {user_id}\n"
                    f"  Phone Number: +{phone_number}\n\n"
                    f"1. View all connected devices.\n2. See a list of groups and channels.\n3. Exit.\n"
                    # Add more fields here if needed
                )
                input_user = input("Choose an option by typing its number: ")
                if input_user == "1":
                    result = client(functions.account.GetAuthorizationsRequest())
                    print(result.stringify())

                elif input_user == "2":
                    pub_gr = 0
                    priv_gr = 0
                    pub_ch = 0
                    priv_ch = 0

                    dialogs = client.get_dialogs()
                    created_groups = [dialog for dialog in dialogs if
                                      isinstance(dialog.entity, Channel) and dialog.entity.creator]

                    for group in created_groups:
                        print('\nGroup Name:', group.entity.title)
                        print('Group ID:', group.entity.id)
                        print('Username:', group.entity.username) if group.entity.username else print("Username: [Private]")
                        print('Creation Date:', group.entity.date.strftime('%Y-%m-%d'))
                        print(
                            f'Link: https://www.t.me/{group.entity.username}\n' if group.entity.username else 'Link: [Private]')

                        if group.entity.megagroup:
                            if group.entity.username:
                                pub_ch += 1
                            else:
                                priv_ch += 1
                        else:
                            if group.entity.username:
                                pub_gr += 1
                            else:
                                priv_gr += 1

                    print(
                        f"Public Groups: {pub_gr}\n"
                        f"Private Groups: {priv_gr}\n"
                        f"Public Channels: {pub_ch}\n"
                        f"Private Channels: {priv_ch}\n\n"
                    )

                else:
                    sys.exit()
        except sqlite3.OperationalError:
            print("\nUnable to connect. Please ensure you are using a Telethon session file.")

    @staticmethod
    def member_scrape():
        """
        Scrape member's info from specified group. (Only support Telethon session file.)
        """
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

        api_id = int(input("Enter your API ID: "))
        api_hash = input("Enter your API HASH: ")
        session_name = input("Enter your Telethon session file name: ")
        group = input("Enter target group username (with @): ")
        with TelegramClient(session_name, api_id, api_hash) as client:
            user_entity = client.get_me()
            user_username = user_entity.username if user_entity.username else user_entity.id

            try:
                group_entity = client.get_entity(group)

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
            except telethon.errors.rpcerrorlist.ChatAdminRequiredError as e:
                print(e)
