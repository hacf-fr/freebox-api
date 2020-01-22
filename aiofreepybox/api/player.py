from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access

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
            if player_api_version is None
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

    async def _get_d_p_id(self) -> Optional[int]:
        """
        Get default player id
        """

        player = await self.get_players()
        if player is not None:
            return player[0]["id"]
        return None

    async def get_player_status(
        self, player_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get player status

        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            return await self._access.get(
                f"player/{player_id}/api/{self._player_api_version}/status/"
            )
        return None

    async def get_player_volume(
        self, player_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get player volume

        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            return await self._access.get(
                f"player/{player_id}/api/{self._player_api_version}/control/volume"
            )
        return None

    async def get_players(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get players
        """
        return await self._access.get("player")

    async def mute_player_switch(
        self, enabled: Optional[bool] = None, player_id: Optional[int] = None
    ) -> Optional[bool]:
        """
        Mute switch

        enabled : `bool`, optional
            , Default to `None`
        player_id : `int`, optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            if enabled is not None:
                player_mute_data = {"mute": enabled}
                await self.set_player_volume(player_mute_data, player_id)
            player_mute = await self.get_player_volume(player_id)
            if player_mute is not None:
                return player_mute["mute"]
        return None

    async def open_player_url(
        self, player_url: str, player_id: Optional[int] = None
    ) -> None:
        """
        Open player url

        player_url : `str`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            player_url_data = {"url": player_url}
            await self.set_player_url(player_url_data, player_id)

    async def send_media_control(
        self, media_control_data: Dict[str, str], player_id: Optional[int] = None
    ) -> None:
        """
        Send media control

        media_control_data : `dict`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            await self._access.post(
                f"player/{player_id}/api/{self._player_api_version}/control/mediactrl",
                media_control_data,
            )

    async def set_player_url(
        self, player_url_data: Dict[str, str], player_id: Optional[int] = None
    ) -> None:
        """
        Set player url and open it

        player_url_data : `dict`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            await self._access.post(
                f"player/{player_id}/api/{self._player_api_version}/control/open",
                player_url_data,
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
            player_id = await self._get_d_p_id()
        if player_id is not None:
            await self._access.put(
                f"player/{player_id}/api/{self._player_api_version}/control/volume",
                player_volume_data,
            )

    async def update_player_volume(
        self,
        mute: Optional[bool] = None,
        volume: Optional[int] = None,
        player_id: Optional[int] = None,
    ) -> None:
        """
        Update player volume

        mute : `bool`, optional
            , Default to `None`
        volume : `int`, optional
            , Default to `None`
        player_id : `int` , optional
            , Default to `None`
        """

        if player_id is None:
            player_id = await self._get_d_p_id()
        if player_id is not None:
            player_data: Dict[str, Any] = {}
            if mute is not None:
                player_data.update({"mute": mute})
            if volume is not None:
                player_data.update({"volume": volume})
            await self.set_player_volume(player_data, player_id)
        return None
