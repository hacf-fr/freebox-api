import asyncio
import json
import logging
import os
import socket
import ssl
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union
from urllib.parse import urljoin

from aiohttp import ClientSession
from aiohttp import TCPConnector

import freebox_api
from freebox_api.access import Access
from freebox_api.api.airmedia import Airmedia
from freebox_api.api.call import Call
from freebox_api.api.connection import Connection
from freebox_api.api.dhcp import Dhcp
from freebox_api.api.freeplug import Freeplug
from freebox_api.api.fs import Fs
from freebox_api.api.ftp import Ftp
from freebox_api.api.fw import Fw
from freebox_api.api.home import Home
from freebox_api.api.lan import Lan
from freebox_api.api.lcd import Lcd
from freebox_api.api.netshare import Netshare
from freebox_api.api.notifications import Notifications
from freebox_api.api.parental import Parental
from freebox_api.api.phone import Phone
from freebox_api.api.player import Player
from freebox_api.api.remote import Remote
from freebox_api.api.rrd import Rrd
from freebox_api.api.storage import Storage
from freebox_api.api.switch import Switch
from freebox_api.api.system import System
from freebox_api.api.tv import Tv
from freebox_api.api.upnpav import Upnpav
from freebox_api.api.upnpigd import Upnpigd
from freebox_api.api.wifi import Wifi
from freebox_api.exceptions import AuthorizationError
from freebox_api.exceptions import InvalidTokenError
from freebox_api.exceptions import NotOpenError

# Token file default location
DEFAULT_TOKEN_FILENAME = "app_auth"  # noqa S105
DEFAULT_TOKEN_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TOKEN_FILE = os.path.join(DEFAULT_TOKEN_DIRECTORY, DEFAULT_TOKEN_FILENAME)

# Default application descriptor
DEFAULT_APP_DESC: Dict[str, str] = {
    "app_id": "aiofpbx",
    "app_name": "freebox-api",
    "app_version": freebox_api.__version__,
    "device_name": socket.gethostname(),
}

logger = logging.getLogger(__name__)


