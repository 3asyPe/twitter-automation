import asyncio
import random
import traceback

from loguru import logger

from config import config
from modules.twitter_account import TwitterAccount
from module_settings import MODULES_NAMES
from utils.sleep import sleep


class Executor:
    def __init__(self):
        self.modules = {
            MODULES_NAMES.SUBSCRIBE: self.subscribe,
            MODULES_NAMES.UNSUBSCRIBE: self.unsubscribe,
        }

        self.groups = self._generate_groups()

    def get_accounts(self, thread_id: int):
        group_len = len(self.groups[0])
        for id, (account, proxy, user_agent) in enumerate(
            self.groups[thread_id], start=thread_id * group_len + 1
        ):
            try:
                yield TwitterAccount(
                    id=id, auth_token=account, user_agent=user_agent, proxy=proxy
                )
            except Exception as e:
                logger.error(f"Error while creating account #{id}: {e}")

    async def run_module(self, module):
        tasks = []
        for thread_id in range(config.THREADS):
            tasks.append(self._run_module_for_group(module, thread_id))

        await asyncio.gather(*tasks)

    async def _run_module_for_group(self, module, thread_id):
        for i, account in enumerate(self.get_accounts(thread_id=thread_id)):
            logger.info(f"Running module {module} for account #{account.id}")

            if thread_id != 0 or i != 0:
                await sleep(
                    account_id=account.id,
                    sleep_from=config.MIN_SLEEP_BEFORE_NEXT_ACCOUNT,
                    sleep_to=config.MAX_SLEEP_BEFORE_NEXT_ACCOUNT,
                )
            try:
                await self.modules[module](account)
            except Exception as e:
                traceback.print_exc()
                logger.error(
                    f"Error while running module {module} for account #{account.id}: {e}"
                )

    async def subscribe(self, account: TwitterAccount):
        print("Subscribing...")

    async def unsubscribe(self, account: TwitterAccount):
        print("Unsubscribing...")

    def _generate_groups(self):
        data = list(zip(config.ACCOUNTS, config.PROXIES, config.USER_AGENTS))
        if config.RANDOMIZE_ACCOUNTS:
            random.shuffle(data)

        groups = []

        for thread_id in range(config.THREADS):
            pointer = len(data) // config.THREADS * thread_id
            next_pointer = (
                pointer + len(data) // config.THREADS
                if thread_id != config.THREADS - 1
                else len(data)
            )

            groups.append(data[pointer:next_pointer])

        return groups
