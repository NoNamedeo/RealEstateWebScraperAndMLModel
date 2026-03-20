from abc import ABC, abstractmethod

class IElement(ABC):
    
    @abstractmethod
    async def get_content(self):
        pass
    
    @abstractmethod
    async def get_children(self):
        pass
    
    @abstractmethod
    async def click(self):
        pass

    @abstractmethod
    async def get_attributes(self):
        pass

    @abstractmethod
    async def get_html(self):
        pass