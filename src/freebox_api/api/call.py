"""
Call API.
https://dev.freebox.fr/sdk/os/call/
"""
from typing import Dict

from freebox_api.access import Access


class Call:
    """
    Call
    """

    def __init__(self, access: Access):
        self._access = access

    mark_call_log_as_read_data_schema = {"new": False}

    async def delete_call_log(self, log_id: int) -> Dict[str, bool]:
        """
        Delete call log

        log_id : `int`
        """
        return await self._access.delete(f"call/log/{log_id}")  # type: ignore

    async def delete_calls_log(self) -> None:
        """
        Delete calls log
        """
        return await self._access.delete("call/log/delete_all/")  # type: ignore

    async def get_call_log(self, log_id):
        """
        Get call log
        """
        return await self._access.get(f"call/log/{log_id}")

    async def get_calls_log(self):
        """
        Get calls logs
        """
        return await self._access.get("call/log/")

    async def mark_calls_log_as_read(self):
        """
        Mark calls log as read
        """
        return await self._access.post("call/log/mark_all_as_read/")

    async def update_call_log(self, log_id, call_entry):
        """
        Update call log
        Used to mark call log as read

        call_entry : `dict`
        """
        return await self._access.put(f"call/log/{log_id}", call_entry)
