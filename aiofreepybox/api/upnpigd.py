from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access


class Upnpigd:
    """
    Upnpigd
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    async def delete_redir(self, redir_id: int):
        """
        Deletes the given upnpigd redirection

        redir_id : `int`
        """
        return await self._access.delete(f"upnpigd/redir/{redir_id}")

    async def get_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get the upnpigd configuration
        """
        return await self._access.get("upnpigd/config/")

    async def get_redirs(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get the list of upnpigd redirections
        """
        return await self._access.get("upnpigd/redir/")

    async def update_configuration(
        self, upnpigd_config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update the upnpigd configuration

        upnpigd_config : `dict`
        """
        return await self._access.put("upnpigd/config/", upnpigd_config)
