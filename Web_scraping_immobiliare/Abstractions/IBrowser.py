from abc import ABC, abstractmethod

class IBrowser(ABC):
    
    @abstractmethod
    async def start(self, **start_kwargs):
        pass
    
    @abstractmethod
    async def set_url(self, url) -> None:
        pass
    
    @abstractmethod
    async def find_element(self, by, value, timeout):
        pass
    
    @abstractmethod
    async def find_elements(self, by, value, timeout):
        pass
    
    @abstractmethod
    async def click(self, by, value):
        pass
    
    @abstractmethod
    async def back(self):
        pass
    
    @abstractmethod
    async def get_current_window(self):
        pass
    
    @abstractmethod
    async def get_all_windows(self):
        pass
    
    @abstractmethod
    async def switch_to_window(self, window):
        pass
    
    @abstractmethod
    async def close_window(self):
        pass