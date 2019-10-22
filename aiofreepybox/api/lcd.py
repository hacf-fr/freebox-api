class Lcd:
    """
    Lcd
    """

    def __init__(self, access):
        self._access = access

    async def get_configuration(self):
        """
        Get configuration
        """
        return await self._access.get("lcd/config")

    async def set_configuration(
        self, orientation=None, brightness=None, orientation_forced=None
    ):
        """
        Set configuration

        orientation : `int`
        brightness : `int`
        orientation_forced : `bool`
        """
        lcd_config = dict
        if orientation is None and brightness is None and orientation_forced is None:
            return await self.get_configuration()
        elif orientation is not None:
            lcd_config["orientation"] = orientation
        if brightness is not None:
            lcd_config["brightness"] = brightness
        elif orientation_forced is not None:
            lcd_config["orientation_forced"] = orientation_forced
        return await self._access.put("lcd/config", lcd_config)

    async def update_configuration(self, lcd_config):
        """
        Update configuration

        lcd_config : `dict`
        """
        return await self._access.put("lcd/config", lcd_config)
