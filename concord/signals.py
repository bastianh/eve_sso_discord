import logging

from blinker import signal
from discord import User
from itsdangerous import URLSafeTimedSerializer
from requests_oauthlib import OAuth2Session

from concord import settings

LOGGER = logging.getLogger(__name__)

discord_message = signal('discord_message')
discord_guild_member_add = signal('discord_guild_member_add')


# @discord_message.connect
# def on_discord_message(client, message):
#    print(client, message)
#    LOGGER.info("%r %r %r %r", client, message.author, message.channel, message)
#    if message.author.id != client.user.id:
#        client.send_message(message.channel, message.content)


@discord_guild_member_add.connect
def on_guild_member_add(client, user, **kwargs):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)

    evesso = OAuth2Session(settings.CLIENT_ID, redirect_uri=settings.CALLBACK_URL)
    auth_url, state = evesso.authorization_url(settings.AUTHORIZATION_BASE_URL, state=s.dumps(user))

    user = User(**user)

    client.send_message(user, "Hello Capsuleer!")
    client.send_message(user, "Welcome to this discord server. To be able to join any channels you have to "
                              "authenticate yourself as an EVE-Online capsuleer.")
    client.send_message(user, "Please follow this link to the EVE-Online page and authenticate yourself: %r" % auth_url)
