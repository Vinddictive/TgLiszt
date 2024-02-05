"""

        Retrieve information about the user's created groups and channels.
        Watch the demo here: https://www.youtube.com/watch?v=1nIXnC39Hm0

"""

from telethon.sync import TelegramClient
from telethon.tl.types import Channel

api_id = API_ID
api_hash = 'API_HASH'

with TelegramClient('session_file.session', api_id, api_hash) as client:
    pub_gr = 0
    priv_gr = 0
    pub_ch = 0
    priv_ch = 0

    dialogs = client.get_dialogs()
    created_groups = [dialog for dialog in dialogs if isinstance(dialog.entity, Channel) and dialog.entity.creator]

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
