import random

from better_automation.twitter import TwitterClient as Client
from loguru import logger

from config import config
from module_settings import TwitterModulesNames, TwitterTweetModes
from modules.twitter_account import TwitterAccount
from modules.twitter_module import TwitterModule
from utils.file_system import load_file
from utils.input import ainput
from utils.sleep import sleep


class TwitterTweet(TwitterModule):
    _module_name = TwitterModulesNames.TWEET

    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        super().__init__(account=account, all_accounts=all_accounts)

        self.modes = {
            TwitterTweetModes.TWEET_FROM_INPUT: self._tweet_from_input,
            TwitterTweetModes.TWEET_TWEETS_FROM_FILE: self._tweet_from_file,
        }

    async def run(self):
        func = self.module_settings["mode"]
        client = await self.account.get_client_session()
        await self._run_module(func=self.modes[func], client=client)

    async def _tweet(self, client: Client, text: str, media_id: str | None = None):
        logger.info(f"{self.account} Tweeting text={text}")
        await client.tweet(text=text, media_id=media_id)
        logger.success(f"{self.account} Tweeted text={text}")

    async def _upload_image(self, client: Client, image: bytes) -> str:
        logger.info(f"{self.account} Uploading image...")
        media_id = await client.upload_image(image=image)
        logger.success(f"{self.account} Uploaded image")
        return media_id

    async def _tweet_from_input(self, client: Client):
        text = await ainput(f"{self.account} Enter tweet text: ")
        await self._tweet(client=client, text=text)

    async def _tweet_from_file(self, client: Client):
        if self.module_settings["all_tweets"]:
            tweets = load_file(
                file_name=self.module_settings["tweets_file"],
                file_format="json",
                convert_to_set=True,
                convert_to_hashable=True,
            )
            number_of_tweets = len(tweets)
        else:
            number_of_tweets = random.randint(
                self.module_settings["min_number_of_tweets"],
                self.module_settings["max_number_of_tweets"],
            )

        for i in range(number_of_tweets):
            # This function is returning a cached value, but it's the same object for all threads
            # so we can remove objects from the list.
            # This way different threads can use the same list and remove objects from it
            tweets = load_file(
                file_name=self.module_settings["tweets_file"],
                file_format="json",
                convert_to_set=True,
                convert_to_hashable=True,
            )

            if len(tweets) == 0:
                break

            tweet = tweets.pop()
            if isinstance(tweet, tuple):
                tweet = dict(tweet)

            logger.info(f"{self.account} Tweeting #{i+1} tweet")

            if isinstance(tweet, dict):
                media_id = await self._upload_image(client=client, image=load_file(
                    tweet["image"], file_format="bytes"
                ))
                await self._tweet(client=client, text=tweet["text"], media_id=media_id)
            else:
                await self._tweet(client=client, text=tweet)


            if self.module_settings["post_only_unique_tweets_on_all_accounts"]:
                logger.info(
                    f"{self.account} Deleted tweet from text={tweet} to not post it again (not saved to file yet)"
                )

            if i != number_of_tweets - 1:
                await sleep(
                    account=self.account,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_REQUEST,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_REQUEST,
                )

        logger.success(f"{self.account} Tweeted {number_of_tweets} tweets")