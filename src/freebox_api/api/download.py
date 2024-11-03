"""
Download API.
https://dev.freebox.fr/sdk/os/download/
"""

import base64

import sys

if sys.version_info < (3, 12):
    from typing_extensions import Required
else:
    from typing import Required
from typing import Any, TypedDict, Union, List
from typing import Dict
from typing import Optional

from freebox_api.access import Access


class _DownloadAddURL(TypedDict, total=False):
    """
    Add download by URL parameters data structure.

    https://dev.freebox.fr/sdk/os/download/#adding-by-url

    download_url : `str` – The URL
    download_url_list : `str` – A list of URL separated by a new line delimiter
    (use download_url or download_url_list)
    download_dir : `str` – The download destination directory
    (optional: will use the configuration download_dir by default)
    recursive : `bool` – If true the download will be recursive
    username : `str` – Auth username (optional)
    password : `str` – Auth password (optional)
    archive_password : `str` – The password required to extract downloaded content
    (only relevant for nzb)
    cookies : `str` – The http cookies (to be able to pass session cookies along with url)
    """

    download_dir: str
    recursive: bool
    username: str
    password: str
    archive_password: str
    cookies: str


class DownloadAddURL(_DownloadAddURL):
    """Add download by URL parameters data structure."""

    download_url: Required[str]


class DownloadAddURLList(_DownloadAddURL):
    """Add download by URL list parameters data structure."""

    download_url_list: Required[str]


class DownloadAddFile(TypedDict, total=False):
    """
    Add download by file upload parameters data structure.

    https://dev.freebox.fr/sdk/os/download/#adding-by-file-upload

    download_file : `str` – The download file (must be uploaded using multipart/form-data
    download_dir : `str` – The download destination directory
    (optional: will use the configuration download_dir by default)
    archive_password : `str` – The password required to extract downloaded content
    (only relevant for nzb)
    """

    download_file: Required[str]
    download_dir: str
    archive_password: str


class Download:
    """
    Download
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    download_url_schema: DownloadAddURL = {
        "download_url": "",
        "username": "",
        "password": "",
        "recursive": False,
        "download_dir": "",
    }
    download_url_list_schema: DownloadAddURLList = {
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

    async def add_download_task(
        self,
        download_params: Union[DownloadAddURL, DownloadAddURLList, DownloadAddFile],
    ) -> Dict[str, Any]:
        """
        Add download from params

        download_params : `dict`
        """
        return await self._access.post("downloads/add/", download_params)

    async def add_download_task_from_url(
        self,
        download_url: str,
        download_dir: Optional[str] = None,
        archive_password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add download from url

        download_url : `str`
        download_dir : `str`, optional
            Default to None
        archive_password : `str`, optional
            Default to None
        """
        download_params: DownloadAddURL = {
            "download_url": download_url,
        }
        if download_dir:
            download_params["download_dir"] = download_dir
        if archive_password:
            download_params["archive_password"] = archive_password
        return await self.add_download_task(download_params)

    async def add_download_task_from_urls(
        self,
        download_urls: List[str],
        download_dir: Optional[str] = None,
        archive_password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add download from url

        download_urls : `list[str]`
        download_dir : `str`, optional
            Default to None
        archive_password : `str`, optional
            Default to None
        """
        download_params: DownloadAddURLList = {
            "download_url_list": "/n".join(download_urls),
        }
        if download_dir:
            download_params["download_dir"] = download_dir
        if archive_password:
            download_params["archive_password"] = archive_password
        return await self.add_download_task(download_params)

    async def add_download_task_from_file(
        self,
        download_file: str,
        download_dir: Optional[str] = None,
        archive_password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add download from file

        download_file : `str`
        download_dir : `str`, optional
            Default to None
        archive_password : `str`, optional
            Default to None
        """
        download_params: DownloadAddFile = {
            "download_file": download_file,
        }
        if download_dir:
            download_params["download_dir"] = download_dir
        if archive_password:
            download_params["archive_password"] = archive_password
        return await self.add_download_task(download_params)

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
