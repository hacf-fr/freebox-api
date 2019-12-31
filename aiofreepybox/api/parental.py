from aiofreepybox.access import Access
from typing import Any, Dict, List, Optional


class Parental:
    """
    Parental
    """

    def __init__(self, access: Access):
        self._access = access

    # valid values are: allowed, denied or webonly
    default_filter_mode = "allowed"
    parental_control_configuration_schema = {"default_filter_mode": default_filter_mode}
    parental_filter_schema = {
        "desc": "",
        "forced": False,
        "forced_mode": "denied",
        "macs": [""],
        "tmp_mode": "allowed",
        "tmp_mode_expire": 0,
    }

    async def create_parental_filter(
        self, parental_filter: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create parental filter

        parental_filter : `dict`
        """
        return await self._access.post("parental/filter/", parental_filter)

    async def delete_parental_filter(self, filter_id: int) -> None:
        """
        Delete parental filter

        filter_id : `int`
        """
        await self._access.delete(f"parental/filter/{filter_id}")

    async def edit_parental_filter(
        self, filter_id: int, parental_filter: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit parental filter

        filter_id : `int`
        parental_filter : `dict`
        """
        return await self._access.put(f"parental/filter/{filter_id}", parental_filter)

    async def edit_parental_filter_planning(
        self, filter_id: int, parental_filter_planning: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit parental filter planning

        filter_id : `int`
        parental_filter_planning : `dict`
        """
        return await self._access.put(
            f"parental/filter/{filter_id}/planning/", parental_filter_planning
        )

    async def get_parental_config(self) -> Optional[Dict[str, str]]:
        """
        Get parental config
        """
        return await self._access.get("parental/config/")

    async def get_parental_filter(
        self, filter_id: int
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get parental filters
        """
        return await self._access.get("parental/filter/{filter_id}")

    async def get_parental_filter_planning(
        self, filter_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get parental filter planning

        filter_id : `int`
        """
        return await self._access.get(f"parental/filter/{filter_id}/planning/")

    async def get_parental_filters(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get parental filters
        """
        return await self._access.get("parental/filter/")

    async def set_parental_control_configuration(
        self, parental_c_c: Dict[str, str]
    ) -> Optional[Dict[str, str]]:
        """
        Set parental control configuration

        parental_c_c : `dict`
        """
        return await self._access.put("parental/config/", parental_c_c)
