class Airmedia:

    def __init__(self, access):
        self._access = access

    action = [
        'start',
        'stop'
    ]

    media_type = [
        'photo',
        'video'
    ]

    airmedia_data_schema = {
        'action': action[0],
        'media': '',
        'media_type': media_type[1],
        'password': '',
        'position': 0
    }

    airmedia_configuration_schema = {
        'enabled': True
    }

    async def get_airmedia_configuration(self):
        """
        Get airmedia configuration
        """
        return await self._access.get('airmedia/config/')

    async def get_airmedia_receivers(self):
        """
        Get airmedia receivers
        """
        return await self._access.get('airmedia/receivers/')

    async def send_airmedia(self, receiver_name, airmedia_data):
        """
        Send airmedia

        receiver_name : `str`
        airmedia_data : `dict`
        """
        await self._access.post('airmedia/receivers/{receiver_name}/', airmedia_data)

    async def update_airmedia_configuration(self, airmedia_enabled):
        """
        Update airmedia configuration

        airmedia_enabled : `bool`
        """
        airmedia_configuration_data = self.airmedia_configuration_schema
        airmedia_configuration_data['enabled'] = airmedia_enabled
        return await self._access.put('airmedia/config/', airmedia_configuration_data)
