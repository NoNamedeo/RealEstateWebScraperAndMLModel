from Enums.SearchBy import SearchBy
from Abstractions.IScraper import IScraper

class ImmobiliarePriceScraper(IScraper):
    
    def __init__(self):
        pass

    async def scrape(self, browser) -> dict:
        
        price_div = await browser.find_element(SearchBy.CSS, ".Overview_price__4hIcc")
        if price_div:
            if (await price_div.get_content()) == "da ":
                span_1 = (await price_div.get_children())[-1]
                span_2 = (await span_1.get_children())[-1]
                price = await span_2.get_content()
                return {"Asta": True, "Prezzo": price}
            else:
                if any(c.isdigit() for c in (await price_div.get_content())):
                    price = await price_div.get_content()
                    return {"Asta": False, "Prezzo": price}
                    
                else:
                    price_text = await price_div.get_content()
                    return {"Prezzo": price_text}
        return {"Prezzo": None}