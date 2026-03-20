from Abstractions.IScraper import IScraper
from Enums.SearchBy import SearchBy
import json
import re

class ImmobiliarePositionScraper(IScraper):

    def __init__(self):
        pass

    async def scrape(self, browser) -> dict:
        data = {}

        next_data = await browser.find_element(SearchBy.ID, "__NEXT_DATA__")
        json_string = await next_data.get_html()

        #re che elimina i "<...>" ai lati del json
        match = re.match(r'^<[^>]*>(.*)<[^>]*>$', json_string)
        if match:
            json_string = match.group(1)

        try:
            data_json = json.loads(json_string)

            latitude = data_json["props"]["pageProps"]["detailData"]["realEstate"]["properties"][0]["location"]["latitude"]
            longitude = data_json["props"]["pageProps"]["detailData"]["realEstate"]["properties"][0]["location"]["longitude"]

            data["Latitudine"] = latitude
            data["Longitudine"] = longitude
            return data
        except Exception as e:
            print(e)
            return data

