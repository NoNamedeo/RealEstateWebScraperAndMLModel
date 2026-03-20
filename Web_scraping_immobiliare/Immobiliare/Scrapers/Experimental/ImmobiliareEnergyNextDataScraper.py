from Abstractions.IScraper import IScraper
from Enums.SearchBy import SearchBy
import json
import re

class ImmobiliareEnergyNextDataScraper(IScraper):

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

            thermal_insulation = data_json["props"]["pageProps"]["detailData"]["realEstate"]["properties"][0]["energy"]["thermalInsulation"]
            heating_type = data_json["props"]["pageProps"]["detailData"]["realEstate"]["properties"][0]["energy"]["heatingType"]
            energy_status = data_json["props"]["pageProps"]["detailData"]["realEstate"]["properties"][0]["energy"]["energyStatus"]

            if(energy_status == "In attesa di certificazione"):
                energy_status = None

            data["Classe energetica"] = energy_status
            data["Cappotto termico"] = thermal_insulation
            data["Riscaldamento"] = heating_type

            return data
        except Exception as e:
            print(e)
            return data

