#!/usr/bin/env python3
import asyncio
import re
import time
from aiohttp import request
from aiomultiprocess import Pool
from functools import partial

TITLE_REGEXP = re.compile(r'<title>(.*)</title>')
IDXS = range(20)
URL = 'https://google.com/'


async def get(url, idx):
    async with request('GET', url) as response:
        return (await response.text('latin1'), idx)


PARTIAL_GET = partial(get, URL)


async def aiomultiprocess_test():
    print('''
===========================aiomultiprocess======================================
''')
    async with Pool() as pool:
        async for result, idx in pool.map(PARTIAL_GET, IDXS):
            # Do some work on the result and display it
            print(re.findall(TITLE_REGEXP, result)[0], idx)
    print('''
================================================================================
''')


async def asyncio_test():
    print('''
===========================asyncio==============================================
''')
    tasks = [asyncio.create_task(PARTIAL_GET(idx)) for idx in IDXS]
    for task in asyncio.as_completed(tasks):
        result, idx = await task
        # Do some work on the result and display it
        print(re.findall(TITLE_REGEXP, result)[0], idx)
    print('''
================================================================================
''')


if __name__ == '__main__':
    start_multi = time.time()
    asyncio.run(aiomultiprocess_test())
    end_multi = time.time()

    start_asyncio = time.time()
    asyncio.run(asyncio_test())
    end_asyncio = time.time()

    print(f'aiomultiprocess: {end_multi - start_multi}s')
    print(f'asyncio: {end_asyncio - start_asyncio}s')
