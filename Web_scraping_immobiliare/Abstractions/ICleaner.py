from abc import ABC, abstractmethod

class ICleaner(ABC):

    @abstractmethod
    async def clean(self, data):
        pass

    @abstractmethod
    async def get_cleaned_columns(self):
        pass
