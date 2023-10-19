"""
System API.
https://dev.freebox.fr/sdk/os/system/
"""
from freebox_api.access import Access


class System:
    """
    System
    """

    def __init__(self, access: Access):
        self._access = access

    async def get_config(self):
        """
        Get system configuration:
        """
        return await self._access.get("system/")

    async def reboot(self):
        """
        Reboot freebox
        """
        await self._access.post("system/reboot")
