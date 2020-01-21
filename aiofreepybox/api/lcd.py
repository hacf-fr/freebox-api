from typing import Any, Dict, Optional

from aiofreepybox.access import Access


class Lcd:
    """
    Lcd
    """

    def __init__(self, access: Access):
        self._access = access

    async def get_config(self) -> Optional[Dict[str, Any]]:
        """
        Get configuration
        """
        return await self._access.get("lcd/config")

    async def set_config(self, lcd_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Set configuration

        lcd_config : `dict`
        """
        return await self._access.put("lcd/config", lcd_config)

    async def update_config(
        self,
        orientation: int = None,
        brightness: int = None,
        orientation_forced: bool = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Update configuration

        orientation : `int`
        brightness : `int`
        orientation_forced : `bool`
        """
        lcd_config = {}
        if orientation is None and brightness is None and orientation_forced is None:
            return await self.get_config()
        if orientation is not None:
            lcd_config["orientation"] = orientation
        if brightness is not None:
            lcd_config["brightness"] = brightness
        if orientation_forced is not None:
            lcd_config["orientation_forced"] = orientation_forced
        return await self.set_config(lcd_config)
