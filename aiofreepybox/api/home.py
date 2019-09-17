# Home structure : adapter > node > endpoint
class Home:

    def __init__(self, access):
        self._access = access

    async def get_adapter(self, adapter_id):
        '''
        Retrieve a registered HomeAdapter
        '''
        return await self._access.get('home/adapters/{0}'.format(adapter_id))

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

    async def get_endpoint_value(self, node_id, endpoint_id):
        '''
        Get endpoint value
        '''
        return await self._access.get('home/endpoints/{0}/{1}'.format(node_id, endpoint_id))

    async def set_endpoint_value(self, node_id, endpoint_id, value):
        '''
        Set endpoint value
        '''
        self._access.put('home/endpoints/{0}/'.format(node_id), endpoint_id, value)

    async def del_link(self, link_id):
        '''
        Delete link
        '''
        return await self._access.delete('home/links/', link_id)

    async def get_link(self, link_id):
        '''
        Get link
        '''
        return await self._access.get('home/links/{0}'.format(link_id))

    async def get_links(self):
        '''
        Get links
        '''
        return await self._access.get('home/links/')

    async def del_node(self, node_id):
        '''
        Delete node id
        '''
        return await self._access.delete('home/nodes/', node_id)

    async def get_node(self, node_id):
        '''
        Get node id
        '''
        return await self._access.get('home/nodes/{0}'.format(node_id))

    async def set_node(self, node_id, node_data):
        '''
        Set node data
        '''
        return await self._access.put('home/nodes/', node_id, node_data)

    async def get_nodes(self):
        '''
        Get nodes
        '''
        return await self._access.get('home/nodes/')

    async def get_pairing_state(self, adapter_id):
        '''
        Get the current pairing state
        '''
        return await self._access.get('home/pairing/{0}'.format(adapter_id))

    async def set_rule(self, template_name, create_payload):
        '''
        Set node rule
        '''
        return await self._access.post('home/rules/', template_name, create_payload)

    async def get_rule_config(self, node_id, template_name, role_id):
        '''
        Get node rule configuration data
        '''
        return await self._access.get('home/nodes/{0}/rules/template/{1}/{2}'.format(node_id, template_name, role_id))

    async def set_rule_config(self, rule_node_id, node_rule_data):
        '''
        Set node rule configuration data
        '''
        self._access.put('home/rules/', rule_node_id, node_rule_data)

    async def get_rules(self, node_id):
        '''
        Get node rules
        '''
        return await self._access.get('home/nodes/{0}/rules'.format(node_id))

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

    async def get_tile(self, tile_id):
        '''
        Get the Tile with provided id
        '''
        return await self._access.get('home/tileset/{0}'.format(tile_id))

    async def get_tilesets(self):
        '''
        Get the list of Tileset
        '''
        return await self._access.get('home/tileset/all')

    async def pairing_next(self, adapter_id, next_payload):
        '''
        Start pairing step
        '''
        return await self._access.post('home/pairing/', adapter_id, next_payload)

    async def pairing_start(self, adapter_id, start_payload):
        '''
        Start pairing step
        '''
        return await self._access.post('home/pairing/', adapter_id, start_payload)

    async def pairing_stop(self, adapter_id, stop_payload):
        '''
        Stop pairing
        '''
        return await self._access.post('home/pairing/', adapter_id, stop_payload)
