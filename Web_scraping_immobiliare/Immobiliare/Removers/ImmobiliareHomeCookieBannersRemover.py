from Enums.SearchBy import SearchBy
from Abstractions.IRemover import IRemover
from Abstractions.IBrowser import IBrowser

class ImmobiliareHomeCookieBannersRemover(IRemover):

    def __init__(self):
        pass
    
    async def remove(self, browser: IBrowser):
        try:
            cookie_banner = await browser.find_element(SearchBy.ID, "didomi-notice-agree-button")
            await cookie_banner.click()
        except Exception as e:
            print("Except del cookie banner: ", e)
                
        try:
            save_research_banner = await browser.find_element(SearchBy.CLASS, "nd-dialogFrame__close")
            await save_research_banner.click()
        except Exception as e:
            print("Except del salva ricerca banner: ", e)