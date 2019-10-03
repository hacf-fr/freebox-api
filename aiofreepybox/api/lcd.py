class Lcd:

    def __init__(self, access):
        self._access = access

    lcd_config_schema = {
        'orientation': 0,
        'brightness': 100,
        'orientation_forced': False
    }

    async def get_configuration(self):
        '''
        Get configuration
        '''
        return await self._access.get('lcd/config')

    async def set_configuration(self, lcd_config=lcd_config_schema):
        '''
        Set configuration
        '''
        return await self._access.put('lcd/config', lcd_config)
