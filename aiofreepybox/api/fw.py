class Fw:

    def __init__(self, access):
        self._access = access

    ip_proto = [
        'tcp',
        'udp'
    ]

    port_forwarding_config_schema = {
        'comment': '',
        'enabled': bool,
        'ipProto': ip_proto[0],
        'lanIp': '',
        'lanPort': int,
        'srcIp': '',
        'wanPortEnd': int,
        'wanPortStart': int
    }

    incoming_port_configuration_data_schema = {
        'enabled': bool,
        'inPort': int
    }

    dmz_configuration_schema = {
        'enabled': bool,
        'ip': ''
    }

    async def create_port_forwarding_configuration(self, port_forwarding_config=port_forwarding_config_schema):
        '''
        Create port forwarding configuration
        '''
        return await self._access.post('fw/redir/', port_forwarding_config)

    async def delete_port_forwarding_configuration(self, config_id):
        '''
        Delete port forwarding configuration
        '''
        await self._access.delete(f'fw/redir/{config_id}')

    async def edit_incoming_port_configuration(self, port_id, incoming_port_configuration_data=incoming_port_configuration_data_schema):
        '''
        Edit incoming port configuration
        '''
        return await self._access.put(f'fw/incoming/{port_id}', incoming_port_configuration_data)

    async def get_dmz_configuration(self):
        '''
        Get dmz configuration
        '''
        return await self._access.get('fw/dmz/')

    async def get_incoming_ports_configuration(self):
        '''
        Get incoming ports configuration
        '''
        return await self._access.get('fw/incoming/')

    async def get_port_forwarding_configuration(self):
        '''
        Get port forwarding configuration
        '''
        return await self._access.get('fw/redir/')

    async def set_dmz_configuration(self, dmz_configuration=dmz_configuration_schema):
        '''
        Set dmz configuration
        '''
        return await self._access.put('fw/dmz/', dmz_configuration)
