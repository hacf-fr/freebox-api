"""
LCD API.
https://dev.freebox.fr/sdk/os/lcd/
"""
from freebox_api.access import Access


class Lcd:
    """
    LCD
    """

    def __init__(self, access: Access):
        self._access = access

    lcd_config_schema = {
        "orientation": 0,
        "brightness": 100,
        "orientation_forced": False,
    }

    async def get_configuration(self):
        """
        Get configuration
        """
        return await self._access.get("lcd/config")

    async def set_configuration(self, lcd_config=None):
        """
        Set configuration
        """
        if lcd_config is None:
            lcd_config = self.lcd_config_schema
        return await self._access.put("lcd/config", lcd_config)
