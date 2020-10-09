import time


class Tv:

    def __init__(self, access):
        self._access = access

    async def archive_tv_record(self, record_id):
        '''
        Archive tv record
        '''
        return await self._access.post(f'pvr/programmed/{record_id}/ack/')

    async def create_tv_record(self, tv_record):
        '''
        Create tv record
        '''
        return await self._access.post('pvr/programmed/', tv_record)

    async def create_tv_record_generator(self, tv_record_generator):
        '''
        Create tv record generator
        '''
        return await self._access.post('pvr/generator/', tv_record_generator)

    async def delete_finished_tv_record(self, record_id):
        '''
        Delete finished tv record
        '''
        await self._access.delete(f'pvr/finished/{record_id}')

    async def delete_programmed_tv_record(self, record_id):
        '''
        Delete programmed tv record
        '''
        await self._access.delete(f'pvr/programmed/{record_id}')

    async def delete_tv_record_generator(self, generator_id):
        '''
        Delete tv record generator
        '''
        await self._access.delete(f'pvr/generator/{generator_id}')

    async def edit_finished_tv_record(self, record_id, finished):
        '''
        Edit finished tv record
        '''
        return await self._access.put(f'pvr/finished/{record_id}', finished)

    async def edit_programmed_tv_record(self, record_id, tv_record):
        '''
        Edit programmed tv record
        '''
        return await self._access.put(f'pvr/programmed/{record_id}', tv_record)

    async def edit_tv_record_generator(self, generator_id, tv_record_generator):
        '''
        Edit tv record generator
        '''
        return await self._access.put(f'pvr/generator/{generator_id}', tv_record_generator)

    async def get_finished_tv_records(self):
        '''
        Get finished tv records
        '''
        return await self._access.get('pvr/finished/')

    async def get_mycanal_token(self):
        '''
        Get mycanal token
        '''
        return await self._access.get('tv/mycanal_token')

    async def get_programmed_tv_records(self):
        '''
        Get programmed tv records
        '''
        return await self._access.get('pvr/programmed/')

    async def get_tv_bouquet(self):
        '''
        Get tv bouquet
        '''
        return await self._access.get('tv/bouquets/')

    async def get_tv_bouquet_channels(self, bouquet_id='freeboxtv'):
        '''
        Get tv bouquet channels
        '''
        return await self._access.get(f'tv/bouquets/{bouquet_id}/channels/')

    async def get_tv_channels(self):
        '''
        Get tv channels
        '''
        return await self._access.get('tv/channels/')

    async def get_tv_default_bouquet_channels(self):
        '''
        Get tv default bouquet channels
        '''
        return await self.get_tv_bouquet_channels()

    async def get_tv_program(self, program_id):
        '''
        Get tv program
        '''
        return await self._access.get(f'tv/epg/programs/{program_id}')

    async def get_tv_program_highlights(self, channel_id, date=int(time.time())):
        '''
        Get tv program highlights
        '''
        return await self._access.get(f'tv/epg/highlights/{channel_id}/{date}')

    async def get_tv_programs_by_channel(self, channel_id, date=int(time.time())):
        '''
        Get tv programs by channel
        '''
        return await self._access.get(f'tv/epg/by_channel/{channel_id}/{date}')

    async def get_tv_programs_by_date(self, date=int(time.time())):
        '''
        Get tv programs by date
        '''
        return await self._access.get(f'tv/epg/by_time/{date}')

    async def get_tv_records_configuration(self):
        '''
        Get tv records configuration
        '''
        return await self._access.get('pvr/config/')

    async def get_tv_record_generator(self, generator_id):
        '''
        Get tv record generator
        '''
        return await self._access.get(f'pvr/generator/{generator_id}')

    async def get_tv_records_media_list(self):
        '''
        Get tv records media list
        '''
        return await self._access.get('pvr/media/')

    async def get_tv_status(self):
        '''
        Get tv status
        '''
        return await self._access.get('tv/status/')
