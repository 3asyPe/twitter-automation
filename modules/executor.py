import asyncio
import atexit
import random
import traceback

from loguru import logger

from config import config
from modules.twitter_account import TwitterAccount
from module_settings import TwitterModulesNames, MODULES_SETTINGS, TwitterTweetModes
from modules.twitter_follow import TwitterFollow
from modules.twitter_unfollow import TwitterUnfollow
from modules.twitter_tweet import TwitterTweet
from modules.twitter_retweet import TwitterRetweet
from modules.twitter_like import TwitterLike
from utils.errors import InvalidToken, AccountLocked, AccountSuspended
from utils.sleep import sleep
from utils.file_system import save_to_file, load_file


class Executor:
    def __init__(self):
        self.groups, self.accounts = self._generate_accounts()

        self.twitter_modules = {
            TwitterModulesNames.FOLLOW: TwitterFollow,
            TwitterModulesNames.UNFOLLOW: TwitterUnfollow,
            TwitterModulesNames.TWEET: TwitterTweet,
            TwitterModulesNames.RETWEET: TwitterRetweet,
            TwitterModulesNames.LIKE: TwitterLike,
        }

        self.database_modules = {}

    async def run_module(self, module):
        self._register_exit_handlers(module)

        tasks = []
        for thread_id in range(config.THREADS):
            tasks.append(self._run_module_for_group(module=module, thread_id=thread_id))

        await asyncio.gather(*tasks)

    async def _run_module_for_group(self, module, thread_id):
        for i, account in enumerate(self.groups[thread_id]):
            logger.info(f"{account} Running module {module}")

            if thread_id != 0 or i != 0:
                await sleep(
                    account=account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_ACCOUNT,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_ACCOUNT,
                )
            try:
                await self.twitter_modules[module](
                    account=account, all_accounts=self.accounts
                ).run()
            except InvalidToken:
                save_to_file(
                    file_name=config.PATH_TO_WRITE_INVALID_TOKENS,
                    data=account.auth_token,
                )
            except AccountLocked:
                save_to_file(
                    file_name=config.PATH_TO_WRITE_LOCKED_ACCOUNTS,
                    data=account.auth_token,
                )
            except AccountSuspended:
                save_to_file(
                    file_name=config.PATH_TO_WRITE_SUSPENDED_ACCOUNTS,
                    data=account.auth_token,
                )
            except Exception as e:
                traceback.print_exc()
                logger.error(f"{account} Error while running module {module}: {e}")
            else:
                logger.success(f"{account} Module {module} finished")

    def _generate_accounts(self) -> tuple[list, list]:
        data = list(zip(config.ACCOUNTS, config.PROXIES, config.USER_AGENTS))
        if config.RANDOMIZE_ACCOUNTS:
            random.shuffle(data)

        accounts = []

        for id, (auth_token, proxy, user_agent) in enumerate(data, start=1):
            try:
                account = TwitterAccount(
                    id=id, auth_token=auth_token, user_agent=user_agent, proxy=proxy
                )
            except Exception as e:
                logger.error(f"Error while creating Account #{id}: {e}")
                continue

            accounts.append(account)

        if config.THREADS <= 0:
            config.THREADS = 1
        elif config.THREADS > len(accounts):
            config.THREADS = len(accounts)

        total_accounts = len(accounts)
        group_size = total_accounts // config.THREADS
        remainder = total_accounts % config.THREADS

        groups = []
        start = 0
        for i in range(config.THREADS):
            # Add an extra account to some groups to distribute the remainder
            end = start + group_size + (1 if i < remainder else 0)
            groups.append(accounts[start:end])
            start = end

        return groups, accounts

    def _register_exit_handlers(self, module):
        if (
            module == TwitterModulesNames.TWEET
            and MODULES_SETTINGS[TwitterModulesNames.TWEET]["mode"]
            == TwitterTweetModes.TWEET_TWEETS_FROM_FILE
            and MODULES_SETTINGS[TwitterModulesNames.TWEET][
                "delete_written_tweets_from_file"
            ]
        ):
            atexit.register(
                save_to_file,
                file_name=MODULES_SETTINGS[TwitterModulesNames.TWEET]["tweets_file"],
                data=load_file(
                    file_name=MODULES_SETTINGS[TwitterModulesNames.TWEET][
                        "tweets_file"
                    ],
                    file_format="json",
                    convert_to_set=True,
                ),  # Cached value
                file_format="json",
                open_format="w",
            )
