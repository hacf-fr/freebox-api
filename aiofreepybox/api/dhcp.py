import logging
from aiofreepybox.access import Access
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class Dhcp:
    """
    Dhcp
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    static_lease_schema = {"ip": "", "mac": "", "comment": ""}
    dhcp_configuration_schema = {
        "always_broadcast": True,
        "dns": [""],
        "enabled": True,
        "ip_range_start": "",
        "ip_range_end": "",
        "sticky_assign": True,
    }
    dhcp_v6_configuration_data_schema = {
        "dns": [""],
        "enabled": True,
        "use_custom_dns": False,
    }

    async def create_dhcp_static_lease(self, static_lease: Dict[str, Any]):
        """
        Create dhcp static lease

        static_lease : `dict`
        """
        return await self._access.post("dhcp/static_lease/", static_lease)

    async def delete_dhcp_static_lease(self, lease_id: int) -> None:
        """
        Delete dhcp static lease

        lease_id : `int`
        """
        await self._access.delete(f"dhcp/static_lease/{lease_id}")

    async def edit_dhcp_static_lease(self, lease_id: int, static_lease: Dict[str, Any]):
        """
        Edit dhcp static lease

        lease_id : `int`
        static_lease : `dict`
        """
        return await self._access.put(f"dhcp/static_lease/{lease_id}", static_lease)

    async def get_config(self) -> Optional[Dict[str, Any]]:
        """
        Get DHCP configuration
        """
        return await self._access.get("dhcp/config/")

    async def set_config(self, dhcp_configuration: Dict[str, Any]):
        """
        Update DHCP configuration

        dhcp_configuration : `dict`
        """
        return await self._access.put("dhcp/config/", dhcp_configuration)

    async def get_v6_config(self) -> Optional[Dict[str, Any]]:
        """
        Get DHCP v6 configuration
        """
        return await self._access.get("dhcpv6/config/")

    async def set_v6_config(self, dhcp_v6_configuration_data: Dict[str, Any]):
        """
        Update DHCP v6 configuration

        dhcp_v6_configuration_data : `dict`
        """
        return await self._access.put("dhcpv6/config/", dhcp_v6_configuration_data)

    async def get_dhcp_dynamic_leases(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get the list of DHCP dynamic leases
        """
        return await self._access.get("dhcp/dynamic_lease/")

    async def get_dhcp_static_leases(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get the list of DHCP static leases
        """
        return await self._access.get("dhcp/static_lease/")

    # TODO: remove
    async def get_dynamic_dhcp_lease(self):
        """
        Get the list of DHCP dynamic leases
        """
        logger.warning(
            "Using deprecated call get_dynamic_dhcp_lease, please use get_dhcp_dynamic_leases instead"
        )
        return await self.get_dhcp_dynamic_leases()

    # TODO: remove
    async def get_static_dhcp_lease(self):
        """
        Get the list of DHCP static leases
        """
        logger.warning(
            "Using deprecated call get_static_dhcp_lease, please use get_dhcp_static_leases instead"
        )
        return await self.get_dhcp_static_leases()
