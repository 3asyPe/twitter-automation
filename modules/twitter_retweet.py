import random

from better_automation.twitter import TwitterClient as Client
from better_automation.twitter.errors import HTTPException
from loguru import logger

from config import config
from module_settings import TwitterModulesNames, TwitterRetweetModes
from modules.twitter_account import TwitterAccount
from modules.twitter_module import TwitterModule
from utils.file_system import load_file
from utils.sleep import sleep


class TwitterRetweet(TwitterModule):
    _module_name = TwitterModulesNames.RETWEET

    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        super().__init__(account=account, all_accounts=all_accounts)

        self.modes = {
            TwitterRetweetModes.RETWEET_TWEETS_FROM_FILE: self._retweet_from_file,
        }

    async def run(self):
        func = self.module_settings["mode"]
        client = await self.account.get_client_session()
        await self._run_module(func=self.modes[func], client=client)

    async def _retweet(self, client: Client, tweet_id: str):
        logger.info(f"{self.account} Retweeting tweet with id={tweet_id}")
        try:
            await client.repost(tweet_id=tweet_id)
        except HTTPException as e:
            if 327 in e.api_codes:
                logger.error(f"{self.account} Already retweeted tweet with id={tweet_id}. Skipping...")
                return
            raise e
        logger.success(f"{self.account} Retweeted tweet with id={tweet_id}")

    async def _retweet_from_file(self, client: Client):
        if self.module_settings["all_tweets"]:
            tweets = load_file(
                file_name=self.module_settings["tweets_file"],
                file_format="txt",
            ).copy()
            number_of_tweets = len(tweets)
        else:
            number_of_tweets = random.randint(
                self.module_settings["min_number_of_retweets"],
                self.module_settings["max_number_of_retweets"],
            )

        random.shuffle(tweets)

        for i in range(number_of_tweets):
            tweet = tweets.pop()

            await self._retweet(client=client, tweet_id=tweet)

            if i != number_of_tweets - 1:
                await sleep(
                    account=self.account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_REQUEST,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_REQUEST,
                )

        logger.success(f"{self.account} Retweeted {number_of_tweets} tweets")
