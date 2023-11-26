from contextlib import asynccontextmanager
import re
import aiohttp

from aiohttp import TCPConnector
from aiohttp_proxy import ProxyConnector
from better_automation.twitter import Client
from better_automation.twitter import Account
from better_proxy import Proxy


class TwitterAccount(Account):
    def __init__(
        self, id: int, auth_token: str, user_agent: str, proxy: str | None = None
    ):
        self.id = id
        self.user_agent = user_agent
        self.proxy = proxy

        super().__init__(auth_token=self._validate_token(auth_token))

    @asynccontextmanager
    async def get_client_session(self) -> Client:
        async with aiohttp.ClientSession(
            connector=self._get_session_connector()
        ) as session:
            client = Client(account=self, session=session)
            await client.request_user_data()
            yield client

    def _validate_token(self, auth_token: str) -> str | None:
        word_pattern = r"^[a-z0-9]{40}$"
        words = re.split(r"[\s,:;.()\[\]{}<>]", auth_token)

        for word in words:
            if re.match(word_pattern, word):
                return word

        raise ValueError("Invalid auth token")

    def _get_session_connector(self) -> TCPConnector | ProxyConnector:
        if self.proxy:
            if self.proxy.startswith("https://"):
                self.proxy = self.proxy.replace("https://", "http://")

            return ProxyConnector.from_url(
                url=Proxy.from_str(proxy=self.proxy).as_url, verify_ssl=False
            )

        return TCPConnector(verify_ssl=False)

    def __str__(self):
        return f"<TwitterAccount #{self.id} auth_token={self.short_auth_token}>"

    def __repr__(self):
        return f"<TwitterAccount #{self.id} auth_token={self.short_auth_token}>"
