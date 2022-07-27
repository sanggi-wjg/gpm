class PageQueryParameter:
    __slots__ = ['offset', 'limit']

    def __init__(self, offset: int, limit: int):
        self.offset = offset
        self.limit = limit


async def page_parameter(offset: int = 0, limit: int = 10) -> PageQueryParameter:
    return PageQueryParameter(offset=offset, limit=limit)
