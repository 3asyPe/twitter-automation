import random

from better_automation.twitter import TwitterClient as Client
from loguru import logger

from config import config
from module_settings import TwitterModulesNames, TwitterLikeModes
from modules.twitter_account import TwitterAccount
from modules.twitter_module import TwitterModule
from utils.file_system import load_file
from utils.input import ainput
from utils.sleep import sleep


class TwitterLike(TwitterModule):
    _module_name = TwitterModulesNames.LIKE

    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        super().__init__(account=account, all_accounts=all_accounts)

        self.modes = {
            TwitterLikeModes.LIKE_TWEETS_FROM_FILE: self._like_tweets_from_file,
        }

    async def run(self):
        func = self.module_settings["mode"]
        client = await self.account.get_client_session()
        await self._run_module(func=self.modes[func], client=client)

    async def _like(self, client: Client, tweet_id: str):
        logger.info(f"{self.account} Liking post with id={tweet_id}")
        await client.like(tweet_id=tweet_id)
        logger.success(f"{self.account} Liked post with id={tweet_id}")

    async def _like_tweets_from_file(self, client: Client):
        if self.module_settings["all_tweets"]:
            tweets = load_file(
                file_name=self.module_settings["tweets_file"],
                file_format="txt",
            ).copy()
            number_of_tweets = len(tweets)
        else:
            number_of_tweets = random.randint(
                self.module_settings["min_number_of_likes"],
                self.module_settings["max_number_of_likes"],
            )

        random.shuffle(tweets)

        for i in range(number_of_tweets):
            tweet = tweets.pop()

            await self._like(client=client, tweet_id=tweet)

            if i != number_of_tweets - 1:
                await sleep(
                    account=self.account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_REQUEST,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_REQUEST,
                )

        logger.success(f"{self.account} Liked {number_of_tweets} tweets")
