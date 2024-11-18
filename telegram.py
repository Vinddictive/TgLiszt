import sqlite3, sys, re  # noqa E401

try:
    from telethon import functions, errors as telethon_errors
    from telethon.sync import TelegramClient, events
    from telethon.sessions import StringSession
    from telethon.tl.types import Channel
except ModuleNotFoundError:
    print(
        "\n―― ⚠️ The Telethon library is not installed."
        "\n―― Please install it by running: `pip install telethon`"
    )
    sys.exit(1)
except ImportError as ie:
    print(
        f"\n―― ⚠️ {ie}"
        "\n―― Try updating Telethon by running: `pip install --upgrade telethon`"
    )
    sys.exit(1)


def _show_warning() -> None:
    print(
        "\n―― ⚠️ WARNING: Frequently creating sessions and requesting OTPs may increase the risk of "
        "your account being temporarily or permanently banned."
        "\n―― Telegram monitors unusual activity, such as multiple login attempts in a short period of time."
        "\n―― Be cautious and avoid creating too many sessions too quickly."
        "\n―― ℹ️ Telegram ToS: https://core.telegram.org/api/terms"
        "\n―― ℹ️ Telethon FAQ: "
        "https://docs.telethon.dev/en/stable/quick-references/faq.html#my-account-was-deleted-limited-when-using-the-library\n")


def _handle_user_actions(client) -> None:
    while True:
        print(
            f"\n―― [ 1 ] Get account's info"
            f"\n―― [ 2 ] See a list of user created Channels"
            f"\n―― [ 3 ] Update 2-Step Verification (2FA) password"
            f"\n―― [ 0 ] Exit"
        )

        user_input = input("\n―― Choose an option by typing its number: ")

        if user_input == "1":
            _show_user_info(client)
        elif user_input == "2":
            _show_user_channels(client)
        elif user_input == "3":
            _update_password(client)
        elif user_input == "0":
            if client.is_connected():
                client.disconnect()
            sys.exit(0)
        else:
            print("―― Invalid input! Please enter a valid option.\n")


def _show_user_info(client) -> None:
    me = client.get_me()
    print(
        f"\n\t[ACCOUNT's INFO]\n"
        f"\tID: {me.id}\n"
        f"\tFirst Name: {me.first_name if me.first_name else '-'}\n"
        f"\tLast Name: {me.last_name if me.last_name else '-'}\n"
        f"\tUsername: {'@' + me.username if me.username else '-'}\n"
        f"\tPhone Number: +{me.phone}\n"
        f"\tPremium: {me.premium}\n"
        f"\tRestricted: {me.restricted}\n"
        f"\tFake: {me.fake}\n"
        f"\tScam: {me.scam}\n"
    )


def _show_user_channels(client) -> None:
    public_group = 0
    private_group = 0
    public_channel = 0
    private_channel = 0

    dialogs = client.get_dialogs()
    created_groups = [dialog for dialog in dialogs if isinstance(dialog.entity, Channel) and dialog.entity.creator]

    for group in created_groups:
        e = group.entity
        print(
            f"ID: {e.id}\n"
            f"Title: {e.title}\n"
            f"Username: {e.username if e.username else '-'}\n"
            f"Creation Date: {e.date.strftime('%Y-%m-%d')}\n"
            f"Link: {f'https://www.t.me/{e.username}' if e.username else '-'}\n"
        )

        if e.username:
            if e.megagroup:
                public_group += 1
            else:
                public_channel += 1
        else:
            if e.megagroup:
                private_group += 1
            else:
                private_channel += 1

    print(
        f"Public Groups: {public_group}\n"
        f"Private Groups: {private_group}\n"
        f"Public Channels: {public_channel}\n"
        f"Private Channels: {private_channel}\n"
    )


def _update_password(client) -> None:
    try:
        new_pwd = input("Enter your new 2FA password: ")
        client.edit_2fa(new_password=new_pwd)
        print(f"―― 🟢 2FA password has been updated successfully!")
    except telethon_errors.PasswordHashInvalidError:
        user_confirm = input(
            "―― ℹ️ 2-Step Verification (2FA) is already enabled on this account. "
            "To update it, you'll need to provide the current password.\n"
            "Would you like to proceed with changing your 2FA password? (y/n): "
        ).strip().lower()

        if user_confirm in {"y", "yes"}:
            curr_pwd = input("Enter your current 2FA password: ")
            new_pwd = input("Enter your new 2FA password: ")
            try:
                client.edit_2fa(current_password=curr_pwd, new_password=new_pwd)
                print(f"―― 🟢 2FA password has been updated successfully!")
            except telethon_errors.PasswordHashInvalidError:
                print("―― ❌ The current password you provided is incorrect.")
            except telethon_errors.RPCError as e:
                print(f"―― ❌ An error occurred: {e}")
    except telethon_errors.RPCError as e:
        print(f"―― ❌ An error occurred: {e}")
    except Exception as e:
        print(f"―― ❌ An unexpected error occurred: {e}")


