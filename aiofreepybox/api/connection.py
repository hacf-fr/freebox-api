class Connection:

    def __init__(self, access):
        self._access = access

    async def get_status(self):
        '''
        Get connection status:
        '''
        return await self._access.get('connection/')

    async def get_config(self):
        '''
        Get connection configuration:
        '''
        return await self._access.get('connection/config/')

    async def set_config(self, conf):
        '''
        Update connection configuration:
        '''
        await self._access.put('connection/config/', conf)

    async def get_xdsl(self):
        '''
        Get xdsl infos:
        '''
        return await self._access.get('connection/xdsl/')

    async def get_ftth(self):
        '''
        Get ftth infos:
        '''
        return await self._access.get('connection/ftth/')
