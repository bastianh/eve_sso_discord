import logging

import discord

from concord import settings
from concord.signals import discord_message, discord_guild_member_add

LOGGER = logging.getLogger(__name__)
client = discord.Client()
client.login(settings.DISCORD_EMAIL, settings.DISCORD_PASSWORD)

if not client.is_logged_in:
    print('Logging in to Discord failed')
    exit(1)


@client.event
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)


@client.event
def on_socket_update(event, data):
    if event == "GUILD_MEMBER_ADD":
        discord_guild_member_add.send(client, **data)


@client.event
def on_message(message):
    discord_message.send(client, message=message)
