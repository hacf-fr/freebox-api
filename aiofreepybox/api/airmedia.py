class Airmedia:
    """
    Airmedia
    """

    def __init__(self, access):
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

    async def get_airmedia_configuration(self):
        """
        Get airmedia configuration
        """
        return await self._access.get("airmedia/config/")

    async def get_airmedia_receivers(self):
        """
        Get airmedia receivers
        """
        return await self._access.get("airmedia/receivers/")

    async def send_airmedia(self, receiver_name, airmedia_data):
        """
        Send airmedia

        receiver_name : `str`
        airmedia_data : `dict`
        """
        await self._access.post("airmedia/receivers/{receiver_name}/", airmedia_data)

    async def set_airmedia_configuration(
        self, airmedia_enabled=None, airmedia_password=None
    ):
        """
        set airmedia configuration

        airmedia_enabled : `bool`
        airmedia_password : `str`
        """

        if airmedia_enabled is None and airmedia_password is None:
            return
        airmedia_configuration_data = {}
        if airmedia_enabled is not None:
            airmedia_configuration_data["enabled"] = airmedia_enabled
        if airmedia_password is not None:
            airmedia_configuration_data["password"] = airmedia_password
        return await self._access.put("airmedia/config/", airmedia_configuration_data)

    async def update_airmedia_configuration(self, airmedia_configuration_data):
        """
        Update airmedia configuration

        airmedia_configuration_data : `dict`
        """
        return await self._access.put("airmedia/config/", airmedia_configuration_data)
