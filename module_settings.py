import enum


class ModulesNames(str, enum.Enum):
    FOLLOW = "FOLLOW"
    UNFOLLOW = "UNFOLLOW"


class TwitterFollowModes(str, enum.Enum):
    # Folllow accounts to one user by username
    FOLLOW_ONE_USER = "FOLLOW_ONE_USER"

    # Follow accounts to users from file
    FOLLOW_USERS_FROM_FILE = "FOLLOW_USERS_FROM_FILE"

    # Follow accounts between each other
    FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER = "FOLLOW_ACCOUNTS_BETWEEN_EACH_OTHER"


class TwitterUnfollowModes(str, enum.Enum):
    # Unfollow one account by username
    UNFOLLOW_ONE_USER = "UNFOLLOW_ONE_USER"

    # Unfollow all accounts from file
    UNFOLLOW_USERS_FROM_FILE = "UNFOLLOW_USERS_FROM_FILE"


MODULES_SETTINGS = {
    ModulesNames.FOLLOW: {
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
    ModulesNames.UNFOLLOW: {
        "mode": TwitterUnfollowModes.UNFOLLOW_USERS_FROM_FILE,
        # For UNFOLLOW_ONE_USER mode
        "username": "BaddiesPee",
        # For UNSUBSCRIBE_TO_USERS_FROM_FILE mode
        "users_file": "data/users_to_unfollow.txt",
        # For UNFOLLOW_USERS_FROM_FILE mode
        "min_number_of_accounts": 2,  # Minimum number of accounts to subscribe
        "max_number_of_accounts": 4,  # Maximum number of accounts to subscribe
        # !WARNING! On big number of accounts it can red flag your accounts and lead to ban
        "all_accounts": True,  # Subscribe all accounts between each other
    },
}
