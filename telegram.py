import sqlite3, sys, re  # noqa E401

try:
    from telethon.sync import TelegramClient, events
    from telethon.sessions import StringSession
    from telethon import functions, errors as t_errors
    from telethon.tl.types import Channel
except (ImportError, ModuleNotFoundError):
    print("\n―― ⚠️ The Telethon library is not installed.")
    print("―― Please install it by running: `pip install telethon`")
    sys.exit()

try:
    from pyrogram import Client, filters, errors as p_errors
except (ImportError, ModuleNotFoundError):
    print("\n―― ⚠️ The Pyrogram library is not installed.")
    print("―― Please install it by running: `pip install pyrogram`")
    sys.exit()


def _info_msg(string=None, warn=False):
    if warn:
        print(
            "\n―― ⚠️ WARNING: Frequently creating sessions and requesting OTPs may increase the risk of "
            "your account being temporarily or permanently banned."
            "\n―― Telegram monitors unusual activity, such as multiple login attempts in a short period of time."
            "\n―― Be cautious and avoid creating too many sessions too quickly."
            "\n―― ℹ️ Telegram ToS: https://core.telegram.org/api/terms"
            "\n―― ℹ️ Telethon FAQ: https://docs.telethon.dev/en/stable/quick-references/faq.html#my-account-was-deleted-limited-when-using-the-library\n\n")
    else:
        print(f"\n{string}")
        print("\n―― 🟢 String session created successfully!")
        try:
            import pyperclip
            pyperclip.copy(string)  # Auto copy the string to Clipboard
            print("―― 🟢 String copied to clipboard!")
        except ModuleNotFoundError:
            pass


class SessionManager:
    """
    Create a Telegram session using Telethon or Pyrogram.

    `[YouTube] How to Create Telegram Sessions <https://www.youtube.com/watch?v=-2vWERIXXZU>`_
    """

    @staticmethod
    def telethon(api_id: int = None, api_hash: str = None, phone: str = None, password=None,
                 session_file=False, session_string=False) -> None:
        """
        Create Telethon Sessions.

        `API ID & API HASH <https://my.telegram.org/auth>`_ |
        `What are Sessions? <https://docs.telethon.dev/en/stable/concepts/sessions.html#what-are-sessions>`_
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param phone: Phone number in international format (e.g. +1234567890).
        :param password: 2-Step Verification password.
        :param session_file: If True, create a Telethon session file.
        :param session_string: If True, generate a Telethon string session.
        """

        if session_file and session_string or not session_file and not session_string:
            print("\n―― ⚠️ Please specify a valid session type."
                  "\n―― To create a Telethon session file, set 'session_file' to True."
                  "\n―― To generate a Telethon string session, set 'session_string' to True.")
            return

        _info_msg(warn=True)

        api_id_ = api_id or int(input("Enter your API ID: "))
        api_hash_ = api_hash or input("Enter your API HASH: ")

        try:
            if session_file:
                phone_ = phone or input("Enter your phone number (e.g. +1234567890): ")
                pwd_ = password or input("Enter 2-Step Verification (press 'Enter' if you don't have it): ")
                client = TelegramClient(f'{phone_}.session', api_id_, api_hash_)
                client.start(phone_, pwd_)
                print("\n―― 🟢 Session file created successfully!")

            if session_string:
                print("\n―― [ 1 ] Log in to create a new session string"
                      "\n―― [ 2 ] Generate a session string from an existing session file"
                      "\n―― [ 0 ] Exit")
                user_input = input("\n―― Choose how you want to create the session string: ")

                if user_input == "1":
                    phone_ = phone or input("Enter your phone number (e.g. +1234567890): ")
                    pwd_ = password or input("Enter 2-Step Verification (press 'Enter' if you don't have it): ")
                    with TelegramClient(StringSession(), api_id_, api_hash_).start(phone=phone_, password=pwd_) as client:
                        string = client.session.save()
                        _info_msg(string=string)

                elif user_input == "2":
                    name = input("Enter your Telethon session file name (e.g. `my_session.session`): ")
                    try:
                        client = TelegramClient(name, api_id_, api_hash_)
                        string = StringSession.save(client.session)
                        _info_msg(string=string)
                    except sqlite3.OperationalError:
                        print("\n―― ⚠️ Unable to generate the session string. "
                              "Please ensure you are using a Telethon session file.")
                elif user_input == "0":
                    return
                else:
                    print("\n―― ⚠️ Invalid input. Please type `1` to create a new string session or `2` "
                          "to generate a string session from an existing session file.")

        except t_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")

    @staticmethod
    def pyrogram(api_id: int = None, api_hash: str = None, phone: str = None,
                 session_file=False, session_string=False) -> None:
        """
        Create Pyrogram Sessions.

        `API ID & API HASH <https://my.telegram.org/auth>`_ |
        `More about Pyrogram <https://docs.pyrogram.org/api/client/>`_
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param phone: Phone number in international format (e.g. +1234567890).
        :param session_file: If True, create a Pyrogram session file.
        :param session_string: If True, generate a Pyrogram string session.
        """

        if session_file and session_string or not session_file and not session_string:
            print("\n―― ⚠️ Please specify a valid session type."
                  "\n―― To create a Pyrogram session file, set 'session_file' to True."
                  "\n―― To generate a Pyrogram string session, set 'session_string' to True.")
            return

        _info_msg(warn=True)

        try:
            api_id_ = api_id or int(input("Enter your API ID: "))
            api_hash_ = api_hash or input("Enter your API HASH: ")

            if session_file:
                phone_ = phone or input("Enter your phone number (e.g. +1234567890): ")
                with Client(phone_, api_id_, api_hash_, phone_number=phone_) as client:
                    client.send_message('me', 'Hi!')
                    print("\n―― 🟢 Session file created successfully!")
            if session_string:
                print("\n―― [ 1 ] Log in to create a new session string"
                      "\n―― [ 2 ] Generate a session string from an existing session file"
                      "\n―― [ 0 ] Exit")
                user_input = input("\n―― Choose how you want to create the session string: ")

                if user_input == "1":
                    phone_ = phone or input("Enter your phone number (e.g. +1234567890): ")
                    with Client(phone_, api_id_, api_hash_, phone_number=phone_) as client:
                        string = client.export_session_string()
                        _info_msg(string=string)
                elif user_input == "2":
                    try:
                        name = input("Enter your Pyrogram session file name (e.g. `my_session.session`): ")
                        with Client(name, api_id_, api_hash_) as client:
                            string = client.export_session_string()
                            _info_msg(string=string)
                    except sqlite3.OperationalError:
                        print("\n―― ⚠️ Unable to generate the session string. "
                              "Please ensure you are using a Pyrogram session file.")
                elif user_input == "0":
                    return
                else:
                    print("\n―― ⚠️ Invalid input. Please type `1` to create a new string session or `2` "
                          "to generate a string session from an existing session file.")

        except p_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")


