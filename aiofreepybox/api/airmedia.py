from typing import Any, Dict, List, Mapping, Optional

from aiofreepybox.access import Access


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

    async def get_airmedia_configuration(self) -> Optional[Dict[str, bool]]:
        """
        Get airmedia configuration
        """
        return await self._access.get("airmedia/config/")

    async def get_airmedia_receivers(self) -> Optional[List[Dict[str, Any]]]:
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
    ) -> Optional[Dict[str, Any]]:
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
        else:
            airmedia_config: Dict[str, Any] = {}
            if airmedia_enabled is not None:
                airmedia_config.update({"enabled": airmedia_enabled})
            if airmedia_password is not None:
                airmedia_config.update({"password": airmedia_password})
        return await self.set_airmedia_configuration(airmedia_config)

    async def airmedia_switch(self, enabled: Optional[bool] = None) -> Optional[bool]:
        """
        Airmedia switch

        airmedia_enabled : `bool`, optional
            , Default to None
        """

        if enabled is None:
            config = await self.get_airmedia_configuration()
            if config is not None:
                return config["enabled"]
        else:
            config = {"enabled": enabled}
            apply = await self.set_airmedia_configuration(config)
            if apply is not None:
                return apply["enabled"]
        return None
