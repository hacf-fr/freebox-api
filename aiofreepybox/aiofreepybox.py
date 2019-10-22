import aiohttp
import asyncio
import ipaddress
import json
import logging
import os
import socket
import ssl
from urllib.parse import urljoin

import aiofreepybox
from aiofreepybox.exceptions import (
    AuthorizationError,
    HttpRequestError,
    InsufficientPermissionsError,
    InvalidTokenError,
    NotOpenError,
)
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

# Default application descriptor
APP_DESC = {
    "app_id": "aiofpbx",
    "app_name": "aiofreepybox",
    "app_version": aiofreepybox.__version__,
    "device_name": socket.gethostname(),
}

# Token file default location
TOKEN_FILENAME = "app_auth"
TOKEN_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(TOKEN_DIR, TOKEN_FILENAME)

# App defaults
_DEFAULT_API_VERSION = "v6"
_DEFAULT_CERT = "freebox_certificates.pem"
_DEFAULT_HOST = "mafreebox.freebox.fr"
_DEFAULT_HTTP_PORT = "80"
_DEFAULT_HTTPS_PORT = "443"
_DEFAULT_SSL = True
_DEFAULT_TIMEOUT = 10

_LOGGER = logging.getLogger(__name__)


class Freepybox:
    """
    This python library is implementing the freebox OS API.
    It handles the authentication process and provides a raw access to the freebox API in an asynchronous manner.

    app_desc : `dict`
        , Default to APP_DESC
    token_file : `str`
        , Default to TOKEN_FILE
    api_version : `str`, "server" or "v(1-7)"
        , Default to _DEFAULT_API_VERSION
    timeout : `int`
        , Default to _DEFAULT_TIMEOUT
    """

    def __init__(self, app_desc=None, token_file=None, api_version=None, timeout=None):
        self.api_version = (
            api_version if api_version is not None else _DEFAULT_API_VERSION
        )
        self.app_desc = app_desc if app_desc is not None else APP_DESC
        self.fbx_desc = None
        self.fbx_url = ""
        self.timeout = timeout if timeout is not None else _DEFAULT_TIMEOUT
        self.token_file = token_file if token_file is not None else TOKEN_FILE
        self._access = None
        self._session = None

    async def open(self, host=None, port=None):
        """
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules

        host : `str`
            , Default to `None`
        port : `str`
            , Default to `None`
        """

        if not self._is_app_desc_valid(self.app_desc):
            raise InvalidTokenError("Invalid application descriptor")

        host, port = await self._check_and_validate_parameters(host, port)

        # Get API access
        self._access = await self._get_app_access(
            host, port, self.api_version, self.token_file, self.app_desc, self.timeout
        )

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

        if self._access is None or self._session.closed:
            _LOGGER.warning(f"Closing but freebox is not connected")
            return

        await self._access.post("login/logout")
        await self._session.close()
        await asyncio.sleep(0.250)

    async def discover(self, default_host=None, default_port=None):
        """
        Discover a freebox on the network

        default_host : `str`
            , Default to None
        default_port : `str`
            , Default to None
        """

        # Setup host and port
        if default_host is None:
            default_host = _DEFAULT_HOST
        elif self._is_ipv4(default_host) and default_port is None:
            default_port = _DEFAULT_HTTP_PORT
        elif self._is_ipv6(default_host):
            _LOGGER.error(f"{default_host} : IPv6 is not supported")
            return None

        default_port = (
            _DEFAULT_HTTPS_PORT
            if default_port is None and _DEFAULT_SSL
            else default_port
            if _DEFAULT_SSL
            else _DEFAULT_HTTP_PORT
        )
        s = "" if default_port == _DEFAULT_HTTP_PORT or not _DEFAULT_SSL else "s"

        # Check session
        if (
            self.fbx_desc is not None
            and self._session is not None
            and not self._session.closed
        ):
            conns = list(self._session._connector._conns.keys())[0]
            if default_host != conns.host or default_port != conns.port:
                self.fbx_desc = None
                await self._session.close()
                await asyncio.sleep(0.250)
                return await self.discover(default_host, default_port)
            else:
                return self.fbx_desc

        # Try to connect
        if (
            self._session is None
            or not isinstance(self._session, aiohttp.ClientSession)
            or self._session.closed
        ):

            # Checking host and port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((default_host, int(default_port)))
            if result != 0:
                if default_port != _DEFAULT_HTTP_PORT:
                    return await self.discover(default_host, _DEFAULT_HTTP_PORT)
                else:
                    return None
            sock.close()

            try:
                if s == "s":
                    cert_path = os.path.join(os.path.dirname(__file__), _DEFAULT_CERT)
                    ssl_ctx = ssl.create_default_context()
                    ssl_ctx.load_verify_locations(cafile=cert_path)
                    conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
                else:
                    conn = aiohttp.TCPConnector()

                self._session = aiohttp.ClientSession(connector=conn)
            except aiohttp.client_exceptions.ClientConnectorError or aiohttp.client_exceptions.ClientConnectorCertificateError or ssl.SSLCertVerificationError:
                return None

        # Found freebox
        try:
            r = await self._session.get(
                f"http{s}://{default_host}:{default_port}/api_version",
                timeout=self.timeout,
            )
            self.fbx_desc = await r.json()
        except aiohttp.client_exceptions.ClientResponseError:
            raise HttpRequestError(
                f"A network error occurred while reading from the freebox at {default_host}:{default_port}"
            )
        return self.fbx_desc

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

    async def _check_and_validate_parameters(self, target_host, target_port):
        """
        Validate host and port

        target_host : `str`
        target_port : `str`
        """

        # Discover
        if await self.discover(target_host, target_port) is None:
            if self._session is not None:
                await self._session.close()
                await asyncio.sleep(0.250)
            unknown = "?"
            raise NotOpenError(
                f"Cannot detect freebox at {target_host if target_host is not None else unknown}:{target_port if target_port is not None else unknown}, please check your configuration."
            )

        # Setting host and port
        host = (
            self.fbx_desc["api_domain"]
            if (
                (target_host is None or target_port == _DEFAULT_HTTP_PORT)
                or (target_host is not None and target_port is None)
            )
            and _DEFAULT_SSL
            else _DEFAULT_HOST
            if target_host is None and not _DEFAULT_SSL
            else target_host
        )
        port = (
            self.fbx_desc["https_port"]
            if (target_port is None or target_port == _DEFAULT_HTTP_PORT)
            and _DEFAULT_SSL
            else target_port
            if _DEFAULT_SSL
            else _DEFAULT_HTTP_PORT
        )

        await self.discover(host, port)
        self._check_api_version()
        self.fbx_url = self._get_base_url(host, port)

        return host, port

    def _check_api_version(self):
        """
        Check api version
        """

        # Set API version if needed
        server_version = self.fbx_desc["api_version"].split(".")[0]
        short_api_version_target = _DEFAULT_API_VERSION[1:]
        if self.api_version == "server":
            self.api_version = f"v{server_version}"

        # Check user API version
        short_api_version = self.api_version[1:]
        if (
            short_api_version_target < server_version
            and short_api_version == server_version
        ):
            _LOGGER.warning(
                f"Using new API version {self.api_version}, results may vary."
            )
        elif (
            short_api_version < short_api_version_target and int(short_api_version) > 0
        ):
            _LOGGER.warning(
                f"Using deprecated API version {self.api_version}, results may vary."
            )
        elif short_api_version > server_version or int(short_api_version) < 1:
            _LOGGER.warning(
                f"Freebox server does not support this API version ({self.api_version}), resetting to {_DEFAULT_API_VERSION}."
            )
            self.api_version = _DEFAULT_API_VERSION

    async def _get_app_access(
        self, host, port, api_version, token_file, app_desc, timeout=_DEFAULT_TIMEOUT
    ):
        """
        Returns an access object used for HTTP(S) requests.

        host : `str`
        port : `str`
        api_version : `str`
        token_file : `str`
        app_desc : `dict`
        timeout : `int`
        """

        base_url = self._get_base_url(host, port, api_version)

        # Read stored application token
        _LOGGER.debug("Reading application authorization file.")
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file)

        # If no valid token is stored then request a token to freebox api - Only for LAN connection
        if app_token is None or file_app_desc != app_desc:
            _LOGGER.warning(
                "No valid authorization file found, requesting authorization."
            )

            # Get application token from the freebox
            app_token, track_id = await self._get_app_token(base_url, app_desc, timeout)

            # Check the authorization status
            out_msg_flag = False
            status = None
            while status != "granted":
                status = await self._get_authorization_status(
                    base_url, track_id, timeout
                )

                # denied status = authorization failed
                if status == "denied":
                    raise AuthorizationError(
                        "The app token is invalid or has been revoked."
                    )

                # Pending status : user must accept the app request on the freebox
                elif status == "pending":
                    if not out_msg_flag:
                        out_msg_flag = True
                        print("Please confirm the authentification on the freebox.")
                    await asyncio.sleep(1)

                # timeout = authorization failed
                elif status == "timeout":
                    raise AuthorizationError("Authorization timed out.")

            _LOGGER.info("Application authorization granted.")

            # Store application token in file
            self._writefile_app_token(app_token, track_id, app_desc, token_file)
            _LOGGER.info(f"Application token file was generated: {token_file}.")

        # Create and return freebox http access module
        fbx_access = Access(
            self._session, base_url, app_token, app_desc["app_id"], timeout
        )
        return fbx_access

    async def _get_app_token(self, base_url, app_desc, timeout=_DEFAULT_TIMEOUT):
        """
        Get the application token from the freebox

        base_url : `str`
        app_desc : `dict`
        timeout : `int`

        Returns app_token, track_id
        """

        # Get authentification token
        url = urljoin(base_url, "login/authorize/")
        data = json.dumps(app_desc)
        r = await self._session.post(url, data=data, timeout=timeout)
        resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get("success"):
            raise AuthorizationError(
                "Authorization failed (APIResponse: {}).".format(json.dumps(resp))
            )

        app_token = resp["result"]["app_token"]
        track_id = resp["result"]["track_id"]

        return app_token, track_id

    async def _get_authorization_status(
        self, base_url, track_id, timeout=_DEFAULT_TIMEOUT
    ):
        """
        Get authorization status of the application token

        base_url : `str`
        track_id : `str`
        timeout : `int`

        Returns:
            unknown 	the app_token is invalid or has been revoked
            pending 	the user has not confirmed the authorization request yet
            timeout 	the user did not confirmed the authorization within the given time
            granted 	the app_token is valid and can be used to open a session
            denied 	    the user denied the authorization request
        """

        url = urljoin(base_url, f"login/authorize/{track_id}")
        r = await self._session.get(url, timeout=timeout)
        resp = await r.json()
        return resp["result"]["status"]

    def _get_base_url(self, host, port, freebox_api_version=None):
        """
        Returns base url for HTTP(S) requests

        host : `str`
        port : `str`
        freebox_api_version : `str`
            , Default to `None`
        """

        s = "s" if _DEFAULT_SSL else ""
        if freebox_api_version is None:
            return f"http{s}://{host}:{port}"
        else:
            abu = self.fbx_desc["api_base_url"]
            return f"http{s}://{host}:{port}{abu}{freebox_api_version}/"

    def _is_app_desc_valid(self, app_desc):
        """
        Check validity of the application descriptor

        app_desc : `dict`
        """

        return all(
            k in app_desc for k in ("app_id", "app_name", "app_version", "device_name")
        )

    def _is_ipv4(self, ip_address):
        """
        Check ip version for v4

        ip_address : `str`
        """
        try:
            ipaddress.IPv4Network(ip_address)
            return True
        except ValueError:
            return False

    def _is_ipv6(self, ip_address):
        """
        Check ip version for v6

        ip_address : `str`
        """
        try:
            ipaddress.IPv6Network(ip_address)
            return True
        except ValueError:
            return False

    def _readfile_app_token(self, file):
        """
        Read the application token in the authentication file.

        file : `str`

        Returns app_token, track_id, app_desc
        """

        try:
            with open(file, "r") as f:
                d = json.load(f)
                app_token = d["app_token"]
                track_id = d["track_id"]
                app_desc = {
                    k: d[k]
                    for k in ("app_id", "app_name", "app_version", "device_name")
                    if k in d
                }
                return app_token, track_id, app_desc

        except FileNotFoundError:
            return None, None, None

    def _writefile_app_token(self, app_token, track_id, app_desc, file):
        """
        Store the application token in a TOKEN_FILE file

        app_token : `str`
        track_id : `str`
        app_desc : `dict`
        file : `str`
        """

        d = {**app_desc, "app_token": app_token, "track_id": track_id}

        with open(file, "w") as f:
            json.dump(d, f)
