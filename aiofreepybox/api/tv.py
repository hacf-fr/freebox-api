class Tv:

    def __init__(self, access):
        self._access = access

    async def get_FinishedTvRecords(self):
        '''
        Get Finished Tv Records
        '''
        return await self._access.get('pvr/finished/')

    async def get_TvBouquetChannels(self, bouquetId):
        '''
        Get Tv Bouquet Channels
        '''
        return await self._access.get('tv/bouquets/{0}/channels/'.format(bouquetId))

    async def get_TvBouquet(self):
        '''
        Get Tv Bouquet 
        '''
        return await self._access.get('tv/bouquets/')

    async def get_TvChannels(self):
        '''
        Get Tv Channels
        '''
        return await self._access.get('tv/channels/')

    async def get_TvDefaultBouquetChannels(self):
        '''
        Get Tv Default Bouquet Channels
        '''
        return await self._access.get('tv/bouquets/freeboxtv/channels/')

    async def get_TvProgram(self, programId):
        '''
        Get Tv Program
        '''
        return await self._access.get('tv/epg/programs/', programId)

    async def get_TvProgramHighlights(self, channelId, date):
        '''
        Get Tv Program Highlights
        '''
        return await self._access.get('tv/epg/highlights/{0}/'.format(channelId), date)

    async def get_TvProgramsByChannel(self, channelId, date):
        '''
        Get Tv Programs By Channel
        '''
        return await self._access.get('tv/epg/by_channel/{0}/'.format(channelId), date)

    async def get_TvProgramsByDate(self, date):
        '''
        Get Tv Programs By Date
        '''
        return await self._access.get('tv/epg/by_time/', date)

    async def create_TvRecord(self, tVRecord):
        '''
        Create Tv Record
        '''
        return await self._access.post('pvr/', 'programmed/', tVRecord)

    async def create_TvRecordGenerator(self, tVRecordGenerator):
        '''
        Create Tv Record Generator
        '''
        return await self._access.post('pvr/', 'generator/', tVRecordGenerator)

    async def edit_TvRecordGenerator(self, generatorId, tVRecordGenerator):
        '''
        Edit Tv Record Generator
        '''
        return await self._access.put('pvr/generator/', generatorId, tVRecordGenerator)

    async def get_TvRecordGenerator(self, generatorId):
        '''
        Get Tv Record Generator
        '''
        return await self._access.get('pvr/generator/', generatorId)

    async def get_TvRecordsConfiguration(self):
        '''
        Get Tv Records Configuration
        '''
        return await self._access.get('pvr/config/')

    async def get_TvRecordsMediaList(self):
        '''
        Get Tv Records Media List
        '''
        return await self._access.get('pvr/media/')

    async def get_TvStatus(self):
        '''
        Get Tv Status
        '''
        return await self._access.get('tv/status/')
