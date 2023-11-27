import random

from better_automation.twitter import Client
from better_automation.twitter.errors import Forbidden
from loguru import logger

from config import config
from module_settings import TwitterModulesNames, TwitterUnfollowModes
from modules.twitter_account import TwitterAccount
from modules.twitter_module import TwitterModule
from utils.errors import AccountNotFound, FollowItSelfError
from utils.file_system import load_file
from utils.sleep import sleep


class TwitterUnfollow(TwitterModule):
    _module_name = TwitterModulesNames.UNFOLLOW

    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        super().__init__(account=account, all_accounts=all_accounts)

        self.modes = {
            TwitterUnfollowModes.UNFOLLOW_ONE_USER: self._unfollow_one_user,
            TwitterUnfollowModes.UNFOLLOW_USERS_FROM_FILE: self._unfollow_users_from_file,
        }

    async def run(self):
        func = self.module_settings["mode"]
        async with self.account.get_client_session() as client:
            await self._run_module(func=self.modes[func], client=client)

    async def _unfollow_one_user(
        self, client: Client, username: str | None = None, log_error=True
    ):
        username = username or self.module_settings["username"]

        logger.info(f"{self.account} Unfollowing user {username}")

        try:
            user = await client.request_user_data(username=username)
        except KeyError as e:
            if log_error:
                logger.error(f"{self.account} User username={username} not found")
            raise AccountNotFound(f"User username={username} not found") from e

        await client.unfollow(user_id=user.id)
        logger.success(f"{self.account} Unfollowed user {username}")

    async def _unfollow_users_from_file(self, client: Client):
        usernames = load_file(file_name=self.module_settings["users_file"])

        if self.module_settings["all_accounts"]:
            min_number_of_accounts = len(usernames)
            max_number_of_accounts = len(usernames)
        else:
            min_number_of_accounts = min(
                self.module_settings["min_number_of_accounts"], len(usernames)
            )
            max_number_of_accounts = min(
                self.module_settings["max_number_of_accounts"], len(usernames)
            )

        num_of_accounts = random.randint(min_number_of_accounts, max_number_of_accounts)

        usernames = random.sample(usernames, num_of_accounts)

        for i, username in enumerate(usernames):
            try:
                await self._unfollow_one_user(
                    client=client, username=username, log_error=False
                )
            except AccountNotFound:
                logger.error(f"{self.account} User username={username} not found")

            if i != num_of_accounts - 1:
                await sleep(
                    account=self.account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_REQUEST,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_REQUEST,
                )
