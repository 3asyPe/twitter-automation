import asyncio
import questionary
from loguru import logger

from modules.executor import Executor
from module_settings import MODULES_NAMES


def get_module():
    choices = []
    for id, item in enumerate(MODULES_NAMES, start=1):
        choices.append(
            questionary.Choice(f"{id}) {item.value.capitalize()}", item.value)
        )

    choices.append(questionary.Choice(f"{len(choices) + 1}) Exit", "exit"))

    result = questionary.select(
        "Select a method to get started",
        choices=choices,
        qmark="⚙️ ",
        pointer="✅ ",
    ).ask()
    return result


def main():
    logger.info("Be carefull with this tool, it can get your account banned!")

    executor = Executor()
    module = get_module()

    if module != "exit":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(executor.run_module(module))

    logger.info("Subscribe to me here - https://t.me/easypeoff")
    logger.info("You can thank me here - 0x00000D01B969922762a63F3cfD8ec9545DE4d513")


if __name__ == "__main__":
    main()
