#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This example can be run safely as it won't change anything in your box configuration
'''

import asyncio
import m3u8

from aiofreepybox import Freepybox


async def demo():
    # Instantiate Freepybox class using default application descriptor
    # and default token_file location
    fbx = Freepybox()

    # To find out the HTTPS host and port of your freebox, go to
    # http://mafreebox.freebox.fr/api_version

    # Connect to the freebox
    # Be ready to authorize the application on the Freebox if you use this
    # example for the first time
    await fbx.open(host='abcdefgh.fbxos.fr', port=1234)

    if fbx.api_version == 'v6':
        # Get a jpg snapshot from a camera
        fbx_cam_jpg = await fbx.home.get_camera_snapshot()

        # Get a TS stream from a camera
        r = await fbx.home.get_camera_stream_m3u8()
        m3u8_obj = m3u8.loads(await r.text())
        fbx_ts = await fbx.home.get_camera_ts(m3u8_obj.files[0])

    # Dump freebox configuration using system API
    # Extract temperature and mac address
    fbx_config = await fbx.system.get_config()
    sensors = fbx_config['sensors']
    temp_sw = next(s for s in sensors if s['id'] == 'temp_sw')
    print('Freebox temperature : {0}'.format(temp_sw['value']))
    print('Freebox mac address : {0}'.format(fbx_config['mac']))

    # Dump DHCP configuration using dhcp API
    fbx_dhcp_config = await fbx.dhcp.get_config()
    # Modify ip_range configuration
    fbx_dhcp_config['ip_range_start'] = '192.168.0.10'
    fbx_dhcp_config['ip_range_end'] = '192.168.0.50'
    # Send new configuration to the freebox. This line is commented to avoid any disaster.
    # await fbx.dhcp.set_config(fbx_dhcp_config)

    # Get the call list and print the last call entry
    fbx_call_list = await fbx.call.get_call_list()
    print(fbx_call_list[0])

    # Reboot your freebox. This line is commented to avoid any disaster.
    # await fbx.system.reboot()

    # Close the freebox session
    await fbx.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()
