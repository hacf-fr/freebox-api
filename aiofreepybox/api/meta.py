class Meta:

    def __init__(self, access):
        self._access = access

    async def get_catchup_channel(self, channel_id):
        """
        Get catchup channel

        channel_id : `int`
        """
        return await self._access.get(f'meta/static/catchup/channels/{channel_id}')

    async def get_catchup_group(self, channel_id, group_id):
        """
        Get catchup group

        channel_id : `int`
        group_id : `int`
        """
        return await self._access.get(f'meta/static/catchup/channels/{channel_id}/groups/{group_id}')

    async def get_catchup_group_programs(self, channel_id, group_id, catchup_program_filter):
        """
        Get catchup group programs

        channel_id : `int`
        group_id : `int`
        catchup_program_filter : `dict`
        """
        return await self._access.get(f'meta/static/catchup/channels/{channel_id}/groups/{group_id}/programs?limit=20', catchup_program_filter)

    async def get_catchup_highlight_headings(self):
        """
        Get catchup highlight headings
        """
        return await self._access.get('meta/static/catchup/highlight_headings')

    async def get_catchup_highlights(self, heading_id):
        """
        Get catchup highlights

        heading_id : `int`
        """
        return await self._access.get(f'meta/static/catchup/highlights/{heading_id}')

    async def get_catchup_home_highlight_headings(self):
        """
        Get catchup home highlight headings
        """
        return await self._access.get('meta/static/catchup/highlight_home')

    async def get_catchup_program(self, channel_id, program_id):
        """
        Get catchup program

        channel_id : `int`
        program_id : `int`
        """
        return await self._access.get(f'meta/static/catchup/channels/{channel_id}/programs/{program_id}')

    async def get_catchup_programs(self, channel_id, catchup_program_filter):
        """
        Get catchup programs

        channel_id : `int`
        catchup_program_filter : `dict`
        """
        return await self._access.get(f'meta/static/catchup/channels/{channel_id}/programs?limit=20', catchup_program_filter)

    async def get_catchup_top_programs(self, channel_id, catchup_program_filter):
        """
        Get catchup top program

        channel_id : `int`
        catchup_program_filter : `dict`
        """
        return await self._access.get(f'meta/static/catchup/channels/{channel_id}/top', catchup_program_filter)

    async def get_meta_diffusions(self, diffusions_filter):
        """
        Get meta diffusions

        diffusions_filter : `dict`
        """
        return await self._access.get('meta/static/epg/diffusions?limit=20&join_emission=1', diffusions_filter)

    async def get_meta_emission_casting(self, emission_id):
        """
        Get meta emission casting

        emission_id : `int`
        """
        return await self._access.get(f'meta/static/plurimedia/emissions/{emission_id}/casting')

    async def get_meta_emission_collections(self, filter_emission_id):
        """
        Get meta emission collections

        filter_emission_id : `int`
        """
        query = {
            'filter_emission_id': filter_emission_id
        }
        return await self._access.get('meta/static/plurimedia/collections?limit=20', query)

    async def get_meta_emission_diffusions(self, filter_emission_id):
        """
        Get meta emission diffusions

        filter_emission_id : `int`
        """
        query = {
            'filter_emission_id': filter_emission_id
        }
        return await self._access.get('meta/static/epg/diffusions?limit=20', query)

    async def get_meta_emission_vod_entries(self, filter_plurimedia_emission_id):
        """
        Get meta emission vod entries

        filter_plurimedia_emission_id : `int`
        """
        query = {
            'filter_plurimedia_emission_id': filter_plurimedia_emission_id
        }
        return await self._access.get('meta/static/vod/catalog/entries?limit=20', query)

    async def get_meta_emissions(self, emissions_filter):
        """
        Get meta emissions

        emissions_filter : `dict`
        """
        return await self._access.get('meta/static/plurimedia/emissions?limit=20', emissions_filter)

    async def get_meta_epg_highlights(self):
        """
        Get meta epg highlights
        """
        return await self._access.get('meta/static/epg/homev7')

    async def get_meta_format(self, format_id):
        """
        Get meta format

        format_id : `int`
        """
        return await self._access.get(f'meta/static/plurimedia/formats/{format_id}')

    async def get_meta_formats(self):
        """
        Get meta formats
        """
        return await self._access.get('meta/static/plurimedia/formats')

    async def get_meta_genre(self, genre_id):
        """
        Get meta genre

        genre_id : `int`
        """
        return await self._access.get(f'meta/static/plurimedia/genres/{genre_id}')

    async def get_meta_tv_channel(self, channel_uuid):
        """
        Get meta tv channel

        channel_uuid : `str`
        """
        return await self._access.get(f'meta/static/tv/channels_by_uuid/{channel_uuid}')

    async def get_meta_tv_channels(self, channel_filter):
        """
        Get meta tv channels

        channel_filter : `dict`
        """
        return await self._access.get(f'meta/static/tv/channels/', channel_filter)

    async def get_meta_vod_entry_links(self, vod_entry_id, model):
        """
        Get meta vod entry links

        vod_entry_id : `int`
        model : `str`
        """
        query = {
            'model': model
        }
        return await self._access.get(f'meta/static/vod/catalog/entries/{vod_entry_id}/links', query)

    async def get_meta_vod_services(self):
        """
        Get meta vod services
        """
        return await self._access.get('meta/static/vod/services?join_app=1')

    async def search_catchup(self, search_catchup_query):
        """
        Search catchup

        search_catchup_query : `str`
        """
        query = {
            'query': search_catchup_query
        }
        return await self._access.get('meta/search/catchup', query)

    async def search_meta_emissions(self, search_emissions_query, search_emission_filter=None):
        """
        Search meta emissions

        search_emissions_query : `str`
        search_emission_filter : `dict`, optional
            , by default None
        """
        query = {
            'query': search_emissions_query
        }
        if search_emission_filter is not None:
            query.update(search_emission_filter)
        return await self._access.get('meta/search/plurimedia/emissions?limit=20', query)

    async def search_meta_tv_channel(self, search_tv_channel_query):
        """
        Search meta tv channel

        search_tv_channel_query : `str`
        """
        query = {
            'query': search_tv_channel_query
        }
        return await self._access.get('meta/search/tv_channels', query)