class SessionManager:
    """
    Create Telegram sessions using Telethon or Pyrogram.

    `[YouTube] How to Create Telegram Sessions <https://www.youtube.com/watch?v=-2vWERIXXZU>`_
    """

    @staticmethod
    def telethon(api_id: int = None, api_hash: str = None, phone: str = None) -> None:
        """
        Create Telethon Sessions.

        `API ID & API HASH <https://my.telegram.org/auth>`_ |
        `What are Sessions? <https://docs.telethon.dev/en/stable/concepts/sessions.html#what-are-sessions>`_

        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param phone: Phone number in international format. If you want to generate a string session,
               enter your telethon session file name instead.
        """

        _show_warning()

        user_api_id = api_id or int(input("Enter your API ID: "))
        user_api_hash = api_hash or input("Enter your API HASH: ")
        user_phone = phone or input("Enter your phone number (e.g. +1234567890): ")

        try:
            client = TelegramClient(f'{user_phone}.session', user_api_id, user_api_hash)
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(user_phone)
                try:
                    client.sign_in(user_phone, input("Enter the code sent to your phone: "))
                except telethon_errors.SessionPasswordNeededError:
                    client.sign_in(password=input("Enter 2-Step Verification (2FA) password: "))
        except sqlite3.OperationalError:
            print(
                "\n―― ❌ The provided session file could not be opened. "
                "This issue may occur if the session file was created using a different library or is corrupted. "
                "Please ensure that the session file is compatible with Telethon."
            )
            return
        except telethon_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
            return
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")
            return

        print(
            f"\n―― 🟢 TELETHON SESSION ↓"
            f"\n―― ✨ SESSION FILE saved as `{user_phone}{'.session' if not user_phone.endswith('.session') else ''}`"
            f"\n―― ✨ STRING SESSION: {StringSession.save(client.session)}"  # noqa
        )

        _handle_user_actions(client)

    @staticmethod
    def pyrogram(api_id: int = None, api_hash: str = None, phone: str = None) -> None:
        """
        Create Pyrogram Sessions.

        `API ID & API HASH <https://my.telegram.org/auth>`_ |
        `More about Pyrogram <https://docs.pyrogram.org/api/client/>`_
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param phone: Phone number in international format. If you want to generate a string session,
               enter your pyrogram session file name instead.
        """
        try:
            from pyrogram import Client, filters, errors as pyrogram_errors
        except (ImportError, ModuleNotFoundError):
            print("\n―― ⚠️ The Pyrogram library is not installed.")
            print("―― Please install it by running: `pip install pyrogram`")
            sys.exit(1)

        _show_warning()

        user_api_id = api_id or int(input("Enter your API ID: "))
        user_api_hash = api_hash or input("Enter your API HASH: ")
        user_phone = phone or input("Enter your phone number (e.g. +1234567890): ")

        try:
            client = Client(user_phone, user_api_id, user_api_hash, phone_number=user_phone)
            client.start()
        except sqlite3.OperationalError:
            print(
                "\n―― ❌ The provided session file could not be opened. "
                "This issue may occur if the session file was created using a different library or is corrupted. "
                "Please ensure that the session file is compatible with Pyrogram."
            )
            return
        except pyrogram_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
            return
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")
            return

        print(
            f"\n―― 🟢 PYROGRAM SESSION ↓"
            f"\n―― ✨ SESSION FILE saved as `{user_phone}{'.session' if not user_phone.endswith('.session') else ''}`"
            f"\n―― ✨ STRING SESSION: {client.export_session_string()}")

        client.stop()
        sys.exit(0)


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
        print(
            "\n―― ℹ️ This method only supports Telethon session files. If you're using Pyrogram, "
            "please switch to Telethon for this function to work properly."
        )

        user_api_id = api_id or int(input("Enter your API ID: "))
        user_api_hash = api_hash or input("Enter your API HASH: ")
        user_session_name = session_name or input("Enter your Telethon session file name (e.g. `my_session.session`): ")

        try:
            client = TelegramClient(user_session_name, user_api_id, user_api_hash)
            client.connect()
            if client.is_user_authorized():
                print("\n―― 🟢 User Authorized!")

                @client.on(events.NewMessage(from_users=777000))
                async def get_otp_msg(event):
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
        except telethon_errors.RPCError as e:
            print(f"\n―― ❌ An RPC error occurred: {e}")
        except Exception as e:
            print(f"\n―― ❌ An unexpected error occurred: {e}")
