class Tv:

    def __init__(self, access):
        self._access = access

    async def get_finished_tv_records(self):
        '''
        Get finished tv records
        '''
        return await self._access.get('pvr/finished/')

    async def get_tv_bouquet_channels(self, bouquetid):
        '''
        Get tv bouquet channels
        '''
        return await self._access.get('tv/bouquets/{0}/channels/'.format(bouquetid))

    async def get_tv_bouquet(self):
        '''
        Get tv bouquet 
        '''
        return await self._access.get('tv/bouquets/')

    async def get_tv_channels(self):
        '''
        Get tv channels
        '''
        return await self._access.get('tv/channels/')

    async def get_tv_default_bouquet_channels(self):
        '''
        Get tv default bouquet channels
        '''
        return await self._access.get('tv/bouquets/freeboxtv/channels/')

    async def get_tv_program(self, programid):
        '''
        Get tv program
        '''
        return await self._access.get('tv/epg/programs/', programid)

    async def get_tv_program_highlights(self, channelid, date):
        '''
        Get tv program highlights
        '''
        return await self._access.get('tv/epg/highlights/{0}/'.format(channelid), date)

    async def get_tv_programs_by_channel(self, channelid, date):
        '''
        Get tv programs by channel
        '''
        return await self._access.get('tv/epg/by_channel/{0}/'.format(channelid), date)

    async def get_tv_programs_by_date(self, date):
        '''
        Get tv programs by date
        '''
        return await self._access.get('tv/epg/by_time/', date)

    async def create_tv_record(self, tvrecord):
        '''
        Create tv record
        '''
        return await self._access.post('pvr/', 'programmed/', tvrecord)

    async def create_tv_record_generator(self, tvrecordgenerator):
        '''
        Create tv record generator
        '''
        return await self._access.post('pvr/', 'generator/', tvrecordgenerator)

    async def edit_tv_record_generator(self, generatorid, tvrecordgenerator):
        '''
        Edit tv record generator
        '''
        return await self._access.put('pvr/generator/', generatorid, tvrecordgenerator)

    async def get_tv_record_generator(self, generatorid):
        '''
        Get tv record generator
        '''
        return await self._access.get('pvr/generator/', generatorid)

    async def get_tv_records_configuration(self):
        '''
        Get tv records configuration
        '''
        return await self._access.get('pvr/config/')

    async def get_tvrecords_media_list(self):
        '''
        Get tv records media list
        '''
        return await self._access.get('pvr/media/')

    async def get_tv_status(self):
        '''
        Get tv status
        '''
        return await self._access.get('tv/status/')
