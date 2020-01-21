from typing import Dict, Optional

from aiofreepybox.access import Access


class Upnpav:
    """
    Upnpav
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    async def get_configuration(self) -> Optional[Dict[str, bool]]:
        """
        Get upnpav configuration
        """
        return await self._access.get("upnpav/config/")

    async def set_configuration(
        self, configuration: Dict[str, bool]
    ) -> Optional[Dict[str, bool]]:
        """
        Set upnpav configuration

        configuration : `dict`
        """
        return await self._access.put("upnpav/config/", configuration)
