from typing import Any, Dict, Optional

from aiofreepybox.access import Access


class System:
    """
    System
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    expansion_types = [
        "unknown",
        "dsl_lte",
        "dsl_lte_external_antennas",
        "ftth_p2p",
        "ftth_pon",
        "security",
    ]
    expansions_type = {
        "unknown": "Inconnu",
        "dsl_lte": "xDSL + 4G",
        "dsl_lte_external_antennas": "xDSL + 4G avec antennes externes",
        "ftth_p2p": "FTTH P2P",
        "ftth_pon": "FTTH PON",
        "security": "Sécurité / Alarme",
    }
    images_fbx_gw_back = [
        "resources/images/fbx/gw_back_v6.png",
        "resources/images/fbx/gw_back_mini4k.png",
        "resources/images/fbx/gw_back_onebox.png",
        "resources/images/fbx/gw_back_v7.png",
        "resources/images/fbx/gw_back_v7_empty.png",
    ]

    async def get_config(self) -> Optional[Dict[str, Any]]:
        """
        Get system configuration:
        """
        return await self._access.get("system/")

    def get_img_fbx_gw_back(self, img_id: int) -> str:
        """
        Get freebox gateway back image

        img_id : `int`
        """
        return f"/{self.images_fbx_gw_back[img_id]}"

    def get_img_fbx_gw_back_expansion(
        self, img_expansion_types: str, slot_index: int
    ) -> str:
        """
        Get freebox gateway back expansion image path

        img_expansion_types : `expansion_types`[index]
        slot_index : 0 | 1
        """
        return (
            f"/resources/images/fbx/gw_back_v7_{img_expansion_types}_{slot_index}.png"
        )

    '''     Disabled: requires password login

    async def get_settings(self):
        """
        Get system settings
        """
        return await self._access.get('settings/')
    '''

    async def reboot(self) -> None:
        """
        Reboot freebox
        """
        await self._access.post("system/reboot")

    '''     Disabled: requires password login

    async def set_settings(self, setting_id, settings_data):
        """
        Set system settings
        """
        return await self._access.put(f'settings/{setting_id}', settings_data)
    '''
