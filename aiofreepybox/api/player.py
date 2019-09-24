class Player:

    def __init__(self, access):
        self._access = access

    player_volume_data_schema = {
        'mute': bool(),
        'volume': int
    }

    player_url_data_schema = {
        'url': str()
    }

    media_control_seek_args = {
        'seekPosition': int,
        'type': 'seek_position'
    }

    media_control_stream = {
        'quality': str(),
        'source': str()
    }

    media_control_stream_args = {
        'stream': media_control_stream,
        'type': 'stream'
    }

    media_control_track_args = {
        'trackId': int,
        'type': 'track_id'
    }

    media_control_command = [
        'play',
        'pause',
        'play_pause',
        'stop',
        'next',
        'prev',
        'seek_forward',
        'seek_backward',
        'seek_to',
        'repeat_all',
        'repeat_one',
        'repeat_off',
        'repeat_toggle',
        'shuffle_on',
        'shuffle_off',
        'shuffle_toggle',
        'record',
        'record_stop',
        'select_audio_track',
        'select_srt_track',
        'select_stream'
    ]

    media_control_data_schema = {
        'args': media_control_stream_args,
        'cmd': media_control_command[0]
    }

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

    async def set_player_volume(self, player_id, player_volume_data=player_volume_data_schema, api_version='v6'):
        '''
        Set player volume
        '''
        await self._access.put('player/{0}/api/{1}/control/volume'.format(player_id, api_version), player_volume_data)

    async def open_player_url(self, player_id, player_url_data=player_url_data_schema, api_version='v6'):
        '''
        Open player url
        '''
        await self._access.post('player/{0}/api/{1}/control/open'.format(player_id, api_version), player_url_data)

    async def send_media_control(self, player_id, media_control_data=media_control_data_schema, api_version='v6'):
        '''
        Send media control
        '''
        await self._access.post('player/{0}/api/{1}/control/mediactrl'.format(player_id, api_version), media_control_data)
