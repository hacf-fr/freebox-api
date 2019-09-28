class Storage:

    def __init__(self, access):
        self._access = access

    eject_schema = {
        'state': 'disabled'
    }

    async def check_partition(self, id):
        '''
        Check partition
        '''
        return await self._access.put(f'storage/partition/{id}/check')

    async def eject_disk(self, disk_id, eject=eject_schema):
        '''
        Eject storage disk
        '''
        return await self._access.put(f'storage/disk/{disk_id}', eject)

    async def format_partition(self, id, format_data):
        '''
        Format partition
        '''
        return await self._access.put(f'storage/partition/{id}/format', format_data)

    async def get_config(self):
        '''
        Get storage configuration
        '''
        return await self._access.get('storage/config/')

    async def get_disk(self, id):
        '''
        Get disk
        '''
        return await self._access.get(f'storage/disk/{id}')

    async def get_disks(self):
        '''
        Get disks list
        '''
        return await self._access.get('storage/disk/')

    async def get_partition(self, id):
        '''
        Get partition
        '''
        return await self._access.get(f'storage/partition/{id}')

    async def get_partitions(self):
        '''
        Get partitions list
        '''
        return await self._access.get('storage/partition/')

    async def get_raid(self, id=0):
        '''
        Get raid
        '''
        return await self._access.get(f'storage/raid/{id}')

    async def get_raids(self):
        '''
        Get raids list
        '''
        return await self._access.get('storage/raid/')
