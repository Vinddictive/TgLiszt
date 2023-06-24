from telethon.sync import TelegramClient
from telethon.tl.types import Channel

# API credentials
api_id = 26892726
api_hash = 'd80afce6c6f8412ce0e9d1ae5a01f8c7'

# Create a TelegramClient instance
with TelegramClient('my_session.session', api_id, api_hash) as client:
    # Get all the dialogs (including groups)
    dialogs = client.get_dialogs()

    # Initialize counters
    public_group_count = 0
    private_group_count = 0
    public_channel_count = 0
    private_channel_count = 0

    # Filter the dialogs to get only the groups you created
    created_groups = [dialog for dialog in dialogs if isinstance(dialog.entity, Channel) and dialog.entity.creator]

    # Print the information about each created group
    for group in created_groups:
        print('Group Name:', group.entity.title)
        print('Group ID:', group.entity.id)

        if group.entity.username:
            print('Username:', group.entity.username)
        else:
            print('Username: Private')

        creation_date = group.entity.date.strftime('%Y-%m-%d')
        print('Creation Date:', creation_date)
        print('---')

        if group.entity.megagroup:
            if group.entity.username:
                public_channel_count += 1
            else:
                private_channel_count += 1
        else:
            if group.entity.username:
                public_group_count += 1
            else:
                private_group_count += 1

    # Print the count of each type of group and channel
    print('Public Groups:', public_group_count)
    print('Private Groups:', private_group_count)
    print('Public Channels:', public_channel_count)
    print('Private Channels:', private_channel_count)
