# modified fetch function with semaphore
import random
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from aiohttp import ClientSession

async def fetch(url, session, params):
    async with session.post(url, params=params, data=params) as response:
        delay = response.headers.get("DELAY")
        date = response.headers.get("DATE")
        # print("{}:{} with delay {}".format(date, response.url, delay))
        rs = await response.read()
        print(rs)
        return rs


async def bound_fetch(sem, url, session, params):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session, params)


async def run(r):
    url = "http://localhost:5000/"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(r):
            params = {
                'username': 'pouria' + str(i),
                'password': 'ali'
            }
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url + 'signup', session, params))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

    async with ClientSession() as session:
        for i in range(r):
            params = {
                'username': 'pouria' + str(i),
                'password': 'ali'
            }
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url + 'login', session, params))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

number = 10000
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)