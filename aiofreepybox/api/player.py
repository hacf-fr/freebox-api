class Player:

    def __init__(self, access):
        self._access = access

    async def get_players(self):
        '''
        Get players
        '''
        return await self._access.get('player')

    async def get_player_status(self, player_id, api_version='v6'):
        '''
        Get player status
        '''
        return await self._access.get('player/{0}/api/{1}/status/'.format(player_id, api_version))

    async def get_player_volume(self, player_id, api_version='v6'):
        '''
        Get player volume
        '''
        return await self._access.get('player/{0}/api/{1}/control/volume'.format(player_id, api_version))

    async def set_player_volume(self, player_id, player_volume_data, api_version='v6'):
        '''
        Set player volume
        '''
        await self._access.put('player/{0}/api/{1}/control/volume'.format(player_id, api_version), player_volume_data)

    async def open_player_url(self, player_id, player_url_data, api_version='v6'):
        '''
        Open player url
        '''
        return await self._access.post('player/{0}/api/{1}/control/open'.format(player_id, api_version), player_url_data)

    async def send_media_control(self, player_id, media_control_data, api_version='v6'):
        '''
        Send media control
        '''
        return await self._access.post('player/{0}/api/{1}/control/mediactrl'.format(player_id, api_version), media_control_data)
