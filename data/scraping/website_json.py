import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def check_website(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            tables = soup.find_all('table')
            table_count = len(tables)
            table_info = [{'id': table.get('id'), 'class': table.get('class')} for table in tables]

            lists_with_id = soup.find_all(['ul', 'ol'], id=True)
            list_with_id_count = len(lists_with_id)
            list_with_id_info = [{'id': lst.get('id'), 'class': lst.get('class')} for lst in lists_with_id]

            return {
                "table_count": table_count,
                "table_info": table_info,
                "list_with_id_count": list_with_id_count,
                "list_with_id_info": list_with_id_info,
            }
        
async def process_urls(urls):
    tasks = [check_website(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    # urls = ["https://finance.yahoo.com/topic/economic-news"]
    urls = ["https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes"]

    result = await check_website(urls[0])
    print(f"Table count: {result['table_count']}")
    print(f"Table info: {result['table_info']}")
    print(f"List with id count: {result['list_with_id_count']}")
    print(f"List with id info: {result['list_with_id_info']}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())



