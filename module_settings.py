import enum


class TwitterModulesNames(str, enum.Enum):
    FOLLOW = "FOLLOW"
    UNFOLLOW = "UNFOLLOW"
    TWEET = "TWEET"


class TwitterFollowModes(str, enum.Enum):
    # Follow accounts to one user by username
    FOLLOW_ONE_USER = "FOLLOW_ONE_USER"

    # Follow users from file
    FOLLOW_USERS_FROM_FILE = "FOLLOW_USERS_FROM_FILE"

    # Follow accounts between each other
    FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER = "FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER"


class TwitterUnfollowModes(str, enum.Enum):
    # Unfollow one account by username
    UNFOLLOW_ONE_USER = "UNFOLLOW_ONE_USER"

    # Unfollow accounts from file
    UNFOLLOW_USERS_FROM_FILE = "UNFOLLOW_USERS_FROM_FILE"


class TwitterTweetModes(str, enum.Enum):
    # Tweet tweets by inputting them in console for every account
    TWEET_FROM_INPUT = "TWEET_FROM_INPUT"

    # Tweet tweets from json file
    TWEET_TWEETS_FROM_FILE = "TWEET_TWEETS_FROM_FILE"


MODULES_SETTINGS = {
    TwitterModulesNames.FOLLOW: {
        # Follow accounts to one user by username
        # TwitterFollowModes.FOLLOW_ONE_USER
        #
        # Follow accounts to users from file
        # TwitterFollowModes.FOLLOW_USERS_FROM_FILE
        #
        # Follow accounts between each other
        # TwitterFollowModes.FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER
        "mode": TwitterFollowModes.FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER,
        # For FOLLOW_ONE_USER mode
        "username": "BaddiesPee",
        # For FOLLOW_USERS_FROM_FILE mode
        "users_file": "data/users_to_follow.txt",
        # For FOLLOW_USERS_FROM_FILE and FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER modes
        "min_number_of_accounts": 2,  # Minimum number of accounts to subscribe
        "max_number_of_accounts": 4,  # Maximum number of accounts to subscribe
        # !WARNING! On big number of accounts it can red flag your accounts and lead to ban
        "all_accounts": True,  # Subscribe all accounts between each other
    },
    TwitterModulesNames.UNFOLLOW: {
        # Unfollow one account by username
        # TwitterUnfollowModes.UNFOLLOW_ONE_USER
        #
        # Unfollow accounts from file
        # TwitterUnfollowModes.UNFOLLOW_USERS_FROM_FILE
        "mode": TwitterUnfollowModes.UNFOLLOW_USERS_FROM_FILE,
        # For UNFOLLOW_ONE_USER mode
        "username": "BaddiesPee",
        # For UNFOLLOW_USERS_FROM_FILE mode
        "users_file": "data/users_to_unfollow.txt",
        "min_number_of_accounts": 2,  # Minimum number of accounts to subscribe
        "max_number_of_accounts": 4,  # Maximum number of accounts to subscribe
        # !WARNING! On big number of accounts it can red flag your accounts and lead to ban
        "all_accounts": True,  # Subscribe all accounts between each other
    },
    TwitterModulesNames.TWEET: {
        # Tweet tweets by inputting them in console for every account
        # TwitterTweetModes.TWEET_FROM_INPUT
        #
        # Tweet tweets from json file
        # TwitterTweetModes.TWEET_TWEETS_FROM_FILE
        "mode": TwitterTweetModes.TWEET_FROM_INPUT,
        "min_number_of_tweets": 0,  # Minimum number of tweets to post
        "max_number_of_tweets": 5,  # Maximum number of tweets to post
        "all_tweets": True,  # Post all tweets from file
        "tweets_file": "data/tweets.json",  # File with tweets
        # Avoid duplicates on different accounts
        "post_only_unique_tweets_on_all_accounts": True,
        # Delete written tweets from file to avoid duplicates on next run
        "delete_written_tweets_from_file": True,
    },
}
