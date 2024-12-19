"""
This example can be run safely as it won't change anything in your box configuration
"""

import asyncio

# import m3u8

# from pathlib import Path

from freebox_api import Freepybox

# from freebox_api.aiofreepybox import DEFAULT_TOKEN_FILE


async def demo():
    # Instantiate Freepybox class using default application descriptor
    # and default token_file location
    fbx = Freepybox(api_version="latest")
    # fbx = Freepybox(token_file=DEFAULT_TOKEN_FILE, api_version="latest")
    # fbx = Freepybox(token_file=Path(DEFAULT_TOKEN_FILE), api_version="latest")

    # To find out the HTTPS host and port of your Freebox, go to
    # http://mafreebox.freebox.fr/api_version

    # Connect to the Freebox
    # Be ready to authorize the application on the Freebox if you use this
    # example for the first time

    # Valid certificate
    # await fbx.open(host="[custom].freeboxos.fr", port=[https_port])
    # Invalid, self signed, certificate
    # await fbx.open(host="[api_domain].fbxos.fr", port=[https_port])
    # Invalid, self signed, certificate
    await fbx.open(host="mafreebox.freebox.fr", port=443)

    print("\n" * 2)
    print("=" * 50)
    print("= Connected =")
    print(fbx._access.base_url)  # pylint: disable=protected-access
    print("=" * 50)

    ##############
    # System     #
    ##############
    print("-" * 25)
    print("- System config -")
    print("-" * 25)
    fbx_config = await fbx.system.get_config()
    print(fbx_config)
    print(f"Freebox model name : {fbx_config['model_info']['pretty_name']}")
    print(f"Freebox firmware version : {fbx_config['firmware_version']}")
    print(f"Freebox MAC address : {fbx_config['mac']}")

    sensors = fbx_config["sensors"]
    print("-" * 25)
    print("- System config sensors -")
    print(sensors)
    temp_sw = next(s for s in sensors if s["id"] == "temp_sw")
    print(f"Freebox {temp_sw['name']} : {temp_sw['value']}")
    print("-" * 25)

    ##############
    # Connection #
    ##############
    print("-" * 25)
    print("- Connection config -")
    print("-" * 25)
    conn_config = await fbx.connection.get_config()
    print(conn_config)
    print(
        f"Freebox API access : https://{conn_config['api_domain']}:{conn_config['https_port']}/"
    )

    print("-" * 25)
    print("- Connection status -")
    conn_status = await fbx.connection.get_status()
    print(conn_status)
    print(f"Freebox IPv4 : {conn_status['ipv4']}")
    print(f"Freebox IPv6 : {conn_status['ipv6']}")

    ##############
    # DHCP       #
    ##############
    print("-" * 25)
    print("- DHCP config -")
    print("-" * 25)
    dhcp_config = await fbx.dhcp.get_config()
    print(dhcp_config)

    # Modify ip_range configuration
    # dhcp_config["ip_range_start"] = "192.168.0.10"
    # dhcp_config["ip_range_end"] = "192.168.0.50"
    # Send new configuration to the Freebox. This line is commented to avoid any disaster.
    # await fbx.dhcp.set_config(dhcp_config)

    ##############
    # LAN        #
    ##############
    print("-" * 25)
    print("- LAN config -")
    print("-" * 25)
    lan_config = await fbx.lan.get_config()
    print(lan_config)
    print("-" * 25)
    print("- LAN hosts -")
    print("-" * 25)
    lan_hosts = await fbx.lan.get_hosts_list()
    print(lan_hosts[0])

    ##############
    # Home       #
    ##############
    print("-" * 25)
    print("- Home -")
    print("-" * 25)
    try:
        print("- Camera list -")
        home_cameras = await fbx.home.get_camera()
        print(home_cameras)
        print("-" * 25)
        print("- Camera snapshot -")
        # Get a jpg snapshot from the first camera
        home_camera_snapshot = await fbx.home.get_camera_snapshot()
        print(home_camera_snapshot)

        print("-" * 25)
        print("- Camera stream -")
        # Get a TS stream from a camera
        home_camera_stream = await fbx.home.get_camera_stream_m3u8()  # noqa F841
        # m3u8_obj = m3u8.loads(await home_camera_stream.text())
        # fbx_ts = await fbx.home.get_camera_ts(m3u8_obj.files[0])  # noqa F841
    except Exception as error:
        print(error)

    ##############
    # AirMedia   #
    ##############
    print("-" * 25)
    print("- AirMedia receivers -")
    print("-" * 25)
    airmedia_receivers = await fbx.airmedia.get_airmedia_receivers()
    print(airmedia_receivers)

    ##############
    # Player     #
    ##############
    print("-" * 25)
    print("- Player list -")
    print("-" * 25)
    try:
        players = await fbx.player.get_players()
        print(players)
    except Exception as error:
        print(error)

    ##############
    # Call       #
    ##############
    print("-" * 25)
    print("- Call -")
    print("-" * 25)
    fbx_call_list = await fbx.call.get_calls_log()
    print(fbx_call_list[0])

    ##############
    # Download   #
    ##############
    print("-" * 25)
    print("- Download tasks -")
    print("-" * 25)
    download_tasks = await fbx.download.get_download_tasks()
    print(download_tasks)

    ##############
    # TV         #
    ##############
    print("-" * 25)
    print("- TV channels -")
    print("-" * 25)
    tv_channels = list((await fbx.tv.get_tv_channels()).values())
    print(tv_channels[0])

    print("-" * 25)
    print("- TV programs for channel -")
    tv_programs = await fbx.tv.get_tv_programs_by_channel(tv_channels[0]["uuid"])
    print(tv_programs)

    # Reboot your Freebox. This line is commented to avoid any disaster.
    # await fbx.system.reboot()

    # Close the Freebox session
    await fbx.close()
    print("=" * 50)
    print("= Disconnected =")
    print("=" * 50)
    print("\n" * 2)


loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()
