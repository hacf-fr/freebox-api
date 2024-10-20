"""
Download API.
https://dev.freebox.fr/sdk/os/download/
"""

import base64
from typing import Any
from typing import Dict
from typing import Optional

from freebox_api.access import Access


class Download:
    """
    Download
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    download_url_schema = {
        "download_url": "",
        "download_url_list": "",  # items separated by /n
        "username": "",
        "password": "",
        "recursive": False,
        "download_dir": "",
    }
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
    download_update_schema = {
        "io_priority": "",
        "status": download_state[0],
    }
    mark_item_as_read_schema = {"is_read": True}

    async def get_download_tasks(self) -> Dict[str, Any]:
        """
        Get downloads
        """
        return await self._access.get("downloads/")  # type: ignore

    async def get_download_task(self, download_id: int) -> Dict[str, Any]:
        """
        Get download

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}")  # type: ignore

    async def delete_download_task(self, download_id: int) -> None:
        """
        Delete download

        download_id : `int`
        """
        await self._access.delete(f"downloads/{download_id}")

    async def delete_download_task_files(self, download_id: int) -> None:
        """
        Delete download files

        download_id : `int`
        """
        await self._access.delete(f"downloads/{download_id}/erase/")

    async def update_download_task(
        self, download_id: int, download_update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update download

        download_id : `int`
        download_update_data : `dict`
        """
        return await self._access.put(f"downloads/{download_id}", download_update_data)

    async def get_download_log(self, download_id: int) -> Dict[str, Any]:
        """
        Get download log

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/log/")  # type: ignore

    async def add_download_task_from_url(
        self, download_url: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add download from url

        download_url : `str`
        """
        return await self._access.post("downloads/add/", download_url)

    async def add_download_task_from_file(
        self, download_file: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add download from file

        download_file : `dict`
        """
        return await self._access.post("downloads/add/", download_file)

    # Download Stats

    async def get_download_stats(self) -> Dict[str, Any]:
        """
        Get download stats
        """
        return await self._access.get("downloads/stats/")  # type: ignore

    # Download Files

    async def get_download_files(self, download_id: int) -> Dict[str, Any]:
        """
        Get download files

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/files/")  # type: ignore

    async def update_download_file(
        self, download_id: int, file_id: int, download_file_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update download file

        download_id : `int`
        file_id : `int`
        download_file_data : `dict`
        """
        return await self._access.put(
            f"downloads/{download_id}/files/{file_id}", download_file_data
        )

    # Download Trackers [UNSTABLE]

    async def get_download_trackers(self, download_id: int) -> Dict[str, Any]:
        """
        Get download trackers

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/trackers/")  # type: ignore

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

    async def update_download_tracker(
        self, download_id: int, tracker_url: str, download_tracker_data: Dict[str, Any]
    ) -> None:
        """
        Update download tracker

        download_id : `int`
        tracker_url : `str`
        download_tracker_data : `dict`
        """
        await self._access.put(
            f"downloads/{download_id}/trackers/{tracker_url}", download_tracker_data
        )

    # Download Peers [UNSTABLE]

    async def get_download_peers(self, download_id: int) -> Dict[str, Any]:
        """
        Get download peers

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/peers/")  # type: ignore

    # Download Pieces

    async def get_download_pieces(self, download_id: int) -> Dict[str, Any]:
        """
        Get download pieces

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/pieces/")  # type: ignore

    # Download Blacklist [UNSTABLE]

    async def get_download_blacklist(self, download_id: int) -> Dict[str, Any]:
        """
        Get download blacklist

        download_id : `int`
        """
        return await self._access.get(f"downloads/{download_id}/blacklist/")  # type: ignore

    async def empty_download_blacklist(self, download_id: int) -> None:
        """
        Empty download blacklist

        download_id : `int`
        """
        await self._access.delete(f"downloads/{download_id}/blacklist/empty/")

    async def delete_download_blacklist_entry(self, host: str) -> None:
        """
        Delete download blacklist entry

        host : `str`
        """
        await self._access.delete(f"downloads/blacklist/{host}")

    async def create_download_blacklist_entry(
        self, download_blacklist_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create download blacklist entry

        download_blacklist_data : `dict`
        """
        return await self._access.post("downloads/blacklist/", download_blacklist_data)

    # Download Feeds
    # https://dev.freebox.fr/sdk/os/download_feeds/

    async def get_download_feeds(self) -> Dict[str, Any]:
        """
        Get download feeds
        """
        return await self._access.get("downloads/feeds/")  # type: ignore

    async def get_download_feed(self, feed_id: int) -> Dict[str, Any]:
        """
        Get download feed

        feed_id : `int`
        """
        return await self._access.get(f"downloads/feeds/{feed_id}/")  # type: ignore

    async def create_download_feed(self, rss_url: str) -> Dict[str, Any]:
        """
        Create download feed

        rss_feed_data : `dict`
        """
        return await self._access.post("downloads/feeds/", {"url": rss_url})

    async def delete_download_feed(self, feed_id: int) -> None:
        """
        Delete download feed

        feed_id : `int`
        """
        await self._access.delete(f"downloads/feeds/{feed_id}/")

    async def update_download_feed(
        self, feed_id: int, auto_download: bool
    ) -> Dict[str, Any]:
        """
        Update download feed

        feed_id : `int`
        auto_download : `bool`
        """
        return await self._access.post(
            f"downloads/feeds/{feed_id}/", {"auto_download": auto_download}
        )

    async def fetch_download_feed(self, feed_id: int) -> None:
        """
        Fetch download feed

        feed_id : `int`
        """
        await self._access.post(f"downloads/feeds/{feed_id}/fetch/")

    async def fetch_all_download_feed(self) -> None:
        """
        Fetch all download feed
        """
        await self._access.post("downloads/feeds/fetch/")

    async def get_download_feed_items(self, feed_id: int) -> Dict[str, Any]:
        """
        Get download feed items

        feed_id : `int`
        """
        return await self._access.get(f"downloads/feeds/{feed_id}/items/")  # type: ignore

    async def mark_download_item_as_read(
        self,
        feed_id: int,
        item_id: int,
        mark_item_as_read: Optional[Dict[str, Any]] = None,
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

    async def download_feed_item(self, feed_id: int, item_id: int) -> None:
        """
        Download feed item

        feed_id : `int`
        item_id : `int`
        """
        await self._access.post(f"downloads/feeds/{feed_id}/items/{item_id}/download/")

    async def mark_download_feed_as_read(self, feed_id: int) -> None:
        """
        Mark download feed as read

        feed_id : `int`
        """
        await self._access.post(f"downloads/feeds/{feed_id}/mark_all_as_read/")

    # Download Configuration
    # https://dev.freebox.fr/sdk/os/download_config/

    async def get_downloads_configuration(self) -> Dict[str, Any]:
        """
        Get downloads configuration
        """
        return await self._access.get("downloads/config/")  # type: ignore

    async def set_downloads_configuration(
        self, downloads_configuration: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set downloads configuration

        downloads_configuration : `dict`
        """
        return await self._access.put("downloads/config/", downloads_configuration)

    # Undocumented
    # TODO: working APIs ?

    async def download_file(self, file_path: str) -> Dict[str, Any]:
        """
        Download file

        file_path : `str`
        """
        path_b64 = base64.b64encode(file_path.encode("utf-8")).decode("utf-8")
        return await self._access.get(f"dl/{path_b64}")  # type: ignore
