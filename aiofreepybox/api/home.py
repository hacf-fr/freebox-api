# Home structure : adapter > node > endpoint
class Home:

    def __init__(self, access):
        self._access = access

    async def get_adapter(self, adapterid):
        '''
        Retrieve a registered HomeAdapter
        '''
        return await self._access.get('home/adapters/', adapterid)

    async def get_adapters(self):
        '''
        Retrieve the list of registered HomeAdapters
        '''
        return await self._access.get('home/adapters/')

    async def get_camera(self):
        '''
        Get camera info
        '''
        return await self._access.get('camera/')

    async def get_endpoint_value(self, nodeid, endpointid):
        '''
        Get endpoint value
        '''
        return await self._access.get('home/endpoints/{0}/'.format(nodeid), endpointid)

    async def set_endpoint_value(self, nodeid, endpointid, value):
        '''
        Set endpoint value
        '''
        self._access.put('home/endpoints/{0}/'.format(nodeid), endpointid, value)

    async def del_link(self, linkid):
        '''
        Delete link
        '''
        return await self._access.delete('home/links/', linkid)

    async def get_link(self, linkid):
        '''
        Get link
        '''
        return await self._access.get('home/links/', linkid)

    async def get_links(self):
        '''
        Get links
        '''
        return await self._access.get('home/links/')

    async def del_node(self, nodeid):
        '''
        Delete node id
        '''
        return await self._access.delete('home/nodes/', nodeid)

    async def get_node(self, nodeid):
        '''
        Get node id
        '''
        return await self._access.get('home/nodes/', nodeid)

    async def set_node(self, nodeid, nodedata):
        '''
        Set node data
        '''
        return await self._access.put('home/nodes/', nodeid, nodedata)

    async def get_nodes(self):
        '''
        Get nodes
        '''
        return await self._access.get('home/nodes/')

    async def get_pairing_state(self, adapterid):
        '''
        Get the current pairing state
        '''
        return await self._access.get('home/pairing/', adapterid)

    async def set_rule(self, templatename, createpayload):
        '''
        Set node rule
        '''
        return await self._access.post('home/rules/', templatename, createpayload)

    async def get_rule_config(self, nodeid, templatename, roleid):
        '''
        Get node rule configuration data
        '''
        return await self._access.get('home/nodes/{0}/rules/template/{1}'.format(nodeid, templatename), roleid)

    async def set_rule_config(self, rulenodeid, noderuledata):
        '''
        Set node rule configuration data
        '''
        self._access.put('home/rules/', rulenodeid, noderuledata)

    async def get_rules(self, nodeid):
        '''
        Get node rules
        '''
        return await self._access.get('home/nodes/{0}/'.format(nodeid), 'rules')

    async def get_secmod(self):
        '''
        Get security module
        '''
        return await self._access.get('home/secmod/')

    async def get_sms_numbers(self):
        '''
        Get sms numbers
        '''
        return await self._access.get('home/sms/numbers')

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

    async def pairing_next(self, adapterid, nextpayload):
        '''
        Start pairing step
        '''
        return await self._access.post('home/pairing/', adapterid, nextpayload)

    async def pairing_start(self, adapterid, startpayload):
        '''
        Start pairing step
        '''
        return await self._access.post('home/pairing/', adapterid, startpayload)

    async def pairing_stop(self, adapterid, stoppayload):
        '''
        Stop pairing
        '''
        return await self._access.post('home/pairing/', adapterid, stoppayload)
