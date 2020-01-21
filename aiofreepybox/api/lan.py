from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access

_DEFAULT_INTERFACE = "pub"


class Lan:
    """
    Lan
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    host_type = [
        "workstation",
        "laptop",
        "smartphone",
        "tablet",
        "printer",
        "vg_console",
        "television",
        "nas",
        "ip_camera",
        "ip_phone",
        "freebox_player",
        "freebox_hd",
        "freebox_delta",
        "networking_device",
        "multimedia_device",
        "freebox_mini",
        "other",
    ]
    lan_host_data_schema = {"id": "", "primary_name": "", "host_type": host_type[0]}
    wol_schema = {"mac": "", "password": ""}

    async def delete_lan_host(
        self, host_id: int, interface: str = _DEFAULT_INTERFACE
    ) -> None:
        """
        Delete lan host

        host_id : `int`
        interface : `str` , optional
            , Default to _DEFAULT_INTERFACE
        """
        await self._access.delete(f"lan/browser/{interface}/{host_id}/")

    async def get_config(self) -> Optional[Dict[str, str]]:
        """
        Get Lan configuration
        """
        return await self._access.get("lan/config/")

    async def set_config(self, conf: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Update Lan config with conf dictionary

        conf : `dict`
        """
        return await self._access.put("lan/config/", conf)

    async def get_interfaces(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get browsable Lan interfaces
        """
        return await self._access.get("lan/browser/interfaces")

    async def get_hosts_list(
        self, interface: str = _DEFAULT_INTERFACE
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get the list of hosts on a given interface

        interface : `str` , optional
            , Default to _DEFAULT_INTERFACE
        """
        return await self._access.get(f"lan/browser/{interface}")

    async def get_host_information(
        self, host_id: int, interface: str = _DEFAULT_INTERFACE
    ) -> Optional[Dict[str, Any]]:
        """
        Get specific host informations on a given interface

        host_id : `int`
        interface : `str` , optional
            , Default to _DEFAULT_INTERFACE
        """
        return await self._access.get(f"lan/browser/{interface}/{host_id}")

    async def set_host_information(
        self,
        host_id: int,
        lan_host_data: Dict[str, Any],
        interface: str = _DEFAULT_INTERFACE,
    ) -> Optional[Dict[str, Any]]:
        """
        Update specific host informations on a given interface

        host_id : `int`
        lan_host_data : `dict`
        interface : `str` , optional
            , Default to _DEFAULT_INTERFACE
        """
        return await self._access.put(
            f"lan/browser/{interface}/{host_id}", lan_host_data
        )

    async def wake_lan_host(
        self, wol: Dict[str, str], interface: str = _DEFAULT_INTERFACE
    ):
        """
        Wake lan host

        wol : `dict`
        interface : `str` , optional
            , Default to _DEFAULT_INTERFACE
        """
        return await self._access.post(f"lan/wol/{interface}/", wol)
