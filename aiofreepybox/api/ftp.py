from typing import Any, Dict, Optional

from aiofreepybox.access import Access


class Ftp:
    """
    Ftp
    """

    def __init__(self, access: Access):
        self._access = access

    ftp_configuration_schema = {
        "enabled": False,
        "allow_anonymous": False,
        "allow_anonymous_write": False,
        "allow_remote_access": False,
        "remote_domain": "",
        "password": "",
        "port_ctrl": 12345,
        "port_data": 45678,
    }

    async def get_ftp_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get ftp configuration
        """
        return await self._access.get("ftp/config/")

    async def set_ftp_configuration(self, ftp_configuration: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Set ftp configuration
        """
        return await self._access.put("ftp/config/", ftp_configuration)

    async def ftp_switch(self, enabled: Optional[bool] = None) -> Optional[bool]:
        """
        Ftp server switch

        enabled : `bool` , optional
            , Default to None

        Returns `None` or enabled : `bool`
        """

        if enabled is not None:
            ftp_config = {"enabled": enabled}
            config = await self.set_ftp_configuration(ftp_config)
        else:
            config = await self.get_ftp_configuration()

        if config["enabled"] is enabled or enabled is None:
            return config["enabled"]
        else:
            return None
