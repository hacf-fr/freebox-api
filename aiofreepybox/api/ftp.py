class Ftp:
    """
    Ftp
    """

    def __init__(self, access):
        self._access = access

    ftp_configuration_schema = {
        "enabled": False,
        "allow_anonymous": False,
        "allow_anonymous_write": False,
        "allow_remote_access": False,
        "remote_domain": "",
        "password": "",
        "port_ctrl": 12345,
        "port_data": 45678,
    }

    async def get_ftp_configuration(self):
        """
        Get ftp configuration
        """
        return await self._access.get("ftp/config/")

    async def set_ftp_configuration(self, ftp_configuration):
        """
        Set ftp configuration
        """
        return await self._access.put("ftp/config/", ftp_configuration)
