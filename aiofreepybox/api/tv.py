import time
from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access

_DEFAULT_BOUQUET = "freeboxtv"


class Tv:
    """
    Tv
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    async def archive_tv_record(self, record_id: int):
        """
        Archive tv record

        record_id : `int`
        """
        return await self._access.post(f"pvr/programmed/{record_id}/ack/")

    async def create_tv_record(
        self, tv_record: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create tv record

        tv_record : `dict`
        """
        return await self._access.post("pvr/programmed/", tv_record)

    async def create_tv_record_generator(self, tv_record_generator: Dict[str, Any]):
        """
        Create tv record generator

        tv_record_generator : `dict`
        """
        return await self._access.post("pvr/generator/", tv_record_generator)

    async def delete_finished_tv_record(self, record_id: int) -> None:
        """
        Delete finished tv record

        record_id : `int`
        """
        await self._access.delete(f"pvr/finished/{record_id}")

    async def delete_programmed_tv_record(self, record_id: int) -> None:
        """
        Delete programmed tv record

        record_id : `int`
        """
        await self._access.delete(f"pvr/programmed/{record_id}")

    async def delete_tv_record_generator(self, generator_id: int) -> None:
        """
        Delete tv record generator

        generator_id : `int`
        """
        await self._access.delete(f"pvr/generator/{generator_id}")

    async def edit_finished_tv_record(
        self, record_id: int, finished: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit finished tv record

        record_id : `int`
        finished : `dict`
        """
        return await self._access.put(f"pvr/finished/{record_id}", finished)

    async def edit_programmed_tv_record(
        self, record_id: int, tv_record: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit programmed tv record

        record_id : `int`
        tv_record : `dict`
        """
        return await self._access.put(f"pvr/programmed/{record_id}", tv_record)

    async def edit_tv_record_generator(
        self, generator_id: int, tv_record_generator: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Edit tv record generator

        generator_id : `int`
        tv_record_generator : `dict`
        """
        return await self._access.put(
            f"pvr/generator/{generator_id}", tv_record_generator
        )

    async def get_finished_tv_records(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get finished tv records
        """
        return await self._access.get("pvr/finished/")

    async def get_mycanal_token(self) -> Optional[str]:
        """
        Get mycanal token
        """
        return await self._access.get("tv/mycanal_token")

    async def get_programmed_tv_records(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get programmed tv records
        """
        return await self._access.get("pvr/programmed/")

    async def get_tv_bouquet(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get tv bouquet
        """
        return await self._access.get("tv/bouquets/")

    async def get_tv_bouquet_channels(
        self, bouquet_id: str = _DEFAULT_BOUQUET
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get tv bouquet channels

        bouquet_id : `str` , optional
            , Default to _DEFAULT_BOUQUET
        """
        return await self._access.get(f"tv/bouquets/{bouquet_id}/channels/")

    async def get_tv_channels(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Get tv channels
        """
        return await self._access.get("tv/channels/")

    async def get_tv_default_bouquet_channels(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get tv default bouquet channels
        """
        return await self.get_tv_bouquet_channels()

    async def get_tv_program(self, program_id: int) -> Optional[Dict[str, Any]]:
        """
        Get tv program

        program_id : `int`
        """
        return await self._access.get(f"tv/epg/programs/{program_id}")

    async def get_tv_program_highlights(
        self, channel_id: int, date: int = int(time.time())
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get tv program highlights

        channel_id : `int`
        date : `int`
        """
        return await self._access.get(f"tv/epg/highlights/{channel_id}/{date}")

    async def get_tv_programs_by_channel(
        self, channel_id: int, date: int = int(time.time())
    ) -> Optional[Dict[str, Any]]:
        """
        Get tv programs by channel

        channel_id : `int`
        date : `int`
        """
        return await self._access.get(f"tv/epg/by_channel/{channel_id}/{date}")

    async def get_tv_programs_by_date(
        self, date: int = int(time.time())
    ) -> Optional[Dict[str, Any]]:
        """
        Get tv programs by date

        date : `int`
        """
        return await self._access.get(f"tv/epg/by_time/{date}")

    async def get_tv_records_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get tv records configuration
        """
        return await self._access.get("pvr/config/")

    async def get_tv_record_generator(
        self, generator_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get tv record generator

        generator_id : `int`
        """
        return await self._access.get(f"pvr/generator/{generator_id}")

    async def get_tv_records_media_list(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get tv records media list
        """
        return await self._access.get("pvr/media/")

    async def get_tv_status(self) -> Optional[Dict[str, bool]]:
        """
        Get tv status
        """
        return await self._access.get("tv/status/")
