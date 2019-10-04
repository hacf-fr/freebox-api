class Nat:

    def __init__(self, access):
        self._access = access

    async def get_port_forwarding_list(self):
        """
        Get the list of port forwarding
        """
        return await self._access.get('fw/redir/')

    async def get_port_forwarding(self, redir_id):
        """
        Get a specific port forwarding
        """
        return await self._access.get(f'fw/redir/{redir_id}')

    async def set_port_forwarding(self, redir_id, port_configuration):
        """
        Update a port forwarding
        """
        return await self._access.put(f'fw/redir/{redir_id}', port_configuration)

    async def create_port_forwarding(self, port_configuration):
        """
        Add a port forwarding
        """
        return await self._access.post('fw/redir/', port_configuration)

    async def delete_port_forwarding(self, redir_id):
        """
        Delete a port forwarding
        """
        return await self._access.delete(f'fw/redir/{redir_id}')

    async def get_incoming_port_list(self):
        """
        Get the list of incoming ports
        """
        return await self._access.get('fw/incoming/')

    async def get_incoming_port(self, inc_port_id):
        """
        Get a specific incoming port
        """
        return await self._access.get(f'fw/incoming/{inc_port_id}')

    async def set_incoming_port(self, inc_port_id, port_configuration):
        """
        Update an incoming port
        """
        return await self._access.put(f'fw/incoming/{inc_port_id}', port_configuration)

    async def get_dmz(self):
        """
        Get the current DMZ configuration
        """
        return await self._access.get('fw/dmz/')

    async def set_dmz(self, dmz_configuration):
        """
        Update the current DMZ configuration
        """
        return await self._access.put('fw/dmz/', dmz_configuration)
