class Netshare:

    def __init__(self, access):
        self._access = access

    server_type = [
        'powerbook',
        'powermac',
        'macmini',
        'imac',
        'macbook',
        'macbookpro',
        'macbookair',
        'macpro',
        'appletv',
        'airport',
        'xserve'
    ]

    afp_configuration_schema = {
        'enabled': False,
        'guestAllow': False,
        'loginName': '',
        'loginPassword': '',
        'serverType': server_type[0]
    }

    samba_configuration_schema = {
        'fileShareEnabled': False,
        'logonEnabled': False,
        'logonPassword': '',
        'logonUser': '',
        'printShareEnabled': True,
        'workgroup': 'workgroup'
    }

    async def get_afp_configuration(self):
        """
        Get afp configuration
        """
        return await self._access.get('netshare/afp/')

    async def get_samba_configuration(self):
        """
        Get samba configuration
        """
        return await self._access.get('netshare/samba/')

    async def set_afp_configuration(self, afp_configuration):
        """
        Set afp configuration
        """
        return await self._access.put('netshare/afp/', afp_configuration)

    async def set_samba_configuration(self, samba_configuration):
        """
        Set samba configuration
        """
        return await self._access.put('netshare/samba/', samba_configuration)
