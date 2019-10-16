import asyncio
import ipaddress
import os
import json
import logging
import socket
import ssl
import time
from urllib.parse import urljoin

import aiohttp

import aiofreepybox
from aiofreepybox.exceptions import *
from aiofreepybox.access import Access
from aiofreepybox.api.tv import Tv
from aiofreepybox.api.system import System
from aiofreepybox.api.dhcp import Dhcp
from aiofreepybox.api.switch import Switch
from aiofreepybox.api.lan import Lan
from aiofreepybox.api.lcd import Lcd
from aiofreepybox.api.wifi import Wifi
from aiofreepybox.api.phone import Phone
from aiofreepybox.api.fs import Fs
from aiofreepybox.api.fw import Fw
from aiofreepybox.api.freeplug import Freeplug
from aiofreepybox.api.call import Call
from aiofreepybox.api.connection import Connection
from aiofreepybox.api.home import Home
from aiofreepybox.api.parental import Parental
from aiofreepybox.api.nat import Nat
from aiofreepybox.api.notifications import Notifications
from aiofreepybox.api.rrd import Rrd
from aiofreepybox.api.upnpav import Upnpav
from aiofreepybox.api.upnpigd import Upnpigd

# Token file default location
token_filename = 'app_auth'
token_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(token_dir, token_filename)

# Default application descriptor
app_desc = {
    'app_id': 'aiofpbx',
    'app_name': 'aiofreepybox',
    'app_version': aiofreepybox.__version__,
    'device_name': socket.gethostname()
    }

logger = logging.getLogger(__name__)


