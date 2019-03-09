class Nat:

    def __init__(self, access):
        self._access = access

    async def get_all_redir(self):
        '''
        Get redirections configuration
        '''
        return await self._access.get('fw/redir/')

    async def get_redir(self, redir):
        '''
        Get redirections configuration
        '''
        return await self._access.get('fw/redir/{0}'.format(redir))

    async def set_redir(self, redir, conf):
        '''
        Set redirection configuration
        '''
        return await self._access.put('fw/redir/{0}'.format(redir), conf)

    async def get_all_inc(self):
        '''
        Get incoming ports configuration
        '''
        return await self._access.get('fw/incoming/')

    async def get_inc(self, inc):
        '''
        Get incoming port configuration
        '''
        return await self._access.get('fw/incoming/{}'.format(inc))

    async def set_inc(self, inc, conf):
        '''
        Set incoming port configuration
        '''
        return await self._access.put('fw/incoming/{}'.format(inc), conf)

    async def get_dmz(self):
        '''
        Get DMZ configuration
        '''
        return await self._access.get('fw/dmz/')

    async def set_dmz(self, conf):
        '''
        Set DMZ configuration
        '''
        return await self._access.put('fw/dmz/', conf)
