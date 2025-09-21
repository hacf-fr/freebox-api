"""Freebox API."""

import asyncio
import json
import logging
import socket
import ssl
import types
from typing import Dict, Optional, Self, Tuple, Type
from urllib.parse import urljoin

from aiohttp import ClientError, ClientSession, TCPConnector

from .access import Access
from .api.airmedia import Airmedia
from .api.call import Call
from .api.connection import Connection
from .api.dhcp import Dhcp
from .api.download import Download
from .api.freeplug import Freeplug
from .api.fs import Fs
from .api.ftp import Ftp
from .api.fw import Fw
from .api.home import Home
from .api.lan import Lan
from .api.lcd import Lcd
from .api.netshare import Netshare
from .api.notifications import Notifications
from .api.parental import Parental
from .api.phone import Phone
from .api.player import Player
from .api.remote import Remote
from .api.rrd import Rrd
from .api.storage import Storage
from .api.switch import Switch
from .api.system import System
from .api.tv import Tv
from .api.upnpav import Upnpav
from .api.upnpigd import Upnpigd
from .api.wifi import Wifi
from .constants import FREEBOX_CA
from .exceptions import (
    AuthorizationError,
    HttpRequestError,
    NotOpenError,
)

# Constants
DEFAULT_APP_ID = "aiofpbx"
DEFAULT_APP_NAME = "freebox-api"
DEFAULT_HOSTNAME = "mafreebox.freebox.fr"
DEFAULT_PORT = 443
DEFAULT_TIMEOUT = 10
DEFAULT_API = "latest"
DEFAULT_DEVICE_NAME = socket.gethostname()
DEFAULT_VERSION = "1.0"

logger = logging.getLogger(__name__)


class Freepybox:
    """Freebox."""

    def __init__(
        self,
        host: str = DEFAULT_HOSTNAME,
        port: int = DEFAULT_PORT,
        *,
        app_id: str = DEFAULT_APP_ID,
        app_name: str = DEFAULT_APP_NAME,
        app_version: str = DEFAULT_VERSION,
        device_name: str = DEFAULT_DEVICE_NAME,
        api_version: str = DEFAULT_API,
        timeout: int = DEFAULT_TIMEOUT,
        verify_ssl: bool = True,
    ) -> None:
        self.app_id = app_id
        self.api_version = api_version
        self._timeout = timeout
        self.verify_ssl = verify_ssl

        self._session: ClientSession
        self._access: Access

        self.base_url = f"https://{host}:{port}/api/{api_version}/"
        self.app_desc = {
            "app_id": app_id,
            "app_name": app_name,
            "app_version": app_version,
            "device_name": device_name,
        }

        # Define modules
        self.tv: Tv
        self.system: System
        self.dhcp: Dhcp
        self.airmedia: Airmedia
        self.player: Player
        self.switch: Switch
        self.lan: Lan
        self.storage: Storage
        self.lcd: Lcd
        self.wifi: Wifi
        self.phone: Phone
        self.ftp: Ftp
        self.fs: Fs
        self.fw: Fw
        self.freeplug: Freeplug
        self.call: Call
        self.connection: Connection
        self.download: Download
        self.home: Home
        self.parental: Parental
        self.netshare: Netshare
        self.notifications: Notifications
        self.remote: Remote
        self.rrd: Rrd
        self.upnpav: Upnpav
        self.upnpigd: Upnpigd

    async def open(self, app_token: str) -> None:
        """
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules
        """
        await self._async_create_session()

        self._access = await self._get_access(app_token)

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
        self.download = Download(self._access)
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

    async def register_app(self) -> str | None:
        """Register freebox app."""
        await self._async_create_session()

        out_msg_flag = False
        status = None

        app_token, track_id = await self._get_app_token()

        # Track authorization progress
        while status != "granted":
            url = urljoin(self.base_url, f"login/authorize/{track_id}")
            try:
                async with asyncio.timeout(self._timeout):
                    resp = await self._session.request("get", url)
                    resp.raise_for_status()
                    resp_data = await resp.json()

            except ClientError as error:
                raise HttpRequestError(
                    "Error occurred while communicating with Freebox."
                ) from error

            if "result" not in resp_data:
                raise AuthorizationError(f"Response unknown ({resp_data})")

            if "status" not in resp_data["result"]:
                raise AuthorizationError(f"status not found ({resp_data})")

            status = str(resp_data["result"]["status"])

            # denied status = authorization failed
            if status == "denied":
                raise AuthorizationError("The app token is invalid or has been revoked")

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

        return app_token

    async def _async_create_session(self) -> None:
        """Create session."""
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_verify_locations(cadata=FREEBOX_CA)
        conn = (
            TCPConnector(ssl_context=ssl_ctx)
            if self.verify_ssl
            else TCPConnector(verify_ssl=self.verify_ssl)
        )
        self._session = ClientSession(connector=conn)

    async def _get_access(self, app_token: str) -> Access:
        """
        Returns an access object used for HTTP requests.
        """

        # Create freebox http access module
        return Access(
            self._session, self.base_url, app_token, self.app_id, self._timeout
        )

    async def _get_app_token(self) -> Tuple[str, int]:
        """
        Get the application token from the freebox
        Returns (app_token, track_id)
        """
        try:
            async with asyncio.timeout(self._timeout):
                url = urljoin(self.base_url, "login/authorize/")
                resp = await self._session.request("post", url, json=self.app_desc)

            resp.raise_for_status()
            resp_data = await resp.json()
        except ClientError as error:
            raise HttpRequestError(
                f"Error occurred while communicating with Freebox. ({error})"
            ) from error

        # raise exception if resp.success != True
        if "success" not in resp_data:
            raise AuthorizationError(
                f"Authorization failed (APIResponse: {json.dumps(resp_data)})"
            )

        return (
            resp_data["result"].get("app_token"),
            resp_data["result"].get("track_id"),
        )

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> bool:
        """Async exit."""
        await self.close()

    async def __aenter__(self) -> Self:
        """Context Manager."""
        return self
