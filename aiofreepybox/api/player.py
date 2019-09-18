class Player:

    def __init__(self, access):
        self._access = access

    async def get_players(self):
        '''
        Get players
        '''
        return await self._access.get('player')

    async def get_player_status(self, player_id):
        '''
        Get player status
        '''
        return await self._access.get('player/{0}/api/v6/status/'.format(player_id))

    async def get_player_volume(self, player_id):
        '''
        Get player volume
        '''
        return await self._access.get('player/{0}/api/v6/volume/'.format(player_id))

    async def set_player_volume(self, player_id, player_volume_data):
        '''
        Set player volume
        '''
        await self._access.put('player/{0}/api/v6/control/volume'.format(player_id), player_volume_data)

    async def open_player_url(self, player_id, player_url_data):
        '''
        Open player url
        '''
        return await self._access.post('player/{0}/api/v6/control/open'.format(player_id), player_url_data)

    async def send_media_control(self, player_id, media_control_data):
        '''
        Send media control
        '''
        return await self._access.post('player/{0}/api/v6/control/mediactrl'.format(player_id), media_control_data)
