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
        'mediaType': media_type[1],
        'password': '',
        'position': int
    }

    airmedia_configuration_schema = {
        'enabled': True
    }

    async def get_airmedia_configuration(self):
        '''
        Get airmedia configuration
        '''
        return await self._access.get('airmedia/config/')

    async def get_airmedia_receivers(self):
        '''
        Get airmedia receivers
        '''
        return await self._access.get('airmedia/receivers/')

    async def send_airmedia(self, receiver_name, airmedia_data=airmedia_data_schema):
        '''
        Send airmedia
        '''
        await self._access.post('airmedia/receivers/{receiver_name}/', airmedia_data)

    async def update_airmedia_configuration(self, airmedia_configuration=airmedia_configuration_schema):
        '''
        Update airmedia configuration
        '''
        return await self._access.put('airmedia/config/', airmedia_configuration)
