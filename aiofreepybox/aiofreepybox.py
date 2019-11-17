import aiohttp
import asyncio
import base64
import bz2
import ipaddress
import json
import logging
import os
import socket
import ssl
from typing import Any, Dict, List, Optional, Tuple, Union
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
_APP_DESC = {
    "app_id": "aiofpbx",
    "app_name": "aiofreepybox",
    "app_version": aiofreepybox.__version__,
    "device_name": socket.gethostname(),
}
_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Db file default location
_DB_FILENAME = ".db"
_DB_FILE = os.path.join(_DATA_DIR, _DB_FILENAME)

# App defaults
_DEFAULT_API_VERSION = "v6"
_DEFAULT_CERT = "freebox_certificates.pem"
_DEFAULT_DEVICE_NAME = "Freebox Server"
_DEFAULT_HOST = "mafreebox.freebox.fr"
_DEFAULT_HTTP_PORT = "80"
_DEFAULT_HTTPS_PORT = "443"
_DEFAULT_SSL = True
_DEFAULT_TIMEOUT = 10
_DEFAULT_UNKNOWN = "None"
_LOGGER = logging.getLogger(__name__)

# Token file default location
_TOKEN_FILENAME = ".app_auth"
_TOKEN_FILE = os.path.join(_DATA_DIR, _TOKEN_FILENAME)


