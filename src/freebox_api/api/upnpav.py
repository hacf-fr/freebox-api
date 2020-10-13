class Upnpav:
    def __init__(self, access):
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
