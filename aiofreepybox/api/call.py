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

    async def get_call_log(self):
        """
        Get call logs
        """
        return await self._access.get("call/log/")

    # TODO: remove
    async def get_call_list(self):
        """
        Returns the collection of all call entries
        """
        _LOGGER.warning(
            "Using deprecated get_call_list, please use get_call_log instead"
        )
        return await self.get_call_log()

    async def mark_call_log_as_read(self, log_id, mark_call_log_as_new=False):
        """
        Mark call log as read

        log_id : `int`
        mark_call_log_as_new : `bool`
        """
        mark_call_log_as_read_data = self.mark_call_log_as_read_data_schema
        mark_call_log_as_read_data["new"] = mark_call_log_as_new
        return await self._access.put(f"call/log/{log_id}", mark_call_log_as_read_data)
