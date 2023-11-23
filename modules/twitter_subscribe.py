from better_automation.twitter import Client
from loguru import logger

from module_settings import MODULES_NAMES, TWITTER_SUBSCRIBE_MODES
from modules.twitter_account import TwitterAccount
from modules.twitter_module import TwitterModule


class TwitterSubscribe(TwitterModule):
    _module_name = MODULES_NAMES.SUBSCRIBE

    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        super().__init__(account=account, all_accounts=all_accounts)

        self.modes = {
            TWITTER_SUBSCRIBE_MODES.FOLLOW_ONE_USER: self._follow_one_user,
            TWITTER_SUBSCRIBE_MODES.FOLLOW_USERS_FROM_FILE: self._follow_users_from_file,
            TWITTER_SUBSCRIBE_MODES.FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER: self._follow_accounts_between_each_other,
        }

    async def run(self):
        func = self.module_settings["mode"]
        async with self.account.get_client_session() as client:
            await self._run_module(func=self.modes[func], client=client)

    async def _follow_one_user(self, client: Client):
        print("Follow one user")
        # user = await client.request_user_data(username=self.config["username"])
        # logger.info(f"<Account #{self.account.id}> Following user {user.username}")
        # await client.follow(user_id=user.id)

    async def _follow_users_from_file(self, client: Client):
        print("Follow users from file")

    async def _follow_accounts_between_each_other(self, client: Client):
        print("Follow accounts between each other")
