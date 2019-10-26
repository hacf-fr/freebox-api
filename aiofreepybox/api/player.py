_DEFAULT_PLAYER_API_VERSION = "v6"


class Player:
    """
    Player
    """

    def __init__(self, access, player_api_version=None):
        self._access = access
        self._player_api_version = (
            _DEFAULT_PLAYER_API_VERSION
            if player_api_version is None
            else player_api_version
        )

    media_control_seek_args = {"seek_position": 0, "type": "seek_position"}

    media_control_stream = {"quality": "", "source": ""}

    media_control_stream_args = {"stream": media_control_stream, "type": "stream"}

    media_control_track_args = {"track_id": 0, "type": "track_id"}

    media_control_command = [
        "play",
        "pause",
        "play_pause",
        "stop",
        "next",
        "prev",
        "seek_forward",
        "seek_backward",
        "seek_to",
        "repeat_all",
        "repeat_one",
        "repeat_off",
        "repeat_toggle",
        "shuffle_on",
        "shuffle_off",
        "shuffle_toggle",
        "record",
        "record_stop",
        "select_audio_track",
        "select_srt_track",
        "select_stream",
    ]

    media_control_data_schema = {
        "args": media_control_stream_args,
        "cmd": media_control_command[0],
    }

    async def get_player_status(self, player_id):
        """
        Get player status

        player_id : `int`
        """
        return await self._access.get(
            f"player/{player_id}/api/{self._player_api_version}/status/"
        )

    async def get_player_volume(self, player_id):
        """
        Get player volume

        player_id : `int`
        """
        return await self._access.get(
            f"player/{player_id}/api/{self._player_api_version}/control/volume"
        )

    async def get_players(self):
        """
        Get players
        """
        return await self._access.get("player")

    async def open_player_url(self, player_id, player_url_data=None):
        """
        Open player url

        player_id : `int`
        player_url_data : `str` or `dict`
            , Default to `None`
        """

        if player_url_data is None:
            return
        player_url_data_schema = dict
        if type(player_url_data) == type({}):
            player_url_data_schema = player_url_data
        else:
if isinstance(player_url_data, str):
    player_url_data = { "url": player_url_data }        

        await self._access.post(
            f"player/{player_id}/api/{self._player_api_version}/control/open",
            player_url_data_schema,
        )

    async def send_media_control(self, player_id, media_control_data):
        """
        Send media control

        player_id : `int`
        media_control_data : `dict`
        """
        await self._access.post(
            f"player/{player_id}/api/{self._player_api_version}/control/mediactrl",
            media_control_data,
        )

    async def set_player_volume(self, player_id, mute=None, volume=None):
        """
        Set player volume

        player_id : `int`
        mute : `bool`, optional
            , Default to `None`
        volume : `int`, optional
            , Default to `None`
        """

        player_volume_data = dict
        if mute is None and volume is None:
            return
        elif mute is not None:
            player_volume_data["mute"] = mute
        if volume is not None:
            player_volume_data["volume"] = volume

        await self._access.put(
            f"player/{player_id}/api/{self._player_api_version}/control/volume",
            player_volume_data,
        )

    async def update_player_volume(self, player_id, player_volume_data):
        """
        Update player volume

        player_id : `int`
        player_volume_data : `dict`
        """
        await self._access.put(
            f"player/{player_id}/api/{self._player_api_version}/control/volume",
            player_volume_data,
        )