class Freepybox:
    def __init__(self, app_desc=app_desc, token_file=token_file, api_version='auto', timeout=10):
        self.token_file = token_file
        self.api_version = api_version
        self.api_version_target = 'v6'
        self.timeout = timeout
        self.app_desc = app_desc
        self.fbx_desc = {}
        self._access = None

    async def open(self, host='auto', port='auto'):
        """
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules
        """
        if not self._is_app_desc_valid(self.app_desc):
            raise InvalidTokenError('Invalid application descriptor')

        default_host = 'mafreebox.freebox.fr'
        default_port = 443
        secure = 's'

        # Detect host, port and api_version
        if host != 'auto':
            default_host = host

        if port != 'auto':
            default_port = port
            if default_port == 80:
                secure = ''

        # Checking host and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((default_host, default_port))
        if result != 0:
            raise HttpRequestError(f'Port {default_port} is closed, cannot detect freebox')
        else:
            sock.close()

        cert_path = os.path.join(os.path.dirname(__file__), 'freebox_certificates.pem')
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_verify_locations(cafile=cert_path)

        conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
        self._session = aiohttp.ClientSession(connector=conn)

        r = await self._session.get(f'http{secure}://{default_host}:{default_port}/api_version', timeout=self.timeout)
        self.fbx_desc = await r.json()

        if host == 'auto':
            host = self.fbx_desc['api_domain']

        if port == 'auto':
            port = self.fbx_desc['https_port']

        server_version = self.fbx_desc['api_version'].split('.')[0]
        short_api_version_target = self.api_version_target[1:]
        short_api_version = self.api_version[1:]

        # Check auto api version
        if self.api_version == 'auto':
            self.api_version = self.api_version_target
        # Check server api version
        elif self.api_version == 'server':
            self.api_version = f'v{server_version}'
            if server_version > short_api_version_target:
                logger.warning(f'Using new API version {self.api_version}, results may vary ')
        # Check user api version
        elif short_api_version < short_api_version_target and int(short_api_version) > 0:
            logger.warning(f'Using deprecated API version {self.api_version}, results may vary ')
        elif server_version < short_api_version:
            logger.warning(f'Freebox server does not support this API version ({self.api_version}), downgrading to v{server_version}.')
            self.api_version = f'v{server_version}'
        elif short_api_version != short_api_version_target:
            logger.warning(f'User defined API version set to {self.api_version}, results may vary')

        self._access = await self._get_freebox_access(host, port, self.api_version, self.token_file, self.app_desc, self.timeout)

        # Instantiate freebox modules
        self.tv = Tv(self._access)
        self.system = System(self._access)
        self.dhcp = Dhcp(self._access)
        self.switch = Switch(self._access)
        self.lan = Lan(self._access)
        self.lcd = Lcd(self._access)
        self.wifi = Wifi(self._access)
        self.phone = Phone(self._access)
        self.fs = Fs(self._access)
        self.fw = Fw(self._access)
        self.freeplug = Freeplug(self._access)
        self.call = Call(self._access)
        self.connection = Connection(self._access)
        self.home = Home(self._access)
        self.parental = Parental(self._access)
        self.nat = Nat(self._access)
        self.notifications = Notifications(self._access)
        self.rrd = Rrd(self._access)
        self.upnpav = Upnpav(self._access)
        self.upnpigd = Upnpigd(self._access)

    async def close(self):
        """
        Close the freebox session
        """
        if self._access is None:
            raise NotOpenError('Freebox is not open')

        await self._access.post('login/logout')
        await self._session.close()

    async def get_permissions(self):
        """
        Returns the permissions for this app.

        The permissions are returned as a dictionary key->boolean where the
        keys are the permission identifier (cf. the constants PERMISSION_*).
        A permission not listed in the returned permissions is equivalent to
        having this permission set to false.

        Note that the permissions are the one the app had when the session was
        opened. If they have been changed in the meantime, they may be outdated
        until the session token is refreshed.
        If the session has not been opened yet, returns None.
        """
        if self._access:
            return await self._access.get_permissions()
        else:
            return None

    async def _get_freebox_access(self, host, port, api_version, token_file, app_desc, timeout=10):
        """
        Returns an access object used for HTTP requests.
        """

        base_url = self._get_base_url(host, port, api_version)

        # Read stored application token
        logger.info('Read application authorization file')
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file)

        # If no valid token is stored then request a token to freebox api - Only for LAN connection
        if app_token is None or file_app_desc != app_desc:
            logger.info('No valid authorization file found')

            # Get application token from the freebox
            app_token, track_id = await self._get_app_token(base_url, app_desc, timeout)

            # Check the authorization status
            out_msg_flag = False
            status = None
            while(status != 'granted'):
                status = await self._get_authorization_status(base_url, track_id, timeout)

                # denied status = authorization failed
                if status == 'denied':
                    raise AuthorizationError('The app token is invalid or has been revoked')

                # Pending status : user must accept the app request on the freebox
                elif status == 'pending':
                    if not out_msg_flag:
                        out_msg_flag = True
                        print('Please confirm the authentification on the freebox')
                    await asyncio.sleep(1)

                # timeout = authorization failed
                elif status == 'timeout':
                    raise AuthorizationError('Authorization timed out')

            logger.info('Application authorization granted')

            # Store application token in file
            self._writefile_app_token(app_token, track_id, app_desc, token_file)
            logger.info(f'Application token file was generated: {token_file}')

        # Create freebox http access module
        fbx_access = Access(self._session, base_url, app_token, app_desc['app_id'], timeout)

        return fbx_access

    async def _get_authorization_status(self, base_url, track_id, timeout):
        """
        Get authorization status of the application token
        Returns:
            unknown 	the app_token is invalid or has been revoked
            pending 	the user has not confirmed the authorization request yet
            timeout 	the user did not confirmed the authorization within the given time
            granted 	the app_token is valid and can be used to open a session
            denied 	    the user denied the authorization request
        """
        url = urljoin(base_url, f'login/authorize/{track_id}')
        r = await self._session.get(url, timeout=timeout)
        resp = await r.json()
        return resp['result']['status']

    async def _get_app_token(self, base_url, app_desc, timeout=10):
        """
        Get the application token from the freebox
        Returns (app_token, track_id)
        """
        # Get authentification token
        url = urljoin(base_url, 'login/authorize/')
        data = json.dumps(app_desc)
        r = await self._session.post(url, data=data, timeout=timeout)
        resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('Authorization failed (APIResponse: {})'
                                     .format(json.dumps(resp)))

        app_token = resp['result']['app_token']
        track_id = resp['result']['track_id']

        return(app_token, track_id)

    def _writefile_app_token(self, app_token, track_id, app_desc, file):
        """
        Store the application token in g_app_auth_file file
        """
        d = {**app_desc, 'app_token': app_token, 'track_id': track_id}

        with open(file, 'w') as f:
            json.dump(d, f)

    def _readfile_app_token(self, file):
        """
        Read the application token in the authentication file.
        Returns (app_token, track_id, app_desc)
        """
        try:
            with open(file, 'r') as f:
                d = json.load(f)
                app_token = d['app_token']
                track_id = d['track_id']
                app_desc = {k: d[k] for k in ('app_id', 'app_name', 'app_version', 'device_name') if k in d}
                return (app_token, track_id, app_desc)

        except FileNotFoundError:
            return (None, None, None)

    def _get_base_url(self, host, port, freebox_api_version):
        """
        Returns base url for HTTPS requests
        :return:
        """
        abu = self.fbx_desc['api_base_url']
        return f'https://{host}:{port}{abu}{freebox_api_version}/'

    def _is_app_desc_valid(self, app_desc):
        """
        Check validity of the application descriptor
        """
        return all(k in app_desc for k in ('app_id', 'app_name', 'app_version', 'device_name'))
