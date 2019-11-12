from aiofreepybox.access import Access
from typing import Any, Dict, List, Mapping, Optional


class Airmedia:
    """
    Airmedia
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    action = ["start", "stop"]

    media_type = ["photo", "video"]

    airmedia_data_schema = {
        "action": action[0],
        "media": "",
        "media_type": media_type[1],
        "password": "",
        "position": 0,
    }

    async def get_airmedia_configuration(self) -> Dict[str, bool]:
        """
        Get airmedia configuration
        """
        return await self._access.get("airmedia/config/")

    async def get_airmedia_receivers(self) -> List[Dict[str, Any]]:
        """
        Get airmedia receivers
        """
        return await self._access.get("airmedia/receivers/")

    async def send_airmedia(
        self, receiver_name: str, airmedia_data: Dict[str, Any]
    ) -> None:
        """
        Send airmedia

        receiver_name : `str`
        airmedia_data : `dict`
        """
        await self._access.post(f"airmedia/receivers/{receiver_name}/", airmedia_data)

    async def set_airmedia_configuration(
        self, airmedia_configuration_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set airmedia configuration

        airmedia_configuration_data : `dict`
        """
        return await self._access.put("airmedia/config/", airmedia_configuration_data)

    async def update_airmedia_configuration(
        self,
        airmedia_enabled: Optional[bool] = None,
        airmedia_password: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Update airmedia configuration

        airmedia_enabled : `bool`, optional
            , Default to None
        airmedia_password : `str`, optional
            , Default to None
        """

        if airmedia_enabled is None and airmedia_password is None:
            return None
        airmedia_c_enabled: Mapping[str, bool] = (
            {"enabled": airmedia_enabled} if isinstance(airmedia_enabled, bool) else {}
        )
        airmedia_config: Dict[str, Any] = (
            {**airmedia_c_enabled, "password": airmedia_password}
            if isinstance(airmedia_password, str)
            else {**airmedia_c_enabled}
        )

        return await self.set_airmedia_configuration(airmedia_config)

    async def airmedia_switch(self, enabled: Optional[bool] = None) -> bool:
        """
        Airmedia switch

        airmedia_enabled : `bool`, optional
            , Default to None
        """

        if enabled is None:
            return (await self.get_airmedia_configuration())["enabled"]
        airmedia_config = {"enabled": enabled}
        return (await self.set_airmedia_configuration(airmedia_config))["enabled"]
