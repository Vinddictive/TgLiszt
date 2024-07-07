import winsound
import sqlite3
import json
import csv
import sys
import re

try:
    import pyperclip
except ModuleNotFoundError:
    print("\n―― ⚠️ Pyperclip library is not installed. Please install it using 'pip install pyperclip'")
    sys.exit()

try:
    from telethon.sync import TelegramClient, events
    from telethon.sessions import StringSession
    from telethon.tl.types import Channel
    from telethon import functions
    import telethon.errors
except ModuleNotFoundError:
    print("\n―― ⚠️ Telethon library is not installed. Please install it using 'pip install telethon'")
    sys.exit()

try:
    from pyrogram import Client, filters
except ModuleNotFoundError:
    print("\n―― ⚠️ Pyrogram library is not installed. Please install it using 'pip install pyrogram'")
    sys.exit()


class SessionManager:
    @staticmethod
    def telethon(api_id: int = None, api_hash: str = None, phone: str = None, password=None,
                 session_file: bool = False, session_string: bool = False):
        """
        Create a Telegram session using Telethon.

        This method allows you to create a Telegram session either as a session file or as a session string.

        All parameters are optional (except 'session_file' and 'session_string'). If not provided, you will be prompted to enter them.

        If `session_string` is set to True, you will be prompted to choose between:

        [1] Creating a string session by logging in.

        [2] Generating a string session from an existing session file.

        :param api_id: Your Telegram API ID.
        :param api_hash: Your Telegram API hash.
        :param phone: Your phone number in international format.
        :param password: Your 2-Step Verification password.
        :param session_file: If True, create a Telethon session file.
        :param session_string: If True, generate a Telethon string session.
        """

        if session_file and session_string or not session_file and not session_string:
            print("\n―― ℹ️ Please specify a valid session type."
                  "\n―― To create a Telethon session file, set 'session_file' to True."
                  "\n―― To generate a Telethon string session, set 'session_string' to True.")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            return

        try:
            if api_id and api_hash and phone:
                my_api_id = api_id
                my_api_hash = api_hash
                my_phone = phone
                my_pwd = password
            else:
                my_api_id = int(input("Enter your API ID: "))
                my_api_hash = input("Enter your API HASH: ")
                my_phone = input("Enter your phone number in international format: ")
                my_pwd = input("Enter 2-Step Verification: \n")

            if session_file:
                client = TelegramClient(f'{my_phone}.session', my_api_id, my_api_hash)
                client.start(my_phone, my_pwd)
                print("\n―― 🟢 Session file created successfully!")
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            elif session_string:
                print("\n―― [1]. Create string session by logging in\n―― [2]. Generate string session from existing session file")
                session_method = input("\n―― Choose how you want to create the session string: ")

                if session_method == "1":
                    with TelegramClient(StringSession(), my_api_id, my_api_hash).start(phone=my_phone, password=my_pwd) as client:
                        my_string = client.session.save()
                        pyperclip.copy(my_string)  # Auto copy the string to Clipboard
                        print(f"\n{my_string}")
                        print("\n―― 🟢 String session created successfully!"
                              f"\n―― String copied to clipboard!")
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

                elif session_method == "2":
                    session_name = input("Enter your Telethon session file name: ")
                    try:
                        client = TelegramClient(session_name, my_api_id, my_api_hash)
                        string = StringSession.save(client.session)
                        pyperclip.copy(string)
                        print(f"\n{string}\n")
                        print("\n―― 🟢 String session generated successfully!"
                              f"\n―― String copied to clipboard!")
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    except sqlite3.OperationalError:
                        print("\n―― ⚠️ Unable to generate the session string. Please ensure you are using a Telethon session file.")
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                else:
                    print("\n―― ⚠️ Invalid input. Please type '1' to create a new string session or '2' to generate a string session from an existing session file.")
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        except Exception as e:
            print(f"\n―― ❌ An error has occurred: {e}")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

    @staticmethod
    def pyrogram(api_id: int = None, api_hash: str = None, phone: str = None, session_file: bool = False, session_string: bool = False):
        """
        Create a Telegram session using Pyrogram.

        This method allows you to create a Telegram session either as a session file or as a session string.

        All parameters are optional (except 'session_file' and 'session_string'). If not provided, you will be prompted to enter them.

        If `session_string` is set to True, you will be prompted to choose between:

        [1] Creating a string session by logging in.

        [2] Generating a string session from an existing session file.

        :param api_id: Your Telegram API ID.
        :param api_hash: Your Telegram API hash.
        :param phone: Your phone number in international format.
        :param session_file: If True, create a Pyrogram session file.
        :param session_string: If True, generate a Pyrogram string session.
        """

        if session_file and session_string or not session_file and not session_string:
            print("\n―― ℹ️ Please specify a valid session type."
                  "\n―― To create a Pyrogram session file, set 'session_file' to True."
                  "\n―― To generate a Pyrogram string session, set 'session_string' to True.")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            return

        try:
            if api_id and api_hash and phone:
                my_api_id = api_id
                my_api_hash = api_hash
                my_phone = phone
            else:
                my_api_id = int(input("Enter your API ID: "))
                my_api_hash = input("Enter your API HASH: ")
                my_phone = input("Enter your phone number in international format: ")

            if session_file:
                with Client(my_phone, my_api_id, my_api_hash, phone_number=my_phone) as client:
                    client.send_message('me', 'Hi!')
                    print("\n―― 🟢 Session file created successfully!")
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            elif session_string:
                print("\n―― [1]. Create string session by logging in\n―― [2]. Generate string session from existing session file")
                session_method = input("\n―― Choose how you want to create the session string: ")

                if session_method == "1":
                    with Client(my_phone, my_api_id, my_api_hash, phone_number=my_phone) as client:
                        string = client.export_session_string()
                        pyperclip.copy(string)
                        print(f"\n{string}\n")
                        print("\n―― 🟢 String session created successfully!"
                              f"\n―― String copied to clipboard!")
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                elif session_method == "2":
                    try:
                        name = input("Enter your Pyrogram session file name: ")
                        with Client(name, my_api_id, my_api_hash) as client:
                            string = client.export_session_string()
                            pyperclip.copy(string)
                            print(f"\n{string}\n")
                            print("\n―― 🟢 String session generated successfully!"
                                  f"\n―― String copied to clipboard!")
                            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    except sqlite3.OperationalError:
                        print("\n―― ⚠️ Unable to generate the session string. Please ensure you are using a Pyrogram session file.")
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                else:
                    print("\n―― ⚠️ Invalid input. Please type '1' to create a new string session or '2' to generate a string session from an existing session file.")
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        except Exception as e:
            print(f"\n―― ❌ An error has occurred: {e}")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)


