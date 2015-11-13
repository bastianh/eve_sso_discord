import logging
import threading

import cherrypy

from concord import settings
from concord.discord_client import client as discord_client
from concord.webserver import OauthCallbackHandler

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class DiscordThread(threading.Thread):
    def run(self):
        discord_client.run()

    def setup(self):
        LOGGER.info("discord setup")


class WebserverThread(threading.Thread):
    def __init__(self, discord, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        self.discord_client = discord_client
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def run(self):
        cherrypy.config.update({
            'server.socket_port': settings.HTTP_PORT,
            'server.socket_host': '0.0.0.0',
            'engine.autoreload_on': False,
            'request.show_tracebacks': settings.DEBUG
        })
        cherrypy.tree.mount(OauthCallbackHandler(self.discord_client), "/callback", None)
        cherrypy.engine.start()

    def setup(self):
        LOGGER.info("discord setup %r", self)


DiscordThread(name='discord').start()
WebserverThread(name='web', discord=discord_client).start()
