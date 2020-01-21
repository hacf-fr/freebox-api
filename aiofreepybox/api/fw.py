from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access


class Fw:
    """
    Fw
    """

    def __init__(self, access: Access) -> None:
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

    async def create_port_forwarding_configuration(
        self, port_forwarding_config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create port forwarding configuration

        port_forwarding_config : `dict`
        """
        return await self._access.post("fw/redir/", port_forwarding_config)

    async def delete_port_forwarding_configuration(self, config_id: int) -> None:
        """
        Delete port forwarding configuration

        config_id : `int`
        """
        await self._access.delete(f"fw/redir/{config_id}")

    async def edit_incoming_port_configuration(
        self, port_id: int, incoming_port_configuration_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit incoming port configuration

        port_id : `int`
        incoming_port_configuration_data : `dict`
        """
        return await self._access.put(
            f"fw/incoming/{port_id}", incoming_port_configuration_data
        )

    async def get_dmz_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get dmz configuration
        """
        return await self._access.get("fw/dmz/")

    async def get_incoming_ports_configuration(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get incoming ports configuration
        """
        return await self._access.get("fw/incoming/")

    async def get_port_forwarding_configuration(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get port forwarding configuration
        """
        return await self._access.get("fw/redir/")

    async def set_dmz_configuration(
        self, dmz_configuration: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Set dmz configuration

        dmz_configuration : `dict`
        """
        return await self._access.put("fw/dmz/", dmz_configuration)

    async def update_port_forwarding_configuration(
        self, port_forwarding_config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update port forwarding configuration

        port_forwarding_config : `dict`
        """
        return await self._access.put("fw/redir/", port_forwarding_config)
