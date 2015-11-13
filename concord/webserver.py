import cherrypy
from discord import User, Member, Server, Role
from discord.utils import find
from itsdangerous import URLSafeTimedSerializer
from requests_oauthlib import OAuth2Session

from concord import settings


class OauthCallbackHandler(object):
    def __init__(self, discord_client):
        self.discord_client = discord_client
        self.serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        super().__init__()

    def index(self, code, state):
        user = User(**self.serializer.loads(state, max_age=300))

        evesso = OAuth2Session(settings.CLIENT_ID)
        token = evesso.fetch_token(settings.TOKEN_URL,
                                   authorization_response=cherrypy.request.base + cherrypy.request.path_info + "?" + cherrypy.request.query_string,
                                   state=state, method="POST", client_secret=settings.SECRET_KEY)

        r = evesso.get(settings.VERIFY_URL)
        userdata = r.json()

        if userdata['CharacterName']:
            server = self.discord_client.servers[0]
            assert isinstance(server, Server)
            member = find(lambda m: m.id == user.id, server.members)
            assert isinstance(member, Member)
            role = find(lambda r: r.name == 'Capsuleer', server.roles)
            assert isinstance(role, Role)

            self.discord_client.add_roles(member, role)
            self.discord_client.send_message(member, "Welcome %s! You should no be able to switch channels." % userdata[
                'CharacterName'])

            # self.discord_client.send_message(user, "Found you!")
            return "Welcome %s! You can now close this window." % userdata['CharacterName']

        return "Unknown Error."

    index.exposed = True
