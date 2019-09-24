class Lan:

    def __init__(self, access):
        self._access = access

    wol_schema = {
        'mac': str(),
        'password': str()
    }

    async def get_config(self):
        '''
        Get Lan configuration
        '''
        return await self._access.get('lan/config/')

    async def set_config(self, conf):
        '''
        Update Lan config with conf dictionary
        '''
        await self._access.put('lan/config/', conf)

    async def get_interfaces(self):
        '''
        Get browsable Lan interfaces
        '''
        return await self._access.get('lan/browser/interfaces')

    async def get_hosts_list(self, interface='pub'):
        '''
        Get the list of hosts on a given interface
        '''
        return await self._access.get('lan/browser/{0}'.format(interface))

    async def get_host_information(self, host_id, interface='pub'):
        '''
        Get specific host informations on a given interface
        '''
        return await self._access.get('lan/browser/{0}/{1}'.format(interface, host_id))

    async def set_host_information(self, host_id, conf, interface='pub'):
        '''
        Update specific host informations on a given interface
        '''
        await self._access.put('lan/browser/{0}/{1}'.format(interface, host_id), conf)

    async def wake_lan_host(self, wol=wol_schema, interface='pub'):
        '''
        Wake lan host
        '''
        return await self._access.post('lan/wol/{0}/'.format(interface), wol)
