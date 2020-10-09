class Connection:
    def __init__(self, access):
        self._access = access

    lte_configuration_data_schema = {"enabled": True}

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
        """
        await self._access.put("connection/config/", connection_configuration)

    async def set_lte_config(
        self, lte_configuration_data=lte_configuration_data_schema
    ):
        """
        Update lte connection configuration
        """
        await self._access.put("connection/lte/config/", lte_configuration_data)
