import asyncio
import random

from loguru import logger


async def sleep(account, sleep_from: int, sleep_to: int, log=True):
    sleep_time = random.randint(sleep_from, sleep_to)
    if log:
        logger.info(f"{account} Sleeping for {sleep_time} seconds")
    await asyncio.sleep(sleep_time)
