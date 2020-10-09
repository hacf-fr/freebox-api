class Switch:
    def __init__(self, access):
        self._access = access

    switch_duplex = ["auto", "full", "half"]

    switch_port_configuration_schema = {"duplex": switch_duplex[0], "speed": ""}

    async def get_status(self):
        """
        Get Switch status
        """
        return await self._access.get("switch/status/")

    async def get_port_conf(self, port_id):
        """
        Get port_id Port configuration
        """
        return await self._access.get(f"switch/port/{port_id}")

    async def set_port_conf(
        self, port_id, switch_port_configuration=switch_port_configuration_schema
    ):
        """
        Update port_id Port configuration with conf dictionary
        """
        await self._access.put(f"switch/port/{port_id}", switch_port_configuration)

    async def get_port_stats(self, port_id):
        """
        Get port_id Port stats
        """
        return await self._access.get(f"switch/port/{port_id}/stats")