class Freepybox:
    def __init__(
        self,
        app_desc: Dict[str, str] = DEFAULT_APP_DESC,
        token_file: str = DEFAULT_TOKEN_FILE,
        api_version: str = "v3",
        timeout: int = 10,
    ):
        self.app_desc: Dict[str, str] = app_desc
        self.token_file: str = token_file
        self.api_version: str = api_version
        self.timeout: int = timeout
        self._session: ClientSession
        self._access: Access

    async def open(self, host: str, port: str) -> None:
        """
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules
        """
        if not self._is_app_desc_valid(self.app_desc):
            raise InvalidTokenError("Invalid application descriptor")

        cert_path = os.path.join(os.path.dirname(__file__), "freebox_certificates.pem")
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_verify_locations(cafile=cert_path)

        conn = TCPConnector(ssl_context=ssl_ctx)
        self._session = ClientSession(connector=conn)

        self._access = await self._get_freebox_access(
            host, port, self.api_version, self.token_file, self.app_desc, self.timeout
        )

        # Instantiate freebox modules
        self.tv = Tv(self._access)
        self.system = System(self._access)
        self.dhcp = Dhcp(self._access)
        self.airmedia = Airmedia(self._access)
        self.player = Player(self._access)
        self.switch = Switch(self._access)
        self.lan = Lan(self._access)
        self.storage = Storage(self._access)
        self.lcd = Lcd(self._access)
        self.wifi = Wifi(self._access)
        self.phone = Phone(self._access)
        self.ftp = Ftp(self._access)
        self.fs = Fs(self._access)
        self.fw = Fw(self._access)
        self.freeplug = Freeplug(self._access)
        self.call = Call(self._access)
        self.connection = Connection(self._access)
        self.home = Home(self._access)
        self.parental = Parental(self._access)
        self.netshare = Netshare(self._access)
        self.notifications = Notifications(self._access)
        self.remote = Remote(self._access)
        self.rrd = Rrd(self._access)
        self.upnpav = Upnpav(self._access)
        self.upnpigd = Upnpigd(self._access)

    async def close(self) -> None:
        """
        Close the freebox session
        """
        if not self._access:
            raise NotOpenError("Freebox is not open")

        await self._access.post("login/logout")
        await self._session.close()

    async def get_permissions(self) -> Optional[Dict[str, bool]]:
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

    async def _get_freebox_access(
        self,
        host: str,
        port: str,
        api_version: str,
        token_file: str,
        app_desc: Dict[str, str],
        timeout: int = 10,
    ) -> Access:
        """
        Returns an access object used for HTTP requests.
        """

        base_url: str = self._get_base_url(host, port, api_version)

        # Read stored application token
        logger.info("Read application authorization file")
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file)

        # If no valid token is stored then request a token to freebox api -
        # Only for LAN connection
        if app_token is None or file_app_desc != app_desc:
            logger.info("No valid authorization file found")

            # Get application token from the freebox
            app_token, track_id = await self._get_app_token(base_url, app_desc, timeout)

            # Check the authorization status
            out_msg_flag = False
            status: Optional[str] = None
            while status != "granted":
                status = await self._get_authorization_status(
                    base_url, track_id, timeout
                )

                # denied status = authorization failed
                if status == "denied":
                    raise AuthorizationError(
                        "The app token is invalid or has been revoked"
                    )

                # Pending status : user must accept the app request on the freebox
                elif status == "pending":
                    if not out_msg_flag:
                        out_msg_flag = True
                        print("Please confirm the authentification on the freebox")
                    await asyncio.sleep(1)

                # timeout = authorization failed
                elif status == "timeout":
                    raise AuthorizationError("Authorization timed out")

            logger.info("Application authorization granted")

            # Store application token in file
            self._writefile_app_token(app_token, track_id, app_desc, token_file)
            logger.info("Application token file was generated: {0}".format(token_file))

        # Create freebox http access module
        fbx_access = Access(
            self._session, base_url, app_token, app_desc["app_id"], timeout
        )

        return fbx_access

    async def _get_authorization_status(
        self, base_url: str, track_id: int, timeout: int
    ) -> str:
        """
        Get authorization status of the application token

        Returns:
            unknown: the app_token is invalid or has been revoked
            pending: the user has not confirmed the authorization request yet
            timeout: the user did not confirmed the authorization within the given time
            granted: the app_token is valid and can be used to open a session
            denied: the user denied the authorization request
        """
        url = urljoin(base_url, f"login/authorize/{track_id}")
        resp = await self._session.get(url, timeout=timeout)
        resp_data = await resp.json()
        return str(resp_data["result"]["status"])

    async def _get_app_token(
        self, base_url: str, app_desc: Dict[str, str], timeout: int = 10
    ) -> Tuple[str, int]:
        """
        Get the application token from the freebox
        Returns (app_token, track_id)
        """
        # Get authentification token
        url = urljoin(base_url, "login/authorize/")
        data = json.dumps(app_desc)
        resp = await self._session.post(url, data=data, timeout=timeout)
        resp_data = await resp.json()

        # raise exception if resp.success != True
        if not resp_data.get("success"):
            raise AuthorizationError(
                "Authorization failed (APIResponse: {0})".format(json.dumps(resp_data))
            )

        app_token: str = resp_data["result"]["app_token"]
        track_id: int = resp_data["result"]["track_id"]

        return (app_token, track_id)

    def _writefile_app_token(
        self, app_token: str, track_id: int, app_desc: Dict[str, str], token_file: str
    ) -> None:
        """
        Store the application token in g_app_auth_file file
        """
        file_content: Dict[str, Union[str, int]] = {
            **app_desc,
            "app_token": app_token,
            "track_id": track_id,
        }

        with open(token_file, "w") as f:
            json.dump(file_content, f)

    def _readfile_app_token(
        self, token_file: str
    ) -> Union[Tuple[str, int, Dict[str, Any]], Tuple[None, None, None]]:
        """
        Read the application token in the authentication file.
        Returns (app_token, track_id, app_desc)
        """
        try:
            with open(token_file, "r") as f:
                d = json.load(f)
                app_token: str = d["app_token"]
                track_id: int = d["track_id"]
                app_desc: Dict[str, str] = {
                    k: d[k]
                    for k in ("app_id", "app_name", "app_version", "device_name")
                    if k in d
                }
                return (app_token, track_id, app_desc)

        except FileNotFoundError:
            return (None, None, None)

    def _get_base_url(self, host: str, port: str, api_version: str) -> str:
        """
        Returns base url for HTTPS requests
        """
        return f"https://{host}:{port}/api/{api_version}/"

    def _is_app_desc_valid(self, app_desc: Dict[str, str]) -> bool:
        """
        Check validity of the application descriptor
        """
        return all(
            k in app_desc for k in ("app_id", "app_name", "app_version", "device_name")
        )
