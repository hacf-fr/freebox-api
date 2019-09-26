class Dhcp:

    def __init__(self, access):
        self._access = access

    static_lease_schema = {
        'ip': '',
        'mac': '',
        'comment': ''
    }

    dhcp_configuration_schema = {
        'alwaysBroadcast': bool,
        'dns': [''],
        'enabled': bool,
        'ipRangeStart': '',
        'ipRangeEnd': '',
        'stickyAssign': bool
    }

    dhcp_v6_configuration_data_schema = {
        'dns': [''],
        'enabled': bool,
        'useCustomDns': bool
    }

    async def create_dhcp_static_lease(self, static_lease=static_lease_schema):
        '''
        Create dhcp static lease
        '''
        return await self._access.post('dhcp/static_lease/', static_lease)

    async def delete_dhcp_static_lease(self, lease_id):
        '''
        Delete dhcp static lease
        '''
        await self._access.delete(f'dhcp/static_lease/{lease_id}')

    async def edit_dhcp_static_lease(self, lease_id, static_lease=static_lease_schema):
        '''
        Edit dhcp static lease
        '''
        return await self._access.put(f'dhcp/static_lease/{lease_id}', static_lease)

    async def get_config(self):
        '''
        Get DHCP configuration
        '''
        return await self._access.get('dhcp/config/')

    async def set_config(self, dhcp_configuration=dhcp_configuration_schema):
        '''
        Update a config with new conf dictionary
        '''
        return await self._access.put('dhcp/config/', dhcp_configuration)

    async def get_v6_config(self):
        '''
        Get DHCP v6 configuration
        '''
        return await self._access.get('dhcpv6/config/')

    async def set_v6_config(self, dhcp_v6_configuration_data=dhcp_v6_configuration_data_schema):
        '''
        Update DHCP v6 configuration
        '''
        return await self._access.put('dhcpv6/config/', dhcp_v6_configuration_data)

    async def get_dynamic_dhcp_lease(self):
        '''
        Get the list of DHCP dynamic leases
        '''
        return await self._access.get('dhcp/dynamic_lease/')

    async def get_static_dhcp_lease(self):
        '''
        Get the list of DHCP static leases
        '''
        return await self._access.get('dhcp/static_lease/')
