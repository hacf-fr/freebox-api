import base64
import logging
import os
import aiofreepybox.exceptions


logger = logging.getLogger(__name__)


class Fs:

    def __init__(self, access):
        self._access = access
        self._path = '/'

    archive_schema = {
        'dst': '',
        'files': ['']
    }

    copy_mode = [
        'overwrite',
        'both',
        'recent',
        'skip'
    ]

    copy_schema = {
        'dst': '',
        'files': [''],
        'mode': copy_mode[0]
    }

    create_directory_schema = {
        'dirname': '',
        'parent': ''
    }

    create_path_schema = {
        'path': '',
    }

    extract_schema = {
        'src': '',
        'dst': ''
    }

    move_schema = {
        'dst': '',
        'files': [''],
        'mode': copy_mode[0]
    }

    remove_schema = {
        'files': ['']
    }

    rename_schema = {
        'src': '',
        'dst': ''
    }

    update_task_state_schema = {
        'state': ''
    }

    eject_schema = {
        'state': 'disabled'
    }

    def pwd(self):
        '''
        Returns the working directory
        '''
        return self._path

    async def cd(self, path):
        '''
        Changes the current directory
        '''
        if await self._path_exists(path):
            self._path = os.path.join(self._path, path)
        else:
            logger.error('{} does not exist'.format(os.path.join(self._path, path)))

    async def _path_exists(self, path):
        '''
        Returns True if the path exists
        '''
        try:
            await self.get_file_info(os.path.join(self._path, path))
            return True
        except aiofreepybox.exceptions.HttpRequestError:
            logger.debug('{} does not exist'.format(os.path.join(self._path, path)))
            return False

    async def ls(self):
        '''
        List directory
        '''
        return [i['name'] for i in await self.list_file(self._path)]

    async def archive_files(self, archive=archive_schema):
        '''
        Archive files
        '''
        return await self._access.post('fs/archive/', archive)

    async def cp(self, copy=copy_schema):
        '''
        Copy files
        '''
        return await self._access.post('fs/copy/', copy)

    async def mkdir(self, create_directory=create_directory_schema):
        '''
        Create directory
        '''
        return await self._access.post('fs/mkdir/', create_directory)

    async def mkpath(self, create_path=create_path_schema):
        '''
        Create path
        '''
        return await self._access.post('fs/mkpath/', create_path)

    async def delete_file_task(self, task_id):
        '''
        Delete file task
        '''
        return await self._access.delete(f'fs/tasks/{task_id}')

    async def rm(self, remove=remove_schema):
        '''
        Delete files
        '''
        return await self._access.post('fs/rm/', remove)

    async def extract_archive(self, extract=extract_schema):
        '''
        Extract archive
        '''
        return await self._access.post('fs/extract/', extract)

    async def get_tasks_list(self):
        '''
        Returns the collection of all tasks
        '''
        return await self._access.get('fs/tasks/')

    async def list_files(self, path, remove_hidden=0, count_sub_folder=0):
        '''
        Returns the list of files for the given path
        '''
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return await self._access.get(f'fs/ls/{path_b64}?removeHidden={remove_hidden}&countSubFolder={count_sub_folder}')

    async def get_file_info(self, path):
        '''
        Returns information for the given path
        '''
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return await self._access.get(f'fs/ls/{path_b64}')

    async def mv(self, move=move_schema):
        '''
        Move files
        '''
        return await self._access.post('fs/mv/', move)

    async def rename_file(self, rename=rename_schema):
        '''
        Rename file
        '''
        return await self._access.post('fs/rename/', rename)

    async def set_file_task_state(self, task_id, update_task_state=update_task_state_schema):
        '''
        Set file task state
        '''
        return await self._access.put(f'fs/tasks/{task_id}', update_task_state)

    async def eject_storage_disk(self, disk_id, eject=eject_schema):
        '''
        Eject storage disk
        '''
        return await self._access.put(f'storage/disk/{disk_id}', eject)

    async def get_storage_disks(self):
        '''
        Get storage disks
        '''
        return await self._access.get('storage/disk/')
