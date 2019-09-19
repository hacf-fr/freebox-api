# Home structure : adapter > node > endpoint
class Home:

    def __init__(self, access):
        self._access = access

    async def del_home_adapter(self, home_adapter_id):
        '''
        Delete home adapter
        '''
        return await self._access.delete('home/adapters/{0}'.format(home_adapter_id))

    async def get_home_adapter(self, home_adapter_id):
        '''
        Retrieve a registered home adapter
        '''
        return await self._access.get('home/adapters/{0}'.format(home_adapter_id))

    async def get_home_adapters(self):
        '''
        Retrieve the list of registered home adapters
        '''
        return await self._access.get('home/adapters')

    async def get_camera(self):
        '''
        Get camera info
        '''
        return await self._access.get('camera')

    async def get_home_endpoint_value(self, node_id, endpoint_id):
        '''
        Get home endpoint value
        '''
        return await self._access.get('home/endpoints/{0}/{1}'.format(node_id, endpoint_id))

    async def get_home_endpoint_values(self, endpoint_list):
        '''
        Get home endpoint values
        '''
        return await self._access.post('home/endpoints/get', endpoint_list)

    async def set_home_endpoint_value(self, node_id, endpoint_id, value):
        '''
        Set home endpoint value
        '''
        return await self._access.put('home/endpoints/{0}/{1}'.format(node_id, endpoint_id), value)

    async def del_home_link(self, link_id):
        '''
        Delete home link
        '''
        return await self._access.delete('home/links/{0}'.format(link_id))

    async def get_home_link(self, link_id):
        '''
        Get home link
        '''
        return await self._access.get('home/links/{0}'.format(link_id))

    async def get_home_links(self):
        '''
        Get home links
        '''
        return await self._access.get('home/links')

    async def del_home_node(self, node_id):
        '''
        Delete home node id
        '''
        return await self._access.delete('home/nodes/{0}'.format(node_id))

    async def get_home_node(self, node_id):
        '''
        Get home node id
        '''
        return await self._access.get('home/nodes/{0}'.format(node_id))

    async def edit_home_node(self, node_id, node_data):
        '''
        Edit home node data
        '''
        return await self._access.put('home/nodes/{0}'.format(node_id), node_data)

    async def get_home_nodes(self):
        '''
        Get home nodes
        '''
        return await self._access.get('home/nodes')

    async def create_home_node_rule(self, template_name, create_home_node_payload):
        '''
        Create home node rule
        '''
        return await self._access.post('home/rules/{0}'.format(template_name), create_home_node_payload)

    async def get_home_node_existing_rule_config(self, node_id, rule_node_id, role_id):
        '''
        Get home node existing rule configuration data
        '''
        return await self._access.get('home/nodes/{0}/rules/node/{1}/{2}'.format(node_id, rule_node_id, role_id))

    async def get_home_node_template_rule_config(self, node_id, template_name, role_id):
        '''
        Get node rule template configuration data
        '''
        return await self._access.get('home/nodes/{0}/rules/template/{1}/{2}'.format(node_id, template_name, role_id))

    async def set_home_node_rule_config(self, rule_node_id, node_rule_data):
        '''
        Set node rule configuration data
        '''
        return await self._access.put('home/rules/{0}'.format(rule_node_id), node_rule_data)

    async def get_home_node_new_rules(self, node_id):
        '''
        Get node new rules
        '''
        return await self._access.get('home/nodes/{0}/rules'.format(node_id))

    async def get_secmod(self):
        '''
        Get security module
        '''
        return await self._access.get('home/secmod')

    async def create_sms_number(self, sms_number_data):
        '''
        Create sms number
        '''
        return await self._access.post('home/sms/numbers', sms_number_data)

    async def edit_sms_number(self, sms_number_id, sms_number_data):
        '''
        Edit sms number
        '''
        return await self._access.put('home/sms/numbers/{0}'.format(sms_number_id), sms_number_data)

    async def get_sms_numbers(self):
        '''
        Get sms numbers
        '''
        return await self._access.get('home/sms/numbers')

    async def send_sms_number_validation(self, sms_number_id, sms_validation_data):
        '''
        Send sms number validation
        '''
        return await self._access.post('home/sms/numbers/{0}/send_validation_sms'.format(sms_number_id), sms_validation_data)

    async def validate_sms_number(self, sms_number_id, sms_number_validation_data):
        '''
        Validate sms number
        '''
        return await self._access.post('home/sms/numbers/{0}/validate'.format(sms_number_id), sms_number_validation_data)

    async def get_home_tile(self, tile_id):
        '''
        Get the home tile with provided id
        '''
        return await self._access.get('home/tileset/{0}'.format(tile_id))

    async def get_home_tilesets(self):
        '''
        Get the list of home tileset
        '''
        return await self._access.get('home/tileset/all')

    async def get_home_pairing_state(self, home_adapter_id):
        '''
        Get the current home pairing state
        '''
        return await self._access.get('home/pairing/{0}'.format(home_adapter_id))

    async def next_home_pairing_step(self, home_adapter_id, next_pairing_step_payload):
        '''
        Next home pairing step
        '''
        return await self._access.post('home/pairing/{0}'.format(home_adapter_id), next_pairing_step_payload)

    async def start_home_pairing_step(self, home_adapter_id, start_pairing_step_payload):
        '''
        Start home pairing step
        '''
        return await self._access.post('home/pairing/{0}'.format(home_adapter_id), start_pairing_step_payload)

    async def stop_home_pairing_step(self, home_adapter_id, stop_pairing_step_payload):
        '''
        Stop home pairing
        '''
        return await self._access.post('home/pairing/{0}'.format(home_adapter_id), stop_pairing_step_payload)
