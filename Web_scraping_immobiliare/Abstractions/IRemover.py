from abc import ABC, abstractmethod
from Abstractions.IBrowser import IBrowser

class IRemover(ABC):

    @abstractmethod
    async def remove(self, browser: IBrowser):
        pass