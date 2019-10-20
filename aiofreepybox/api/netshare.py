class Netshare:
    """
    Netshare
    """

    def __init__(self, access):
        self._access = access

    server_type = [
        "powerbook",
        "powermac",
        "macmini",
        "imac",
        "macbook",
        "macbookpro",
        "macbookair",
        "macpro",
        "appletv",
        "airport",
        "xserve",
    ]

    afp_configuration_schema = {
        "enabled": False,
        "guest_allow": False,
        "login_name": "",
        "login_password": "",
        "server_type": server_type[0],
    }

    samba_configuration_schema = {
        "file_share_enabled": False,
        "logon_enabled": False,
        "logon_password": "",
        "logon_user": "",
        "print_share_enabled": True,
        "workgroup": "workgroup",
    }

    async def get_afp_configuration(self):
        """
        Get afp configuration
        """
        return await self._access.get("netshare/afp/")

    async def get_samba_configuration(self):
        """
        Get samba configuration
        """
        return await self._access.get("netshare/samba/")

    async def set_afp_configuration(self, afp_configuration):
        """
        Set afp configuration

        afp_configuration : `dict`
        """
        return await self._access.put("netshare/afp/", afp_configuration)

    async def set_samba_configuration(self, samba_configuration):
        """
        Set samba configuration

        samba_configuration : `dict`
        """
        return await self._access.put("netshare/samba/", samba_configuration)
