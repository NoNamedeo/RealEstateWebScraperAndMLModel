from Abstractions.IElement import IElement

class NodriverElement(IElement):
    
    def __init__(self, element):
        self._element = element

    async def get_content(self):
        if self._element:
            return self._element.text
        return None
    
    async def get_children(self):
        children = []
        for child in self._element.children:
            children.append(NodriverElement(child))
        return children
    
    async def click(self):
        if self._element:
            await self._element.click()
        else:
            print("Warning: Element is None, cannot click")

    async def get_attributes(self):
        if self._element:
            return self._element.attributes
        return None

    async def get_html(self):
        if self._element:
            return await self._element.get_html()
        return None