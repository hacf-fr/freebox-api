class Player:

    def __init__(self, access):
        self._access = access
        self._api_version_target = 'v6'

    player_volume_data_schema = {
        'mute': bool(),
        'volume': int
    }

    player_url_data_schema = {
        'url': ''
    }

    media_control_seek_args = {
        'seek_position': int,
        'type': 'seek_position'
    }

    media_control_stream = {
        'quality': '',
        'source': ''
    }

    media_control_stream_args = {
        'stream': media_control_stream,
        'type': 'stream'
    }

    media_control_track_args = {
        'track_id': int,
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

    async def get_player_status(self, player_id, api_version=None):
        """
        Get player status

        player_id : `int`
        api_version : `str`, optional
            , by default `self.api_version_target`
        """
        if api_version is None:
            api_version = self.api_version_target
        return await self._access.get(f'player/{player_id}/api/{api_version}/status/')

    async def get_player_volume(self, player_id, api_version=None):
        """
        Get player volume

        player_id : `int`
        api_version : `str`, optional
            , by default `self.api_version_target`
        """
        if api_version is None:
            api_version = self.api_version_target
        return await self._access.get(f'player/{player_id}/api/{api_version}/control/volume')

    async def get_players(self):
        """
        Get players
        """
        return await self._access.get('player')

    async def open_player_url(self, player_id, player_url_data=None, api_version=None):
        """
        Open player url

        player_id : `int`
        player_url_data : `dict`, optional
            , by default `self.player_url_data_schema`
        api_version : `str`, optional
            , by default `self.api_version_target`
        """
        if player_url_data is None:
            player_url_data = self.player_url_data_schema
        if api_version is None:
            api_version = self.api_version_target
        await self._access.post(f'player/{player_id}/api/{api_version}/control/open', player_url_data)

    async def send_media_control(self, player_id, media_control_data=None, api_version=None):
        """
        Send media control

        player_id : `int`
        media_control_data : `dict`, optional
            , by default `self.media_control_data_schema`
        api_version : `str`, optional
            , by default `self.api_version_target`
        """
        if media_control_data is None:
            media_control_data = self.media_control_data_schema
        if api_version is None:
            api_version = self.api_version_target
        await self._access.post(f'player/{player_id}/api/{api_version}/control/mediactrl', media_control_data)

    async def set_player_volume(self, player_id, player_volume_data=None, api_version=None):
        """
        Set player volume

        player_id : `int`
        player_volume_data : `dict`, optional
            , by default `self.player_volume_data_schema`
        api_version : `str`, optional
            , by default `self.api_version_target`
        """
        if player_volume_data is None:
            player_volume_data = self.player_volume_data_schema
        if api_version is None:
            api_version = self.api_version_target
        await self._access.put(f'player/{player_id}/api/{api_version}/control/volume', player_volume_data)
