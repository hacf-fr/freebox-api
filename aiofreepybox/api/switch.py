from aiofreepybox.access import Access
from typing import Any, Dict, List, Optional


class Switch:
    """
    Switch
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    switch_duplex = ["auto", "full", "half"]
    switch_port_configuration_schema = {"duplex": switch_duplex[0], "speed": ""}

    async def get_status(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get Switch status
        """
        return await self._access.get("switch/status/")

    async def get_port_conf(self, port_id: int) -> Optional[Dict[str, Any]]:
        """
        Get port_id Port configuration

        port_id : `int`
        """
        return await self._access.get(f"switch/port/{port_id}")

    async def set_port_conf(self, port_id: int, switch_port_configuration: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update port_id Port configuration with conf dictionary

        port_id : `int`
        switch_port_configuration : `dict`
        """
        return await self._access.put(f"switch/port/{port_id}", switch_port_configuration)

    async def get_port_stats(self, port_id: int) -> Optional[Dict[str, int]]:
        """
        Get port_id Port stats

        port_id : `int`
        """
        return await self._access.get(f"switch/port/{port_id}/stats")
