from Enums.SearchBy import SearchBy
from Abstractions.IRemover import IRemover
from Abstractions.IBrowser import IBrowser

class ImmobiliareFlatCookieBannersRemover(IRemover):

    def __init__(self):
        pass
    
    async def remove(self, browser: IBrowser):
        try:
            flat_banner = await browser.find_element(SearchBy.CLASS, "ab-message-button")
            await flat_banner.click()
        except:
            pass