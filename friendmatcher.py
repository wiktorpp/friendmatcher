import discord
from TOKEN import TOKEN

import message_handler
import traceback
from importlib import reload

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

users_enabled = set()
user_id_to_priviledged_user = dict()
already_matched = {}

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))
    message_handler.client = client

@client.event
async def on_message(message):
    global message_handler
    if message.content == ".reload":
        users_enabled = message_handler.users_enabled
        user_id_to_priviledged_user = message_handler.user_id_to_priviledged_user
        already_matched = message_handler.already_matched
        message_handler = reload(message_handler)
        message_handler.client = client
        message_handler.users_enabled = users_enabled
        message_handler.user_id_to_priviledged_user = user_id_to_priviledged_user
        message_handler.already_matched = already_matched
    else:
        try:
            await message_handler.on_message(message)
        except:
            error = traceback.format_exc()
            await message.channel.send(error)

if __name__ == "__main__":
    client.run(TOKEN)

#https://discord.com/oauth2/authorize?client_id=738728621459505184&permissions=8&scope=bot