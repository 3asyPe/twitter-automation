from contextlib import contextmanager
import re
import aiohttp

from aiohttp import TCPConnector
from aiohttp_proxy import ProxyConnector
from better_automation.twitter import Client
from better_automation.twitter import Account
from better_proxy import Proxy


class TwitterAccount:
    def __init__(
        self, id: int, auth_token: str, user_agent: str, proxy: str | None = None
    ):
        self.id = id
        self.auth_token = self.validate_token(auth_token)
        self.user_agent = user_agent
        self.proxy = proxy
        self._account = Account(auth_token=self.auth_token)

    def validate_token(self, auth_token: str) -> str | None:
        word_pattern = r"^[a-z0-9]{40}$"
        words = re.split(r"[\s,:;.()\[\]{}<>]", auth_token)

        for word in words:
            if re.match(word_pattern, word):
                return word

        raise ValueError("Invalid auth token")

    @contextmanager
    async def get_client_session(self) -> Client:
        async with aiohttp.ClientSession(
            connector=self._get_session_connector()
        ) as session:
            yield Client(account=self._account, session=session)

    def _get_session_connector(self) -> TCPConnector | ProxyConnector:
        if self.proxy:
            if self.proxy.startswith("https://"):
                self.proxy = self.proxy.replace("https://", "http://")

            return ProxyConnector.from_url(
                url=Proxy.from_str(proxy=self.proxy).as_url, verify_ssl=False
            )

        return TCPConnector(verify_ssl=False)
