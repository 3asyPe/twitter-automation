import random

from abc import ABC, abstractmethod
from better_automation.twitter.account import AccountStatus
from better_automation.twitter.errors import *
from typing import Callable, Awaitable
from loguru import logger

from config import config
from module_settings import TwitterModulesNames, MODULES_SETTINGS
from modules.twitter_account import TwitterAccount
from utils.errors import InvalidToken, AccountLocked, AccountSuspended
from utils.sleep import sleep


class TwitterModule(ABC):
    def __init__(self, account: TwitterAccount, all_accounts: list[TwitterAccount]):
        self.account = account
        self.all_accounts = all_accounts
        self.module_settings = MODULES_SETTINGS[self._module_name]

    async def _run_module(self, func: Callable[..., Awaitable], *args, **kwargs):
        retry = 0
        max_retries = random.randint(config.MIN_RETRIES, config.MAX_RETRIES)
        while retry < max_retries + 1:
            try:
                try:
                    await func(*args, **kwargs)
                    break
                except Unauthorized as e:
                    logger.error(f"{self} Unauthorized")
                    raise InvalidToken(f"{self} Invalid Token")
                except HTTPException as e:
                    if self.account.status == AccountStatus.LOCKED:
                        logger.error(f"{self} is locked")
                        raise AccountLocked(f"{self} is locked")
                    elif self.account.status == AccountStatus.SUSPENDED:
                        logger.error(f"{self} is suspended")
                        raise AccountSuspended(f"{self} is suspended")
                    raise e
            except TwitterAPIException as e:
                logger.error(
                    f"{self} Error while running module {self._module_name}: {e}"
                )
                retry += 1
                if retry == max_retries + 1:
                    raise e

            logger.info(
                f"{self} Retrying module {self._module_name} ({retry}/{max_retries})"
            )
            await sleep(
                account=self.account,
                sleep_from=config.MIN_RETRY_DELAY,
                sleep_to=config.MIN_RETRY_DELAY,
            )

    @property
    @staticmethod
    @abstractmethod
    def _module_name() -> TwitterModulesNames:
        pass
