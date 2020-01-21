from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access


class Notifications:
    """
    Notifications
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    os_type = ["android", "ios"]
    subscription = ["security", "wan", "downloader", "phone"]
    notification_target_data_schema = {
        "id": "",
        "name": "",
        "subscriptions": subscription,
        "token": "",
        "type": os_type[0],
    }

    async def create_notification_target(
        self, notification_target_data: Dict[str, Any]
    ):
        """
        Create notification target

        notification_target_data : `dict`
        """
        return await self._access.post("notif/targets/", notification_target_data)

    async def delete_notification_target(self, target_id: str) -> None:
        """
        Delete notification target

        target_id : `str`
        """
        await self._access.delete(f"notif/targets/{target_id}")

    async def edit_notification_target(
        self, target_id: str, notification_target_data: Dict[str, Any]
    ):
        """
        Edit notification target

        target_id : `str`
        notification_target_data : `dict`
        """
        return await self._access.put(
            f"notif/targets/{target_id}", notification_target_data
        )

    async def get_notification_target(self, target_id: str) -> Optional[Dict[str, Any]]:
        """
        Get notification target

        target_id : `str`
        """
        return await self._access.get(f"notif/targets/{target_id}")

    async def get_notification_targets(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get notification targets

        """
        return await self._access.get(f"notif/targets/")
