class Lan:

    def __init__(self, access):
        self._access = access

    host_type = [
        'workstation',
        'laptop',
        'smartphone',
        'tablet',
        'printer',
        'vg_console',
        'television',
        'nas',
        'ip_camera',
        'ip_phone',
        'freebox_player',
        'freebox_hd',
        'freebox_delta',
        'networking_device',
        'multimedia_device',
        'freebox_mini',
        'other'
    ]

    lan_host_data_schema = {
        'id': '',
        'primary_name': '',
        'host_type': host_type[0]
    }

    wol_schema = {
        'mac': '',
        'password': ''
    }

    async def delete_lan_host(self, host_id, interface='pub'):
        """
        Delete lan host

        host_id : `int`
        interface : `str`
        """
        await self._access.delete(f'lan/browser/{interface}/{host_id}/')

    async def get_config(self):
        """
        Get Lan configuration
        """
        return await self._access.get('lan/config/')

    async def set_config(self, conf):
        """
        Update Lan config with conf dictionary

        conf : `dict`
        """
        return await self._access.put('lan/config/', conf)

    async def get_interfaces(self):
        """
        Get browsable Lan interfaces
        """
        return await self._access.get('lan/browser/interfaces')

    async def get_hosts_list(self, interface='pub'):
        """
        Get the list of hosts on a given interface

        interface : `str`
        """
        return await self._access.get(f'lan/browser/{interface}')

    async def get_host_information(self, host_id, interface='pub'):
        """
        Get specific host informations on a given interface

        host_id : `int`
        interface : `str`
        """
        return await self._access.get(f'lan/browser/{interface}/{host_id}')

    async def set_host_information(self, host_id, lan_host_data, interface='pub'):
        """
        Update specific host informations on a given interface

        host_id : `int`
        lan_host_data : `dict`
        interface : `str`
        """
        return await self._access.put(f'lan/browser/{interface}/{host_id}', lan_host_data)

    async def wake_lan_host(self, wol, interface='pub'):
        """
        Wake lan host

        wol : `dict`
        interface : `str`
        """
        return await self._access.post(f'lan/wol/{interface}/', wol)
