from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import Channel
from pyrogram import Client
import pyperclip

import json
import csv
import re


class TelethonSession:
    @staticmethod
    def session_file(api_id: int, api_hash: str, phone, password=None):
        """
        Create new telethon session file.
        :param api_id: Your api id.
        :param api_hash: Your api hash.
        :param phone: Your phone number.
        :param password: Optional if the account have 2FA enabled.
        """
        client = TelegramClient(f'{phone}.session', api_id, api_hash)
        client.start(phone, password)
        print("\n🟢 Success!")

    @staticmethod
    def session_string(api_id: int, api_hash: str):
        """
        Get telethon string session.
        May not work if your account have 2FA enabled. Please disable 2FA to use this method.
        :param api_id:  Your api id.
        :param api_hash: Your api hash.
        """
        with TelegramClient(StringSession(), api_id, api_hash) as client:
            session_string = client.session.save()
            pyperclip.copy(session_string)  # Auto copy the string to Clipboard
            print(f"Your session string:\n{session_string}\n\n🟢 Success!")


class PyrogramSession:
    @staticmethod
    def session_file(api_id: int, api_hash: str, phone: str):
        """
        Create new pyrogram session file.
        :param api_id: Your api id.
        :param api_hash: Your api hash.
        :param phone: Your phone number.
        """
        with Client(phone, api_id, api_hash, phone_number=phone) as client:
            client.send_message('me', 'Hello, Pyrogram!')
            print("🟢 Success!")

    @staticmethod
    def session_string(api_id: int, api_hash: str, phone: str):
        """
        Get pyrogram string session.
        :param api_id:  Your api id.
        :param api_hash: Your api hash.
        :param phone: Your phone number.
        """
        with Client(phone, api_id=api_id, api_hash=api_hash, phone_number=phone) as client:
            session_string = client.export_session_string()
            pyperclip.copy(session_string)
            print(f"{session_string}\n\n🟢 Success!")


class Telegram:
    @staticmethod
    def login(session: str, api_id: int, api_hash: str):
        """
        Login to Telegram using either session file or string.
        :param session: Path to session file.
        :param api_id: Your api id.
        :param api_hash: Your api hash.
        """
        # The session name must include with its .session format
        client = TelegramClient(session, api_id, api_hash)
        client.connect()
        if client.is_user_authorized():
            print("🟢 User Authorized")

            @client.on(events.NewMessage(from_users=777000))
            async def handle_incoming_message(event):
                otp = re.search(r'\b(\d{5})\b', event.raw_text)
                if otp:
                    print("OTP received ✅\nYour login code:", otp.group(0))
                    client.disconnect()
            print("Please login to your telegram app. [Listening for OTP...]\n")
            with client:
                client.run_until_disconnected()
        else:
            print("🔴 Authorization Failed\n"
                  "Incorrect session file or the session no longer active. Please login and try again.")

    @staticmethod
    def get_group_channel(api_id: int, api_hash: str, session_name: str):
        """
        Retrieve details from all your own groups and channels, including both public and private.
        :param api_id: Your api id.
        :param api_hash: Your api hash.
        :param session_name: Session file name.
        """
        with TelegramClient(session_name, api_id, api_hash) as client:  # Session name must include its .session format
            pub_gr = 0
            priv_gr = 0
            pub_ch = 0
            priv_ch = 0

            dialogs = client.get_dialogs()
            created_groups = [dialog for dialog in dialogs if
                              isinstance(dialog.entity, Channel) and dialog.entity.creator]

            for group in created_groups:
                print('Group Name:', group.entity.title)
                print('Group ID:', group.entity.id)
                print('Username:', group.entity.username) if group.entity.username else print("Private")
                print('Creation Date:', group.entity.date.strftime('%Y-%m-%d'))
                print('---')

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
                f"""
            Pub Group: {pub_gr}
            Priv Group: {priv_gr}

            Pub Channel: {pub_ch}
            Priv Channel: {priv_ch}
                """
            )

    @staticmethod
    def member_scrape(api_id: int, api_hash: str, session_name: str, group: str):
        """
        Scrape member's info from specified chat (group).
        :param api_id: Your api id.
        :param api_hash: Your api hash.
        :param session_name: Name of your session file.
        :param group: Target group username (with @)
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

    @staticmethod
    def session_check(session_type, session, api_id, api_hash):
        """
        Simple code to check if a user is authorized.
        :param session_type: The type of session.
        :param session: Session information (file path or string session).
        :param api_id: The Telegram API ID.
        :param api_hash: The Telegram API hash.
        """
        if session_type == "file":
            client = TelegramClient(session, api_id, api_hash)
            client.connect()
            if client.is_user_authorized():
                print("User is authorized ✅")
            else:
                print("User is not authorized ❌")
        elif session_type == "string":
            client = TelegramClient(StringSession(session), api_id, api_hash)
            client.connect()
            if client.is_user_authorized():
                print("User is authorized ✅")
            else:
                print("User is not authorized ❌")

    @staticmethod
    def send_message(session_type, session, username, msg, api_id, api_hash):
        if session_type == "file":
            client = TelegramClient(session, api_id, api_hash)

            async def send_message():
                chat = await client.get_entity(username)
                await client.send_message(chat, msg)
                print(f'Message sent to {username} ✅')
            with client:
                client.loop.run_until_complete(send_message())

        elif session_type == "string":
            client = TelegramClient(StringSession(session), api_id, api_hash)

            async def send_message():
                chat = await client.get_entity(username)
                await client.send_message(chat, msg)
                print(f'Message sent to {username}: {msg}')
            with client:
                client.loop.run_until_complete(send_message())
