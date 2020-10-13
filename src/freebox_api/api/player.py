from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from freebox_api.access import Access

_DEFAULT_PLAYER_API_VERSION = "v6"


class Player:
    """
    Player
    """

    def __init__(
        self, access: Access, player_api_version: Optional[str] = None
    ) -> None:
        self._access = access
        self._player_api_version = (
            _DEFAULT_PLAYER_API_VERSION
            if not player_api_version
            else player_api_version
        )

    media_control_seek_args = {"seek_position": 0, "type": "seek_position"}
    media_control_stream = {"quality": "", "source": ""}
    media_control_stream_args = {"stream": media_control_stream, "type": "stream"}
    media_control_track_args = {"track_id": 0, "type": "track_id"}
    media_control_command = {
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
    }
    media_control_data_schema = {"args": media_control_stream_args, "cmd": "pause"}

    async def get_players(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get players
        """
        return await self._access.get("player")

    async def _get_default_player_id(self) -> int:
        """
        Get default player id
        """

        players = await self.get_players()
        return players[0]["id"]

    async def get_player_status(
        self, player_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get player status

        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_default_player_id()

        return await self._access.get(
            f"player/{player_id}/api/{self._player_api_version}/status/"
        )

    async def get_player_volume(
        self, player_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get player volume

        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_default_player_id()

        return await self._access.get(
            f"player/{player_id}/api/{self._player_api_version}/control/volume"
        )

    async def set_player_volume(
        self, player_volume_data: Dict[str, Any], player_id: Optional[int] = None
    ) -> None:
        """
        Set player volume

        player_volume_data : `dict`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_default_player_id()

        await self._access.put(
            f"player/{player_id}/api/{self._player_api_version}/control/volume",
            player_volume_data,
        )

    async def update_player_volume(
        self,
        volume: Optional[int] = None,
        mute: Optional[bool] = None,
        player_id: Optional[int] = None,
    ) -> None:
        """
        Update player volume

        volume : `int`, optional
            , Default to `None`
        mute : `bool`, optional
            , Default to `None`
        player_id : `int` , optional
            , Default to `None`
        """

        player_data: Dict[str, Any] = {}
        if volume is not None:
            player_data.update({"volume": volume})
        if mute is not None:
            player_data.update({"mute": mute})
        await self.set_player_volume(player_data, player_id)

    async def send_media_control(
        self, media_control_data: Dict[str, str], player_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send media control

        media_control_data : `dict`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_default_player_id()

        return await self._access.post(
            f"player/{player_id}/api/{self._player_api_version}/control/mediactrl",
            media_control_data,
        )

    async def execute_media_control_command(
        self, command: str, player_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute media control command

        media_control_data : `dict`
        player_id : `int` , optional
            , Default to `None`
        """
        return await self.send_media_control({"name": command}, player_id)

    async def set_media_url(
        self, media_url_data: Dict[str, str], player_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Set media url and open it

        media_url_data : `dict`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_default_player_id()

        return await self._access.post(
            f"player/{player_id}/api/{self._player_api_version}/control/open",
            media_url_data,
        )

    async def open_media_url(
        self, media_url: str, player_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Open player url

        media_url : `str`
        player_id : `int` , optional
            , Default to `None`
        """
        return await self.set_media_url({"url": media_url}, player_id)
