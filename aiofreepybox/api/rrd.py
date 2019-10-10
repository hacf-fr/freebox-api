import time
import operator


class Rrd:

    def __init__(self, access):
        self._setup = False
        self._access = access

    db = [
        'net',
        'temp',
        'dsl',
        'switch'
    ]

    fields = [
        'time'
    ]

    fields_net = [
        'bw_down',
        'bw_up',
        'rate_down',
        'rate_up',
        'vpn_rate_down',
        'vpn_rate_up'
    ]

    fields_fans = []

    fields_temp = []

    fields_temps = []

    fields_dsl = [
        'rate_down',
        'rate_up',
        'snr_down',
        'snr_up'
    ]

    fields_switch_rx = [
        'rx_1',
        'rx_2',
        'rx_3',
        'rx_4'
    ]

    fields_switch_tx = [
        'tx_1',
        'tx_2',
        'tx_3',
        'tx_4'
    ]

    rrd_data_schema = {
        'dateStart': int(time.time() - 3600),
        'dateEnd': int(time.time()),
        'db': db[1],
        'fields': fields_temps,
        'precision': 10
    }

    async def init(self):
        """
        Init
            Call Init on startup to setup temp and fans fields
        """
        if not self._setup:
            resp = await self._access.get('system/')
            self.fields_temp = list(map(operator.itemgetter('id'), resp['sensors']))
            self.fields_fans = list(map(operator.itemgetter('id'), resp['fans']))
            self.fields_temps = self.fields_temp + self.fields_fans
            self._setup = True

    async def get_rrd_stats(self, rrd_data=None):
        '''
        Get rrd stats
        '''
        if rrd_data is None:
            rrd_data = self.rrd_data_schema
        return await self._access.post('rrd/', rrd_data)
