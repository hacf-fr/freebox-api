import inspect
import logging

_LOGGER = logging.getLogger(__name__)


class Switches:
    """
    Switches

    All your switch are belong to us
    """

    def __init__(self, shelf):
        api_members = inspect.getmembers(shelf, predicate=inspect.getmembers)
        s_name = self.__class__.__name__.casefold()
        for c_name, c_obj in api_members:
            if (
                hasattr(c_obj, "_access")
                and not c_name.startswith("_")
                and c_name != s_name
            ):
                l_methods = inspect.getmembers(
                    getattr(shelf, c_name), predicate=inspect.ismethod
                )
                for k, v in l_methods:
                    if "_switch" in k and not k.startswith("_"):
                        setattr(self, k, v)
                        self._sw_list.add(k)

    _sw_list: set = set()

    def get_switches(self):
        """Return a set of all known switches"""
        return self._sw_list

    async def switch_set(self, switches_set: set, enable: bool):
        """
        Switch a set of switches

        switches : `set`
        enable : `bool`
        """

        for sw_name in switches_set:
            if hasattr(self, sw_name) and sw_name in self._sw_list:
                await getattr(self, sw_name)(enabled=enable)
            else:
                _LOGGER.debug(f"Can't switch {sw_name}, it is not a switch")

    async def status(self, s_list=None):
        """
        Return status dict for a set of switches

        s_list : `set`

        Returns all switches if s_list is not a set of switches
        """

        status = {}
        if not isinstance(s_list, set):
            s_list = self._sw_list

        for sw_name in s_list:
            if hasattr(self, sw_name) and sw_name in self._sw_list:
                status[sw_name] = await getattr(self, sw_name)
            else:
                _LOGGER.debug(f"Can't get status for {sw_name}, it is not a switch")
        return status
