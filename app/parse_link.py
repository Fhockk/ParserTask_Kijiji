# from parse_pages import unq_links
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import re
import json
import time
from send_tobd import publish

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

# links = ['https://www.kijiji.ca/v-apartments-condos/city-of-toronto/1-bedroom-den-condo-downtown-toronto/1627643774', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/beautiful-new-2-bedroom-condo-at-lawrence-dufferin/1636833573', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/2-beds-1-bath-sunny-bright-two-bedroom-basement-apartment-for/1636193936', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/private-room-available-immediately-north-york-scarborough/1636819687', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/room-for-rent-700-for-men-only/1636818822', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/buy-a-house-with-zero-down-5-or-10-program/1577240418', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/one-b-r-basement-for-rent-separate-entrance/1636809522', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/2-bed-den-2-bath-condo-with-parking-for-rent-in-scarborough/1636808417', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/apartment-for-rent-in-victoria-village-sundial-crescent/1636804807', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/one-yonge:-beautiful-2bed-and-lake-views-in-prime-harbourfront/1636793728', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/beautiful-lakeshore-condos-for-rent-88-park-lawn-rd/1636786767', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/for-rent-studio-on-richmond-2bdrm-2baths-locker/1636481803', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/large-3-bedroom-house-with-finished-basement-for-rent/1636789654', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/bachelor-for-lease-near-tmu/1636785218', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/condominium-apartment-for-rent/1636783469', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/gorgeous-waterfront-bachelor-for-lease/1636782288', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/looking-for-land-to-rent/1636776129', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/sunny-spacious-furnished-condo-in-torontos-west-end/1636765564', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/southeast-2-bedroom-waterfront/1636763633', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/students-and-refugees-accommodation-in-downtown/1636756591', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/student-accommodation/1636755941', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/house-for-lease-rent/1636755631', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/large-2-bed-den-including-utilities-for-3875-downtown-toronto/1636754816']
# links = ['https://www.kijiji.ca/v-apartments-condos/city-of-toronto/bachelor-apartement-in-great-location-bayview-and-davisville/1639057928', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/fully-renovated-2-bedroom-in-etobicoke/1639869260', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/small-bedroom-for-rent/1639421000', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/room-for-rent/1639420846', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/2-bedroom-3-bathroom-corner-townhouse-1200sqft/1639407483', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/basement-apartment-for-rent/1639406824', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/modern-one-bedroom-apartment/1639406639', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/house-for-rent/1639404370', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/3-bedrooms-and-2-5-washrooms/1639403978', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/quiet-and-private-room-1-bedroom-basement-unit-for-rent/1639403381', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/a-luxury-2-bed-2-bath-condominuim-for-rent/1635511108', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/cozy-spacious-renovated-1-bedroom-pad-danforth-pape-w-patio/1639401549', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/affordable-truck-rental-moving-services-647-488-7711/1639399750', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/4-story-5-bedroom-home/1639398174', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/3-bedroom-condo-for-rent/1639397522', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/bachelor-suit-on-davenport-dufferin/1639397112', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/in-the-market-additional-condos-available-now-in-downtown/1639394161', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/in-the-market-additional-condos-available-now-in-downtown/1639395707', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/1-bedroom-college-and-dufferin/1639394363', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/newly-renovated-multiunit-with-3-separate-units/1639393749', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/house-for-rent/1639393597', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/house-for-rent/1639392219', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/brand-new-basement-apartment-for-rent/1639391609', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/furnished-studio-apt-in-downtown-core-walk-to-eaton-centre/1639390814', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/furnished-one-bedroom-apartment/1639390128', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/1-bedroom-basement-apartment/1639389491', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/young-wellesley-1-bed1bath-condo-available-february-1st-2023/1639388710', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/golden-equity-properties-at-514-516-dawes-rd-toronto-east-york/1616340887', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/two-bdrm-two-bath-condo-with-great-view-in-regent-park/1604844268', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/rentals-at-brentwood-towers-lascelles-yonge-davisville/1631944716', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/furnished-house-2-bed-den-1-bath-in-east-york/1635721133', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/basement-for-rent/1639381098', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/space-for-lease-available-immediately/1639385673', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/the-prestige-new-never-occupied/1637516755', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/high-end-downtown-condo-fully-furnished/1639381810', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/2-bedroom-apartment-for-rent:-jane-finch-2-100-a-month/1639380959', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/3-bedroom-bungalow-upper-unit-for-rent/1639002534', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/yonge-and-sheppard-furnished-2-bedroom-2-bathroom-for-rent/1639374195', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/new-condo-for-rent/1639375569', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/room-for-rent/1639377485', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/2-bedroom-basement-apartment/1639374943', 'https://www.kijiji.ca/v-apartments-condos/city-of-toronto/2-bedroom-basement-appt-for-rent/1639372962']

