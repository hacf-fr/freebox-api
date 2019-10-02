class Ftp:

    def __init__(self, access):
        self._access = access

    ftp_configuration_schema = {
        'allowAnonymous': False,
        'allowAnonymousWrite': False,
        'enabled': False,
        'password': ''
    }

    async def get_ftp_configuration(self):
        '''
        Get ftp configuration
        '''
        return await self._access.get('ftp/config/')

    async def set_ftp_configuration(self, ftp_configuration):
        '''
        Set ftp configuration
        '''
        return await self._access.put('ftp/config/', ftp_configuration)
