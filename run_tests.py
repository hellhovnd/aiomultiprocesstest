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
URLS = [URL] * 20


async def get(url):
    async with request('GET', url) as response:
        return await response.text('latin1')


async def get_with_index(url, idx):
    async with request('GET', url) as response:
        return (await response.text('latin1'), idx)


PARTIAL_GET = partial(get_with_index, URL)


async def aiomultiprocess_test_with_work():
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


async def asyncio_test_with_work():
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


async def aiomultiprocess_test_just_requests():
    print('''
===========================aiomultiprocess======================================
''')
    async with Pool() as pool:
        # Just execute the requests
        await pool.map(get, URLS)
    print('done!')
    print('''
================================================================================
''')


async def asyncio_test_just_requests():
    print('''
===========================asyncio==============================================
''')
    tasks = [asyncio.create_task(get(url)) for url in URLS]
    await asyncio.gather(*tasks)
    print('done!')
    print('''
================================================================================
''')



if __name__ == '__main__':
    start_multi_work = time.time()
    asyncio.run(aiomultiprocess_test_with_work())
    end_multi_work = time.time()

    start_asyncio_work = time.time()
    asyncio.run(asyncio_test_with_work())
    end_asyncio_work = time.time()

    start_multi_requests = time.time()
    asyncio.run(aiomultiprocess_test_just_requests())
    end_multi_requests = time.time()

    start_asyncio_requests = time.time()
    asyncio.run(asyncio_test_just_requests())
    end_asyncio_requests = time.time()

    print(f'aiomultiprocess - doing work: {end_multi_work - start_multi_work}s')
    print(f'asyncio - doing work: {end_asyncio_work - start_asyncio_work}s')
    print(f'aiomultiprocess - just requests: {end_multi_requests - start_multi_requests}s')
    print(f'asyncio - just requests: {end_asyncio_requests - start_asyncio_requests}s')