class Freepybox:
    """
    This python library is implementing the freebox OS API.
    It handles the authentication process and provides a raw access
    to the freebox API in an asynchronous manner.

    app_desc : `dict` , optional
        , Default to _APP_DESC
    token_file : `str` , optional
        , Default to _TOKEN_FILE
    api_version : `str`, "server" or "v(1-7)" , optional
        , Default to _DEFAULT_API_VERSION
    timeout : `int` , optional
        , Default to _DEFAULT_TIMEOUT
    """

    def __init__(
        self,
        app_desc: Optional[Dict[str, str]] = None,
        token_file: Optional[str] = None,
        api_version: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> None:
        self.api_version: str = (
            api_version if api_version is not None else _DEFAULT_API_VERSION
        )
        self.app_desc: Dict[str, str] = app_desc if app_desc is not None else _APP_DESC
        self.timeout: int = timeout if timeout is not None else _DEFAULT_TIMEOUT
        self.token_file: str = token_file if token_file is not None else _TOKEN_FILE
        self._access: Optional[Access] = None
        self._fbx_db: Dict[str, Any] = {}
        self._fbx_uid: str = ""
        self._session: Optional[aiohttp.ClientSession] = None

    async def close(self) -> None:
        """
        Close the freebox session
        """

        if self._access is None or self._session.closed:  # type: ignore # noqa
            _LOGGER.warning(f"Closing but freebox is not connected")
            return

        await self._access.post("login/logout")
        await self._session.close()  # type: ignore # noqa
        await asyncio.sleep(0.250)

    async def discover(
        self, host_in: Optional[str] = None, port_in: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Discover a freebox on the network

        host : `str` , optional
            , Default to None
        port : `str` , optional
            , Default to None
        """

        if host_in and self._is_ipv6(host_in):
            raise ValueError(f"{host_in} : IPv6 is not supported")

        # Check session
        try:
            fbx_addict = await self._disc_check_session(
                self._disc_set_host_and_port(host_in, port_in)
            )
        except ValueError as err:
            return err.args[0]

        # Connect if session is closed
        if any(
            [
                self._session is None,
                not isinstance(self._session, aiohttp.ClientSession),
                (self._session and self._session.closed),
            ]
        ) and not await self._disc_connect(**(fbx_addict)):
            raise ValueError("Port closed")

        # Found freebox
        try:
            async with self._session.get(  # type: ignore # noqa
                f"http{fbx_addict['s']}://{fbx_addict['host']}:{fbx_addict['port']}/api_version",
                timeout=self.timeout,
            ) as r:
                if r.content_type != "application/json":
                    await self._disc_close_to_return()
                    raise ValueError("Invalid content type")
                fbx_desc = await r.json()
        except (ssl.SSLCertVerificationError, ValueError) as err:
            await self._disc_close_to_return()
            raise ValueError(err.args[0])

        fbx_device = fbx_desc.get("device_name", None)
        if fbx_device != _DEFAULT_DEVICE_NAME:
            await self._disc_close_to_return()
            raise ValueError(f"{fbx_device}: Wrong device")

        self._fbx_update_db(fbx_desc, fbx_addict)
        return fbx_desc

    async def get_permissions(self) -> Optional[dict]:
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
        return None

    async def open(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        uid: Optional[str] = None,
    ) -> None:
        """
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules

        host : `str` , optional
            , Default to `None`
        port : `str` , optional
            , Default to `None`
        uid : `str` , optional
            , Default to `None`
        """

        if not self._is_app_desc_valid(self.app_desc):
            raise InvalidTokenError("Invalid application descriptor")

        # Get API access
        if uid is None:
            uid = ""
            try:
                uid = await self._fbx_open_init(host, port)
            except NotOpenError:
                raise
        else:
            try:
                uid = await self._fbx_open_db(uid)
            except NotOpenError:
                raise

        try:
            self._access = await self._get_app_access(
                uid, self.token_file, self.app_desc, self.timeout
            )
        except AuthorizationError:
            raise

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

    def _check_api_version(self, fbx_api_version: str) -> str:
        """
        Check api version
        """

        # Set API version if needed
        api_version = None
        s_fbx_version = fbx_api_version.split(".")[0]
        s_default_api_version = _DEFAULT_API_VERSION[1:]
        if self.api_version == "server":
            api_version = f"v{s_fbx_version}"
        # Check user API version
        s_api_version = self.api_version[1:]
        if s_default_api_version < s_fbx_version and s_api_version == s_fbx_version:
            _LOGGER.warning(
                f"Using new API version {self.api_version}, results may vary."
            )
        elif 0 < int(s_api_version) and s_api_version < s_default_api_version:
            _LOGGER.warning(
                f"Using deprecated API version {self.api_version}, results may vary."
            )
        elif 1 > int(s_api_version) or s_api_version > s_fbx_version:
            _LOGGER.warning(
                "Freebox server does not support this API version ("
                f"{self.api_version}), resetting to {_DEFAULT_API_VERSION}."
            )
            api_version = _DEFAULT_API_VERSION

        if api_version is None:
            return self.api_version
        else:
            self.api_version = api_version
            return api_version

    async def _disc_check_session(self, fbx_addict: Dict[str, Any]) -> Dict[str, Any]:
        """Check discovery session"""

        if (
            self._session
            and not self._session.closed
            and self._session._connector._conns  # type: ignore # noqa
        ):
            c = list(self._session._connector._conns.keys())[0]  # type: ignore # noqa
            if (
                c.host == fbx_addict["host"]
                and c.port == int(fbx_addict["port"])
                and c.is_ssl == (not not fbx_addict["s"])
            ):
                raise ValueError(self._fbx_db[self._fbx_uid]["desc"])
            await self._disc_close_to_return()
            raise ValueError(
                await self.discover(fbx_addict["host"], fbx_addict["port"])
            )

        return fbx_addict

    async def _disc_close_to_return(self) -> None:
        """Close discovery session"""

        if self._session is not None and not self._session.closed:
            await self._session.close()
            await asyncio.sleep(0.250)

    async def _disc_connect(self, host: str, port: str, s: str) -> bool:
        """Connect for discovery"""

        if not self._fbx_ping_port(host, port):
            return False

        # Connect
        try:
            if s == "s":
                cert_path = os.path.join(os.path.dirname(__file__), _DEFAULT_CERT)
                ssl_ctx = ssl.create_default_context()
                ssl_ctx.load_verify_locations(cafile=cert_path)
                conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
            else:
                conn = aiohttp.TCPConnector()
            self._session = aiohttp.ClientSession(connector=conn)
        except ssl.SSLCertVerificationError:
            await self._disc_close_to_return()
            return False

        return True

    def _disc_set_host_and_port(
        self, host_in: Optional[str] = None, port_in: Optional[str] = None
    ) -> Dict[str, Any]:
        """Set discovery host and port"""

        host, port = (
            host_in if host_in else _DEFAULT_HOST,
            port_in if port_in else _DEFAULT_HTTP_PORT,
        )
        if not host_in and not port_in:
            port = _DEFAULT_HTTPS_PORT if _DEFAULT_SSL else port
        s = "s" if _DEFAULT_SSL and port != _DEFAULT_HTTP_PORT else ""

        del self, host_in, port_in
        return locals()

    async def _fbx_enum_conns(self, db: Dict[str, Any]) -> Dict[str, Any]:
        """Try freebox connections"""
        for i, conn in enumerate(db["conn"]):
            try:
                d = await self.discover(conn["host"], conn["port"])
            except ValueError:
                pass
            else:
                self._fbx_db[d["uid"]]["conf"]["cc"] = i
                break
        if not d:
            raise NotOpenError
        return d

    async def _fbx_open_init(
        self, host_in: Optional[str] = None, port_in: Optional[str] = None
    ) -> str:
        """Init freebox link for open"""

        host = None
        port = None
        try:
            fbx_desc = await self.discover(host_in, port_in)
            host, port = self._fbx_open_setup(fbx_desc, host_in, port_in)
        except ValueError as err:
            unk = _DEFAULT_UNKNOWN
            host, port = (
                next(v for v in [host_in, host, unk] if v),
                next(v for v in [port_in, port, unk] if v),
            )
            raise NotOpenError(
                f"{err.args[0]}: Cannot detect freebox at "
                f"{host}:{port}"
                ", please check your configuration."
            )
        d = await self._fbx_enum_conns(self._fbx_db[fbx_desc["uid"]])

        self._fbx_db[d["uid"]]["conf"]["api_version"] = self._check_api_version(
            self._fbx_db[d["uid"]]["desc"]["api_version"]
        )
        self._fbx_uid = d["uid"]
        return d["uid"]

    async def _fbx_open_db(self, uid: str) -> str:
        """Open freebox db"""

        db = self._readfile_fbx_db(_DB_FILE, uid)
        d: Dict[str, Any] = {}
        if db is None:
            try:
                d = await self.discover()
            except ValueError as err:
                raise NotOpenError(
                f"{err.args[0]}: Cannot detect freebox for uid: {uid}"
                ", please check your configuration."
                )
        else:
            self._fbx_db[uid] = db
            d = await self._fbx_enum_conns(db)
        if uid != d["uid"]:
            raise NotOpenError(
                f"Cannot detect freebox for uid: {uid}"
                ", please check your configuration."
                )
        self._fbx_db[d["uid"]]["conf"]["api_version"] = self._check_api_version(
            self._fbx_db[d["uid"]]["desc"]["api_version"]
        )
        self._fbx_uid = uid
        return uid

    def _fbx_open_setup(
        self,
        fbx_desc: Dict[str, Any],
        host: Optional[str] = None,
        port: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Setup host and port value for open"""

        if _DEFAULT_SSL and fbx_desc["https_available"]:
            host, port = (
                fbx_desc["api_domain"] if host is None or self._is_ipv4(host) else host,
                fbx_desc["https_port"]
                if port is None or port == _DEFAULT_HTTP_PORT
                else port,
            )
        else:
            host, port = (
                _DEFAULT_HOST if host is None else host,
                _DEFAULT_HTTP_PORT if port is None else port,
            )

        return host, port

    def _fbx_ping_port(self, host: str, port: str) -> bool:
        """Check if a port if open"""

        result = 0
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(_DEFAULT_TIMEOUT)
            result = sock.connect_ex((host, int(port)))
            sock.close()
        except socket.gaierror:
            result = 1
        finally:
            if result != 0:
                return False
            return True

    def _fbx_update_db(
        self, fbx_desc: Dict[str, Any], fbx_addict: Optional[Dict[str, Any]]
    ) -> None:

        uid: str = fbx_desc["uid"]
        try:
            fbx_data: List[Dict[str, Any]] = self._fbx_db[uid]["conn"]
        except KeyError:
            fbx_api_add = [
                {
                    "host": fbx_desc["api_domain"],
                    "port": fbx_desc["https_port"],
                    "s": "s" if fbx_desc["https_available"] else "",
                }
            ]
            fbx_conf = {"api_version": "", "cc": 0}
            fbx_entry = {uid: {"conn": fbx_api_add, "conf": fbx_conf, "desc": fbx_desc}}
            self._fbx_db.update(fbx_entry)
            fbx_data = self._fbx_db[uid]["conn"]
            if not self._readfile_fbx_db(_DB_FILE, uid):
                self._writefile_fbx_db(_DB_FILE, uid)

        finally:
            if fbx_addict is not None:
                for k in fbx_data:
                    if dict(k) == fbx_addict:
                        return
                fbx_data.append(fbx_addict)
                self._fbx_db[uid]["conn"] = fbx_data
                self._writefile_fbx_db(_DB_FILE, uid)

    async def _get_app_access(
        self,
        uid: str,
        token_file: str,
        app_desc: Dict[str, str],
        timeout: int = _DEFAULT_TIMEOUT,
    ) -> Access:
        """
        Returns an access object used for HTTP(S) requests.

        uid : `str`
        token_file : `str`
        app_desc : `dict`
        timeout : `int`
            , Default to _DEFAULT_TIMEOUT
        """

        # Read stored application token
        _LOGGER.debug("Reading application authorization file.")
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file, uid)

        # If no valid token is stored then request a token to freebox api - Only for LAN connection
        if app_token is None or file_app_desc != app_desc:
            _LOGGER.warning(
                "No valid authorization file found, requesting authorization."
            )

            # Get application token from the freebox
            app_token, track_id = await self._get_app_token(app_desc, uid, timeout)

            # Check the authorization status
            out_msg_flag = False
            status = None
            while status != "granted":
                status = await self._get_authorization_status(track_id, uid, timeout)

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
            tk_file = self._writefile_app_token(
                app_token, track_id, app_desc, token_file, uid
            )
            _LOGGER.info(f"Application token file was generated: {tk_file}.")

        # Create and return freebox http access module
        fbx_access = Access(
            self._session,
            self._get_db_base_url(uid),
            app_token,
            app_desc["app_id"],
            timeout,
        )
        return fbx_access

    async def _get_app_token(
        self, app_desc: Dict[str, str], uid: str, timeout: int = _DEFAULT_TIMEOUT
    ) -> Tuple[str, str]:
        """
        Get the application token from the freebox

        app_desc : `dict`
        uid : `str`
        timeout : `int`
            , Default to _DEFAULT_TIMEOUT

        Returns app_token, track_id
        """

        # Get authentification token
        url = urljoin(self._get_db_base_url(uid), "login/authorize/")
        data = json.dumps(app_desc)
        async with self._session.post(  # type: ignore # noqa
            url, data=data, timeout=timeout
        ) as r:
            resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get("success"):
            raise AuthorizationError(
                "Authorization failed (APIResponse: {}).".format(json.dumps(resp))
            )

        app_token, track_id = resp["result"]["app_token"], resp["result"]["track_id"]
        return app_token, track_id

    async def _get_authorization_status(
        self, track_id: str, uid: str, timeout: int = _DEFAULT_TIMEOUT
    ) -> str:
        """
        Get authorization status of the application token

        track_id : `str`
        uid : `str`
        timeout : `int`
            , Default to _DEFAULT_TIMEOUT

        Returns:
            unknown     the app_token is invalid or has been revoked
            pending     the user has not confirmed the authorization request yet
            timeout     the user did not confirmed the authorization within the given time
            granted     the app_token is valid and can be used to open a session
            denied      the user denied the authorization request
        """

        url = urljoin(self._get_db_base_url(uid), f"login/authorize/{track_id}")
        async with self._session.get(url, timeout=timeout) as r:  # type: ignore # noqa
            resp = await r.json()
            return resp["result"]["status"]

    def _get_db_base_url(self, uid: str, api: Optional[bool] = True) -> str:
        """
        Returns base url for HTTP(S) requests

        uid : `str`
        api : `bool` , optional
            , Default to `True`
        """

        abu = ""
        conn = self._fbx_db[uid]["conn"][(self._fbx_db[uid]["conf"]["cc"])]
        if api:
            abu = self._fbx_db[uid]["desc"]["api_base_url"]
            api_version = self._fbx_db[uid]["conf"]["api_version"]
            abu =  f"{abu}{api_version}/"
        return f"http{conn['s']}://{conn['host']}:{conn['port']}{abu}"

    def _is_app_desc_valid(self, app_desc: Dict[str, str]) -> bool:
        """
        Check validity of the application descriptor

        app_desc : `dict`
        """
        return all(
            k in app_desc for k in ("app_id", "app_name", "app_version", "device_name")
        )

    def _is_ipv4(self, ip_address: str) -> bool:
        """
        Check ip version for v4

        ip_address : `str`
        """

        try:
            ipaddress.IPv4Network(ip_address)
            return True
        except ValueError:
            return False

    def _is_ipv6(self, ip_address: str) -> bool:
        """
        Check ip version for v6

        ip_address : `str`
        """

        try:
            ipaddress.IPv6Network(ip_address)
            return True
        except ValueError:
            return False

    def _readfile_app_token(self, file: str, uid: str) -> Tuple[Any, Any, Any]:
        """
        Read the application token in the authentication file.

        file : `str`
        uid : `str`

        Returns app_token, track_id, app_desc
        """
        fname = file + "_" + base64.b64encode(uid.encode("utf-8")).decode("utf-8")

        try:
            with bz2.open(fname, "rt", encoding="utf-8") as zf:
                d = json.load(zf)
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

    def _readfile_fbx_db(self, file: str, uid: str) -> Optional[Dict[str, Any]]:
        """
        Read the freebox db in the db file.

        file : `str`
        uid : `str`

        Returns fbx_db
        """
        fname = file + "_" + base64.b64encode(uid.encode("utf-8")).decode("utf-8")

        try:
            with bz2.open(fname, "rt", encoding="utf-8") as zf:
                d = json.load(zf)
                return d
        except FileNotFoundError:
            return None

    def _writefile_app_token(
        self,
        app_token: str,
        track_id: str,
        app_desc: Dict[str, str],
        file: str,
        uid: str,
    ) -> str:
        """
        Store the application token in a _TOKEN_FILE file

        app_token : `str`
        track_id : `str`
        app_desc : `dict`
        file : `str`
        uid : `str`
        """

        d = {**app_desc, "app_token": app_token, "track_id": track_id}
        fname = file + "_" + base64.b64encode(uid.encode("utf-8")).decode("utf-8")
        with bz2.open(fname, "wt", encoding="utf-8") as zf:
            json.dump(d, zf)
        return fname

    def _writefile_fbx_db(self, file: str, uid: str) -> str:
        """
        Store the freebox db in a _DB_FILE file

        file : `str`
        uid : `str`
        """

        fname = file + "_" + base64.b64encode(uid.encode("utf-8")).decode("utf-8")
        with bz2.open(fname, "wt", encoding="utf-8") as zf:
            json.dump(self._fbx_db[uid], zf)
        return fname

    @property
    def fbx_desc(self) -> Optional[dict]:
        """Freebox API description."""
        return self._fbx_db[self._fbx_uid]["desc"]

    @property
    def fbx_api_url(self) -> Optional[str]:
        """Freebox api url."""
        return self._get_db_base_url(self._fbx_uid)

    @property
    def fbx_uid(self) -> Optional[str]:
        """Freebox uid."""
        return self._fbx_uid

    @property
    def fbx_url(self) -> Optional[str]:
        """Freebox url."""
        return self._get_db_base_url(self._fbx_uid, api=False)
