from Abstractions.IScraper import IScraper
from Enums.SearchBy import SearchBy


class ImmobiliareTitleScraper(IScraper):

    def __init__(self):
        self._unknown_flat_number = 0

    async def scrape(self, browser) -> dict:
        title = await browser.find_element(SearchBy.CLASS, "Title_title__EKYn1")
        if title:
            return {"Titolo": await title.get_content()}
        self._unknown_flat_number += 1
        return {"Titolo": f"Appartamento sconosciuto numero {self._unknown_flat_number}"}