class Telegram:
    @staticmethod
    def login(api_id: int = None, api_hash: str = None, session_name: str = None):
        """
        Login to Telegram using Telethon session file.

        All parameters are optional. If not provided, you will be prompted to enter them.

        """
        try:
            if api_id and api_hash and session_name:
                my_api_id = api_id
                my_api_hash = api_hash
                my_session = session_name
            else:
                my_api_id = int(input("Enter your API ID: "))
                my_api_hash = input("Enter your API HASH: ")
                my_session = input("Enter your Telethon session file name: ")

            client = TelegramClient(my_session, my_api_id, my_api_hash)
            client.connect()
            if client.is_user_authorized():
                print("\n―― 🟢 User Authorized!")

                @client.on(events.NewMessage(from_users=777000))  # '777000' is the ID of Telegram Notification Service.
                async def catch_msg(event):
                    otp = re.search(r'\b(\d{5})\b', event.raw_text)
                    if otp:
                        print("\n―― OTP received ✅\n―― Your login code:", otp.group(0))
                        client.disconnect()
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                print("\n―― Please request an OTP code in your Telegram app.\n―― 📲 𝙻𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚏𝚘𝚛 𝚒𝚗𝚌𝚘𝚖𝚒𝚗𝚐 𝙾𝚃𝙿 . . .")
                with client:
                    client.run_until_disconnected()
            else:
                print("\n―― 🔴 Authorization Failed!"
                      "\n―― Invalid Telethon session file or the session has expired.")
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        except sqlite3.OperationalError:
            print("\n―― ⚠️ Unable to generate the session string. Please ensure you are using a Pyrogram session file.")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        except Exception as e:
            print(f"\n—— ❌ An error has occurred: {e}")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

    @staticmethod
    def userinfo():
        """
        Retrieves information about the current user.
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
        Scrape member's info from specified group.
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
