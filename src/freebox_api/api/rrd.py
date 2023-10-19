"""
RRD API [UNSTABLE].
https://dev.freebox.fr/sdk/os/rrd/
"""
import time

from freebox_api.access import Access


class Rrd:
    """
    RRD
    """

    def __init__(self, access: Access):
        self._access = access

    db = ["net", "temp", "dsl", "switch"]

    fields = [
        "bw_down",
        "bw_up",
        "cpub",
        "cpum",
        "fan_speed",
        "hdd",
        "rate_down",
        "rate_up",
        "snr_down",
        "snr_up",
        "sw",
        "rx_1",
        "rx_2",
        "rx_3",
        "rx_4",
        "tx_1",
        "tx_2",
        "tx_3",
        "tx_4",
        "femto",
        "vpn_rate_down",
        "vpn_rate_up",
        "time",
    ]

    fields_net = [fields[0], fields[1], fields[6], fields[7], fields[20], fields[21]]

    fields_temp = [fields[2], fields[3], fields[4], fields[5], fields[10], fields[19]]

    fields_dsl = [fields[6], fields[7], fields[8], fields[9]]

    fields_switch_rx = [fields[11], fields[12], fields[13], fields[14]]

    fields_switch_tx = [fields[15], fields[16], fields[17], fields[18]]

    rrd_data_schema = {
        "dateStart": int(time.time() - 3600),
        "dateEnd": int(time.time()),
        "db": db[0],
        "fields": fields,
        "precision": 10,
    }

    async def get_rrd_stats(self, rrd_data=rrd_data_schema):
        """
        Get rrd stats
        """
        return await self._access.post("rrd/", rrd_data)
