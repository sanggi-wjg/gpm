class PageQueryParameter:
    __slots__ = ['offset', 'limit']

    def __init__(self, offset: int = 0, limit: int = 10):
        self.offset = offset
        self.limit = limit


class TechStackSearch(PageQueryParameter):
    __slots__ = ['name']

    def __init__(self, offset: int = 0, limit: int = 10, name: str = None):
        super().__init__(offset, limit)
        self.name = name
