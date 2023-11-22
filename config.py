def load_file(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


class Config:
    ACCOUNTS = load_file("data/accounts.txt")
    PROXIES = load_file("data/proxies.txt")
    USER_AGENTS = load_file("data/user_agents.txt")

    THREADS = 3
    RETRIES = 1
    RANDOMIZE_ACCOUNTS = False

    MIN_RETRY_DELAY = 30
    MAX_RETRY_DELAY = 60

    MIN_SLEEP_BEFORE_NEXT_ACCOUNT = 1
    MAX_SLEEP_BEFORE_NEXT_ACCOUNT = 2

    MIN_SLEEP_BEFORE_NEXT_REQUEST = 3  # For automatic module only
    MAX_SLEEP_BEFORE_NEXT_REQUEST = 4  # For automatic module only


config = Config()
