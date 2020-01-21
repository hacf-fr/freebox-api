from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access


class Phone:
    """
    Phone
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    async def dect_switch(self, enabled: Optional[bool] = None) -> Optional[bool]:
        """
        Dect switch

        enabled : `bool` , optional
            , Default to None

        Returns `None` or enabled : `bool`
        """

        if enabled is not None:
            dect_config = {"dect_enabled": enabled}
            config = await self.set_phone_config(dect_config)
        else:
            config = await self.get_phone_config()
        if config is not None:
            return config["dect_enabled"]
        else:
            return None

    async def get_dect_vendors(self) -> Optional[List[Dict[str, str]]]:
        """
        Get dect vendors
        """
        return await self._access.get("phone/dect_vendors/")

    async def get_phones(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get phones list
        """
        return await self._access.get("phone/")

    async def get_phone_config(self) -> Optional[Dict[str, Any]]:
        """
        Get phone configuration
        """
        return await self._access.get("phone/config/")

    async def set_phone_config(self, phone_entry: Dict[str, Any]):
        """
        Set phone config

        phone_entry : `dict`
        """
        return await self._access.put("phone/config/", phone_entry)

    async def start_dect_configuration(
        self,
        dect_enabled: Optional[bool] = None,
        dect_registration: Optional[bool] = None,
    ):
        """
        Start dect configuration
        To start dect configuration dect_enabled and dect_registration must be True ,
        but it can also be used to enable/disable dect with dect_enabled True/False

        dect_enabled : `bool`
        dect_registration : `bool`
        """

        dect_configuration = {}
        if dect_enabled is None and dect_registration is None:
            return await self.get_phone_config()
        elif dect_enabled is not None:
            dect_configuration["dect_enabled"] = dect_enabled
        if dect_registration is not None:
            dect_configuration["dect_registration"] = dect_registration
        return await self.set_phone_config(dect_configuration)

    async def start_dect_page(self):
        """
        Start dect paging
        """
        return await self._access.post("phone/dect_page_start/")

    async def stop_dect_page(self):
        """
        Stop dect paging
        """
        return await self._access.post("phone/dect_page_stop/")

    async def start_fxs_ring(self):
        """
        Start fxs ring
        """
        return await self._access.post("phone/fxs_ring_start/")

    async def stop_fxs_ring(self):
        """
        Stop fxs ring
        """
        return await self._access.post("phone/fxs_ring_stop/")
