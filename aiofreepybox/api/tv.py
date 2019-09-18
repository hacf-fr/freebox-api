import time


class Tv:

    def __init__(self, access):
        self._access = access

    async def get_finished_tv_records(self):
        '''
        Get finished tv records:
        '''
        return await self._access.get('pvr/finished/')

    async def get_tv_bouquet_channels(self, bouquet_id='freeboxtv'):
        '''
        Get tv bouquet channels:
        '''
        return await self._access.get('tv/bouquets/{0}/channels/'.format(bouquet_id))

    async def get_tv_bouquet(self):
        '''
        Get tv bouquet:
        '''
        return await self._access.get('tv/bouquets/')

    async def get_tv_channels(self):
        '''
        Get tv channels:
        '''
        return await self._access.get('tv/channels/')

    async def get_tv_default_bouquet_channels(self):
        '''
        Get tv default bouquet channels:
        '''
        return await self.get_tv_bouquet_channels()

    async def get_tv_program(self, program_id):
        '''
        Get tv program:
        '''
        return await self._access.get('tv/epg/programs/{0}'.format(program_id))

    async def get_tv_program_highlights(self, channel_id, date=int(time.time())):
        '''
        Get tv program highlights:
        '''
        return await self._access.get('tv/epg/highlights/{0}/{1}'.format(channel_id, date))

    async def get_tv_programs_by_channel(self, channel_id, date=int(time.time())):
        '''
        Get tv programs by channel:
        '''
        return await self._access.get('tv/epg/by_channel/{0}/{1}'.format(channel_id, date))

    async def get_tv_programs_by_date(self, date=int(time.time())):
        '''
        Get tv programs by date:
        '''
        return await self._access.get('tv/epg/by_time/{0}'.format(date))

    async def create_tv_record(self, tv_record):
        '''
        Create tv record:
        '''
        return await self._access.post('pvr/programmed/', tv_record)

    async def create_tv_record_generator(self, tv_record_generator):
        '''
        Create tv record generator:
        '''
        return await self._access.post('pvr/generator/', tv_record_generator)

    async def edit_tv_record_generator(self, generator_id, tv_record_generator):
        '''
        Edit tv record generator:
        '''
        await self._access.put('pvr/generator/{0}'.format(generator_id), tv_record_generator)

    async def get_tv_record_generator(self, generator_id):
        '''
        Get tv record generator:
        '''
        return await self._access.get('pvr/generator/{0}'.format(generator_id))

    async def get_tv_records_configuration(self):
        '''
        Get tv records configuration:
        '''
        return await self._access.get('pvr/config/')

    async def get_tv_records_media_list(self):
        '''
        Get tv records media list:
        '''
        return await self._access.get('pvr/media/')

    async def get_tv_status(self):
        '''
        Get tv status:
        '''
        return await self._access.get('tv/status/')
