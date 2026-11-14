"""
Parental Control API.
https://dev.freebox.fr/sdk/os/parental/
"""

from freebox_api.access import Access


class Parental:
    """
    Parental Control
    """

    def __init__(self, access: Access):
        self._access = access

    # valid values are: allowed, denied or webonly
    default_filter_mode = "allowed"

    parental_control_configuration_schema = {"default_filter_mode": default_filter_mode}

    async def create_parental_filter(self, parental_filter):
        """
        Create parental filter
        """
        return await self._access.post("parental/filter/", parental_filter)

    async def delete_parental_filter(self, filter_id: int) -> dict[str, bool]:
        """
        Delete parental filter
        """
        return await self._access.delete(f"parental/filter/{filter_id}")  # type: ignore

    async def edit_parental_filter(self, filter_id, parental_filter):
        """
        Edit parental filter
        """
        return await self._access.put(f"parental/filter/{filter_id}", parental_filter)

    async def edit_parental_filter_planning(self, filter_id, parental_filter_planning):
        """
        Edit parental filter planning
        """
        return await self._access.put(
            f"parental/filter/{filter_id}/planning/", parental_filter_planning
        )

    async def get_parental_config(self):
        """
        Get parental config
        """
        return await self._access.get("parental/config/")

    async def get_parental_filter_planning(self, filter_id):
        """
        Get parental filter planning
        """
        return await self._access.get(f"parental/filter/{filter_id}/planning/")

    async def get_parental_filters(self):
        """
        Get parental filters
        """
        return await self._access.get("parental/filter/")

    async def set_parental_control_configuration(
        self, parental_control_configuration=parental_control_configuration_schema
    ):
        """
        Set parental control configuration
        """
        return await self._access.put(
            "parental/config/", parental_control_configuration
        )

    async def get_profiles(self):
        """
        Get the parental control profiles
        """
        return await self._access.get("profile/")

    async def get_network_controls(self):
        """
        Get the network control (Internet access) of every profile
        """
        return await self._access.get("network_control/")

    async def get_network_control(self, profile_id: int):
        """
        Get the network control (Internet access) of a profile
        """
        return await self._access.get(f"network_control/{profile_id}")

    async def set_network_control(self, profile_id: int, network_control):
        """
        Set the network control (Internet access) of a profile

        The router rejects an update without the "macs" and "cdayranges"
        of the profile: send back the ones returned by get_network_control.
        Pause the profile with "override": True and "override_mode": "denied"
        ("override_until": 0 keeps it paused until further notice),
        resume its planning with "override": False.
        """
        return await self._access.put(f"network_control/{profile_id}", network_control)
