"""
Storage API [UNSTABLE].
https://dev.freebox.fr/sdk/os/storage/
"""
from freebox_api.access import Access


class Storage:
    """
    Storage
    """

    def __init__(self, access: Access):
        self._access = access

    eject_schema = {"state": "disabled"}

    async def check_partition(self, id):
        """
        Check partition

        id : `int`
        """
        return await self._access.put(f"storage/partition/{id}/check")

    async def eject_disk(self, disk_id, eject_data=None):
        """
        Eject storage disk

        disk_id : `int`
        eject_data : `dict`
        """
        if eject_data is None:
            eject_data = self.eject_schema
        return await self._access.put(f"storage/disk/{disk_id}", eject_data)

    async def format_partition(self, id, format_data):
        """
        Format partition

        id : `int`
        format_data : `dict`
        """
        return await self._access.put(f"storage/partition/{id}/format", format_data)

    async def get_config(self):
        """
        Get storage configuration
        """
        return await self._access.get("storage/config/")

    async def get_disk(self, id):
        """
        Get disk

        id : `int`
        """
        return await self._access.get(f"storage/disk/{id}")

    async def get_disks(self):
        """
        Get disks list
        """
        return await self._access.get("storage/disk/")

    async def get_partition(self, id):
        """
        Get partition

        id : `int`
        """
        return await self._access.get(f"storage/partition/{id}")

    async def get_partitions(self):
        """
        Get partitions list
        """
        return await self._access.get("storage/partition/")

    async def get_raid(self, id):
        """
        Get raid

        id : `int`
        """
        return await self._access.get(f"storage/raid/{id}")

    async def get_raids(self):
        """
        Get raids list
        """
        return await self._access.get("storage/raid/")
