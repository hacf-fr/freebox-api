class Fw:
    def __init__(self, access):
        self._access = access

    ip_proto = ["tcp", "udp"]

    port_forwarding_config_schema = {
        "comment": "",
        "enabled": True,
        "ip_proto": ip_proto[0],
        "lan_ip": "",
        "lan_port": 0,
        "src_ip": "",
        "wan_port_end": 0,
        "wan_port_start": 0,
    }

    incoming_port_configuration_data_schema = {"enabled": True, "in_port": 0}

    dmz_configuration_schema = {"enabled": False, "ip": ""}

    async def create_port_forwarding_configuration(self, port_forwarding_config):
        """
        Create port forwarding configuration

        port_forwarding_config : `dict`
        """
        return await self._access.post("fw/redir/", port_forwarding_config)

    async def delete_port_forwarding_configuration(self, config_id):
        """
        Delete port forwarding configuration

        config_id : `int`
        """
        await self._access.delete(f"fw/redir/{config_id}")

    async def edit_incoming_port_configuration(
        self, port_id, incoming_port_configuration_data
    ):
        """
        Edit incoming port configuration

        port_id : `int`
        incoming_port_configuration_data : `dict`
        """
        return await self._access.put(
            f"fw/incoming/{port_id}", incoming_port_configuration_data
        )

    async def get_dmz_configuration(self):
        """
        Get dmz configuration
        """
        return await self._access.get("fw/dmz/")

    async def get_incoming_ports_configuration(self):
        """
        Get incoming ports configuration
        """
        return await self._access.get("fw/incoming/")

    async def get_port_forwarding_configuration(self):
        """
        Get port forwarding configuration
        """
        return await self._access.get("fw/redir/")

    async def set_dmz_configuration(self, dmz_configuration=None):
        """
        Set dmz configuration

        dmz_configuration : `dict`
        """
        if dmz_configuration is None:
            dmz_configuration = self.dmz_configuration_schema
        return await self._access.put("fw/dmz/", dmz_configuration)
