import base64
from typing import Any, Dict, List, Optional

from freebox_api.access import Access


class Downloads:
    """
    Downloads
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    download_advanced_schema = {
        "download_url_list": [""],
        "username": "",
        "password": "",
        "recursive": False,
        "download_dir": "",
    }
    download_url_schema = {"download_url": ""}
    download_blacklist_data_schema = {"host": "", "expire": 0}
    rss_feed_data_schema = {"url": ""}
    new_download_tracker_data_schema = {"announce": ""}
    download_file_priority = ["no_dl", "low", "normal", "high"]
    download_file_status = ["queued", "error", "done", "downloading"]
    download_ratio_schema = {"ratio": 0}
    download_state = [
        "stopped",
        "queued",
        "starting",
        "downloading",
        "stopping",
        "error",
        "done",
        "checking",
        "repairing",
        "extracting",
        "seeding",
        "retry",
    ]
    download_state_schema = {"status": download_state[0]}
    mark_item_as_read_schema = {"isRead": True}

    async def add_download_advanced(self, download_advanced: Dict[str, Any]) -> None:
        """
        Add download advanced

        download_advanced : `dict`
        """
        await self._access.post("downloads/add/", download_advanced)

    async def add_download_from_file(self, download_file: Dict[str, Any]) -> None:
        """
        Add download from file

        download_file : `dict`
        """
        await self._access.post("downloads/add/", download_file)

    async def add_download_from_url(self, download_url: Dict[str, Any]) -> None:
        """
        Add download from url

        download_url : `dict`
        """
        await self._access.post("downloads/add/", download_url)

    async def create_download_blacklist_entry(
        self, download_blacklist_data: Dict[str, Any]
    ) -> None:
        """
        Create download blacklist entry

        download_blacklist_data : `dict`
        """
        await self._access.post("downloads/blacklist/", download_blacklist_data)

    async def create_download_feed(
        self, rss_feed_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create download feed

        rss_feed_data : `dict`
        """
        return await self._access.post("downloads/feeds/", rss_feed_data)

    async def create_download_tracker(
        self, download_id: int, new_download_tracker_data: Dict[str, Any]
    ) -> None:
        """
        Create download tracker

        download_id : `int`
        new_download_tracker_data : `dict`
        """
        await self._access.post(
            f"downloads/{download_id}/trackers/", new_download_tracker_data
        )

    async def delete_download(self, download_id: int) -> None:
        """
        Delete download

        download_id : `int`
        """
        await self._access.delete(f"downloads/{download_id}")

    async def delete_download_blacklist_entry(self, host: str) -> None:
        """
        Delete download blacklist entry

        host : `str`
        """
        await self._access.delete(f"downloads/blacklist/{host}")

    async def delete_download_erase_files(self, download_id: int) -> None:
        """
        Delete download erase files

        download_id : `int`
        """
        await self._access.delete(f"downloads/{download_id}/erase/")

    async def delete_download_feed(self, feed_id: int) -> None:
        """
        Delete download feed

        feed_id : `int`
        """
        await self._access.delete(f"downloads/feeds/{feed_id}/")

    async def download_feed_item(self, feed_id: int, item_id: int) -> None:
        """
        Download feed item

        feed_id : `int`
        item_id : `int`
        """
        await self._access.post(f"downloads/feeds/{feed_id}/items/{item_id}/download/")

    async def download_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Download file

        file_path : `str`
        """
        path_b64 = base64.b64encode(file_path.encode("utf-8")).decode("utf-8")
        return await self._access.get(f"dl/{path_b64}")

    async def edit_download_file(
        self, download_id: int, file_id: int, download_file_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit download file

        download_id : `int`
        file_id : `int`
        download_file_data : `dict`
        """
        return await self._access.put(
            f"downloads/{download_id}/files/{file_id}", download_file_data
        )

    async def edit_download_ratio(
        self, download_id: int, download_ratio: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit download ratio

        download_id : `int`
        download_ratio : `dict`
        """
        return await self._access.put(f"downloads/{download_id}", download_ratio)

    async def edit_download_state(
        self, download_id: int, download_state_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit download state

        download_id : `int`
        download_state_data : `dict`
        """
        return await self._access.put(f"downloads/{download_id}", download_state_data)

    async def edit_download_tracker(
        self, download_id: int, tracker_url: str, download_tracker_data: Dict[str, Any]
    ) -> None:
        """
        Edit download tracker

        download_id : `int`
        tracker_url : `str`
        download_tracker_data : `dict`
        """
        await self._access.put(
            f"downloads/{download_id}/trackers/{tracker_url}", download_tracker_data
        )

    async def empty_download_blacklist(self, download_id: int) -> None:
        """
        Empty download blacklist

        download_id : `int`
        """
        await self._access.delete(f"downloads/{download_id}/blacklist/empty/")

    async def fetch_download_feed(self, feed_id: int) -> None:
        """
        Fetch download feed

        feed_id : `int`
        """
        await self._access.post(f"downloads/feeds/{feed_id}/fetch/")

    async def get_download(self, download_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}")

    async def get_download_blacklist(
        self, download_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get download blacklist

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/blacklist/")

    async def get_download_feed_items(self, feed_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download feed items

        feed_id : `int`
        """
        return await self._access.get(f"downloads/feeds/{feed_id}/items/")

    async def get_download_feeds(self, feed_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download feeds

        feed_id : `int`
        """
        return await self._access.get("downloads/feeds/")

    async def get_download_files(self, download_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download files

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/files/")

    async def get_download_log(self, download_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download log

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/log/")

    async def get_download_peers(self, download_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download peers

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/peers/")

    async def get_download_trackers(self, download_id: int) -> Optional[Dict[str, Any]]:
        """
        Get download trackers

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/trackers/")

    async def get_downloads(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get downloads
        """
        return await self._access.get("downloads/")

    async def get_downloads_configuration(
        self, download_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get downloads configuration

        download_id : `int`
        """
        return await self._access.get("downloads/config/")

    async def mark_download_feed_as_read(self, feed_id: int) -> None:
        """
        Mark download feed as read

        feed_id : `int`
        """
        await self._access.post(f"downloads/feeds/{feed_id}/mark_all_as_read/")

    async def mark_download_item_as_read(
        self, feed_id: int, item_id: int, mark_item_as_read: Dict[str, Any] = None
    ) -> None:
        """
        Mark download feed item as read

        feed_id : `int`
        item_id : `int`
        mark_item_as_read : `dict`
        """
        if mark_item_as_read is None:
            mark_item_as_read = self.mark_item_as_read_schema
        await self._access.post(
            f"downloads/feeds/{feed_id}/items/{item_id}", mark_item_as_read
        )

    async def remove_download_tracker(
        self, download_id: int, tracker_url: str, download_tracker: Dict[str, Any]
    ) -> None:
        """
        Remove download tracker

        download_id : `int`
        tracker_url : `str`
        download_tracker : `dict`
        """
        await self._access.delete(
            f"downloads/{download_id}/trackers/{tracker_url}", download_tracker
        )

    async def set_downloads_configuration(
        self, downloads_configuration: Dict[str, Any]
    ):
        """
        Set downloads configuration

        downloads_configuration : `dict`
        """
        return await self._access.put("downloads/config/", downloads_configuration)
