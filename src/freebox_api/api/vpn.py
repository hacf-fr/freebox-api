class Vpn:
    """
    API to manage VPN Servers & Clients
    """

    def __init__(self, access):
        self._access = access
    
    ipsec_auths = { 'psk': { 'id_source': 'custom', 'id_custom': 'fbxvpn_psk' }, 'lcert_reap': { 'id_source': 'fbxpki', 'id_custom': '' } }
    vpnserver_ipsec_write_parms = { 'ike_version': 'int' }
    vpnserver_ipsec_data_schema = { 'ike_version': 2, 'auth_modes': ipsec_auths }
    pptp_mppes = [ 'disable', 'require', 'require_128' ]
    pptp_auths_write_parms = { 'pap': 'bool', 'chap': 'bool', 'mschapv2': 'bool' }
    pptp_auths = { 'pap': False, 'chap': False, 'mschapv2': True }
    vpnserver_pptp_write_parms = { 'mppe': 'text' }
    vpnserver_pptp_data_schema = { 'mppe': pptp_mppes[1], 'allowed_auth': pptp_auths }
    vpnserver_wireguard_write_parms = { 'mtu': 'int' }
    vpnserver_wireguard_data_schema = { 'mtu': 1360 }
    openvpn_ciphers = [ 'blowfish', 'aes128', 'aes256' ]
    vpnserver_open_write_parms = { 'cipher': 'text', 'use_tcp': 'bool', 'disable_fragment': 'bool' }
    vpnserver_open_data_schema = { 'cipher': openvpn_ciphers[2], 'use_tcp': False, 'disable_fragment': False }
    vpnservers = [ 'ipsec', 'pptp', 'openvpn_routed', 'openvpn_bridge', 'wireguard' ]
    vpnserver_global_write_parms = { 'enabled': 'bool', 'enable_ipv4': 'bool', 'enable_ipv6': 'bool', 'port_ike': 'int', 'port_nat': 'int', 'port': 'int' }
    vpnserver_data_schema = { 'enabled': False, 'enable_ipv4': True, 'enable_ipv6': True, 'port_ike': 500, 'port_nat': 4500, 'port': 63166,
                             'conf_ipsec': vpnserver_ipsec_data_schema, 'conf_pptp': vpnserver_pptp_data_schema, 'conf_openvpn': vpnserver_open_data_schema }
    vpnserver_user_write_parms = { 'login': 'text', 'password': 'text', 'ip_reservation': 'text' }
    vpnserver_user_data_schema = { 'login': 'freebox', 'password': '', 'ip_reservation': '' }
    
    vpnclient_open_write_parms = { 'username': 'text', 'password': 'text', 'config_file': 'text' }
    vpnclient_open_data_schema = { 'username': '', 'password': '', 'config_file': '' }
    pptp_all_auths_write_parms = { 'eap': 'bool', 'mschap': 'bool', 'pap': 'bool', 'chap': 'bool', 'mschapv2': 'bool' }
    pptp_all_auths = { 'eap': False, 'mschap': False, 'pap': False, 'chap': False, 'mschapv2': True }
    vpnclient_pptp_write_parms = { 'username': 'text', 'password': 'text', 'mppe': 'text', 'remote_host': 'text' }
    vpnclient_pptp_data_schema = { 'username': '', 'password': '', 'mppe': pptp_mppes[2], 'remote_host': '', 'allowed_auth': pptp_all_auths }
    vpnclient_types = [ 'pptp', 'openvpn' ]
    vpnclient_data_schema = { 'type': vpnclient_types[0], 'description': '', 'active': False,
                             'conf_pptp': vpnclient_pptp_data_schema, 'conf_openvpn': vpnclient_open_data_schema}

    async def get_server_list(self):
        """
        Gets VPN Server list
        """
        return await self._access.get('vpn/')

    async def get_server_config(self, vpn_id):
        """
        Gets a VPN Server configuration
        """
        return await self._access.get(f"vpn/{vpn_id}/config/")

    async def set_server_config(self, vpn_id, glob_conf={}, spec_conf = None):
        """
        Updates a server config
        """
        if spec_conf != None:
            if vpn_id == 'ipsec':
                spec_conf['auth_modes'] = self.ipsec_auths
                glob_conf['conf_ipsec'] = spec_conf
            elif vpn_id == 'pptp':
                spec_conf['allowed_auth'] = self.pptp_auths
                glob_conf['conf_pptp'] = spec_conf
            elif vpn_id == 'openvpn_routed': glob_conf['conf_openvpn'] = spec_conf
            elif vpn_id == 'openvpn_bridge': glob_conf['conf_openvpn'] = spec_conf
            else: glob_conf['conf_wireguard'] = spec_conf
        return await self._access.put(f"vpn/{vpn_id}/config/", glob_conf)

    async def set_server_pptp_auth(self, vpn_id, conf = pptp_auths):
        """
        Updates auth for a PPTP VPN server config
        """
        cur_conf = self.get_server_config(vpn_id)
        if cur_conf == None: return None
        if cur_conf['type'] != 'pptp': return None
        if cur_conf['conf_pptp']['mppe'] != self.pptp_mppes[0]: return None
        return await self._access.put(f"vpn/{vpn_id}/config/", { 'conf_pptp': { 'allowed_auth': conf } })

    async def get_server_users(self):
        """
        Gets VPN Server user list
        """
        return await self._access.get('vpn/user/')

    async def get_server_user(self, login):
        """
        Gets a VPN Server user details
        """
        return await self._access.get(f"vpn/user/{login}")

    async def add_server_user(self, conf):
        """
        Adds a VPN Server user
        """
        return await self._access.post('vpn/user/', conf)

    async def del_server_user(self, login):
        """
        Deletes a VPN Server user
        """
        return await self._access.delete(f"vpn/user/{login}")

    async def set_server_user(self, login, conf):
        """
        Updates a VPN Server user
        """
        return await self._access.put(f"vpn/user/{login}", conf)

    async def get_server_ippool(self):
        """
        Gets VPN Server IP pool reservations
        """
        return await self._access.get('vpn/ip_pool/')

    async def get_server_connections(self):
        """
        Gets a VPN Server connections
        """
        return await self._access.get('vpn/connection/')

    async def close_server_connection(self, id):
        """
        Closes a VPN Server connection
        """
        return await self._access.delete(f"vpn/connection/{id}")

    async def get_server_user_config(self, server_name, login):
        """
        Gets an OpenVPN Server user configuration for OpenVPN
        """
        return await self._access.get(f"vpn/download_config/{server_name}/{login}")

    async def get_client_list(self):
        """
        Gets VPN Client list
        """
        return await self._access.get('vpn_client/config/')

    async def get_client_config(self, vpn_id):
        """
        Gets a VPN Client configuration
        """
        return await self._access.get(f"vpn_client/config/{vpn_id}")

    async def add_client(self, conf, vpntype=vpnclient_types[0], descr=''):
        """
        Adds a VPN Client
        """
        glob_conf = { 'type': vpntype, 'description': descr, 'active': False }
        if vpntype == 'pptp':
            conf['allowed_auth'] = self.pptp_all_auths
            glob_conf['conf_pptp'] = conf
        elif vpntype == 'openvpn': glob_conf['conf_openvpn'] = conf
        return await self._access.post('vpn_client/config/', payload=glob_conf)

    async def del_client(self, id):
        """
        Deletes a VPN Client
        """
        return await self._access.delete(f"vpn_client/config/{id}")

    async def set_client_active(self, id):
        """
        Changes the active VPN Client
        """
        return await self._access.put(f"vpn_client/config/{id}", { 'active': True })

    async def set_client(self, id, conf, descr=None):
        """
        Changes the VPN Client
        """
        glob_conf = {}
        if descr != None: glob_conf['description'] = descr
        curconf = self.get_client_config(id)
        if curconf['type'] == 'pptp':
            conf['allowed_auth'] = self.pptp_all_auths
            glob_conf['conf_pptp'] = conf
        elif curconf['type'] == 'openvpn': glob_conf['conf_openvpn'] = conf            
        return await self._access.put(f"vpn_client/config/{id}", glob_conf)

    async def set_client_pptp_auth(self, id, conf):
        """
        Changes Auth for PPTP VPN Client
        """
        cur_conf = self.get_client_config(id)
        if cur_conf == None: return None
        if cur_conf['type'] != 'pptp': return None
        if cur_conf['conf_pptp']['mppe'] != self.pptp_mppes[0]: return None
        return await self._access.put(f"vpn_client/config/{id}", { 'conf_pptp': { 'allowed_auth': conf } })

    async def get_client_status(self):
        """
        Gets VPN Client status
        """
        return await self._access.get('vpn_client/status/')

    async def get_client_logs(self):
        """
        Gets VPN Client logs
        """
        return await self._access.get('vpn_client/log/')
    
    async def set_slavery(self, slave=True):
        """
        Manages if download must only be done with a VPN client connection
        """
        return await self._access.put('vpn_client/apps/', { 'fbxgrabberd': { 'use_vpn': slave } })

    async def get_slavery(self):
        """
        Gets application (=downloads) slavery status
        """
        return await self._access.get('vpn_client/apps/')
