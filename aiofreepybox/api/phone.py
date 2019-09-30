class Phone:

    def __init__(self, access):
        self._access = access

    dect_configuration_schema = {
        'dect_enabled': True,
        'dect_registration': True
    }

    async def get_dect_vendors(self):
        '''
        Get dect vendors
        '''
        return await self._access.get('phone/dect_vendors/')

    async def get_phones(self):
        '''
        Get phones list
        '''
        return await self._access.get('phone/')

    async def get_phone_config(self):
        '''
        Get phone configuration
        '''
        return await self._access.get('phone/config/')

    async def start_dect_configuration(self, dect_configuration=dect_configuration_schema):
        '''
        Start dect configuration
        '''
        return await self._access.put('phone/config/', dect_configuration)

    async def start_dect_page(self):
        '''
        Start dect paging
        '''
        return await self._access.post('phone/dect_page_start/')

    async def stop_dect_page(self):
        '''
        Stop dect paging
        '''
        return await self._access.post('phone/dect_page_stop/')

    async def start_fxs_ring(self):
        '''
        Start fxs ring
        '''
        return await self._access.post('phone/fxs_ring_start/')

    async def stop_fxs_ring(self):
        '''
        Stop fxs ring
        '''
        return await self._access.post('phone/fxs_ring_stop/')
