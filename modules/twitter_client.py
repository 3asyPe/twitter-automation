from modules.twitter_account import TwitterAccount


class TwitterClient:
    def __init__(self, account: TwitterAccount):
        self.account = account

    async def subscribe(self):
        print("Subscribing...")