all_data = []
# data = {}


class ParseLinks:
    def __init__(self):
        self.starttime = time.time()
        self.data = {}

    async def get_page_data(self, session, link):
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        try:
            async with session.get(url=link, headers=headers) as response:
                response_text = await response.text()

                soup = BeautifulSoup(response_text, 'lxml')
                info = re.search(r'var dataLayer = (.+)', str(response_text)).group(1)[:-1][1:-1]
                dictt = json.loads(info)


                try:
                    ad_id = soup.select_one("li.currentCrumb-3831268168").find("a").text
                except:
                    ad_id = None

                try:
                    title = soup.select_one("h1.title-2323565163").text.strip()
                except:
                    title = None

                try:
                    locationn = soup.select_one("span.address-3617944557").text.strip()
                except:
                    locationn = None

                try:
                    item_posted = soup.select_one("div.datePosted-383942873").find("time").get("datetime")[:10]
                    # item_posted = soup.select_one("div.datePosted-383942873").find('span').get('title')              # .find("time").get("datetime")[:10]
                    # itemm_postt = item_posted.find('span').get('title')
                except:
                    item_posted = None

                try:
                    price = str(dictt['a']['prc']['amt'])[:-2]
                except:
                    price = None

                try:
                    utilities = soup.select_one("span.utilities-3542420827").text.strip()[:-18]
                except:
                    utilities = None

                try:
                    author_id = re.search(r'"otherAdsUrl":".+u002F(\d+)","isAdmarkt"', str(response_text)).group(1)
                except:
                    author_id = None

                # role = soup.select_one("div.line-2791721720").text.strip()

                try:
                    author_name = soup.select_one("a.link-2686609741").text.strip()
                except:
                    author_name = None

                try:
                    role = soup.select_one("div.line-2791721720").text.strip()
                except:
                    role = None

                try:
                    hydro = dictt['a']['attr']['hydro_s']  # 0 bool
                    if int(hydro):
                        hydro = True
                    else:
                        hydro = False
                except:
                    hydro = None

                try:
                    heat = dictt['a']['attr']['heat_s']  # 1
                    if int(heat):
                        heat = True
                    else:
                        heat = False
                except:
                    heat = None

                try:
                    water = dictt['a']['attr']['water_s']  # 0
                    if int(water):
                        water = True
                    else:
                        water = False
                except:
                    water = None

                try:
                    parking = dictt['a']['attr']['numberparkingspots_s']
                    if int(parking):
                        parking = True
                    else:
                        parking = False
                except:
                    parking = None

                try:
                    agr_type = dictt['a']['attr']['agreementtype_s']
                except:
                    agr_type = None

                try:
                    moveindate = dictt['a']['attr']['dateavailable_tdt'][:10]
                except:
                    moveindate = None

                try:
                    pet = dictt['a']['attr']['petsallowed_s']
                    if int(pet):
                        pet = True
                    else:
                        pet = False
                except:
                    pet = None

                try:
                    sizee = dictt['a']['attr']['areainfeet_i']
                except:
                    sizee = None

                try:
                    furnished = dictt['a']['attr']['furnished_s']
                    if int(furnished):
                        furnished = True
                    else:
                        furnished = False
                except:
                    furnished = None

                try:
                    dishwasher = dictt['a']['attr']['dishwasher_s']
                    if int(dishwasher):
                        dishwasher = True
                    else:
                        dishwasher = False
                except:
                    dishwasher = None

                try:
                    fridge = dictt['a']['attr']['fridgefreezer_s']
                    if int(fridge):
                        fridge = True
                    else:
                        fridge = False
                except:
                    fridge = None

                try:
                    air_cond = dictt['a']['attr']['airconditioning_s']
                    if int(air_cond):
                        air_cond = True
                    else:
                        air_cond = False
                except:
                    air_cond = None

                try:
                    balcony = dictt['a']['attr']['balcony_s']
                    if int(balcony):
                        balcony = True
                    else:
                        balcony = False
                except:
                    balcony = None

                try:
                    smoking = dictt['a']['attr']['smokingpermitted_s']
                    if int(smoking):
                        smoking = True
                    else:
                        smoking = False
                except:
                    smoking = None

                try:
                    gym = dictt['a']['attr']['gym_s']
                    if int(gym):
                        gym = True
                    else:
                        gym = False
                except:
                    gym = None

                try:
                    pool = dictt['a']['attr']['pool_s']
                    if int(pool):
                        pool = True
                    else:
                        pool = False
                except:
                    pool = None

                try:
                    concierge = dictt['a']['attr']['concierge_s']
                    if int(concierge):
                        concierge = True
                    else:
                        concierge = False
                except:
                    concierge = None

                try:
                    security = dictt['a']['attr']['twentyfourhoursecurity_s']
                    if int(security):
                        security = True
                    else:
                        security = False
                except:
                    security = None

                try:
                    bicycle_park = dictt['a']['attr']['bicycleparking_s']
                    if int(bicycle_park):
                        bicycle_park = True
                    else:
                        bicycle_park = False
                except:
                    bicycle_park = None

                try:
                    storage_space = dictt['a']['attr']['storagelocker_s']
                    if int(storage_space):
                        storage_space = True
                    else:
                        storage_space = False
                except:
                    storage_space = None

                try:
                    elevator = dictt['a']['attr']['elevator_s']
                    if int(elevator):
                        elevator = True
                    else:
                        elevator = False
                except:
                    elevator = None

                try:
                    barrier = dictt['a']['attr']['barrierfreeentrancesandramps_s']
                    if int(barrier):
                        barrier = True
                    else:
                        barrier = False
                except:
                    barrier = None

                try:
                    vis_aid = dictt['a']['attr']['visualaids_s']
                    if int(vis_aid):
                        vis_aid = True
                    else:
                        vis_aid = False
                except:
                    vis_aid = None

                try:
                    acc_wash = dictt['a']['attr']['accessiblewashroomsinsuite_s']
                    if int(acc_wash):
                        acc_wash = True
                    else:
                        acc_wash = False
                except:
                    acc_wash = None

                try:
                    acc_wheelch = dictt['a']['attr']['wheelchairaccessible_s']
                    if int(acc_wheelch):
                        acc_wheelch = True
                    else:
                        acc_wheelch = False
                except:
                    acc_wheelch = None

                try:
                    description = soup.select_one("div.descriptionContainer-231909819").text[11:].replace('\n', ' ')
                except:
                    description = None

                data = {
                    'ad_id': ad_id,
                    'title': title,
                    'locationn': locationn,
                    'item_posted': item_posted,
                    'price': price,
                    'utilities': utilities,
                    'author_id': author_id,
                    'hydro': hydro,
                    'heat': heat,
                    'water': water,
                    'parking': parking,
                    'agr_type': agr_type,
                    'moveindate': moveindate,
                    'pet': pet,
                    'sizee': sizee,
                    'furnished': furnished,
                    'dishwasher': dishwasher,
                    'fridge': fridge,
                    'air_cond': air_cond,
                    'balcony': balcony,
                    'smoking': smoking,
                    'gym': gym,
                    'pool': pool,
                    'concierge': concierge,
                    'security': security,
                    'bicycle_park': bicycle_park,
                    'storage_space': storage_space,
                    'elevator': elevator,
                    'barrier': barrier,
                    'vis_aid': vis_aid,
                    'acc_wash': acc_wash,
                    'acc_wheelch': acc_wheelch,
                    'description': description,
                    'author_name': author_name,
                    'role': role
                }

                all_data.append(data)
                # print(data)
        except (aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ServerDisconnectedError):
            pass

    async def gather_data(self, unq):
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        connector = aiohttp.TCPConnector(force_close=True)
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                tasks = []
                for link in unq:
                    task = asyncio.create_task(self.get_page_data(session, link))
                    tasks.append(task)

                await asyncio.gather(*tasks)
        except RuntimeError:
            pass

    def main(self, unq):
        asyncio.run(self.gather_data(unq))
        finishtime = time.time() - self.starttime
        publish(all_data)
        # for _ in all_data:
        #     print(_)
        print("TIME: " + str(finishtime))


# For test
# if __name__ == '__main__':
#     second = ParseLinks()
#     second.main()