class Telegram:
    """
    Interact with Telegram.

    `[YouTube] Login to Telegram Using a Session File or String Session <https://www.youtube.com/watch?v=T2qQfX7kjgI>`_
    """

    @staticmethod
    def login(api_id: int = None, api_hash: str = None, session_name: str = None) -> None:
        """
        Login to Telegram using Telethon session file.
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param session_name: Your Telethon session file name
        """
        print("\n―― ℹ️ This method only supports Telethon session files. If you're using Pyrogram, "
              "please switch to Telethon for this function to work properly.")

        api_id_ = api_id or int(input("Enter your API ID: "))
        api_hash_ = api_hash or input("Enter your API HASH: ")
        name_ = session_name or input("Enter your Telethon session file name (e.g. `my_session.session`): ")

        try:
            client = TelegramClient(name_, api_id_, api_hash_)
            client.connect()
            if client.is_user_authorized():
                print("\n―― 🟢 User Authorized!")

                @client.on(events.NewMessage(from_users=777000))  # '777000' is the ID of Telegram Notification Service.
                async def catch_msg(event):
                    otp = re.search(r'\b(\d{5})\b', event.raw_text)
                    if otp:
                        print("\n―― OTP received ✅\n―― Your login code:", otp.group(0))
                        client.disconnect()

                print("\n―― Please request an OTP code in your Telegram app."
                      "\n―― 📲 𝙻𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚏𝚘𝚛 𝚒𝚗𝚌𝚘𝚖𝚒𝚗𝚐 𝙾𝚃𝙿 . . .")
                with client:
                    client.run_until_disconnected()
            else:
                print("\n―― 🔴 Authorization Failed!"
                      "\n―― Invalid Telethon session file or the session has expired.")
        except sqlite3.OperationalError:
            print("\n―― ⚠️ Invalid Telethon session file. Please ensure you are using a Telethon session file.")
        except t_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")

    @staticmethod
    def userinfo(api_id: int = None, api_hash: str = None, session_name: str = None) -> None:
        """
        Retrieves information about the current user.
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param session_name: Your Telethon session file name
        """
        print("\n―― ℹ️ This method only supports Telethon session files. If you're using Pyrogram, "
              "please switch to Telethon for this function to work properly.")

        api_id_ = api_id or int(input("Enter your API ID: "))
        api_hash_ = api_hash or input("Enter your API HASH: ")
        name_ = session_name or input("Enter your Telethon session file name: ")

        try:
            with TelegramClient(name_, api_id_, api_hash_) as client:
                me = client.get_me()
                name = me.first_name if me.first_name else "-"
                username = f'@{me.username}' if me.username else "-"
                uid = me.id
                phone = me.phone

                print(
                    f"\n  [ACCOUNT's INFO]\n"
                    f"  Name: {name}\n"
                    f"  Username: {username}\n"
                    f"  ID: {uid}\n"
                    f"  Phone Number: +{phone}\n"
                    f"\n[ 1 ] View Authorized Devices"
                    f"\n[ 2 ] See a list of user created groups and channels"
                    f"\n[ 3 ] Set a new 2-Step Verification (2FA) password"
                    f"\n[ 0 ] Exit\n"
                )
                user_input = input("Choose an option by typing its number: ")

                if user_input == "1":
                    result = client(functions.account.GetAuthorizationsRequest())
                    print(result.stringify())

                elif user_input == "2":
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
                        print('Username:', group.entity.username) if group.entity.username else print(
                            "Username: [Private]")
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
                elif user_input == "3":
                    new_pwd = input("Enter your new 2FA password: ")
                    try:
                        client.edit_2fa(new_password=new_pwd)
                        print(f"—— 🟢 2FA password '{new_pwd}' has been set successfully!")
                    except t_errors.PasswordHashInvalidError:
                        print("―― ℹ️ It seems 2FA is already enabled 🤷‍♀️")
                else:
                    return

        except sqlite3.OperationalError:
            print("\n―― ⚠️ Unable to connect. Please ensure you are using a Telethon session file.")
        except t_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")
