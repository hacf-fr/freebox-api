from aiofreepybox.access import Access
from typing import Any, Dict, List, Optional


class Storage:
    """
    Storage
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    async def check_partition(self, id: int):
        """
        Check partition

        id : `int`
        """
        return await self._access.put(f"storage/partition/{id}/check")

    async def eject_disk(
        self, disk_id: int, eject_data: Optional[Dict[str, str]] = None
    ):
        """
        Eject storage disk

        disk_id : `int`
        eject_data : `dict`
        """
        if eject_data is None:
            eject_data = {"state": "disabled"}
        return await self._access.put(f"storage/disk/{disk_id}", eject_data)

    async def format_partition(self, id: int, format_data: Dict[str, str]):
        """
        Format partition

        id : `int`
        format_data : `dict`
        """
        return await self._access.put(f"storage/partition/{id}/format", format_data)

    async def get_config(self) -> Optional[Dict[str, Any]]:
        """
        Get storage configuration
        """
        return await self._access.get("storage/config/")

    async def get_disk(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Get disk

        id : `int`
        """
        return await self._access.get(f"storage/disk/{id}")

    async def get_disks(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get disks list
        """
        return await self._access.get("storage/disk/")

    async def get_partition(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Get partition

        id : `int`
        """
        return await self._access.get(f"storage/partition/{id}")

    async def get_partitions(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get partitions list
        """
        return await self._access.get("storage/partition/")

    async def get_raid(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Get raid

        id : `int`
        """
        return await self._access.get(f"storage/raid/{id}")

    async def get_raids(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get raids list
        """
        return await self._access.get("storage/raid/")
