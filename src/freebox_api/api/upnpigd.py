"""
UPnP IGD API.
https://dev.freebox.fr/sdk/os/igd/
"""
from typing import Dict

from freebox_api.access import Access


class Upnpigd:
    """
    UPnP IGD
    """

    def __init__(self, access: Access):
        self._access = access

    async def delete_redir(self, id: str) -> Dict[str, bool]:
        """
        Deletes the given upnpigd redirection
        """
        return await self._access.delete(f"upnpigd/redir/{id}")  # type: ignore

    async def get_configuration(self):
        """
        Get the upnpigd configuration
        """
        return await self._access.get("upnpigd/config/")

    async def get_redirs(self):
        """
        Get the list of upnpigd redirections
        """
        return await self._access.get("upnpigd/redir/")

    async def update_configuration(self, upnpigd_config):
        """
        Update the upnpigd configuration
        """
        return await self._access.put("upnpigd/config/", upnpigd_config)
