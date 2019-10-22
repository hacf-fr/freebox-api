class Phone:
    """
    Phone
    """

    def __init__(self, access):
        self._access = access

    async def get_dect_vendors(self):
        """
        Get dect vendors
        """
        return await self._access.get("phone/dect_vendors/")

    async def get_phones(self):
        """
        Get phones list
        """
        return await self._access.get("phone/")

    async def get_phone_config(self):
        """
        Get phone configuration
        """
        return await self._access.get("phone/config/")

    async def set_phone_config(self, phone_entry):
        """
        Set phone config

        phone_entry : `dict`
        """
        return await self._access.put("phone/config/", phone_entry)

    async def start_dect_configuration(self, dect_enabled=None, dect_registration=None):
        """
        Start dect configuration
        To start dect configuration dect_enabled and dect_registration must be True ,
        but it can also be used to enable/disable dect with dect_enabled True/False

        dect_enabled : `bool`
        dect_registration : `bool`
        """

        dect_configuration = dict
        if dect_enabled is None and dect_registration is None:
            return await get_phone_config()
        elif dect_enabled is not None:
            dect_configuration["dect_enabled"] = dect_enabled
        if dect_registration is not None:
            dect_configuration["dect_registration"] = dect_registration
        return await self._access.put("phone/config/", dect_configuration)

    async def start_dect_page(self):
        """
        Start dect paging
        """
        return await self._access.post("phone/dect_page_start/")

    async def stop_dect_page(self):
        """
        Stop dect paging
        """
        return await self._access.post("phone/dect_page_stop/")

    async def start_fxs_ring(self):
        """
        Start fxs ring
        """
        return await self._access.post("phone/fxs_ring_start/")

    async def stop_fxs_ring(self):
        """
        Stop fxs ring
        """
        return await self._access.post("phone/fxs_ring_stop/")
