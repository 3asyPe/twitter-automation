import asyncio
import sys
from loguru import logger


async def ainput(string: str) -> str:
    logger.info(string)
    return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
