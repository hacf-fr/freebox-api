import operator
import time
from typing import Any, Dict, List, Optional

from aiofreepybox.access import Access

_UPTO_V5_FIELDS_TEMP = ["cpub", "cpum", "hdd", "sw"]
_UPTO_V5_FIELDS_FAN = ["fan_speed"]


class Rrd:
    """
    Rrd
    """

    def __init__(self, access: Access) -> None:
        self._setup = False
        self._access = access

    db = ["net", "temp", "dsl", "switch"]
    fields = ["time"]
    fields_net = [
        "bw_down",
        "bw_up",
        "rate_down",
        "rate_up",
        "vpn_rate_down",
        "vpn_rate_up",
    ]
    fields_fans: List[str] = []
    fields_temp: List[str] = []
    fields_temps: List[str] = []
    fields_dsl = ["rate_down", "rate_up", "snr_down", "snr_up"]
    fields_switch_rx = ["rx_1", "rx_2", "rx_3", "rx_4"]
    fields_switch_tx = ["tx_1", "tx_2", "tx_3", "tx_4"]
    rrd_data_schema = {
        "dateStart": int(time.time() - 3600),
        "dateEnd": int(time.time()),
        "db": db[0],
        "fields": fields_net,
        "precision": 10,
    }

    async def init(self) -> None:
        """
        Init
            Call init on startup to setup temp and fans fields
        """

        if not self._setup:
            a_v = self._access.base_url.split("/")
            s_a_v = a_v[(a_v.__len__() - 2)][1:]

            if int(s_a_v) > 5:
                resp = await self._access.get("system/")
                self.fields_temp = list(map(operator.itemgetter("id"), resp["sensors"]))
                self.fields_fans = list(map(operator.itemgetter("id"), resp["fans"]))
            else:
                self.fields_temp = _UPTO_V5_FIELDS_TEMP
                self.fields_fans = _UPTO_V5_FIELDS_FAN

            self.fields_temps = self.fields_temp + self.fields_fans
            self._setup = True

    async def get_rrd_stats(
        self, rrd_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get rrd stats
        """
        return await self._access.post("rrd/", rrd_data)
