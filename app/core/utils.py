from functools import partial
import asyncio
import re


_snake_1 = partial(re.compile(r'(.)((?<![^A-Za-z])[A-Z][a-z]+)').sub, r'\1_\2')
_snake_2 = partial(re.compile(r'([a-z0-9])([A-Z])').sub, r'\1_\2')


def snake_case(string: str) -> str:
    return _snake_2(_snake_1(string)).casefold()


def spinal_case(string: str) -> str:
    return snake_case(string).replace('_', '-')


async def gather_limit(max_concurr, *tasks):
    semaphore = asyncio.Semaphore(max_concurr)

    async def run_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(run_task(task) for task in tasks))
