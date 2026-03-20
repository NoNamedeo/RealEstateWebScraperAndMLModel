from abc import ABC, abstractmethod
from Abstractions.IBrowser import IBrowser

class IScraper(ABC):

    @abstractmethod
    async def scrape(self, browser) -> dict:
        pass
