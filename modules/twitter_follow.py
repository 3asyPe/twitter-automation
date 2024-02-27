import random

from better_automation.twitter import TwitterClient as Client
from better_automation.twitter.errors import Forbidden
from loguru import logger

from config import config
from module_settings import TwitterModulesNames, TwitterFollowModes
from modules.twitter_account import TwitterAccount
from modules.twitter_module import TwitterModule
from utils.errors import AccountNotFound, FollowItSelfError
from utils.file_system import load_file
from utils.sleep import sleep


class TwitterFollow(TwitterModule):
    _module_name = TwitterModulesNames.FOLLOW

    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        super().__init__(account=account, all_accounts=all_accounts)

        self.modes = {
            TwitterFollowModes.FOLLOW_ONE_USER: self._follow_one_user,
            TwitterFollowModes.FOLLOW_USERS_FROM_FILE: self._follow_users_from_file,
            TwitterFollowModes.FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER: self._follow_accounts_between_each_other,
        }

    async def run(self):
        func = self.module_settings["mode"]
        client = await self.account.get_client_session()
        await self._run_module(func=self.modes[func], client=client)

    async def _follow_one_user(
        self, client: Client, username: str | None = None, log_error=True
    ):
        username = username or self.module_settings["username"]

        logger.info(f"{self.account} Following user {username}")

        if self.account.data.username == username:
            if log_error:
                logger.error(f"{self.account} Cannot follow itself")
            raise FollowItSelfError(f"User cannot follow itself")

        try:
            user = await client.request_user_data(username=username)
        except KeyError as e:
            if log_error:
                logger.error(f"{self.account} User username={username} not found")
            raise AccountNotFound(f"User username={username} not found") from e

        try:
            await client.follow(user_id=user.id)
        except Forbidden as e:
            if e.api_codes == [158]:
                if log_error:
                    logger.error(f"{self.account} Cannot follow itself")
                raise FollowItSelfError(f"User cannot follow itself") from e
            raise e

        logger.success(f"{self.account} Followed user {username}")

    async def _follow_users_from_file(self, client: Client):
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
                await self._follow_one_user(
                    client=client, username=username, log_error=False
                )
            except AccountNotFound:
                logger.error(f"{self.account} User username={username} not found")
            except FollowItSelfError:
                logger.info(f"{self.account} Skipping myself")

            if i != num_of_accounts - 1:
                await sleep(
                    account=self.account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_REQUEST,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_REQUEST,
                )

    async def _follow_accounts_between_each_other(self, client: Client):
        if self.module_settings["all_accounts"]:
            min_number_of_accounts = len(self.all_accounts)
            max_number_of_accounts = len(self.all_accounts)
        else:
            min_number_of_accounts = min(
                self.module_settings["min_number_of_accounts"], len(self.all_accounts)
            )
            max_number_of_accounts = min(
                self.module_settings["max_number_of_accounts"], len(self.all_accounts)
            )

        num_of_accounts = random.randint(min_number_of_accounts, max_number_of_accounts)

        accounts = random.sample(self.all_accounts, num_of_accounts)

        for i, account in enumerate(accounts):
            temp_client = await self.account.get_client_session()
            username = account.data.username

            await sleep(account=self.account, sleep_from=1, sleep_to=5, log=False)

            try:
                await self._follow_one_user(
                    client=client, username=username, log_error=False
                )
            except AccountNotFound:
                logger.error(
                    f"{self.account} User username={account.data.username} not found"
                )
            except FollowItSelfError:
                logger.info(f"{self.account} Skipping myself")

            if i != num_of_accounts - 1:
                await sleep(
                    account=self.account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_REQUEST,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_REQUEST,
                )
