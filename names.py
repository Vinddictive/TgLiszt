from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
import random

api_id = 26892726
api_hash = 'd80afce6c6f8412ce0e9d1ae5a01f8c7'

# List of names in a text file, each name on a separate line
names_file = 'names.txt'

with open(names_file, 'r') as file:
    names = file.read().splitlines()

# Randomly select a name from the list
random_name = random.choice(names)

# Split the full name into first name and last name
first_name, last_name = random_name.split(' ', 1)

with TelegramClient('my_session.session', api_id, api_hash) as client:
    print("Your session file has been created successfully!")

    # Change the account name using the randomly selected first name and last name
    result = client(UpdateProfileRequest(first_name=first_name, last_name=last_name))
    print(f"Account name has been changed to: {first_name} {last_name}")
