import asyncio
from Abstractions.IScraper import IScraper
from Enums.SearchBy import SearchBy

class ImmobiliareCharacteristicsScraper(IScraper):

    def __init__(self):
        pass

    async def scrape(self, browser) -> dict:
        #await asyncio.sleep(5)
        all_items_button = await browser.find_element(SearchBy.CLASS, "nd-button.PrimaryFeatures_button__B4aSd")
        await all_items_button.click()

        item_titles = await browser.find_elements(SearchBy.CLASS, "DialogSection_featureTitle__I21Ax")
        item_values = await browser.find_elements(SearchBy.CLASS, "DialogSection_description__FTCWE")

        if item_titles is not [] and item_values is not []:
            data = {}
            if len(item_titles) == len(item_values):
                for title, value in zip(item_titles, item_values):
                    data[await title.get_content()] = await value.get_content()

            close_items_button = await browser.find_element(SearchBy.CLASS, "nd-button.FeaturesDialog_close__j3tj6")
            await close_items_button.click()

            return data

        return {}