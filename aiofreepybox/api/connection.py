class Connection:
    """
    Connection
    """

    def __init__(self, access):
        self._access = access

    async def lte_switch(self, enabled=None):
        """
        Lte switch

        enabled : `bool` , optional
            , Default to None

        Returns `None` or enabled : `bool`
        """

        if enabled is not None:
            lte_config = dict
            lte_config["enabled"] = enabled
            await self.set_lte_config(lte_config)

        config = await self.get_lte_config()
        if config["enabled"] is enabled or enabled is None:
            return config["enabled"]
        else:
            return None

    async def get_config(self):
        """
        Get connection configuration
        """
        return await self._access.get("connection/config/")

    async def get_connection_logs(self):
        """
        Get connection logs
        """
        return await self._access.get("connection/logs/")

    async def get_ftth(self):
        """
        Get ftth infos
        """
        return await self._access.get("connection/ftth/")

    async def get_lte_config(self):
        """
        Get lte connection configuration
        """
        return await self._access.get("connection/lte/config/")

    async def get_status(self):
        """
        Get connection status
        """
        return await self._access.get("connection/")

    async def get_xdsl(self):
        """
        Get xdsl infos
        """
        return await self._access.get("connection/xdsl/")

    async def remove_connection_logs(self):
        """
        Remove connection logs
        """
        return await self._access.delete("connection/logs/")

    async def set_config(self, connection_configuration):
        """
        Update connection configuration

        connection_configuration : `dict`
        """
        await self._access.put("connection/config/", connection_configuration)

    async def set_lte_config(self, lte_configuration_data):
        """
        Set lte connection configuration

        lte_configuration_data : `dict`
        """
        await self._access.put("connection/lte/config/", lte_configuration_data)
