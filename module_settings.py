import enum


class MODULES_NAMES(str, enum.Enum):
    SUBSCRIBE = "SUBSCRIBE"
    UNSUBSCRIBE = "UNSUBSCRIBE"


class TWITTER_SUBSCRIBE_MODES(str, enum.Enum):
    # Folllow accounts to one user by username
    FOLLOW_ONE_USER = "FOLLOW_ONE_USER"

    # Follow accounts to users from file
    FOLLOW_USERS_FROM_FILE = "FOLLOW_USERS_FROM_FILE"

    # Follow accounts between each other
    FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER = "FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER"


MODULES_SETTINGS = {
    MODULES_NAMES.SUBSCRIBE: {
        "mode": TWITTER_SUBSCRIBE_MODES.FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER,
        # For FOLLOW_ONE_USER mode
        "username": "BaddiesPee",
        # For SUBSCRIBE_TO_USERS_FROM_FILE mode
        "users_file": "data/users_to_follow.txt",
        # For SUBSCRIBE_TO_USERS_FROM_FILE and FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER modes
        "min_number_of_accounts": 2,  # Minimum number of accounts to subscribe between each other
        "max_number_of_accounts": 4,  # Maximum number of accounts to subscribe between each other
        # !WARNING! On big number of accounts it can red flag your accounts and lead to ban
        "all_accounts": True,  # Subscribe all accounts between each other
    },
    MODULES_NAMES.UNSUBSCRIBE: {
        "mode": None,
    },
}
