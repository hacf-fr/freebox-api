# Home structure : adapter > node > endpoint
class Home:

    def __init__(self, access):
        self._access = access

    async def get_adapters(self):
        '''
        Retrieve the list of registered HomeAdapters
        '''
        return await self._access.get('home/adapters/')

    async def get_endpointvalue(self, nodeid, endpointid):
        '''
        Get endpoint value
        '''
        return await self._access.get('home/endpoints/{0}/'.format(nodeid), endpointid)

    async def set_endpointvalue(self, nodeid, endpointid, value):
        '''
        Set endpoint value
        '''
        self._access.put('home/endpoints/{0}/'.format(nodeid), endpointid, value)

    async def get_endpointvalues(self):
        '''
        Get endpoint values
        '''
        return await self._access.get('home/endpointvalues/')

    async def get_node(self, nodeid):
        '''
        Get node id
        '''
        return await self._access.get('home/nodes/', nodeid)

    async def get_nodes(self):
        '''
        Get nodes
        '''
        return await self._access.get('home/nodes/')

    async def get_tile(self, tileid):
        '''
        Get the Tile with provided id
        '''
        return await self._access.get('home/tileset/', tileid)

    async def get_tilesets(self):
        '''
        Get the list of Tileset
        '''
        return await self._access.get('home/tileset/all')
