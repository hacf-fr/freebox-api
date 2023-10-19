"""
Notification API.
No public documentation available yet.
"""
from typing import Dict

from freebox_api.access import Access


class Notifications:
    """
    Notification
    """

    def __init__(self, access: Access):
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
        self, notification_target_data=notification_target_data_schema
    ):
        """
        Create notification target
        """
        return await self._access.post("notif/targets/", notification_target_data)

    async def delete_notification_target(self, target_id: str) -> Dict[str, bool]:
        """
        Delete notification target
        """
        return await self._access.delete(f"notif/targets/{target_id}")  # type: ignore

    async def edit_notification_target(self, target_id, notification_target_data):
        """
        Edit notification target
        """
        return await self._access.put(
            f"notif/targets/{target_id}", notification_target_data
        )

    async def get_notification_target(self, target_id):
        """
        Get notification target
        """
        return await self._access.get(f"notif/targets/{target_id}")
