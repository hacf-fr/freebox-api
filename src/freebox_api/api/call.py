import logging

_LOGGER = logging.getLogger(__name__)


class Call:
    """
    Call
    """

    def __init__(self, access):
        self._access = access

    mark_call_log_as_read_data_schema = {"new": False}

    async def delete_call_log(self, log_id):
        """
        Delete call log

        log_id : `int`
        """
        await self._access.delete(f"call/log/{log_id}")

    async def delete_calls_log(self):
        """
        Delete calls log
        """
        await self._access.delete("call/log/delete_all/")

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

    # TODO: remove
    async def get_call_list(self):
        """
        Returns the collection of all call entries
        """
        _LOGGER.warning(
            "Using deprecated get_call_list, please use get_calls_log instead"
        )
        return await self.get_calls_log()

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
