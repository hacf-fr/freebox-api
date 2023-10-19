"""
UPnP AV API.
https://dev.freebox.fr/sdk/os/upnpav/
"""
from freebox_api.access import Access


class Upnpav:
    """
    UPnP AV
    """

    def __init__(self, access: Access):
        self._access = access

    async def get_configuration(self):
        """
        Get upnpav configuration
        """
        return await self._access.get("upnpav/config/")

    async def set_configuration(self, configuration):
        """
        Set upnpav configuration
        """
        return await self._access.put("upnpav/config/", configuration)
