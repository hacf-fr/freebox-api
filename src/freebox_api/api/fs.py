"""
File System API.
https://dev.freebox.fr/sdk/os/fs/
"""
import base64
import logging
import os
from typing import Dict

import freebox_api.exceptions
from freebox_api.access import Access

logger = logging.getLogger(__name__)


class Fs:
    """
    File System
    """

    def __init__(self, access: Access):
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

    def pwd(self):
        """
        Returns the working directory
        """
        return self._path

    async def cd(self, path):
        """
        Changes the current directory
        """
        if await self._path_exists(path):
            self._path = os.path.join(self._path, path)
        else:
            logger.error(
                "{} path does not exist".format(os.path.join(self._path, path))
            )

    async def _path_exists(self, path):
        """
        Returns True if the path exists
        """
        try:
            await self.get_file_info(os.path.join(self._path, path))
            return True
        except freebox_api.exceptions.HttpRequestError:
            logger.debug(
                "{} path does not exist".format(os.path.join(self._path, path))
            )
            return False

    async def archive_files(self, archive):
        """
        Archive files
        """
        return await self._access.post("fs/archive/", archive)

    async def cp(self, copy):
        """
        Copy files
        """
        return await self._access.post("fs/copy/", copy)

    async def delete_file_task(self, task_id: int) -> Dict[str, bool]:
        """
        Delete file task
        """
        return await self._access.delete(f"fs/tasks/{task_id}")  # type: ignore

    async def extract_archive(self, extract):
        """
        Extract archive
        """
        return await self._access.post("fs/extract/", extract)

    async def get_file_info(self, path):
        """
        Returns information for the given path
        """
        path_b64 = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        return await self._access.get(f"fs/ls/{path_b64}")

    async def get_hash(self, hash_id):
        """
        Get the hash value

        To get the hash,
        the task must have succeeded and also to be in the state "done".

        hash_id : `int`
        """
        return await self._access.get(f"fs/tasks/{hash_id}/hash")

    async def get_tasks_list(self):
        """
        Returns the collection of all tasks
        """
        return await self._access.get("fs/tasks/")

    async def hash_file(self, src, hash_type):
        """
        Hash a file

        src : `str`
            The file with its path
        hash_type : `str`
            The type of hash (md5, sha1, ...)
        """
        self.hash_file_schema["src"] = base64.b64encode(src.encode("utf-8")).decode(
            "utf-8"
        )
        self.hash_file_schema["hash_type"] = hash_type
        return await self._access.post("fs/hash/", self.hash_file_schema)

    async def list_files(self, path, remove_hidden=0, count_sub_folder=0):
        """
        Returns the list of files for the given path
        """
        path_b64 = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        return await self._access.get(
            (
                f"fs/ls/{path_b64}?removeHidden={1 if remove_hidden else 0}"
                f"&countSubFolder={1 if count_sub_folder else 0}"
            )
        )

    async def ls(self):
        """
        List directory
        """
        return [i["name"] for i in await self.list_files(self._path)]

    async def mkdir(self, create_directory=create_directory_schema):
        """
        Create directory
        """
        return await self._access.post("fs/mkdir/", create_directory)

    async def mkpath(self, path):
        """
        Create path

        path : `str`
            The path to create
        """
        self.create_path_schema["path"] = base64.b64encode(path.encode("utf-8")).decode(
            "utf-8"
        )
        return await self._access.post("fs/mkpath/", self.create_path_schema)

    async def mv(self, move):
        """
        Move files
        """
        return await self._access.post("fs/mv/", move)

    async def rename_file(self, src, dst):
        """
        Rename file

        src : `str`
            The file with its path
        dst : `str`
            The new file name
        """
        self.rename_schema["src"] = base64.b64encode(src.encode("utf-8")).decode(
            "utf-8"
        )
        self.rename_schema["dst"] = dst
        return await self._access.post("fs/rename/", self.rename_schema)

    async def rm(self, remove):
        """
        Delete files
        """
        return await self._access.post("fs/rm/", remove)

    async def set_file_task_state(self, task_id, update_task_state):
        """
        Set file task state
        """
        return await self._access.put(f"fs/tasks/{task_id}", update_task_state)
