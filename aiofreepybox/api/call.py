from aiofreepybox import logger


class Call:

    def __init__(self, access):
        self._access = access

    mark_call_log_as_read_data_schema = {
        'new': False
    }

    async def delete_call_log(self, log_id):
        '''
        Delete call log
        '''
        await self._access.delete(f'call/log/{log_id}')

    async def get_call_log(self):
        '''
        Get call logs
        '''
        return await self._access.get('call/log/')

# TODO: remove
    async def get_call_list(self):
        '''
        Returns the collection of all call entries
        '''
        logger.warning('Using deprecated get_call_list, please use get_call_log instead')
        return await self.get_call_log()

    async def mark_call_log_as_read(self, log_id, mark_call_log_as_read_data=mark_call_log_as_read_data_schema):
        '''
        Mark call log as read
        '''
        return await self._access.put(f'call/log/{log_id}', mark_call_log_as_read_data)
