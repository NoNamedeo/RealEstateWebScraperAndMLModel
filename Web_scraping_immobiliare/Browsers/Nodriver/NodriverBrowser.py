import nodriver as nd
from Enums.SearchBy import SearchBy
from Abstractions.IBrowser import IBrowser
from Enums.SearchBy import SearchBy
from Abstractions.IBrowser import IBrowser
from Browsers.Nodriver.NodriverElement import NodriverElement

class NodriverBrowser(IBrowser):
    
    def __init__(self):
        self._browser = None
        self._current_tab = None
        
    async def start(self, **start_kwargs):
        self._browser = await nd.start(**start_kwargs)

    async def set_url(self, url: str):
        self._current_tab = await self._browser.get(url)

    async def find_element(self, by, value, timeout=10):
        match by:
            case SearchBy.CSS:
                return NodriverElement(await self._current_tab.select(value, timeout=timeout))
            case SearchBy.XPATH:
                results = await self._current_tab.xpath(value, timeout=timeout)
                if not results:
                    raise Exception("Element not found")
                return NodriverElement(results[0])
            case SearchBy.CLASS:
                return NodriverElement(await self._current_tab.select(f".{value}", timeout=timeout))
            case SearchBy.ID:
                return NodriverElement(await self._current_tab.select(f"#{value}", timeout=timeout))
            case SearchBy.BEST_MATCH:
                return NodriverElement(await self._current_tab.select(value, best_match=True, timeout=timeout))
            case SearchBy.RAW_ELEMENT:
                return value
            case SearchBy.DICT_OF_QUERIES:
                raise Exception("no implementation in Nodriver for DICT_OF_QUERIES.")
            case _:
                raise Exception("SearchBy not supported for this method.")

    async def find_elements(self, by, value, timeout=10):
         match by:
            case SearchBy.CSS:
                results = await self._current_tab.select_all(value, timeout=timeout)
                elements = []
                for result in results:
                    elements.append(NodriverElement(result))
                return elements
            case SearchBy.XPATH:
                results = await self._current_tab.xpath(value, timeout=timeout)
                elements = []
                for result in results:
                    elements.append(NodriverElement(result))
                return elements
            case SearchBy.CLASS:
                results = await self._current_tab.select_all(f".{value}", timeout=timeout)
                elements = []
                for result in results:
                    elements.append(NodriverElement(result))
                return elements
            case SearchBy.ID:
                results = await self._current_tab.select_all(f"#{value}", timeout=timeout)
                elements = []
                for result in results:
                    elements.append(NodriverElement(result))
                return elements
            case SearchBy.BEST_MATCH:
                results = await self._current_tab.select_all(value, best_match=True, timeout=timeout)
                elements = []
                for result in results:
                    elements.append(NodriverElement(result))
                return elements
            case SearchBy.RAW_ELEMENT:
                return value
            case SearchBy.DICT_OF_QUERIES:
                raise Exception("no implementation in Nodriver for DICT_OF_QUERIES.")
            case _:
                raise Exception("SearchBy not supported for this method.")

    async def click(self, by, value):
        if by == SearchBy.RAW_ELEMENT:
            await value.click()
        else:
            element = await self.find_element(by, value)
            await element.click()

    async def back(self):
        await self._current_tab.back()

    async def get_current_window(self):
        return self._current_tab

    async def get_all_windows(self):
        return self._browser.tabs

    async def switch_to_window(self, window):
        self._current_tab = window

    async def close_window(self):
        await self._current_tab.close()
    