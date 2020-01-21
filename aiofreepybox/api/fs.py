import base64
import logging
import os
from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access
import aiofreepybox.exceptions

_LOGGER = logging.getLogger(__name__)


class Fs:
    """
    Fs
    """

    def __init__(self, access: Access) -> None:
        self._access = access
        self._path = "/"

    archive_schema = {"dst": "", "files": [""]}
    copy_mode = ["overwrite", "both", "recent", "skip"]
    copy_schema = {"dst": "", "files": [""], "mode": copy_mode[0]}
    create_directory_schema = {"dirname": "", "parent": ""}
    create_path_schema = {"path": ""}
    extract_schema = {"src": "", "dst": ""}
    hash_file_schema = {"src": "", "hash_type": "sha1"}
    move_schema = {"dst": "", "files": [""], "mode": copy_mode[0]}
    remove_schema = {"files": [""]}
    rename_schema = {"src": "", "dst": ""}
    task_state = ["queued", "running", "paused", "done", "failed"]
    update_task_state_schema = {"state": task_state[0]}

    def pwd(self) -> str:
        """
        Returns the working directory
        """
        return self._path

    async def cd(self, path: str) -> None:
        """
        Changes the current directory

        path : `str`
        """
        if await self._path_exists(path):
            self._path = os.path.join(self._path, path)
        else:
            _LOGGER.error(
                "{} path does not exist".format(os.path.join(self._path, path))
            )

    async def _path_exists(self, path: str) -> bool:
        """
        Returns True if the path exists

        path : `str`
        """
        try:
            await self.get_file_info(os.path.join(self._path, path))
            return True
        except aiofreepybox.exceptions.HttpRequestError:
            _LOGGER.debug(
                "{} path does not exist".format(os.path.join(self._path, path))
            )
            return False

    async def archive_files(self, archive: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Archive files

        archive : `dict`
        """
        return await self._access.post("fs/archive/", archive)

    async def cp(self, copy: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Copy files

        copy : `dict`
        """
        return await self._access.post("fs/copy/", copy)

    async def delete_file_task(self, task_id: int):
        """
        Delete file task

        task_id : `int`
        """
        return await self._access.delete(f"fs/tasks/{task_id}")

    async def extract_archive(
        self, extract: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract archive

        extract : `dict`
        """
        return await self._access.post("fs/extract/", extract)

    async def get_file_info(self, path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Returns information for the given path

        path : `str`
        """
        path_b64 = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        return await self._access.get(f"fs/ls/{path_b64}")

    async def get_hash(self, hash_id: int) -> Optional[Dict[str, str]]:
        """
        Get the hash value

        To get the hash,
        the task must have succeeded and also to be in the state "done".

        hash_id : `int`
        """
        return await self._access.get(f"fs/tasks/{hash_id}/hash")

    async def get_tasks_list(self) -> Optional[List[Dict[str, Any]]]:
        """
        Returns the collection of all tasks
        """
        return await self._access.get("fs/tasks/")

    async def hash_file(self, src: str, hash_type: str) -> Optional[Dict[str, Any]]:
        """
        Hash a file

        src : `str`
            The file with its path
        hash_type : `str`
            The type of hash (md5, sha1, ...)
        """
        hash_file_schema = {
            "src": base64.b64encode(src.encode("utf-8")).decode("utf-8"),
            "hash_type": hash_type,
        }
        return await self._access.post("fs/hash/", hash_file_schema)

    async def list_files(
        self, path: str, remove_hidden: bool = False, count_sub_folder: bool = False
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Returns the list of files for the given path

        path : `str`
        remove_hidden : `bool`
        count_sub_folder : `bool`
        """
        path_b64 = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        return await self._access.get(
            f"fs/ls/{path_b64}?removeHidden={1 if remove_hidden else 0}&countSubFolder={1 if count_sub_folder else 0}"
        )

    async def ls(self) -> Optional[List[str]]:
        """
        List directory
        """
        files_l = await self.list_files(self._path)
        if files_l is not None:
            return [i["name"] for i in files_l]
        else:
            return None

    async def mkdir(self, create_directory: Dict[str, Any]):
        """
        Create directory

        create_directory : `dict`
        """
        return await self._access.post("fs/mkdir/", create_directory)

    async def mkpath(self, path: str):
        """
        Create path

        path : `str`
            The path to create
        """
        create_path_schema = {
            "path": base64.b64encode(path.encode("utf-8")).decode("utf-8")
        }
        return await self._access.post("fs/mkpath/", create_path_schema)

    async def mv(self, move: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Move files

        move : `dict`
        """
        return await self._access.post("fs/mv/", move)

    async def rename_file(self, src: str, dst: str) -> Optional[str]:
        """
        Rename file

        src : `str`
            The file with its path
        dst : `str`
            The new file name
        """
        rename_schema = {
            "src": base64.b64encode(src.encode("utf-8")).decode("utf-8"),
            "dst": dst,
        }
        return await self._access.post("fs/rename/", rename_schema)

    async def rm(self, remove: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Delete files

        remove : `dict`
        """
        return await self._access.post("fs/rm/", remove)

    async def set_file_task_state(
        self, task_id: int, update_task_state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Set file task state

        task_id : `int`
        update_task_state : `dict`
        """
        return await self._access.put(f"fs/tasks/{task_id}", update_task_state)

