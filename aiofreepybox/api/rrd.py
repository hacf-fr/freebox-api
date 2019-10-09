import time


class Rrd:

    def __init__(self, access):
        self._access = access

    db = [
        'net',
        'temp',
        'dsl',
        'switch'
    ]

    fields = [
        'bw_down',
        'bw_up',
        'rate_down',
        'rate_up',
        'vpn_rate_down',
        'vpn_rate_up',
        'snr_down',
        'snr_up',
        'rx_1',
        'rx_2',
        'rx_3',
        'rx_4',
        'tx_1',
        'tx_2',
        'tx_3',
        'tx_4',
        'time'
    ]

    fields_net = [
        fields[0],
        fields[1],
        fields[2],
        fields[3],
        fields[4],
        fields[5]
    ]

    '''
    fields_temp = [
        get temp fields from system.get_config['sensors']
        get fans fields from system.get_config['fans']
    ]
    '''

    fields_dsl = [
        fields[2],
        fields[3],
        fields[6],
        fields[7]
    ]

    fields_switch_rx = [
        fields[8],
        fields[9],
        fields[10],
        fields[11]
    ]

    fields_switch_tx = [
        fields[12],
        fields[13],
        fields[14],
        fields[15]
    ]

    rrd_data_schema = {
        'dateStart': int(time.time() - 3600),
        'dateEnd': int(time.time()),
        'db': db[0],
        'fields': fields,
        'precision': 10
    }

    async def get_rrd_stats(self, rrd_data=None):
        '''
        Get rrd stats
        '''
        if rrd_data is None:
            rrd_data = self.rrd_data_schema
        return await self._access.post('rrd/', rrd_data)
