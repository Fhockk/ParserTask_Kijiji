import asyncio
import aiohttp
import re
import json
import time
from bs4 import BeautifulSoup
from send import publish

"""FIX ERROR"""
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper

_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

"""END OF FIX ERROR"""

# starttime = time.time()
# page_parsed = []
# links = []
unq_links = []


class ParsePages:
    def __init__(self):
        self.starttime = time.time()
        self.page_parsed = []
        self.links = []

    async def get_page_data(self, session, page):
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        urls = [f'https://www.kijiji.ca/b-apartments-condos/alberta/page-{page}/c37l9003',
                f'https://www.kijiji.ca/b-apartments-condos/british-columbia/page-{page}/c37l9007',
                f'https://www.kijiji.ca/b-apartments-condos/manitoba/page-{page}/c37l9006',
                f'https://www.kijiji.ca/b-apartments-condos/nova-scotia/page-{page}/c37l9002',
                f'https://www.kijiji.ca/b-apartments-condos/new-brunswick/page-{page}/c37l9005',
                f'https://www.kijiji.ca/b-apartments-condos/newfoundland/page-{page}/c37l9008',
                f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273?ad=offering',
                f'https://www.kijiji.ca/b-apartments-condos/prince-edward-island/page-{page}/c37l9011',
                f'https://www.kijiji.ca/b-appartement-condo/quebec/page-{page}/c37l9001',
                f'https://www.kijiji.ca/b-apartments-condos/saskatchewan/page-{page}/c37l9009'
                ]
        # url = f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273?ad=offering"
        for url in urls:
            try:
                async with session.get(url=url, headers=headers) as response:
                    response_text = await response.text()
                    self.page_parsed.append(page)
                    soup = BeautifulSoup(response_text, 'lxml')
                    all_adds = soup.findAll(class_='search-item')
                    unq = []
                    for ad in all_adds:
                        unq.append('https://www.kijiji.ca' + ad.select_one('a.title').get('href'))
                        self.links.append('https://www.kijiji.ca' + ad.select_one('a.title').get('href'))
                    print(f"Обработал страницу {page}")
                    publish(unq)
                    # print(len(unq))
            except (aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ClientOSError,
                    aiohttp.client_exceptions.ServerDisconnectedError):
                continue

    async def gather_data(self):
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        urls = [f'https://www.kijiji.ca/b-apartments-condos/alberta/c37l9003',
                f'https://www.kijiji.ca/b-apartments-condos/british-columbia/c37l9007',
                f'https://www.kijiji.ca/b-apartments-condos/manitoba/c37l9006',
                f'https://www.kijiji.ca/b-apartments-condos/nova-scotia/c37l9002',
                f'https://www.kijiji.ca/b-apartments-condos/new-brunswick/c37l9005',
                f'https://www.kijiji.ca/b-apartments-condos/newfoundland/c37l9008',
                f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering',
                f'https://www.kijiji.ca/b-apartments-condos/prince-edward-island/c37l9011',
                f'https://www.kijiji.ca/b-appartement-condo/quebec/c37l9001',
                f'https://www.kijiji.ca/b-apartments-condos/saskatchewan/c37l9009'
                ]
        # url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering'
        connector = aiohttp.TCPConnector(force_close=True)
        for url in urls:
            try:
                async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
                    response = await session.get(url=url, headers=headers)
                    info = re.search(r'var dataLayer = (.+)', str(await response.text()))
                    info_js = info.group(1)[:-1][1:-1]
                    html = json.loads(info_js)
                    ad_count = html['s']['tr']
                    pages_count = int(ad_count/45)
                    if pages_count > 100:
                        pages_count = 100
                    tasks = []

                    for page in range(1, pages_count):
                        task = asyncio.create_task(self.get_page_data(session, page))
                        tasks.append(task)

                    await asyncio.gather(*tasks)
            except RuntimeError:
                continue

    def main(self):
        global unq_links
        asyncio.run(self.gather_data())
        # asyncio.get_event_loop().run_until_complete(gather_data())
        finishtime = time.time() - self.starttime
        unq_links = list(set(self.links))
        # print(links)
        print("TIME: " + str(finishtime))


# For test
if __name__ == '__main__':
    first = ParsePages()
    first.main()


